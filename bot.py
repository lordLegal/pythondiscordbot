import asyncio
import datetime
import os
import re
import threading
import time
from typing import Sized

import discord
import docker
import pymongo
import requests
from discord import Member, channel, embeds
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions
from discord.ext.commands.cooldowns import BucketType
from discord.utils import get
from docker.api import container
from github import Github
from PIL import Image, ImageDraw, ImageFont
from pymongo.message import update
# from bs4 import BeautifulSoup
# import urllib.request
from stackapi import StackAPI

import pilowtest as pic
import tt

time_date_ = datetime.datetime.now()
time_date_string = str(time_date_)
time_date_splittet = time_date_string.split('.')[0]

#####################################################################################################################
#                                                       MongoDB                                                     #
#                                                         by                                                        #
#                                                        Retox                                                      #
#####################################################################################################################
print("Whats New?")
global inpu
inpu = input()

clients = pymongo.MongoClient(
    "mongodb+srv://admin:Gnsv2u00@cluster0.n69bg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = clients.test
mydb = clients["pythondiscordbot"]
col = mydb["dockers"]
usr = mydb["users"]
gu = mydb["guilds"]
bugs = mydb["bugs"]
us_gu = mydb["user_guild"]
rank_col = mydb["guild_ranks"]


#####################################################################################################################
#                                                    Discord Start                                                  #
#                                                         by                                                        #
#                                                        Retox                                                      #
#####################################################################################################################
def get_prefix(client, message):
    if isinstance(message.channel, discord.channel.DMChannel):
        return '$'
    else:
        a = message.guild.id
        b = gu.find_one({"_id": a})
        g = b['prefix']
        return g


intents = discord.Intents.all()


client = commands.Bot(command_prefix="!", intents=intents)
client.remove_command('help')

#####################################################################################################################
#                                                       Events                                                      #
#                                                         by                                                        #
#                                                        Retox                                                      #
#####################################################################################################################


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Run python code on a BOT $help '))
    print('I am here')
    a = client.get_guild(id)
    searcher = col.find().distinct('ids')
    dockers = docker.from_env()

    for x in searcher:
        z = dockers.containers.get(x)
        try:
            col.delete_one({"ids": x})
            z.stop()
            z.remove()
        except Exception:
            col.delete_one({"ids": x})
    # gui = client.channels.cache.get("823187538747064370")
    print(inpu)
    if inpu != " " or inpu != "" or inpu != None:
        embed = discord.Embed()
        embed.add_field(name="Newest update:", value=inpu, inline=False)
        embed.set_footer(text=time_date_splittet)
        chan = client.get_channel(823248289544929280)
        await chan.send(embed=embed)

    print("DB ready")


@client.event
async def on_member_join(member):
    gu_id = int(member.guild.id)
    guid_str = str(member.guild.id)
    fu_usr = usr.find({"_id": guid_str})
    if guid_str == fu_usr:
        pass
    else:
        usr.insert_one({"_id": guid_str, "status": "not",
                        "reason": "no", "xp": 0, "msg": 0})
    a = gu.find_one({"_id": gu_id})
    print(a)
    role_name = str(a['role'])
    role = discord.utils.get(member.guild.roles, name=role_name)
    print(role_name)
    try:
        if role_name == "none":
            pass
        else:
            print("test")
            await member.add_roles(role)
    except Exception:
        pass

    print(member.guild.id)


@ client.event
async def on_member_remove(member):
    print(member)


@ client.event
async def on_guild_join(guild):
    gu_id = guild.id
    gu.insert_one({"_id": gu_id, "prefix": "$", "role": "none", "lvl": "no"})


@ client.event
async def on_guild_remove(guild):
    gu_id = guild.id
    a = gu.find_one({"_id": gu_id})
    gu.delete_one(a)


@ client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embedr = discord.Embed(title="Cooldown", color=0xff0000)
        embedr.add_field(name="please wait for the cooldown",
                         value="you can try it in {:.2f}s".format(error.retry_after), inline=False)
        await ctx.send(embed=embedr)
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title="Command not Found", color=0xff0000)
        embed.set_author(name="Python-bot")
        embed.set_thumbnail(url="https://i.imgur.com/pMPV4Qq.png")
        embed.add_field(
            name="py3", value="run python3 code with 'py2 ** githublink the script name** **pip packteches**'", inline=False)
        embed.add_field(
            name="py2", value="run python2 code with 'py2 ** githublink the script name** **pip packteches**'", inline=False)
        embed.add_field(
            name="github", value="search repos with 'github **keywords**'", inline=False)
        embed.add_field(
            name="bug", value="If you found a bug please report it with this command **ONLY USE THIS IN DMs**", inline=False)
        embed.add_field(
            name="clear", value="You can clear channels with 'clear **the number of deleted messages**'", inline=False)
        embed.add_field(
            name="leaderboard", value="You can see the leaderboard of the server", inline=False)
        embed.add_field(
            name="lvl", value="You can see the xp or the lvl and the rank with 'lvl' or 'lvl @MEMBER'", inline=False)
        embed.add_field(
            name="aliases", value="You can see all aliases for each command", inline=False)
        embed.add_field(
            name="set", value="You can set the setting of your server[defaultrole, prefix, lvl] (CAN ONLY BE USED FROM ADMINS)", inline=False)
        embed.add_field(
            name="stackoverflow", value="You can search for questions in Stack Overflow", inline=False)
        await ctx.send(embed=embed)


async def error_not_found(ctx):
    embed = discord.Embed(title="Command not Found", color=0xff0000)
    embed.set_author(name="Python-bot")
    embed.set_thumbnail(url="https://i.imgur.com/pMPV4Qq.png")
    embed.add_field(
        name="py3", value="run python3 code with 'py2 ** githublink the script name** **pip packteches**'", inline=False)
    embed.add_field(
        name="py2", value="run python2 code with 'py2 ** githublink the script name** **pip packteches**'", inline=False)
    embed.add_field(
        name="github", value="search repos with 'github **keywords**'", inline=False)
    embed.add_field(
        name="bug", value="If you found a bug please report it with this command **ONLY USE THIS IN DMs**", inline=False)
    embed.add_field(
        name="clear", value="You can clear channels with 'clear **the number of deleted messages**'", inline=False)
    embed.add_field(
        name="leaderboard", value="You can see the leaderboard of the server", inline=False)
    embed.add_field(
        name="lvl", value="You can see the xp or the lvl and the rank with 'lvl' or 'lvl @MEMBER'", inline=False)
    embed.add_field(
        name="aliases", value="You can see all aliases for each command", inline=False)
    embed.add_field(
        name="set", value="You can set the setting of your server[defaultrole, prefix, lvl] (CAN ONLY BE USED FROM ADMINS)", inline=False)
    embed.add_field(
        name="stackoverflow", value="You can search for questions in Stack Overflow", inline=False)
    await ctx.send(embed=embed)


def gen_rank(str_guid, str_usrid):
    for us_gus in us_gu.find({"gu_id": str_guid}):
        print(us_gus)
        gu_id = us_gus['gu_id']
        fo_id = us_gus['ids'][0]['id']
        xp_int = int(us_gus['ids'][1]['xp'])
        namerer = us_gus['ids'][5]['name']
        link = us_gus['ids'][6]['pfp']

        ingu = rank_col.find({'guid': gu_id}).distinct('usrid')
        print(ingu)
        if not ingu or ingu == '[]' or ingu == []:

            print("comlete-not")
            rank_col.insert_one({"guid": str_guid, "usrid": fo_id,
                                 "xp": xp_int, "pfp": link, "name": str(namerer)})
        else:
            if fo_id not in ingu:
                print("not")
                rank_col.insert_one({"guid": str_guid, "usrid": fo_id,
                                     "xp": xp_int, "pfp": link, "name": str(namerer)})

            else:
                pruingu = ingu[0]
                print(pruingu)
                rankfo = rank_col.find_one({"guid": str_guid, "usrid": fo_id})
                print(rankfo)
                rank_col.delete_one(rankfo)

                print("del")
                rank_col.insert_one({"guid": str_guid, "usrid": fo_id,
                                     "xp": xp_int, "pfp": link, "name": str(namerer)})

    print("end-com")


def get_rank(str_guid, str_usrid):
    zulul = rank_col.find({"guid": str_guid}).sort("xp", -1)
    for num, doc in enumerate(zulul):
        print(num, "-->", doc)
        urid = doc['usrid']
        if urid == str_usrid:
            return num + 1


@client.event
async def on_message(ev_message):
    if isinstance(ev_message.channel, discord.channel.DMChannel):
        print("dm")
        await client.process_commands(ev_message)
    else:

        mag = ev_message
        gu_id_int = int(mag.guild.id)
        mag_id = str(mag.author.id)
        tag = mag.author.discriminator
        name = mag.author.name
        author_name = name + "#" + tag
        gus = gu.find_one({"_id": gu_id_int})
        da_ad = gus['lvl']
        if da_ad == 'yes' and mag_id != "823141173853028353" and mag_id != '815492748249399306':
            mag = ev_message
            mag_id = str(mag.author.id)
            print(mag_id)
            gu_id = str(mag.guild.id)
            print(gu_id)

            jahr_st = int(time.strftime("%Y"))
            monat_st = int(time.strftime("%m"))
            Tag_st = int(time.strftime("%d"))
            sek_st = int(time.strftime("%S"))
            min_st = int(time.strftime("%M"))
            stun_st = int(time.strftime("%H"))

            jahr = jahr_st * 365
            jahr = jahr * 86400

            if monat_st == 1:
                monat = 31
                monat = monat * 86400
            if monat_st == 2:
                monat = 28
                monat = monat * 86400
            if monat_st == 3:
                monat = 31
                monat = monat * 86400
            if monat_st == 4:
                monat = 30
                monat = monat * 86400
            if monat_st == 5:
                monat = 31
                monat = monat * 86400
            if monat_st == 6:
                monat = 30
                monat = monat * 86400
            if monat_st == 7:
                monat = 31
                monat = monat * 86400
            if monat_st == 8:
                monat = 31
                monat = monat * 86400
            if monat_st == 9:
                monat = 30
                monat = monat * 86400
            if monat_st == 10:
                monat = 31
                monat = monat * 86400
            if monat_st == 11:
                monat = 30
                monat = monat * 86400
            if monat_st == 12:
                monat = 31
                monat = monat * 86400
            tag = Tag_st * 86400
            sek = sek_st
            min = min_st * 60
            stunde = stun_st * 3600
            date = jahr + monat + tag + sek + min + stunde
            date1 = date + 31536000  # ein Jahr
            date2 = date + 15768000  # halbes Jahr
            date3 = date + 7884000  # 3 Monate
            date4 = date + 3942000  # 1,5 Monate
            date5 = date + 2628000  # 1 Monat
            date6 = date + 1814400  # 3 Wochen
            date7 = date + 1209600  # 2 Wochen
            date8 = date + 604800  # 1 Woche
            date9 = date + 518400  # 6 Tage
            date10 = date + 432000  # 5 Tage
            date11 = date + 345600  # 4Tage
            date12 = date + 259200  # 3 Tage
            date13 = date + 172800  # 2 Tage
            date14 = date + 86400  # 1 Tag
            date15 = date + 43200  # 12 Stunden
            date16 = date + 21600  # 6 Stunden
            date17 = date + 10800  # 3 Stunden
            date18 = date + 7200  # 2 Stunde
            date19 = date + 3600  # 1 Stunde
            date20 = date + 1800  # 30 Minuten
            date21 = date + 900  # 15 Minuten
            date22 = date + 600  # 10 Minuten
            date23 = date + 300  # 5 Minuten
            date24 = date + 1
            gen_rank(gu_id, mag_id)
            try:
                fo_mag_id = us_gu.find_one({"gu_id": gu_id,
                                            "ids": {"id": mag_id}})

                print(fo_mag_id)
                fo_id = str(fo_mag_id['ids'][0]['id'])
                xp_int = int(fo_mag_id['ids'][1]['xp'])
                msg_int = int(fo_mag_id['ids'][2]['msg'])
                date_re = int(fo_mag_id['ids'][3]['date'])
                lvl = int(fo_mag_id['ids'][4]['LVL'])
                msg = msg_int + 1
                xp = xp_int + 1

                print("error")

                if mag_id == fo_id:
                    x = True
                    if date_re < date1 and x == True:    # +5 Standard + 5 Jahres Bonus
                        x = False
                        xps = xp + 5
                    if date_re < date2 and x == True:    # +5 Standard + 5 Jahres Bonus
                        x = False
                        xps = xp + 5
                    if date_re < date3 and x == True:    # +5 Standard + 7 Jahres Bonus
                        x = False
                        xps = xp + 7
                    if date_re < date4 and x == True:    # +5 Standard + 8 Jahres Bonus
                        x = False
                        xps = xp + 8
                    if date_re < date5 and x == True:    # +5 Standard + 9 Jahres Bonus
                        x = False
                        xps = xp + 9
                    if date_re < date6 and x == True:    # +5 Standard + 10 Jahres Bonus
                        x = False
                        xps = xp + 10
                    if date_re < date7 and x == True:    # +5 Standard + 11 Jahres Bonus
                        x = False
                        xps = xp + 11
                    if date_re < date8 and x == True:    # +5 Standard + 12 Jahres Bonus
                        x = False
                        xps = xp + 12
                    if date_re < date9 and x == True:    # +5 Standard + 13 Jahres Bonus
                        x = False
                        xps = xp + 13
                    if date_re < date10 and x == True:    # +5 Standard + 14 Jahres Bonus
                        x = False
                        xps = xp + 14
                    if date_re < date11 and x == True:    # +5 Standard + 15 Jahres Bonus
                        x = False
                        xps = xp + 15
                    if date_re < date12 and x == True:    # +5 Standard + 16 Jahres Bonus
                        x = False
                        xps = xp + 16
                    if date_re < date13 and x == True:    # +5 Standard + 17 Jahres Bonus
                        x = False
                        xps = xp + 17
                    if date_re < date14 and x == True:    # +5 Standard + 18 Jahres Bonus
                        x = False
                        xps = xp + 18
                    if date_re < date15 and x == True:    # +5 Standard + 19 Jahres Bonus
                        x = False
                        xps = xp + 19
                    if date_re < date16 and x == True:    # +5 Standard + 20 Jahres Bonus
                        x = False
                        xps = xp + 20
                    if date_re < date17 and x == True:    # +5 Standard + 21 Jahres Bonus
                        x = False
                        xps = xp + 21
                    if date_re < date18 and x == True:    # +5 Standard + 22 Jahres Bonus
                        x = False
                        xps = xp
                        print("ja")
                    if date_re < date19 and x == True:    # +5 Standard + 23 Jahres Bonus
                        x = False
                        xps = xp
                        print("ja")
                    if date_re < date20 and x == True:    # +5 Standard + 24 Jahres Bonus
                        x = False
                        xps = xp
                        print("ja")
                    if date_re < date21 and x == True:    # +5 Standard + 25 Jahres Bonus
                        x = False
                        xps = xp
                        print("ja")
                    if date_re < date22 and x == True:    # +5 Standard + 26 Jahres Bonus
                        x = False
                        xps = xp
                        print("ja")
                    if date_re < date23 and x == True:    # +5 Standard + 27 Jahres Bonus
                        x = False
                        xps = xp + 3
                        print("ja")
                    if date_re < date24 and x == True:    # +5 Standard + 29 Jahres Bonus
                        x = False
                        xps = xp
                        print("ja")

                na = {"gu_id": gu_id,  "ids": [{"id": mag_id}, {
                    "xp": xps}, {"msg": msg}, {"date": date}, {"LVL": lvl}, {"name": author_name}, {"pfp": str(mag.author.avatar_url)}]}
                us_gu.update(fo_mag_id, na)

            except Exception:
                us_gu.insert_one(
                    {"gu_id": gu_id,  "ids": [{"id": mag_id}, {"xp": 5}, {"msg": 1}, {"date": date}, {"LVL": 0}, {"name": author_name}, {"pfp": str(mag.author.avatar_url)}]})

        await client.process_commands(ev_message)

#####################################################################################################################
#                                                        Tasks                                                      #
#                                                         by                                                        #
#                                                        Retox                                                      #
#####################################################################################################################


async def py3_task(ctx, link, dateiname, * pips):
    author = ctx.message.author
    author_name = author.name
    u = author.id
    author_id = str(u)

    a = datetime.datetime.now()
    d = str(a)
    c = d.split('.')[0]

    s = time.strftime('%S')
    x = time.strftime('%M')
    int_x2 = int(x)
    min_x = int_x2*60
    int_s = int(s)
    m = min_x + int_s

    t = int(m)
    g = t+120
    print(g)

    print(author_name)

    a = link.split("/")[-1]
    d = a
    c = d.split(".")[0]
    pip = " ".join(pips)
    if pip == 'none':
        clone = '/bin/sh -c "git clone ' + link + \
            ' ; python3 -u /' + c + '/' + dateiname + '>&2"'
    else:
        clone = '/bin/sh -c "git clone ' + link + ' ; pip3 install ' + \
            pip + ' ; python3 -u /' + c + '/' + dateiname + '"'

    print(clone)
    dockers = docker.from_env()
    userdocker = dockers.containers.run(
        image='mypython:3-alpine', detach=True, stderr=True, remove=False, name=author_id, command=clone)
    print("Test")
    log = userdocker.logs()
    logg = log.decode("utf-8")

    short = userdocker.short_id
    str_short = str(short)
    dict = {"ids": str_short}
    col.insert_one(dict)

    embed = discord.Embed(title="Log", color=0xc1861f)
    embed.add_field(name=f"from {author_name}", value="```" +
                    'loding...' + "```", inline=True)
    message = await ctx.send(embed=embed)

    print("status")
    userdocker.reload()
    status = userdocker.status
    str_status = str(status)
    print(f'status:{status}')

    global super_log
    super_log = 'test'
    while t < g and str_status == 'running':
        s = time.strftime('%S')
        x = time.strftime('%M')
        int_x2 = int(x)
        min_x = int_x2*60
        int_s = int(s)
        m = min_x + int_s
        t = int(m)
        await asyncio.sleep(5)
        log = userdocker.logs()
        logg = log.decode("utf-8")
        lens = int(len(logg))
        # print(int(lens))
        userdocker.reload()
        status = userdocker.status
        str_status = str(status)
        if lens > 1998 and super_log != logg:
            login_data = {
                'api_dev_key': '0ZrhtBXCoCviCxpJUn75tw7CvapiukpW',
                'api_user_name': 'Retox',
                'api_user_password': 'WLivh?xFKDLNjH7'
            }
            data = {
                'api_option': 'paste',
                'api_dev_key': '0ZrhtBXCoCviCxpJUn75tw7CvapiukpW',
                'api_paste_code': logg,
                'api_paste_name': f'Logg von {author_name}',
                'api_paste_expire_date': '1Y',
                'api_user_key': None,
                'api_paste_format': 'apache'
            }

            login = requests.post(
                "https://pastebin.com/api/api_login.php", data=login_data)
            print("Login status: ", login.status_code if login.status_code !=
                  200 else "OK/200")
            print("User token: ", login.text)
            data['api_user_key'] = login.text

            r = requests.post(
                "https://pastebin.com/api/api_post.php", data=data)
            print("Paste send: ", r.status_code if r.status_code !=
                  200 else "OK/200")
            print("Paste URL: ", r.text)
            i = str(r.text)
            inks = i.split('%')[0]
            print(inks)
            while super_log != logg:
                a = datetime.datetime.now()
                d = str(a)
                c = d.split('.')[0]
                super_log = logg

                embeds = discord.Embed(title="Log", color=0xc1861f)
                embeds.add_field(
                    name=f"from {author_name}", value=f'**Sorry the text was above the limit here you can see the log** {inks}```', inline=True)
                embeds.set_footer(text=c)
                await message.edit(content="", embed=embeds)
                super_log = logg

        else:

            while super_log != logg:
                a = datetime.datetime.now()
                d = str(a)
                c = d.split('.')[0]
                super_log = logg

                embeds = discord.Embed(title="Log", color=0xc1861f)
                embeds.add_field(name=f"from {author_name}", value="```" +
                                 super_log + "```", inline=True)
                embeds.set_footer(text=c)
                await message.edit(content="", embed=embeds)
                super_log = logg
    else:
        if str_status == 'exited':
            embeds.add_field(
                name="Stoped!!!", value="has stoped", inline=False)
            embeds.set_footer(text=c)
            await message.edit(content="", embed=embeds)
            print(f'Stoped container from {author_name}')
            userdocker.stop()
            userdocker.remove()
            col.delete_one({"ids": x})

    embeds.add_field(
        name="Stoped!!!", value="has stoped becouse of the time", inline=False)
    embeds.set_footer(text=c)
    await message.edit(content="", embed=embeds)
    print(f'Stoped container from {author_name}')
    userdocker.stop()
    userdocker.remove()
    col.delete_one({"ids": x})

#####################################################################################################################
#####################################################################################################################
#####################################################################################################################
#####################################################################################################################


async def py2_task(ctx, link, dateiname, * pips):
    author = ctx.message.author
    author_name = author.name
    u = author.id
    author_id = str(u)

    a = datetime.datetime.now()
    d = str(a)
    c = d.split('.')[0]

    s = time.strftime('%S')
    x = time.strftime('%M')
    int_x2 = int(x)
    min_x = int_x2*60
    int_s = int(s)
    m = min_x + int_s

    t = int(m)
    g = t+120
    print(g)

    print(author_name)

    a = link.split("/")[-1]
    d = a
    c = d.split(".")[0]
    pip = " ".join(pips)
    if pip == 'none':
        clone = '/bin/sh -c "git clone ' + link + \
            ' ; python2 -u /' + c + '/' + dateiname + '>&2"'
    else:
        clone = '/bin/sh -c "git clone ' + link + ' ; pip2 install ' + \
            pip + ' ; python2 -u /' + c + '/' + dateiname + '"'

    print(clone)
    dockers = docker.from_env()
    userdocker = dockers.containers.run(
        image='mypython:2-alpine', detach=True, stderr=True, remove=False, name=author_id, command=clone)
    print("Test")
    log = userdocker.logs()
    logg = log.decode("utf-8")

    short = userdocker.short_id
    str_short = str(short)
    dict = {"ids": str_short}
    col.insert_one(dict)

    embed = discord.Embed(title="Log", color=0xc1861f)
    embed.add_field(name=f"from {author_name}", value="```" +
                    'loding...' + "```", inline=True)
    message = await ctx.send(embed=embed)

    print("status")
    userdocker.reload()
    status = userdocker.status
    str_status = str(status)
    print(f'status:{status}')

    global super_log
    super_log = 'test'
    while t < g and str_status == 'running':
        s = time.strftime('%S')
        x = time.strftime('%M')
        int_x2 = int(x)
        min_x = int_x2*60
        int_s = int(s)
        m = min_x + int_s
        t = int(m)
        await asyncio.sleep(5)
        log = userdocker.logs()
        logg = log.decode("utf-8")
        lens = int(len(logg))
        # print(int(lens))
        userdocker.reload()
        status = userdocker.status
        str_status = str(status)
        if lens > 1998 and super_log != logg:
            login_data = {
                'api_dev_key': '0ZrhtBXCoCviCxpJUn75tw7CvapiukpW',
                'api_user_name': 'Retox',
                'api_user_password': 'WLivh?xFKDLNjH7'
            }
            data = {
                'api_option': 'paste',
                'api_dev_key': '0ZrhtBXCoCviCxpJUn75tw7CvapiukpW',
                'api_paste_code': logg,
                'api_paste_name': f'Logg von {author_name}',
                'api_paste_expire_date': '1Y',
                'api_user_key': None,
                'api_paste_format': 'apache'
            }

            login = requests.post(
                "https://pastebin.com/api/api_login.php", data=login_data)
            print("Login status: ", login.status_code if login.status_code !=
                  200 else "OK/200")
            print("User token: ", login.text)
            data['api_user_key'] = login.text

            r = requests.post(
                "https://pastebin.com/api/api_post.php", data=data)
            print("Paste send: ", r.status_code if r.status_code !=
                  200 else "OK/200")
            print("Paste URL: ", r.text)
            i = str(r.text)
            inks = i.split('%')[0]
            print(inks)
            while super_log != logg:
                a = datetime.datetime.now()
                d = str(a)
                c = d.split('.')[0]
                super_log = logg

                embeds = discord.Embed(title="Log", color=0xc1861f)
                embeds.add_field(
                    name=f"from {author_name}", value=f'**Sorry the text was above the limit here you can see the log** {inks}```', inline=True)
                embeds.set_footer(text=c)
                await message.edit(content="", embed=embeds)
                super_log = logg

        else:

            while super_log != logg:
                a = datetime.datetime.now()
                d = str(a)
                c = d.split('.')[0]
                super_log = logg

                embeds = discord.Embed(title="Log", color=0xc1861f)
                embeds.add_field(name=f"from {author_name}", value="```" +
                                 super_log + "```", inline=True)
                embeds.set_footer(text=c)
                await message.edit(content="", embed=embeds)
                super_log = logg
    else:
        if str_status == 'exited':
            embeds.add_field(
                name="Stoped!!!", value="has stoped", inline=False)
            embeds.set_footer(text=c)
            await message.edit(content="", embed=embeds)
            print(f'Stoped container from {author_name}')
            userdocker.stop()
            userdocker.remove()
            col.delete_one({"ids": x})

    embeds.add_field(
        name="Stoped!!!", value="has stoped becouse of the time", inline=False)
    embeds.set_footer(text=c)
    await message.edit(content="", embed=embeds)
    print(f'Stoped container from {author_name}')
    userdocker.stop()
    userdocker.remove()
    col.delete_one({"ids": x})


async def bug_task(ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        author = ctx.message.author
        id = author.id
        tag = author.discriminator
        name = author.name
        author_name = name + "#" + tag

        embed = discord.Embed(title="**Report system for Python-bot**")
        embed.add_field(
            name="First Infos", value=" Please enter any text and hit [Enter]. File attachments are not supported. if you want to do send me a picture or a video pls send it with https://streamable.com/ for Videos or https://imgur.com/upload for pictures", inline=False)
        await ctx.send(embed=embed)

        a = await ctx.channel._get_channel()
        print(a)
        embed = discord.Embed(title="**Report system for Python-bot**")
        embed.add_field(name="How important is it?[Very important/important/not realy important]",
                        value="Please enter any text and hit [Enter]. File attachments are not supported.", inline=False)
        await ctx.channel.send(embed=embed)
        msg1 = await client.wait_for('message')
        res1 = (msg1.content)
        if res1 != None and res1 != "":
            print(res1)
            embed = discord.Embed(title="**Report system for Python-bot**")
            embed.add_field(name="Whats the Bug?(please describe the bug)",
                            value="Please enter any text and hit [Enter]. File attachments are not supported.", inline=False)
            await ctx.channel.send(embed=embed)
            msg2 = await client.wait_for('message')
            res2 = (msg2.content)
            if res2 != None and res2 != "":
                print(res2)
                embed = discord.Embed(title="**Report system for Python-bot**")
                embed.add_field(name="Where did it happen?[Please write a Channel or Server/Guild]",
                                value="Please enter any text and hit [Enter]. File attachments are not supported.", inline=False)
                await ctx.channel.send(embed=embed)
                msg3 = await client.wait_for('message')
                res3 = (msg3.content)
                if res3 != None and res3 != "":
                    print(res3)
                    embed = discord.Embed(
                        title="**Report system for Python-bot**")
                    embed.add_field(name="Something else you want to tell me?",
                                    value="Please enter any text and hit [Enter]. File attachments are not supported.", inline=False)
                    await ctx.channel.send(embed=embed)
                    msg4 = await client.wait_for('message')
                    res4 = (msg4.content)
                    if res4 != None and res4 != "":
                        print(res4)
                        bugs.insert_one({"id": id, "name": author_name, "ans1": res1,
                                         "ans2": res2, "ans3": res3, "ans4": res4, })
                        embed = discord.Embed(
                            title="**Report system for Python-bot**")
                        embed.add_field(name="Thank you for your Report",
                                        value="It will be worked on it", inline=False)
                        await ctx.channel.send(embed=embed)


#####################################################################################################################
#                                                       Commands                                                    #
#                                                         by                                                        #
#                                                        Retox                                                      #
#####################################################################################################################


@ client.command(pass_context=True, aliases=['h'], case_insensitive=True)
async def help(ctx):
    embed = discord.Embed(title="HELP", color=0xff0000)
    embed.set_author(name="Python-bot")
    embed.set_thumbnail(url="https://i.imgur.com/pMPV4Qq.png")
    embed.add_field(name="help", value="shows this command", inline=False)
    embed.add_field(
        name="py3", value="run python3 code with 'py2 ** githublink the script name** **pip packteches**'", inline=False)
    embed.add_field(
        name="py2", value="run python2 code with 'py2 ** githublink the script name** **pip packteches**'", inline=False)
    embed.add_field(
        name="github", value="search repos with 'github **keywords**'", inline=False)
    embed.add_field(
        name="bug", value="If you found a bug please report it with this command **ONLY USE THIS IN DMs**", inline=False)
    embed.add_field(
        name="clear", value="You can clear channels with 'clear **the number of deleted messages**'", inline=False)
    embed.add_field(
        name="leaderboard", value="You can see the leaderboard of the server", inline=False)
    embed.add_field(
        name="lvl", value="You can see the xp or the lvl and the rank with 'lvl' or 'lvl @MEMBER'", inline=False)
    embed.add_field(
        name="aliases", value="You can see all aliases for each command", inline=False)
    embed.add_field(
        name="set", value="You can set the setting of your server[defaultrole, prefix, lvl] (CAN ONLY BE USED FROM ADMINS)", inline=False)
    embed.add_field(
        name="stackoverflow", value="You can search for questions in Stack Overflow", inline=False)
    await ctx.send(embed=embed)


@ client.command(pass_context=True, aliases=['python3'], case_insensitive=True)
@ commands.cooldown(1, 300, BucketType.user)
async def py3(ctx, link, dateiname, * pips):
    author = ctx.message.author
    u = author.id
    author_id = str(u)
    searchers = usr.find().distinct('_id')

    for x in searchers:
        if x == author_id:
            a = usr.find_one({"_id": author_id, })
            a_a = a['status']
            b_b = a['reason']
            b = str(b_b)
            if a_a == 'banned':
                embed = discord.Embed(
                    title="**Sry your Banned**", color=0xff0000)
                embed.add_field(name="If you think your banned becouse of no reason",
                                value="pls write me with $bug", inline=False)
                embed.add_field(name="Reason:", value=f"``{b}``")
                await ctx.send(embed=embed)
            else:
                client.loop.create_task(py3_task(ctx, link, dateiname, * pips))
    else:
        usr.insert_one({"_id": author_id, "status": "not",
                        "reason": "no"})
        client.loop.create_task(py3_task(ctx, link, dateiname, * pips))


@ client.command(pass_context=True, aliases=['git'], case_insensitive=True)
async def github(ctx, * keyworda):
    keywords = ",".join(keyworda)
    ACCESS_TOKEN = '33cf731019ac819a3f180fc82a10aaf7140a07b5'
    g = Github(ACCESS_TOKEN)
    keywords = [keyword.strip() for keyword in keywords.split(',')]
    keywordi = ",".join(keyworda)
    keywordg = str(keywordi)

    embedss = discord.Embed(title="Github")
    embedss.set_thumbnail(
        url="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png")
    embedss.add_field(name="Keywords", value=keywordg, inline=False)
    embedss.add_field(
        name="Found repos", value="-------------------------------------------------------------", inline=False)

    query = '+'.join(keywords) + '+in:readme+in:description'
    result = g.search_repositories(query, 'stars', 'desc')
    max_size = 10
    print(f'Found {result.totalCount} file(s)')
    if result.totalCount > max_size:
        result = result[:max_size]

    for file in result:
        # print(f'{file.clone_url}')
        global repos
        repos = str(file.clone_url)
        global h
        h = repos
        embedss.add_field(
            name=f'-------------------------------------------------------------', value=h, inline=False)
    await ctx.send(embed=embedss)


@ client.command(pass_context=True, aliases=['python2'], case_insensitive=True)
@ commands.cooldown(1, 300, BucketType.default)
async def py2(ctx, link, dateiname, * pips):
    author = ctx.message.author
    u = author.id
    author_id = str(u)
    searchers = usr.find().distinct('_id')

    for x in searchers:
        if x == author_id:
            a = usr.find_one({"_id": author_id, })
            a_a = a['status']
            b_b = a['reason']
            b = str(b_b)
            if a_a == 'banned':
                embed = discord.Embed(
                    title="**Sry your Banned**", color=0xff0000)
                embed.add_field(name="If you think your banned becouse of no reason",
                                value="pls write me with $bug", inline=False)
                embed.add_field(name="Reason:", value=f"``{b}``")
                await ctx.send(embed=embed)
            else:
                client.loop.create_task(py2_task(ctx, link, dateiname, * pips))

        else:
            usr.insert_one({"_id": author_id, "status": "not",
                            "reason": "no"})


@ client.command(pass_context=True, aliases=['sv'], case_insensitive=True)
async def stackoverflow(ctx, * searches):
    str_search = str(" ".join(searches))
    SITE = StackAPI('stackoverflow')
    questions = SITE.fetch('questions', max=10,
                           tagged=searches, sort='votes')
    a = str(questions)

    g1 = re.sub("'", "", a)
    g2 = re.sub("{", "", g1)
    g3 = re.sub("}", "", g2)
    g4 = re.sub(":", "", g3)
    g5 = re.sub(",", "", g4)
    print(str_search)
    stack = discord.Embed()
    stack.set_thumbnail(
        url="https://image.flaticon.com/icons/png/512/2111/2111628.png")
    stack.add_field(name="Keywords", value=str_search, inline=False)
    stack.add_field(
        name="Found questions", value="-------------------------------------------------------------", inline=False)

    l = tt.Find(a)
    i = 0
    for i in range(10):
        stack.add_field(
            name="-------------------------------------------------------------", value=l[i], inline=False)
        i = i+1
    print(str_search)
    await ctx.send(embed=stack)


@ client.command(pass_context=True, aliases=['sp_help'], case_insensitive=True)
async def super_help(ctx):
    author = ctx.message.author
    g = author.id
    t = str(g)
    if t == '282616377653592064':
        embed = discord.Embed(title="Bot Info", color=0x37ff00)
        embed.set_thumbnail(url="https://i.imgur.com/pMPV4Qq.png")
        embed.add_field(name="help", value="shows this command", inline=False)
        embed.add_field(
            name="py3", value="run python3 code with 'py2 ** githublink the script name** **pip packteches**'", inline=False)
        embed.add_field(
            name="py2", value="run python2 code with 'py2 ** githublink the script name** **pip packteches**'", inline=False)
        embed.add_field(
            name="github", value="search repos with 'github **keywords**'", inline=False)
        embed.add_field(
            name="bug", value="If you found a bug please report it with this command **ONLY USE THIS IN DMs**", inline=False)
        embed.add_field(
            name="clear", value="You can clear channels with 'clear **the number of deleted messages**'", inline=False)
        embed.add_field(
            name="leaderboard", value="You can see the leaderboard of the server", inline=False)
        embed.add_field(
            name="lvl", value="You can see the xp or the lvl and the rank with 'lvl' or 'lvl @MEMBER'", inline=False)
        embed.add_field(
            name="aliases", value="You can see all aliases for each command", inline=False)
        embed.add_field(
            name="set", value="You can set the setting of your server[defaultrole, prefix, lvl] (CAN ONLY BE USED FROM ADMINS)", inline=False)
        embed.add_field(
            name="stackoverflow", value="You can search for questions in Stack Overflow", inline=False)

        await ctx.send(embed=embed)
        emed = discord.Embed(title="to Invite the Bot", color=0x37ff00)
        emed.add_field(name="Click this link please",
                       value="https://discord.com/api/oauth2/authorize?client_id=815492748249399306&permissions=8&scope=bot")
        await ctx.send(embed=emed)
    else:
        pass


@ client.command(pass_context=True, case_insensitive=True)
async def bug(ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        client.loop.create_task(bug_task(ctx))
    else:
        client.loop.create_task(error_not_found(ctx))


@ client.command(pass_context=True, aliases=['ba'], case_insensitive=True)
async def bann(ctx, wer, * reason):
    author = ctx.message.author
    g = author.id
    t = str(g)
    print(t)
    # searchers = usr.find({"_id": w})
    if t == '282616377653592064':
        re = str(reason)
        fo = {"_id": wer, "status": "not", "reason": "no"}
        print(fo)
        na = {"$set": {"status": "banned", "reason": re}}
        print(na)
        usr.update(fo, na)


@ client.command(pass_context=True, aliases=['ub'], case_insensitive=True)
async def unbann(ctx, wer):
    author = ctx.message.author
    g = author.id
    t = str(g)
    searchers = usr.find({"_id": wer})
    print(t)
    if t == '282616377653592064':
        a = usr.find({"_id": wer})
        g = str(a)
        print(g)
        a = usr.find_one({"_id": wer})
        na = {"$set": {"status": "not", "reason": "no"}}
        print(na)
        usr.update(a, na)

'''
@ client.command(pass_context=True, case_insensitive=True)
async def abb(ctx):
    author = ctx.message.author
    g = author.id
    t = str(g)
    print(t)
    if t == '282616377653592064':
        print("test")
        a = ctx.guild.id
        print(a)
        gu.insert_one({"_id": a, "prefix": "$", "role": "none"})
'''


@client.command(pass_context=True, case_insensitive=True)
@has_permissions(administrator=True)
async def set(ctx, sadge, cas):
    int_gu_id = int(ctx.guild.id)
    fo = gu.find_one({"_id": int_gu_id})
    if sadge == "prefix" or sadge == 'pref':
        gu_id = ctx.guild.id
        na = {"_id": gu_id, "prefix": cas}
        gu.update(fo, na)
        embed = discord.Embed(color=0xff0000)
        embed.add_field(
            name="Changed", value=f"You changed **prefix to {cas}**", inline=False)
        await ctx.send(embed=embed)
    if sadge == 'defaultrole' or sadge == 'defr' or sadge == "dr":
        a = ctx.guild.id
        a = gu.find_one({"_id": a})
        pref = a['prefix']
        na = {"$set": {'prefix': pref, 'role': cas}}
        print(a)
        if get(ctx.guild.roles, name=cas):
            gu.update(a, na)
            embed = discord.Embed(color=0xff0000)
            embed.add_field(
                name="Changed", value=f"You changed **defaultrole to {cas}**", inline=False)
            await ctx.send(embed=embed)
        else:
            embeder = discord.Embed(color=0xff0000)
            embeder.add_field(
                name="ERROR", value=f"Can't find the role {cas} please write the role name", inline=False)

    if sadge == "lvl" or sadge == 'xp':
        if cas == "yes" or cas == "no" or cas == None:
            a = ctx.guild.id
            d = gu.find_one({"_id": a})
            pref = d['prefix']
            ro = d['role']
            na = {"$set": {'prefix': pref, 'role': ro, 'lvl': cas}}
            gu.update(d, na)
            embed = discord.Embed(color=0xff0000)
            embed.add_field(
                name="Changed", value=f"You changed **lvl to {cas}**", inline=False)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(color=0xff0000)
            embed.add_field(
                name="ERROR", value="Please write ``set lvl [yes/no]``", inline=False)
            await ctx.send(embed=embed)
    if sadge == None and cas == None or sadge == None or cas == None:
        embed = discord.Embed(color=0xff0000)
        embed.add_field(
            name="ERROR", value="You can set the setting of your server[defaultrole, prefix, lvl] (CAN ONLY BE USED FROM ADMINS)", inline=False)


@client.command(pass_context=True, case_insensitive=True)
@ has_permissions(administrator=True)
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=1)
    await ctx.channel.purge(limit=amount)


@client.command(pass_context=True, aliases=['tc'], case_insensitive=True)
async def testcommand(ctx, command):
    print("a")
    if command == 'py3':
        embed = discord.Embed()
        embed.add_field(name="Preview command",
                        value="`$py3 https://github.com/lordLegal/Test-repo.git while.py none`", inline=False)
        await ctx.send(embed=embed)
    if command == 'py2':
        embed = discord.Embed()
        embed.add_field(name="Preview command",
                        value="Use py3", inline=False)
        await ctx.send(embed=embed)
    if command == 'github':
        embed = discord.Embed()
        embed.add_field(name="Preview command",
                        value="```$github python discord```", inline=False)
        await ctx.send(embed=embed)
    if command == 'clear':
        embed = discord.Embed()
        embed.add_field(name="Preview command",
                        value="```$clear 10```", inline=False)
        await ctx.send(embed=embed)
    if command == 'set':
        embed = discord.Embed()
        embed.add_field(name="Preview command",
                        value="```$set lvl [yes/no]``` or ```$set prefix .``` or ```$set defaultrole Admin```", inline=False)
        await ctx.send(embed=embed)
    if command == 'stackoverflow':
        embed = discord.Embed()
        embed.add_field(name="Preview command",
                        value="```$stackoverflow python discord```", inline=False)
        await ctx.send(embed=embed)
    if command == 'lvl':
        embed = discord.Embed()
        embed.add_field(name="Preview command",
                        value="```$lvl @Python_is_cool```", inline=False)
        await ctx.send(embed=embed)


@client.command(pass_context=True, aliases=['alis'], case_insensitive=True)
async def aliases(ctx):
    embed = discord.Embed()
    embed.add_field(
        name="Aliases", value="here are the Aliases from all commands", inline=False)
    embed.add_field(name="python3", value="py3", inline=False)
    embed.add_field(name='python2', value="py2")
    embed.add_field(name="github", value="git")
    embed.add_field(name="clear", value="clear")
    embed.add_field(name="aliases", value="alis")
    embed.add_field(name="help", value="h")
    embed.add_field(name="leaderboard", value="lead")
    embed.add_field(name="lvl", value="xp")
    embed.add_field(name="testcommand", value="tc")
    embed.add_field(name="aliases", value="alis")
    embed.add_field(name="stackoverflow", value="sv")
    await ctx.send(embed=embed)


@client.command(pass_context=True, aliases=['xp'], case_insensitive=True)
async def lvl(ctx, ead="None"):

    guild = str(ctx.guild.id)
    str_id = str(ctx.message.author.id)
    setting = gu.find_one({"_id": int(ctx.guild.id)})
    lvl = setting['lvl']

    if str_id != "823141173853028353" and str_id != "815492748249399306" and lvl == 'yes':
        if ead == "None":
            author = ctx.message.author
            id = author.id
            pfp = author.avatar_url
            print(pfp)
            tag = author.discriminator
            name = author.name
            author_name = name + "#" + tag
            fo_mag_id = us_gu.find_one({"gu_id": guild,
                                        "ids": {"id": str_id}})
            fo_id = str(fo_mag_id['ids'][0]['id'])
            xp_int = int(fo_mag_id['ids'][1]['xp'])
            msg_int = int(fo_mag_id['ids'][2]['msg'])
            date_re = int(fo_mag_id['ids'][3]['date'])
            lvl = int(fo_mag_id['ids'][4]['LVL'])
            global LVLsg
            LVLsg = 0
            global max_xp
            max_xp = 50
            xp = str(xp_int)
            print(xp_int)

            if xp_int >= 50:
                print("LVL1")
                LVLsg = 1
                max_xp = 500
                na = {'gu_id': guild, 'ids': [
                    {'id': str_id}, {'xp': xp_int}, {'msg': msg_int}, {'date': date_re}, {'LVL': LVLsg}, {"name": author_name}, {"pfp": str(ctx.message.author.avatar_url)}]}
                us_gu.update(fo_mag_id, na)
            if xp_int >= 500:
                print("LVL2")
                LVLsg = 2
                max_xp = 1500
                na = {'gu_id': guild, 'ids': [
                    {'id': str_id}, {'xp': xp_int}, {'msg': msg_int}, {'date': date_re}, {'LVL': LVLsg}, {"name": author_name}, {"pfp": str(ctx.message.author.avatar_url)}]}
                us_gu.update(fo_mag_id, na)
            if xp_int >= 1500:
                print("LVL3")
                LVLsg = 3
                max_xp = 3000
                na = {'gu_id': guild, 'ids': [
                    {'id': str_id}, {'xp': xp_int}, {'msg': msg_int}, {'date': date_re}, {'LVL': LVLsg}, {"name": author_name}, {"pfp": str(ctx.message.author.avatar_url)}]}
                us_gu.update(fo_mag_id, na)
            if xp_int >= 3000:
                print("LVL4")
                LVLsg = 4
                max_xp = 5000
                na = {'gu_id': guild, 'ids': [
                    {'id': str_id}, {'xp': xp_int}, {'msg': msg_int}, {'date': date_re}, {'LVL': LVLsg}, {"name": author_name}, {"pfp": str(ctx.message.author.avatar_url)}]}
                us_gu.update(fo_mag_id, na)
            if xp_int >= 5000:
                print("LVL5")
                LVLsg = 5
                max_xp = 10000
                na = {'gu_id': guild, 'ids': [
                    {'id': str_id}, {'xp': xp_int}, {'msg': msg_int}, {'date': date_re}, {'LVL': LVLsg}, {"name": author_name}, {"pfp": str(ctx.message.author.avatar_url)}]}
                us_gu.update(fo_mag_id, na)
            if xp_int >= 10000:
                print("LVL6")
                LVLsg = 6
                max_xp = 20000
                na = {'gu_id': guild, 'ids': [
                    {'id': str_id}, {'xp': xp_int}, {'msg': msg_int}, {'date': date_re}, {'LVL': LVLsg}, {"name": author_name}, {"pfp": str(ctx.message.author.avatar_url)}]}
                us_gu.update(fo_mag_id, na)
            if xp_int >= 20000:
                print("LVL7")
                LVLsg = 7
                max_xp = 40000
                na = {'gu_id': guild, 'ids': [
                    {'id': str_id}, {'xp': xp_int}, {'msg': msg_int}, {'date': date_re}, {'LVL': LVLsg}, {"name": author_name}, {"pfp": str(ctx.message.author.avatar_url)}]}
                us_gu.update(fo_mag_id, na)
            if xp_int >= 40000:
                print("LVL8")
                LVLsg = 8
                max_xp = 60000
                na = {'gu_id': guild, 'ids': [
                    {'id': str_id}, {'xp': xp_int}, {'msg': msg_int}, {'date': date_re}, {'LVL': LVLsg}, {"name": author_name}, {"pfp": str(ctx.message.author.avatar_url)}]}
                us_gu.update(fo_mag_id, na)
            if xp_int >= 60000:
                print("LVL9")
                LVLsg = 9
                max_xp = 90000
                na = {'gu_id': guild, 'ids': [
                    {'id': str_id}, {'xp': xp_int}, {'msg': msg_int}, {'date': date_re}, {'LVL': LVLsg}, {"name": author_name}, {"pfp": str(ctx.message.author.avatar_url)}]}
                us_gu.update(fo_mag_id, na)
            if xp_int >= 90000:
                print("LVL10")
                LVLsg = 10
                max_xp = 120000
                na = {'gu_id': guild, 'ids': [
                    {'id': str_id}, {'xp': xp_int}, {'msg': msg_int}, {'date': date_re}, {'LVL': LVLsg}, {"name": author_name}, {"pfp": str(ctx.message.author.avatar_url)}]}
                us_gu.update(fo_mag_id, na)
            pic.download(pfp, str_id)

            font = ImageFont.truetype("font2.ttf", 30)
            font2 = ImageFont.truetype("font2.ttf", 50)
            rank = str(get_rank(guild, str_id))
            img = Image.open("vorlage.png")
            img4 = Image.open(f"{str_id}.png")
            img3 = Image.open("profpfp.png")
            size = (200, 200)
            sudo = img4.resize(size)
            sudo.save(f"{str_id}.png")
            img2 = Image.open(f"{str_id}.png")
            draw = ImageDraw.Draw(img)
            img.paste(img2, (533, 53))
            img.paste(img3, (400, 13), mask=img3)

            draw.text((0, 0), f"{author_name}", (240, 248, 255), font=font)
            draw.text((1080, 0), f"Rank#{rank}", (240, 248, 255), font=font)
            print(LVLsg)
            draw.text((565, 250), f"LVL: {str(LVLsg)}",
                      (240, 248, 255), font=font2)
            draw.text((490, 300), f"{xp}/{str(max_xp)} XP",
                      (240, 248, 255), font=font2)
            img.save(f'{str_id}_send.png', 'PNG')

            await ctx.send(file=discord.File(f"{str_id}_send.png"))
            os.remove(f"{str_id}_send.png")
            os.remove(f"{str_id}.png")
        else:
            inp = str(ead)
            id = inp.split('<')
            id = id[1]
            id2 = id.split('>')
            id2 = id2[0]
            id3 = id2.split('@')
            id3 = id3[1]
            id4 = id3.split('!')
            id4 = id4[1]

            print(id3, id4)
            fo_mag_id = us_gu.find_one({"gu_id": guild,
                                        "ids": {"id": str(id4)}})
            if fo_mag_id == None:
                embed = discord.Embed(color=0xff0000)
                embed.add_field(name="ERROR",
                                value="The player that you added have not written any message", inline=False)
                await ctx.send(embed=embed)
            else:
                print(fo_mag_id)
                fo_id = str(fo_mag_id['ids'][0]['id'])
                xp_int = int(fo_mag_id['ids'][1]['xp'])
                msg_int = int(fo_mag_id['ids'][2]['msg'])
                date_re = int(fo_mag_id['ids'][3]['date'])
                lvl = int(fo_mag_id['ids'][4]['LVL'])
                author_name = fo_mag_id['ids'][5]['name']
                pfp = fo_mag_id['ids'][6]['pfp']
                global LVLsgg
                LVLsgg = 0
                global max_xpp
                max_xpp = 50
                xp = str(xp_int)
                print(xp_int)

                if xp_int >= 50:
                    print("LVL1")
                    LVLsgg = 1
                    max_xpp = 500
                    na = {'gu_id': guild, 'ids': [
                        {'id': id4}, {'xp': xp_int}, {'msg': msg_int}, {'date': date_re}, {'LVL': LVLsgg}, {"name": author_name}, {"pfp": pfp}]}
                    us_gu.update(fo_mag_id, na)
                if xp_int >= 500:
                    print("LVL2")
                    LVLsgg = 2
                    max_xpp = 1500
                    na = {'gu_id': guild, 'ids': [
                        {'id': id4}, {'xp': xp_int}, {'msg': msg_int}, {'date': date_re}, {'LVL': LVLsgg}, {"name": author_name}, {"pfp": pfp}]}
                    us_gu.update(fo_mag_id, na)
                if xp_int >= 1500:
                    print("LVL3")
                    LVLsgg = 3
                    max_xpp = 3000
                    na = {'gu_id': guild, 'ids': [
                        {'id': id4}, {'xp': xp_int}, {'msg': msg_int}, {'date': date_re}, {'LVL': LVLsgg}, {"name": author_name}, {"pfp": pfp}]}
                    us_gu.update(fo_mag_id, na)
                if xp_int >= 3000:
                    print("LVL4")
                    LVLsgg = 4
                    max_xpp = 5000
                    na = {'gu_id': guild, 'ids': [
                        {'id': id4}, {'xp': xp_int}, {'msg': msg_int}, {'date': date_re}, {'LVL': LVLsgg}, {"name": author_name}, {"pfp": pfp}]}
                    us_gu.update(fo_mag_id, na)
                if xp_int >= 5000:
                    print("LVL5")
                    LVLsgg = 5
                    max_xpp = 10000
                    na = {'gu_id': guild, 'ids': [
                        {'id': id4}, {'xp': xp_int}, {'msg': msg_int}, {'date': date_re}, {'LVL': LVLsgg}, {"name": author_name}, {"pfp": pfp}]}
                    us_gu.update(fo_mag_id, na)
                if xp_int >= 10000:
                    print("LVL6")
                    LVLsgg = 6
                    max_xpp = 20000
                    na = {'gu_id': guild, 'ids': [
                        {'id': id4}, {'xp': xp_int}, {'msg': msg_int}, {'date': date_re}, {'LVL': LVLsgg}, {"name": author_name}, {"pfp": pfp}]}
                    us_gu.update(fo_mag_id, na)
                if xp_int >= 20000:
                    print("LVL7")
                    LVLsgg = 7
                    max_xpp = 40000
                    na = {'gu_id': guild, 'ids': [
                        {'id': id4}, {'xp': xp_int}, {'msg': msg_int}, {'date': date_re}, {'LVL': LVLsgg}, {"name": author_name}, {"pfp": pfp}]}
                    us_gu.update(fo_mag_id, na)
                if xp_int >= 40000:
                    print("LVL8")
                    LVLsgg = 8
                    max_xpp = 60000
                    na = {'gu_id': guild, 'ids': [
                        {'id': id4}, {'xp': xp_int}, {'msg': msg_int}, {'date': date_re}, {'LVL': LVLsgg}, {"name": author_name}, {"pfp": pfp}]}
                    us_gu.update(fo_mag_id, na)
                if xp_int >= 60000:
                    print("LVL9")
                    LVLsgg = 9
                    max_xpp = 90000
                    na = {'gu_id': guild, 'ids': [
                        {'id': id4}, {'xp': xp_int}, {'msg': msg_int}, {'date': date_re}, {'LVL': LVLsgg}, {"name": author_name}, {"pfp": pfp}]}
                    us_gu.update(fo_mag_id, na)
                if xp_int >= 90000:
                    print("LVL10")
                    LVLsgg = 10
                    max_xpp = 120000
                    na = {'gu_id': guild, 'ids': [
                        {'id': id4}, {'xp': xp_int}, {'msg': msg_int}, {'date': date_re}, {'LVL': LVLsgg}, {"name": author_name}, {"pfp": pfp}]}
                    us_gu.update(fo_mag_id, na)
                pic.download(pfp, id4)

                font = ImageFont.truetype("font2.ttf", 30)
                font2 = ImageFont.truetype("font2.ttf", 50)
                rank = str(get_rank(guild, id4))
                img = Image.open("vorlage.png")
                img4 = Image.open(f"{id4}.png")
                img3 = Image.open("profpfp.png")
                size = (200, 200)
                sudo = img4.resize(size)
                sudo.save(f"{id4}.png")
                img2 = Image.open(f"{id4}.png")
                draw = ImageDraw.Draw(img)
                img.paste(img2, (533, 53))
                img.paste(img3, (400, 13), mask=img3)

                draw.text((0, 0), f"{author_name}", (240, 248, 255), font=font)
                draw.text((1080, 0), f"Rank#{rank}",
                          (240, 248, 255), font=font)
                print(LVLsgg)
                draw.text((565, 250), f"LVL: {str(LVLsgg)}",
                          (240, 248, 255), font=font2)
                draw.text((490, 300), f"{xp}/{str(max_xpp)} XP",
                          (240, 248, 255), font=font2)
                img.save(f'{id4}_send.png', 'PNG')

                await ctx.send(file=discord.File(f"{id4}_send.png"))
                os.remove(f"{id4}_send.png")
                os.remove(f"{id4}.png")
    else:
        embed = discord.Embed(color=0xff0000)
        embed.add_field(name="Your admin didn't activate the setting",
                        value="if you are a admin activate it with `set lvl yes`", inline=False)
        await ctx.send(embed=embed)
'''
@ client.command()
async def pfp(ctx):
    id = ctx.message.author
    await ctx.send(file=discord.File("discordbotlogo.png"))
'''


@client.command(pass_context=True, aliases=['leaderboard'], case_insensitive=True)
async def lead(ctx):

    setting = gu.find_one({"_id": int(ctx.guild.id)})
    lvl = setting['lvl']
    print(lvl)

    if lvl == "yes":

        fori = rank_col.find({"guid": str(ctx.guild.id)}).sort("xp", -1)
        gu_name = ctx.guild.name
        gu_id = ctx.guild.id
        font = ImageFont.truetype("fontlead.ttf", 100)
        font2 = ImageFont.truetype("fontlead.ttf", 80)
        font3 = ImageFont.truetype("fontlead.ttf", 50)
        font4 = ImageFont.truetype("fontlead.ttf", 70)
        img = Image.new('RGB', (2480, 3508), color='black')
        draw = ImageDraw.Draw(img)
        draw.text(
            (470, 196), f"Leaderboard from {gu_name}", (240, 248, 255), font=font)
        draw.text(
            (115, 390), f"Rank", (240, 248, 255), font=font2)
        draw.text(
            (950, 390), f"Name", (240, 248, 255), font=font2)
        draw.text(
            (1900, 390), f"XP", (240, 248, 255), font=font2)

        for num, doc in enumerate(fori):
            if int(num + 1) > 10:
                break
            nmer = doc['name']
            id_usr = doc['usrid']

            pfp_link = doc['pfp']
            xp = doc['xp']
            numer = num+1
            pic.download(str(pfp_link), str(id_usr))
            print(num + 1, pfp_link, nmer, xp)

            rank_pos = int(400)
            name_pos = int(400)
            xp_pos = int(400)

            print(str(numer))
            print(rank_pos, numer)

            plus_rank_pos = rank_pos + (300 * numer)
            plus_name_pos = name_pos + (300 * numer)
            plus_xp_pos = xp_pos + (300 * numer)

            print(plus_rank_pos, plus_name_pos, plus_xp_pos)

            draw.text(
                (130, plus_rank_pos), f"{str(numer)}#", (240, 248, 255), font=font2)  # +300

            print(len(str(nmer)))
            name_len = len(str(nmer))

            lon = None

            if name_len > 32:
                lon = "set"
                draw.text(
                    (610, plus_name_pos), f"{str(nmer)}", (240, 248, 255), font=font3)  # +300

            if name_len > 13 and lon == None:
                lon = "set"
                draw.text(
                    (610, plus_name_pos), f"{str(nmer)}", (240, 248, 255), font=font4)  # +300

            if lon == None:
                draw.text(
                    (610, plus_name_pos), f"{str(nmer)}", (240, 248, 255), font=font2)  # +300

            draw.text(
                (1890, plus_xp_pos), f"{str(xp)}", (240, 248, 255), font=font2)  # +300

            pr_img = Image.open(f"{id_usr}.png")
            print(pr_img.size)
            size = (256, 256)
            sudo = pr_img.resize(size)
            sudo.save(f"{id_usr}.png")
            img.paste(sudo, (350, plus_rank_pos))  # +300

        img.save(f"{gu_id}_send.png", "PNG")

        await ctx.send(file=discord.File(f"{gu_id}_send.png"))

        os.remove(f"{gu_id}_send.png")

        forik = rank_col.find({"guid": str(ctx.guild.id)}).sort("xp", -1)
        for num, doc in enumerate(forik):

            id_usr4 = doc['usrid']

            print(f"{id_usr4}.png")
            os.remove(f"{str(id_usr4)}.png")
    else:
        embed = discord.Embed(color=0xff0000)
        embed.add_field(name="Your admin didn't activate the setting",
                        value="if you are a admin activate it with `set lvl yes`", inline=False)
        await ctx.send(embed=embed)


# client.run("ODE1NDkyNzQ4MjQ5Mzk5MzA2.YDtMzg.8bd-Cc0rGS4cTSJv0lfAnGFIKHM")  # Real
client.run("ODIzMTQxMTczODUzMDI4MzUz.YFcf9Q.8ySn-WN5vLDwFA_HRQxtmuRtu9E")  # Beta

# https://top.gg/bot/815492748249399306/vote
