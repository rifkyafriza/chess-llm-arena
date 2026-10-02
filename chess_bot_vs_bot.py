import chess
import chess.svg
import json
import urllib.request
import webbrowser
import os
import time
import random

def llm_move(board, model_name):
    url = "http://localhost:20128/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_API_KEY_HERE"
    }
    legal = [m.uci() for m in board.legal_moves]
    prompt = f"FEN: {board.fen()}\nLegal: {legal}\nReply EXACTLY with ONE UCI move from list. No extra text."
    
    data = json.dumps({
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0,
        "stream": False
    }).encode("utf-8")
    
    req = urllib.request.Request(url, data=data, headers=headers)
    
    print("\n" + "="*40)
    print(f"[DEBUG] MODEL: {model_name}")
    print(f"[DEBUG] PROMPT:\n{prompt}")
    print("="*40)
    
    with urllib.request.urlopen(req) as res:
        raw_res = res.read()
        print(f"[DEBUG] RAW RESP:\n{raw_res.decode('utf-8')}")
        print("="*40)
        body = json.loads(raw_res)
        return body["choices"][0]["message"]["content"].strip()

def render_gui(board):
    html = f"""
    <html>
    <head>
        <meta http-equiv="refresh" content="2">
        <style>
            body {{ display:flex; flex-direction:column; justify-content:center; align-items:center; background:#222; color:#fff; font-family:sans-serif; height:100vh; margin:0; }}
            .player {{ font-size: 24px; font-weight: bold; margin: 15px; padding: 10px 20px; background: #444; border-radius: 8px; }}
        </style>
    </head>
    <body>
        <div class="player">Black: {model_black}</div>
        {chess.svg.board(board, size=500)}
        <div class="player">White: {model_white}</div>
    </body>
    </html>
    """
    with open("ui_bot_vs_bot.html", "w") as f:
        f.write(html)

board = chess.Board()
model_white = "model-white"
model_black = "model-black"

render_gui(board)
webbrowser.open("file://" + os.path.realpath("ui_bot_vs_bot.html"))

while not board.is_game_over():
    if board.turn == chess.WHITE:
        print(f"\nWhite ({model_white}) is thinking...")
        model = model_white
    else:
        print(f"\nBlack ({model_black}) is thinking...")
        model = model_black
        
    try:
        uci = llm_move(board, model)
        print(f"Move: {uci}")
        
        move = chess.Move.from_uci(uci)
        if move in board.legal_moves:
            board.push(move)
            render_gui(board)
        else:
            print("Illegal move. Forcing random move to prevent freeze.")
            board.push(random.choice(list(board.legal_moves)))
            render_gui(board)
            
    except Exception as e:
        print(f"Error: {e}. Forcing random move.")
        board.push(random.choice(list(board.legal_moves)))
        render_gui(board)
        time.sleep(1)

print("\nGame Over:", board.result())
