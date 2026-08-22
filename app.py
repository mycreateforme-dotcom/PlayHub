import streamlit as st
import streamlit.components.v1 as components
import json
import os

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="PlayHub - Online Games",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
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

# --- DATABASE HELPERS ---
def load_games():
    if not os.path.exists(DB_FILE):
        save_games(INITIAL_GAMES)
        return INITIAL_GAMES
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return INITIAL_GAMES

def save_games(games_list):
    with open(DB_FILE, "w") as f:
        json.dump(games_list, f, indent=2)

def increment_play(game_id):
    games = load_games()
    for g in games:
        if g["id"] == game_id:
            g["plays"] += 1
            break
    save_games(games)

# --- SESSION STATE INITIALIZATION ---
if "active_game" not in st.session_state:
    st.session_state.active_game = None
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

# --- SIDEBAR: AUTH & ADMIN TOOLS ---
with st.sidebar:
    st.title("🎮 PlayHub Menu")
    
    if not st.session_state.is_admin:
        st.subheader("Leader Admin Login")
        user_input = st.text_input("Username")
        pass_input = st.text_input("Password", type="password")
        if st.button("Log In", use_container_width=True):
            if user_input == ADMIN_USER and pass_input == ADMIN_PASS:
                st.session_state.is_admin = True
                st.success("Welcome Leader Admin Keshav!")
                st.rerun()
            else:
                st.error("Invalid credentials.")
    else:
        st.success("Logged in as **Leader Admin (Keshav)**")
        if st.button("Log Out", use_container_width=True):
            st.session_state.is_admin = False
            st.rerun()
            
        st.markdown("---")
        st.subheader("➕ Add New Game")
        new_title = st.text_input("Game Title")
        new_url = st.text_input("Game URL (https://...)")
        new_icon = st.selectbox("Icon", ["🎮", "🚀", "⚔️", "🤖", "⚡", "🏓", "💥", "🏄", "🪐", "♟️"])
        new_plays = st.number_input("Initial Plays", min_value=0, value=0, step=10)
        
        if st.button("Publish Game", use_container_width=True):
            if new_title and new_url:
                games = load_games()
                new_entry = {
                    "id": f"game_{len(games)}_{int(os.times()[4])}",
                    "title": new_title,
                    "url": new_url,
                    "icon": new_icon,
                    "plays": int(new_plays)
                }
                games.insert(0, new_entry)
                save_games(games)
                st.success(f"Added {new_title}!")
                st.rerun()
            else:
                st.warning("Please fill in both Title and URL.")

# --- MAIN DASHBOARD ---
games = load_games()
total_global_plays = sum(g.get("plays", 0) for g in games)

col_title, col_stat = st.columns([3, 1])
with col_title:
    st.title("🎮 PlayHub")
    st.caption("Click any game below to play directly in your browser without logging in.")
with col_stat:
    st.metric("Total Global Plays", f"{total_global_plays:,}")

st.markdown("---")

# --- GAME PLAYER OVERLAY ---
if st.session_state.active_game:
    active = next((g for g in games if g["id"] == st.session_state.active_game), None)
    if active:
        col_header, col_btn1, col_btn2 = st.columns([4, 1, 1])
        with col_header:
            st.subheader(f"Playing: {active['icon']} {active['title']}")
        with col_btn1:
            st.link_button("⤢ Open in Full Tab", active["url"], use_container_width=True)
        with col_btn2:
            if st.button("✕ Close Game", use_container_width=True):
                st.session_state.active_game = None
                st.rerun()

        components.iframe(active["url"], height=700, scrolling=True)
        st.markdown("---")

# --- GAME CATALOG GRID ---
cols_per_row = 4
for i in range(0, len(games), cols_per_row):
    row_games = games[i : i + cols_per_row]
    cols = st.columns(cols_per_row)
    
    for idx, game in enumerate(row_games):
        with cols[idx]:
            with st.container(border=True):
                st.markdown(f"<h1 style='text-align: center; margin: 0;'>{game.get('icon', '🎮')}</h1>", unsafe_allow_html=True)
                st.markdown(f"<h4 style='text-align: center; margin: 0.2rem 0;'>{game['title']}</h4>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center; color: gray; font-size: 0.85rem;'>{game.get('plays', 0):,} plays</p>", unsafe_allow_html=True)
                
                if st.button(f"▶ Play", key=f"play_{game['id']}", use_container_width=True):
                    increment_play(game["id"])
                    st.session_state.active_game = game["id"]
                    st.rerun()
                
                # Admin controls per card
                if st.session_state.is_admin:
                    with st.expander("⚙️ Admin Controls"):
                        new_count = st.number_input("Override Plays", min_value=0, value=game["plays"], key=f"edit_{game['id']}")
                        if st.button("Save Plays", key=f"save_{game['id']}"):
                            current_games = load_games()
                            for g in current_games:
                                if g["id"] == game["id"]:
                                    g["plays"] = int(new_count)
                                    break
                            save_games(current_games)
                            st.rerun()
                        
                        if st.button("🗑️ Delete Game", key=f"del_{game['id']}", type="primary"):
                            current_games = [g for g in load_games() if g["id"] != game["id"]]
                            save_games(current_games)
                            if st.session_state.active_game == game["id"]:
                                st.session_state.active_game = None
                            st.rerun()
