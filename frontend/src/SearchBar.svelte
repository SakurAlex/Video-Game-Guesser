<script lang="ts">
  import searchIcon from './assets/search.svg';
  let searchQuery = "";
</script>

<div class="search-container">
  <input
    type="text"
    bind:value={searchQuery}
    placeholder="Search for the game you want to guess..."
    class="search-input"
  />
  <button class="search-button" aria-label="Search">
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
    border-radius: 10px;
    border: 1.2px solid #CCCCCC;
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
    border-radius: 16px;
    padding: 0;
    border: none;
  }

  .search-button img {
    width: 24px;
    height: 24px;
  }

</style>
