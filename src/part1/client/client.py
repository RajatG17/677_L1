import sys
import socket
import random 
import time

#Client class
class Client:

	#Function to start client and connect to the server at <server_hostname>,<server_port>
	def StartClient(self, server_hostname, server_port) :
		all_stock_names = ["GameStart", "FishCo"]

		#Number of client requests issued
		max_client_requests = 3000
		#Store average latency of responses
		avg_latency = 0
		#For-loop to send client requests sequentially
		for total in range(max_client_requests):
			print("Client Request Number  : " + str(total))

			#Start timer to track latency
			start = time.perf_counter()

			# Create socket
			client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
			client_socket.connect((server_hostname, server_port))

			#Create client request in the format of (method name,stock name)
			methodName = "Lookup"
			#Randomly pick one of the two stock names for lookup
			index = random.randrange(2)    
			stockName = all_stock_names[index]
			buffer = methodName + "," + stockName
			print("Client request sent : " + buffer)
			client_socket.send(bytes(buffer, "utf8")) # Send buffer to server
			#Receive response from server
			returned_price = client_socket.recv(4096)
			returned_price = returned_price.decode("utf-8")
			if (returned_price == -1):
				print("Error occured while returning the stock price, stock name not present in the catalog") 
			elif (returned_price == -2):
				print("Error occured while returning the stock price, method name is not valid") 	
			elif (returned_price == 0):
				print("Error occured while returning the stock price, trading is suspended") 
			else:
				print("Received response from server, stock price of : " + stockName + " is : " + str(returned_price))	
			#Close socket		
			client_socket.close()

			#End timer to track latency
			end = time.perf_counter() - start

			print("Latency : " + str(end))
			avg_latency = avg_latency+end
			
		avg_latency = avg_latency/max_client_requests	
		print("Average latency : " + str(avg_latency))	

#Expected 3 command line arguments, Eg - python3 client.py <server_ip> <server_port>
if (len(sys.argv) != 3):
    print ("Invalid command line args, Enter server hostname and server port")
else:    
	server_hostname = sys.argv[1]
	server_port = int(sys.argv[2])
	print("Client connecting to server hostname : " + sys.argv[1] + " , server port : " + str(sys.argv[2]))
	#Create an instance of Client class
	client = Client()
	#Start Client 
	client.StartClient(server_hostname, server_port)

