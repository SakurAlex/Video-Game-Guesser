<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import userCover from "./assets/default_user.svg";
  export let isVisible = false;
  export let user = null;
  export let stats = null;

  let loading = false;
  let error = '';

  const dispatch = createEventDispatcher();
  const API_BASE_URL = "http://localhost:8000/api";

  async function logout() {
    loading = true;
    error = '';

    try {
      const response = await fetch(`${API_BASE_URL}/auth/logout`, {
        method: 'POST',
        credentials: 'include',
      });

      if (response.ok) {
        dispatch('logout');
        close();
      } else {
        error = 'Logout failed';
      }
    } catch (err) {
      error = 'Network error';
      console.error('Logout error:', err);
    } finally {
      loading = false;
    }
  }

  function close() {
    isVisible = false;
    error = '';
    dispatch('close');
  }

  function handleOverlayClick(event) {
    if (event.target === event.currentTarget) {
      close();
    }
  }

  function handleKeydown(event) {
    if (event.key === 'Escape') {
      close();
    }
  }

  function getWinRateColor(winRate) {
    if (winRate >= 70) return '#4caf50'; // Green
    if (winRate >= 50) return '#ff9800'; // Orange
    return '#f44336'; // Red
  }

  function getAverageAttempts() {
    if (!stats || stats.total_games === 0) return 'N/A';
    return (stats.total_attempts / stats.total_games).toFixed(1);
  }
</script>

{#if isVisible}
  <div class="overlay" on:click={handleOverlayClick} on:keydown={handleKeydown}>
    <div class="profile-modal">
      <div class="profile-header">
        <h2>User Profile</h2>
        <button class="close-button" on:click={close}>&times;</button>
      </div>

      <div class="profile-body">
        {#if user}
          <div class="user-info">
            <div class="user-image">
              <img src={userCover} alt="user-cover" class="user-cover" />
            </div>
            <div class="user-details">
              <h3>{user.username}</h3>
              <p class="email">{user.email}</p>
            </div>
          </div>

          {#if stats}
            <div class="stats-section">
              <h4>Game Statistics</h4>
              
              <div class="stats-grid">
                <div class="stat-card">
                  <div class="stat-number">{stats.total_games}</div>
                  <div class="stat-label">Total Games</div>
                </div>

                <div class="stat-card">
                  <div class="stat-number">{stats.games_won}</div>
                  <div class="stat-label">Games Won</div>
                </div>

                <div class="stat-card">
                  <div class="stat-number" style="color: {getWinRateColor(stats.win_rate)}">{stats.win_rate}%</div>
                  <div class="stat-label">Win Rate</div>
                </div>

                <div class="stat-card">
                  <div class="stat-number">{stats.best_attempts || 'N/A'}</div>
                  <div class="stat-label">Best Score</div>
                </div>

                <div class="stat-card">
                  <div class="stat-number">{getAverageAttempts()}</div>
                  <div class="stat-label">Avg. Attempts</div>
                </div>

                <div class="stat-card">
                  <div class="stat-number">{stats.total_attempts}</div>
                  <div class="stat-label">Total Attempts</div>
                </div>
              </div>

              {#if stats.total_games > 0}
                <div class="progress-section">
                  <div class="progress-bar">
                    <div class="progress-label">Win Rate Progress</div>
                    <div class="progress-container">
                      <div 
                        class="progress-fill" 
                        style="width: {stats.win_rate}%; background-color: {getWinRateColor(stats.win_rate)}"
                      ></div>
                    </div>
                    <div class="progress-text">{stats.games_won} / {stats.total_games} games won</div>
                  </div>
                </div>
              {:else}
                <div class="no-stats">
                  <p>🎮 Start playing to see your statistics!</p>
                </div>
              {/if}
            </div>
          {/if}

          {#if error}
            <div class="error-message">{error}</div>
          {/if}

          <div class="profile-actions">
            <button 
              class="logout-button" 
              on:click={logout}
              disabled={loading}
            >
              {#if loading}
                <div class="loading-spinner"></div>
                Logging out...
              {:else}
                Logout
              {/if}
            </button>
          </div>
        {:else}
          <div class="no-user">
            <p>No user information available</p>
          </div>
        {/if}
      </div>
    </div>
  </div>
{/if}

<style>
  .overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.6);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }

  .profile-modal {
    background: white;
    border-radius: 16px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    width: 100%;
    max-width: 600px;
    margin: 20px;
    max-height: 90vh;
    overflow-y: auto;
  }

  .profile-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 24px;
    border-bottom: 1px solid #e5e5e5;
  }

  .profile-header h2 {
    margin: 0;
    font-size: 24px;
    font-weight: 700;
    color: #2c3e50;
  }

  .close-button {
    background: none;
    border: none;
    font-size: 28px;
    color: #9ca3ab;
    cursor: pointer;
    padding: 0;
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: background-color 0.2s ease;
  }

  .close-button:hover {
    background-color: #f5f5f5;
  }

  .profile-body {
    padding: 24px;
  }

  .user-info {
    display: flex;
    align-items: center;
    margin-bottom: 30px;
    padding: 20px;
    background: #f8f9fa;
    border-radius: 12px;
  }

  .user-image {
    width: 64px;
    height: 64px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
    font-weight: bold;
    color: #2c3e50;
    margin-right: 20px;
  }

  .user-cover {
    width: 100%;
    height: 100%;
  }

  .user-details h3 {
    margin: 0 0 4px 0;
    font-size: 22px;
    font-weight: 600;
    color: #2c3e50;
  }

  .email {
    margin: 0;
    color: #666;
    font-size: 16px;
  }

  .stats-section h4 {
    margin: 0 0 20px 0;
    font-size: 20px;
    font-weight: 600;
    color: #2c3e50;
  }

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 16px;
    margin-bottom: 24px;
  }

  .stat-card {
    background: white;
    border: 2px solid #e1e5e9;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }

  .stat-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  .stat-number {
    font-size: 32px;
    font-weight: 700;
    color: #2c3e50;
    margin-bottom: 4px;
  }

  .stat-label {
    font-size: 14px;
    color: #666;
    font-weight: 500;
  }

  .progress-section {
    margin-top: 24px;
  }

  .progress-bar {
    background: #f8f9fa;
    border-radius: 12px;
    padding: 20px;
  }

  .progress-label {
    font-weight: 600;
    color: #2c3e50;
    margin-bottom: 12px;
  }

  .progress-container {
    background: #e1e5e9;
    border-radius: 8px;
    height: 12px;
    overflow: hidden;
    margin-bottom: 8px;
  }

  .progress-fill {
    height: 100%;
    border-radius: 8px;
    transition: width 0.3s ease;
  }

  .progress-text {
    font-size: 14px;
    color: #666;
    text-align: center;
  }

  .no-stats {
    text-align: center;
    padding: 40px 20px;
    color: #666;
  }

  .no-stats p {
    font-size: 18px;
    margin: 0;
  }

  .error-message {
    background-color: #fee;
    color: #c33;
    padding: 12px;
    border-radius: 8px;
    margin-bottom: 16px;
    font-size: 14px;
    border: 1px solid #fcc;
  }

  .profile-actions {
    margin-top: 24px;
    padding-top: 24px;
    border-top: 1px solid #e5e5e5;
  }

  .logout-button {
    background-color: #e9776e;
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
  }

  .logout-button:hover:not(:disabled) {
    background-color: #e46458;
  }

  .logout-button:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }

  .loading-spinner {
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top: 2px solid white;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  .no-user {
    text-align: center;
    padding: 40px 20px;
    color: #666;
  }

  @media (max-width: 640px) {
    .profile-modal {
      margin: 10px;
    }

    .profile-header,
    .profile-body {
      padding: 16px 20px;
    }

    .user-info {
      flex-direction: column;
      text-align: center;
    }

    .avatar {
      margin-right: 0;
      margin-bottom: 16px;
    }

    .stats-grid {
      grid-template-columns: repeat(2, 1fr);
      gap: 12px;
    }

    .stat-card {
      padding: 16px;
    }

    .stat-number {
      font-size: 24px;
    }
  }
</style>
