import discord
import asyncio
import colorsys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
ROLE_ID = int(os.getenv("ROLE_ID"))

intents = discord.Intents.default()
client = discord.Client(intents=intents)

async def waving_color():
    await client.wait_until_ready()
    guild = client.get_guild(GUILD_ID)
    role = guild.get_role(ROLE_ID)

    hue = 0.0
    while not client.is_closed():
        # HSV → RGB (trả về giá trị 0–1 → nhân 255)
        r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)
        rgb_color = discord.Color.from_rgb(int(r * 255), int(g * 255), int(b * 255))
        await role.edit(color=rgb_color)

        hue += 0.01  # Tiến dần hue (vòng tròn màu)
        if hue > 1.0:
            hue = 0.0

        await asyncio.sleep(1)  # Delay mỗi bước màu (giảm để mượt hơn)

@client.event
async def on_ready():
    print(f"✅ Bot đã đăng nhập: {client.user}")
    client.loop.create_task(waving_color())

client.run(TOKEN)
