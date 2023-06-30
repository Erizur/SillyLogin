import sys
from interface import UiWidgets
from service import ConnectService, AccountManager, DataManager
from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication([])

    loginUi = UiWidgets.MainLogin(400,150)
    loginUi.show()

    sys.exit(app.exec())