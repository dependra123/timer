import tkinter as tk
from cryptography.fernet import Fernet
from tkinter import filedialog
import os
import threading
import ctypes
import sys
import queue
from pathlib import Path



folder_mode = False
fpath = ""


def filemode():

    fpath = filedialog.askopenfile()
    print ("folder mode")
    return fpath
def foldermode():
  
    fpath = filedialog.askdirectory()
    print ("folder mode")
    return fpath

# Create a window
root = tk.Tk()
root.title("Encryptor")
root.geometry("300x200")

fpath = filemode()




key = Fernet.generate_key()

#save the key to a file
with open("key.key", "wb") as key_file:
    key_file.write(key)
    key_file.close()

#make a key with fernet and save it in a file
fernet = Fernet(key) 

#make a function that converts data to binary
def convert_to_binary(data):
    return (data).encode("utf-8")

#make a fu
def encrypt(file_path):
    file_fpath = file_path.name

    #use Path.read_bytes to read from file_fpath
    data = Path(file_fpath).read_bytes()
    print ("read")
    print ("encrypting")
    #encrypt the file with the key
    encrypted_file = fernet.encrypt(data)
    print ("encrypted")
    Path(file_fpath).write_bytes(encrypted_file)
    print ("encrypted file saved")
    
    #rename the file to .encrypted
    os.rename(file_fpath, file_fpath + ".encrypted")
    
    



folders = queue.Queue()
print(fpath)
if os.path.isdir(fpath.name):
    folders.put(fpath)
    
    #for each file in the folder, encrypt it
    for file in os.listdir(folders.get()):
        print("opening file: " + file)
        #check if folder is empty
        if not len(os.listdir(fpath.name)) == 0:
            if os.path.isdir(fpath.name + "\\" + file):
                folders.put(fpath.name + "\\" + file)
            else:
                with open("file_names.txt", "a") as file_names:
                    file_names.write(fpath.name + "\\" + file + ".ENCRYPTED" + "\n")
                    file_names.close()
                encrypt(fpath.name + "\\" + file)
                print (file + "encrypted")

else:
    encrypt(fpath)
    with open("file_names.txt", "a") as file_names:
        file_names.write(fpath.name + "\n")
        file_names.close()
    print (fpath.name + "encrypted") 

    print(fpath.name + "removed")
#wait for all threads to finish
"""for thread in threading.enumerate():
    if thread is not threading.current_thread():
        thread.join()"""
#close the window
root.destroy()
#start a new thread to delete the Fpath.name



