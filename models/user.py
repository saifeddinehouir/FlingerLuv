class User:
    def __init__(self, telegram_id, first_name, username, age,gender, looking_for, bio=None,photo_url=None):
        self.telegram_id = telegram_id
        self.first_name = first_name
        self.username = username
        self.age = age
        self.gender = gender
        self.looking_for = looking_for
        self.bio = bio
        self.photo_url = photo_url

