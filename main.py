from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response

# STEP 0: LOAD BOT TOKEN FROM .env 
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
SYMBOL: Final[str] = os.getenv('AWARENESS_SYMBOL')

# STEP 1: BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True #NOQA no quality assurance
client: Client = Client(intents=intents)

# STEP 2: MESSAGE FUNCTIONALITY
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('(Message was empty because intents were not enabled probably)')
        return
    
    #ignore all messages that don't begin with '?'
    if user_message[0] != SYMBOL:
        return
    
    user_message = user_message[1:]
    
    is_private: bool = user_message[0:4] == 'help'
    
    try:
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

# STEP 3: HANDLING STARTUP FOR BOT
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')

# STEP 4: HANDLING INCOMING MESSAGES
@client.event
async def on_message(message : Message) -> None:
    if message.author == client.user:   #avoid endless loop of bot responding to self
        return
    
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)

# STEP 5: MAIN ENTRY POINT
def main() -> None:
    client.run(token = TOKEN)

if __name__ == "__main__":
    main()