from discord.ext import commands
from discord import Message, Embed, Colour

class GhostPing(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, ctx: Message) -> None:
        if len(ctx.mentions) >= 1 and True in [
            ctx.mentions[0] == ctx.author and len(ctx.mentions) == 1,
            ctx.mentions[0].bot and len(ctx.mentions) == 1
        ]: return
        if True in [
            ctx.author.bot,
            ctx.author.guild_permissions.manage_messages
        ]: return
        
        embed = Embed(title = "Ghost ping", timestamp = ctx.created_at, colour = Colour.random())
        embed.add_field(name = "Auteur" , value = ctx.author.mention)
        embed.add_field(name = "Message", value = ctx.content)
        embed.add_field(name="Salon:", value=f"ID: {ctx.channel.id}\n Nom: <#{ctx.channel.id}>", inline = False)

        await ctx.channel.send(embed = embed)

def setup(bot: commands.Bot) -> None:
    bot.add_cog(GhostPing(bot))