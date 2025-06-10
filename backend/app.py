from flask import Flask, jsonify, send_from_directory, request, session
from datetime import datetime 
import os
import requests
import time
import difflib
import random 
import hashlib
import sqlite3
from functools import wraps
from flask_cors import CORS

# Configuration
static_path = os.getenv('STATIC_PATH', 'static')
template_path = os.getenv('TEMPLATE_PATH', 'templates')

IGDB_CLIENT_ID = "6i9cms08h0gktanme8jlx3rvwj5wni"
IGDB_CLIENT_SECRET = "omkrpeuw9a6wp11z9jq1f4mo445ams"
IGDB_BASE_URL = "https://api.igdb.com/v4"

# App setup
app = Flask(__name__, static_folder=static_path, template_folder=template_path)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')
CORS(app, supports_credentials=True)

#Helper mappings from names to IGDB IDs
PLATFORM_NAME_TO_ID = {
    'PC': 6,
    'Mac': 2,
    'Linux': 3,
    'iOS': 39,
    'Android': 34,
    'PlayStation 1': 7,
    'PlayStation 2': 8,
    'PlayStation 3': 9,
    'PlayStation Portable (PSP)': 36,
    'PlayStation Vita': 167,
    'PlayStation 4': 48,
    'PlayStation 5': 187,
    'Xbox': 11,
    'Xbox 360': 12,
    'Xbox One': 49,
    'Xbox Series X': 169,
    'Nintendo Entertainment System (NES)': 18,
    'Super Nintendo (SNES)': 19,
    'Nintendo 64': 4,
    'GameCube': 21,
    'Wii': 5,
    'Wii U': 41,
    'Nintendo Switch': 130,
    'Game Boy': 33,
    'Game Boy Color': 43,
    'Game Boy Advance': 24,
    'Nintendo DS': 20,
    'Nintendo 3DS': 37,
    'Arcade': 28,
    'Dreamcast': 13
}

GENRE_NAME_TO_ID = {
    'Action': 4,
    'Adventure': 31,
    'Role-playing (RPG)': 12,
    'Shooter': 5,
    'Platform': 8,
    'Puzzle': 9,
    'Racing': 10,
    'Sports': 14,
    'Strategy': 15,
    'Simulation': 13,
    'Fighting': 6,
    'Stealth': 20,
    'Survival': 23,
    'Sandbox': 24,
    'Pinball': 34,
    'Educational': 38,
    'Indie': 32,
    'Arcade': 33,
    'Family': 25,
    'Music': 18
}

def map_platform_names_to_ids(names):
    """Turn platform names into IGDB platform IDs."""
    return [PLATFORM_NAME_TO_ID[n] for n in names if n in PLATFORM_NAME_TO_ID]

def map_genre_names_to_ids(names):
    """Turn genre names into IGDB genre IDs."""
    return [GENRE_NAME_TO_ID[n] for n in names if n in GENRE_NAME_TO_ID]

# Database setup
def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect('game_guess.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # User stats table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_stats (
            user_id INTEGER PRIMARY KEY,
            total_games INTEGER DEFAULT 0,
            games_won INTEGER DEFAULT 0,
            total_attempts INTEGER DEFAULT 0,
            best_attempts INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

# Token management for IGDB API
access_token = None
token_expires_at = 0

def get_access_token():
    """Get or refresh Twitch access token for IGDB API"""
    global access_token, token_expires_at
    
    if access_token and time.time() < token_expires_at:
        return access_token
    
    data = {
        'client_id': IGDB_CLIENT_ID,
        'client_secret': IGDB_CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }
    
    try:
        response = requests.post("https://id.twitch.tv/oauth2/token", data=data)
        response.raise_for_status()
        token_data = response.json()
        
        access_token = token_data['access_token']
        token_expires_at = time.time() + token_data['expires_in'] - 60
        
        return access_token
    except Exception as e:
        print(f"Token error: {e}")
        return None

def igdb_request(endpoint, query):
    """Make request to IGDB API"""
    token = get_access_token()
    if not token:
        return None
    
    headers = {
        'Client-ID': IGDB_CLIENT_ID,
        'Authorization': f'Bearer {token}',
        'Content-Type': 'text/plain'
    }
    
    try:
        response = requests.post(f"{IGDB_BASE_URL}/{endpoint}", headers=headers, data=query)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"IGDB error: {e}")
        return None

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

def get_user_stats(user_id):
    """Get user statistics"""
    conn = sqlite3.connect('game_guess.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user_stats WHERE user_id = ?', (user_id,))
    stats = cursor.fetchone()
    conn.close()
    
    if not stats:
        return {
            'total_games': 0,
            'games_won': 0,
            'total_attempts': 0,
            'best_attempts': None,
            'win_rate': 0
        }
    
    return {
        'total_games': stats[1],
        'games_won': stats[2],
        'total_attempts': stats[3],
        'best_attempts': stats[4],
        'win_rate': round((stats[2] / stats[1] * 100) if stats[1] > 0 else 0, 1)
    }

def update_user_stats(user_id, won, attempts):
    """Update user statistics"""
    conn = sqlite3.connect('game_guess.db')
    cursor = conn.cursor()
    
    # Get current stats
    cursor.execute('SELECT * FROM user_stats WHERE user_id = ?', (user_id,))
    current = cursor.fetchone()
    
    if current:
        new_total_games = current[1] + 1
        new_games_won = current[2] + (1 if won else 0)
        new_total_attempts = current[3] + attempts
        new_best_attempts = min(current[4], attempts) if current[4] and won else (attempts if won else current[4])
        
        cursor.execute('''
            UPDATE user_stats 
            SET total_games = ?, games_won = ?, total_attempts = ?, best_attempts = ?
            WHERE user_id = ?
        ''', (new_total_games, new_games_won, new_total_attempts, new_best_attempts, user_id))
    else:
        cursor.execute('''
            INSERT INTO user_stats (user_id, total_games, games_won, total_attempts, best_attempts)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, 1, 1 if won else 0, attempts, attempts if won else None))
    
    conn.commit()
    conn.close()

# Game logic functions (existing)
def score_match(game_name, search_term):
    """Score how well a game matches the search term"""
    game_lower = game_name.lower()
    search_lower = search_term.lower()
    
    if game_lower == search_lower:
        return 1000
    
    if game_lower.startswith(search_lower):
        return 900
    
    words = game_lower.split()
    for word in words:
        if word.startswith(search_lower):
            return 700
    
    search_words = search_lower.split()
    if len(search_words) > 1:
        matches = 0
        for search_word in search_words:
            for game_word in words:
                if game_word.startswith(search_word):
                    matches += 1
                    break
                elif search_word in game_word:
                    matches += 0.5
                    break
        
        match_ratio = matches / len(search_words)
        if match_ratio >= 0.8:
            return 600
        elif match_ratio >= 0.6:
            return 400
    
    if search_lower in game_lower:
        return 300
    
    similarity = difflib.SequenceMatcher(None, search_lower, game_lower).ratio()
    if similarity > 0.7:
        return int(similarity * 200)
    
    for word in words:
        if search_lower in word:
            return 100
    
    return 0

def search_games(query, limit=20):
    """Search for games using multiple strategies"""
    if not query or len(query.strip()) < 2:
        return []
    
    search_term = query.strip()
    all_games = []
    
    # Direct search
    direct_query = f'''search "{search_term}";
fields name, first_release_date, cover.url;
where category = 0;
limit 50;'''
    
    games = igdb_request('games', direct_query)
    if games:
        all_games.extend(games)
    
    # Search individual words
    words = [w for w in search_term.lower().split() if len(w) >= 3]
    for word in words:
        word_query = f'''search "{word}";
fields name, first_release_date, cover.url;
where category = 0;
limit 30;'''
        
        games = igdb_request('games', word_query)
        if games:
            all_games.extend(games)
    
    unique_games = {game['id']: game for game in all_games}
    
    # Score and sort
    scored_games = []
    for game in unique_games.values():
        score = score_match(game['name'], search_term)
        if score > 0:
            release_year = None
            if game.get('first_release_date'):
                release_year = time.strftime('%Y', time.gmtime(game['first_release_date']))
            
            # Process cover URL
            cover_url = process_cover_url(game.get('cover'))
            
            scored_games.append({
                'game': {
                    'id': game['id'],
                    'name': game['name'],
                    'release_year': release_year,
                    'cover_url': cover_url
                },
                'score': score
            })
    
    scored_games.sort(key=lambda x: x['score'], reverse=True)
    return [item['game'] for item in scored_games[:limit]]

def process_cover_url(cover_data):
    """Process IGDB cover URL"""
    if not cover_data:
        return None
    
    if isinstance(cover_data, dict) and 'url' in cover_data:
        url = cover_data['url']
        
        # IGDB cover URL format: //images.igdb.com/igdb/image/upload/t_thumb/xxxxx.jpg
        if url.startswith('//'):
            return f"https:{url}"
        elif url.startswith('http'):
            return url
    
    return None

def get_game_info(game_id):
    """Get detailed game information"""
    query = f'''fields name, first_release_date, genres.name, involved_companies.company.name, involved_companies.developer, involved_companies.publisher, platforms.name, cover.url;where id = {game_id};'''
    
    games = igdb_request('games', query)
    if not games:
        return None
    
    game = games[0]
    
    # Extract data
    release_year = None
    if game.get('first_release_date'):
        release_year = time.strftime('%Y', time.gmtime(game['first_release_date']))
    
    genres = [g['name'] for g in game.get('genres', [])]
    
    developers = []
    publishers = []
    for company_info in game.get('involved_companies', []):
        company_name = company_info.get('company', {}).get('name', '')
        if company_name:
            if company_info.get('developer'):
                developers.append(company_name)
            if company_info.get('publisher'):
                publishers.append(company_name)
    
    platforms = [p['name'] for p in game.get('platforms', [])]
    
    # cover URL
    cover_url = process_cover_url(game.get('cover'))
    
    return {
        'id': game['id'],
        'name': game['name'],
        'release_year': release_year,
        'genres': genres,
        'developers': developers,
        'publishers': publishers,
        'platforms': platforms,
        'cover_url': cover_url
    }
# Auth Endpoints
@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    if not data or not all(k in data for k in ['username', 'email', 'password']):
        return jsonify({'error': 'Username, email, and password are required'}), 400
    
    username = data['username'].strip()
    email = data['email'].strip()
    password = data['password']
    
    # Basic length checks
    if len(username) < 3:
        return jsonify({'error': 'Username must be at least 3 characters long'}), 400
    
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters long'}), 400
    
    conn = sqlite3.connect('game_guess.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                      (username, email, hash_password(password)))
        user_id = cursor.lastrowid
        conn.commit()

        # Persist session so subsequent requests are authenticated
        session['user_id'] = user_id
        session['username'] = username
        
        return jsonify({
            'message': 'User registered successfully',
            'user': {'id': user_id, 'username': username, 'email': email}
        }), 201
        
    except sqlite3.IntegrityError as e:
        if 'username' in str(e):
            return jsonify({'error': 'Username already exists'}), 400
        elif 'email' in str(e):
            return jsonify({'error': 'Email already exists'}), 400
        else:
            return jsonify({'error': 'Registration failed'}), 400
    finally:
        conn.close()

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json()
    
    if not data or not all(k in data for k in ['username', 'password']):
        return jsonify({'error': 'Username and password are required'}), 400
    
    username = data['username'].strip()
    password = data['password']
    
    conn = sqlite3.connect('game_guess.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, email, password_hash FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    
    if not user or user[3] != hash_password(password):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    session['user_id'] = user[0]
    session['username'] = user[1]
    
    return jsonify({
        'message': 'Login successful',
        'user': {'id': user[0], 'username': user[1], 'email': user[2]}
    })

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """Logout user"""
    session.clear()
    return jsonify({'message': 'Logout successful'})

@app.route('/api/auth/me', methods=['GET'])
@require_auth
def get_current_user():
    """Get current user info"""
    user_id = session['user_id']
    
    conn = sqlite3.connect('game_guess.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, email FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    stats = get_user_stats(user_id)
    
    return jsonify({
        'user': {'id': user[0], 'username': user[1], 'email': user[2]},
        'stats': stats
    })

@app.route('/api/health')
def health_check():
    return jsonify({"status": "healthy", "message": "backend service is running"})



@app.route('/api/key')
def get_key():
    return jsonify({'apiKey': os.getenv('NYT_API_KEY')})

# Static Frontend Fallback
@app.route('/')
@app.route('/<path:path>')
def serve_frontend(path=''):
    if path and os.path.exists(os.path.join(static_path, path)):
        return send_from_directory(static_path, path)
    # Otherwise fall back to index.html so client‑side routing works
    return send_from_directory(template_path, 'index.html')

# Game Endpoints
@app.route('/api/games/search', methods=['GET'])
def search_endpoint():
    """Search for games"""
    try:
        query = request.args.get('q', '').strip()
        limit = max(1, min(int(request.args.get('limit', 10)), 20))
        
        if not query:
            return jsonify({'error': 'Query parameter "q" is required'}), 400
        
        results = search_games(query, limit)
        
        return jsonify({
            'query': query,
            'results': results,
            'count': len(results)
        })
        
    except ValueError:
        return jsonify({'error': 'Invalid limit parameter'}), 400
    except Exception as e:
        print(f"Search error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/games/<int:game_id>', methods=['GET'])
def game_details(game_id):
    """Get game details by ID"""
    try:
        game_info = get_game_info(game_id)
        
        if not game_info:
            return jsonify({'error': 'Game not found'}), 404
        
        return jsonify(game_info)
        
    except Exception as e:
        print(f"Game details error: {e}")
        return jsonify({'error': 'Internal server error'}), 500


#New filtered list endpoint
@app.route('/api/games', methods=['GET'])
def get_games():
    """Fetch games with optional year range / platform / genre / top-N filters"""
    year_start = request.args.get('yearStart', type=int)
    year_end   = request.args.get('yearEnd', type=int)
    platforms  = request.args.getlist('platforms')
    genres     = request.args.getlist('genres')
    top_tier   = request.args.get('topTier', type=int)

    # Build IGDB where clauses
    where_clauses = []
    if year_start or year_end:
        # Use provided range or set reasonable defaults
        start_year = year_start if year_start else 1970
        end_year = year_end if year_end else datetime.now().year
        
        start_timestamp = int(datetime(start_year, 1, 1).timestamp())
        end_timestamp = int(datetime(end_year, 12, 31, 23, 59, 59).timestamp())
        where_clauses.append(
            f"first_release_date >= {start_timestamp} & first_release_date <= {end_timestamp}"
        )

    # Only add platform filter if not all platforms are selected
    if platforms and len(platforms) < len(PLATFORM_NAME_TO_ID):
        ids = map_platform_names_to_ids(platforms)
        where_clauses.append(f"platforms = ({','.join(map(str, ids))})")

    # Only add genre filter if not all genres are selected
    if genres and len(genres) < len(GENRE_NAME_TO_ID):
        ids = map_genre_names_to_ids(genres)
        where_clauses.append(f"genres = ({','.join(map(str, ids))})")

    # Assemble the IGDB query
    query  = "fields name, first_release_date, genres.name, platforms.name, total_rating_count;"
    if where_clauses:
        query += " where " + " & ".join(where_clauses) + ";"
    query += " sort total_rating_count desc;"
    if top_tier:
        query += f" limit {top_tier};"

    # Execute and return
    games = igdb_request('games', query)
    return jsonify(games)


@app.route('/api/games/random', methods=['GET'])
def get_random_game():
    """Pick a random game within the current filters."""
    try:
        # 1) Read filters
        year_start = request.args.get('yearStart', type=int)
        year_end   = request.args.get('yearEnd', type=int)
        platforms  = request.args.getlist('platforms')
        genres     = request.args.getlist('genres')
        top_tier   = request.args.get('topTier', type=int)
        
        # Debug information: record API call
        print("🔔 /api/games/random endpoint called!")
        print(f"📝 Request filters - Year Range: {year_start} to {year_end}, Platforms: {len(platforms)}, Genres: {len(genres)}, TopTier: {top_tier}")
        print(f"📊 Total available - Platforms: {len(PLATFORM_NAME_TO_ID)}, Genres: {len(GENRE_NAME_TO_ID)}")
        print(f"🔍 Will filter? - Year Range: {year_start or year_end}, Platforms: {platforms and len(platforms) < len(PLATFORM_NAME_TO_ID)}, Genres: {genres and len(genres) < len(GENRE_NAME_TO_ID)}")

        # 2) Build WHERE clauses
        where_clauses = []
        if year_start or year_end:
            # Use provided range or set reasonable defaults
            start_year = year_start if year_start else 1970
            end_year = year_end if year_end else datetime.now().year
            
            start_timestamp = int(datetime(start_year, 1, 1).timestamp())
            end_timestamp = int(datetime(end_year, 12, 31, 23, 59, 59).timestamp())
            where_clauses.append(
                f"first_release_date >= {start_timestamp} & first_release_date <= {end_timestamp}"
            )
        
        # Only add platform filter if not all platforms are selected
        if platforms and len(platforms) < len(PLATFORM_NAME_TO_ID):
            ids = map_platform_names_to_ids(platforms)
            where_clauses.append(f"platforms = ({','.join(map(str,ids))})")
        
        # Only add genre filter if not all genres are selected  
        if genres and len(genres) < len(GENRE_NAME_TO_ID):
            ids = map_genre_names_to_ids(genres)
            where_clauses.append(f"genres = ({','.join(map(str,ids))})")

        # 3) Fetch filtered set (no hard limit here)
        query  = "fields id, name;"
        if where_clauses:
            query += " where " + " & ".join(where_clauses) + ";"
        
        sort_options = [
            "total_rating_count desc",
            "name asc", 
            "first_release_date desc",
            "total_rating desc"
        ]
        random_sort = random.choice(sort_options)
        query += f" sort {random_sort};"
        random_offset = random.randint(0, 300)
        query += f" limit 100; offset {random_offset};"

        filtered = igdb_request('games', query) or []
        if not filtered:
            return jsonify({'error': 'No games match those filters'}), 404

        # 4) Pick randomly and return full details
        choice   = random.choice(filtered)
        detailed = get_game_info(choice['id'])
        if not detailed:
            return jsonify({'error': 'Could not fetch game details'}), 500
        
        return jsonify(detailed)

    except Exception as e:
        print(f"Random game error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/game/win', methods=['POST'])
@require_auth
def record_win():
    """Record a game win"""
    data = request.get_json()
    attempts = data.get('attempts', 10)
    
    user_id = session['user_id']
    update_user_stats(user_id, True, attempts)
    
    return jsonify({'message': 'Win recorded successfully'})

@app.route('/api/game/loss', methods=['POST'])
@require_auth
def record_loss():
    """Record a game loss"""
    data = request.get_json()
    attempts = data.get('attempts', 10)
    
    user_id = session['user_id']
    update_user_stats(user_id, False, attempts)
    
    return jsonify({'message': 'Loss recorded successfully'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)
    
