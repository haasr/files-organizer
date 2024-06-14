import logging

# For information about logging levels, see https://docs.python.org/3/library/logging.html#levels
LOG_LEVEL = (
    # logging.NOTSET
    # logging.DEBUG
    logging.INFO
    # logging.WARN
    # logging.ERROR
    # logging.CRITICAL
)

LOG_FILE_PATH = 'filesorganizer.log' # Log file will be written in working directory, unless a path prefix is used
LOG_FILE_MODE = 'a' # w -- write: will clear next time program is executed. a -- append: will add new log entries to the end


# DON'T INCLUDE TRAILING SLASHES

# Uncomment the path prefix of your OS (comment out the others):

# On Windows, you might have multiple drives with directories you want to monitor.
# PATH_PREFIX is just for convenience when constructing keys in DIRECTORIES_MAP.
# You can specify n directories on n different drives in DIRECTORIES_MAP.
PATH_PREFIX = (
    'C:/Users' # Windows
    # '/home'  # Most Unix
    # '/Users' # MacOS
)

# Your username:
USERNAME = 'Ryan'

# Mappings:
# Top-level keys = folders to scan for changes.
# Nested K,V pairs are to map the file type to the directory it should be moved into.
DIRECTORIES_MAP = {
    # Downloads
    f"{PATH_PREFIX}/{USERNAME}/Downloads": {
        f"audio": f"{PATH_PREFIX}/{USERNAME}/Downloads/Audio",
        f"citations": f"{PATH_PREFIX}/{USERNAME}/Downloads/Citations",
        f"executables": f"{PATH_PREFIX}/{USERNAME}/Downloads/Executables",
        f"images": f"{PATH_PREFIX}/{USERNAME}/Downloads/Images",
        f"pdfs": f"{PATH_PREFIX}/{USERNAME}/Downloads/PDFs",
        f"powerpoints": f"{PATH_PREFIX}/{USERNAME}/Downloads/PowerPoints",
        f"spreadsheets": f"{PATH_PREFIX}/{USERNAME}/Downloads/Spreadsheets",
        f"text_files": f"{PATH_PREFIX}/{USERNAME}/Downloads/Text_Files",
        f"videos": f"{PATH_PREFIX}/{USERNAME}/Downloads/Videos",
        f"word_documents": f"{PATH_PREFIX}/{USERNAME}/Downloads/Word_Documents",
    },


    # Most of the stuff on my desktop can just go to the Documents folder anyway
    f"{PATH_PREFIX}/{USERNAME}/Desktop": {
        # Keep images on my desktop. Normally I want them there for temp use to get my attention.
        f"pdfs": f"{PATH_PREFIX}/{USERNAME}/Documents/PDFs",
        f"powerpoints": f"{PATH_PREFIX}/{USERNAME}/Documents/PowerPoints",
        f"spreadsheets": f"{PATH_PREFIX}/{USERNAME}/Documents/Spreadsheets",
        # Keep text files there as well. Usually little notes for me.
        f"videos": f"{PATH_PREFIX}/{USERNAME}/Videos",
        f"word_documents": f"{PATH_PREFIX}/{USERNAME}/Documents/Word_Documents",
    },
}

# Order all ext's from more to less common for short-circuit eval
EXTENSIONS_MAP = {
    "audio":          [ '.mp3', '.wav', '.ogg', '.aac', '.aiff', '.m4a' ],
    "citations":      [ '.bib', '.enl', '.ris', ],
    "executables":    [ '.exe', '.msi', '.appimage', ],
    "images":         [ '.png', '.jpg', '.jpeg', '.gif', '.webp', '.heic', '.svg', '.ico', ],
    "pdfs":           [ '.pdf', ],
    "powerpoints":    [ '.ppt', '.pptx', ],
    "spreadsheets":   [ '.csv', '.xls', '.xlsx', '.xlsm', ], # xlsm are the ones with macros
    "text_files":     [ '.txt', '.text', ],
    "videos":         [ '.mp4', '.mov', '.mkv', '.avi', ],
    "word_documents": [ '.doc', '.docx', ],
}

OBSERVER_RECURSIVE = False
