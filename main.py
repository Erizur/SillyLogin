import sys
from interface import UiWidgets
from service import ConnectService, AccountManager, DataManager
from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication([])

    loginUi = UiWidgets.MainLogin(400,150)
    loginUi.show()

    try:
        #load style if there's one.
        with open("stylesheet.qss", "r") as f:
            _style = f.read()
            app.setStyleSheet(_style)
    except:
        print("Not loading an userstyle.")

    sys.exit(app.exec())