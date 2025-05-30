from flask import Flask, jsonify, send_from_directory, request
import os
from flask_cors import CORS

static_path = os.getenv('STATIC_PATH','static')
template_path = os.getenv('TEMPLATE_PATH','templates')

app = Flask(__name__, static_folder=static_path, template_folder=template_path)
CORS(app)

@app.route('/api/health')
def health_check():
    return jsonify({"status": "healthy", "message": "backend service is running"})

@app.route('/api/key')
def get_key():
    return jsonify({'apiKey': os.getenv('NYT_API_KEY')})

@app.route('/')
@app.route('/<path:path>')
def serve_frontend(path=''):
    if path != '' and os.path.exists(os.path.join(static_path,path)):
        return send_from_directory(static_path, path)
    return send_from_directory(template_path, 'index.html')

games = [
    {"id": 1, "name": "The Legend of Zelda: Breath of the Wild"},
    {"id": 2, "name": "Super Mario Odyssey"},
    {"id": 3, "name": "Minecraft"},
    {"id": 4, "name": "Grand Theft Auto V"},
    {"id": 5, "name": "Call of Duty: Modern Warfare"},
    {"id": 6, "name": "Fortnite"},
    {"id": 7, "name": "Among Us"},
    {"id": 8, "name": "Cyberpunk 2077"},
    {"id": 9, "name": "Red Dead Redemption 2"},
    {"id": 10, "name": "The Witcher 3: Wild Hunt"},
    {"id": 11, "name": "Valorant"},
    {"id": 12, "name": "League of Legends"},
    {"id": 13, "name": "Counter-Strike 2"},
    {"id": 14, "name": "Apex Legends"},
    {"id": 15, "name": "Overwatch 2"},
    {"id": 16, "name": "Elden Ring"},
    {"id": 17, "name": "God of War"},
    {"id": 18, "name": "Spider-Man: Miles Morales"},
    {"id": 19, "name": "Horizon Zero Dawn"},
    {"id": 20, "name": "Fall Guys"},
    {"id": 21, "name": "Mario Kart 8 Deluxe"},
    {"id": 22, "name": "Mario Party Superstars"},
    {"id": 23, "name": "Super Mario Bros. Wonder"}
]

def search_games(query, limit=10):
    """Simple search function with scoring"""
    if not query or not query.strip():
        return []
    
    search_term = query.lower().strip()
    scored_games = []
    
    for game in games:
        game_name = game["name"].lower()
        score = 0
        
        # Exact match gets highest score
        if game_name == search_term:
            score = 1000
        # Starts with query gets high score
        elif game_name.startswith(search_term):
            score = 100
        # Contains query gets medium score
        elif search_term in game_name and len(search_term) > 3:
            score = 50
        # Word boundary matches get bonus points
        else:
            words = game_name.split()
            for word in words:
                if word.startswith(search_term):
                    score = 75
                    break
        
        # Boost score for shorter names (more relevant)
        if score > 0:
            score += max(0, 50 - len(game["name"]))
            scored_games.append({"game": game, "score": score})
    
    # Sort by score (descending) and return top results
    scored_games.sort(key=lambda x: x["score"], reverse=True)
    return [item["game"] for item in scored_games[:limit]]

@app.route('/api/games/search', methods=['GET'])
def search_games_endpoint():
    """GET endpoint for game search autocomplete"""
    try:
        query = request.args.get('q', '').strip()
        limit = int(request.args.get('limit', 10))
        
        # Validate limit (between 1 and 20)
        limit = max(1, min(limit, 20))
        
        if not query:
            return jsonify({
                'error': 'Query parameter "q" is required'
            }), 400
        
        results = search_games(query, limit)
        
        return jsonify({
            'query': query,
            'results': results,
            'count': len(results)
        })
        
    except ValueError:
        return jsonify({'error': 'Invalid limit parameter'}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)
