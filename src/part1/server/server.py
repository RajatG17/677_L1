import sys
import os
import socket

cwd = os.getcwd()
print("Current working directory : " + str(cwd))
sys.path.append(cwd+"/util/")
sys.path.append(cwd+"/../util/")
sys.path.append(cwd+"/lab-1-asterix-and-the-stock-bazaar-677-lab1/src/part1/util/")

print("sys.path : " + str(sys.path))

import MyThreadPool

class Server:

    def __init__(self, max_threads=3):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_thread_pool = MyThreadPool.MyThreadPool(max_threads)
        self.catalog = {"GameStart" : [44.6, 0], "FishCo" : [20.4, 0]}
        self.total_requests_served = 0
        self.is_trading_suspended = False

    def Lookup(self, company_name, client_socket, address) :
        if (company_name not in self.catalog.keys()):
            print("Stock name is invalid, returning error...")
            server_response = bytes("-1", "utf8")
        else:
            if (self.is_trading_suspended):
                server_response = bytes("0", "utf8")
            else:
                server_response = bytes(str(self.catalog[company_name][0]), "utf8")  
        print("server_response : " + server_response.decode("utf-8") + " for client address : " + str(address))            
        client_socket.send(server_response)     

    def StartServer(self, hostname, port):
        #self.server_socket.bind((socket.gethostname(), 8899))
        self.server_socket.bind((hostname, port))
        self.server_socket.listen()
        while (True):
            (client_socket, address) = self.server_socket.accept()
            buffer = client_socket.recv(4096)
            buffer = buffer.decode("utf-8")
            (method_name, stock_name) = buffer.split(",", 2)
            print("method_name : " + method_name)
            print("stock_name : " + stock_name)
            if not(method_name == "Lookup"):
                print("Invalid method name, returning error...")
                server_response = bytes("-2", "utf8")
                print("server_response : " + server_response.decode("utf-8"))    
                client_socket.send(server_response)
            else :
                self.server_thread_pool.IssueRequest(self.Lookup, [stock_name, client_socket, address])

    def StopServer(self):  
        self.server_thread_pool.StopAllThreads()      
        self.server_socket.close()

print(f"Arguments count: {len(sys.argv)}")
if (len(sys.argv) != 3):
    print ("Invalid command line args")
else:    
    hostname = sys.argv[1]
    port = int(sys.argv[2])
    print("Connecting to hostname : " + sys.argv[1] + " , port : " + str(sys.argv[2]))
    server = Server(2)
    server.StartServer(hostname, port)
        
