from aiohttp import web
import random
import time
import re
import string


workerPort = 8081 # 8080 (master port) + 1 (worker ID)

routes = web.RouteTableDef()

@routes.get("/")
async def function(request):
	try:
		print("worker OK")
		# wait 0.1 - 0.3 s
		randomRequestWaitTime = random.random() * 0.2 + 0.1
		print(randomRequestWaitTime)
		time.sleep(randomRequestWaitTime)

		# calculate number of words
		data = await request.json()
		words = re.sub("[" + string.punctuation + "]", "", data.get("data")).split()
		print("Words:", words)
		result = len(words)
		print("Result:", result)

		# wait 0.1 - 0.3 s
		randomResponseWaitTime = random.random() * 0.2 + 0.1
		print(randomResponseWaitTime)
		time.sleep(randomResponseWaitTime)
		
		return web.json_response({"name": "worker", "status": "OK", "numberOfWords": result}, status = 200)
	except Exception as e:
		return web.json_response({"name": "worker", "error": str(e)}, status = 500)

app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port = workerPort)
