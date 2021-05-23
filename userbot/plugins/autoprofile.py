# ©source zEd - @ZedThon


import asyncio
import base64
import os
import random
import shutil
import time
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont
from pySmartDL import SmartDL
from telethon.errors import FloodWaitError
from telethon.tl import functions

from . import AUTONAME, BOTLOG, BOTLOG_CHATID, DEFAULT_BIO
from .sql_helper.globals import addgvar, delgvar, gvarstatus

DEFAULTUSERBIO = DEFAULT_BIO or " 𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 𝙕𝞝𝘿𝙏𝙃𝙊𝙉 𝐒𝐎𝐔𝐑𝐂𝐄  "
CHANGE_TIME = Config.CHANGE_TIME
DEFAULTUSER = AUTONAME or Config.ALIVE_NAME

FONT_FILE_TO_USE = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

autopic_path = os.path.join(os.getcwd(), "userbot", "original_pic.png")
digitalpic_path = os.path.join(os.getcwd(), "userbot", "digital_pic.png")
autophoto_path = os.path.join(os.getcwd(), "userbot", "photo_pfp.png")

digitalpfp = Config.DIGITAL_PIC or "https://telegra.ph/file/f72cde9805f01e0bf04ed.jpg"


@bot.on(admin_cmd(pattern="autopic ?(.*)"))
async def autopic(event):
    if event.fwd_from:
        return
    if Config.DEFAULT_PIC is None:
        return await edit_delete(
            event,
            "**عـذرا هنـاك خطـأ**\n وظيفة الصورة التـلقائيـة تحتاج إلى ضبط DEFAULT PIC var في Heroku vars",
            parse_mode=parse_pre,
        )
    downloader = SmartDL(Config.DEFAULT_PIC, autopic_path, progress_bar=False)
    downloader.start(blocking=False)
    while not downloader.isFinished():
        pass
    input_str = event.pattern_match.group(1)
    if input_str:
        try:
            input_str = int(input_str)
        except ValueError:
            input_str = 60
    else:
        if gvarstatus("autopic_counter") is None:
            addgvar("autopic_counter", 30)
    if gvarstatus("autopic") is not None and gvarstatus("autopic") == "true":
        return await edit_delete(event, f"`تـم تفـعيل التـغير التـلقائـي للـصور `")
    addgvar("autopic", True)
    if input_str:
        addgvar("autopic_counter", input_str)
    await edit_delete(event, f"`بـدأ التـغيـر الصور التـلقائي `")
    await autopicloop()



@bot.on(admin_cmd(pattern="اسم تلقائي$"))
async def _(event):
    if event.fwd_from:
        return
    if gvarstatus("اسم تلقائي") is not None and gvarstatus("اسم تلقائي") == "true":
        return await edit_delete(event, f"**الاسم التلقائي ممكّن بالفعل 𓄼**")
    addgvar("اسم تلقائي", True)
    await edit_delete(event, "**تـم بـدأ الاسـم التـلقائـي 𓄼**")
    await autoname_loop()


@bot.on(admin_cmd(pattern="نبذة تلقائي$"))
async def _(event):
    if event.fwd_from:
        return
    if gvarstatus("نبذة تلقائي") is not None and gvarstatus("نبذة تلقائي") == "true":
        return await edit_delete(event, f"** الـنبذة التلقائيه مفعـلة 𓄼**")
    addgvar("نبذة تلقائي", True)
    await edit_delete(event, "")
    await autobio_loop()


@bot.on(admin_cmd(pattern="انهاء (.*)"))
async def _(event):  # sourcery no-metrics
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if input_str == "autopic":
        if gvarstatus("autopic") is not None and gvarstatus("autopic") == "true":
            delgvar("autopic")
            if os.path.exists(autopic_path):
                file = await event.client.upload_file(autopic_path)
                try:
                    await event.client(functions.photos.UploadProfilePhotoRequest(file))
                    os.remove(autopic_path)
                except BaseException:
                    return
            return await edit_delete(event, "`Autopic has been stopped now`")
        return await edit_delete(event, "`Autopic haven't enabled`")
    if input_str == "digitalpfp":
        if gvarstatus("digitalpic") is not None and gvarstatus("digitalpic") == "true":
            delgvar("digitalpic")
            await event.client(
                functions.photos.DeletePhotosRequest(
                    await bot.get_profile_photos("me", limit=1)
                )
            )
            return await edit_delete(event, "`Digitalpfp has been stopped now`")
        return await edit_delete(event, "`Digitalpfp haven't enabled`")
    if input_str == "bloom":
        if gvarstatus("bloom") is not None and gvarstatus("bloom") == "true":
            delgvar("bloom")
            if os.path.exists(autopic_path):
                file = await event.client.upload_file(autopic_path)
                try:
                    await event.client(functions.photos.UploadProfilePhotoRequest(file))
                    os.remove(autopic_path)
                except BaseException:
                    return
            return await edit_delete(event, "`Bloom has been stopped now`")
        return await edit_delete(event, "`Bloom haven't enabled`")
    if input_str == "اسم تلقائي":
        if gvarstatus("اسم تلقائي") is not None and gvarstatus("اسم تلقائي") == "true":
            delgvar("اسم تلقائي")
            await event.client(
                functions.account.UpdateProfileRequest(first_name=DEFAULTUSER)
            )
            return await edit_delete(event, "**تم إيقاف الاسم التلقائي الآن 𓄼**")
        return await edit_delete(event, "**لم يتم تمكين الاسم التلقائي 𓄼**")
    if input_str == "نبذة تلقائي":
        if gvarstatus("نبذة تلقائي") is not None and gvarstatus("نبذة تلقائي") == "true":
            delgvar("نبذة تلقائي")
            await event.client(
                functions.account.UpdateProfileRequest(about=DEFAULTUSERBIO)
            )
            return await edit_delete(event, "`Autobio has been stopped now`")
        return await edit_delete(event, "`Autobio haven't enabled`")


async def autopicloop():
    AUTOPICSTART = gvarstatus("autopic") == "true"
    if AUTOPICSTART and Config.DEFAULT_PIC is None:
        if BOTLOG:
            return await bot.send_message(
                BOTLOG_CHATID,
                "**Error**\n`For functing of autopic you need to set DEFAULT_PIC var in Heroku vars`",
            )
        return
    if gvarstatus("autopic") is not None:
        try:
            counter = int(gvarstatus("autopic_counter"))
        except Exception as e:
            LOGS.warn(str(e))
    while AUTOPICSTART:
        if not os.path.exists(autopic_path):
            downloader = SmartDL(Config.DEFAULT_PIC, autopic_path, progress_bar=False)
            downloader.start(blocking=False)
            while not downloader.isFinished():
                pass
        shutil.copy(autopic_path, autophoto_path)
        im = Image.open(autophoto_path)
        file_test = im.rotate(counter, expand=False).save(autophoto_path, "PNG")
        current_time = datetime.now().strftime("  Time: %H:%M \n  Date: %d.%m.%y ")
        img = Image.open(autophoto_path)
        drawn_text = ImageDraw.Draw(img)
        fnt = ImageFont.truetype(FONT_FILE_TO_USE, 30)
        drawn_text.text((150, 250), current_time, font=fnt, fill=(124, 252, 0))
        img.save(autophoto_path)
        file = await bot.upload_file(autophoto_path)
        try:
            await bot(functions.photos.UploadProfilePhotoRequest(file))
            os.remove(autophoto_path)
            counter += counter
            await asyncio.sleep(CHANGE_TIME)
        except BaseException:
            return
        AUTOPICSTART = gvarstatus("autopic") == "true"


async def digitalpicloop():
    DIGITALPICSTART = gvarstatus("digitalpic") == "true"
    i = 0
    while DIGITALPICSTART:
        if not os.path.exists(digitalpic_path):
            downloader = SmartDL(digitalpfp, digitalpic_path, progress_bar=False)
            downloader.start(blocking=False)
            while not downloader.isFinished():
                pass
        shutil.copy(digitalpic_path, autophoto_path)
        Image.open(autophoto_path)
        current_time = datetime.now().strftime("%H:%M")
        img = Image.open(autophoto_path)
        drawn_text = ImageDraw.Draw(img)
        cat = str(base64.b64decode("dXNlcmJvdC9oZWxwZXJzL3N0eWxlcy9kaWdpdGFsLnR0Zg=="))[
            2:36
        ]
        fnt = ImageFont.truetype(cat, 200)
        drawn_text.text((350, 100), current_time, font=fnt, fill=(124, 252, 0))
        img.save(autophoto_path)
        file = await bot.upload_file(autophoto_path)
        try:
            if i > 0:
                await bot(
                    functions.photos.DeletePhotosRequest(
                        await bot.get_profile_photos("me", limit=1)
                    )
                )
            i += 1
            await bot(functions.photos.UploadProfilePhotoRequest(file))
            os.remove(autophoto_path)
            await asyncio.sleep(CHANGE_TIME)
        except BaseException:
            return
        DIGITALPICSTART = gvarstatus("digitalpic") == "true"


async def bloom_pfploop():
    BLOOMSTART = gvarstatus("bloom") == "true"
    if BLOOMSTART and Config.DEFAULT_PIC is None:
        if BOTLOG:
            return await bot.send_message(
                BOTLOG_CHATID,
                "**Error**\n`For functing of bloom you need to set DEFAULT_PIC var in Heroku vars`",
            )
        return
    while BLOOMSTART:
        if not os.path.exists(autopic_path):
            downloader = SmartDL(Config.DEFAULT_PIC, autopic_path, progress_bar=False)
            downloader.start(blocking=False)
            while not downloader.isFinished():
                pass
        # RIP Danger zone Here no editing here plox
        R = random.randint(0, 256)
        B = random.randint(0, 256)
        G = random.randint(0, 256)
        FR = 256 - R
        FB = 256 - B
        FG = 256 - G
        shutil.copy(autopic_path, autophoto_path)
        image = Image.open(autophoto_path)
        image.paste((R, G, B), [0, 0, image.size[0], image.size[1]])
        image.save(autophoto_path)
        current_time = datetime.now().strftime("\n Time: %H:%M:%S \n \n Date: %d/%m/%y")
        img = Image.open(autophoto_path)
        drawn_text = ImageDraw.Draw(img)
        fnt = ImageFont.truetype(FONT_FILE_TO_USE, 60)
        ofnt = ImageFont.truetype(FONT_FILE_TO_USE, 250)
        drawn_text.text((95, 250), current_time, font=fnt, fill=(FR, FG, FB))
        drawn_text.text((95, 250), " 𓄼", font=ofnt, fill=(FR, FG, FB))
        img.save(autophoto_path)
        file = await bot.upload_file(autophoto_path)
        try:
            await bot(functions.photos.UploadProfilePhotoRequest(file))
            os.remove(autophoto_path)
            await asyncio.sleep(CHANGE_TIME)
        except BaseException:
            return
        BLOOMSTART = gvarstatus("bloom") == "true"


async def autoname_loop():
    AUTONAMESTART = gvarstatus("اسم تلقائي") == "true"
    while AUTONAMESTART:
        DM = time.strftime("%d-%m-%y")
        HM = time.strftime("%H:%M")
        name = f"𓄼 {HM} 𓄹 "
        LOGS.info(name)
        try:
            await bot(functions.account.UpdateProfileRequest(first_name=name))
        except FloodWaitError as ex:
            LOGS.warning(str(ex))
            await asyncio.sleep(ex.seconds)
        await asyncio.sleep(CHANGE_TIME)
        AUTONAMESTART = gvarstatus("اسم تلقائي") == "true"


async def autobio_loop():
    AUTOBIOSTART = gvarstatus("autobio") == "true"
    while AUTOBIOSTART:
        DMY = time.strftime("%d.%m.%Y")
        HM = time.strftime("%H:%M:%S")
        bio = f" - {DEFAULTUSERBIO} - 𓄼 {HM}"
        LOGS.info(bio)
        try:
            await bot(functions.account.UpdateProfileRequest(about=bio))
        except FloodWaitError as ex:
            LOGS.warning(str(ex))
            await asyncio.sleep(ex.seconds)
        await asyncio.sleep(CHANGE_TIME)
        AUTOBIOSTART = gvarstatus("autobio") == "true"


bot.loop.create_task(autopicloop())
bot.loop.create_task(digitalpicloop())
bot.loop.create_task(bloom_pfploop())
bot.loop.create_task(autoname_loop())
bot.loop.create_task(autobio_loop())


CMD_HELP.update(
    {
        "autoprofile": """**Plugin : **`autoprofile`
•  **Syntax : **`.autopic angle`
•  **Function : **__Rotating image along with the time on it with given angle if no angle is given then doesnt rotate. You need to set __`DEFAULT_PIC`__ in heroku__
•  **Syntax : **`.digitalpfp`
•  **Function : **__Your profile pic changes to digitaltime profile picutre__
•  **Syntax : **`.bloom`
•  **Function : **__Random colour profile pics will be set along with time on it. You need to set__ `DEFAULT_PIC`__ in heroku__
•  **Syntax : **`.autoname`
•  **Function : **__for time along with name, you must set __`AUTONAME`__ in the heroku vars first for this to work__
•  **Syntax : **`.autopic`
•  **Function : **__for time along with your bio, Set __`DEFAULT_BIO`__ in the heroku vars first__
•  **Syntax : **`.end + `
•  **Function : **__To stop the given functions like autopic ,difitalpfp , bloom , autoname and autobio__
**⚠️DISCLAIMER⚠️**
__USING THIS PLUGIN CAN RESULT IN ACCOUNT BAN. WE ARE NOT RESPONSIBLE FOR YOUR BAN.__
"""
    }
)