import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESKTOP_DIR = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

APP_NAME = 'Local Printer Print'
ICON_PATH = BASE_DIR + '/assets/checks.png'

TARGET_PRINTER_NAMES = [
    'IN_PRINTER',
    'OUT_PRINTER',
    'ICB_PRINTER',
    'YTO_PRINTER',
    'SF_PRINTER'
]
