alv = (
"""
**©Rolix - @RolixXx1
  - Plugin Alive** 
  - **Commend:** `.السورس`
  - **Function:** لعرض معلومات السورس
"""
)

import time
from platform import python_version
from telethon import version
from resources.strings import *

from . import ALIVE_NAME, StartTime, get_readable_time, icsv, mention
from . import reply_id as rd

DEFAULTUSER = ALIVE_NAME or "Rolix"
ICSS_IMG = Config.ALIVE_PIC or "https://telegra.ph/file/886a14cb392a7fd6f4ee5.jpg"
ICSS_TEXT = Config.CUSTOM_ALIVE_TEXT or "اهلا بك في سورس تلثون روليكس"
ICSEM = Config.CUSTOM_ALIVE_EMOJI or "⌔︙"


@icssbot.on(admin_cmd(outgoing=True, pattern="السورس$"))
@icssbot.on(sudo_cmd(pattern="السورس$", allow_sudo=True))
async def ica(icss):
    if icss.fwd_from:
        return
    ics_id = await rd(icss)
    icsupt = await get_readable_time((time.time() - StartTime))
    _, check_sgnirts = check_data_base_heal_th()
    if ICSS_IMG:
        ics_c = f"**{ICSS_TEXT}**\n"
        ics_c += f"𓍹ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ𓍻 \n"
        ics_c += f"**{ICSEM} اصدار تلثون روليكس ↫** `{icsv}`\n"
        ics_c += f"**{ICSEM} مدة التشغيل ↫** `{icsupt}`\n"
        ics_c += f"**{ICSEM} المستخدم ↫** {mention}\n"
        ics_c += f"**{ICSEM} **  **[قـنـاة الـسـورس]**(https://t.me/RolixXx1) .\n"
        ics_c += f"**{ICSEM} **  **[المطــــــور ¹𓆰]**(https://t.me/YY_YPY) .  \n"
        ics_c += f"**{ICSEM} **  **[المطــــــور ²𓆰]**(https://t.me/vod_ik_ax) .  \n"
        ics_c += f"𓍹ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ𓍻\n"
        await icss.client.send_file(
            icss.chat_id, ICSS_IMG, caption=ics_c, reply_to=ics_id
        )
        await icss.delete()
    else:
        await eor(
            icss,
            f"**{ICSS_TEXT}**\n\n"
            f"**{ICSEM} قاعدة البيانات ↫**  `{check_sgnirts}`\n"
            f"**{ICSEM} اصدار التليثون  ↫** `{version.__version__}\n`"
            f"**{ICSEM} اصدار تلثون روليكس ↫** `{icsv}`\n"
            f"**{ICSEM} اصدار البايثون  ↫** `{python_version()}\n`"
            f"**{ICSEM} مدة التشغيل ↫** `{icsupt}\n`"
            f"**{ICSEM} المستخدم ↫** {mention}\n",
        )


def check_data_base_heal_th():
    is_database_working = False
    output = "لم يتم تعيين قاعدة بيانات"
    if not Config.DB_URI:
        return is_database_working, output
    from userbot.plugins.sql_helper import SESSION

    try:
        SESSION.execute("SELECT 1")
    except Exception as e:
        output = f"❌ {str(e)}"
        is_database_working = False
    else:
        output = "تعمل بنجاح"
        is_database_working = True
    return is_database_working, output


CMD_HELP.update({"alive": f"{alv}"})
