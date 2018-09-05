from __future__ import print_function
import socket               								# Import socket module
import argparse                                             # Import argparse module
import atexit
import thread
import threading
# Part 1 Done

# TODO IP difference between client and server, exit cmd
# Required arguments specification
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("-p", "--port", type=int, help="the port number for the chat server", required=True)
parser.add_argument("-l", "--logfile", help="name of logfile", required=True)
parser.add_argument("-h", "--handler", type=int, help="indicates unknown clients", required=True)
parser.add_argument("--help", action="help", default=argparse.SUPPRESS, help=argparse._("show this help message and exit"))
args = parser.parse_args()
# Global output file
outputFile = open(args.logfile, 'w')

# On exit, log to file
@atexit.register
def exitCleanUp():
    logToFile("terminating server...")

# Logging method
def logToFile(msg):
    #LOCK?
    outputFile.write(msg)
    outputFile.write("\n")
    outputFile.flush()

def sendWelcomeMsg(clientName, clientAddress, sock):
    # log
    logToFile("received register " + clientName + " from host " + clientAddress[0] + " port " + str(clientAddress[1]))
    if (clientName):
        # Message Type: welcome <client1>
        welcomeMsg = "welcome " + clientName
        sock.sendto(welcomeMsg, clientAddress)

#def sendClientMsgToClient(senderName, receiverName, receiverAddress, sock):

def connectionHandler(sock):
    while True:
        clientMsgData, clientAddress = sock.recvfrom(1024)
        clientMsgDataList = clientMsgData.split()
        # new client connection
        if len(clientMsgDataList) == 2 and clientMsgDataList[0].lower() == "register":
            # log
            logToFile("client connection from host " + clientAddress[0] + " port " + str(clientAddress[1]))
            clientName = clientMsgDataList[1]
            # terminal output
            print(clientName, "registered from host", clientAddress[0], "port", str(clientAddress[1]))
            # Initiate thread to send client welcome messages
            sendWelcomeMsgThread = threading.Thread(target=sendWelcomeMsg, args=(clientName, clientAddress, sock,))
            sendWelcomeMsgThread.setDaemon(True)
            sendWelcomeMsgThread.start()
        # Some client send msg
        #elif len(clientMsgDataList) > 2 and clientMsgDataList[0] == "sendto":
            # Log sendto
            # If reveiver is present/not present
        #else:


def main():
    # Socket initialization
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    port = args.port
    sock.bind(('localhost', port))
    print("[DEBUG] Binding completed  ! !")
    # log
    logToFile("server started on "+ socket.gethostbyname(socket.getfqdn()) + " at port " + str(port) + "...")
    # TODO: add thread and command line logic
    connectionHandlerThread = threading.Thread(target=connectionHandler, args=(sock,))
    connectionHandlerThread.setDaemon(True)
    connectionHandlerThread.start()

    while True:
        cmd = raw_input("> ")
        print("[DEBUG] Input command :", cmd)
        if str(cmd) == "exit":
            break
        else:
            print("[DEBUG] Unsupported command")


main()




