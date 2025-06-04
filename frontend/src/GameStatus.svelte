<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import giveUpIcon from "./assets/change.svg";
  import type { GameGuess } from "./types";

  export let remainingAttempts = 10;
  export let correctGame: GameGuess | null = null;

  const dispatch = createEventDispatcher();

  function handleGiveUp() {
    if (correctGame) {
      const answerMessage = `
You gave up! Here's the correct answer:

Game: ${correctGame.gameName}
Release Year: ${correctGame.releaseYear}
Genres: ${correctGame.genres.join(", ")}
Developers: ${correctGame.developers.join(", ")}
Publishers: ${correctGame.publishers.join(", ")}
Platforms: ${correctGame.platforms.join(", ")}
    `;
      alert(answerMessage);
    } else {
      alert("You gave up! But no game was loaded.");
    }

    dispatch("giveUp");
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

  .give-up-button:hover {
    opacity: 0.9;
  }

  .give-up-text {
    font-size: 1.125rem;
    font-weight: 700;
    color: white;
  }
</style>
