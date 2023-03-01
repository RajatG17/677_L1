import sys
import os
import socket

#Set path for importing class "MyThreadPool"
cwd = os.getcwd()
sys.path.append(cwd+"/util/")
sys.path.append(cwd+"/../util/")
sys.path.append(cwd+"/lab-1-asterix-and-the-stock-bazaar-677-lab1/src/part1/util/")

import MyThreadPool

#Server class
class Server:

    #Server constructor that takes the argument <max_threads> for ThreadPool size 
    def __init__(self, max_threads=3):
        #Creates server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Creates a MyThreadPool object which is a ThreadPool of size <max_threads>
        self.server_thread_pool = MyThreadPool.MyThreadPool(max_threads)
        self.catalog = {"GameStart" : [44.6, 0], "FishCo" : [20.4, 0]}
        self.is_trading_suspended = False

    #Function for Lookup
    def Lookup(self, company_name, client_socket, address) :
        if (company_name not in self.catalog.keys()):
            print("Stock name is invalid, returning error...")
            server_response = bytes("-1", "utf8")
        else:
            if (self.is_trading_suspended):
                print("Trading is suspended, returning error...")
                server_response = bytes("0", "utf8")
            else:
                server_response = bytes(str(self.catalog[company_name][0]), "utf8")  
        print("Server response : " + server_response.decode("utf-8") + " for client address : " + str(address))            
        client_socket.send(server_response)     

    #Function to start server at <hostname>,<port>
    def StartServer(self, hostname, port):
        #Bind the server socket to the hostname and port, and start listening
        self.server_socket.bind((hostname, port)) 
        self.server_socket.listen()
        #Infinite loop to accept client requests and send responses
        while (True):
            (client_socket, address) = self.server_socket.accept()
            buffer = client_socket.recv(4096) # Receive buffer
            buffer = buffer.decode("utf-8")
            (method_name, stock_name) = buffer.split(",", 2)
            print("Method name : " + method_name + " , stock_name : " + stock_name)
            if not(method_name == "Lookup"):
                print("Invalid method name, returning error...")
                server_response = bytes("-2", "utf8")
                print("Server response : " + server_response.decode("utf-8"))    
                client_socket.send(server_response)
            else :
                #Call function "IssueRequest" of MyThreadPool to execute client request on a thread 
                self.server_thread_pool.IssueRequest(self.Lookup, [stock_name, client_socket, address])#Call Lookup method

    #Method to stop server
    def StopServer(self):     
        self.server_socket.close()

#Expected 3 command line arguments, Eg - python3 server.py <server_ip> <server_port>
if (len(sys.argv) != 3):
    print ("Invalid command line args")
else:    
    hostname = sys.argv[1]
    port = int(sys.argv[2])
    print("Server on hostname : " + sys.argv[1] + " , port : " + str(sys.argv[2]))
    #Create an instance of Server class with ThreadPool size passed as an argument
    server = Server(2)
    #Start Server
    server.StartServer(hostname, port)
        
