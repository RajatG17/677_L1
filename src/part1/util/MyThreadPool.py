import threading
from threading import Thread
from threading import Event

#Class for client request 
class Request:
    #Constructor with the function and its arguments as constructor arguments
    def __init__(self, function, arguments):
        self.function = function
        self.arguments = arguments

#Class of thread used in handwritten ThreadPool class "MyThreadPool"
class MyThread(Thread):
    def __init__(self, thread_pool):
        Thread.__init__(self)
        self.thread_pool = thread_pool
    
    #Function executed by thread
    def run(self):
        while(1):
            #Get the next client request and call the Lookup function 
            client_request = self.thread_pool.GetNextClientRequest()
            client_function = client_request.function
            client_arguments = client_request.arguments
            client_function(client_arguments[0], client_arguments[1], client_arguments[2])

#Class of handwritten ThreadPool class "MyThreadPool"
class MyThreadPool:
    #Constructor with thread pool size passed as an argument
    def __init__(self, max_threads):
        self.max_threads = max_threads
        #Lock for request queue
        self.request_queue_condition_lock = threading.Condition()
        #request queue for client requests
        self.request_queue = list()
        #Create threads in the thread pool of size <max_threads>
        self.threads = list()
        for i in range(max_threads):
            self.threads.append(MyThread(self))    
        #Start the worker threads in the thread pool   
        for i in range(max_threads):
            self.threads[i].start()        

    #Function to get the next client request from the request queue
    def GetNextClientRequest(self):
        while(1):
            #Acquire lock on request queue
            self.request_queue_condition_lock.acquire()
            try:
                #Wait until request queue becomes non-empty
                while(len(self.request_queue) == 0):
                    self.request_queue_condition_lock.wait()
                #After acquiring lock, pop first request from request queue 
                next_request = self.request_queue.pop(0)
                self.request_queue_condition_lock.notify()
            finally:
                #Release lock on request queue
                self.request_queue_condition_lock.release()
            return next_request     

    def IssueRequest(self, function, arguments):
        request = Request(function, arguments) 
        #Acquire lock on request queue
        self.request_queue_condition_lock.acquire()
        try:
            #After acquiring lock, append request to the end of request queue 
            self.request_queue.append(request)
            #Notify threads waiting on the lock on request queue
            self.request_queue_condition_lock.notify()
        finally:
            #Release lock on request queue
            self.request_queue_condition_lock.release()   
