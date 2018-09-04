from __future__ import print_function
import socket               								# Import socket module
import argparse                                             # Import argparse module
import atexit

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

def main():
    # Socket initialization
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    port = args.port
    sock.bind(('localhost', port))
    print("[DEBUG] Binding completed  ! !")
    # log
    logToFile("server started on "+ socket.gethostbyname(socket.getfqdn()) + " at port " + str(port) + "...")
    while True:
        clientMsg = sock.recvfrom(1024)
        print("[DEBUG] Data received from client : ", str(clientMsg[0]))
        clientAddress = clientMsg[1]
        # log
        logToFile("client connection from host " + clientAddress[0] + " port " + str(clientAddress[1]))
        clientMsgDataList= clientMsg[0].split()

        if len(clientMsgDataList) == 2 and clientMsgDataList[0].lower() == "register":
            clientName = clientMsgDataList[1]
            print(clientName, "registered from host", clientAddress[0], "port", str(clientAddress[1]))
            # Message Type: welcome <client1>
            welcomeMsg = "welcome " + clientName
            # log
            logToFile("received register " + clientName + " from host " + clientAddress[0] + " port " + str(clientAddress[1]))
            if (clientName):
                sock.sendto(welcomeMsg, clientAddress)
        else:
            print("[ERROR] incorrect client msg format")

main()
