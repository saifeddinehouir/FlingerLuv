import json
from handlers.handlers import users_list  # Import the actual list

def save_users_to_file(filename="users.json"):
    with open(filename, "w") as f:
        json.dump(users_list, f)

def load_users_from_file(filename="users.json"):
    try:
        with open(filename, "r") as f:
            loaded_users = json.load(f)
            users_list.clear()
            users_list.extend(loaded_users)
    except FileNotFoundError:
        pass  # No file yet, keep users_list as empty