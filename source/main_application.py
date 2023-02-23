"""Ice Climatology Tool Main Application

This is the main driver and is the script that should be run to launch the application. It currently needs to be run from directory it lives in.

Example:
    Run this program from the ``ice_climatology_tool`` directory using::

        $ python main_application.py

"""
import sys
from icemap_window import Window
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 16px;
        }
    ''')
    
    win = Window()
    win.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Exit')
