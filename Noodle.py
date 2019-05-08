# -------------------------------------------------------------------------------------------------------------------
import sys
import string,random
import math
import psycopg2
import os

from datetime import datetime
from collections import defaultdict

try:
    import discord
    from discord.ext.commands import Bot
except ImportError:
    print("Discord.py がインストールされていません。\nDiscord.pyをインストールしてください。")
    sys.exit(1)
# -------------------------------------------------------------------------------------------------------------------
client = Bot(command_prefix='&',pm_help=True)
all_member = "569835479508451338"
get_user = "569835527780433920"
get_bot = "569835528992849930"
count = 0
counts = 0
number = 0
left = '⏪'
right = '⏩'


def predicate(message,l,r):
    def check(reaction,user):
        if reaction.message.id != message.id or user == client.user:
            return False
        if l and reaction.emoji == left:
            return True
        if r and reaction.emoji == right:
            return True
        return False

    return check


# -------------------------------------------------------------------------------------------------------------------
@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name=">help | ver:1.0.0"))


# -------------------------------------------------------------------------------------------------------------------
@client.event
async def on_member_join(member):
    if not member.server.id == "521143812278714378":
        return
    await client.edit_channel(client.get_channel(all_member),
                              name="総メンバー数：{}".format(len(member.server.members)))
    await client.edit_channel(client.get_channel(get_user),name="ユーザー数：{}".format(
        len([member for member in member.server.members if not member.bot])))
    await client.edit_channel(client.get_channel(get_bot),
                              name="ボットの数：{}".format(
                                  len([member for member in member.server.members if member.bot])))


# -------------------------------------------------------------------------------------------------------------------
@client.event
async def on_member_remove(member):
    if not member.server.id == "521143812278714378":
        return
    await client.edit_channel(client.get_channel(all_member),
                              name="総メンバー数：{}".format(len(member.server.members)))
    await client.edit_channel(client.get_channel(get_user),name="ユーザー数：{}".format(
        len([member for member in member.server.members if not member.bot])))
    await client.edit_channel(client.get_channel(get_bot),
                              name="ボットの数：{}".format(
                                  len([member for member in member.server.members if member.bot])))


@client.event
async def on_message(message):
    if datetime.now().strftime("%H:%M:%S") == datetime.now().strftime(
            "12:00:00") or message.content == ">update-message":
        if message.author.server_permissions.administrator:
            if not message.server.id == "521143812278714378":
                return
            await client.delete_message(message)
            counter = 0
            all_message = "569835558642384896"
            channel_name = client.get_channel(all_message)
            for i in message.server.channels:
                async for log in client.logs_from(i,limit=99999999999):
                    if log.server.id == message.server.id:
                        counter += 1
            await client.edit_channel(channel_name,name="総メッセージ数：{}".format(counter))
            return
    help_message = ["""
            -------------------------------
            このBOTはプロデュースが𝗠𝗞𝗠𝗞𝟭𝟭𝟬𝟭™#3577
            組み立てをThe.First.Step#3454が行いました！
            質問等はThe.First.Step#3454にDMでお問い合わせ下さい！

            -------------------------------
            このBOTの招待は[こちらから](<https://discordapp.com/api/oauth2/authorize?client_id=531765421070745600&permissions=392417&scope=bot>)
            このBOTの中身は[こちらから](<https://github.com/LoveNuddle/Noodle/blob/master/Noodle.py>)
            公式鯖[こちらから](<https://discord.gg/4YatQpp>)
            -------------------------------""",
            """
            Command一覧
            ここでは識別IDを`[0iKV5]`で例えています。
            実際は違いますのでご注意を。

            -------------------------------
            `>q-c 質問内容` or `>question-create 質問内容`
            ↳質問出来るよ！
            ↳自分が今気になってることを質問してみてね！
            ↳↳[例:>q-c なんで地球って青いの？]

            -------------------------------
            `>question-editing 識別ID 変更内容`
            ↳質問作成した時に質問識別のIDが作成されるから
            ↳自分の問題内容を変えたい場合は使ってね！
            ↳↳[例:>question-editing 0iKV5 地球は赤かったかもよ？]
            ※このコマンドは自分の質問しか編集できません。

            -------------------------------
            `>question-delete 識別ID`
            ↳入力したIDの質問を削除できます
            ↳解決した問題などはこれで削除しましょう。
            ↳↳[例:>question-delete 0iKV5]
            ※このコマンドは自分の質問しか削除できません。

            -------------------------------
            `>question-list`
            ↳今までされた質問すべてを閲覧できる！
            
            -------------------------------
            `>locate 識別ID`
            ↳入力したIDの詳細が見れます。
            ↳今までに回答された内容を閲覧可能です！
            ↳↳[例:>locate 0iKV5]
            
            -------------------------------
            """,
            """
            Command一覧
            ここでは識別IDを`[0iKV5]`で例えています。
            実際は違いますのでご注意を。
            
            -------------------------------
            `>answer 識別ID 回答内容`
            ↳これは誰でも回答できます！
            ↳自分が質問に答える際はこれを使用してください。
            ↳↳[例:>answer 0iKV5 地球が赤いわけないだろ...]
            
            -------------------------------
            `>best-answer 解答識別ID`
            ↳ベストアンサー機能です！
            ↳自分がお世話になった解答にお礼代わりに送りましょう！
            ↳↳[例:>best-answer 0iKV5]

            -------------------------------
            `>answer-top`
            ↳ベストアンサーされた回数ランキングです！

            -------------------------------"""]

    if message.content == ">help":
        index = 0
        embed = discord.Embed(
            title="Help一覧:",
            description=help_message[index],
            color=discord.Color(0xc088ff),
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
        )
        msg = await client.send_message(message.channel,embed=embed)
        while True:
            l = index != 0
            r = index != len(help_message) - 1
            if l:
                await client.add_reaction(msg,left)
            if r:
                await client.add_reaction(msg,right)
            react,user = await client.wait_for_reaction(check=predicate(msg,l,r))
            if react.emoji == left:
                index -= 1
            elif react.emoji == right:
                index += 1
            embed = discord.Embed(
                title="Help一覧:",
                description=help_message[index],
                color=discord.Color(0xc088ff),
            )
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
            )
            await client.edit_message(msg,embed=embed)
            await client.clear_reactions(msg)

    if message.content.startswith(">question-create"):
        def randomname(n):
            a = ''.join(random.choices(string.ascii_letters + string.digits,k=n))
            return a

        numbers = randomname(5)
        content = message.content[17:]
        if content == "":
            embed = discord.Embed(
                description=f"{message.author.mention}さん\nメッセージを入力してくれよな！",
                color=discord.Color(0xc088ff),
            )
            await client.send_message(message.channel,embed=embed)
            return
        
        out_words = ["しね","金！暴力！SEX！（迫真）","おっぱい","ちんこ","まんこ","殺す","ちんぽ","おちんちん","アナル","sex","セックス","オナニー","おちんぽ","ちくび",
                     "乳首","陰茎","うざい","黙れ","きもい","やりますねぇ！","覚醒剤","覚せい剤","麻薬","コカイン","SEX","害児","pornhub","xvideo","せっくす",
                     "mother fucker","金正恩","penis","fuck","死ね","殺す","アホ","赤ちゃん製造ミルク","ザー汁","ザーメン","精液","精子","こ↑こ↓",
                     "やりますねぇ"]
        if any([True for s in out_words if s in content]):
            embed = discord.Embed(
                description=f"{message.author.mention}さん\n禁止用語が入っているので質問できません！",
                color=discord.Color(0xc088ff),
            )
            await client.send_message(message.channel,embed=embed)
            await client.delete_message(message)
            return

        ans = db_write(
            str(numbers),
            int(message.author.id),
            str(content)
        )
        if ans == True:
            embed = discord.Embed(
                description=f"{message.author.mention}さん\n\n`{content}`\n\nID:{numbers}",
                color=discord.Color(0xc088ff),
                timestamp=message.timestamp
            )
            embed.set_footer(
                text="作成時刻:"
            )
            await client.send_message(message.channel,embed=embed)
            return

    if message.content.startswith(">q-c"):
        def randomname(n):
            a = ''.join(random.choices(string.ascii_letters + string.digits,k=n))
            return a

        numbers = randomname(5)
        content = message.content[5:]
        if content == "":
            embed = discord.Embed(
                description=f"{message.author.mention}さん\nメッセージを入力してくれよな！",
                color=discord.Color(0xc088ff),
            )
            await client.send_message(message.channel,embed=embed)
            return
        
        out_words = ["しね","金！暴力！SEX！（迫真）","おっぱい","ちんこ","まんこ","殺す","ちんぽ","おちんちん","アナル","sex","セックス","オナニー","おちんぽ","ちくび",
                     "乳首","陰茎","うざい","黙れ","きもい","やりますねぇ！","覚醒剤","覚せい剤","麻薬","コカイン","SEX","害児","pornhub","xvideo","せっくす",
                     "mother fucker","金正恩","penis","fuck","死ね","殺す","アホ","赤ちゃん製造ミルク","ザー汁","ザーメン","精液","精子","こ↑こ↓",
                     "やりますねぇ"]
        if any([True for s in out_words if s in content]):
            embed = discord.Embed(
                description=f"{message.author.mention}さん\n禁止用語が入っているので質問できません！",
                color=discord.Color(0xc088ff),
            )
            await client.send_message(message.channel,embed=embed)
            await client.delete_message(message)
            return

        ans = db_write(
            str(numbers),
            int(message.author.id),
            str(content)
        )
        if ans == True:
            embed = discord.Embed(
                description=f"{message.author.mention}さん\n\n`{content}`\n\nID:{numbers}",
                color=discord.Color(0xc088ff),
                timestamp=message.timestamp
            )
            embed.set_footer(
                text="作成時刻:"
            )
            await client.send_message(message.channel,embed=embed)
            return

    if message.content == ">question-list":
        async def message_number(numbers):
            if len(list(db_read())) == 0:
                embed = discord.Embed(
                    title="現在の質問リスト:",
                    description="質問が一つもありません！",
                    color=discord.Color(0xc088ff),
                )
                await client.send_message(message.channel,embed=embed)
                return
            page = 1
            for row2 in db_read_count():
                join = "".join(numbers[(page - 1) * 5:page * 5])
                embed = discord.Embed(
                    title="現在の質問リスト:",
                    description=join + f"-------------------------------\n\n総閲覧数:{int(row2[0])} | 総回答数:{int(row2[1])}",
                    color=discord.Color(0xc088ff),
                )
                embed.set_footer(
                    text=f"質問一覧　　{math.ceil(len(numbers) / 5)}ページ中 / {page}ページ目を表示中"
                )
                msg = await client.send_message(message.channel,embed=embed)
                while True:
                    l = page != 1
                    r = page < len(numbers) / 5
                    if l:
                        await client.add_reaction(msg,left)
                    if r:
                        await client.add_reaction(msg,right)
                    react,user = await client.wait_for_reaction(check=predicate(msg,l,r))
                    if react.emoji == left:
                        page -= 1
                    elif react.emoji == right:
                        page += 1
                    for row2 in db_read_count():
                        join = "".join(numbers[(page - 1) * 5:page * 5])
                        embed = discord.Embed(
                            title="現在の質問リスト:",
                            description=join + f"-------------------------------\n\n総閲覧数:{int(row2[0])} | 総回答数:{int(row2[1])}",
                            color=discord.Color(0xc088ff),
                        )
                        embed.set_footer(
                            text=f"質問一覧　　{math.ceil(len(numbers) / 5)}ページ中 / {page}ページ目を表示中"
                        )
                        await client.edit_message(msg,embed=embed)
                        await client.clear_reactions(msg)

        numbers = []
        for row in db_read():
            numbers.append("".join(
                f"""-------------------------------\n<@{row[1]}>さんの質問\n\n`{str(row[2])}`\n\n閲覧数：{row[3]}\n回答数：{row[4]}\nID：{str(row[0])}\n\n"""))
        else:
            await message_number(numbers)

    if message.content.startswith(">question-editing"):
        content = message.content[24:]
        for row in list(db_read()):
            if int(row[1]) == int(message.author.id):
                ans = db_access(
                    str(message.content.split()[1]),
                    str(content)
                )
                if str(row[0]) == message.content.split()[1]:
                    if ans == True:
                        embed = discord.Embed(
                            title="QUESTION:",
                            description=f"ID：`{message.content.split()[1]}`\n<@{message.author.id}>さんが作成した質問\n\n**変更内容:**\n`{content}`",
                            color=discord.Color(0xc088ff),
                            timestamp=message.timestamp
                        )
                        embed.set_footer(
                            text="変更時刻:"
                        )
                        await client.send_message(message.channel,embed=embed)
                        return
        else:
            embed = discord.Embed(
                title="",
                description=f"もしコマンドが反応しなかった場合\nあなたにはこの認証コードを\n編集する権限がない証拠です...",
                color=discord.Color(0xc088ff),
                timestamp=message.timestamp
            )
            embed.set_footer(
                text="現在時刻:"
            )
            await client.send_message(message.channel,embed=embed)
            return

    if message.content.startswith(">locate"):
        async def answer_all(numbers):
            global embeds
            if db_count_up_1(str(message.content.split()[1])):
                for row in list(db_read()):
                    if str(row[0]) == message.content.split()[1]:
                        embed = discord.Embed(
                            title="QUESTION:",
                            description=f"""<@{row[1]}>さんの質問\n\n`{str(row[2])}`\n\n閲覧数：{row[3]}\n回答数：{row[4]}\nID：{str(row[0])}\n""",
                            color=discord.Color(0xc088ff),
                        )
                        await client.send_message(message.channel,embed=embed)
                for row1 in db_get_answer():
                    page = 1
                    join = "".join(numbers[(page - 1) * 2:page * 2])
                    if str(row1[0]) == message.content.split()[1]:
                        embeds = discord.Embed(
                            description=join + "-------------------------------",
                            color=discord.Color(0xc088ff),
                            timestamp=message.timestamp
                        )
                        embeds.set_footer(
                            text="表示時刻:"
                        )
                        msg = await client.send_message(message.channel,embed=embeds)
                        while True:
                            l = page != 1
                            r = page < len(numbers) / 2
                            if l:
                                await client.add_reaction(msg,left)
                            if r:
                                await client.add_reaction(msg,right)
                            react,user = await client.wait_for_reaction(check=predicate(msg,l,r))
                            if react.emoji == left:
                                page -= 1
                            elif react.emoji == right:
                                page += 1
                            join = "".join(numbers[(page - 1) * 2:page * 2])
                            embeds = discord.Embed(
                                description=join + "-------------------------------",
                                color=discord.Color(0xc088ff),
                                timestamp=message.timestamp
                            )
                            embeds.set_footer(
                                text="表示時刻:"
                            )
                            await client.edit_message(msg,embed=embeds)
                            await client.clear_reactions(msg)

        numbers = []
        for row1 in db_get_answer():
            if str(row1[0]) == message.content.split()[1]:
                numbers.append("".join(
                    [f"""-------------------------------\n<@{int(row1[2])}>さんの回答\n`{row1[1]}`\n\n"""]))
                print(numbers)
        await answer_all(numbers)

    if message.content.startswith(">answer "):
        def randomname(n):
            a = ''.join(random.choices(string.ascii_letters + string.digits,k=n))
            return a

        if message.content[14:] == "":
            embed = discord.Embed(
                description=f"{message.author.mention}さん\nメッセージを入力してくれよな！",
                color=discord.Color(0xc088ff),
            )
            await client.send_message(message.channel,embed=embed)
            return

        numbers = randomname(5)
        
        out_words = ["しね","金！暴力！SEX！（迫真）","おっぱい","ちんこ","まんこ","殺す","ちんぽ","おちんちん","アナル","sex","セックス","オナニー","おちんぽ","ちくび",
                     "乳首","陰茎","うざい","黙れ","きもい","やりますねぇ！","覚醒剤","覚せい剤","麻薬","コカイン","SEX","害児","pornhub","xvideo","せっくす",
                     "mother fucker","金正恩","penis","fuck","死ね","殺す","アホ","赤ちゃん製造ミルク","ザー汁","ザーメン","精液","精子","こ↑こ↓",
                     "やりますねぇ"]
        if any([True for s in out_words if s in message.content[14:]]):
            embed = discord.Embed(
                description=f"{message.author.mention}さん\n禁止用語が入っているので質問できません！",
                color=discord.Color(0xc088ff),
            )
            await client.send_message(message.channel,embed=embed)
            await client.delete_message(message)
            return
        for row in list(db_read()):
            if str(row[0]) == message.content.split()[1]:
                if db_count_up(str(message.content.split()[1])):
                    global counts
                    counts += 1
                    if db_answer(message.content.split()[1],message.content[14:],int(message.author.id),str(numbers)) == True:
                        embed = discord.Embed(
                            title="QUESTION:",
                            description=f"<@{int(message.author.id)}>さん\n解答内容:\n\n`{message.content[14:]}`",
                            color=discord.Color(0xc088ff),
                            timestamp=message.timestamp
                        )
                        embed.set_footer(
                            text="時刻:"
                        )
                        await client.send_message(message.channel,embed=embed)
                        for row1 in db_get_answer():
                            if int(row1[2]) == int(message.author.id):
                                if str(row1[0]) == str(row[0]):
                                    user = await client.get_user_info(f"{int(row[1])}")
                                    embeds = discord.Embed(
                                        title="QUESTION:",
                                        description=f"<@{int(message.author.id)}>さん\n解答先: `{str(row[2])}`\n\n解答内容:\n\n`{message.content[14:]}`\n\n解答識別ID:{numbers}",
                                        color=discord.Color(0xc088ff),
                                        timestamp=message.timestamp
                                    )
                                    embeds.set_footer(
                                        text="時刻:"
                                    )
                                    await client.send_message(user,embed=embeds)
                                    return

    if message.content.startswith(">best-answer"):
        if db_get_best_answer(str(message.content.split()[1])) == True:
            embed = discord.Embed(
                description=f"この質問にはもうすでにベストアンサーがついてるよ！",
                color=discord.Color(0xc088ff),
                timestamp=message.timestamp
            )
            embed.set_footer(
                text="時刻:"
            )
            await client.send_message(message.channel,embed=embed)
            return
        else:
            for row,row1 in zip(list(db_read()),db_get_answer()):
                if str(row1[3]) == message.content.split()[1]:
                    if int(row1[2]) == int(message.author.id):
                        embed = discord.Embed(
                            description=f"{message.author.mention}さん\n自分の回答はベストアンサーすることができません...",
                            color=discord.Color(0xc088ff),
                        )
                        await client.send_message(message.channel,embed=embed)
                        return
                    if message.content.split()[1] == "":
                        embed = discord.Embed(
                            description=f"{message.author.mention}さん\nメッセージを入力してくれよな！",
                            color=discord.Color(0xc088ff),
                        )
                        await client.send_message(message.channel,embed=embed)
                        return
                    if db_write_best_answer(str(message.content.split()[1])) == True:
                        if db_access_answer(str(message.content.split()[1]),str(row1[1])):
                            if str(row1[0]) == str(row[0]):
                                user = await client.get_user_info(f"{int(row1[2])}")
                                embeds = discord.Embed(
                                    title="QUESTION:",
                                    description=f"<@{int(row1[2])}>さんの回答をベストアンサーにしました！",
                                    color=discord.Color(0xc088ff),
                                    timestamp=message.timestamp
                                )
                                embeds.set_footer(
                                    text="時刻:"
                                )
                                await client.send_message(message.channel,embed=embeds)
                                embeds = discord.Embed(
                                    title="QUESTION:",
                                    description=f"あなたの回答がベストアンサーに認定されました！\n\n解答先: `{str(row[2])}`\n\n解答内容:\n\n`{row1[1]}`",
                                    color=discord.Color(0xc088ff),
                                    timestamp=message.timestamp
                                )
                                embeds.set_footer(
                                    text="時刻:"
                                )
                                await client.send_message(user,embed=embeds)
                                return db_count_up_2(int(row1[2])) == True

    if message.content == ">answer-top":
        async def send(member_data):
            embed = discord.Embed(
                title="Best-Answer-Top10",
                color=discord.Color(0xc088ff),
                description=member_data
            )
            await client.send_message(message.channel,embed=embed)

        i = 1
        member_data = ""
        for row in db_get():
            print(row)
            member_data += "{0}位: <@{1}> [`合計:{2}回`]\n".format(i,row[0],row[1])
            if i % 10 == 0:
                await send(member_data)
                member_data = ""
            i += 1
        else:
            await send(member_data)
            return

    if message.content.startswith(">question-delete"):
        if message.content.split()[1] == "":
            embed = discord.Embed(
                description=f"{message.author.mention}さん\nメッセージを入力してくれよな！",
                color=discord.Color(0xc088ff),
            )
            await client.send_message(message.channel,embed=embed)
            return

        for row in list(db_read()):
            if int(row[1]) == int(message.author.id):
                if str(row[0]) == message.content.split()[1]:
                    if db_reset_question(int(message.author.id),str(message.content.split()[1])) == True:
                        embed = discord.Embed(
                            description=f"<@{message.author.id}>さんが自身の質問を削除しました。",
                            color=discord.Color(0xc088ff),
                        )
                        await client.send_message(message.channel,embed=embed)
                        return
        else:
            embed = discord.Embed(
                description=f"もしコマンドが反応しなかった場合\nあなたにはこのコードを\n削除する権限がない証拠です...",
                color=discord.Color(0xc088ff),
                timestamp=message.timestamp
            )
            embed.set_footer(
                text="現在時刻:"
            )
            await client.send_message(message.channel,embed=embed)
            return

    if message.content.startswith(">>question-delete"):
        for row in list(db_read()):
            kengensya = ["304932786286886912","439725181389373442"]
            if message.author.id in kengensya:
                if str(row[0]) == message.content.split()[1]:
                    if db_reset_all_question(str(message.content.split()[1])) == True:
                        embed = discord.Embed(
                            description=f"<@{message.author.id}>さんが強制的に質問を削除しました。",
                            color=discord.Color(0xc088ff),
                        )
                        await client.send_message(message.channel,embed=embed)
                        return
            else:
                embed = discord.Embed(
                    description="このコマンドはBOTの管理者のみ使用可能です。",
                    color=discord.Color(0xc088ff),
                )
                await client.send_message(message.channel,embed=embed)
                return

def db_read():
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS question(create_id varchar, create_name Bigint, question text, answer_id INT, answer_question text, locate_number int);")
    c.execute('''SELECT create_id,create_name,question,locate_number,answer_id from question;''')
    ans = c.fetchall()
    for row in ans:
        yield (row[0],row[1],row[2],row[3],row[4])
    else:
        con.commit()
        c.close()
        con.close()


def db_read_count():
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS question(create_id varchar, create_name Bigint, question text, answer_id INT, answer_question text, locate_number int);")
    c.execute('''SELECT sum(locate_number),sum(answer_id) from question;''')
    ans = c.fetchall()
    for row in ans:
        yield (row[0],row[1])
    else:
        con.commit()
        c.close()
        con.close()


def db_access(create_id,question):
    create_id = str(create_id)
    question = str(question)
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS question(create_id varchar, create_name Bigint, question text, answer_id INT, answer_question text, locate_number int);")
    c.execute("""UPDATE question set question=%s where create_id=%s;""",(question,create_id))
    con.commit()
    c.close()
    con.close()
    return True


def db_count_up(create_id):
    create_id = str(create_id)
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS question(create_id varchar, create_name Bigint, question text, answer_id INT, answer_question text, locate_number int);")
    c.execute("UPDATE question set answer_id = answer_id + 1 where create_id=%s;",(create_id,))
    con.commit()
    c.close()
    con.close()
    return True


def db_count_up_1(create_id):
    create_id = str(create_id)
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS question(create_id varchar, create_name Bigint, question text, answer_id INT, answer_question text, locate_number int);")
    c.execute("UPDATE question set locate_number = locate_number + 1 where create_id=%s;",(create_id,))
    con.commit()
    c.close()
    con.close()
    return True


def db_write(create_id,create_name,question,):
    create_id = str(create_id)
    create_name = int(create_name)
    question = str(question)
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS question(create_id varchar, create_name Bigint, question text, answer_id INT, answer_question text, locate_number int);")
    c.execute("INSERT INTO question(create_id, create_name, question,locate_number,answer_id) VALUES(%s,%s,%s,0,0);",
              (create_id,create_name,question))
    con.commit()
    c.close()
    con.close()
    return True


def db_count_up_2(create_name):
    create_name = int(create_name)
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS question_number(create_name Bigint);")
    c.execute("INSERT INTO question_number(create_name) VALUES(%s);",
              (create_name,))
    print(con)
    con.commit()
    c.close()
    con.close()
    return True

def db_get():
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS question_number(create_name Bigint);")
    c.execute("select create_name, count(*) from question_number group by create_name order by count(*) desc")
    ans = c.fetchall()
    for row in ans:
        print(row)
        yield (row[0],row[1])

def db_get_answer_number(create_name):
    create_name = int(create_name)
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS question_test(create_id varchar ,answer_questions text,create_name Bigint,number_id varchar);")
    c.execute('''SELECT create_name from question_test where create_name=%s;''',(create_name,))
    ans = c.fetchall()
    for row in ans:
        yield (row)
    else:
        con.commit()
        c.close()
        con.close()

def db_get_answer():
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS question_test(create_id varchar ,answer_questions text,create_name Bigint,number_id varchar);")
    c.execute('''SELECT create_id,answer_questions,create_name,number_id from question_test;''')
    ans = c.fetchall()
    for row in ans:
        yield (row[0],row[1],row[2],row[3])
    else:
        con.commit()
        c.close()
        con.close()

def db_access_answer(create_id,answer_question):
    create_id = str(create_id)
    answer_question = str(answer_question)
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute(
            "CREATE TABLE IF NOT EXISTS question_test(create_id varchar ,answer_questions text,create_name Bigint,number_id varchar);")
    c.execute("""UPDATE question_test set answer_questions='Best-Answer!!\n' || %s where number_id=%s;""",(answer_question,create_id,))
    con.commit()
    c.close()
    con.close()
    return True

def db_answer(create_id,answer_question,create_name,number_id):
    create_id = str(create_id)
    answer_question = str(answer_question)
    create_name = int(create_name)
    number_id = str(number_id)
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS question_test(create_id varchar ,answer_questions text,create_name Bigint,number_id varchar);")
    c.execute("INSERT INTO question_test(answer_questions, create_id, create_name, number_id) VALUES(%s,%s,%s,%s);",
              (answer_question,create_id,create_name,number_id))
    con.commit()
    c.close()
    con.close()
    return True

def db_write_best_answer(create_id):
    create_id = str(create_id)
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS question_answer(create_id varchar);")
    c.execute("INSERT INTO question_answer(create_id) VALUES(%s);",
              (create_id,))
    con.commit()
    c.close()
    con.close()
    return True

def db_get_best_answer(create_id):
    create_id = str(create_id)
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS question_answer(create_id varchar);")
    c.execute('SELECT * FROM question_answer WHERE create_id=%s;',(create_id,))
    if c.fetchall():
        con.commit()
        c.close()
        con.close()
        return True

def db_reset_question(create_name,create_id):
    create_name = int(create_name)
    create_id = str(create_id)
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS question(create_id varchar, create_name Bigint, question text, answer_id INT, answer_question text, locate_number int);")
    c.execute("delete from question where create_name=%s AND create_id=%s;",(create_name,create_id,))
    con.commit()
    c.close()
    con.close()
    return True


def db_reset_all_question(create_id):
    create_id = str(create_id)
    con = psycopg2.connect(os.environ.get("DATABASE_URL"))
    c = con.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS question(create_id varchar, create_name Bigint, question text, answer_id INT, answer_question text, locate_number int);")
    c.execute("delete from question where create_id=%s;",(create_id,))
    con.commit()
    c.close()
    con.close()
    return True


client.run(os.environ.get("TOKEN"))
