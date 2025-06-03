from flask import Flask, jsonify, send_from_directory, request
import os
import requests
import time
import difflib
from flask_cors import CORS

# Configuration
static_path = os.getenv('STATIC_PATH', 'static')
template_path = os.getenv('TEMPLATE_PATH', 'templates')

IGDB_CLIENT_ID = "6i9cms08h0gktanme8jlx3rvwj5wni"
IGDB_CLIENT_SECRET = "omkrpeuw9a6wp11z9jq1f4mo445ams"
IGDB_BASE_URL = "https://api.igdb.com/v4"

# App setup
app = Flask(__name__, static_folder=static_path, template_folder=template_path)
CORS(app)

# Token management
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

def score_match(game_name, search_term):
    """Score how well a game matches the search term"""
    game_lower = game_name.lower()
    search_lower = search_term.lower()
    
    # Exact match
    if game_lower == search_lower:
        return 1000
    
    # Starts with search
    if game_lower.startswith(search_lower):
        return 900
    
    # Word starts with search
    words = game_lower.split()
    for word in words:
        if word.startswith(search_lower):
            return 700
    
    # Multi-word matching
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
    
    # Contains search
    if search_lower in game_lower:
        return 300
    
    # Fuzzy match
    similarity = difflib.SequenceMatcher(None, search_lower, game_lower).ratio()
    if similarity > 0.7:
        return int(similarity * 200)
    
    # Partial word match
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
fields name, first_release_date;
where category = 0;
limit 50;'''
    
    games = igdb_request('games', direct_query)
    if games:
        all_games.extend(games)
    
    # Search individual words
    words = [w for w in search_term.lower().split() if len(w) >= 3]
    for word in words:
        word_query = f'''search "{word}";
fields name, first_release_date;
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
            
            scored_games.append({
                'game': {
                    'id': game['id'],
                    'name': game['name'],
                    'release_year': release_year
                },
                'score': score
            })
    
    # Return top results
    scored_games.sort(key=lambda x: x['score'], reverse=True)
    return [item['game'] for item in scored_games[:limit]]

def get_game_info(game_id):
    """Get detailed game information"""
    query = f'''fields name, first_release_date, genres.name, involved_companies.company.name, involved_companies.developer, involved_companies.publisher, platforms.name;where id = {game_id};'''
    
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
    
    return {
        'id': game['id'],
        'name': game['name'],
        'release_year': release_year,
        'genres': genres,
        'developers': developers,
        'publishers': publishers,
        'platforms': platforms
    }

# Routes
@app.route('/api/health')
def health_check():
    return jsonify({"status": "healthy", "message": "backend service is running"})

@app.route('/api/key')
def get_key():
    return jsonify({'apiKey': os.getenv('NYT_API_KEY')})

@app.route('/')
@app.route('/<path:path>')
def serve_frontend(path=''):
    if path and os.path.exists(os.path.join(static_path, path)):
        return send_from_directory(static_path, path)
    return send_from_directory(template_path, 'index.html')

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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)
