import discord
from discord.ext import tasks, commands
import datetime
import os
import random

# ENV-Variablen aus Railway
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Wirtschaftssprüche für Montag
montag_sprueche = [
    "„Geld verdienen ist ein Nebenprodukt von Werterschaffung.“ – Tobias Knoof",
    "„Der Markt kann länger irrational bleiben, als du solvent bleiben kannst.“ – John Maynard Keynes",
    "„Die Wirtschaft ist zu wichtig, um sie allein den Ökonomen zu überlassen.“ – Unbekannt",
    "„Reich wird man erst durch Dinge, die man nicht begehrt.“ – Mahatma Gandhi",
    "„Erfolg ist nicht endgültig, Misserfolg ist nicht fatal – was zählt, ist der Mut weiterzumachen.“ – Winston Churchill",
]

# Motivationssprüche für Mittwoch
mittwoch_sprueche = [
    "„Die Kunst ist, einmal mehr aufzustehen, als man umgeworfen wird.“ – Winston Churchill",
    "„Erfolg hat drei Buchstaben: TUN.“ – Goethe",
    "„Es wird nicht leichter. Du wirst besser.“",
    "„Je steiniger der Weg, desto wertvoller das Ziel.“",
    "„Sei jeden Tag stärker als deine stärkste Ausrede.“",
]

# Freundliche Freitagssprüche
freitag_sprueche = [
    "Fast geschafft. Mach ihn dir so schön, wie du kannst.",
    "Freitag – der schönste Tag der Woche. Wahrscheinlich du selbst.",
    "Nur noch ein bisschen. Kaffee hilft. Gute Laune auch.",
]

# Nachrichtentext-Vorlagen
def get_monday_message():
    return (
        "Guten Morgen ☕️\n"
        "Neue Woche, neues Kapitel.\n"
        f"Denk dran:\n_{random.choice(montag_sprueche)}_\n"
        "Du musst nicht perfekt starten – nur ehrlich mit dir selbst.\n"
        "Mach was draus 💼"
    )

def get_tuesday_message():
    return (
        "Hey – guten Morgen 🌤\n"
        "Dienstag ist wie ein unauffälliger Freund: Er ist da, aber macht keinen Lärm.\n"
        "Also – durchatmen, weitergehen.\n"
        "Einen ruhigen, produktiven Tag dir 👊"
    )

def get_wednesday_message():
    return (
        "Guten Morgen ✨\n"
        "Halbzeit. Vielleicht war die Woche hart – aber du bist noch da.\n"
        f"_{random.choice(mittwoch_sprueche)}_\n"
        "Heute geht noch was. Du bist stärker, als du denkst 💪"
    )

def get_thursday_message():
    return (
        "Moin ☁️\n"
        "Es ist Donnerstag. Noch nicht ganz geschafft, aber du bist nah dran.\n"
        "Nimm dir heute 5 Minuten nur für dich. Ohne Handy. Ohne Ablenkung.\n"
        "Du verdienst Klarheit 🧘"
    )

def get_friday_message():
    return (
        "Guten Morgen 🥐\n"
        f"{random.choice(freitag_sprueche)}"
    )

def get_friday_evening_message():
    return (
        "20:00 Uhr – Feierabend.\n"
        "Du hast’s gepackt.\n"
        "Jetzt ist Zeit zum Loslassen, Abschalten, Energie tanken.\n\n"
        "Hab ein richtig gutes Wochenende! 🍷📚🎧"
    )

@bot.event
async def on_ready():
    print(f"Eingeloggt als {bot.user}")
    send_daily_message.start()
    send_friday_evening_message.start()

@tasks.loop(minutes=1)
async def send_daily_message():
    now = datetime.datetime.now()
    if now.hour == 8 and now.minute == 0:
        channel = bot.get_channel(CHANNEL_ID)
        weekday = now.weekday()

        if weekday == 0:
            msg = get_monday_message()
        elif weekday == 1:
            msg = get_tuesday_message()
        elif weekday == 2:
            msg = get_wednesday_message()
        elif weekday == 3:
            msg = get_thursday_message()
        elif weekday == 4:
            msg = get_friday_message()
        else:
            return

        await channel.send(msg)

@tasks.loop(minutes=1)
async def send_friday_evening_message():
    now = datetime.datetime.now()
    if now.weekday() == 4 and now.hour == 20 and now.minute == 0:
        channel = bot.get_channel(CHANNEL_ID)
        msg = get_friday_evening_message()
        await channel.send(msg)

bot.run(TOKEN)
