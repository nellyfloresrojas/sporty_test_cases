import os

APPIUM_PORT = int(os.getenv('APPIUM_PORT', 4723))
WAIT_TIME = int(os.getenv('WAIT_TIME', 12))