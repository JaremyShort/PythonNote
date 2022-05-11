import asyncio


# region py3.5以前
print("----------------------------py3.5以前的异步----------------------------")

@asyncio.coroutine
def func1():
    print(1)
    # IO耗时操作
    yield from asyncio.sleep(2)
    print(2)


@asyncio.coroutine
def func2():
    print(3)
    # IO耗时操作
    yield from asyncio.sleep(2)
    print(4)


tasks = [asyncio.ensure_future(func1()), asyncio.ensure_future(func2())]

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))


# endregion


# region py3.5以后
print("----------------------------py3.5以后的异步----------------------------")

async def func3():
    print(11)
    await asyncio.sleep(2)
    print(22)


async def func4():
    print(33)
    await asyncio.sleep(2)
    print(44)


tasks = [asyncio.ensure_future(func3()), asyncio.ensure_future(func4())]

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))

# endregion
