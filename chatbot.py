import os
import json
from dotenv import load_dotenv
from importlib import import_module

load_dotenv()

AI_ENGINE = json.loads(os.getenv("AI_ENGINE"))

# Load file settings from file
def load_settings():
    try:
        with open("settings.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"current_bot": "default"}  # Default bot on first boot

# Store file settings
def save_settings(settings):
    with open("settings.json", "w") as f:
        json.dump(settings, f)

settings = load_settings()
current_bot_name = settings["current_bot"]
current_bot = AI_ENGINE[current_bot_name]

# Dynamic chatbot loader
def load_bot(bot_name):
    if bot_name in AI_ENGINE:
        bot_info = AI_ENGINE[bot_name]
        bot_module = import_module(f"{bot_info['model']}_bot")
        return getattr(bot_module, f"{bot_info['model'].capitalize()}Bot")(
            api_key=os.getenv(f"{bot_info['model'].upper()}_API_KEY"),
            model_version=bot_info['version']
        )
    print("Invalid bot name.")
    return None

# Initialize the current bot
bot_instance = load_bot(current_bot_name)
last_user_input = None  # Stores the last question

while True:
    user_input = input("Me: ").strip()

    if user_input.lower() in ["@exit", "@quit", "@q"]:
        print("Exiting...")
        break

    if user_input.startswith("@bot: "):  # Switch bot
        current_bot_name = user_input.split(": ")[1].strip()
        bot_instance = load_bot(current_bot_name)
        settings["current_bot"] = current_bot_name
        save_settings(settings)
        print(f"Switched to: {current_bot_name}")
        continue

    if user_input.startswith("@ask: "):  # Switch bot & ask last question
        bot_name = user_input.split(": ")[1].strip()
        if last_user_input is None:
            print("No previous question to ask.")
            continue
        bot_instance = load_bot(bot_name)
        user_input = last_user_input  # Use the last question for the new bot

    if user_input.startswith("@relay: "):  # Get answer from current bot & ask another bot
        bot_name = user_input.split(": ")[1].strip()
        if bot_name not in AI_ENGINE:
            print("Invalid bot name.")
            continue

        if last_user_input is None:
            print("No previous question to relay.")
            continue

        # Get answer from the current bot
        response_1 = bot_instance.get_response(last_user_input)

        # Ask another bot using the first bot's response
        second_bot = load_bot(bot_name)
        response_2 = second_bot.get_response(f"{last_user_input} (first bot said: {response_1})")

        print(f"-+--------------------------------------------------------+-")
        print(f"{current_bot_name.capitalize()}: {response_1}")
        print(f"{bot_name.capitalize()}: {response_2}")
        print(f"-+--------------------------------------------------------+-")
        continue

    last_user_input = user_input  # Store the last question
    response = bot_instance.get_response(user_input)

    print(f"-+--------------------------------------------------------+-")
    print(f"{current_bot_name.capitalize()}: {response}")
    print(f"-+--------------------------------------------------------+-")
