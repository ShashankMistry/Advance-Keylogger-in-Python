from cryptography.fernet import Fernet

file_path = "C:\\Users\\shash\\PycharmProjects\\Keylogger\\Project"
extend = "\\"
file_merge = file_path + extend

key = Fernet.generate_key()
file = open(file_merge + 'key.key', 'wb')
file.write(key)
file.close()

# current_key_is = "hpcGE5hdtMeYyrM9BW3p7FsWc_VZ-0sE8Fb5WxKpY_Y="
