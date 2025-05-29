<script lang="ts">
  import rightIcon from './assets/right.svg';
  import settingsIcon from './assets/settings.svg';
  import homeIcon from './assets/home.svg';
  import helpIcon from './assets/question.svg';
  import githubIcon from './assets/github.svg';
</script>

<nav class="navigation-bar">
  <div class="difficulty-section">
    <span class="difficulty-text">Too hard? Lower the difficulty</span>
    <img src={rightIcon} alt="rightArrow" class="arrow-icon" />
  </div>
  <div class="navigation-buttons">
    <button class="navigation-button"><img src={settingsIcon} alt="settings" /></button>
    <button class="navigation-button"><img src={homeIcon} alt="home" /></button>
    <button class="navigation-button"><img src={helpIcon} alt="help" /></button>
    <button class="navigation-button">
      <a href="https://github.com/SakurAlex/Game-Guesser" target="_blank">
        <img src={githubIcon} alt="github" />
      </a>
    </button>
  </div>
</nav>

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
    color: #B3B5BD;
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

  .navigation-button img {
    width: 100%;
    height: 100%;
    object-fit: contain;
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
  }

  @keyframes pulse {
    0%, 100% {
      transform: scale(1);
    }
    50% {
      transform: scale(1.05);
    }
  }
</style>
