<script lang="ts">
  import searchIcon from './assets/search.svg';
  let searchQuery = "";

  //if the text input is not empty, the search button will be active (change to blue)
  $: hasContent = searchQuery.trim().length > 0;
</script>

<div class="search-container">
  <input
    type="text"
    bind:value={searchQuery}
    placeholder="Search for the game you want to guess..."
    class="search-input"
  />
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
  }

  .search-input {
    width: 540px;
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
    color: #B3B5BD;
    opacity: 1;
  }

  .search-button {
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #B3B5BD;
    box-shadow: -4px 4px 4px 0px rgba(0, 0, 0, 0.15);
    border-radius: 16px;
    padding: 0;
    border: none;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  .search-button.active {
    background-color: #B9DBF3;
  }
  
  .search-button:hover {
    opacity: 0.9;
  }

  .search-button img {
    width: 24px;
    height: 24px;
  }
</style>
