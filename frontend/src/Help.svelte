<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  
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
      <div class="tutorials-header">
        <h2>How to use GameGuesser</h2>
        <button class="close-button" on:click={close}
          >&times;</button
        >
      </div>
      <div class="tutorials-body">
        <div class="help-section">
          <p>This is a small game to guess the game!</p>
          <p>You have 10 chances (default) to guess the correct game.</p>
        </div>
        <div class="help-section">
          <h3>How to start</h3>
          <ul>
            <li>
              Input the name of the game you want to guess in the search bar
            </li>
            <li>Click the blue search button to make a guess</li>
            <li>Check the hint information to adjust your next guess</li>
          </ul>
        </div>
        <!-- Login related help -->
        {#if user}
          <div class="help-section">
            <h3>Your Profile</h3>
            <ul>
              <li>Click on your username to view your game statistics</li>
              <li>Track your win rate and best scores</li>
            </ul>
          </div>
        {:else}
          <div class="help-section">
            <h3>Create Account</h3>
            <ul>
              <li>Click "Login" to create an account or sign in</li>
              <li>Track your progress and view statistics</li>
            </ul>
          </div>
        {/if}
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
    background: white;
    border-radius: 16px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    max-width: 600px;
  }

  .tutorials-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 16px 8px 16px;
    border-bottom: 1px solid #e5e5e5;
  }

  .tutorials-header h2 {
    margin: 0;
    font-size: 24px;
    font-weight: 700;
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

  .tutorials-body {
    padding: 16px;
  }

  .help-section {
    margin-bottom: 10px;
  }

  .help-section:last-child {
    margin-bottom: 0;
  }

  .help-section h3 {
    margin: 0 0 6px 0;
    font-size: 18px;
    font-weight: 600;
    color: #2c3e50;
  }

  .help-section p {
    margin: 0px 0;
    font-size: 16px;
    line-height: 1.5;
    color: #67666e;
  }

  .help-section ul {
    margin: 5px 0;
    padding-left: 20px;
  }

  .help-section li {
    margin: 6px 0;
    font-size: 16px;
    color: #67666e;
  }

  @media (max-width: 640px) {
    .tutorials-content {
      width: 95%;
    }

    .tutorials-header,
    .tutorials-body {
      padding: 16px;
    }

    .tutorials-header h2 {
      font-size: 20px;
    }

    .help-section h3 {
      font-size: 16px;
    }

    .help-section p,
    .help-section li {
      font-size: 14px;
    }
  }
</style> 