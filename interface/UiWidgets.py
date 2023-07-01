import sys
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import *
from service import AccountManager, ConnectService, DataManager

accMan = AccountManager.accMan
conService = ConnectService.conService
setMan = DataManager.setMan

language = setMan.currentLanguage

class MainLogin(QtWidgets.QWidget):
    def __init__(self, w = 0, h = 0):
        super().__init__()
        self.setWindowTitle(language.getLanString("login_window"))

        self.resize(w, h)
        self.setMinimumSize(w, h)
        self.setMaximumSize(w, h)

        self.manageWindow = None
        self.testConnectionDialog()

        self.defaultLayout = QtWidgets.QGridLayout(self)
        #self.defaultLayout.setContentsMargins(10,10,10,10)

        self.menuLayout = QtWidgets.QGridLayout()
        self.topGrid = QtWidgets.QGridLayout()

        self.accountDropdown = QtWidgets.QComboBox(self)
        self.loadAccountList()

        self.managerOpen = QtWidgets.QPushButton(self)
        self.managerOpen.setText(language.getLanString("manage_button"))
        self.managerOpen.clicked.connect(self.openManageScreen)

        self.statusLabel = QtWidgets.QLabel(self)
        self.statusBar = QtWidgets.QProgressBar(self)
        self.statusBar.setMaximum(100)

        self.userImage = QtWidgets.QLabel(self)

        self.loginButton = QtWidgets.QPushButton(self)
        self.loginButton.setText(language.getLanString("login_button"))
        self.loginButton.clicked.connect(self.loginConnection)

        self.exitButton = QtWidgets.QPushButton(self)
        self.exitButton.setText(language.getLanString("exit_button"))
        self.exitButton.clicked.connect(self.quitApp)

        self.statusLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.statusLabel.setText(language.getLanString("choose_acc"))
        self.statusLabel.setMaximumSize(w, 20)
        self.statusBar.setTextVisible(False)

        self.userImage.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.userImage.setMaximumSize(120, 120)
        self.loadUserPicture()

        self.topGrid.addWidget(self.accountDropdown, 0, 0, 1, 2)
        self.topGrid.addWidget(self.managerOpen, 0, 2)
        self.topGrid.addWidget(self.statusLabel, 1, 0, 1, 0)
        self.topGrid.addWidget(self.statusBar, 2, 0, 1, 0)

        self.menuLayout.addLayout(self.topGrid, 1, 0, 1, 0)
        self.menuLayout.addWidget(self.loginButton, 2, 0, 1, 2)
        self.menuLayout.addWidget(self.exitButton, 2, 2)

        self.defaultLayout.addWidget(self.userImage, 0, 0)
        self.defaultLayout.addLayout(self.menuLayout, 0, 1)

    def testConnectionDialog(self):
        value = conService.testInternet()
        if value is True:
            return
        else:
            QtWidgets.QApplication.beep()
            self.netDialog = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.Critical, 
                                                    language.getLanString("nettest_failtitle"), language.getLanString("nettest_fail"), 
                                                    QtWidgets.QMessageBox.StandardButton.Ok)
            self.netDialog.show()
    
    def loginConnection(self):
        account = accMan.allAccounts[self.accountDropdown.currentIndex()]
        dataReturn = conService.startConnection(account.username, account.passw, self)
        if dataReturn == 200:
            self.statusLabel.setText(language.getLanString("done"))
            self.statusBar.setValue(100)
            self.netDialog = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.Information, 
                                                    language.getLanString("loginyes_title"), language.getLanString("loginyes_exit"), 
                                                    QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            self.netDialog.accepted.connect(QCoreApplication.quit)
            self.netDialog.show()
        else:
            self.generateConError(language.getLanString("login_no"))
        

    def generateConError(self, errorC : str):
        QtWidgets.QApplication.beep()
        self.statusLabel.setText(language.getLanString("label_login_error"))
        self.statusBar.setValue(0)
        self.netDialog = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.Critical,
                                                    language.getLanString("loginfail_title"), language.getLanString("loginfail_desc") + errorC, 
                                                    QtWidgets.QMessageBox.StandardButton.Ok)
        self.netDialog.show()
    
    def loadAccountList(self):
        self.accountDropdown.clear()
        for i in accMan.allAccounts:
            self.accountDropdown.addItem(accMan.strFormatAcc(i), i)

    def loadUserPicture(self):
        userPixmap = QtGui.QPixmap('img/userpic.png')
        self.userImage.setScaledContents(True)
        self.userImage.setPixmap(userPixmap)

    def openManageScreen(self):
        self.manageWindow = ManageScreen(self, 300, 250)
        self.manageWindow.loadAccountList()
        self.manageWindow.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.manageWindow.show()
        print("Opened up manager...")
    
    def quitApp(self):
        QtWidgets.QApplication.beep()
        self.exitDialog = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.Question, 
                                                language.getLanString("exit_title"), language.getLanString("exit_confirm"), 
                                                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        self.exitDialog.accepted.connect(QCoreApplication.quit)
        self.exitDialog.show()

class ManageScreen(QtWidgets.QWidget):
    # TO DO: CHANGE THIS TO A QWIDGET. THE REASON OF THIS IS BECAUSE QTABWIDGETS GET CREATED IN A WEIRD WAY AND I HAVE TO ADD BUTTONS OUTSIDE THE TABWIDGET LOL!
    def __init__(self, parent, w = 0, h = 0):
        super().__init__()
        self.setWindowTitle(language.getLanString("manage_wintitle"))
        self.setWindowFlags(Qt.WindowType.Dialog)

        self.mainParent = parent

        self.resize(w, h)
        self.setMinimumSize(w, h)
        self.setMaximumSize(w, h)

        self.tabWidget = QtWidgets.QTabWidget(self)
        self.mainLayout = QtWidgets.QGridLayout(self)

        self.closeButton = QtWidgets.QPushButton(language.getLanString("close_button"), self)
        self.closeButton.clicked.connect(self.saveSettings)
        self.mainLayout.addWidget(self.tabWidget, 0, 0, 1, 0)
        self.mainLayout.addWidget(self.closeButton, 1, 3, 1, 2)

        self.initializeAccountTab()
        self.initializeSettingsTab()

        self.tabWidget.addTab(self.accountWidget, language.getLanString("accounts_tab"))
        self.tabWidget.addTab(self.settingsWidget, language.getLanString("settings_tab"))

    def initializeSettingsTab(self):
        self.settingsWidget = QtWidgets.QWidget(self)
        self.setWidGrid = QtWidgets.QGridLayout(self.settingsWidget)
        self.accWidGrid.setContentsMargins(15,15,15,15)

        self.languageLay = QtWidgets.QGridLayout()
        self.languageDropdown = QtWidgets.QComboBox(self.settingsWidget)

        self.languageLabel = QtWidgets.QLabel(self.settingsWidget)
        self.languageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.languageLabel.setMaximumWidth(80)
        self.languageLabel.setText(language.getLanString("language_label"))

        self.loadSettings()

        self.languageLay.addWidget(self.languageLabel, 0, 0)
        self.languageLay.addWidget(self.languageDropdown, 0, 1, 1, -1)

        self.setWidGrid.addLayout(self.languageLay, 0, 0)

    def loadSettings(self):
        #TODO: I have no other customizable settings yet. Planning to do something related to themes here.
        for i in setMan.allLanguages:
            self.languageDropdown.addItem(i.languageName, i)
        self.languageDropdown.setCurrentIndex(setMan.allOptions["curlang"])
        self.languageDropdown.currentIndexChanged.connect(self.changeLanguage)
    
    def changeLanguage(self):
        setMan.allOptions["curlang"] = self.languageDropdown.currentIndex()

    def saveSettings(self):
        setMan.saveDefaultSettings()
        self.close()
    
    def initializeAccountTab(self):
        self.accountWidget = QtWidgets.QWidget(self)
        #self.accountWidget.resize(tabw, tabh)
        #self.accountWidget.setMinimumSize(tabw, tabh)
        #self.accountWidget.setMaximumSize(tabw, tabh)

        self.accWidGrid = QtWidgets.QGridLayout(self.accountWidget)
        self.accWidGrid.setContentsMargins(15,15,15,15)

        self.saveAccLay = QtWidgets.QHBoxLayout()
        self.accListLay = QtWidgets.QGridLayout()

        self.accountList = QtWidgets.QComboBox(self.accountWidget)
        self.accountList.currentIndexChanged.connect(self.loadToBox)
        self.addButton = QtWidgets.QPushButton("+", self.accountWidget)
        self.addButton.setMaximumSize(40, 40)
        self.addButton.clicked.connect(self.addAccountTo)

        self.removeButton = QtWidgets.QPushButton("-", self.accountWidget)
        self.removeButton.setMaximumSize(40, 40)
        self.removeButton.clicked.connect(self.showRemoveDialog)

        self.emailBox = QtWidgets.QLineEdit(self.accountWidget)
        self.emailBox.setPlaceholderText(language.getLanString("email_label"))

        self.userNameBox = QtWidgets.QLineEdit(self.accountWidget)
        self.userNameBox.setPlaceholderText(language.getLanString("user_label"))
        
        self.passwordBox = QtWidgets.QLineEdit(self.accountWidget)
        self.passwordBox.setPlaceholderText(language.getLanString("pass_label"))
        self.passwordBox.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        self.showPassButton = QtWidgets.QPushButton(language.getLanString("show"), self.accountWidget)
        self.showPassButton.pressed.connect(self.showPassClick)
        self.showPassButton.released.connect(self.showPassRelease)

        self.updateAccButton = QtWidgets.QPushButton(language.getLanString("updateacc"), self.accountWidget)
        self.updateAccButton.clicked.connect(self.showUpdateDialog)
        self.updateAccButton.setEnabled(False)

        self.saveAccButton = QtWidgets.QPushButton(language.getLanString("addacc"), self.accountWidget)
        self.saveAccButton.clicked.connect(self.showAddDialog)
        self.saveAccButton.setEnabled(False)

        self.saveAccLay.addWidget(self.updateAccButton)
        self.saveAccLay.addWidget(self.saveAccButton)

        self.accListLay.addWidget(self.accountList, 0, 0)
        self.accListLay.addWidget(self.addButton, 0, 1)
        self.accListLay.addWidget(self.removeButton, 0, 2)

        self.accWidGrid.addLayout(self.accListLay, 0, 0, 1, 0)

        self.accWidGrid.addWidget(self.emailBox, 1, 0, 1, 0)
        self.accWidGrid.addWidget(self.userNameBox, 2, 0, 1, 0)
        self.accWidGrid.addWidget(self.passwordBox, 3, 0, 1, 3)
        self.accWidGrid.addWidget(self.showPassButton, 3, 3)

        self.accWidGrid.addLayout(self.saveAccLay, 4, 0, 1, 0)

        self.filledInfoT = QTimer(self.accountWidget)
        self.filledInfoT.timeout.connect(self.verifyForm)
        self.filledInfoT.setInterval(100)
        self.filledInfoT.start()

    def verifyForm(self):
        if self.passwordBox.text() != "" and self.userNameBox.text() != "" and self.emailBox.text() != "":
            self.updateAccButton.setEnabled(True)
            if self.accountList.currentText() == language.getLanString("new_acc"): 
                self.saveAccButton.setEnabled(True)
                self.updateAccButton.setEnabled(False)
            else:
                self.saveAccButton.setEnabled(False)
        else:
            self.updateAccButton.setEnabled(False)
            self.saveAccButton.setEnabled(False)

        if self.accountList.count() < 2:
            self.removeButton.setEnabled(False)
        else:
            self.removeButton.setEnabled(True)

    def showPassClick(self):
        self.passwordBox.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)

    def showPassRelease(self):
        self.passwordBox.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
    
    def loadToBox(self):
        if self.accountList.currentText() == language.getLanString("new_acc"):
            return

        account = accMan.allAccounts[self.accountList.currentIndex()]
        self.emailBox.setText(account.email)
        self.userNameBox.setText(account.username)
        self.passwordBox.setText(account.passw)

    def clearFormBoxes(self):
        self.emailBox.clear()
        self.userNameBox.clear()
        self.passwordBox.clear()
    
    def showUpdateDialog(self):
        QtWidgets.QApplication.beep()
        self.updateDialog = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.Question, 
                                                language.getLanString("updateacc"), language.getLanString("update_confirm"),
                                                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        self.updateDialog.accepted.connect(self.updateSelectedAcc)
        self.updateDialog.show()

    def showAddDialog(self):
        QtWidgets.QApplication.beep()
        self.updateDialog = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.Question, 
                                                language.getLanString("addacc"), language.getLanString("addacc_confirm"),
                                                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        self.updateDialog.accepted.connect(self.addSelectedAcc)
        self.updateDialog.show()

    def showRemoveDialog(self):
        QtWidgets.QApplication.beep()
        self.updateDialog = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.Question, 
                                                language.getLanString("removeacc"), language.getLanString("remove_confirm"), 
                                                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        self.updateDialog.accepted.connect(self.removeSelectedAcc)
        self.updateDialog.show()

    def addAccountTo(self):
        self.accountList.addItem(language.getLanString("new_acc"))
        self.accountList.setCurrentIndex(self.accountList.count() - 1)
        self.clearFormBoxes()

    def addSelectedAcc(self):
        accMan.allAccounts.append(AccountManager.UserAccount(self.emailBox.text(), self.userNameBox.text(), self.passwordBox.text()))
        accMan.exportToJSON()
        self.accountList.clear()
        self.loadAccountList()
        self.clearFormBoxes()
        self.mainParent.loadAccountList()
        self.accountList.setCurrentIndex(self.accountList.count() - 1)

    def removeSelectedAcc(self):
        accMan.allAccounts.remove(accMan.allAccounts[self.accountList.currentIndex()])
        accMan.exportToJSON()
        self.accountList.clear()
        self.loadAccountList()
        self.clearFormBoxes()
        self.mainParent.loadAccountList()
        QtWidgets.QApplication.beep()
        self.doneDialog = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.Information, 
                                                language.getLanString("removeacc"), language.getLanString("remove_done"), 
                                                QtWidgets.QMessageBox.StandardButton.Ok)
        self.doneDialog.show()
    
    def updateSelectedAcc(self):
        accMan.allAccounts[self.accountList.currentIndex()] = AccountManager.UserAccount(self.emailBox.text(), self.userNameBox.text(), self.passwordBox.text())
        accMan.exportToJSON()
        lastIdx = self.accountList.currentIndex()
        self.accountList.clear()
        self.loadAccountList()
        self.accountList.setCurrentIndex(lastIdx)
        self.mainParent.loadAccountList()
        QtWidgets.QApplication.beep()
        self.doneDialog = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.Information, 
                                                language.getLanString("updateacc"), language.getLanString("update_done"), 
                                                QtWidgets.QMessageBox.StandardButton.Ok)
        self.doneDialog.show()

    def loadAccountList(self):
        for i in accMan.allAccounts:
            self.accountList.addItem(accMan.strFormatAcc(i), i)