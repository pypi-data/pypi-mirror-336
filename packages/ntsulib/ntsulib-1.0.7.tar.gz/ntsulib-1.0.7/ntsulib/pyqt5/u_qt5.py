import ctypes
from typing import Union
from PyQt5 import QtCore
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import QWidget, QMainWindow


def get_center_screenGeometry(window: Union[QWidget,QMainWindow], width: int = None, height: int = None) -> Union[QRect,None]:
    screens = QGuiApplication.screens()
    screen_geometry = [screen.availableGeometry() for screen in screens]
    screen_rect = screen_geometry[0].united(screen_geometry[1:]) if len(screen_geometry) > 1 else screen_geometry[0]
    if window and not width and not height:
        rec: QRect = window.geometry()
        m_width = (screen_rect.width() - rec.width()) / 2 + screen_rect.left()
        m_height = (screen_rect.height() - rec.height()) / 2 + screen_rect.top()
        return QRect(int(m_width), int(m_height), rec.width(), rec.height())

    elif window and width and height:
        m_width = (screen_rect.width() - width) / 2 + screen_rect.left()
        m_height = (screen_rect.height() - height) / 2 + screen_rect.top()
        return QRect(int(m_width), int(m_height), width, height)
    return None

def setAntiScreenShot(window:int | QWidget):
    if isinstance(window, int):
        ctypes.windll.user32.SetWindowDisplayAffinity(window, 0x11)
    elif isinstance(window, QWidget):
        ctypes.windll.user32.SetWindowDisplayAffinity(int(window.winId()), 0x11)