import nextcord
import config
import os
from nextcord.ext import commands


intents = nextcord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix = '!', intents = intents)

@bot.event # when the bot is ready, this is what it will do 
async def on_ready():
    print(f'The bot is now online as {bot.user.name} ({bot.user.id})') # status of the bot
    print('__________________________________________________________')

    # Setting the bot's activity (custom)
    activity = nextcord.Activity(name="IbyCode's Demo", type=nextcord.ActivityType.watching)
    await bot.change_presence(activity=activity)

    

#Loading all Cogs/commands
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


bot.run(config.TOKEN)
