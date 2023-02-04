import asyncio
import aiohttp
import pandas as pd


print("Running client script...\n")

# generate list of client IDs
listOfClientIDs = list(range(1, 10001))
# print(listOfClientIDs)

# load dataframe
dataframe = pd.read_json("data/dataset.json", lines = True)
# print(len(dataframe))
rowsPerClient = int(len(dataframe) / len(listOfClientIDs))
# print(rowsPerClient)

# for index, row in dataframe.iloc[10:20].iterrows():
	# print(row.get("content")[0:30])
	# print("_______________________")

# create dict for client IDs and their code
clients = {id:[] for id in listOfClientIDs}
for id, codes in clients.items():
	# print("ID:", id, codes)
	fromRow = (id - 1) * rowsPerClient
	# print(fromRow)
	toRow = fromRow + rowsPerClient
	# print(toRow)
	for index, row in dataframe.iloc[fromRow:toRow].iterrows():
		codes.append(row.get("content"))
	# print("Codes len:", len(codes))

# print(clients[69])
# print(len(clients[69]))
from itertools import islice
def take(n, iterable):
	"""Return the first n items of the iterable."""
	return dict(islice(iterable, n))
clients = take(10, clients.items())

# sending requests for code processing (variables, function, function call)
tasks = []
results = []

async def processCode():
	# make variables visible
	global tasks
	global results

	# send requests for code processing
	async with aiohttp.ClientSession() as session:
		for id, codes in clients.items():
			tasks.append(asyncio.create_task(session.get("http://127.0.0.1:8080/", json = { "user": id, "codes": codes })))
			print("Data for user", id, "with length", len(codes), "sent.")
		results = await asyncio.gather(*tasks)
		results = [await x.text() for x in results]
		print("Results of data processing for all clients retrieved.\n")

asyncio.get_event_loop().run_until_complete(processCode())

# log average number of letters for clients' code
print(results)
