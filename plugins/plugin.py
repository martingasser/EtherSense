import queue
from threading import Thread, Barrier

class EtherSensePlugin:

    def __init__(self, process_async, barrier):
        self.process_async = process_async
        self.barrier = barrier

        self.__bypass = False

        if self.process_async:
            self.frame_queue = queue.Queue()
            self.result_queue = queue.Queue()
            self.last_frame = None
            self.frames_dropped = 0

            self.run = True
            self.processing_thread = Thread(target=self.processing_thread)
            self.processing_thread.start()

    
    def __call__(self, frame):

        if self.__bypass:
            return None

        if self.process_async:
            self.frame_queue.put_nowait(frame)

            try:
                res = self.result_queue.get_nowait()
                self.last_frame = res
            except:
                self.frames_dropped += 1
                res = self.last_frame
            
            if res:
                res[1]['frames_dropped'] = self.frames_dropped
        else:            
            res = self.process(frame)
        
        return res

    def stop(self):
        if self.process_async:
            self.run = False
            self.processing_thread.join()

    @property
    def bypass(self):
        return self.__bypass

    @bypass.setter
    def bypass(self, b):
        self.__bypass = b

    def processing_thread(self):
        while self.run:
            try:
                frame = self.frame_queue.get_nowait()
                self.frame_queue.queue.clear()
                res = self.process(frame)
                self.barrier.wait()
                self.result_queue.put_nowait(res)
            except queue.Empty:
                pass
