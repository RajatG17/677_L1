import sys
import socket
import random 
import time

class Client:

	def StartClient(self, server_hostname, server_port) :
		all_stock_names = ["GameStart", "FishCo"]
		max_client_requests = 3000
		total = 0
		#latencies = []
		avg_latency = 0
		for total in range(max_client_requests):
			print("Client Request  : " + str(total))

			start = time.perf_counter()

			client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create socket
			#client_socket.connect((socket.gethostname(), 8899))
			client_socket.connect((server_hostname, server_port))
			methodName = "Lookup"
			index = random.randrange(2)    
			stockName = all_stock_names[index]
			buffer = methodName + "," + stockName
			print("buffer : " + buffer)
			client_socket.send(bytes(buffer, "utf8")) # Send buffer to server
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
			client_socket.close()
			end = time.perf_counter() - start
			#latencies.append(end)
			print("Latency : " + str(end))
			avg_latency = avg_latency+end
			#print('{:.6f}s for the calculation'.format(end))
		avg_latency = avg_latency/max_client_requests	
		print("Average latency : " + str(avg_latency))	

print(f"Arguments count: {len(sys.argv)}")
if (len(sys.argv) != 3):
    print ("Invalid command line args, Enter server hostname and server port")
else:    
	server_hostname = sys.argv[1]
	server_port = int(sys.argv[2])
	print("Client connecting to server hostname : " + sys.argv[1] + " , server port : " + str(sys.argv[2]))
	client = Client()
	client.StartClient(server_hostname, server_port)

