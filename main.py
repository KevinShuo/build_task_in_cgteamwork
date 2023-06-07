import importlib
from src.views import mainWindow
from src import config

importlib.reload(mainWindow)
importlib.reload(config)

if __name__ == '__main__':
    if config.DEBUG:
        mainWindow.build_UI()
