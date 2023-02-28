import grpc
import sys
import os
import time
import random

wd = os.getcwd()
sys.path.append(wd+"/../Stubs/")

import rpc_pb2_grpc 
import rpc_pb2 

class Client:

    def runClient(self, hostname, port):
        #try connection

        hostname = hostname if hostname else "[::]"
        port = port if port else 65532

        try: 
            channel = grpc.insecure_channel(f"{hostname}:{port}")
        except:
            print("Error connecting to server")

        with channel:

            clientNameList = ["GameStart", "FishCo", "MenhirCo", "BoarCo", "BoarCO","GamStart"]

            # create a stub
            stub = rpc_pb2_grpc.StockBazaarStub(channel)

            for i in range(0, 100):

                price = random.randint(1, 100)
                stockName = clientNameList[random.randint(0, len(clientNameList)-1)]
                response = stub.Update(request=rpc_pb2.stockUpdateRequestMessage(stockName=stockName, price=price)) # rpc call to update price
                if response.updateResult == 1:
                    print(f"\nPrice of {stockName} successfully updated to ${price}")
                elif response.updateResult == -1:
                    print(f"\nInvalid stock name specified: No such stock as {stockName}")
                elif response.updateResult == -2:
                    print(f"\nError updating price of {stockName} : Negative price value specified")
                else:
                    print(f"\nUnknown error occured!")


                time.sleep(random.randint(0,1)*30) # Wait before next update request

            
       
if __name__ == "__main__":

    hostname = input("Enter hostname: ")
    while True:
        port = int(input("Enter port (integer greater than 1024): "))
        if port > 1024:
            break
        else:
            print("Enter a valid port number")
    
    client = Client()
    client.runClient(hostname, port)