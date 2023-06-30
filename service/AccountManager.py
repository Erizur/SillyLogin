import json, os
from service import DataManager

class UserAccount():
    def __init__(self, email, username, passw):
        self.email = email
        self.username = username
        self.passw = passw

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

class AccountManager(DataManager.OutputClass):
    def __init__(self):
        self.sillyEncrypt = DataManager.SillyEncrypt()
        self.allAccounts = [UserAccount("test@test.com", "Test User", "haha")]
        self.readAccountData()

    def strFormatAcc(self, account : UserAccount):
        return account.username + " (" + account.email + ")"

    def readAccountData(self):
        try:
            json_data = json.loads(self.sillyEncrypt.decryptAndLoad('accs'))
            self.allAccounts.clear()
            for i in json_data:
                data = json.loads(json.loads(i))
                self.allAccounts.append(UserAccount(data["email"], data["username"], data["passw"]))
        except:
            self.log("No JSON data detected. Will NOT load previous accounts (if any).")

    def exportToJSON(self):
        finalDump = []

        for i in self.allAccounts:
            dump = json.dumps(i.toJSON())
            finalDump.append(dump)
        
        jsonDump = json.dumps(finalDump)
        self.sillyEncrypt.encryptFile(jsonDump, 'accs')

accMan = AccountManager()

