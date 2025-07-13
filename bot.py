from telegram.ext import ApplicationBuilder, ConversationHandler, CommandHandler, MessageHandler, filters
from config import TOKEN
from handlers.handlers import register_start, get_age, get_gender, get_looking_for, get_bio, cancel, users_list, \
    profile_command, \
    browse_command, get_photo, deactivate_command, help_command, start_command


def main():
   app = ApplicationBuilder().token(TOKEN).build()
   register_conv = ConversationHandler(
       entry_points=[CommandHandler("register", register_start)],
       states={
          0: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
          1: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_gender)],
          2: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_looking_for)],
          3: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_bio)],
          4: [MessageHandler(filters.PHOTO, get_photo)],

       },
       fallbacks=[CommandHandler("cancel", cancel)],
   )
   app.add_handler(register_conv)
   app.add_handler(CommandHandler("start", start_command))
   app.add_handler(CommandHandler("profile", profile_command))
   app.add_handler(CommandHandler("browse", browse_command))
   app.add_handler(CommandHandler("deactivate", deactivate_command))
   app.add_handler(CommandHandler("help", help_command))

   app.run_polling()

   print(users_list)

if __name__ == "__main__":
    main()