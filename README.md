# CLI Bot

A simple CLI bot that allows you to configure multiple chat bots and switch between them via the console.

## Features

- Supports multiple chat bots
- Dynamically loads bot modules
- Saves the last used bot
- Switch bots using commands

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/angelbaev/cli_bot.git
   cd cli-bot
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Create a `.env` file and configure your API keys:
   ```ini
   AI_ENGINE={"default": {"model": "gpt", "version": "4.0"}}
   GPT_API_KEY=your-api-key-here
   ```

## Usage

Run the bot:

```sh
python chatbot.py
```

### Commands

- `@exit`, `@quit`, `@q` → Exit the bot
- `@bot: <bot_name>` → Switch to another bot

## Configuration

- `settings.json` stores the last used bot.
- `AI_ENGINE` in `.env` defines available bots.

## Example

```
Me: Hello!
GPT: Hi there! How can I assist you today?
Me: @bot: assistant
Bot changed to: assistant
Me: What's the weather like?
Assistant: I can check that for you!
```

## License

MIT
