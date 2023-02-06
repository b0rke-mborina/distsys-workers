from aiohttp import web
import random
import time
import asyncio
import aiohttp


masterPort = 8080

# variables for saving data
maxNumberOfReqRes = 10000		# for printing
numberOfReceivedRequests = 0	# count received requests
numberOfReturnedResponses = 0	# count sent responses
maxNumberOfTasks = 100000		# for printing
numberOfSentTasks = 0			# count sent tasks
numberOfCompletedTasks = 0		# count completed tasks

# calculate number of workers N (random 5 - 10)
N = random.randint(5, 10) # 3 random.randint(2, 3) random.randint(3, 5)
print("Number of workers:", N)

# call workers and give them IDs (save to dict)
workers = {"workerWithId" + str(id): [] for id in range(1, N + 1)}
print("Workers:", workers)

routes = web.RouteTableDef()

@routes.get("/")
async def function(request):
	try:
		# make variables visible
		global N, workers
		global maxNumberOfReqRes
		global numberOfReceivedRequests, numberOfReturnedResponses
		global numberOfSentTasks, numberOfCompletedTasks

		# log requests status
		numberOfReceivedRequests += 1
		print(time.ctime(), "New request recieved. Current received requests status:", numberOfReceivedRequests, "/", maxNumberOfReqRes) # time.monotonic()time.strptime(time.localtime())
		data = await request.json()

		# print data and status
		# print("Client id:", data.get("client"))
		# print("Codes length:", len(data.get("codes")))
		# for i in data.get("codes"):
			# print(i[0:30])
			# print("_______________________")

		tasks = []
		results = []
		async with aiohttp.ClientSession(connector = aiohttp.TCPConnector(ssl = False)) as session:
			# send task to processing and log sent tasks status
			currentWorker = 1
			for i in range(len(data.get("codes"))):
				task = asyncio.create_task(
					session.get(f"http://127.0.0.1:{8080 + currentWorker}/", json = { "id": data.get("client"), "data": data.get("codes")[i] })
				)
				numberOfSentTasks += 1
				print(time.ctime(), f"New task sent to worker {currentWorker}. Current sent tasks status:", numberOfSentTasks, "/", maxNumberOfTasks)
				tasks.append(task)
				workers["workerWithId" + str(currentWorker)].append(task)
				if currentWorker == N:
					currentWorker = 1
				else:
					currentWorker += 1
			
			# collect processed tasks and log completed tasks status
			results = await asyncio.gather(*tasks)
			numberOfCompletedTasks += len(results)
			print(time.ctime(), f"Another {len(results)} more tasks completed. Current completed tasks status:", numberOfCompletedTasks, "/", maxNumberOfTasks)
			results = [await result.json() for result in results]
			results = [result.get("numberOfWords") for result in results]
			print(results)

		# log responses status
		numberOfReturnedResponses += 1
		print(time.ctime(), "New response sent. Current sent responses status:", numberOfReturnedResponses, "/", maxNumberOfReqRes)

		return web.json_response({"name": "master", "status": "OK", "client": data.get("client"), "averageWordcount": round(sum(results) / len(results), 2)}, status = 200)
	except Exception as e:
		return web.json_response({"name": "master", "error": str(e)}, status = 500)

app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port = masterPort)
