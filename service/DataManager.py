from cryptography import fernet
from pathlib import Path
import platformdirs, os, json

#Class that allows log and error handling from others.
class OutputClass:
    def log(self, msg):
        print(self.__class__.__name__ + ": " + msg)

# ENCRYPTION USED FOR THE EXAMPLE.
# CHANGE ENCRYPTION METHOD IF POSSIBLE, YOU CAN GET YOUR ACCOUNTS EXPOSED!
class SillyEncrypt(OutputClass):
    def __init__(self):
        # Modify the datapath if required.
        self.dataPath = str(platformdirs.user_data_path(appauthor="AM_Erizur", appname="SillyLogin", ensure_exists=True)) + "/"
        self.keyExists = False
        
        self.verifyKeyfile()
        if self.keyExists == False:
            self.generateKeyfile()
        
    def generateKeyfile(self):
        if self.keyExists == True:
            return
        keyfile = fernet.Fernet.generate_key()
        with open(self.dataPath + 'skey.abc', 'wb') as keydata:
            keydata.write(keyfile)
    
    def verifyKeyfile(self):
        try:
            if(os.path.isfile(self.dataPath + 'skey.abc')):
                self.keyExists = True
                with open(self.dataPath + 'skey.abc', 'rb') as keydata:
                    self.keyData = keydata.read()
        except:
            self.log("Key does not exist... Creating new one.")

    def encryptFile(self, filedata, encrypt_name):
        f = fernet.Fernet(self.keyData)
        data = f.encrypt(filedata.encode())

        with open (self.dataPath + encrypt_name, 'wb') as file:
            file.write(data)
    
    def decryptAndLoad(self, file_name):
        f = fernet.Fernet(self.keyData)

        with open (self.dataPath + file_name, 'rb') as file:
            encrypted_file = file.read()

        decrypted_file = f.decrypt(encrypted_file)
        return decrypted_file.decode()
    
class Language():
    def __init__(self, languageName : str, jsonData):
        self.languageName = languageName.capitalize()
        self.json_data = jsonData
    
    def getLanString(self, string):
        try:
            return self.json_data[string]
        except:
            return "Translation error."

class SettingsManager(OutputClass):
    def __init__(self):
        self.settingsExist = False
        self.currentLanguage = Language("None", None)
        self.allLanguages = []
        self.allOptions = {}
        self.loadDefaultSettings()

    # def loadDefaultSettings(self):
    #     try:
    #         dire = 'translations' #languages directory.
    #         translations = Path(dire).glob('*.json')
    #         for translation in translations:
    #             landata = open(translation, 'r')
    #             lanjson = json.loads(landata.read())
    #             self.allLanguages.append(Language(lanjson["language_name"], lanjson["language_strings"]))
            
    #         with open ('settings.json', 'wb') as file:
    #             json_data = json.loads(file.read())
    #         self.allOptions.clear()
    #         for i in json_data:
    #             data = json.loads(json.loads(i))
    #             self.allOptions.append(Option(data["optionname"], data["value"]))
    #     except:
    #         self.log("No JSON data detected. Will NOT load previous settings (if any).")
        
    def loadDefaultSettings(self):
        dire = 'translations' #languages directory.
        translations = Path(dire).glob('*.json')
        self.allLanguages.clear()
        for translation in translations:
            landata = open(translation, 'r')
            lanjson = json.loads(landata.read())
            self.allLanguages.append(Language(lanjson["language_name"], lanjson["language_strings"]))
            landata.close()
                    
        with open ('settings.json', 'r') as file:
            json_data = json.loads(file.read())
            self.allOptions.clear()
            self.allOptions = json_data["options"]
        
        self.currentLanguage = self.allLanguages[self.allOptions["curlang"]]
    
    def saveDefaultSettings(self):
        dump = {
            "options": self.allOptions
        }
        with open('settings.json', 'wt') as file:
            file.write(json.dumps(dump, indent=4))

setMan = SettingsManager()
