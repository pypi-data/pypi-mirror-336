import asyncio
import websockets

connected_clients = set()

async def handler(websocket, path):
    connected_clients.add(websocket)
    print("New client connected")
    try:
        async for message in websocket:
            print(f"Received: {message}")
            await broadcast(message)
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    finally:
        connected_clients.remove(websocket)

async def broadcast(message):
    if connected_clients:
        await asyncio.gather(*(client.send(message) for client in connected_clients))

def start_server(host="localhost", port=8765):
    print(f"Starting server at ws://{host}:{port}")
    server = websockets.serve(handler, host, port)
    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()
