<script lang="ts">
  import NavigationBar from "./NavigationBar.svelte";
  import SearchBar from "./SearchBar.svelte";
  import GameStatus from "./GameStatus.svelte";
  import GameTable from "./GameTable.svelte";
  import type { GameGuess } from "./types";

  let remainingAttempts = 10;
  let guesses: GameGuess[] = [];
  let healthStatus = "checking...";
  let loading = true;
  let error = null;
  let correctGame: GameGuess | null = null;

  async function fetchInitialRandomGame() {
    try {
      const response = await fetch("http://localhost:8000/api/games/random");
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const randomGameDetails = await response.json();
      correctGame = {
        gameName: randomGameDetails.name,
        releaseYear: randomGameDetails.release_year,
        genres: randomGameDetails.genres,
        developers: randomGameDetails.developers,
        publishers: randomGameDetails.publishers,
        platforms: randomGameDetails.platforms,
        arrow: "",
        genreStatus: "",
        developerStatus: "",
        publisherStatus: "",
        platformStatus: "",
      };
    } catch (err: any) {
      error = `Failed to load random game: ${err.message}`;
      console.error("Error fetching random game:", err);
    }
  }

  fetchInitialRandomGame();

  async function handleGiveUpEvent() {
    remainingAttempts = 10;
    guesses = [];
    correctGame = null;

    await fetchInitialRandomGame();
  }

  function compareYears(guess: GameGuess) {
    if (correctGame) {
      const guessYear = parseInt(guess.releaseYear);
      const answerYear = parseInt(correctGame.releaseYear);
      if (!isNaN(guessYear) && !isNaN(answerYear)) {
        if (guessYear < answerYear) {
          guess.arrow = "up";
        } else if (guessYear > answerYear) {
          guess.arrow = "down";
        } else {
          guess.arrow = "equal";
        }
      }
    }
  }

  function compareArrays(guessArray: string[], correctArray: string[]): string {
    const hasMatch = guessArray.some((item) =>
      correctArray.some(
        (correctItem) =>
          item.toLowerCase().trim() === correctItem.toLowerCase().trim(),
      ),
    );
    return hasMatch ? "green" : "red";
  }

  function compareGenres(guess: GameGuess) {
    if (correctGame && correctGame.genres && guess.genres) {
      guess.genreStatus = compareArrays(guess.genres, correctGame.genres);
    }
  }

  function compareDevelopers(guess: GameGuess) {
    if (correctGame && correctGame.developers && guess.developers) {
      guess.developerStatus = compareArrays(
        guess.developers,
        correctGame.developers,
      );
    }
  }

  function comparePublishers(guess: GameGuess) {
    if (correctGame && correctGame.publishers && guess.publishers) {
      guess.publisherStatus = compareArrays(
        guess.publishers,
        correctGame.publishers,
      );
    }
  }

  function comparePlatforms(guess: GameGuess) {
    if (correctGame && correctGame.platforms && guess.platforms) {
      guess.platformStatus = compareArrays(
        guess.platforms,
        correctGame.platforms,
      );
    }
  }

  function compareAllProperties(guess: GameGuess) {
    compareYears(guess);
    compareGenres(guess);
    compareDevelopers(guess);
    comparePublishers(guess);
    comparePlatforms(guess);
  }

  async function LostEvent() {
    const answerMessage = `
You Lost! Here's the correct answer:

Game: ${correctGame.gameName}
Release Year: ${correctGame.releaseYear}
Genres: ${correctGame.genres.join(", ")}
Developers: ${correctGame.developers.join(", ")}
Publishers: ${correctGame.publishers.join(", ")}
Platforms: ${correctGame.platforms.join(", ")}
    `;
    alert(answerMessage);
    remainingAttempts = 10;
    guesses = [];
    correctGame = null;
    await fetchInitialRandomGame();
  }
</script>

<main>
  <div class="nav-position">
    <NavigationBar />
  </div>
  <div class="content">
    <SearchBar
      on:gameGuessed={(e) => {
        compareAllProperties(e.detail);
        guesses = [...guesses, e.detail];
        remainingAttempts = remainingAttempts - 1;
        if (remainingAttempts == 0) {
          LostEvent();
        }
        if (correctGame) {
          const correctAnswer = `Correct Answer: ${correctGame.gameName}`;
          console.log(correctAnswer);
        }
        if (
          e.detail.gameName.toLowerCase() === correctGame.gameName.toLowerCase()
        ) {
          alert("Congratulations! You guessed the game correctly!");
          remainingAttempts = 10;
          guesses = [];
          correctGame = null;
          fetchInitialRandomGame();
        }
      }}
    />
    <GameStatus
      {remainingAttempts}
      {correctGame}
      on:giveUp={handleGiveUpEvent}
    />
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
