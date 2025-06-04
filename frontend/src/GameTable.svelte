<script lang="ts">
  import type { GameGuess } from "./types";
  export let guesses: GameGuess[] = [];
</script>

<section class="table-container">
  <table>
    <thead>
      <tr>
        <th>Game name</th>
        <th>Release year</th>
        <th>Genre</th>
        <th>Developer</th>
        <th>Publisher</th>
        <th>Platform</th>
      </tr>
    </thead>
    <tbody>
      {#if guesses.length === 0}
        <tr>
          <td colspan="6" class="empty-message">
            🎮 No guesses yet. Try your first one by entering a game name above.
          </td>
        </tr>
      {:else}
        {#each guesses as guess}
          <tr>
            <td>{guess.gameName}</td>
            <td>
              {guess.releaseYear}
              {#if guess.arrow === "up"}
                <span style="color: red;">↑</span>
              {:else if guess.arrow === "down"}
                <span style="color: red;">↓</span>
              {:else if guess.arrow === "equal"}
                <span style="color: green;">=</span>
              {/if}
            </td>
            <td>
              {#if guess.genreStatus === "green"}
                <span style="color: green;">{guess.genres.join(", ")}</span>
              {:else if guess.genreStatus === "red"}
                <span style="color: red;">{guess.genres.join(", ")}</span>
              {:else}
                <span>{guess.genres.join(", ")}</span>
              {/if}
            </td>
            <td>
              {#if guess.developerStatus === "green"}
                <span style="color: green;">{guess.developers.join(", ")}</span>
              {:else if guess.developerStatus === "red"}
                <span style="color: red;">{guess.developers.join(", ")}</span>
              {:else}
                <span>{guess.developers.join(", ")}</span>
              {/if}
            </td>
            <td>
              {#if guess.publisherStatus === "green"}
                <span style="color: green;">{guess.publishers.join(", ")}</span>
              {:else if guess.publisherStatus === "red"}
                <span style="color: red;">{guess.publishers.join(", ")}</span>
              {:else}
                <span>{guess.publishers.join(", ")}</span>
              {/if}
            </td>
            <td>
              {#if guess.platformStatus === "green"}
                <span style="color: green;">{guess.platforms.join(", ")}</span>
              {:else if guess.platformStatus === "red"}
                <span style="color: red;">{guess.platforms.join(", ")}</span>
              {:else}
                <span>{guess.platforms.join(", ")}</span>
              {/if}
            </td>
          </tr>
        {/each}
      {/if}
    </tbody>
  </table>
</section>

<style>
  .table-container {
    background: #ffffff;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: -4px 4px 4px 0px rgba(0, 0, 0, 0.15);
    margin: 20px auto;
    max-width: 1050px;
  }

  table {
    border-collapse: collapse;
    width: 100%;
  }

  thead {
    background-color: #ddebf5;
  }

  th {
    padding: 12px 30px;
    text-align: left;
    font-size: 22px;
    font-weight: bold;
    color: #2c3e50;
  }

  td {
    padding: 16px;
    color: #2c3e50;
    text-align: left;
  }

  .empty-message {
    text-align: center;
    font-size: 22px;
    font-weight: bold;
    color: #9ca3ab;
  }
</style>
