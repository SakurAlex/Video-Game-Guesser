<script lang="ts">
  import NavigationBar from './NavigationBar.svelte';
  import SearchBar from './SearchBar.svelte';
  import GameStatus from './GameStatus.svelte';
  import GameTable from './GameTable.svelte';
  import type { GameGuess } from './types';

  let remainingAttempts = 10;
  let guesses: GameGuess[] = [];
  let healthStatus = "checking...";
  let loading = true;
  let error = null;

  async function checkBackendHealth() {
    try {
      const response = await fetch('/api/health');
      const data = await response.json();
      healthStatus = data.message;
      return true;
    } catch (err) {
      healthStatus = "backend service is not running";
      return false;
    }
  }

</script>

<main>
  <div class="nav-position">
    <NavigationBar />
  </div>
  
  <div class="content">
    <SearchBar />
    <GameStatus {remainingAttempts} />
    <GameTable {guesses} />
  </div>
</main>


<style>
  main {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    width: 100%;
  }

  .nav-position {
    display: flex;
    justify-content: flex-end;
  }

  .content {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    padding-top: 120px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 32px;
  }
</style>
