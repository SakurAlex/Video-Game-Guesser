<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import giveUpIcon from "./assets/change.svg";
  import type { GameGuess } from "./types";

  export let remainingAttempts = 10;
  export let correctGame: GameGuess | null = null;
  export let isGameOver = false;

  const dispatch = createEventDispatcher();

  function handleGiveUp() {
    if (confirm("Are you sure you want to give up? Click OK to see the answer.")) {
      dispatch("giveUp");
    }
  }

  function handlePlayAgain() {
    dispatch("restart");
  }
</script>

<div class="status-container">
    {#if !isGameOver}
      <h2 class="attempts-text">Remaining Attempts: {remainingAttempts}</h2>
    {/if}
  <button on:click={isGameOver ? handlePlayAgain : handleGiveUp} class={isGameOver ? "play-again-button" : "give-up-button"}>
    {#if !isGameOver}
      <img src={giveUpIcon} alt="Give Up" />
      <span class="button-text">GIVE UP</span>
    {:else}
      <img src={giveUpIcon} alt="Give Up" />
      <span class="button-text">PLAY AGAIN</span>
    {/if}
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
    color: #9ca3ab;
  }

  .give-up-button {
    display: flex;
    gap: 0.25rem;
    align-items: center;
    background-color: #e9776e;
    box-shadow: -4px 4px 4px 0px rgba(0, 0, 0, 0.15);
    border-radius: 20px;
    border: none;
    width: 125px;
    height: 36px;
    cursor: pointer;
  }

  .play-again-button {
    display: flex;
    gap: 0.25rem;
    align-items: center;
    background-color: #75ad79;
    box-shadow: -4px 4px 4px 0px rgba(0, 0, 0, 0.15);
    border-radius: 20px;
    border: none;
    width: 160px;
    height: 36px;
    cursor: pointer;
  }

  .give-up-button:hover {
    opacity: 0.9;
  }

  .play-again-button:hover {
    opacity: 0.9;
  }

  .button-text {
    font-size: 1.125rem;
    font-weight: 700;
    color: white;
  }

  .play-again-text {
    font-size: 1.125rem;
    font-weight: 700;
    color: white;
  }
</style>
