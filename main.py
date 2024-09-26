
import discord
from discord.ext import commands
import openai
import keys

intents = discord.Intents.default()
intents.message_content = True

# KEYS
DISCORD_TOKEN = keys.TOKEN
openai.api_key = keys.OPENAI_KEY

# Define the ID of the channel where the bot should respond
ALLOWED_CHANNEL_ID = 1111111111111111111  # Replace with your specific channel ID

# Initialize bot with command prefix and intents
bot = commands.Bot(command_prefix="!", intents=intents)

# Function that sends message to OpenAI API and gets responses
async def ask_gpt(question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": question}
            ]
        )
        answer = response.choices[0].message['content']
        return answer
    except Exception as e:
        return f"Error: {str(e)}"

# Define the /ask slash command
@bot.command(name='ask', help='Ask a question to GPT')
async def ask(ctx, *, question: str):
    # Check if the command is being used in the allowed channel
    if ctx.channel.id != ALLOWED_CHANNEL_ID:
        await ctx.send("You can only use this command in the designated channel.")
        return

    response = await ask_gpt(question)
    await ctx.send(response)

# Notify when the bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# Run the bot
bot.run(DISCORD_TOKEN)
