from discord import application_command, Option, Embed, Colour, Activity, ActivityType, Intents, Message, Game
from discord.ext import commands, tasks
from logger import logger
from json import load as json_load
from time import time
import random 
import extender 

config = json_load(open("config.json", "r"))
start = int(time())  
bot = commands.Bot(intents = Intents.all())
bot.remove_command("help")
extender.setup(bot)

def create_embed(title: str, description: str, author: str, color: Colour):
    embed = Embed(title=title, description=description, colour=color)
    embed.set_footer(text=f"Informations demandées par : {author}")
    return embed

@tasks.loop(minutes=10)
async def change_activity():
    bot.changeable_activites = [f"être sur {len(bot.guilds)} serveurs", "regarder Start from Scratch", "Apex Legends", "Minecraft", "regarder loyds44", "coder", "discuter avec des utilisateurs", "écouter de la musique", "aider les utilisateurs", "gérer des statistiques", "analyser des données", "apprendre de nouvelles choses", "aller à la salle", "se rappeler de scratch on scratch", "écouter de la hardbass", "quelquechose avec quelqu'un"]
    await bot.wait_until_ready()
    await bot.change_presence( activity=Game(random.choice(bot.changeable_activites))) 

@bot.event
async def on_ready() -> None:
  logger.info(f"Logged in as {bot.user.name}.")

  for channel_id in config["status_channels_ids"]:
    await bot.get_channel(channel_id).send(f"Le bot est connecté en tant que {bot.user.mention} :green_circle: (Version Beta)")

  change_activity.start()

@bot.slash_command(
  name = "say",
  description = "Fais dire quelque chose au bot."
)
@commands.has_permissions(administrator = True)
async def say(
  ctx: application_command(), 
  message: Option(str)
) -> None:
  await ctx.delete()
  await ctx.channel.send(message)

@bot.slash_command(
    name = "infos",
    description = "Avoir des Informations sur le bot" 
)
async def infos(ctx: application_command()):
    embed = create_embed("Infos", f"Le ping du bot {bot.user.mention} est de {int(bot.latency * 1000)}ms \n A été lancé <t:{start}:R> | Le <t:{start}:F> \n Actuellement dans {len(bot.guilds)} serveur(s)", ctx.author.name, 0x008FFF)
    await ctx.respond(embed=embed)

@bot.slash_command(
    name = "ping",
    description = "Avoir le ping du bot" 
)
async def ping(ctx: application_command()) -> None:
    embed = create_embed("Ping", f"Le ping du bot {bot.user.mention} est de {int(bot.latency * 1000)}ms", ctx.author.name, 0xFFA900)
    await ctx.respond(embed=embed)

@bot.slash_command(
    name = "help",
    description = "Liste des commandes disponibles" 
)
async def help(ctx: application_command()) -> None:
    embed = create_embed("Help", f"Commandes Disponible : \n `/ping` - Avoir le ping du bot \n `/infos` - Avoir des Informations sur le bot \n `/help` - Liste des commandes disponibles \n `/say` - Fais dire quelque chose au bot (admin only) \n `/embed` - Crée un embed", ctx.author.name, 0x200B9C)
    await ctx.respond(embed=embed)

@bot.slash_command(
    name= "embed",
    description="Crée un embed" 
)
async def embed(
  ctx: application_command(), 
  titre: Option(str), 
  description: Option(str),
) -> None:
  embed = create_embed(titre, description, ctx.author.name,0x093156)
  await ctx.respond(embed=embed)

@bot.slash_command(
  name= "serveur",
  description="Avoir des informations sur le serveur" 
)
async def serveur(ctx: Message) -> None:
  roles_list = " | ".join((f"<@&{role.id}>" for role in list(reversed(ctx.guild.roles))[:35]))
  if len(ctx.guild.roles) >= 35:
     roles_list += " **et plus**"
  embed = create_embed(ctx.guild.name, f"Information sur le serveur {ctx.guild.name} (`{ctx.guild.id}`)", ctx.author.name, 0x1DB747)
  embed.add_field(name="Création du serveur:", value=f"<t:{int(ctx.guild.created_at.timestamp())}:F>", inline = True)
  embed.add_field(name="Proprietaire:", value=f"{ctx.guild.owner.mention} (`{ctx.guild.owner.id}`)", inline = True)
  embed.add_field(name=f"{len(ctx.guild.roles)} roles:", value=roles_list, inline = False)
  embed.add_field(name="Statistiques:",value=f"Nombre de membres: {ctx.guild.member_count} \n Nombre de salons textuels: {len(ctx.guild.text_channels)} \n Nombre de salons vocaux: {len(ctx.guild.voice_channels)}", inline = False)
  await ctx.respond(embed=embed)

bot.run(config["token"])