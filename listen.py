import asyncio
import websockets
import datetime

CHANNEL = "#miia"
BOT_USERNAME = "justinfan12345"

FILE_NAME = CHANNEL[1:] + "_STREAM_LOG_" + datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S") + ".txt"

async def record_chat():
    uri = "wss://irc-ws.chat.twitch.tv:443"

    try:
        async with websockets.connect(uri) as websocket:
            print(f"Connecting to {CHANNEL} as {BOT_USERNAME}...")

            await websocket.send(f"PASS ASGP")
            await websocket.send(f"NICK {BOT_USERNAME}")
            await websocket.send(f"JOIN {CHANNEL}")

            print(f"Connected to {CHANNEL} as {BOT_USERNAME}")

            while True:
                try:
                    message = await websocket.recv()

                    if message.startswith("PING"):
                        await websocket.send("PONG :tmi.twitch.tv")
                        continue

                    if "PRIVMSG" in message:
                        username = message.split("!", 1)[0][1:]
                        content = message.split("PRIVMSG", 1)[1].split(":", 1)[1]
                        timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

                        log_line = f"[{timestamp}] {username}: {content.strip()}"
                        print(log_line)

                        with open(FILE_NAME, "a", encoding="utf-8") as file:
                            file.write(log_line + "\n")

                except websockets.ConnectionClosed:
                    print("Connection closed. Retrying...")
                    break

    except Exception as e:
        print(f"Connection error: {e}")




async def main():
    while True:
        await record_chat()
        print("Reconnecting in 2 seconds...")
        await asyncio.sleep(2)


asyncio.run(main())