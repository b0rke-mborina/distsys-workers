import asyncio
import aiohttp
import pandas as pd


print("client OK")

# generate list of client IDs
listOfClientIDs = list(range(1, 10001))
print(listOfClientIDs)

# load dataframe
dataframe = pd.read_json("data/dataset.json", lines = True)

# create dict for client IDs and their code

# send requests for code processing
async def processCode():
	async with aiohttp.ClientSession() as session:
		print("OK")

asyncio.run(processCode())

# log average number of letters for clients' code
