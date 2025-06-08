<script lang="ts">
  import NavigationBar from "./NavigationBar.svelte";
  import SearchBar from "./SearchBar.svelte";
  import GameStatus from "./GameStatus.svelte";
  import GameTable from "./GameTable.svelte";
  import LoginModal from "./LoginModal.svelte";
  import ProfileModal from "./ProfileModal.svelte";
  import type { GameGuess } from "./types";

  // User state management
  let user = null;
  let userStats = null;
  let showLoginModal = false;
  let showProfileModal = false;
  let authChecked = false;

  let remainingAttempts = 10;
  let guesses: GameGuess[] = [];
  let healthStatus = "checking...";
  let loading = true;
  let error = null;
  let correctGame: GameGuess | null = null;

  const API_BASE_URL = "http://localhost:8000/api";

  // Check user login status
  async function checkAuthStatus() {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/me`, {
        credentials: 'include'
      });
      
      if (response.ok) {
        const data = await response.json();
        user = data.user;
        userStats = data.stats;
      }
    } catch (err) {
      console.log('No active session');
    } finally {
      authChecked = true;
    }
  }

  // 新增：获取用户统计
  async function refreshUserStats() {
    if (!user) return;
    
    try {
      const response = await fetch(`${API_BASE_URL}/auth/me`, {
        credentials: 'include'
      });
      
      if (response.ok) {
        const data = await response.json();
        userStats = data.stats;
      }
    } catch (err) {
      console.error('Failed to refresh stats:', err);
    }
  }

  // Record game results
  async function recordGameResult(won: boolean, attempts: number) {
    if (!user) return;
    
    try {
      const endpoint = won ? '/game/win' : '/game/loss';
      await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify({ attempts })
      });
      
      await refreshUserStats();
    } catch (err) {
      console.error('Failed to record game result:', err);
    }
  }

  async function fetchInitialRandomGame() {
    try {
      const response = await fetch(`${API_BASE_URL}/games/random`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const randomGameDetails = await response.json();
      correctGame = {
        gameName: randomGameDetails.name,
        releaseYear: randomGameDetails.release_year || "Unknown",
        genres: randomGameDetails.genres || [],
        developers: randomGameDetails.developers || [],
        publishers: randomGameDetails.publishers || [],
        platforms: randomGameDetails.platforms || [],
        cover_url: randomGameDetails.cover_url,
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

  // Initialization
  async function initialize() {
    await checkAuthStatus();
    await fetchInitialRandomGame();
    loading = false;
  }

  initialize();

  async function handleGiveUpEvent() {
    // Recording failure results
    if (user) {
      await recordGameResult(false, 10 - remainingAttempts);
    }

    remainingAttempts = 10;
    guesses = [];
    correctGame = null;
    await fetchInitialRandomGame();
  }

  // Improve year comparison function
  function compareYears(guess: GameGuess) {
    if (correctGame && correctGame.releaseYear && guess.releaseYear) {
      // Ensure that the year data exists and is valid
      const guessYearStr = String(guess.releaseYear).trim();
      const correctYearStr = String(correctGame.releaseYear).trim();
      
      // Skip invalid years
      if (guessYearStr === "Unknown" || correctYearStr === "Unknown" || 
          guessYearStr === "" || correctYearStr === "") {
        guess.arrow = "";
        return;
      }
      
      const guessYear = parseInt(guessYearStr);
      const answerYear = parseInt(correctYearStr);
      
      // Ensure that the analysis is successful
      if (!isNaN(guessYear) && !isNaN(answerYear)) {
        if (guessYear < answerYear) {
          guess.arrow = "up";
        } else if (guessYear > answerYear) {
          guess.arrow = "down";
        } else {
          guess.arrow = "equal";
        }
        
        // Debug Information
        console.log(`Year comparison: ${guessYear} vs ${answerYear} -> ${guess.arrow}`);
      } else {
        guess.arrow = "";
        console.log(`Failed to parse years: "${guessYearStr}" vs "${correctYearStr}"`);
      }
    } else {
      guess.arrow = "";
      console.log("Missing year data for comparison");
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
    
    // Recording failure results
    if (user) {
      await recordGameResult(false, 10 - remainingAttempts);
    }

    remainingAttempts = 10;
    guesses = [];
    correctGame = null;
    await fetchInitialRandomGame();
  }

  // Successful login processing
  function handleLoginSuccess(event) {
    user = event.detail;
    showLoginModal = false;
    refreshUserStats();
  }

  // Logout processing
  function handleLogout() {
    user = null;
    userStats = null;
    showProfileModal = false;
  }

  // Show profile
  function showProfile() {
    if (user) {
      showProfileModal = true;
    } else {
      showLoginModal = true;
    }
  }
</script>

{#if loading}
  <div class="loading-screen">
    <div class="loading-spinner"></div>
    <p>Loading GameGuesser...</p>
  </div>
{:else}
  <main>
    <div class="nav-position">
      <NavigationBar {user} on:showProfile={showProfile} on:showLogin={() => showLoginModal = true} />
    </div>
    <div class="content">
      <SearchBar
        on:gameGuessed={async (e) => {
          // Debug Information
          console.log("Game guessed:", e.detail);
          console.log("Correct game:", correctGame);
          
          compareAllProperties(e.detail);
          guesses = [...guesses, e.detail];
          remainingAttempts = remainingAttempts - 1;
          
          if (remainingAttempts == 0) {
            await LostEvent();
            return;
          }
          
          if (correctGame) {
            const correctAnswer = `Correct Answer: ${correctGame.gameName}`;
            console.log(correctAnswer);
          }
          
          if (e.detail.gameName.toLowerCase() === correctGame.gameName.toLowerCase()) {
            alert("Congratulations! You guessed the game correctly!");
            
            //Record victory results
            if (user) {
              await recordGameResult(true, 10 - remainingAttempts);
            }
            
            remainingAttempts = 10;
            guesses = [];
            correctGame = null;
            await fetchInitialRandomGame();
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
{/if}

<!--Modal box-->
<LoginModal 
  bind:isVisible={showLoginModal} 
  on:loginSuccess={handleLoginSuccess}
  on:close={() => showLoginModal = false}
/>

<ProfileModal 
  bind:isVisible={showProfileModal}
  {user}
  stats={userStats}
  on:logout={handleLogout}
  on:close={() => showProfileModal = false}
/>

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

  .loading-screen {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    gap: 20px;
  }

  .loading-spinner {
    width: 40px;
    height: 40px;
    border: 4px solid #e1e5e9;
    border-top: 4px solid #b9dbf3;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  .loading-screen p {
    font-size: 18px;
    color: #666;
    margin: 0;
  }
</style>
