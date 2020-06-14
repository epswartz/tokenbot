import io
import discord
import matplotlib.pyplot as plt
from token_creator import create_token
from PIL import Image

class TokenBotClient(discord.Client):
    """
    Handles all the behavior of the TokenBot.
    """
    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('!token create'):
            try:
                image_url = message.content.split(" ")[2]
                token_output = create_token(image_url)
                if isinstance(token_output, str):
                    print("create_token error:", token_output)
                    await message.channel.send(token_output)
                else:
                    arr = io.BytesIO()
                    token_output.save(arr, format='PNG')
                    arr.seek(0)
                    image_file = discord.File(arr, 'token.png')
                    await message.channel.send(file=image_file)

            except Exception as e:
                print(e)
                await message.channel.send("Unknown error during token creation.")

    async def on_ready(self):
        print("Connected to Discord")
