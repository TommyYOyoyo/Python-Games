from pynput.mouse import Controller
from pynput.mouse import Button as mouseButton
from pynput.keyboard import Listener
from tkinter import *
import time
import random
import threading

mouse = Controller()

isSwitch = False
pressedKey = "/"
hk = None

def on_press(key):
    global pressedKey
    print(type(pressedKey), type(hk))
    pressedKey = str(key)
    print('PYNPUT:', pressedKey, "TKINTER:", hk)
    if pressedKey == hk:
        print("Activated")
        start()
    print('{0} pressed'.format(
        key))
    pressLabel.config(text=key)
        
def on_release(key):
    print('{0} release'.format(
        key))
        
def pressing():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    
def start():
    if startBtn['text'] == "Start":
        startBtn.config(text="AutoClicking...")
        timingLabel.config(text="seconds before the next click(random choosing)")
        repeatTLabel.config(text="repeat times")
        autoclick()

def autoclick():
    try:
        t1 = float(timing.get())
        t2 = float(timing2.get())
        repeat = int(repeatTimes.get())
        print(t1, t2, repeat)
        
        for i in range(repeat):
            print("Clicking")
            if t1 != t2:
                randnum = random.uniform(t1, t2)
                print(randnum)
            else:
                randnum = t1
            mouse.click(mouseButton.left)
            time.sleep(randnum)
    except ValueError:
        repeatTLabel.config(text="Please enter a number!")
        timingLabel.config(text="Please enter a number!")
    startBtn.config(text="Start")

def hotkeySwitch():
    global isSwitch
    isSwitch = True
    shortcutBtn.config(text="press a key", state=DISABLED)
    if isSwitch:
        win.bind("<KeyPress>", hotkeyChange)
    
def hotkeyChange(event):
    global isSwitch
    global hk
    if isSwitch:
        if event.keysym == hk:
            hk = hk
        else:
            hk = event.keysym
        hk = "'"+hk+"'"
        shortcutBtn.config(text=hk, state=NORMAL)
        isSwitch = False
        print("hotkey:"+hk)

pressingThread = threading.Thread(target=pressing, args=(), daemon=True)#lambda event: pressLabel.config(text=event.keysym))
pressingThread.start()

win = Tk()

win.geometry("650x280")

win.title("TommyClicker")

startBtn = Button(win,
                text="Start",
                height=10,
                width=15,
                command=start)

pressLabel = Label(win, text="None", font=("Helvetica", 10))
pressLabel.pack()

startBtn.pack()

frame = Frame(win)
frame.pack()

frame2 = Frame(win)
frame.pack()

repeatTimes = Entry(frame, width=10)
repeatTLabel = Label(frame, text="repeat times")

timing = Entry(win, width=10)
timingLabel = Label(win, text="seconds before the next click(random choosing)")
toLabel = Label(win, text="to")
timing2 = Entry(win, width=10)

shortcutLabel = Label(frame, text="shortcut(PLEASE DONT ENTER A SPECIAL CHARACTER):")
shortcutBtn = Button(frame, text="choose shortcut/hotkey", command=hotkeySwitch, width=15)

repeatTimes.grid(row=0, column=0, columnspan=2)
repeatTLabel.grid(row=0, column=4)

shortcutLabel.grid(row=2, column=1, columnspan=2)
shortcutBtn.grid(row=2, column=4)

timing.pack(side=LEFT)
toLabel.pack(side=LEFT)
timing2.pack(side=LEFT)
timingLabel.pack()
    
win.mainloop()
