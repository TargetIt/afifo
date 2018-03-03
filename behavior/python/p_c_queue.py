# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 09:55:39 2018

@author: relaxIt
"""


# p_c_queue

''' A multi-producer, multi-consumer queue '''


import threading 
from collections import deque
from heapq import heappush, heappop
from time import monotonic as time
import random

__all__ = ['Empty', 'Full', 'Queue', 'PriorityQueue', 'LifoQueue']

class p_c_queue:
    '''Create a queue object with a given maximum size
    
    If maxsize is <= 0, the queue size is infinite.  
    '''
    
    class Empty(Exception):
        'Exception raised by Queue.get(block=0)/get_nowait().'
        pass
    class Full(Exception):
        'Exception raised by Queue.put(block=0)/put_nowait().'
        pass
    
    def __init__(self, maxsize=0):
        self.maxsize = maxsize
        self._init(maxsize)
        
        self.mutex = threading.Lock()
        self.not_empty = threading.Condition(self.mutex)
        self.not_full = threading.Condition(self.mutex)
        
        self.all_tasks_done = threading.Condition(self.mutex)
        self.unfinished_tasks = 0
        
    def task_done(self):
        with self.all_tasks_done:
            unfinished = self.unfinished_tasks - 1
            if unifinished <= 0:
                if unfinished < 0:
                    raise ValueError('task_done() called too many times')
                self.all_tasks_done.notify_all()
            self.unfinished_tasks = unfinished
    
    def join(self):
        with self.all_tasks_done:
            while self.unfinished_tasks:
                self.all_tasks_done.wait()
    
    def qsize(self):
        with self.mutex:
            return self._qsize()
        
    def empty(self):
        with self.mutex:
            return not self._qsize()
    
    def full(self):
        with self.mutex:
            return 0 < self.maxsize <= self._qsize()
        
    def put(self, item, block=True, timeout=None):
        with self.not_full:
            if self.maxsize > 0:
                if not block:
                    if self._qsize() >= self.maxsize:
                        raise Full
                else:
                    while self._qsize() >= self.maxsize:
                        self.not_full.wait()
            
            self._put(item)
            self.unfinished_tasks += 1
            self.not_empty.notify()
            
    def get(self, block=True, timeout=None):
        with self.not_empty:
            if not block:
                if not self._qsize():
                    raise Empty
            else:
                while not self._qsize():
                    self.not_empty.wait()
        
            item = self._get()
            self.not_full.notify()
            return item
        
    def put_nowait(self, item):
        return self.put(item, block=False)
    def get_nowait(self):
        return self.get(block=False)
    
    def _init(self, maxsize):
        self.queue = deque()
        
    def _qsize(self):
        return len(self.queue)
    def _put(self, item):
        return self.queue.append(item)
    def _get(self):
        return self.queue.popleft()
    
    
class PriorityQueue(p_c_queue):
    
    def _init(self, maxsize):
        self.queue = []
    
    def _qsize(self):
        return len(self.queue)
    
    def _put(self, item):
        heappush(self.queue, item)
        
    def _get(self):
        return heappop(self.queue)

class LifoQueue(p_c_queue):
    def _init(self, maxsize):
        self.queue = []
    
    def _qsize(self):
        return len(self.queue)
    
    def _put(self, item):
        self.queue.append(item)
        
    def _get(self):
        return self.queue.pop()
    
myqueue = p_c_queue(3)
class producer(threading.Thread):
    def run(self):
        global myqueue
        while True:
            myqueue.put(random.choice(range(5)))
    pass

class consumer(threading.Thread):
    def run(self):
        global myqueue
        while True:
            print (myqueue.get())
    pass


Pthread = producer()
Cthread = consumer()

Pthread.start()
Cthread.start()