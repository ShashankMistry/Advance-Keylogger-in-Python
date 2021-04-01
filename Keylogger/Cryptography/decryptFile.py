from cryptography.fernet import Fernet

key = "hpcGE5hdtMeYyrM9BW3p7FsWc_VZ-0sE8Fb5WxKpY_Y="

encrypted_keys_information = "system_files_keys.txt"
encrypted_system_information = "system_files_info.txt"
encrypted_clipboard_information = "system_files_text.txt"
file_path = "C:\\Users\\shash\\PycharmProjects\\Keylogger\\Project"
extend = "\\"
file_merge = file_path + extend

encrypted_files = [file_merge + encrypted_system_information, file_merge + encrypted_clipboard_information, file_merge + encrypted_keys_information]
count = 0

for decrypting_files in encrypted_files:
    with open(encrypted_files[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)
    with open("decryption" + str(count) + ".txt", 'ab') as f:
        if count == 0:
            f.truncate(0)
            f.write(decrypted)
        else:
            f.write(decrypted)

    count += 1
