import asyncio
import time
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = "8523746541:AAG3f4Y5EdpCV3Yy_mNxI5EufvTb6sjjjaU"

COOLDOWN = 30 * 60

last_ads = {}

AD_KEYWORDS = [
    "buy", "sell", "available", "price", "stock",
    "netflix", "spotify", "youtube", "prime",
    "vpn", "nord", "premium", "account",
    "subscription", "profile",
    "dm", "pm", "@", "http", "https",
    "₹", "rs", "inr", "$"
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ United Escrow Ads Bot Online"
    )


async def check_ads(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message:
        return

    text = (update.message.text or "").lower()

    is_ad = (
        any(word in text for word in AD_KEYWORDS)
        or len(text) > 120
        or text.count("\n") >= 3
        or update.message.photo
        or update.message.video
        or update.message.document
    )

    if not is_ad:
        return

    chat = update.effective_chat
    user = update.effective_user

    member = await context.bot.get_chat_member(chat.id, user.id)

    if member.status in ["administrator", "creator"]:
        return

    now = time.time()
    if user.id in last_ads:
        remaining = COOLDOWN - (now - last_ads[user.id])

        if remaining > 0:
            try:
                await update.message.delete()
            except:
                pass

            mins = int(remaining // 60)

            try:
                msg = await context.bot.send_message(
                    chat_id=chat.id,
                    text=f"⏳ {user.first_name}, please wait {mins} minute(s) before posting another advertisement."
                )

                await asyncio.sleep(10)
                await msg.delete()

            except:
                pass

            return

    last_ads[user.id] = now


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
    MessageHandler(
        filters.TEXT
        | filters.PHOTO
        | filters.VIDEO
        | filters.Document.ALL,
        check_ads,
    )
)

print("Bot Started...")
app.run_polling()