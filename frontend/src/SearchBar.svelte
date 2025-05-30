<script lang="ts">
  import searchIcon from "./assets/search.svg";

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

  // Reactive statement to check if input has content
  $: hasContent = searchQuery.trim().length > 0;

  // Debounced search function
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
    }, 300); // 300ms delay
  }

  async function searchGames(query: string) {
    if (!query.trim()) return;

    isLoading = true;
    error = null;

    try {
      const response = await fetch(
        `${API_BASE_URL}/games/search?q=${encodeURIComponent(query)}&limit=10`,
      );
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
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

  function selectGame(game: any) {
    selectedGame = game;
    searchQuery = game.name;
    suggestions = [];
    showSuggestions = false;
    selectedIndex = -1;
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
    // Small delay to allow suggestion clicks to register
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
              {game.name}
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
    font-size: 16px;
    font-weight: 500;
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
  }

  .suggestion.selected .suggestion-icon {
    background: rgba(255, 255, 255, 0.8);
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
</style>
