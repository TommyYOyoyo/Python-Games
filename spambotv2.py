"""AUTOSPAM FOR FUN ONLY, V2(LITE)"""

from subprocess import CompletedProcess
import pyautogui
import time

pyautogui.PAUSE = 0.01

def Register_AutoSpamInfo():
    print("Welcome to AutospammerV2(LITE), for fun only. Use at your risks.")
    time.sleep(0.5)
    print("Made with Python_")
    time.sleep(1)
     Spam_Msg = str(input("What message would you like to spam?  Message : "))
     Spam_Times = int(input("How many times would you spam this message? Count : "))
     print("SPAMMING STARTING IN 5 SECONDS! PLEASE PREPARE WELL!")
     time.sleep(5)
     for i in range(Spam_Times):
         pyautogui.typewrite(Spam_Msg, interval=0.001)
         pyautogui.press("enter")
     print("AUTOSPAM COMPLETED")
     pyautogui.typewrite("AUTOSPAM COMPLETED")
     pyautogui.press("enter")
    
 
Register_AutoSpamInfo()

#TEST:testtesttesttest

#V2 (LITE VERSION)
