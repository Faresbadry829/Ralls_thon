import platform
import sys
from datetime import datetime

import psutil
from telethon import __version__

from . import ALIVE_NAME

# ================= CONSTANT =================
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "icss"
# ============================================


@icssbot.on(admin_cmd(outgoing=True, pattern=r"النظام$"))
@icssbot.on(sudo_cmd(allow_sudo=True, pattern=r"النظام$"))
async def psu(event):
    uname = platform.uname()
    softw = "<b> 𓆩 𝑺𝑶𝑼𝑹𝑪𝑬 𝙕𝞝𝘿𝙏𝙃𝙊𝙉 𝑺𝒀𝑺𝑻𝑬𝑴 𝑰𝑵𝑭𝑶 𓆪 </b>\n"
    softw += f"<b> ⌔∮ النظام :↬ </b> `{uname.system}`\n"
    softw += f"<b> ⌔∮ المرجع  :↬ </b> `{uname.release}`\n"
    softw += f"<b> ⌔∮ الاصدار  :↬ </b> `{uname.version}`\n"
    softw += f"<b> ⌔∮ النـوع  :↬ </b> `{uname.machine}`\n"
    # Boot Time
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    softw += f"<b> ⌔∮ تاريـخ التنصيب:↬ </b> `{bt.day}/{bt.month}/{bt.year}  {bt.hour}:{bt.minute}:{bt.second}`\n"
    # CPU Cores
    cpuu = "**- معلومات المعالـج**\n"
    cpuu += "**⌔∮ الماديـه   :** `" + str(psutil.cpu_count(logical=False)) + "`\n"
    cpuu += "**⌔∮ الكليـه      :** `" + str(psutil.cpu_count(logical=True)) + "`\n"
    # CPU frequencies
    cpufreq = psutil.cpu_freq()
    cpuu += f"<b> ⌔∮ اعلـى تـردد    :↬ </b> `{cpufreq.max:.2f}Mhz`\n"
    cpuu += f"<b> ⌔∮ اقـل تـردد    :↬ </b> `{cpufreq.min:.2f}Mhz`\n"
    cpuu += f"<b> ⌔∮ التـردد القياسـي:↬ </b> `{cpufreq.current:.2f}Mhz`\n\n"
    # CPU usage
    cpuu += "**- استخدامات المعالج لكل وحده**\n"
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
        cpuu += f"<b> ⌔∮ كـور {i}  :↬ </b> `{percentage}%`\n"
    cpuu += "**- Total CPU Usage**\n"
    cpuu += f"<b> ⌔∮ الكـليه:↬ </b> `{psutil.cpu_percent()}%`\n"
    # RAM Usage
    svmem = psutil.virtual_memory()
    memm = "**- استخدامـات الذاكـره**\n"
    memm += f"<b> ⌔∮ الكـليه     :↬ </b> `{get_size(svmem.total)}`\n"
    memm += f"<b> ⌔∮ الفعليـه :↬ </b> `{get_size(svmem.available)}`\n"
    memm += f"<b> ⌔∮ المستخدمـه      :↬ </b> `{get_size(svmem.used)}`\n"
    memm += f"<b> ⌔∮ المتاحـه:↬ </b> `{svmem.percent}%`\n"
    # Bandwidth Usage
    bw = "**- استخدامات الباندويـدث**\n"
    bw += f"<b> ⌔∮ الرفـع  :↬ </b> `{get_size(psutil.net_io_counters().bytes_sent)}`\n"
    bw += f"<b> ⌔∮ التحميـل :↬ </b> `{get_size(psutil.net_io_counters().bytes_recv)}`\n"
    help_string = f"{str(softw)}\n"
    help_string += f"{str(cpuu)}\n"
    help_string += f"{str(memm)}\n"
    help_string += f"{str(bw)}\n"
    help_string += "**Engine Info**\n"
    help_string += f"<b> ⌔∮ بايثـون ↬ </b> `{sys.version}`\n"
    help_string += f"<b> ⌔∮ تيليثـون ↬ </b> `{__version__}`"
    await event.edit(help_string)


def get_size(inputbytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if inputbytes < factor:
            return f"{inputbytes:.2f}{unit}{suffix}"
        inputbytes /= factor


@icssbot.on(admin_cmd(pattern="cpu$"))
@icssbot.on(sudo_cmd(pattern="cpu$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    cmd = "ics /proc/cpuinfo | grep 'model name'"
    o = (await _icssutils.runcmd(cmd))[0]
    await edit_or_reply(
        event, f"**[- icss’s](tg://need_update_for_some_feature/) CPU Model:**\n{o}"
    )


@icssbot.on(admin_cmd(pattern=f"sysd$", outgoing=True))
@icssbot.on(sudo_cmd(pattern=f"sysd$", allow_sudo=True))
async def sysdetails(sysd):
    cmd = "git clone https://github.com/dylanaraps/neofetch.git"
    await _catutils.runcmd(cmd)
    neo = "neofetch/neofetch --off --color_blocks off --bold off --cpu_temp C \
                    --cpu_speed on --cpu_cores physical --kernel_shorthand off --stdout"
    a, b, c, d = await _catutils.runcmd(neo)
    result = str(a) + str(b)
    await edit_or_reply(sysd, "Neofetch Result: `" + result + "`")


CMD_HELP.update(
    {
        "النظام": "**Plugin : **`النظام`\
        \n\n**Syntax : **`.النظام`\
        \n**Function : **__Show system specification.__\
        \n\n**Syntax : **`.sysd`\
        \n**Function : **__Shows system information using neofetch.__\
        \n\n**Syntax : **`.cpu`\
        \n**Function : **__shows the cpu information__\
    "
    }
)
