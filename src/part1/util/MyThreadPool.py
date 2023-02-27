import threading
from threading import Thread
from threading import Event

class Request:
    def __init__(self, function, arguments):
        self.function = function
        self.arguments = arguments

class MyThread(Thread):
    def __init__(self, thread_pool):
        Thread.__init__(self)
        self.thread_pool = thread_pool
        #print("self.thread_pool : " + str(self.thread_pool))

    def run(self):
        while(1):
            if self.thread_pool.pool_event.is_set():
                break
            client_request = self.thread_pool.GetNextClientRequest()
            client_function = client_request.function
            client_arguments = client_request.arguments
            client_function(client_arguments[0], client_arguments[1], client_arguments[2])

class MyThreadPool:
    
    def __init__(self, max_threads):
        self.pool_event = Event()
        self.max_threads = max_threads
        self.request_queue_condition_lock = threading.Condition()
        self.request_queue = list()
        self.threads = list()
        for i in range(max_threads):
            self.threads.append(MyThread(self))    
        for i in range(max_threads):
            self.threads[i].start()        

    def GetNextClientRequest(self):
        while(1):
            self.request_queue_condition_lock.acquire()
            try:
                while(len(self.request_queue) == 0):
                    self.request_queue_condition_lock.wait()
                next_request = self.request_queue.pop(0)
                self.request_queue_condition_lock.notify()
            finally:
                self.request_queue_condition_lock.release()
            return next_request     

    def IssueRequest(self, function, arguments):
        request = Request(function, arguments) 
        self.request_queue_condition_lock.acquire()
        try:
            self.request_queue.append(request)
            self.request_queue_condition_lock.notify()
        finally:
            self.request_queue_condition_lock.release()   

    def StopAllThreads(self):
        self.pool_event.set()
        for i in range(self.max_threads):
            self.threads[i].join()        
