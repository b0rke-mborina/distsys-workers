from aiohttp import web


workerPort = 8081 # 8080 (master port) + 1 (worker ID)

routes = web.RouteTableDef()

@routes.post("/")
async def function(request):
	try:
		print("worker OK")
		# wait 0.1 - 0.3 s
		# calculate number of words
		# wait 0.1 - 0.3 s
		return web.json_response({"name": "worker", "status": "OK"}, status = 200)
	except Exception as e:
		return web.json_response({"name": "worker", "error": str(e)}, status = 500)

app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port = workerPort)
