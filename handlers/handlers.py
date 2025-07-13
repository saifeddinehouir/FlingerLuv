import os
from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, \
    InputFile
from telegram.ext import ContextTypes, ConversationHandler
from models.user import User

users_list = []

likes_list = []


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to Flinger! Use /register to create your profile.")


AGE, GENDER, LOOKING_FOR, BIO , PHOTO= range(5)

async def register_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🧑 How old are you?")
    return AGE

async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    age = update.message.text
    if not age.isdigit() or int(age) < 18:
        await update.message.reply_text("🚫 Please enter a valid age (18+).")
        return AGE
    context.user_data['age'] = int(age)
    await update.message.reply_text(
        "👤 What is your gender? (Male/Female/Other)",
        reply_markup=ReplyKeyboardMarkup([["Male", "Female", "Other"]], one_time_keyboard=True)
    )
    return GENDER

async def get_gender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['gender'] = update.message.text
    await update.message.reply_text(
        "💘 Who are you looking for? (Male/Female/Any)",
        reply_markup=ReplyKeyboardMarkup([["Male", "Female", "Any"]], one_time_keyboard=True)
    )
    return LOOKING_FOR

async def get_looking_for(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['looking_for'] = update.message.text
    await update.message.reply_text("📝 Write a short bio about yourself.", reply_markup=ReplyKeyboardRemove())
    return BIO

async def get_bio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['bio'] = update.message.text


    await update.message.reply_text("📸 Upload a photo", reply_markup=ReplyKeyboardRemove())

    return PHOTO

async def get_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📸 get_photo() called")

    if not update.message.photo:
        await update.message.reply_text("❌ That doesn't look like a photo. Please send a profile picture.")
        return PHOTO

    os.makedirs("photos", exist_ok=True)

    photo_file = await update.message.photo[-1].get_file()
    file_path = f'photos/{update.message.from_user.id}.jpg'
    await photo_file.download_to_drive(file_path)

    context.user_data['photo_path'] = file_path
    user = update.effective_user
    new_user = User(
        telegram_id=user.id,
        username=user.username,
        first_name=user.first_name,
        age=context.user_data['age'],
        gender=context.user_data['gender'],
        looking_for=context.user_data['looking_for'],
        bio=context.user_data['bio'],
        photo_url=file_path
    )
    users_list.append(new_user)
    print(users_list)
    await update.message.reply_text("📸 Photo received!")
    await update.message.reply_text("🎉 Ton profil est enregistré ! Tu peux maintenant découvrir d'autres profils avec /browse")

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Registration canceled.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id


    if len(users_list)!=0:
        user = users_list[0]
        photo = InputFile(open(user.photo_url, "rb"))

        profile_text = (
            f"👤 *Your Profile:*\n"
            f"Name: {user.first_name or 'N/A'}\n"
            f"Username: @{user.username or 'N/A'}\n"
            f"Age: {user.age}\n"
            f"Gender: {user.gender}\n"
            f"Looking For: {user.looking_for}\n"
            f"Bio: {user.bio or 'No bio yet.'}\n"
        )
        await update.message.reply_photo(photo=photo, caption=profile_text)
    else:
        await update.message.reply_text("❌ You haven't registered yet. Use /register to get started.")

async def browse_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user= update.effective_user

        profile = User(
            telegram_id=user.id,
            username=user.username,
            first_name=user.first_name,
            age=18,
            gender="Male",
            looking_for="Female",
            bio='bio',
            photo_url=None
        )
        if profile:
            # Sauvegarder l'ID du profil en cours
            context.user_data["current_profile_id"] = profile.telegram_id

            # Créer les boutons Like/Skip
            keyboard = [
                [
                    InlineKeyboardButton("👍 Like", callback_data="like"),
                    InlineKeyboardButton("👎 Skip", callback_data="skip")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            text = (
                f"👤 *{profile.first_name}*, {profile.age}\n"
                f"💬 {profile.bio or '_Aucune bio_'}"
            )

            await update.message.reply_text(
                text, reply_markup=reply_markup, parse_mode="Markdown"
            )

        else:
            await update.message.reply_text("😕 Il n’y a plus de profils à voir pour l’instant. Reviens plus tard !")





async def deactivate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user= update.effective_user
    users_list.remove(users_list[0])
    await update.message.reply_text("👋 Welcome to Flinger! Use /register to create your profile.")

def save_swipe(swiping_user_id, target_user_id, param):
    pass


async def show_next_profile(update, context):
    pass


def check_for_match(swiping_user_id, target_user_id):
    pass


async def like(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    swiping_user_id = query.from_user.id
    target_user_id = context.user_data.get("current_profile_id")

    # Save the "like" swipe
    save_swipe(swiping_user_id, target_user_id, "yes")

    # Check if it's a match
    if check_for_match(swiping_user_id, target_user_id):
        await query.edit_message_text("💥 It's a match! You both liked each other!")

    # Show next profile
    await show_next_profile(update, context)

async def skip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    swiping_user_id = query.from_user.id
    target_user_id = context.user_data.get("current_profile_id")

    # Save the "no" swipe
    save_swipe(swiping_user_id, target_user_id, "no")

    # Show next profile
    await show_next_profile(update, context)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🤖 *Available commands:*\n\n"
        "/start — Welcome message\n"
        "/register — Create your profile\n"
        "/browse — See and swipe profiles\n"
        "/profile — View your profile\n"
        "/matches — See your matches\n"
        "/edit — Edit your profile\n"
        "/help — Show this help message\n"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def edit_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return

async def matches():
    return
