from configparser import Interpolation
from dataclasses import field
from logging import exception
import sys
from msilib.schema import tables
import time
from tkinter import SOLID
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
import _thread
from PyQt5 import QtCore, QtGui, QtWidgets
import csv
import pandas as pd
#  ---------Global List of Musers---------------
global acsendingElements, pandasData
acsendingElements = False
MuserList = []
dataFilePath = "CombineData.csv"
CredentialFilePath = "userData.csv"
pandasData = ""

class Muser():
    userName = ""
    userPassword = ""
    searches = []

    def __init__(self, userName, userPassword):
        self.userName = userName
        self.userPassword = userPassword

    def saveIntoTheCSV(self, filePath):
        df = pd.read_csv(filePath)  # open and read the file

        # get the user,password column
        userNames = df['UserEmail'].values.tolist()
        userPassword = df['Password'].values.tolist()

        userNames.append(self.userName)  # append the new user and password
        userPassword.append(self.userPassword)
        # create new dataFrame
        df = pd.DataFrame({
            'UserEmail': userNames,
            'Password': userPassword
        })
        df.to_csv(filePath)  # save the data frame into the file

    def IsPresent(self, filePath):
        df = pd.read_csv(filePath)  # open and read the file

        # get the user,password column
        userNames = df['UserEmail'].values.tolist()
        userPasswords = df['Password'].values.tolist()
        print(self.userName, self.userPassword)
        for i in range(len(userNames)):
            if self.userName == userNames[i] and self.userPassword == userPasswords[i]:
                return True
        return False
# ---------------------------------------------------------------------------------------------------------------




# ------------SignInUI class-------------

class signInUI(QDialog):
    def __init__(self):
        super(signInUI, self).__init__()
        loadUi("UI/SignInDialog.ui", self)
        self.setWindowTitle('Sign In')
        self.loginBtn.clicked.connect(self.IsUser)
        self.signupBtn.clicked.connect(self.showSignUpWindow)

    def IsUser(self):
        newUserName = self.emailTxt.text()
        newUserPassword = self.passTxt.text()
        logInUser = Muser(newUserName, newUserPassword)
        if (logInUser.IsPresent(CredentialFilePath)):
            self.close()
            pandasData = pd.read_csv(dataFilePath)
            self.window1 = showPopUpMessageBox('Done','Login Suceeseful')
            self.window1.show()
        else:
            msg = QMessageBox()
            self.passTxt.setText('')
            msg.setWindowTitle("New to app")
            msg.setText("You are not registered! kindly SignUp")
            msg.setIcon(QMessageBox.Information)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()

    def showSignUpWindow(self):
        self.close()
        self.window1 = signUpUI()
        self.window1.show()

#  ------------SignUpUI class----------
class signUpUI(QDialog):
    def __init__(self):
        super(signUpUI, self).__init__()
        loadUi("UI/SignUpDialog.ui", self)
        self.setWindowTitle('Sign Up')
        self.registerBtn.clicked.connect(self.AddUser)

    def AddUser(self):
        userName = self.EmailTxt.text()
        userPassword = self.passwordTxt.text()
        # check the Both Password & confirm password is Same
        if (userPassword == self.passwordTxt_2.text()):
            newUser = Muser(userName, userPassword)
            if (newUser.IsPresent(CredentialFilePath)):
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("Account is Already Exist")
                msg.setIcon(QMessageBox.Critical)
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec()
            else:
                newUser.saveIntoTheCSV(CredentialFilePath)
            self.close()
            self.window1 = signInUI()
            self.window1.show()
            self.window1.setWindowTitle('E-commerce Sign In')

        else:
            showErrorMessageBox("Both Passwords doesn't match")


# -----------------------------------------------------------------------------------------------------------------
#                                       Helping Functions




def IsNonStringFieldConvertIntoInt(arr):
    try:
        for i in arr:
            grabageVariable = int(i)
        return True
    except:
        return False


def showErrorMessageBox(message):
    msg = QMessageBox()
    msg.setWindowTitle("Error")
    msg.setText(message)
    msg.setIcon(QMessageBox.Critical)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec()


def showPopUpMessageBox(title, message):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(message)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec()


def checkNonEmptyLimit(arr):
    for i in arr:
        if (i == ' '):
            return True
    return False


def removeStartingSpaceInString(text):
    text = list(text)
    lengthoftext = len(text)
    i = 0
    while (i < lengthoftext):
        if (text[i] == ' '):
            text.pop(i)
            lengthoftext = len(text)
        else:
            break
        i += 1
    return ''.join(text)


def applyLimitRangeInt(no, starting, ending):
    if (no > starting and no < ending):
        return True
    else:
        return False


def convert2DarrayInPandas(arr):
    data = {
        'index': [0]*len(arr[1]),
        'Name': arr[0],
        'Type': arr[1],
        'Price': arr[2],
        'Disc': arr[3],
        'Sold': arr[4],
        'Reviews': arr[5],
        'Ratings': arr[6]
    }
    data = pd.DataFrame(data)
    return data


def convertPandasInto2Darray(df, fieldNames):
    arr = []
    for i in fieldNames:
        arr.append(df[i].values.tolist())
    return arr


def fillComboBox(comboBox, datalist):
    comboBox.clear()
    comboBox.addItems(datalist)
    comboBox.setCurrentIndex(0)




# -----------------------------------------------------------------------------------------------------------------
# -------Main Driver Code----------
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window1 = signInUI()
    window1.setWindowFlags(QtCore.Qt.WindowCloseButtonHint |
                           QtCore.Qt.WindowMinimizeButtonHint)
    window1.setWindowTitle('Sign In')
    window1.show()
    sys.exit(app.exec_())