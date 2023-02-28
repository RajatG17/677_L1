import grpc
import sys
import os
from threading import Lock
from concurrent import futures

wd = os.getcwd()
sys.path.append(wd+"/../Stubs/")

import rpc_pb2_grpc as pb2_grpc
import rpc_pb2 as pb2

# Maximum tradable Volume to be set at startup
tradingVolumeThreshold = 0

# Stock catalog 
Stocks = {
    "GameStart":{
        "price": 20.44,
        "tradingVolume": 0,
        "tradingSuspended":False
        },
    "FishCo":{
        "price": 17.99,
        "tradingVolume": 0,
        "tradingSuspended":False
    },
    "BoarCo":{
        "price": 25.00,
        "tradingVolume": 0,
        "tradingSuspended":False
    },
    "MenhirCo":{
        "price": 14.87,
        "tradingVolume": 0,
        "tradingSuspended":False
    }
}

class StockBazaar(pb2_grpc.StockBazaarServicer):
    global tradingVolumeThreshold

    def __init__(self):
        super().__init__()
        self.Lock = Lock()

    # Lookup method
    def Lookup(self, request, context):
        stockName = request.stockName
        lookUpResponse, tradingVolume = None, None

        if stockName not in list(Stocks.keys()):
            lookUpResponse = -1
            tradingVolume = None
        elif stockName in list(Stocks.keys()) and Stocks[stockName]["tradingSuspended"]:
            lookUpResponse = 0
            tradingVolume = None
        elif stockName in list(Stocks.keys()):
            lookUpResponse = Stocks[stockName]["price"]
            tradingVolume = Stocks[stockName]["tradingVolume"] 

        return pb2.stockLookupResponseMessage(lookupResponse=lookUpResponse, tradingVolume=tradingVolume)

    # Trade method
    def Trade(self, request, context):
        stockName = request.stockName
        stockVolume = request.N
        transactionType = request.type
        tradeResult = -999

        try:
            if stockName not in list(Stocks.keys()):
                tradeResult = -1
            elif Stocks[stockName]["tradingSuspended"]:
                tradeResult = 0
            elif transactionType.lower() in ["buy", "sell"]:
                    self.Lock.acquire()
                    if Stocks[stockName]["tradingVolume"] < tradingVolumeThreshold:
                        Stocks[stockName]["tradingVolume"] += stockVolume # update stock's traded volume
                    if Stocks[stockName]["tradingVolume"] >= tradingVolumeThreshold:
                        Stocks[stockName]["tradingSuspended"] = True # Suspend trading
                    self.Lock.release()
                    tradeResult = 1
                
        except:
            if self.Lock.locked():
                self.Lock.release()
            print(f"Error trading stock of {stockName}")

        return pb2.stockTradeResponseMessage(tradeResult=tradeResult)
        

    #Update method
    def Update(self, request, context):
        stockName = request.stockName
        price = request.price
        updateResult =-999 

        try:
            if stockName in list(Stocks.keys()) and price <= 0:
                updateResult = -2
            elif stockName in list(Stocks.keys()):
                self.Lock.acquire()
                Stocks[stockName]["price"] = price
                self.Lock.release()
                updateResult = 1
            elif stockName not in list(Stocks.keys()):
                updateResult = -1
        except:
            if self.Lock.locked:
                self.Lock.release()
            print(f"Error updating price of {stockName}")

        return pb2.stockUpdateResponseMessage(updateResult=updateResult)

        

    
def serve(port=65532):
    global tradingVolumeThreshold
    
    while True:
        try:
            maxWorkers = int(input("Maximum worker threshold: "))
            if maxWorkers <= 0:
                print("Please enter a positive integer value")
                continue
            else:
                break
        except ValueError:
            print("Please enter a valid positive integer value")
            continue

    while True:
        try:
            tradingVolumeThreshold = int(input("Maximum maximum trading volume threshold: "))
            if tradingVolumeThreshold <= 0:
                print("Please enter a positive integer value")
                continue
            else:
                break
        except ValueError:
            print("Please enter a valid positive integer value")
            continue



    server = grpc.server(futures.ThreadPoolExecutor(max_workers=maxWorkers))
    pb2_grpc.add_StockBazaarServicer_to_server(StockBazaar(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":

    while True:
        port = int(input("Enter port (integer greater than 1024): "))
        if port > 1024:
            break
        else:
            print("Enter a valid port number")
    serve(port)