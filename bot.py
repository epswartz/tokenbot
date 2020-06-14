import os
import discord
from dotenv import load_dotenv
from token_client import TokenBotClient

# Create discord bot user
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = TokenBotClient()

print("TokenBot Initializing...")
client.run(TOKEN)
