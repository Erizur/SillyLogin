# 2023 AM_ERIZUR
# This is literally just for the SillyLogin example
#
# DO NOT use this since it barely does anything
# so you can implement your OWN service!

import requests, random
from PySide6.QtCore import QThread, QObject, Signal
from service import DataManager

language = DataManager.setMan.currentLanguage

class ConnectionService(DataManager.OutputClass):
    def testInternet(self):
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
            state.statusLabel.setText(language.getLanString("attempting"))
            state.statusBar.setValue(50)
            print(ran)
            if ran > 1:
                c = requests.get('https://httpbin.org/basic-auth/' + user + '/' + passw, auth=(user, passw))
            else:
                c = requests.get('https://httpbin.org/basic-auth/' + user + '/' + passw, auth=('nuh', 'uh'))
            state.statusLabel.setText(language.getLanString("verificating"))
            state.statusBar.setValue(80)
            print(c.status_code)
            return c.status_code
        except Exception as err:
            state.generateConError(str(err))
        finally:
            c.close()

conService = ConnectionService()


    

