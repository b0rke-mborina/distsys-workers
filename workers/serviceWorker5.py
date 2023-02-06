from aiohttp import web
import random
import asyncio
import re
import string


workerPort = 8085 # 8080 (master port) + 5 (worker ID)

routes = web.RouteTableDef()

@routes.get("/")
async def function(request):
	try:
		# wait 0.1 - 0.3 s (pause this coroutine only)
		randomRequestWaitTime = random.random() * 0.2 + 0.1
		await asyncio.sleep(randomRequestWaitTime)

		# calculate number of words
		data = await request.json()
		words = re.sub("[" + string.punctuation + "]", "", data.get("data")).split()
		result = len(words)

		# wait 0.1 - 0.3 s (pause this coroutine only)
		randomResponseWaitTime = random.random() * 0.2 + 0.1
		await asyncio.sleep(randomResponseWaitTime)
		
		return web.json_response({"name": "worker", "status": "OK", "numberOfWords": result}, status = 200)
	except Exception as e:
		return web.json_response({"name": "worker", "error": str(e)}, status = 500)

app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port = workerPort)
