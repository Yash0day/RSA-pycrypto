import socket
from Crypto.PublicKey import RSA
from Crypto import Random
import commands
from Crypto.Cipher import PKCS1_OAEP
import sys
import ast


def generate_key():
    random_value = Random.new().read
    generate_key.private_key = RSA.generate(1024,random_value)
    generate_key.public_key = generate_key.private_key.publickey().exportKey()


def main():
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host = socket.gethostbyname("Boyka")
    port = 8000
    encrypt_str = "encrypted_message="

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    sock.bind((host,port))
    sock.listen(4)
    print("Starting Server...")
    (c, (addr,ip)) = sock.accept()

    print("Got Connections from >  " , str(addr))
    generate_key()

    while 1:
        data = c.recv(1024)
        data = data.replace("\r\n", '')

        if data == "Client: OK":
            c.send("public_key=" + generate_key.public_key + "\n")
            print("Public key sent to client")

        elif encrypt_str in data :
            data = data.replace(encrypt_str, '')
            print("Received Encrypted Message \n" + str(data))

            encrypted = eval(data)
            decrypted = generate_key.private_key.decrypt(encrypted)

            c.send("server: OK")
            print("decrypted message : " + decrypted)
            sys.exit()
        elif data == "QUIT" :
            print("Client asked to close the server : ")
            break
        elif len(data) == 0:
            break 
    

    c.send("Server stopped\n")
    sock.close()


if __name__ == "__main__":
    main()
