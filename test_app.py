import pytest
import json
import time
import sqlite3
from flask import jsonify, session
import os
import difflib
import app as test_app


from app import (
    app, init_db, hash_password, get_access_token, igdb_request,
    map_platform_names_to_ids, map_genre_names_to_ids, process_cover_url,
    score_match, search_games, update_user_stats, get_user_stats, require_auth
)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret'
    with app.test_client() as client:
        with app.app_context():
            init_db()
            conn = sqlite3.connect('game_guess.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM users;')
            cursor.execute('DELETE FROM user_stats;')
            conn.commit()
            conn.close()
        yield client


def register_user(client, username=None, email=None, password='password_123'):
    if username is None:
        username = f'testuser_{int(time.time()*1000)}'
    if email is None:
        email = f'{username}@test.com'
    return client.post('/api/auth/register', json={
        'username': username,
        'email': email,
        'password': password
    })


def login_user(client, username, password='password_123'):
    return client.post('/api/auth/login', json={
        'username': username,
        'password': password
    })


def test_health_check(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    data_back = response.get_json()
    assert data_back['status'] == 'healthy'


def test_hash_password():
    assert hash_password('abc') == hash_password('abc')
    assert hash_password('abc') != hash_password('xyz')


def test_get_access_token_failure(monkeypatch):
    monkeypatch.setattr('requests.post', lambda *args, **kwargs: (_ for _ in ()).throw(Exception("fail")))
    test_app.access_token = None
    test_app.token_expires_at = 0
    assert get_access_token() is None


def test_get_access_token_cached(monkeypatch):
    test_app.access_token = 'cached_token'
    test_app.token_expires_at = time.time() + 1000
    assert get_access_token() == 'cached_token'


def test_get_access_token_print(monkeypatch, capsys):
    test_app.access_token = None
    test_app.token_expires_at = 0
    def mock_post(*args, **kwargs):
        raise Exception("simulat error")
    monkeypatch.setattr('requests.post', mock_post)
    token_ckeck = get_access_token()
    assert token_ckeck is None
    captured_check = capsys.readouterr()
    assert "Token error" in captured_check.out


def test_igdb_request_no_token(monkeypatch):
    monkeypatch.setattr('app.get_access_token', lambda: None)
    assert igdb_request('games', 'query') is None


def test_igdb_request_error(monkeypatch, capsys):
    def mock_post(*args, **kwargs):
        raise Exception("Simulated Error")
    monkeypatch.setattr('requests.post', mock_post)
    assert igdb_request('games', 'query') is None
    captured = capsys.readouterr()
    assert "Error" in captured.out


def test_map_platform_names_to_ids():
    assert map_platform_names_to_ids(['PC', 'Error']) == [6]
    assert map_platform_names_to_ids([]) == []


def test_map_genre_names_to_ids():
    assert map_genre_names_to_ids(['Action', 'Error']) == [4]
    assert map_genre_names_to_ids([]) == []


def test_process_cover_url_variants():
    assert process_cover_url({'url': '//images.igdb.com/test.jpg'}).startswith('https://')
    assert process_cover_url({'url': 'http://example.com/test.jpg'}) == 'http://example.com/test.jpg'
    assert process_cover_url(None) is None
    assert process_cover_url({}) is None


def test_score_match_variants():
    assert score_match('Halo', 'Halo') == 1000
    assert score_match('Halo Infinite', 'Infinite') >= 700
    assert score_match('Halo', 'lo') > 0
    assert score_match('Among Us', 'Among') >= 400
    assert score_match('GTA', 'G') >= 700
    assert score_match('Test Game', 'KK') == 0
    assert score_match('Super Mario Bros', 'bro') == 700
    assert score_match('Black Myth WuKong', 'black myth') >= 200 
    assert score_match('The Last of Us', 'las s') == 400
    assert score_match("Call of Duty", "Clal of Duty") > 140
    assert score_match("Call of Duty", "uty") == 300





def test_register_login(client):
    res = register_user(client)
    assert res.status_code == 201
    username = res.get_json()['user']['username']
    email = res.get_json()['user']['email']
    assert register_user(client, username=username, email=f"other_{email}").status_code == 400
    assert register_user(client, username=f"other_{username}", email=email).status_code == 400
    assert login_user(client, username=username).status_code == 200


def test_register_invalid_inputs(client):
    assert register_user(client, username='ab', password='password_123').status_code == 400


def test_login_wrong_password(client):
    username = register_user(client).get_json()['user']['username']
    assert client.post('/api/auth/login', json={'username': username, 'password': 'Error'}).status_code == 401


def test_logout(client):
    username = register_user(client).get_json()['user']['username']
    login_user(client, username=username)
    assert client.post('/api/auth/logout').status_code == 200


def test_logout_without_login(client):
    assert client.post('/api/auth/logout').status_code == 200


def test_require_auth_direct(monkeypatch):
    @require_auth
    def dummy():
        return jsonify({'message': 'ok'})

    # without session
    with app.test_request_context():
        session.clear()
        response, code = dummy()
        assert code == 401
        assert response.get_json()['error'] == 'Authentication required'

    # with session
    with app.test_request_context():
        session['user_id'] = 1
        result = dummy()
        assert hasattr(result, 'get_json')
        assert result.get_json()['message'] == 'ok'


def test_get_current_user(client):
    username = register_user(client).get_json()['user']['username']
    login_user(client, username=username)
    res = client.get('/api/auth/me')
    assert res.status_code == 200


def test_search_games_short(client):
    assert search_games('a') == []


def test_search_games_missing_q(client):
    res = client.get('/api/games/search')
    assert res.status_code == 400
    assert 'Query' in res.get_json()['error']


def test_search_games_invalid_limit(client):
    res = client.get('/api/games/search?q=test&limit=abc')
    assert res.status_code == 400
    assert 'Invalid' in res.get_json()['error']


def test_search_games_error(client, monkeypatch):
    monkeypatch.setattr('app.igdb_request', lambda e, q: (_ for _ in ()).throw(Exception("fail")))
    assert client.get('/api/games/search?q=test').status_code == 500


def test_search_games(client, monkeypatch):
    monkeypatch.setattr('app.igdb_request', lambda e, q: [{'id': 1, 'name': 'Test', 'first_release_date': 1609459200}])
    res = client.get('/api/games/search?q=test')
    assert res.status_code == 200


def test_game_details(client, monkeypatch):
    monkeypatch.setattr('app.igdb_request', lambda e, q: [{
        'id': 1, 'name': 'Test', 'first_release_date': 1609459200,
        'genres': [{'name': 'Action'}], 'platforms': [{'name': 'PC'}],
        'involved_companies': [{'company': {'name': 'Test Dev'}, 'developer': True, 'publisher': False}],
        'cover': {'url': '//images.igdb.com/test.jpg'}
    }])
    assert client.get('/api/games/1').status_code == 200


def test_game_details_error(client, monkeypatch):
    monkeypatch.setattr('app.igdb_request', lambda e, q: (_ for _ in ()).throw(Exception("fail")))
    assert client.get('/api/games/1').status_code == 500


def test_game_details_not_found(client, monkeypatch):
    monkeypatch.setattr('app.get_game_info', lambda id: None)
    res = client.get('/api/games/1')
    assert res.status_code == 404


def test_get_games_filters(client, monkeypatch):
    monkeypatch.setattr('app.igdb_request', lambda e, q: [])
    res = client.get('/api/games?yearStart=2000&yearEnd=2020&platforms=PC&genres=Action&topTier=5')
    assert res.status_code == 200


def test_random_game_all_paths(client, monkeypatch):
    monkeypatch.setattr('app.igdb_request', lambda e, q: [{'id': 1, 'name': 'Game'}])
    monkeypatch.setattr('app.get_game_info', lambda id: {'id': id, 'name': 'Game'})
    assert client.get('/api/games/random').status_code == 200
    monkeypatch.setattr('app.igdb_request', lambda e, q: [])
    assert client.get('/api/games/random').status_code == 404


def test_random_game_failed_details(client, monkeypatch):
    monkeypatch.setattr('app.igdb_request', lambda e, q: [{'id': 1, 'name': 'Game'}])
    monkeypatch.setattr('app.get_game_info', lambda id: None)
    res = client.get('/api/games/random')
    assert res.status_code == 500


def test_update_user_stats(client):
    user_id = register_user(client).get_json()['user']['id']
    update_user_stats(user_id, True, 5)
    stats = get_user_stats(user_id)
    assert stats['total_games'] == 1
    update_user_stats(user_id, True, 3)
    stats = get_user_stats(user_id)
    assert stats['best_attempts'] == 3


def test_record_win_loss(client):
    username = register_user(client).get_json()['user']['username']
    login_user(client, username=username)
    assert client.post('/api/game/win', json={'attempts': 2}).status_code == 200
    assert client.post('/api/game/loss', json={'attempts': 3}).status_code == 200

def test_api_key_route_with_and_without(monkeypatch, client):
    monkeypatch.setenv('NYT_API_KEY', 'dummy')
    res = client.get('/api/key')
    assert res.status_code == 200
    assert res.get_json()['apiKey'] == 'dummy'

    monkeypatch.delenv('NYT_API_KEY', raising=False)
    res = client.get('/api/key')
    assert res.status_code == 200
    assert res.get_json()['apiKey'] is None

def test_serve_frontend_file_exists(client, monkeypatch):
    monkeypatch.setattr(os.path, 'exists', lambda path: True)
    res = client.get('/existingfile.js')
    assert res.status_code in (200, 404)

def test_serve_frontend_file_not_exists(client, monkeypatch):
    monkeypatch.setattr(os.path, 'exists', lambda path: False)
    res = client.get('/nonexistentfile.js')
    assert res.status_code in (200, 404)

def test_process_cover_url_edge_case():
    assert process_cover_url('invalid_data') is None
    assert process_cover_url({'not_url': 'no_url_here'}) is None

def test_get_games_top_tier_invalid(client):
    res = client.get('/api/games?topTier=abc')
    assert res.status_code == 200

def test_record_win_no_json(client):
    username = register_user(client).get_json()['user']['username']
    login_user(client, username=username)
    res = client.post('/api/game/win', json={}) 
    assert res.status_code == 200

def test_record_win_attempts_zero(client):
    username = register_user(client).get_json()['user']['username']
    login_user(client, username=username)
    res = client.post('/api/game/win', json={'attempts': 0})
    assert res.status_code == 200

def test_register_password_too_short(client):
    res = register_user(client, username='validname', password='123')
    assert res.status_code == 400
    assert 'Password must be at least 6 characters' in res.get_json()['error']

def test_igdb_request_exception(monkeypatch, capsys):
    import app
    def mock_post(*args, **kwargs):
        raise requests.exceptions.RequestException("Test exception for IGDB request error coverage.")
    monkeypatch.setattr(app.requests, 'post', mock_post)
    result = app.igdb_request('games', 'query')
    assert result is None
    captured = capsys.readouterr()
    assert "error" in captured.out

def test_score_match_similarity_coverage():
    result = score_match("ABCDEF", "ABXDEF")
    expected_score = int(difflib.SequenceMatcher(None, "abxdef", "abcdef").ratio() * 200)
    assert result == expected_score

def test_score_match_word_contains_search():
    result = score_match("my super hero", "per")
    assert result == 300


   









