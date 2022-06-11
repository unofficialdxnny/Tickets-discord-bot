from discord.ext import commands
import subprocess
import threading
import discord
import asyncio
import ctypes


ctypes.windll.kernel32.SetConsoleTitleW('Moon™')
TOKEN = ''
prefix = '/'
intents = discord.Intents().all()
bot = commands.Bot(command_prefix=prefix, case_insensitive=True, intents=intents)
bot.remove_command('help')



def zoom():
    while True:
        try:
            task, arg1, arg2 = queue.pop(0).split('-')
            subprocess.run([f'{task}', f'{arg1}', f'{arg2}'])
        except:
            pass

threading.Thread(target=zoom).start()

@bot.event
async def on_ready():
    print(f'Servers: {len(bot.guilds)}')
    for guild in bot.guilds:
        print(guild.name)
    print()
    while True:
        members = sum([guild.member_count for guild in bot.guilds])
        activity = discord.Activity(type=discord.ActivityType.watching, name=f'{members} users!')
        await bot.change_presence(activity=activity)
        await asyncio.sleep(60)

@bot.event
async def on_member_join(member):
    channel = await bot.fetch_channel(bots_channel)
    await member.send(f'Welcome to **Moon™**, {member.mention}.\nType `/help` to get started!')

@bot.event
async def on_command_error(ctx, error: Exception):
    if ctx.channel.id == bots_channel:
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(color=16379747, description=f'{error}')
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(color=16379747, description='Missing arguments required to run this command!')
            await ctx.send(embed=embed)
            ctx.command.reset_cooldown(ctx)
        elif 'You do not own this bot.' in str(error):
            embed = discord.Embed(color=16379747, description='You **DONT** permission to run this command!')
            await ctx.send(embed=embed)
        else:
            print(str(error))
    else:
        try:
            await ctx.message.delete()
        except:
            pass

@bot.command()
async def help(ctx):
    print(f'{ctx.author} | {ctx.author.id} -> /help')
    if ctx.channel.type != discord.ChannelType.private:
        embed = discord.Embed(color=16379747)
        embed.add_field(name='Help', value='`/help`', inline=True)
        embed.add_field(name='Open Ticket', value='`/ticket`', inline=True)
        embed.add_field(name='Close Ticket', value='`/close`', inline=True)
        await ctx.send(embed=embed)

@bot.command()
async def ticket(ctx):
    print(f'{ctx.author} | {ctx.author.id} -> /ticket')
    if ctx.channel.type != discord.ChannelType.private:
        channels = [str(x) for x in bot.get_all_channels()]
        if f'ticket-{ctx.author.id}' in str(channels):
            embed = discord.Embed(color=16379747, description='You already have a ticket open!')
            await ctx.send(embed=embed)
        else:
            ticket_channel = await ctx.guild.create_text_channel(f'ticket-{ctx.message.author.name}')
            await ticket_channel.set_permissions(ctx.guild.get_role(ctx.guild.id), send_messages=False, read_messages=False)
            await ticket_channel.set_permissions(ctx.author, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
            embed = discord.Embed(color=16379747, description='Please enter the reason for this ticket, type `/close` if you want to close this ticket.')
            await ticket_channel.send(f'{ctx.author.mention}', embed=embed)
            await ctx.message.delete()

@bot.command()
async def close(ctx):
    print(f'{ctx.author} | {ctx.author.id} -> /close')
    if ctx.channel.type != discord.ChannelType.private:
        if ctx.channel.name == f'ticket-{ctx.message.author.name}':
            await ctx.channel.delete()
        elif ctx.author.id in administrators and 'ticket' in ctx.channel.name:
            await ctx.channel.delete()
        else:
            embed = discord.Embed(color=16379747, description=f'You do not have permission to run this command!')
            await ctx.send(embed=embed)

bot.run(TOKEN)
