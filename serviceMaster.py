# import subprocess
from aiohttp import web
import random
import time
import asyncio
import aiohttp


masterPort = 8080

# variables for saving data
maxNumberOfRequests = 100000	# for printing
requests = []						# saving received requests
sentTasks = []						# sent tasks
completedTasks = []				# completed tasks
noOfSentTasks = 0					# count sent tasks
noOfCompletedTasks = 0			# count completed tasks

currentWorkerId = 1

# calculate number of workers N (random 5 - 10)
N = 3 # random.randint(5, 10)
print("Number of workers:", N)

# call workers and give them IDs (save to dict)
workers = {"workerWithId" + str(id): [] for id in range(1, N + 1)}
print("Workers:", workers)

routes = web.RouteTableDef()

@routes.get("/")
async def function(request):
	try:
		# make variables visible
		global maxNumberOfRequests, requests
		global sentTasks, completedTasks
		global noOfSentTasks, noOfCompletedTasks
		global N, workers

		# log data status
		print("New data recieved. Time:", time.ctime()) # time.monotonic()time.strptime(time.localtime())
		data = await request.json()
		requests.append(data)
		print("Current received data status:", len(requests), "/", maxNumberOfRequests)
		noOfSentTasks += 1

		# print data and status
		print("Client id:", data.get("client"))
		print("Codes length:", len(data.get("codes")))
		# for i in data.get("codes"):
			# print(i[0:30])
			# print("_______________________")
		# requests.append(data)
		# print("New data recieved. Current data status:", len(requests), "/", maxNumberOfRequests)

		"""
		# WORK IN PROGRESS
		if len(requests) >= N: # N * 1000
			# send 1000 lines to each worker
			startTime = time.monotonic_ns()

			# send other lines to workers (1000 to each) when tasks are completed
			print("Data processing starting...")
			async with aiohttp.ClientSession(connector = aiohttp.TCPConnector(ssl = False)) as session:
				# send tasks to processing
				for i in range(1, N + 1):
					sentTasks.append(asyncio.create_task(session.get(f"http://127.0.0.1:{8080 + i}/")))
				noOfSentTasks += N
				print("Tasks processing:", noOfSentTasks, "/", maxNumberOfRequests)

				# collect processed tasks
				for i in range(1, N + 1):
					completedTasks.append(await asyncio.gather(*sentTasks))
				noOfCompletedTasks += N
				print("Tasks completed:", noOfCompletedTasks, "/", maxNumberOfRequests)

			# log timestamps of tasks
			endTime = time.monotonic_ns()
			print("Time:", endTime - startTime)

			# load processed data
			completedTasks = [await x.json() for x in completedTasks]
			
			# return processed data
			for data in completedTasks:
				return web.json_response({"name": "master", "status": "OK", "averageWordcount": len(requests)}, status = 200)
			# print(completedTasks)
		"""

		tasks = []
		results = []
		async with aiohttp.ClientSession(connector = aiohttp.TCPConnector(ssl = False)) as session:
			# send task to processing
			sent = 0
			while sent < len(data.get("codes")):
				for i in range(1, N + 1):
					if sent < len(data.get("codes")):
						tasks.append(asyncio.create_task(session.get(f"http://127.0.0.1:{8080 + i}/", json = { "data": data.get("codes")[i] }))) # "a a a a a"
						sent += 1
			# collect processed tasks
			results = await asyncio.gather(*tasks)
			results = [await result.json() for result in results]
			results = [result.get("numberOfWords") for result in results]
			print(results)

		# subprocess.call('python serviceWorker.py', creationflags=subprocess.CREATE_NEW_CONSOLE)
		return web.json_response({"name": "master", "status": "OK", "client": data.get("client"), "averageWordcount": sum(results) / len(results)}, status = 200)
	except Exception as e:
		return web.json_response({"name": "master", "error": str(e)}, status = 500)

app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port = masterPort)
