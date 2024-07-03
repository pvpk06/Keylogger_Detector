from tkinter import *
from PIL import ImageTk, Image
import tkinter.messagebox as tkMessageBox
import ctypes
import json
from subprocess import check_output
import os
import io, pyfiglet
from turtle import width
import PySimpleGUI as sg
import time, sys
from tqdm import tqdm

home = Tk()
home.title("Keylogger Detector")
directory = "./"
img = Image.open(directory+"/images/home.png")
img = ImageTk.PhotoImage(img)
panel = Label(home, image=img)
panel.pack(side="top", fill="both", expand="yes")
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
[w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
lt = [w, h]
a = str(lt[0]//2-425)
b= str(lt[1]//2-325)
home.geometry("850x650+"+a+"+"+b)
home.resizable(0,0)

def detectmain():
    os.system("cls")
    # Create a pop-up window 
    sg.theme('DarkPurple2')
    layout = [[sg.Text("Do you wish to scan the system? Press OK to continue")], [sg.Button("OK"), sg.Button("Cancel")]]
    window = sg.Window("Anti Keylogger Tool", layout)
    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user presses Cancel or closes window & runs the program if user presses the OK button
        if event == "OK":
            break
        else:
            if event == "Cancel" or event == sg.WIN_CLOSED:
                exit()
    window.close()
    class Process(object):
        def __init__(self, proc_info):
            print(proc_info)
            self.pid = proc_info[1]
            self.cmd = proc_info[0]
        def name(self):
            return '%s' % self.cmd
        def procid(self):
            return '%s' % self.pid
    # Create the action to be taken when a keylogger is identified
    def kill_logger(key_pid):
        result = tkMessageBox.askquestion("Keylogger Detector","Do you want to terminate this keylogger")
        if result == 'yes':
            os.system('taskkill /f /im ' + key_pid )
        else:
            pass      
    def get_process_list():
        process_list = []
        sub_process = str(check_output("tasklist", shell=True).decode())
        x = io.StringIO(sub_process)
        for line in x :
            line = line.split()
            if len(line) > 0:   
                 process_list.append(line)
        return process_list

    process_list = get_process_list()
    def loading():
        
        print ("Searching for KeyLoggers....")
        for i in tqdm (range (100),desc="Loading....", ascii=False, ncols=95):
            time.sleep(0.1)
        print("Scanning Completed.")
        
    loading()
    process_cmd = []
    process_pid = []

    for process in process_list:
        process_cmd.append(process[0])
        process_pid.append(process[1])
    l1 = open("ioc.json", "r")
    l1 = json.loads(l1.read())
    dict1 = l1
    record = 0
    flag = 1
    for x in process_cmd:
        for y in dict1:
            if (x.find(y['name']) > -1):
                tkMessageBox.showinfo("Output","KeyLogger Detected: \nThe following proccess may be a key logger: \n\n\t" + process_pid[
                    record] + " ---> " + x)
                kill_logger(x)
                flag = 0
        record += 1

    if (flag):
        tkMessageBox.showinfo("Output","\nNo Keylogger Detected")


def Exit():
    global home
    result = tkMessageBox.askquestion(
        "Keylogger Detector", 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        home.destroy()
        exit()
    else:
        pass
    
Button(home,font=("",15,''),fg="white",activebackground="#a81728"
       ,bg="#a81728",bd=0,highlightthickness=0,width=25
       ,text="Detect Keylogger",command=detectmain
       ).place(x=5,y=142)

Button(home,font=("",15,''),fg="white",activebackground="#a81728"
       ,bg="#a81728",bd=0,highlightthickness=0,width=25
       ,text="Exit",command=Exit
       ).place(x=571,y=142)
home.mainloop()
