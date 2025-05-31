<script lang="ts">
  export let remainingAttempts = 10;
  import giveUpIcon from './assets/change.svg';
  
  function handleGiveUp() {
    alert("You gave up! Let's check the answer!");
    remainingAttempts = 10;
  }
</script>

<div class="status-container">
  <h2 class="attempts-text">Remaining Attempts: {remainingAttempts}</h2>
  <button on:click={handleGiveUp} class="give-up-button">
    <img src={giveUpIcon} alt="Give Up" />
    <span class="give-up-text">GIVE UP</span>
  </button>
</div>

<style>
  .status-container {
    align-items: center;
    display: flex;
    flex-direction: row;
    margin-top: 20px;
    gap: 10px;
  }

  .attempts-text {
    font-size: 22px;
    font-weight: 700;
    color: #9CA3AB;
  }

  .give-up-button {
    display: flex;
    gap: 0.25rem;
    align-items: center;
    background-color: #E9776E;
    box-shadow: -4px 4px 4px 0px rgba(0, 0, 0, 0.15);
    border-radius: 20px;
    border: none;
    width: 125px;
    height: 36px;
    cursor: pointer;
  }

  .give-up-button:hover {
    opacity: 0.9;
  }

  .give-up-text {
    font-size: 1.125rem;
    font-weight: 700;
    color: white;
  }

</style>
