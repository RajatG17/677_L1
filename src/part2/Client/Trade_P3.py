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
        transactionTypeList = ["Buy", "Sell"]
        time_taken = list()

        hostname = hostname if hostname else "[::]"
        port = port if port else 65532

        for i in range(0, 3000):
            start = time.time()
            try: 
                channel = grpc.insecure_channel(f"{hostname}:{port}")
            except:
                print("Error connecting to server")
            with channel:
                #Create stub 
                stub = rpc_pb2_grpc.StockBazaarStub(channel)
                # Trade function: select stock, volume
                stockName = clientNameList[random.randint(0, len(clientNameList)-1)]
                volume = random.randint(1, 20)
                transactionTtype = transactionTypeList[random.randint(0,len(transactionTypeList)-1)]
                print(f"\nSending trade request for stock {stockName} with volume {volume}:")    
                #rpc call to trade
                response = stub.Trade(request=rpc_pb2.stockTradeRequestMessage(stockName=stockName, N=volume, type=transactionTtype))
                trade_time = time.time() - start
                if response.tradeResult == 1:
                    print(f"Trade request Successful!!")
                elif response.tradeResult == 0:
                    print(f"Trading is suspended for {stockName} at the moment!")
                elif response.tradeResult == -1:
                    print("Invalid stock name specified")
                time_taken.append(trade_time)
                #print(f"Time taken : {trade_time*1000}ms")
        print(f"Average over 3000 calls: {(sum(time_taken)/len(time_taken))*1000}ms")

        
       
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