import discord
from discord.ext import commands, tasks
import datetime

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

birthday_data = {
    "123456789012345678": "2005-10-10",
    "987654321098765432": "2004-04-01"
}


@bot.command(name="setbirthday")
async def set_birthday(ctx, user: discord.User, birthdate: str):
    try:
        datetime.datetime.strptime(birthdate, '%Y-%m-%d')
        
        birthday_data[str(user.id)] = birthdate
        
        await ctx.send(f"Birthday for {user.name} set to {birthdate}")
    except ValueError:
        await ctx.send("Invalid date format. Please use YYYY-MM-DD.")

async def check_birthdays():
    today = datetime.datetime.now().strftime('%m-%d')
    for user_id, birthdate in birthday_data.items():
        birth_month_day = birthdate[5:] 
        if birth_month_day == today:
            user = bot.get_user(int(user_id))
            if user:
                for guild in bot.guilds:
                    for channel in guild.text_channels:
                        await channel.send(f"🎉 **Happy Birthday, {user.name}!** 🎂")

@tasks.loop(hours=24)
async def birthday_task():
    await check_birthdays()

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    birthday_task.start()  

token = "####"
bot.run('YOUR_DISCORD_BOT_TOKEN')
