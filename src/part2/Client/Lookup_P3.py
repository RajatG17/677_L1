import grpc
import sys
import os
import time
import random

wd = os.getcwd()
sys.path.append(wd+"/../Stubs/")

import rpc_pb2_grpc
import rpc_pb2

class Client():
    def runClient(self, hostname, port):

        clientNameList = ["GameStart", "FishCo", "MenhirCo", "BoarCo", "BoarCO","GamStart"]

        hostname = hostname if hostname else "[::]"
        port = port if port else 65532

        time_taken = list()

        
        for i in range(0, 3000):
            start = time.time()
            try: 
                channel = grpc.insecure_channel(f"{hostname}:{port}")
            except:
                print("Error connecting to server")
            with channel:
                #Create stub 
                stub = rpc_pb2_grpc.StockBazaarStub(channel)
                stockName = clientNameList[random.randint(0, len(clientNameList)-1)]
                #rpc call to lookup stock price and volume
                response = stub.Lookup(rpc_pb2.stockLookupMessage(stockName=stockName))
                lookupTime = time.time()-start
                if response.lookupResponse == 0:
                    print(f"\nTrading is suspended for {stockName} at the moment!")
                elif response.lookupResponse == -1 :
                    print("\nInvalid Stock name specified")
                else:
                    print(f"\nPrice of {stockName}: {response.lookupResponse}, and current traded volume : {response.tradingVolume}")
                time_taken.append(lookupTime)
                #print(f"Lookup time : {lookupTime*1000}ms")
        print(f"Average latency over 3000 calls: {(sum(time_taken)/len(time_taken))*1000}ms")


            
    
       
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