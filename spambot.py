"""AUTOSPAM FOR FUN ONLY"""

from subprocess import CompletedProcess
import pyautogui
import time
time.sleep(0.5)

def Register_AutoSpamInfo():
    while True:
        spamfile = open("spamtext.txt", "w")
        print("Welcome to Autospammer, for fun only. Use at your risks.")
        time.sleep(0.5)
        print("Made with Python_")
        time.sleep(1)
        Spam_Msg = str(input("What message would you like to spam?  Message : "))
        Spam_Times = int(input("How many times would you spam this message? Count : "))
        for i in range(Spam_Times):
            spamfile.write(Spam_Msg)
            spamfile.write("\n")
        print("SPAMMING STARTING IN 5 SECONDS! PLEASE PREPARE WELL!")
        time.sleep(5)
        break
    
 
Register_AutoSpamInfo()
   
spamfileRead = open("spamtext.txt", "r")
for msg in spamfileRead:
    pyautogui.typewrite(msg)
    pyautogui.press("enter")
print("SPAM COMPLETED")
pyautogui.typewrite("AUTOSPAM COMPLETED")
pyautogui.press("enter")
    
#TEST:testtesttest
