#!S:\PythonPro\education\Trello\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'pip==21.2.4','console_scripts','pip'
__requires__ = 'pip==21.2.4'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('pip==21.2.4', 'console_scripts', 'pip')()
    )
