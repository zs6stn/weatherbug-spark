from telnetserver import TelnetServer
from weatherbug import WeatherBug
import asyncio

server = TelnetServer()
weatherBug = WeatherBug()

clients = []

async def runServer():
    while True:
        # Make the server parse all the new events
        server.update()

        # For each newly connected client
        for new_client in server.get_new_clients():
            # Add them to the client list 
            clients.append(new_client)
            # Send lightning stats
            result = await weatherBug.getLightningStrikes()
            server.send_message(new_client, result)
            server._handle_disconnect(new_client)

        # For each client that has recently disconnected
        for disconnected_client in server.get_disconnected_clients():
            if disconnected_client not in clients:
                continue

            # Remove him from the clients list
            clients.remove(disconnected_client)

            # Send every client a message saying "Client X disconnected"
            for client in clients:
                server.send_message(client, "Client {} disconnected.".format(disconnected_client))

        # For each message a client has sent
        for sender_client, message in server.get_messages(): 
            if sender_client not in clients:
                continue

            # Send every client a message reading: "I received "[MESSAGE]" from client [ID OF THE SENDER CLIENT]"
            for client in clients:
                server.send_message(client, 'I received "{}" from client {}'.format(message, sender_client))

asyncio.run(runServer())