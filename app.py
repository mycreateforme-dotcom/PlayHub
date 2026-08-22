from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os

app = FastAPI(title="PlayHub API")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = "games_db.json"
ADMIN_USER = "Keshav"
ADMIN_PASS = "QWERTYUIOPASDFGHJKLZXCVBNM"

INITIAL_GAMES = [
    {"id": "game_chess_adapt", "title": "Chess Adapt", "url": "https://mycreateforme-dotcom.github.io/Chess-Adapt-/", "icon": "♟️", "plays": 0},
    {"id": "game_cfm", "title": "HYPERSPACE 3D", "url": "https://mycreateforme-dotcom.github.io/GameCFM/", "icon": "🚀", "plays": 0},
    {"id": "game_cress", "title": "Cress", "url": "https://mycreateforme-dotcom.github.io/cress/", "icon": "⚔️", "plays": 0},
    {"id": "game_stell_titans", "title": "Stell Titans 3D", "url": "https://mycreateforme-dotcom.github.io/Stell-Titans-3D/", "icon": "🤖", "plays": 0},
    {"id": "game_hand_gesture_slicer", "title": "Hand Gesture Slicer", "url": "https://mycreateforme-dotcom.github.io/Hand-Gesture-Slicer/", "icon": "🖐️", "plays": 0},
    {"id": "game_neuro_clash", "title": "Neuro Clash", "url": "https://mycreateforme-dotcom.github.io/Nuero-Clash/", "icon": "⚡", "plays": 0},
    {"id": "game_cyber_pong", "title": "Cyber Pong Overdrive", "url": "https://mycreateforme-dotcom.github.io/CYBER-PONG-OVERDRIVE/", "icon": "🏓", "plays": 0},
    {"id": "game_cyber_force_3d", "title": "Cyber Force 3D", "url": "https://mycreateforme-dotcom.github.io/CYBER-FORCE3D/", "icon": "💥", "plays": 0},
    {"id": "game_cyber_glide", "title": "Cyber Glide", "url": "https://mycreateforme-dotcom.github.io/CYBER-GLIDE/", "icon": "🏄", "plays": 0},
    {"id": "game_space_conquest", "title": "Space Conquest", "url": "https://mycreateforme-dotcom.github.io/Space-Conquest/", "icon": "🪐", "plays": 0}
]

# --- Pydantic Models ---
class LoginRequest(BaseModel):
    username: str
    password: str

class GameCreateRequest(BaseModel):
    title: str
    url: str
    icon: str
    plays: int = 0

class GameUpdatePlaysRequest(BaseModel):
    plays: int

# --- Helper Functions ---
def load_games():
    if not os.path.exists(DB_FILE):
        save_games(INITIAL_GAMES)
        return INITIAL_GAMES
    try:
        with open(DB_FILE, "r") as f:
            data = json.load(f)
            if not isinstance(data, list) or len(data) == 0:
                save_games(INITIAL_GAMES)
                return INITIAL_GAMES
            return data
    except Exception:
        save_games(INITIAL_GAMES)
        return INITIAL_GAMES

def save_games(games_list):
    with open(DB_FILE, "w") as f:
        json.dump(games_list, f, indent=2)

# --- Routes ---
@app.get("/api/games")
def get_games():
    return load_games()

@app.post("/api/login")
def login(creds: LoginRequest):
    if creds.username == ADMIN_USER and creds.password == ADMIN_PASS:
        return {"success": True, "token": "session-active-keshav"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

@app.post("/api/games/{game_id}/play")
def play_game(game_id: str):
    games = load_games()
    for g in games:
        if g["id"] == game_id:
            g["plays"] = g.get("plays", 0) + 1
            save_games(games)
            return {"success": True, "plays": g["plays"]}
    raise HTTPException(status_code=404, detail="Game not found")

@app.post("/api/games")
def add_game(game_data: GameCreateRequest):
    games = load_games()
    new_entry = {
        "id": f"game_{len(games)}_{abs(hash(game_data.title)) % 10000}",
        "title": game_data.title,
        "url": game_data.url,
        "icon": game_data.icon,
        "plays": int(game_data.plays)
    }
    games.insert(0, new_entry)
    save_games(games)
    return new_entry

@app.put("/api/games/{game_id}/plays")
def update_game_plays(game_id: str, body: GameUpdatePlaysRequest):
    games = load_games()
    for g in games:
        if g["id"] == game_id:
            g["plays"] = body.plays
            save_games(games)
            return {"success": True, "game": g}
    raise HTTPException(status_code=404, detail="Game not found")

@app.delete("/api/games/{game_id}")
def delete_game(game_id: str):
    games = load_games()
    updated = [g for g in games if g["id"] != game_id]
    save_games(updated)
    return {"success": True}

@app.post("/api/games/reset")
def reset_games():
    save_games(INITIAL_GAMES)
    return {"success": True, "games": INITIAL_GAMES}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
