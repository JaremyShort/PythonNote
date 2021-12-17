import logging
import queue
import threading
from concurrent.futures import ThreadPoolExecutor

# from utils.config import MAX_THREAD_COUNT


# 任务：事件
def func_a(a, b):
    return a + b


def func_b(a, b):
    return a * b


def func_c(a, b, c):
    return a * b - c


# 回调函数
def handle_result1(result):
    print(type(result), result)


def handle_result2(result):
    print(type(result), result)


def handle_result3(result):
    print(type(result), result)


class EventEngine(object):
    # 初始化事件事件驱动引擎
    def __init__(self):
        # 保存事件列表:异步任务队列
        self.__eventQueue = queue.Queue()
        # 引擎开关
        self.__active = False
        # 事件处理字典{'event1': [handler1,handler2] , 'event2':[handler3, ...,handler4]}
        self.__handlers = {}
        # 事件引擎主进程
        self.__Thread = threading.Thread(target=self.task_queue_consumer, name="主线程")
        # 事件处理线程池
        self.__thread_pool = ThreadPoolExecutor(max_workers=4)
        # 线程处理存储
        self.__thread_Pool = []

    # 注册事件
    def register(self, event, callback, *args, **kwargs):
        Event = {
            "function": event,
            "callback": callback,
            "args": args,
            "kwargs": kwargs,
        }
        self.__handlers[event] = Event

    # 注销事件
    def unregister(self, event):
        if self.__handlers[event]:
            del self.__handlers[event]

    # 提交事件
    def sendevent(self, event):
        if event in self.__handlers.keys():
            self.__eventQueue.put(self.__handlers[event])

    # 开启事件引擎
    def start(self):
        self.__active = True
        self.__Thread.start()

    # 暂停事件引擎
    def stop(self):
        self.__active = False

    # 暂停后开始
    def restart(self):
        self.__active = True

    # 关闭事件引擎
    def close(self):
        pass

    # 开启事件循环
    def task_queue_consumer(self):
        """
        异步任务队列
        """
        while self.__active:
            if self.__eventQueue.empty() == False:
                try:
                    task = self.__eventQueue.get()
                    function = task.get("function")
                    callback = task.get("callback")
                    args = task.get("args")
                    kwargs = task.get("kwargs")
                    try:
                        if callback:
                            thread = self.__thread_pool.submit(
                                callback, function(*args, **kwargs)
                            )
                            self.__thread_Pool.append(thread)
                    except Exception as ex:
                        if callback:
                            callback(ex)
                    finally:
                        self.__eventQueue.task_done()
                except Exception as ex:
                    logging.warning(ex)


# if __name__ == "__main__":
import time

# 初始化多线程异步框架
Engine = EventEngine()
# 启动
Engine.start()
# 注册回调函数
Engine.register(func_a, handle_result1, 1, 2)
Engine.register(func_b, handle_result2, 1, 2)
Engine.register(func_c, handle_result3, 1, 2, 3)
# 提交事件
Engine.sendevent(func_a)
Engine.sendevent(func_b)
Engine.sendevent(func_c)
time.sleep(2)
Engine.stop()
Engine.restart()
Engine.sendevent(func_b)
Engine.sendevent(func_c)
# for i in range(100):
#     Engine.sendevent(func_a)