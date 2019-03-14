import random
import sys
import asyncio
import platform

from itertools import cycle

try:
    from discord.ext import commands
    from discord.ext.commands import Bot
    from discord.voice_client import VoiceClient
    from discord import ChannelType
    import discord
except ImportError:
    print("Discord.py がインストールされていません。\nDiscord.pyをインストールしてください。")
    sys.exit(1)

version = discord.__version__
client = Bot(command_prefix=';',pm_help=True)
status = ['全ての麺類に祝福を...','麺類うめ～','このBOTは兄者によって作られました']
m = "私は"
like = "が好きです"


# ～～をプレイ中の場所を定期的に変更
async def change_status():
    await client.wait_until_ready()
    msgs = cycle(status)

    while not client.is_closed:
        current_status = next(msgs)
        await client.change_presence(game=discord.Game(name=current_status))
        await asyncio.sleep(30)


# Botの脳の部分
@client.event
async def on_ready():
    print("Discordが準備されました。")
    print("Botの名前:" + client.user.name + "(ID:" + client.user.id + ")")
    print('--------')
    print("BOTが取得してるサーバー数:{}".format(len(client.servers)))
    print("Botが取得してるチャンネル数: {}".format(len([c for c in client.get_all_channels()])))
    print("Botが取得してるユーザー数: {}".format(len(set(client.get_all_members()))))
    print('--------')
    print("discord.py Version: {}".format(version))
    print("Python Version: {}".format(platform.python_version()))
    print('--------')
    print("Botの招待")
    print("https://discordapp.com/api/oauth2/authorize?client_id=515864876309282837&permissions=8&scope=bot")


@client.event
async def on_message(message):
    global role
    channel = message.channel

    # 発言がBotだった場合反応しない
    if client.user == message.author:
        return

    # 発言がDMだった場合反応しない
    if message.channel.type == ChannelType.private:
        await client.send_message(message.channel,"**コマンドはDMでは使うことができません...**")
        return

    if message.content.startswith("麺類生成"):
        if message.channel.id == "516098503265484854":
            up = discord.Color(random.randint(0,0xFFFFFF))
            author = message.author
            role_name = message.content.split()[1]
            role = await client.create_role(author.server,name=role_name,color=up)
            await client.send_message(message.channel,f'作成完了:{role_name} の役職を作成しました')
            member = discord.utils.get(message.server.members,name='We are the Noodle')
            await client.add_roles(message.author,role)
            await client.add_roles(member,role)
            await client.send_message(message.channel,f'付与完了:{role_name}の役職を<@515864876309282837>に付与しました')
            await client.send_message(message.channel,f'{message.author.mention} さんに{role_name}役職を付与しました！')

    if like in message.content:
        roles = [role for role in message.server.roles if role.name in message.content]
        await client.add_roles(message.author,*roles)
        await client.send_message(message.channel,
                                  f'{message.author.mention} さんに{",".join([x.name for x in roles])}役職を付与しました！')

    if message.content.startswith("麺類廃棄"):
        if message.channel.id == "516098503265484854":
            role_name = message.content.split()[1]
            role = discord.utils.get(message.server.roles,name=role_name)
            await client.delete_role(message.server,role)
            await client.send_message(message.channel,f'作成完了:{role_name} の役職を削除しました')

    if message.content.startswith("個人情報"):
        try:
            if not message.mentions[0] == None:
                user = message.author
            else:
                user = message.mentions[0]
            userjoindate = str(user.joined_at.strftime("%Y/%m/%d %H:%M:%S"))
            usercreatedate = str(user.created_at.strftime("%Y/%m/%d %H:%M:%S"))
            role = ", ".join([r.name for r in user.roles])
            nickname = str(user.display_name)

            up = discord.Color(random.randint(0,0xFFFFFF))

            userembed = discord.Embed(
                title=":pencil:ユーザー名:",
                description="**『" + user.name + "』**",
                color=up
            )
            userembed.set_author(
                name=user.name + "#" + user.discriminator + "のユーザー情報:"
            )
            userembed.add_field(
                name=":earth_asia:ニックネーム:",
                value="**" + nickname + "**"
            )
            userembed.add_field(
                name=":bulb:サーバー参加日:",
                value="**" + userjoindate + "**"
            )
            userembed.add_field(
                name=":bar_chart:アカウント作成日:",
                value="**" + usercreatedate + "**"
            )
            userembed.add_field(
                name=":hash:ユーザーID:",
                value="**" + user.id + "**"
            )
            userembed.set_thumbnail(
                url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(user)
            )
            userembed.add_field(
                name=":scroll:ユーザーTAG:",

                value="**#" + user.discriminator + "**"
            )
            userembed.add_field(
                name=":signal_strength:ユーザーの現在のステータス:",
                value="**" + str(user.status) + "**"
            )
            userembed.add_field(
                name=":diamond_shape_with_a_dot_inside:ユーザーが現在付与されてる役職",
                value="**" + role + "**"
            )

            await client.send_message(message.channel,embed=userembed)
        except IndexError:
            await client.send_message(message.channel,";info メンションをしてください。")
        except:
            await client.send_message(message.channel,"すいません。ERRORです。")
        finally:
            pass

    if message.content == "鯖情報":
        server = message.server
        region = message.server.region
        channelss = len(message.server.channels)
        memberss = len(message.server.members)
        role = str(len(server.roles))
        emoji = str(len(server.emojis))
        owner = server.owner
        tekitou = server.role_hierarchy[0]
        online = 0
        for i in server.members:
            if str(i.status) == 'online' or str(i.status) == 'idle' or str(i.status) == 'dnd':
                online += 1
        up = discord.Color(random.randint(0,0xFFFFFF))
        try:
            userembed = discord.Embed(
                title=server.name + "の情報:",
                color=up
            )
            userembed.set_thumbnail(
                url=server.icon_url
            )
            userembed.add_field(
                name="サーバーID:",
                value=server.id
            )
            userembed.add_field(
                name="サーバーオーナ:",
                value=owner
            )
            userembed.add_field(
                name="サーバーリュージョン:",
                value=region
            )
            userembed.add_field(
                name="メンバー数:",
                value=memberss
            )
            userembed.add_field(
                name="チャンネル数:",
                value=channelss
            )
            userembed.add_field(
                name="役職数:",
                value=role
            )
            userembed.add_field(
                name="現在オンラインの数:",
                value=online
            )
            userembed.add_field(
                name="鯖に追加した絵文字の数:",
                value=emoji
            )
            userembed.add_field(
                name="サーバー最上位役職:",
                value=tekitou
            )
            userembed.set_footer(
                text="サーバー作成日: " + server.created_at.__format__(' %Y/%m/%d %H:%M:%S')
            )
            await client.send_message(message.channel,embed=userembed)
        except:
            await client.send_message(message.channel,"すいません。ERRORです。.")
        finally:
            pass

    if message.content.startswith("リスト"):
        async def send(member_data):
            up = discord.Color(random.randint(0,0xFFFFFF))
            name = message.content[4:]
            role = discord.utils.get(message.server.roles,name=message.content[4:])
            if not role == None:
                nick_name = f"『{name}』役職を持っているメンバー！！"
            else:
                nick_name = f"{message.author}さん\n『{name}』役職はこの鯖には存在しておりません..."
            embed = discord.Embed(
                title=nick_name,
                description=member_data,
                color=up,
                timestamp=message.timestamp
            )
            embed.set_author(
                name="メンバー詳細:"
            )
            embed.set_footer(
                text="現在時刻:"
            )
            await client.send_message(message.channel,embed=embed)

        i = 1
        member_data = ""
        role = discord.utils.get(message.server.roles,name=message.content[4:])
        for member in message.server.members:
            if role is None:
                member_data = ""
                await send(member_data)
                return
            if role in member.roles:
                member_data += "{0}人目:『{1}』\n".format(i,member.name)
                if i % 100 == 0:
                    await send(member_data)
                    # リセットする
                    member_data = ""
                i += 1
        else:
            await send(member_data)
            return

    if message.content == "全麺類一覧":
        def slice(li,n):
            while li:
                yield li[:n]
                li = li[n:]

        for roles in slice(message.server.role_hierarchy,50):
            role = "\n".join(f'{i}: {role.mention}' for (i,role) in enumerate(roles,start=1) if role.mentionable)
            userembed = discord.Embed(
                title="麺類一覧:",
                description=role,
                color=discord.Color.light_grey()
            )

            userembed.set_thumbnail(
                url=message.server.icon_url
            )
            userembed.set_author(
                name=message.server.name + "の全麺類情報:"
            )
            await client.send_message(message.channel,embed=userembed)
        await client.send_message(message.channel,"この鯖の麺類の合計の数は`{}`です！".format(str(len(message.server.roles))))

    if message.content == '麺類一覧':
        role = "\n".join([r.mention for r in message.author.roles][::-1])
        up = discord.Color(random.randint(0,0xFFFFFF))
        embed = discord.Embed(
            title="**{}**が取得している麺類の一覧:".format(message.author),
            description=role,
            color=up
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(message.author)
        )
        await client.send_message(message.channel,embed=embed)

    if message.content == "ヘルプ":
        embed = discord.Embed(
            title='**Help一覧**',
            colour=discord.Color(random.randint(0,0xFFFFFF)),
            description=""
        )
        embed.set_footer(
            text="朝,昼,晩麺類だよねだよね！"
        )
        embed.set_author(
            name="麺類鯖だけのために作られたBOT",
            icon_url="https://images-ext-1.discordapp.net/external/L0QWB8Lv9rafe5uJ4u_c5YGolY0SvVHrgkiJkX5Pp7c/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/515864876309282837/bb1d5baed8ad4018f6125f4d1dc0f9e6.png?width=676&height=676"
        )
        embed.set_thumbnail(
            url="https://pbs.twimg.com/profile_images/790896010176237568/a8QtyZLF_400x400.jpg"
        )
        embed.add_field(
            name="私は〇〇が好きです",
            value="私は〇〇が好きですと#自己紹介 で打てば役職を付与されます。例:私はうどんが好きです",
            inline=False
        )
        embed.add_field(
            name="個人情報 @メンション",
            value="メンションした人の情報を得られます\nメンションがなければ自分の情報が表示されます",
            inline=False
        )
        embed.add_field(
            name="鯖情報",
            value="サーバーの情報を得られます",
            inline=False
        )
        embed.add_field(
            name="全麺類一覧",
            value="この鯖の麺類役職をすべて表示します。",
            inline=False
        )
        embed.add_field(
            name="麺類一覧",
            value="自分に付与されている麺類役職を表示します。",
            inline=False
        )
        embed.add_field(
            name="リスト [役職名]",
            value="その役職を持っているメンバーを表示します。",
            inline=False
        )
        embed.add_field(
            name="麺類作成 [名前]",
            value="役職が作成されます。　例:麺類作成 Noodle\n全ての麺類に祝福をより上に表示されてる役職は作成しないで下さい。",
            inline=False
        )
        embed.add_field(
            name="麺類破棄 [名前]",
            value="役職が削除されます。　例:麺類破棄 Noodle\nもし役職を二個作ってしまった場合とかに使って下さい。",
            inline=False
        )
        await client.send_message(channel,embed=embed)


client.loop.create_task(change_status())
client.run(os.environ.get("TOKEN"))
