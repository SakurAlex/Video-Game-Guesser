<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import type { GameGuess } from './types';
  import gameCover from "./assets/default_game.svg";

  export let isVisible = false;
  export let correctGame: GameGuess | null = null;
  export let isWin = false;
  export let attempts = 0;

  const dispatch = createEventDispatcher();

  function close() {
    isVisible = false;
    dispatch('close');
  }

  function handleOverlayClick(event: MouseEvent) {
    if (event.target === event.currentTarget) {
      close();
    }
  }

  function handleKeydown(event: KeyboardEvent) {
    if (event.key === 'Escape') {
      close();
    }
  }
</script>

{#if isVisible}
  <div class="result-overlay" on:click={handleOverlayClick} on:keydown={handleKeydown}>
    <div class="result-content">
      <div class="result-header">
        <h2>{isWin ? '🎉 Congratulations! You won!' : 'Game Over...'}</h2>
        <button class="close-button" on:click={close}>&times;</button>
      </div>

      <div class="result-body">
        {#if correctGame}
          <div class="game-info">
            <div class="cover-container">
              {#if correctGame.cover_url}
                <img src={correctGame.cover_url} alt="game cover" class="game-cover"/>
              {:else}
                <img src={gameCover} alt="cover" class="suggestion-cover" />
              {/if}
            </div>

            <div class="game-details">
              <h3>The correct answer is:</h3>
              <p class="game-name">{correctGame.gameName}</p>
              
              <div class="detail-row">
                <span class="label">Release Year:</span>
                <span class="value">{correctGame.releaseYear}</span>
              </div>

              <div class="detail-row">
                <span class="label">Genre:</span>
                <span class="value">{correctGame.genres.join(', ')}</span>
              </div>

              <div class="detail-row">
                <span class="label">Developer:</span>
                <span class="value">{correctGame.developers.join(', ')}</span>
              </div>

              <div class="detail-row">
                <span class="label">Publisher:</span>
                <span class="value">{correctGame.publishers.join(', ')}</span>
              </div>

              <div class="detail-row">
                <span class="label">Platform:</span>
                <span class="value">{correctGame.platforms.join(', ')}</span>
              </div>
            </div>
          </div>

          <div class="stats">
            <p class="attempts">Time taken: {attempts} attempts</p>
          </div>
        {/if}
      </div>

      <div class="result-footer">
        <button class="play-again-button" on:click={() => dispatch('restart')}>
          {isWin ? 'Play Again' : 'Try Again'}
        </button>
      </div>
    </div>
  </div>
{/if}

<style>
  .result-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }

  .result-content {
    background: white;
    border-radius: 16px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    max-width: 800px;
    width: 90%;
    max-height: 90vh;
    display: flex;
    flex-direction: column;
    animation: slideIn 0.3s ease;
  }

  @keyframes slideIn {
    from {
      opacity: 0;
      transform: translateY(-20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .result-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 24px;
    border-bottom: 1px solid #e5e5e5;
  }

  .result-header h2 {
    margin: 0;
    font-size: 24px;
    color: #2c3e50;
  }

  .close-button {
    background: none;
    border: none;
    font-size: 32px;
    color: #9ca3ab;
    cursor: pointer;
    padding: 0;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: background-color 0.2s ease;
  }

  .close-button:hover {
    background-color: #f5f5f5;
  }

  .result-body {
    padding: 24px;
    overflow-y: auto;
  }

  .game-info {
    display: flex;
    gap: 24px;
    margin-bottom: 24px;
  }

  .cover-container {
    width: 200px;
    height: 240px;
    border-radius: 8px;
    overflow: hidden;
    background: #f5f5f5;
  }

  .game-cover {
    width: 100%;
    height: 100%;
    object-fit: cover;
    background-color: #b5b5b5;
  }

  .no-cover {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 48px;
  }

  .game-details {
    flex-grow: 1;
  }

  .game-details h3 {
    margin: 0 0 12px 0;
    color: #666;
    font-size: 18px;
  }

  .game-name {
    font-size: 28px;
    font-weight: 700;
    color: #2c3e50;
    margin: 0 0 24px 0;
  }

  .detail-row {
    margin-bottom: 12px;
  }

  .label {
    color: #666;
    font-weight: 500;
    margin-right: 8px;
  }

  .value {
    color: #2c3e50;
  }

  .stats {
    text-align: center;
    padding: 16px;
    background: #f8f9fa;
    border-radius: 8px;
    margin-top: 24px;
  }

  .attempts {
    font-size: 18px;
    color: #2c3e50;
    margin: 0;
  }

  .result-footer {
    padding: 20px 24px;
    border-top: 1px solid #e5e5e5;
    display: flex;
    justify-content: center;
  }

  .play-again-button {
    background: #75ad79;
    color: white;
    border: none;
    padding: 12px 32px;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.2s ease;
  }

  .play-again-button:hover {
    background: #218838;
  }

  @media (max-width: 768px) {
    .result-content {
      width: 95%;
      max-height: 95vh;
    }

    .game-info {
      flex-direction: column;
    }

    .cover-container {
      width: 100%;
      height: 200px;
    }

    .game-name {
      font-size: 24px;
    }
  }
</style> 