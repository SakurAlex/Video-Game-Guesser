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
          <!--
          <div class="user-avatar">
            {user.username.charAt(0).toUpperCase()}
          </div>
          -->
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
    opacity: 0.8;
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
    background: #f8f9fa;
    border: 2px solid #e1e5e9;
    border-radius: 23px;
    padding: 4px 12px 4px 12px;
    cursor: pointer;
    transition: all 0.2s ease;
    height: 46px;
  }

  .user-button:hover {
    background: #b9dbf3;
    border-color: #a5d0e8;
  }

  .user-avatar {
    width: 36px;
    height: 36px;
    background: linear-gradient(135deg, #b9dbf3, #a5d0e8);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    font-weight: bold;
    color: #2c3e50;
  }

  .username {
    font-family: Inter;
    font-size: 14px;
    font-weight: 600;
    color: #2c3e50;
    max-width: 100px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
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



  @media (max-width: 640px) {
    .navigation-bar-container {
      padding: 10px;
    }

    .navigation-bar {
      width: 100%;
      border-radius: 0;
      padding: 6px 12px;
      justify-content: space-between;
    }

    .difficulty-text {
      font-size: 12px;
    }

    .navigation-button {
      width: 32px;
      height: 32px;
    }

    .user-button {
      height: 36px;
      padding: 2px 8px 2px 2px;
    }

    .user-avatar {
      width: 30px;
      height: 30px;
      font-size: 14px;
    }

    .username {
      font-size: 12px;
      max-width: 60px;
    }

    .login-nav-button {
      height: 36px;
      padding: 0 12px;
      font-size: 12px;
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
