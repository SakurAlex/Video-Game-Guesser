<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import startSearch from './assets/start_search.png';
  import startSelect from './assets/start_select.png';
  import profile from './assets/profile.png';
  import register from './assets/register.png';
  export let user: { username: string } | null = null;
  export let show = false;

  const dispatch = createEventDispatcher();

  function close() {
    dispatch('close');
  }

  function handleOverlayClick(event: MouseEvent) {
    if (event.target === event.currentTarget) {
      close();
    }
  }
</script>

{#if show}
  <div class="tutorials-overlay" on:click={handleOverlayClick}>
    <div class="tutorials-content">
      <h2 class="main-title">How to use GameGuesser</h2>
      <div class="cards-container">
        <div class="tutorial-card">
          <div class="card-header">
            <h3>How to start</h3>
          </div>
          <div class="card-body">
            <p>This is a small game to guess the game!</p>
            <p>You have 10 chances (default) to guess the correct game.</p>
            <p>Input the name of the game you want to guess in the search bar.</p>
            <img src={startSearch} alt="start -search" />
            <p>Click the blue search button to make a guess, check the hint information to adjust your next guess.</p>
            <img src={startSelect} alt="start -select" />
            <p>If you guess the correct game, you will win!</p>
          </div>
        </div>

        <div class="tutorial-card">
          <div class="card-header">
            <h3>{user ? 'Your Profile' : 'Create Account'}</h3>
          </div>
          <div class="card-body">
            {#if user}
              <p>Click on your username to view your game statistics</p>
              <img src={profile} alt="profile" />
              <p>Track your win rate and best scores</p>
            {:else}
              <p>Click "Login" to create an account or sign in</p>
              <img src={register} alt="register" />
              <p>Track your progress and view statistics</p>
            {/if}
          </div>
        </div>
      </div>

      <div class="button-container">
        <button class="got-it-button" on:click={close}>I got it!</button>
      </div>
    </div>
  </div>
{/if}

<style>
  .tutorials-overlay {
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

  .tutorials-content {
    background: transparent;
    border-radius: 16px;
    max-width: 1200px;
    width: 90%;
    padding: 24px;
    display: flex;
    flex-direction: column;
    gap: 24px;
  }

  .main-title {
    text-align: center;
    margin: 0;
    font-size: 28px;
    font-weight: 700;
    color: white;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  }

  .cards-container {
    display: flex;
    gap: 24px;
  }

  .tutorial-card {
    flex: 1;
    background: white;
    border-radius: 12px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    height: 500px;
  }

  .tutorial-card img {
    width: 100%;
    object-fit: contain;
    border-radius: 8px;
    margin: 8px 0;
  }

  .card-header {
    background: white;
    padding: 16px;
    border-bottom: 1px solid #e5e5e5;
    flex-shrink: 0;
  }

  .card-header h3 {
    margin: 0;
    font-size: 20px;
    font-weight: 600;
    color: #2c3e50;
  }

  .card-body {
    padding: 20px;
    overflow-y: auto;
    flex-grow: 1;
  }

  .card-body p {
    margin: 0 0 12px 0;
    font-size: 16px;
    color: #67666e;
  }

  .button-container {
    display: flex;
    justify-content: center;
    margin-top: 8px;
  }

  .got-it-button {
    background: #6ec374;
    color: white;
    border: none;
    padding: 12px 32px;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.2s ease;
  }

  .got-it-button:hover {
    opacity: 0.6;
  }

  @media (max-width: 767px) {
  
  }

</style> 