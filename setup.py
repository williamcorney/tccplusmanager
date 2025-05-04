from setuptools import setup

APP = ['main.py']
DATA_FILES = ['tccplus']
OPTIONS = {
         'iconfile': 'icon.icns',  # Reference the icon file directly
    'packages': ['PyQt6'],
    'plist': {
        'CFBundleName': 'TCC Permission Manager',
        'CFBundleIdentifier': 'com.yourname.tccmanager',
        'CFBundleVersion': '0.1'
    },
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
