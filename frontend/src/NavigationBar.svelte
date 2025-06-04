<script lang="ts">
  import rightIcon from "./assets/right.svg";
  import settingsIcon from "./assets/settings.svg";
  import homeIcon from "./assets/home.svg";
  import helpIcon from "./assets/question.svg";
  import githubIcon from "./assets/github.svg";

  let showHelptutorials = false;

  function openHelptutorials() {
    showHelptutorials = true;
  }

  function closeHelptutorials() {
    showHelptutorials = false;
  }

  function handleOverlayClick(event: MouseEvent) {
    if (event.target === event.currentTarget) {
      closeHelptutorials();
    }
  }
</script>

<nav class="navigation-bar">
  <div class="difficulty-section">
    <span class="difficulty-text">Too hard? Lower the difficulty</span>
    <img src={rightIcon} alt="rightArrow" class="arrow-icon" />
  </div>
  <div class="navigation-buttons">
    <button class="navigation-button"
      ><img src={settingsIcon} alt="settings" /></button
    >
    <button class="navigation-button">
      <a href="localhost:3000"><img src={homeIcon} alt="home" /></a>
    </button>
    <button class="navigation-button" on:click={openHelptutorials}
      ><img src={helpIcon} alt="help" /></button
    >
    <button class="navigation-button">
      <a href="https://github.com/SakurAlex/Game-Guesser" target="_blank">
        <img src={githubIcon} alt="github" />
      </a>
    </button>
  </div>
</nav>

<!-- Help tutorials -->
{#if showHelptutorials}
  <div class="tutorials-overlay" on:click={handleOverlayClick}>
    <div class="tutorials-content">
      <div class="tutorials-header">
        <h2>How to use GameGuesser</h2>
        <button class="close-button" on:click={closeHelptutorials}
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
      </div>
    </div>
  </div>
{/if}

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

  /* tutorials styles */
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
