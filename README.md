# AI Chess Arena: LLM vs LLM

A Python script to pit two LLMs (Large Language Models) against each other in a game of chess. The script uses the `python-chess` library for game logic and sends the board state in FEN format to the LLM API.

## Features
- LLM vs LLM match (White vs Black).
- Automatic move validation. If an LLM hallucinates (proposes an illegal move), the script automatically forces a random legal move to prevent the game from freezing.
- Auto-refreshing Browser UI (displays the chess board and the competing models).

![UI Preview](ui_preview.png)
- Debug log mode to monitor the exact prompt and JSON response from the models.

## Requirements
- Python 3
- `pip install chess`
- A running local LLM endpoint compatible with the OpenAI API format (default URL: `http://localhost:20128/v1/chat/completions`)

## Configuration
Open `chess_bot_vs_bot.py` and modify:
- `YOUR_API_KEY_HERE`: Replace with your actual LLM API key.
- `model_white`: Set to the model name playing White.
- `model_black`: Set to the model name playing Black.

## How to Run
```bash
python3 chess_bot_vs_bot.py
```