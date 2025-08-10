import discord
from discord.ext import commands
import requests
import os

# Load tokens from environment variables (set them in Render/Railway)
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

intents = discord.Intents.default()
intents.message_content = True  # Needed for prefix commands

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def ask(ctx, *, question: str):
    """Ask Perplexity AI a question"""
    await ctx.send("🤖 Thinking...")

    try:
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers={
                "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "sonar-pro",
                "messages": [{"role": "user", "content": question}]
            },
            timeout=15
        )

        if response.status_code != 200:
            await ctx.send(f"⚠ API Error: {response.status_code}")
            return

        data = response.json()
        if "choices" in data and data["choices"]:
            answer = data["choices"][0]["message"]["content"]
            await ctx.send(answer[:2000])  # Discord limit
        else:
            await ctx.send("⚠ No answer from Perplexity.")

    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

bot.run(DISCORD_TOKEN)
