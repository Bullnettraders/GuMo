import discord
from discord.ext import tasks, commands
import datetime
import os
import random

# ENV-Variablen von Railway
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# === Sprüche ===
montag_sprueche = [
    "Geld verdienen ist ein Nebenprodukt von Werterschaffung. – Tobias Knoof",
    "Erfolg ist nicht endgültig, Misserfolg ist nicht fatal; was zählt, ist der Mut weiterzumachen. – Winston Churchill",
    "Der Markt kann länger irrational bleiben, als du solvent bleiben kannst. – John Maynard Keynes",
    "Die Wirtschaft ist zu wichtig, um sie allein den Ökonomen zu überlassen. – Unbekannt",
    "Reich wird man erst durch Dinge, die man nicht begehrt. – Mahatma Gandhi",
    # ... (weiter auffüllbar)
]

mittwoch_sprueche = [
    "Erfolg hat drei Buchstaben: TUN. – Goethe",
    "Es wird nicht leichter. Du wirst besser.",
    "Je steiniger der Weg, desto wertvoller das Ziel.",
    "Die Kunst ist, einmal mehr aufzustehen, als man umgeworfen wird. – Churchill",
    "Sei jeden Tag stärker als deine stärkste Ausrede.",
    # ... (weiter auffüllbar)
]

freitag_sprueche = [
    "Nur noch ein bisschen! Du hast dir das Wochenende verdient.",
    "Freitag – der schönste Tag der Woche!",
    "Fast geschafft! Ein schöner Tag wartet auf dich.",
]

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
        weekday = now.weekday()  # Montag=0 ... Freitag=4

        if weekday == 0:
            msg = f"Guten Morgen! {random.choice(montag_sprueche)}"
        elif weekday == 1:
            msg = "Guten Morgen!"
        elif weekday == 2:
            msg = f"Guten Morgen! {random.choice(mittwoch_sprueche)}"
        elif weekday == 3:
            msg = "Guten Morgen!"
        elif weekday == 4:
            msg = f"Guten Morgen! {random.choice(freitag_sprueche)}"
        else:
            return

        await channel.send(msg)

@tasks.loop(minutes=1)
async def send_friday_evening_message():
    now = datetime.datetime.now()
    if now.weekday() == 4 and now.hour == 20 and now.minute == 0:
        channel = bot.get_channel(CHANNEL_ID)
        await channel.send("Schönes Wochenende! Erhol dich gut 😊")

bot.run(TOKEN)
