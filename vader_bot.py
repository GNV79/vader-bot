import discord
import os
import random
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
client.run(TOKEN)

# İzinler
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Bot tanımı
client = discord.Client(intents=intents)

# Mod değişkenleri
chat_mode = False
gobi_mode = False
user_tracker = set()  # İlk mesajını atanları takip için

# === EVENT: BOT AÇILDI ===
@client.event
async def on_ready():
    print(f'{client.user} karanlık tarafa hizmete hazır.')

# === EVENT: SUNUCUYA YENİ ÜYE ===
@client.event
async def on_member_join(member):
    try:
        await member.send("""
🛡️ **Welcome to Vader Bot.**
You are now under the surveillance of the Empire.

📜 Here’s what you’re allowed to say:

🇹🇷 **Türkçe Komutlar:**
- güç, selam, çay, padme
- takımlar: fenerbahçe, galatasaray, vs.
- !chatmode → sohbet
- !gobi → alternatif Sith evreni

🇬🇧 **English Triggers:**
- force, love, cake, fuck, money
- !chatmode / !exit
- !gobi / !exitgobi

💀 Say the wrong thing and you may regret it.
""")
    except:
        print(f"DM failed: {member.name}")

# === GOBI MODU ===
def gobi_mode_reply(message):
    content = message.content.lower()
    if "usta" in content or "master" in content:
        return "Speak clearly, Gobi. I cannot train a mumbling fool."

    gobi_lines = [
        "Focus, Gobi. Your mind wanders like a lost protocol droid.",
        "Anger is good, Gobi. Use it. Channel it.",
        "Your hesitation disappoints me, Gobi.",
        "Conquer. Destroy. Serve the Empire, Gobi.",
        "The power you seek is already within you, Gobi. But you're too soft to use it.",
        "I did not raise a coward, Gobi.",
        "From this moment, you are Sith. Act like it.",
        "Even a Sith Lord needs tea sometimes. Brew it strong, Gobi.",
        "Silence is wisdom, but you're just quiet because you're clueless.",
        "Say something useful, Gobi... or say nothing at all."
    ]
    return random.choice(gobi_lines)

# === CHAT MODU ===
def vader_auto_reply(user_message):
    msg = user_message.lower()
    if "how" in msg:
        return "With power. Always with power."
    elif "you" in msg and "are" in msg:
        return "I am not your friend. I am your fate."
    elif "i feel" in msg:
        return "Feelings are for the weak. Let go."
    else:
        return random.choice([
            "Your words mean nothing to the Empire.",
            "Careful. Your tone borders on treason.",
            "You wish to question me? Brave... and foolish.",
            "Speak with purpose, not weakness.",
            "You waste time. I deal in results.",
            "I have no time for this... nonsense.",
            "I find your lack of logic disturbing.",
            "You talk too much. That is dangerous.",
            "Impressive... but irrelevant.",
            "That sounds... foolish.",
            "Explain. Or be destroyed."
        ])

# === ANA MESAJ EVENTİ ===
@client.event
async def on_message(message):
    global chat_mode, gobi_mode

    if message.author == client.user:
        return

    # İlk mesajı atan kullanıcıya komut önerisi
    if message.author.id not in user_tracker:
        user_tracker.add(message.author.id)
        await message.channel.send(f"Welcome, {message.author.display_name}. Type `!help` to see what Vader tolerates.")

    # Küfür filtresi (herkese açık)
    kufurler = ["orospu", "piç", "yarrak", "amk", "sik", "anan", "aq", "göt", "yarak", "yarram", "amık"]
    if any(k in message.content.lower() for k in kufurler):
        await message.delete()
        try:
            await message.author.send("Vader sees everything. Watch your mouth, youngling.")
        except discord.Forbidden:
            await message.channel.send("I tried to warn you privately, but your DMs are closed.")
        return

    # === Komutlar ===
    if message.content.lower().startswith("!help"):
        await message.channel.send("""
📜 **VADER BOT KOMUT LİSTESİ**

🇹🇷 Türkçe:
- güç, selam, çay, padme, takımlar (fenerbahçe, galatasaray, vs)
- !chatmode → Sohbet modu
- !gobi → Alternatif evren (Gobi çırağın olur)
- !exit → Chat mode kapatır
- !exitgobi → Gobi modunu kapatır

🇬🇧 English:
- force, dark side, love, cake, etc.
- vader reacts sarcastically and violently.
""")
        return

    elif message.content.lower().startswith("!chatmode"):
        chat_mode = True
        await message.channel.send("Chat mode activated. Speak... but choose your words wisely.")
        return

    elif message.content.lower().startswith("!exit"):
        chat_mode = False
        await message.channel.send("Chat mode deactivated. Back to command structure.")
        return

    elif message.content.lower().startswith("!gobi"):
        gobi_mode = True
        await message.channel.send("🌀 Alternate Reality Engaged. From now on, you are Gobi.")
        return

    elif message.content.lower().startswith("!exitgobi"):
        gobi_mode = False
        await message.channel.send("Reality restored. Gobi has fallen. The Empire continues.")
        return

    # === GOBI MODU AKTİF ===
    if gobi_mode:
        reply = gobi_mode_reply(message)
        await message.channel.send(reply)
        return

    # === CHAT MODU AKTİF ===
    if chat_mode:
        reply = vader_auto_reply(message.content)
        await message.channel.send(reply)
        return

    # === VADER'IN SABİT CEVAPLARI ===
    content = message.content.lower()

    kelime_cevap = {
        "mal": "Sensin mal.",
        "bayram": "Para istemeye mi geldin pezevenk?",
        "obiwan": "Eskileri açma şimdi hiç.",
        "obi-wan": "Ona allah yardım etsin.",
        "yoda": "Pis buruşuk yeşil bok."
    }
    for kelime in kelime_cevap:
        if kelime in content:
            await message.channel.send(kelime_cevap[kelime])
            return

    english_answer = {
        "fuck": "I will not endure this disobedience.",
        "money": "I ain't rich, rebel scum!",
        "dooku": "Old fool. He was never the master.",
        "mace windu": "He was powerful... but still a fool.",
        "ahsoka": "The apprentice still lives. She will fall.",
        "kenobi": "You should not have come back.",
        "hope": "Hope is a dangerous delusion.",
        "cake": "Cake is overrated. Have you ever tried my own homemade tiramisu?",
        "love": "Love is weakness. Try darkside.",
        "father": "I am your father. Never forget it."
    }
    for word in english_answer:
        if word in content:
            await message.channel.send(english_answer[word])
            return

    if "çay" in content:
        await message.channel.send("Çay severim. Rize'de yeni bir Death Star inşa ediliyor: Death Çay.")
    elif "padme" in content:
        await message.channel.send("Eskileri açma şimdi hiç.")
    elif "selam" in content:
        await message.channel.send("Selam yavrum.")
    elif "güç" in content:
        await message.channel.send("Güç karanlık tarafta güçlüdür.")
    elif "fenerbahçe" in content:
        await message.channel.send("Şinanay diye geziyordunuz, girdi size şinanay.")
    elif "barcelona" in content:
        await message.channel.send("Messi gitti, ben geldim. Neyin havası bu?")
    elif "bayern" in content:
        await message.channel.send("Alman disiplini mi? Gel Sith çıraklığına.")
    elif "kenobi" in content:
        await message.channel.send("You should not have come back.")
    elif "rebellion" in content:
        await message.channel.send("You rebel scum!")
    elif "şakşuka" in content:
        await message.channel.send("Olsa da yesem. Tarık Mengüç benim arkadaşım, inanmıyor musun?")
    elif "fear" in content:
        await message.channel.send("Fear will keep them in line.")
    elif "dark side" in content:
        await message.channel.send("Give yourself to the dark side.")

# === ÇALIŞTIR ===
client.run(TOKEN)
