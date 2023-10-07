import os
TOKEN = os.environ['TOKEN']

from app import stay_alive
from settings import database, set_scam_delete, get_scam_delete, set_verified_role, get_verified_role
from tagbase import tagbase, tag_create
from lvlsystem import lvlsystem, get_xp
import json
import random
import datetime
import psutil

import discord
from discord import app_commands
from discord import ui

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

#sync command
@client.event
async def on_guild_join():
  await tree.sync()
  
#ping command
@tree.command(name = "ping", description = "See how fast I reply")
async def first_command(interaction):
    latency = round(client.latency * 1000)
    embed = discord.Embed(
      title = "Pong!",
      description = f"It took me {latency} ms to reply!",
      color = discord.Color.green()
    )
    await interaction.response.send_message(embed=embed)

#help command
@tree.command(
  name = "help", 
  description = "Get help by the bot!"
)
async def help(interaction):
  embed = discord.Embed(
    title = "Help",
    description = "",
    color = discord.Color.blue()
  )
  embed.add_field(
    name="/ping",
    value="See how fast I can reply!"
  )
  embed.add_field(
    name="/verify",
    value="Verify yourself to the server!"
  )
  embed.add_field(
    name="/rps",
    value="Play a game of rock paper scissors!"
  )
  embed.add_field(
    name="/8ball",
    value="Ask the bot anythin and it will answer in a span from yes to no!"
  )
  await interaction.response.send_message(embed=embed, ephemeral=True)

#set verified role
@tree.command(
  name="settings_verified",
  description="Set the role id for your member/verified role!"
)
async def set_verified(interaction, role_id: str):
  user = interaction.user
  guild_id = str(interaction.guild.id)
  if role_id:
    await set_verified_role(guild_id, role_id)
    embed = discord.Embed(
      title = "Successfuly Updated!",
      description = f"successfuly set role_id to {role_id}",
      color = discord.Color.green()
    )
    await interaction.response.send_message(embed=embed)
  else:
    return

#verified role
@tree.command(
  name="verify",
  description="Verify yourself to enter the server!"
)
async def verify(interaction):
  user = interaction.user
  avatar_url = user.avatar
  guild_id = str(interaction.guild.id)
  role_id = await get_verified_role(guild_id)
  if role_id:
    role = discord.utils.get(interaction.guild.roles, id=int(role_id))
    if role:
      await user.add_roles(role)
      embed = discord.Embed(
        title = f"Welcome {user.mention}!",
        description = "Welcome to the Server! We hope you'll have a nice stay here!",
        color = discord.Color.blue()
      )
      embed.set_image(url=avatar_url)
      await interaction.response.send_message(embed=embed)
    else:
      embed = discord.Embed(
        title="Error",
        description="We didn't find the role you're searching for! Try again later!",
        color = discord.Color.red()
      )
      await interaction.response.send_message(embed=embed)
  else:
    embed = discord.Embed(
      title="Error",
      description="We didn't find the role you're searching for! Try again later!",
      color = discord.Color.red()
    )
    await interaction.response.send_message(embed=embed)

    
#scam delete
@tree.command(
  name="settings_delete",
  description="Set up your scam decision"
)
async def set_scamdelete(interaction, delete: str):
  if delete == "true":
    guild_id = interaction.guild.id
    await set_scam_delete(guild_id, delete)
    embed = discord.Embed(
      title = "Succesfully Updated",
      description = f"Set deletion of scam links to {delete}",
      color = discord.Color.green()
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)
  if delete == "false":
    guild_id = interaction.guild.id
    await set_scam_delete(guild_id, delete)
    embed = discord.Embed(
      title = "Succesfully Updated",
      description = f"Set deletion of scam links to {delete}",
      color = discord.Color.green()
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)
  
#on_message (antiscam)
@client.event
async def on_message(ctx):
    user = ctx.author
    if user.bot:
        return
    channel = ctx.channel
    guild_id = str(ctx.guild.id)
    delete = await get_scam_delete(guild_id)
    with open('antiscam.json', 'r') as file:
        scam_links = json.load(file)
    for scam_link in scam_links:
        if scam_link in ctx.content:
            if delete == "true":
                embed = discord.Embed(
                    title=f"{user.mention} sent a dangerous link!",
                    description=f"The user sent a link that will harm other users. Match: {scam_link}",
                    color=discord.Color.red()
                )
                embed.add_field(
                    name=f"{user}'s message:'",
                    value=f"{ctx.content}"
                )
                await ctx.delete()
                await channel.send(embed=embed)
            if delete == "false":
                embed = discord.Embed(
                    title="Warning! Possible scam link detected!",
                    description=f"{user.mention} sent a possible scam link. It's advisable not to click on the link!",
                    color=discord.Color.red()
                )
                await channel.send(embed=embed)
                break

#8ball game
@tree.command(
  name = "8ball",
  description = "What will the holy ball say to your question?",
)
async def ball(interaction, question: str):
  user = interaction.user
  guess = random.randint(1,8)
  if guess == 1:
    embed = discord.Embed(
      title = "The holy 8ball",
      description = "",
      color = discord.Color.red()
    )
    embed.add_field(
      name = f"{user.mention} asked:",
      value = f"{question}"
    )
    embed.add_field(
      name = "8ball says:",
      value = "no."
    )
    await interaction.response.send_message(embed=embed)
  if guess == 2:
    embed = discord.Embed(
      title = "The holy 8ball",
      description = "",
      color = discord.Color.blue()
    )
    embed.add_field(
      name = f"{user.mention} asked:",
      value = f"{question}"
    )
    embed.add_field(
      name = "8ball says:",
      value = "maybe"
    )
    await interaction.response.send_message(embed=embed)
  if guess == 3:
    embed = discord.Embed(
      title = "The holy 8ball",
      description = "",
      color = discord.Color.green()
    )
    embed.add_field(
      name = f"{user.mention} asked:",
      value = f"{question}"
    )
    embed.add_field(
      name = "8ball says:",
      value = "yes"
    )
    await interaction.response.send_message(embed=embed)
  if guess == 4:
    embed = discord.Embed(
      title = "The holy 8ball",
      description = "",
      color = discord.Color.blue()
    )
    embed.add_field(
      name = f"{user.mention} asked:",
      value = f"{question}"
    )
    embed.add_field(
      name = "8ball says:",
      value = "of course!"
    )
    await interaction.response.send_message(embed=embed)
  if guess == 5:
    embed = discord.Embed(
      title = "The holy 8ball",
      description = "",
      color = discord.Color.red()
    )
    embed.add_field(
      name = f"{user.mention} asked:",
      value = f"{question}"
    )
    embed.add_field(
      name = "8ball says:",
      value = "hell no 💀"
    )
    await interaction.response.send_message(embed=embed)
  if guess == 6:
    embed = discord.Embed(
      title = "The holy 8ball",
      description = "",
      color = discord.Color.blue()
    )
    embed.add_field(
      name = f"{user.mention} asked:",
      value = f"{question}"
    )
    embed.add_field(
      name = "8ball says:",
      value = "I dont care."
    )
    await interaction.response.send_message(embed=embed)
  if guess == 7:
    embed = discord.Embed(
      title = "The holy 8ball",
      description = "",
      color = discord.Color.orange()
    )
    embed.add_field(
      name = f"{user.mention} asked:",
      value = f"{question}"
    )
    embed.add_field(
      name = "8ball says:",
      value = "I can't say"
    )
    await interaction.response.send_message(embed=embed)
  if guess == 8:
    embed = discord.Embed(
      title = "The holy 8ball",
      description = "",
      color = discord.Color.yellow()
    )
    embed.add_field(
      name = f"{user.mention} asked:",
      value = f"{question}"
    )
    embed.add_field(
      name = "8ball says:",
      value = "okay."
    )
    await interaction.response.send_message(embed=embed)

#rps command
@tree.command(name="rps", description="Play a game of rock paper scissors")
async def rps(interaction, choice: str):
  user = interaction.user
  guess = random.randint(1,3)
  if choice == "rock":
    if guess == 1:
      embed = discord.Embed(
        title = "Draw",
        description = "I have chosen rock too!",
        color = discord.Color.blue()
      )
      await interaction.response.send_message(embed=embed)
    elif guess == 2:
      embed = discord.Embed(
        title = "Lost",
        description = "I have chosen paper!",
        color = discord.Color.red()
      )
      await interaction.response.send_message(embed=embed)
    elif guess == 3:
      embed = discord.Embed(
        title = "Won",
        description = "I have chosen scissors, GG",
        color = discord.Color.green()
      )
      await interaction.response.send_message(embed=embed)
  elif choice == "paper":
    if guess == 1:
      embed = discord.Embed(
        title = "Won",
        description = "I have chosen rock, GG",
        color = discord.Color.green()
      )
      await interaction.response.send_message(embed=embed)
    elif guess == 2:
      embed = discord.Embed(
        title = "Draw",
        description = "I have chosen paper too!",
        color = discord.Color.blue()
      )
      await interaction.response.send_message(embed=embed)
    elif guess == 3:
      embed = discord.Embed(
        title = "Lost",
        description = "I have chosen scissors!",
        color = discord.Color.red()
      )
      await interaction.response.send_message(embed=embed)
  elif choice == "scissors":
    if guess == 1:
      embed = discord.Embed(
        title = "Lost",
        description = "I have chosen rock!",
        color = discord.Color.red()
      )
      await interaction.response.send_message(embed=embed)
    elif guess == 2:
      embed = discord.Embed(
        title = "Won",
        description = "I have chosen paper, GG",
        color = discord.Color.green()
      )
      await interaction.response.send_message(embed=embed)
    elif guess == "3":
      embed = discord.Embed(
        title = "Draw",
        description = "I have chosen scissors too!",
        color = discord.Color.blue()
      )
      await interaction.response.send_message(embed=embed)

# tag create command
@tree.command(name="tag_create", description="Create a shorthand tag!")
async def tagcreate(interaction, tagname: str, tagcontent: str):
  user = interaction.user.display_name
  guild_id = interaction.guild.id
  check = await tag_check(guild_id, tagname)
  if check == None:
    await tag_create(guild_id, tagname, tagcontent, user)
    embed = discord.Embed (
      title = "Tag created!",
      description = f"{tagname} successfully created!",
      color = discord.Color.green()
    )
    embed.add_field(
      name = "Tag Content:",
      value = f"{tagcontent}"
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)
  else:
    embed = discord.Embed(
      title = "Already existing!",
      description = f"The tag {tagname} is already existing!",
      color = discord.Color.red()
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)

# tag command
class reportButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label='Report', style=discord.ButtonStyle.danger, custom_id="reportButton")

    @discord.ui.button(label='Report', style=discord.ButtonStyle.danger)
    async def report(self, button: discord.ui.Button, interaction: discord.Interaction):
        print("Button Clicked!")
        await interaction.response.send_message('Report button pressed!', ephemeral=True)

@tree.command(name="tag", description="Use a shortcut tag!")
async def tag(interaction, tagname: str):
    guild_id = interaction.guild.id
    content = await tag_get(guild_id, tagname)
    user = await tag_name(guild_id, tagname)

    if content is not None and user is not None:
        view = discord.ui.View()
        view.add_item(reportButton())
      
        embed = discord.Embed(
            title=f"Tag: {tagname}",
            description=f"{content}",
            color=discord.Color.blue()
        )
        embed.set_footer(
            text=f"{user} created this command"
        )
        await interaction.response.send_message(embed=embed, view=view)
    else:
        embed = discord.Embed(
            title="Tag not found!",
            description=f"{tagname} isn't registered, maybe a typo?",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)

#info command
class repoButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label='Open source', style=discord.ButtonStyle.link, url="https://github.com/KayDavKal/Manager_bot")
          
@tree.command(name="info", description="See stats about the Bot!")
async def info(interaction):
  view = discord.ui.View()
  view.add_item(repoButton())
  
  latency = round(client.latency * 1000)
  server_count = len(client.guilds)
  
  uptime = datetime.datetime.utcnow() - client.start_time
  days, hours, minutes, seconds = uptime.days, uptime.seconds // 3600, (uptime.seconds // 60) % 60, uptime.seconds % 60

  process = psutil.Process()
  memory_usage = process.memory_info().rss / (1024 ** 2)

  embed = discord.Embed(
    title = "Bot Informations",
    color = discord.Color.blue()
  )
  embed.add_field(
    name = "Bot Version",
    value = "```1.0.17```",
    inline = True
  )
  embed.add_field(
    name = "Bot Owner",
    value = "```KayDavKal```",
    inline = True
  )
  embed.add_field(
    name = "Ping",
    value = f"```{latency}ms```",
    inline = True
  )
  embed.add_field(
    name = "Servers",
    value = f"```{server_count}```",
    inline = True
  )
  embed.add_field(
    name = "Uptime",
    value = f"```{uptime}```",
    inline = True
  )
  embed.add_field(
    name = "Memory Usage",
    value = f"```{memory_usage: .2f} MB```",
    inline = True
  )
  embed.add_field(
    name = "Library Version",
    value = f"```Discord.py {discord.__version__}```",
    inline = True
  )
  await interaction.response.send_message(embed=embed, view=view)
  
#BOT ONLINE
@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")
    stay_alive()
    await database()
    await tagbase()
    await lvlsystem()
  
client.run(TOKEN)
