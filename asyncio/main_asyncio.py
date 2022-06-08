import asyncio

# region py3.5以前
print("----------------------------py3.5以前的异步----------------------------")

# @asyncio.coroutine
# def func1():
#     print(1)
#     # IO耗时操作
#     yield from asyncio.sleep(2)
#     print(2)


# @asyncio.coroutine
# def func2():
#     print(3)
#     # IO耗时操作
#     yield from asyncio.sleep(2)
#     print(4)
#
#
# tasks = [asyncio.ensure_future(func1()), asyncio.ensure_future(func2())]
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(asyncio.wait(tasks))  # 等价于 asyncio.run()

# endregion

# region py3.5以后
print("----------------------------py3.5以后的异步----------------------------")


# async def func3():
#     print(11)
#     await asyncio.sleep(2)
#     print(22)
#
#
# async def func4():
#     print(33)
#     await asyncio.sleep(2)
#     print(44)
#
#
# tasks = [asyncio.ensure_future(func3()), asyncio.ensure_future(func4())]
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(asyncio.wait(tasks))


# asyncio.run(func3())

# endregion

# region py3.7以后   Task对象

async def others():
    print("start")
    await asyncio.sleep(2)
    print("end")
    return "返回值"


# # 非异步调用
# async def func():
#     print("执行协程函数内部代码")
#
#     res1 = await others()
#     print("IO请求结束，结果为：", res1)
#
#     res2 = await others()
#     print("IO请求结束，结果为：", res2)


# 异步调用
async def func():
    print("执行协程函数内部代码")

    # ★★★ 三种调用方式 ★★★

    # （1）
    # task1 = asyncio.create_task(others())
    # task2 = asyncio.create_task(others())
    # res1 = await task1
    # res2 = await task2
    # print(res1, res2)

    # （2） 注意 asyncio.run() 的等价用法，涉及事件循环的创建时间
    # tasks = [others(), others()]
    # down, pending = asyncio.run(asyncio.wait(tasks))

    # （3）
    tasks = [asyncio.create_task(others(), name="t1"), asyncio.create_task(others(), name="t2")]
    down, pending = await asyncio.wait(tasks)
    print(down)
    print(pending)


asyncio.run(func())
# endregion


# region Future
print("----------------------------Future----------------------------")


# 需要手动设置结果 ★★★

async def set_after(fut):
    await asyncio.sleep(2)
    fut.set_result("666")


async def func5():
    # 获取当前正在运行的事件循环
    loop = asyncio.get_running_loop()  # 不存在loop会报错，区别于asyncio.get_event_loop

    # 创建一个任务（Future对象），没绑定任何行为，则这个任务永远不知道什么时候结束。
    fut = loop.create_future()

    # 创建一个任务（Task对象），绑定了set_after函数，函数内部在2s之后，会给fut赋值。
    await  loop.create_task(set_after(fut))

    # loop.run_in_executor() # 包装普通函数为协程函数

    data = await fut
    print(data)


asyncio.run(func5())

print("----------------------------异步迭代器----------------------------")


class Reader(object):

    def __init__(self):
        self.count = 0

    async def readline(self):
        self.count += 1
        if self.count == 100:
            return None
        return self.count

    def __aiter__(self):
        return self

    async def __anext__(self):
        val = await self.readline()
        if val == None:
            raise StopAsyncIteration
        return val


async def func6():
    obj = Reader()
    async for item in obj:
        print(item)


asyncio.run(func6())

print("----------------------------异步上下文管理器----------------------------")


class AsyncContextManager:

    def __init__(self):
        pass

    async def do_something(self):
        # 异步操作数据库
        return 666

    async def __aenter__(self):
        # 异步连接数据库
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # 异步关闭数据库链接
        await asyncio.sleep(1)


async def func7():
    async with AsyncContextManager() as f:
        result = await f.do_something()
        print(result)


asyncio.run(func7())

print("----------------------------uvloop----------------------------")
# 是asyncio的事件循环的替代方案   性能比asyncio高   ★暂不支持windows  -> uvicorn
# import uvloop
# asyncio.set_event_loop_policy(uvloop.EventLoopPolicy)


print("----------------------------异步redis----------------------------")
import aioredis


async def execute(address, password):
    redis = await aioredis.create_redis(address, password)
    await redis.hmset_dict('car', key1=1, key2=2, key3=3)
    result = await redis.hgetall('car', encoding='utf-8')
    print(result)
    redis.close()

    await redis.wait_closed()


asyncio.run(execute('', ''))

# endregion
