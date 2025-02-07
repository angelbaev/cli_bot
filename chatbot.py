import os
import json
from dotenv import load_dotenv
from importlib import import_module

load_dotenv()

AI_ENGINE = json.loads(os.getenv("AI_ENGINE"));

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

# Dinamic chat bot loader
bot_module = import_module(f"{current_bot['model']}_bot")
print(f"{current_bot['model'].capitalize()}Bot")
bot_instance = getattr(bot_module, f"{current_bot['model'].capitalize()}Bot")( # init bot
    api_key=os.getenv(f"{current_bot['model'].upper()}_API_KEY"),
    model_version=current_bot['version']
)

while True:
    user_input = input("Me: ")
    if user_input.lower() in ["@exit", "@quit", "@q"]:
        break		
    if user_input.startswith("@bot: "):
        bot_name = user_input.split(": ")[1].strip()
        if bot_name in AI_ENGINE:
            settings["current_bot"] = bot_name
            save_settings(settings)
            current_bot_name = bot_name
            current_bot = AI_ENGINE[current_bot_name]

            # Preload bot
            bot_module = import_module(f"{current_bot['model']}_bot")
            bot_instance = getattr(bot_module, f"{current_bot['model'].capitalize()}Bot")(
                api_key=os.getenv(f"{current_bot['model'].upper()}_API_KEY"),
                model_version=current_bot['version']
            )
            print(f"Bot changed to: {bot_name}")
        else:
            print("Invalid bot name.")
        continue

    response = bot_instance.get_response(user_input) # bot func
    print(f"-+--------------------------------------------------------+-")
    print(f"{current_bot_name.capitalize()}: {response}")
    print(f"-+--------------------------------------------------------+-")
