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
