
import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

from optparse import OptionParser as OP

#host = "127.0.1.1"
#port = 8000

parser = OP(usage="usage: %python filename -t <server> -p <port> ")

parser.add_option("-t",type="string",
        help = "IP address of the server",
        dest ='server_ip')

parser.add_option("-p",type="int",
        help = "Port number of the server",
        dest = 'port')
(options, args ) = parser.parse_args()

if (options.server_ip == 0) | (options.port == 0):
    print(parser.usage)

host = options.server_ip
port = options.port

Cserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM )
Cserver.connect((host, port))

#Tell server that connection is OK
Cserver.sendall("Client: OK")

#Receive public key string from server
server_string = Cserver.recv(2048)
                         
#Remove extra characters
server_string = server_string.replace("public_key=", '')
server_string = server_string.replace("\r\n", '')

#Convert string to key
server_public_key = RSA.importKey(server_string)
key_s = PKCS1_OAEP.new(server_public_key)  #Breaking the vulnerability of RSA

#Encrypt message and send to server
message = raw_input("Stream >  \n")
encrypted = server_public_key.encrypt(message, 2048)
Cserver.sendall("encrypted_message=" + str(encrypted))

#Server's response
server_response = Cserver.recv(1024)
server_response = server_response.replace("\r\n", '')

if server_response == "server: OK":
    print "Server decrypted message successfully"

#Tell server to finish connection
Cserver.sendall("Quit")
print(Cserver.recv(1024)) #Quit server response
Cserver.close()
