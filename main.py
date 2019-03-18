import os
import discord

from dotenv import load_dotenv

#dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

load_dotenv(verbose=True)

print(os.getenv("test"))