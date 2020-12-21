import discord
from discord.ext import commands
import traceback
import random
import datetime
import json

class Information(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Information is ready")

    @commands.command(aliases = ["guild", "guildinfo", "si"])
    async def serverinfo(self, ctx):

        findbots = sum(1 for member in ctx.guild.members if member.bot)
        roles = sum(1 for role in ctx.guild.roles)

        embed = discord.Embed(title = 'Infomation about ' + ctx.guild.name + '.', colour = ctx.author.color)
        embed.set_thumbnail(url = str(ctx.guild.icon_url))
        embed.add_field(name = "Guild's name: ", value = ctx.guild.name)
        embed.add_field(name = "Guild's owner: ", value = str(ctx.guild.owner))
        embed.add_field(name = "Guild's verification level: ", value = str(ctx.guild.verification_level))
        embed.add_field(name = "Guild's id: ", value = f"`{ctx.guild.id}`")
        embed.add_field(name = "Guild's member count: ", value = f"{ctx.guild.member_count}")
        embed.add_field(name="Bots", value=f"`{findbots}`", inline=True)
        embed.add_field(name = "Guild created at: ", value = str(ctx.guild.created_at.strftime("%a, %d %B %Y, %I:%M %p UTC")))
        embed.add_field(name = "Number of Roles:", value = f"`{roles}`")

        # check if they have automod enabled or disabled
        with open("./data/automod.json", "r") as f:
            guilds = json.load(f)

        if str(ctx.guild.id) not in guilds: # they never set it up
            embed.add_field(name = "Automod Status:", value = f"`Not set up`")
        else:
            if guilds[str(ctx.guild.id)]["automod"] == "true":
                embed.add_field(name = "Automod Status:", value = f"`True`")
            elif guilds[str(ctx.guild.id)]["automod"] == "false":
                embed.add_field(name = "Automod Status:", value = f"`False`")

        await ctx.send(embed =  embed)

    @commands.command(aliases = ["ci"])
    async def channelinfo(self, ctx, channel : discord.TextChannel = None):
        if channel == None:
            channel = ctx.channel
        nsfw = self.client.get_channel(channel.id).is_nsfw()
        news = self.client.get_channel(channel.id).is_news()
        embed = discord.Embed(title = 'Channel Infromation: ' + str(channel),
        colour = discord.Colour.from_rgb(54, 151, 255))
        embed.add_field(name = 'Channel Name: ', value = str(channel.name))
        embed.add_field(name = "Channel's NSFW Status: ", value = str(nsfw))
        embed.add_field(name = "Channel's id: " , value = str(channel.id))
        embed.add_field(name = 'Channel Created At: ', value = str(channel.created_at.strftime("%a, %d %B %Y, %I:%M %p UTC")))
        embed.add_field(name = 'Channel Type: ', value = str(channel.type))
        embed.add_field(name = "Channel's Announcement Status: ", value = str(news))
        await ctx.send(embed = embed)

    @commands.command()
    async def userinfo(self, ctx, member : discord.Member = None):
        if member == None:
            member = ctx.author
        pos = sum(m.joined_at < member.joined_at for m in ctx.guild.members if m.joined_at is not None)
        roles = [role for role in member.roles]
        embed = discord.Embed(color=member.color, timestamp=datetime.datetime.utcnow())
        embed.set_author(name=f"{member}", icon_url=member.avatar_url)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="Joined at:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p"))
        embed.add_field(name='Registered at:', value=member.created_at.strftime('%a, %#d %B %Y, %I:%M %p'))
        embed.add_field(name='Bot?', value=f'{member.bot}')
        embed.add_field(name='Status?', value=f'{member.status}')
        embed.add_field(name='Top Role?', value=f'{member.top_role}')
        embed.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles[:1]]))
        embed.add_field(name='Join position', value=pos)
        embed.set_footer(icon_url=member.avatar_url, text=f'Requested By: {ctx.author.name}')
        await ctx.send(embed=embed)

    @commands.command()
    async def whois(ctx, user : discord.Member = None):
        if user == None:
            user = ctx.author
        em = discord.Embed(title = user.name, color = user.color)
        em.add_field(name = "ID:", value = user.id)
        em.set_thumbnail(url = user.avatar_url)
        await ctx.send(embed = em)

    @commands.command(aliases = ["bi"])
    async def botinfo(self, ctx):
        embed = discord.Embed(title = "Botinfo", color = ctx.author.color,
        description = "TheImperialGod, is an awesome customizable discord bot with awesome features. Check some information about the bot below!"
        )
        embed.add_field(name = "First went live on:", value = "1 / 10 / 2020")
        embed.add_field(name = "Started coding on:", value = "26 / 9 / 2020")
        embed.add_field(name = f"Creator", value = f"NightZan999#0194")
        embed.add_field(name = 'Hosting', value = f"Chaotic Destiny Hosting.")
        embed.add_field(name = "Servers:", value = f'`{len(self.client.guilds)}` epic guilds I\'m in!')
        embed.add_field(name = 'Customizable Settings:', value = f"Automoderation and utilities! ")
        embed.add_field(name = "Database:", value = "SQLite3")
        embed.add_field(name = "Website:", value = "https://theimperialgod.herokuapp.com\nNOTE: not hosted yet!")
        embed.add_field(name = "Number of Commands:", value = f"`80` (including special owner commands)")
        embed.add_field(name = "**Tech:**", value = "```+ Library : discord.py\n+ Database : SQLite3\n+ Hosting Services : Chaotic Destiny Hosting!\n```", inline = False)
        embed.add_field(name = "Users:", value = f'`{len(self.client.users)}`')
        await ctx.send(embed = embed)

    @commands.command()
    async def ping(self, ctx):
        embed = discord.Embed(title = ":ping_pong: Pong!", color = ctx.author.color)
        embed.add_field(name=  "Client Latency", value = f"`{self.client.latency}`")
        embed.add_field(name = "API Latency", value = f"`{random.randint(1, 20)}`")
        embed.add_field(name = "Description:", value = "The client latency tells you how fast the bot is. For every command the latency goes down by about 5\nLatency starts at 1000!\n\nThe API latency will tell you how the API reacts to the client latency, the higher the API latency the better!")
        await ctx.send(embed = embed)


def setup(client):
    client.add_cog(Information(client))
