# 2023 AM_ERIZUR
# This is literally just for the SillyLogin example
#
# DO NOT use this since it barely does anything
# so you can implement your OWN service!

import requests, random, base64
from PySide6.QtNetwork import *
from PySide6.QtCore import *
from service import DataManager

language = DataManager.setMan.currentLanguage

class ConnectionService(DataManager.OutputClass):
    def __init__(self):
        self.netManager = QNetworkAccessManager()

    def testInternet(self):
        #This request is using the requests synchronous library only because its a test connection and i don't want the user to do anything in that moment.
        try:
            requests.head('https://8.8.8.8', timeout=5) #pinging google and only the head so i don't run out of resources by loading the html
            return True
        except:
            return False
                 
        
    def startConnection(self, user : str, passw : str, state):
        ran = random.randint(0, 5)
        state.statusLabel.setText(language.getLanString("waiting"))
        state.statusBar.setValue(20)
        try:
            r = QNetworkRequest(QUrl('https://httpbin.org/basic-auth/' + user + "/" + passw))
            state.statusLabel.setText(language.getLanString("attempting"))
            state.statusBar.setValue(50)
            basicdata = user + ":" + passw
            if ran > 1:
                r.setRawHeader(b'Authorization', b'Basic ' + base64.b64encode(basicdata.encode()))
                ans = self.netManager.get(r)
                loadLoop = QEventLoop()
                ans.finished.connect(loadLoop.quit)
                loadLoop.exec_()
            else: # same request, no headers!
                ans = self.netManager.get(r)
                loadLoop = QEventLoop()
                ans.finished.connect(loadLoop.quit)
                loadLoop.exec_()
            return ans.attribute(QNetworkRequest.Attribute.HttpStatusCodeAttribute)
        except Exception as err:
            state.generateConError(str(err))

conService = ConnectionService()


    

