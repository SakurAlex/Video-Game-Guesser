<script lang="ts">
  import searchIcon from "./assets/search.svg";
  import { createEventDispatcher } from 'svelte';

  let searchQuery = "";
  let suggestions: any[] = [];
  let selectedIndex = -1;
  let isLoading = false;
  let error: string | null = null;
  let selectedGame: any = null;
  let showSuggestions = false;
  let searchTimeout: NodeJS.Timeout | null = null;
  let suggestionsContainer: HTMLElement;

  const API_BASE_URL = "http://localhost:8000/api";
  const dispatch = createEventDispatcher();

  $: hasContent = searchQuery.trim().length > 0;

  function handleSearch(query: string) {
    if (searchTimeout) {
      clearTimeout(searchTimeout);
    }
    if (!query.trim()) {
      suggestions = [];
      showSuggestions = false;
      error = null;
      return;
    }
    searchTimeout = setTimeout(async () => {
      await searchGames(query);
    }, 300);
  }

  async function searchGames(query: string) {
    isLoading = true;
    error = null;
    try {
      const response = await fetch(`${API_BASE_URL}/games/search?q=${encodeURIComponent(query)}&limit=10`);
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      const data = await response.json();
      suggestions = data.results || [];
      showSuggestions = suggestions.length > 0;
      selectedIndex = -1;
    } catch (err: any) {
      error = `Search failed: ${err.message}. Make sure your Flask backend is running on port 8000.`;
      suggestions = [];
      showSuggestions = false;
    } finally {
      isLoading = false;
    }
  }

  async function selectGame(game: any) {
    selectedGame = null;
    searchQuery = ""; 
    suggestions = [];
    showSuggestions = false;
    selectedIndex = -1;

    try {
      const response = await fetch(`${API_BASE_URL}/games/${game.id}`);
      if (!response.ok) throw new Error(`Failed to fetch game details: ${response.status}`);
      const gameDetails = await response.json();
      selectedGame = gameDetails;

      if (selectedGame) {
        dispatch('gameGuessed', {
          gameName: selectedGame.name,
          releaseYear: selectedGame.release_year,
          genres: selectedGame.genres,
          developers: selectedGame.developers,
          publishers: selectedGame.publishers,
          platforms: selectedGame.platforms
        });
      }
    } catch (err: any) {
      error = `Failed to load game details: ${err.message}`;
    }
  }

  function handleKeydown(event: KeyboardEvent) {
    if (!showSuggestions || suggestions.length === 0) return;
    switch (event.key) {
      case "ArrowDown":
        event.preventDefault();
        selectedIndex = Math.min(selectedIndex + 1, suggestions.length - 1);
        break;
      case "ArrowUp":
        event.preventDefault();
        selectedIndex = Math.max(selectedIndex - 1, -1);
        break;
      case "Enter":
        event.preventDefault();
        if (selectedIndex >= 0 && selectedIndex < suggestions.length) {
          selectGame(suggestions[selectedIndex]);
        }
        break;
      case "Escape":
        suggestions = [];
        showSuggestions = false;
        selectedIndex = -1;
        break;
    }
  }

  function handleInput() {
    selectedGame = null;
    handleSearch(searchQuery);
  }

  function handleFocus() {
    if (suggestions.length > 0 && searchQuery.trim()) {
      showSuggestions = true;
    }
  }

  function handleBlur() {
    setTimeout(() => {
      showSuggestions = false;
      selectedIndex = -1;
    }, 200);
  }

  function handleSuggestionClick(game: any) {
    selectGame(game);
  }
</script>


<div class="search-container">
  <div class="input-wrapper">
    <input
      type="text"
      bind:value={searchQuery}
      on:input={handleInput}
      on:keydown={handleKeydown}
      on:focus={handleFocus}
      on:blur={handleBlur}
      placeholder="Search for the game you want to guess..."
      class="search-input"
      autocomplete="off"
    />

    {#if showSuggestions && (suggestions.length > 0 || isLoading || error)}
      <div class="suggestions" bind:this={suggestionsContainer}>
        {#if isLoading}
          <div class="loading">
            <div class="loading-spinner"></div>
            Searching...
          </div>
        {:else if error}
          <div class="error">{error}</div>
        {:else if suggestions.length === 0 && searchQuery.trim()}
          <div class="no-results">No games found for "{searchQuery}"</div>
        {:else}
          {#each suggestions as game, index}
            <div
              class="suggestion {index === selectedIndex ? 'selected' : ''}"
              on:click={() => handleSuggestionClick(game)}
            >
              <div class="suggestion-icon">{game.name.charAt(0)}</div>
              <div class="suggestion-content">
                <div class="suggestion-name">{game.name}</div>
                {#if game.release_year}
                  <div class="suggestion-year">{game.release_year}</div>
                {/if}
              </div>
            </div>
          {/each}
        {/if}
      </div>
    {/if}
  </div>

  <button class="search-button" class:active={hasContent}>
    <img src={searchIcon} alt="Search" />
  </button>
</div>

<!-- {#if selectedGame}
  <div class="game-details">
    <h3>Selected Game: {selectedGame.name}</h3>
    <div class="game-info">
      {#if selectedGame.release_year}
        <p><strong>Release Year:</strong> {selectedGame.release_year}</p>
      {/if}
      {#if selectedGame.genres && selectedGame.genres.length > 0}
        <p><strong>Genres:</strong> {selectedGame.genres.join(', ')}</p>
      {/if}
      {#if selectedGame.developers && selectedGame.developers.length > 0}
        <p><strong>Developers:</strong> {selectedGame.developers.join(', ')}</p>
      {/if}
      {#if selectedGame.publishers && selectedGame.publishers.length > 0}
        <p><strong>Publishers:</strong> {selectedGame.publishers.join(', ')}</p>
      {/if}
      {#if selectedGame.platforms && selectedGame.platforms.length > 0}
        <p><strong>Platforms:</strong> {selectedGame.platforms.join(', ')}</p>
      {/if}
    </div>
  </div>
{/if} -->

<style>
  .search-container {
    display: flex;
    align-items: center;
    gap: 11px;
    height: 48px;
    position: relative;
  }

  .input-wrapper {
    position: relative;
    width: 540px;
  }

  .search-input {
    width: 100%;
    height: 48px;
    padding: 0 16px;
    font-family: Inter;
    font-size: 18px;
    font-weight: 600;
    color: #000000;
    background-color: white;
    box-shadow: -4px 4px 4px 0px rgba(0, 0, 0, 0.15);
    border-radius: 15px;
    border: none;
    outline: none;
  }

  .search-input::placeholder {
    color: #b3b5bd;
    opacity: 1;
  }

  .search-input:focus {
    box-shadow:
      -4px 4px 4px 0px rgba(0, 0, 0, 0.15),
      0 0 0 2px rgba(185, 219, 243, 0.5);
  }

  .search-button {
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #b3b5bd;
    box-shadow: -4px 4px 4px 0px rgba(0, 0, 0, 0.15);
    border-radius: 16px;
    padding: 0;
    border: none;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  .search-button.active {
    background-color: #b9dbf3;
  }

  .search-button:hover {
    opacity: 0.9;
  }

  .search-button img {
    width: 24px;
    height: 24px;
  }

  /* Suggestions dropdown styles */
  .suggestions {
    position: absolute;
    top: calc(100% + 8px);
    left: 0;
    right: 0;
    background: white;
    border-radius: 15px;
    box-shadow: -4px 4px 12px rgba(0, 0, 0, 0.25);
    max-height: 400px;
    overflow-y: auto;
    z-index: 1000;
    border: 1px solid #e1e5e9;
  }

  .suggestion {
    padding: 12px 16px;
    cursor: pointer;
    border-bottom: 1px solid #f1f3f4;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    font-family: Inter;
  }

  .suggestion:last-child {
    border-bottom: none;
  }

  .suggestion:hover {
    background: #f8f9fa;
  }

  .suggestion.selected {
    background: #b9dbf3;
    color: #333;
  }

  .suggestion-icon {
    margin-right: 12px;
    width: 32px;
    height: 32px;
    background: #b9dbf3;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #333;
    font-size: 14px;
    font-weight: bold;
    flex-shrink: 0;
  }

  .suggestion.selected .suggestion-icon {
    background: rgba(255, 255, 255, 0.8);
  }

  .suggestion-content {
    display: flex;
    flex-direction: column;
    min-width: 0;
  }

  .suggestion-name {
    font-size: 16px;
    font-weight: 500;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .suggestion-year {
    font-size: 14px;
    font-weight: 400;
    color: #666;
    margin-top: 2px;
  }

  .no-results {
    padding: 16px;
    text-align: center;
    color: #666;
    font-style: italic;
    font-family: Inter;
  }

  .loading {
    padding: 16px;
    text-align: center;
    color: #b9dbf3;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: Inter;
  }

  .loading-spinner {
    width: 20px;
    height: 20px;
    border: 2px solid #e1e5e9;
    border-top: 2px solid #b9dbf3;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-right: 8px;
  }

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }

  .error {
    padding: 16px;
    background: #fee;
    color: #c33;
    text-align: center;
    border-radius: 8px;
    margin: 8px;
    font-family: Inter;
    font-size: 14px;
  }

  /* Game details styles */
  .game-details {
    margin-top: 20px;
    padding: 20px;
    background: white;
    border-radius: 15px;
    box-shadow: -4px 4px 4px 0px rgba(0, 0, 0, 0.15);
  }

  .game-details h3 {
    font-family: Inter;
    font-size: 20px;
    font-weight: 600;
    margin: 0 0 15px 0;
    color: #333;
  }

  .game-info p {
    font-family: Inter;
    font-size: 14px;
    margin: 8px 0;
    color: #555;
  }

  .game-info strong {
    color: #333;
  }
</style>
