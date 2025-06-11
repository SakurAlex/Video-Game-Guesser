<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import rightIcon from "./assets/right.svg";
  import settingsIcon from "./assets/settings.svg";
  import homeIcon from "./assets/home.svg";
  import helpIcon from "./assets/question.svg";
  import githubIcon from "./assets/github.svg";
  import Settings from './Settings.svelte';
  import Help from './Help.svelte';

  // User Status
  export let user: { username: string } | null = null;

  let showHelptutorials = false;
  let showSettings = false;

  const dispatch = createEventDispatcher();

  // Processing of personal data clicks
  function handleProfileClick() {
    dispatch('showProfile');
  }

  // Handle login clicks
  function handleLoginClick() {
    dispatch('showLogin');
  }

  function handleHomeClick() {
    window.location.reload();
  }
</script>

<nav class="navigation-bar">
  <div class="difficulty-section">
    <span class="difficulty-text">Too hard? Lower the difficulty</span>
    <img src={rightIcon} alt="rightArrow" class="arrow-icon" />
  </div>
  <div class="navigation-buttons">
    
    <button class="navigation-button"
      on:click={() => showSettings = true}
    >
      <img src={settingsIcon} alt="settings" />
    </button>

    <button class="navigation-button" on:click={handleHomeClick}>
      <img src={homeIcon} alt="home" />
    </button>
    <button class="navigation-button" on:click={() => showHelptutorials = true}
      ><img src={helpIcon} alt="help" /></button
    >
    <button class="navigation-button">
      <a href="https://github.com/SakurAlex/Game-Guesser" target="_blank">
        <img src={githubIcon} alt="github" />
      </a>
    </button>
    
    <!-- User status display -->
    {#if user}
      <div class="user-section">
        
        <button class="user-button" on:click={handleProfileClick}>
          <span class="username">{user.username}</span>
        </button>
      </div>
    {:else}
      <button class="login-nav-button" on:click={handleLoginClick}>
        Login
      </button>
    {/if}
  </div>
</nav>

{#if showSettings}
  <Settings on:close={() => showSettings = false} />
{/if}

<Help 
  {user} 
  show={showHelptutorials} 
  on:close={() => showHelptutorials = false} 
/>

<style>
  .navigation-bar {
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #fff;
    border-radius: 22px;
    box-shadow: -4px 4px 4px 0px rgba(0, 0, 0, 0.15);
    padding: 0px 12px;
    height: 56px;
    width: fit-content;
    gap: 5px;
    margin-top: 12px;
    margin-right: 12px;
  }

  .difficulty-section {
    display: flex;
    align-items: center;
    animation: pulse 2s infinite ease-in-out;
  }

  .difficulty-text {
    font-family: Inter;
    font-size: 18px;
    font-style: normal;
    font-weight: 600;
    color: #b3b5bd;
  }

  .arrow-icon {
    width: 50px;
    height: 50px;
    background-color: none;
  }

  .navigation-buttons {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .navigation-button {
    width: 46px;
    height: 46px;
    background: none;
    border: none;
    cursor: pointer;
    padding: 0;
    border: none;
    background: none;
    outline: none;
  }

  .navigation-button img:hover {
    opacity: 0.6;
  }

  .navigation-button img {
    width: 100%;
    height: 100%;
    object-fit: contain;
  }

  /* User related styles */
  .user-section {
    margin-right: 8px;
  }

  .user-button {
    display: flex;
    align-items: center;
    gap: 8px;
    background: #000000;
    color: #ffffff;
    border: none;
    border-radius: 25px;
    padding: 4px 12px 4px 12px;
    cursor: pointer;
    transition: all 0.2s ease;
    height: 46px;
  }

  .user-button:hover {
    opacity: 0.6;
  }

  .username {
    font-family: Inter;
    font-size: 14px;
    font-weight: 600;
    color: #ffffff;
    max-width: 100px;
  }

  .login-nav-button {
    background: #b9dbf3;
    border: none;
    border-radius: 23px;
    padding: 0 16px;
    height: 46px;
    cursor: pointer;
    font-family: Inter;
    font-size: 14px;
    font-weight: 600;
    color: #2c3e50;
    transition: background-color 0.2s ease;
  }

  .login-nav-button:hover {
    background: #a5d0e8;
  }

  /* responsive design */
  @media (max-width: 1024px) {
    .difficulty-section {
      display: none;
    }

    .navigation-bar {
      padding: 0px 8px;
      gap: 8px;
    }

    .navigation-buttons {
      gap: 8px;
    }
  }


  @keyframes pulse {
    0%,
    100% {
      transform: scale(1);
    }
    50% {
      transform: scale(1.05);
    }
  }
</style>
