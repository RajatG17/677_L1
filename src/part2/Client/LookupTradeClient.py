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

        hostname = hostname if hostname else "[::]"
        port = port if port else 65532

        try: 
            channel = grpc.insecure_channel(f"{hostname}:{port}")
        except:
            print("Error connecting to server")
        with channel:
            #Create stub 
            stub = rpc_pb2_grpc.StockBazaarStub(channel)
            for i in range(0, 200):
                # Trade function: select stock, volume
                    stockName = clientNameList[random.randint(0, len(clientNameList)-1)]
                    volume = random.randint(1, 100)
                    transactionTtype = transactionTypeList[random.randint(0,len(transactionTypeList)-1)]
                    print(f"\nSending trade request for stock {stockName} with volume {volume}:")    
                    #rpc call to trade
                    start = time.time()
                    response = stub.Trade(request=rpc_pb2.stockTradeRequestMessage(stockName=stockName, N=volume, type=transactionTtype))
                    trade_time = time.time() - start
                    if response.tradeResult == 1:
                        print(f"Trade request Successful!!")
                    elif response.tradeResult == 0:
                        print(f"Trading is suspended for {stockName} at the moment!")
                    elif response.tradeResult == -1:
                        print("Invalid stock name specified")
                    print(f"Time taken : {trade_time*1000}ms")


                    stockName = clientNameList[random.randint(0, len(clientNameList)-1)]
                    #rpc call to lookup stock price and volume
                    start = time.time()
                    response = stub.Lookup(rpc_pb2.stockLookupMessage(stockName=stockName))
                    lookupTime = time.time()-start
                    if response.lookupResponse == 0:
                        print(f"\nTrading is suspended for {stockName} at the moment!")
                    elif response.lookupResponse == -1 :
                        print("\nInvalid Stock name specified")
                    else:
                        print(f"\nPrice of {stockName}: {response.lookupResponse}, and current traded volume : {response.tradingVolume}")
                        print(f"Lookup time : {lookupTime*1000}ms")
        
       
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