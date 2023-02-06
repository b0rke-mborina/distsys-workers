from aiohttp import web
import random
import asyncio
import aiohttp
import logging


# setup port and logging settings
masterPort = 8080
logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(message)s', datefmt = '%Y-%m-%d %H:%M:%S')

# variables for saving data
M = 1000								# sample size
maxNumberOfReqRes = 10000		# for printing
numberOfReceivedRequests = 0	# count received requests
numberOfReturnedResponses = 0	# count sent responses
# maxNumberOfTasks = 100000	# for printing
numberOfSentTasks = 0			# count sent tasks
numberOfCompletedTasks = 0		# count completed tasks

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
		# make variables visible
		global N, workers, M
		global maxNumberOfReqRes # , maxNumberOfTasks
		global numberOfReceivedRequests, numberOfReturnedResponses
		global numberOfSentTasks, numberOfCompletedTasks

		# log requests status and get data from request
		numberOfReceivedRequests += 1
		logging.info(f"New request recieved. Current received requests status: {numberOfReceivedRequests} / {maxNumberOfReqRes}")
		data = await request.json()
		codesLength = len(data.get("codes"))

		# divide all codes into chunks od 1000 lines
		allCodes = '\n'.join(data.get("codes"))
		codes = allCodes.split("\n")
		data["codes"] = ["\n".join(codes[i:i+M]) for i in range(0, len(codes), M)]

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
				logging.info(f"New task sent to worker {currentWorker}. Current sent tasks status: {numberOfSentTasks}") #  / {maxNumberOfTasks}
				tasks.append(task)
				workers["workerWithId" + str(currentWorker)].append(task)
				if currentWorker == N:
					currentWorker = 1
				else:
					currentWorker += 1
			
			# collect processed tasks and log completed tasks status
			results = await asyncio.gather(*tasks)
			numberOfCompletedTasks += len(results)
			logging.info(f"Another {len(results)} more tasks completed. Current completed tasks status: {numberOfCompletedTasks}") #  / {maxNumberOfTasks}
			results = [await result.json() for result in results]
			results = [result.get("numberOfWords") for result in results]

		# log responses status
		numberOfReturnedResponses += 1
		logging.info(f"New response sent. Current sent responses status: {numberOfReturnedResponses} / {maxNumberOfReqRes}")
		
		return web.json_response({"name": "master", "status": "OK", "client": data.get("client"), "averageWordcount": round(sum(results) / codesLength, 2)}, status = 200)
	except Exception as e:
		return web.json_response({"name": "master", "error": str(e)}, status = 500)

app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port = masterPort, access_log = None)
