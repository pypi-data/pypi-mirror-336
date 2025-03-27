import threading

class Job(threading.Thread):
    def __init__(self, job_function):
        super(Job, self).__init__()
        self.__flag = threading.Event() 
        self.__flag.set() 
        self.__running = threading.Event()
        self.__running.set() 

        self.job_function = job_function

    def run(self):
        while self.__running.isSet():
            self.__flag.wait() 
            self.job_function()

    def pause(self):
        self.__flag.clear() 

    def resume(self):
        self.__flag.set() 

    def stop(self):
        self.__flag.set() 
        self.__running.clear() 