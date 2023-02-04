# import subprocess
from aiohttp import web
import random
import time
import asyncio
import aiohttp


masterPort = 8080

maxNumberOfRequests = 100000
requests = []

# calculate number of workers N (random 5 - 10)
N = random.randint(5, 10)
print("Number of workers:", N)

# call workers and give them IDs (save to dict)
workers = {"workerWithId" + str(id): [] for id in range(1, N + 1)}
print("Workers:", workers)

routes = web.RouteTableDef()

@routes.get("/")
async def function(request):
	try:
		print("master OK")

		# make variables visible
		global maxNumberOfRequests
		global requests
		global N
		global workers

		# print data and status
		data = await request.json()
		print("User id:", data.get("user"))
		print("Codes length:", len(data.get("codes")))
		# for i in data:
			# print(i[0:30])
			# print("_______________________")
		requests.append(data)
		print("New data recieved. Current data status", len(requests), "/", maxNumberOfRequests)

		# send 1000 lines to each worker
		startTime = time.monotonic_ns()

		# WORK IN PROGRESS
		if len(requests) >= 10000:
			tasks = []
			async with aiohttp.ClientSession() as session:
				for i in range(1, N + 1):
					tasks.append(asyncio.create_task(session.get(f"http://127.0.0.1:{8080 + i}/")))
				res = await asyncio.gather(*tasks)
				res = [await x.text() for x in res]
				print(res)
			# for i in range(1, N + 1):
				# task = asyncio.create_task(session.get("http://service0:8080/"))
				# response = await asyncio.gather(task)
				# responseData = await response[0].json()
				# tasks = asyncio.create_task(*workers.get(f"workerWithId{i}"))
			results = res
			endTime = time.monotonic_ns()
			print("Time:", endTime - startTime)
			#  - log timestamps of tasks
			#  - count received and done tasks
			#  - send other lines to workers (1000 to each) when tasks are completed

		# subprocess.call('python serviceWorker.py', creationflags=subprocess.CREATE_NEW_CONSOLE)
		return web.json_response({"name": "master", "status": "OK", "averageWordcount": len(requests)}, status = 200) # sum(results) / len(results)
	except Exception as e:
		return web.json_response({"name": "master", "error": str(e)}, status = 500)

app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port = masterPort)
