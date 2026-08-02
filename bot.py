import os
import telebot
import yt_dlp

TOKEN = "8802385569:AAHeY5DiNttswZL4hbkJDxTCH8eWYzgdciw"
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
  bot.reply_to(
      message,
      "أهلاً بك! أرسل لي رابط فيديو من تيك توك أو انستجرام وسأقوم بتحميله"
      " لك.",
  )


@bot.message_handler(
    func=lambda message: "tiktok.com" in message.text
    or "instagram.com" in message.text
)
def download_video(message):
  url = message.text
  sent_msg = bot.reply_to(message, "جاري المعالجة والتحميل، أرجو الانتظار...")

  output_template = "video.mp4"

  ydl_opts = {
      "outtmpl": output_template,
      "format": "best",
      "quiet": True,
  }

  try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      ydl.download([url])

    with open(output_template, "rb") as video:
      bot.send_video(message.chat.id, video, caption="تم التحميل بواسطة البوت")

    bot.delete_message(message.chat.id, sent_msg.message_id)

    if os.path.exists(output_template):
      os.remove(output_template)

  except Exception as e:
    bot.edit_message_text(
        f"حدث خطأ أثناء التحميل: {str(e)}",
        message.chat.id,
        sent_msg.message_id,
    )
    if os.path.exists(output_template):
      os.remove(output_template)


if __name__ == "__main__":
  print("البوت يعمل الآن...")
  bot.infinity_polling()
