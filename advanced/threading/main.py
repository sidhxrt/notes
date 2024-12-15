# THREADS

# THREADING IS FOR WORKING IN PARALLEL,
# ASYNC IS FOR WAITING IN PARALLEL.

"""
when we run our code, it will wait for each line to be executed or each block of\
code to execute before the next one can happen.

now, if we put something in one of the code-block that requires a bit of waiting time\
like we are waiting on a server or response from something external;\
our program is just gonna sit there doing nothing.

now, there are a couple of ways around this to fix this thing(we can do stuffs quicker i.e execute the whole program quicker).
"""

"""
what is a Thread?
A thread is a separate flow of execution. This means that our program\
will have two things happening at once. 
But for most Python 3 implementaions the different threads do not actually execute at the same time: they merely appear to.

https://realpython.com/intro-to-python-threading/
"""

"""
Asynchronous Programming
A synchronous program is executed one step at a time. Even with conditional branching,
loops and function calls, we can still think about the code in terms of taking one execution step
at a time. When each step is complete, the program moves on to the next one.

An asynchronous program behaves differently. It still takes one execution step at a time.
The difference is that the system may not wait for an execution step to be completed before\
moving on to the next one.

https://realpython.com/python-async-features/
"""

# SYNCHRONOUS VERSION
import requests
from time import perf_counter
def sync_version(urls):
    for url in urls:
        r = requests.get(f"http://127.0.0.1:8000/items/{url}")
        print(r.json())

start = perf_counter()
sync_version(range(1, 2500))
stop = perf_counter()
print("time taken: ", stop - start)
# time taken:  13.974706900000456
"""
# so as we see, we are taking 14 seconds for 2.5k url requests, now what if the url took time to respond, it will increase the overall time of program execution.
# so first option to reduce this time is to use threading

"""


# THREADING
# in this option, we will be using the concurrent futures, threadpoolexecutor.
# threadpoolexecutor allows us to use extra threads.
import requests
from time import perf_counter
from concurrent.futures import ThreadPoolExecutor

start = perf_counter()
urls = range(1, 2500)

def get_data(url):
    r = requests.get(f"http://127.0.0.1:8000/items/{url}")
    print(r.json())

with ThreadPoolExecutor() as executor:
    executor.map(get_data, urls)  # read docs, instead of map, we can use alot of other ways/stuffs.
# we usually use executor.map if we were making network requests.

stop = perf_counter()
print("time taken: ", stop - start)
# time taken:  8.304286599999614

"""
Generally, threads and multi-threading like how we did above, its better\
for if we are trying to work in parallel.
So if our code is constantly doing something, if we are not waiting for anything external then\
threading is the best way for us.

But if we are dealing with any network requests, then we should use async.
"""
# READ MORE ABOUT THREADPOOLEXECUTOR AND CONCURRENT MODULE


#ASYNC
import asyncio
import aiohttp
from time import perf_counter

# 'fetch' is the function that actually makes the request
async def fetch(s, url):
    async with s.get(f"http://127.0.0.1:8000/items/{url}") as r:
        if r.status != 200:
            r.raise_for_status()
        return await r.text()

# 'fetch_all' creates all the tasks, we are using asyncio here and it will await for the response for us.
# this is basically like sending out all of our requests in one go.
# and it will manage and wait for each of the responses to come back.
# so it will basically remove any of that time spent waiting in our code.
async def fetch_all(s, urls):
    tasks = []
    for url in urls:
        task = asyncio.create_task(fetch(s, url))
        tasks.append(task)
    res = await asyncio.gather(*tasks)
    return res

async def main():
    urls = range(1, 2500)
    async with aiohttp.ClientSession() as session:
        htmls = await fetch_all(session, urls)
        print(htmls)

if __name__ == '__main__':
    start = perf_counter()
    asyncio.run(main())
    stop = perf_counter()
    print("time taken: ", stop - start)
# time taken:  2.2188625000017055

# here, all 2.5k requests will be hit, and then once all requests are made, then the response is sent back to us within/in a list.
# if we see terminal of demo_fastapi_server, we will see all 2.5k requests one by one; once it is complete, then we will see all 2.5k responses at once in this program ka terminal(as a list).

"""
so, when should we use synchronous/threading/async?

- if we are trying to request data from the same server over and over again, we are going to find that we are gonna get rate-limited\
  so we are not generally going to be able to use this async version\
  but we can work it through because if for example, the rate limit on our server that we are trying to get to is 300 calls per minute,\
  and we only need to make 200 calls, we can asynchronously send 200 and get all the responses back in a flash.
  if we were doing it synchronously, we would have to send 200 single requests which could take more time.

- if we have lots of urls that we need to visit for, lots of different sites, lots of different servers, we can then use our async code to request them all in one go\
  and get the responses back and then handle it that way.
"""