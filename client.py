import asyncio
import aiohttp
import pandas as pd

print("Running client script...\n")

# generate list of client IDs
listOfClientIDs = list(range(1, 10001))
# print(listOfClientIDs, "\n")

# load dataframe
print("Loading dataframe...\n")
dataframe = pd.read_json("data/dataset.json", lines = True)
print("Dataframe loaded.\n")
# print(len(dataframe), "\n")

# calculate rows per client
rowsPerClient = int(len(dataframe) / len(listOfClientIDs)) # 10
# print(rowsPerClient, "\n")

# print start of code (for check only - DELETE AT END)
# for index, row in dataframe.iloc[10:20].iterrows():
	# print(row.get("content")[0:30])
	# print("_______________________")

# create dict for client IDs and their code (by calculating row indices in dataframe and adding code from rows as value to ID property)
clients = {id:[] for id in listOfClientIDs}
for id, codes in clients.items():
	# print("ID:", id, codes)
	fromRow = (id - 1) * rowsPerClient
	# print("Start:", fromRow + 1)
	toRow = fromRow + rowsPerClient
	# print("End:", toRow)
	for index, row in dataframe.iloc[fromRow + 1:toRow + 1].iterrows():
		codes.append(row.get("content"))
	# print("Codes len:", len(codes), "\n")

# take limited amount of clients (for check only - DELETE AT END)
# print(clients[69])
# print(len(clients[69]), "\n")
from itertools import islice
def take(n, iterable):
	"""Return the first n items of the iterable."""
	return dict(islice(iterable, n))
# clients = take(5000, clients.items())

# sending requests for code processing (variables, function, function call)
tasks = []
results = []

async def processCode():
	# make variables visible
	global tasks
	global results

	# send requests for code processing
	print("Sending data...\n")
	async with aiohttp.ClientSession(connector = aiohttp.TCPConnector(ssl = False)) as session:
		for id, codes in clients.items():
			tasks.append(asyncio.create_task(session.get("http://127.0.0.1:8080/", json = { "client": id, "codes": codes })))
			# print("Task for client", id, "with length", len(codes), "sent.")
		print("Data sent.\n")
		print("Waiting for all responses...\n")
		results = await asyncio.gather(*tasks)
		results = [await x.json() for x in results]
		print("Results of data processing for all clients retrieved.\n")

asyncio.get_event_loop().run_until_complete(processCode())

# log average number of letters for clients' code
# print(results, "\n")
processedDataItem = {}
for result in results:
	print("Average code lenght for client with ID", result.get("client"), "is", result.get("averageWordcount"))
# print("Length:", len(results), "\n")
