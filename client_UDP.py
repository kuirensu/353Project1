from __future__ import print_function
import socket               # Import socket module
import argparse             # Import argparse module
import atexit

#Part 1 Done

#Required arguments specification
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("-s", "--serverIP", help="indicate the server IP address", required=True)
parser.add_argument("-p", "--port", type=int, help="port number for client to connect to server", required=True)
parser.add_argument("-l", "--logfile", help="name of logfile", required=True)
parser.add_argument("-n", "--name", help="indicates client name", required=True)
parser.add_argument("--help", action="help", default=argparse.SUPPRESS, help=argparse._("show this help message and exit"))
args = parser.parse_args()
# Global output file
outputFile = open(args.logfile, 'w')

# On exit, log to file
@atexit.register
def exitCleanUp():
    logToFile("terminating client...")

# Logging method
def logToFile(msg):
    outputFile.write(msg)
    outputFile.write("\n")
    outputFile.flush()

def main():
    # Socket initialization
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverAddress = (args.serverIP, args.port)
    print ("[DEBUG] server_address is ", serverAddress)
    clientName = args.name
    # Message Type: register <client1>
    clientRegisterMsg = "register " + clientName
    sock.sendto(clientRegisterMsg, serverAddress)
    # log
    logToFile("connecting to the server " + serverAddress[0] + " at port " + str(serverAddress[1]))
    logToFile("sending register message " + clientName)
    print("connected to server and registered\nwaiting for messages...")
    while True:
        serverMsg = sock.recvfrom(1024)
        print("[DEBUG] Received message from server : ", serverMsg[0])
        serverMsgDataList = serverMsg[0].split()

        if len(serverMsgDataList) == 2 and serverMsgDataList[0] == "welcome" and serverMsgDataList[1].lower() == clientName.lower():
            serverWelcomeMsg = serverMsgDataList[0]
            #log print
            logToFile("received " + serverWelcomeMsg)
        else:
            print("[ERROR] incorrect server msg format")

main()



