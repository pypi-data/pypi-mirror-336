
import asyncio
import websockets


async def send_messages(websocket, username):
    while True:
        msg = input(f"{username}: ")
        await websocket.send(f"{username}: {msg}")

async def listen_messages(websocket):
    async for message in websocket:
        print(f"\nBroadcast: {message}")

async def send_messages(websocket, username):
    while True:
        msg = input(f"{username}: ")
        if msg.strip().lower() == "/exit":
            print("Exiting chat...")
            await websocket.close()
            break
        await websocket.send(f"{username}: {msg}")

async def connect_to_server(uri="ws://localhost:8765"):
    try:
        async with websockets.connect(uri) as websocket:
            print(f"Connected to {uri}")
            await asyncio.gather(
                listen_messages(websocket),
                send_messages(websocket)
            )
    except ConnectionRefusedError:
        print("Could not connect to server.")
