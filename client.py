import asyncio
import aiohttp
import pandas as pd


print("Running client script...\n")

# generate list of client IDs
listOfClientIDs = list(range(1, 10001))

# load dataframe
print("Loading dataframe...\n")
dataframe = pd.read_json("data/dataset.json", lines = True)
print("Dataframe loaded.\n")

# calculate rows per client
rowsPerClient = int(len(dataframe) / len(listOfClientIDs)) # 10

# create dict for client IDs and their code (by calculating row indices in dataframe and adding code from rows as value to ID property)
clients = {id:[] for id in listOfClientIDs}
for id, codes in clients.items():
	fromRow = (id - 1) * rowsPerClient
	toRow = fromRow + rowsPerClient
	for index, row in dataframe.iloc[fromRow + 1:toRow + 1].iterrows():
		codes.append(row.get("content"))

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
		print("Data sent.\n")
		print("Waiting for all responses...\n")
		results = await asyncio.gather(*tasks)
		results = [await x.json() for x in results]
		print("Results of data processing for all clients retrieved.\n")

asyncio.get_event_loop().run_until_complete(processCode())

# log average number of letters for clients' code
processedDataItem = {}
for result in results:
	print("Average code lenght for client with ID", result.get("client"), "is", result.get("averageWordcount"))
