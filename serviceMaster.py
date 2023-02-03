# import subprocess
from aiohttp import web


routes = web.RouteTableDef()

@routes.post("/")
async def function(request):
	try:
		print("master OK")
		# calculate number of workers N (random 5 - 10)
		# call workers and give them IDs (save to dict)
		# send 1000 lines to each worker
		#  - log timestamps of tasks
		#  - count received and done tasks
		#  - send other lines to workers (100o to each) when tasks are completed

		# subprocess.call('python serviceWorker.py', creationflags=subprocess.CREATE_NEW_CONSOLE)
		return web.json_response({"name": "master", "status": "OK"}, status = 200)
	except Exception as e:
		return web.json_response({"name": "master", "error": str(e)}, status = 500)

app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port = 8080)
