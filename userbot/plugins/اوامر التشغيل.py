import sys
from os import execl

from . import BOTLOG, BOTLOG_CHATID, HEROKU_APP, bot, mention


@icssbot.on(admin_cmd(pattern="اعاده تشغيل$"))
@icssbot.on(sudo_cmd(pattern="اعاده تشغيل$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, "#اعاده_التشغيل \n" "⪼ بوت تلثون روليكس في وضع اعاده التشغيل انتظر"
        )
    await edit_or_reply(
        event,
        f"**⌔∮ اهلا عزيزي** - {mention}\n"
        f"**يتم الان اعـادة تشغيـل بـوت تلثون روليكس يستغـرق الامر 1-2 دقيقه ▬▭ ...**",
    )
    await bot.disconnect()
    execl(sys.executable, sys.executable, *sys.argv)


@icssbot.on(admin_cmd(pattern="ايقاف$"))
@icssbot.on(sudo_cmd(pattern="ايقاف$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, "#اطفاء \n" "بوت ريس ثـون في وضع الاطفاء"
        )
    await edit_or_reply(
        event, "**جارٍ إيقاف تشغيل بوت تلثون روليكس الآن ... شغِّلني يدويًا لاحقًا**"
    )
    if HEROKU_APP is not None:
        HEROKU_APP.process_formation()["userbot"].scale(0)
    else:
        sys.exit(0)


CMD_HELP.update(
    {
        "اوامر التشغيل": "**اسم الاضافـه : **`اوامر التشغيل`\
        \n\n  •  **╮•❐ الامـر ⦂ **`.اعاده تشغيل`\
        \n  •  **الشـرح •• **__اعـادة تشغيـل البوت اذا حدثت اخطـاء او  شيئ آخر قد يتوقف دقيقـه ثم يعـود للعمل...__\
        \n\n  •  **╮•❐ الامـر ⦂ **`.ايقاف`\
        \n**  •  الشـرح •• **__لإيقاف تشغيل البوت من هيروكو. لا يمكنك اعادة التشغيل بواسطة الروبوت ، فأنت بحاجة إلى الوصول إلى هيروكو وتشغيله أو استخدام ___ @hk_heroku_bot"
    }
)
