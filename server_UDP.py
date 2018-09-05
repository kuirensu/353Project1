from __future__ import print_function
import socket               								# Import socket module
import argparse                                             # Import argparse module
import atexit
import thread
import threading
# Part 1,2 Done

# TODO IP difference between client and server
# Required arguments specification
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("-p", "--port", type=int, help="the port number for the chat server", required=True)
parser.add_argument("-l", "--logfile", help="name of logfile", required=True)
parser.add_argument("-h", "--handler", type=int, help="indicates unknown clients", required=True)
parser.add_argument("--help", action="help", default=argparse.SUPPRESS, help=argparse._("show this help message and exit"))
args = parser.parse_args()
# Global data structures
clientsList = []
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

def getNameFromAddress(address):
    for client in clientsList:
        if client[1] == address:
            return client[0]
    return None

def getAddressFromName(clientName):
    for client in clientsList:
        if client[0] == clientName:
            return client[1]
    return None

def handleClientToClientMsg(senderName, clientMsgData, sock):
    clientMsgDataList = clientMsgData.split()
    receiverName = clientMsgDataList[1]
    receiverAddress = getAddressFromName(receiverName)
    if receiverAddress is None:
        print("[ERROR] receiver with name", receiverName, "does not exist")
    clientMsgDataList[0] = "recvfrom"
    clientMsgDataList[1] = senderName
    senderMsg = " ".join(clientMsgDataList)
    sock.sendto(senderMsg, receiverAddress)
    # Log recvfrom
    logRecvfrom(senderName, receiverName, clientMsgData)

# convert sender's raw message to <message string>
def getMsgFromRawMsg(rawMsg):
    rawMsgList = rawMsg.split()
    del rawMsgList[0]
    del rawMsgList[0]
    senderMsg = " ".join(rawMsgList)
    return senderMsg

def logSendto(senderName, receiverName, senderMsgRaw):
    senderMsg = getMsgFromRawMsg(senderMsgRaw)
    sendtoLog = "sendto " + receiverName + " from " + senderName + " " + senderMsg
    logToFile(sendtoLog)

def logRecvfrom(senderName, receiverName, senderMsgRaw):
    senderMsg = getMsgFromRawMsg(senderMsgRaw)
    recvfromLog = "recvfrom " + senderName + " to " + receiverName + " " + senderMsg
    logToFile(recvfromLog)

def isClientExist(clientName):
    for client in clientsList:
        if client[0] == clientName:
            return True
    return False

def connectionHandler(sock):
    while True:
        clientMsgData, clientAddress = sock.recvfrom(1024)
        clientMsgDataList = clientMsgData.split()
        # new client connection
        # TODO remove save client
        if len(clientMsgDataList) == 2 and clientMsgDataList[0].lower() == "register":
            # log
            logToFile("client connection from host " + clientAddress[0] + " port " + str(clientAddress[1]))
            clientName = clientMsgDataList[1]
            # Add new client to clientsList
            clientsList.append((clientName, clientAddress))
            print("[DEBUG] clientsList : ", clientsList)
            # terminal output
            print(clientName, "registered from host", clientAddress[0], "port", str(clientAddress[1]))
            # Initiate thread to send client welcome messages
            sendWelcomeMsgThread = threading.Thread(target=sendWelcomeMsg, args=(clientName, clientAddress, sock,))
            sendWelcomeMsgThread.setDaemon(True)
            sendWelcomeMsgThread.start()
        # Some client send msg
        elif len(clientMsgDataList) > 2 and clientMsgDataList[0] == "sendto":
            receiverName = clientMsgDataList[1]
            senderName = getNameFromAddress(clientAddress)
            if senderName is None:
                print("[ERROR] sender with address", senderAddress, "does not exist")
    
            # Log sendto
            logSendto(senderName, receiverName, clientMsgData)
            if isClientExist(receiverName):
                # Initiate thread to send a client's msg to another client
                handleClientToClientMsgThread = threading.Thread(target=handleClientToClientMsg, args=(senderName, clientMsgData, sock,))
                handleClientToClientMsgThread.setDaemon(True)
                handleClientToClientMsgThread.start()
            elif args.handler == 0:
                logToFile(receiverName + " not registered with server")
            #elif args.handler == 1:
                
        else:
            print("[DEBUG] Recieved unsupported message")


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




