import discord
import asyncio
import colorsys
import os
import logging
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
ROLE_ID = int(os.getenv("ROLE_ID"))
SLEEP_INTERVAL = int(os.getenv("SLEEP_INTERVAL", 10))  # Time between color changes in seconds

# Define intents
intents = discord.Intents.default()
intents.guilds = True

# Create Discord client
client = discord.Client(intents=intents)

async def rainbow_role_color():
    await client.wait_until_ready()

    # Fetch the guild (server)
    try:
        guild = await client.fetch_guild(GUILD_ID)
    except Exception as e:
        logging.error(f"Error fetching guild: {e}")
        return

    # Find the role by ID
    role = None
    try:
        roles = await guild.fetch_roles()
        for r in roles:
            if r.id == ROLE_ID:
                role = r
                break
    except Exception as e:
        logging.error(f"Error fetching roles: {e}")
        return

    if role is None:
        logging.error("Role not found!")
        return

    hue = 0.0
    while not client.is_closed():
        r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)
        rgb_color = discord.Color.from_rgb(int(r * 255), int(g * 255), int(b * 255))

        try:
            await role.edit(color=rgb_color)
        except discord.Forbidden:
            logging.error("Bot lacks permission to edit the role!")
            return
        except Exception as e:
            logging.error(f"Error editing role color: {e}")
            return

        hue = (hue + 0.05) % 1.0  # Keep hue in [0.0, 1.0]
        await asyncio.sleep(SLEEP_INTERVAL)

@client.event
async def on_ready():
    logging.info(f"✅ Bot connected as: {client.user}")
    client.loop.create_task(rainbow_role_color())

# Run the bot
client.run(TOKEN)
# Note: Make sure to set the environment variables DISCORD_TOKEN, GUILD_ID, ROLE_ID, and SLEEP_INTERVAL in your .env file.