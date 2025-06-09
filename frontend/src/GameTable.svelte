<script lang="ts">
  import type { GameGuess } from "./types";
  export let guesses: GameGuess[] = [];
</script>

<section class="table-container">
  <table>
    <thead>
      <tr>
        <th>Cover</th>
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
          <td colspan="7" class="empty-message">
            🎮 No guesses yet. Try your first one by entering a game name above.
          </td>
        </tr>
      {:else}
        {#each guesses as guess}
          <tr>
            <td class="cover-image">
              {#if guess.cover_url}
                <img src={guess.cover_url} alt="cover" class="cover-image" />
              {:else}
                <span>🎮</span>
              {/if}
            </td>
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
              <div class="tags-container">
                {#each guess.genres || [] as genre, index}
                  <span class="tag {guess.genreStatuses?.[index] || 'default'}"
                    >{genre}</span
                  >
                {/each}
              </div>
            </td>
            <td>
              <div class="tags-container">
                {#each guess.developers || [] as developer, index}
                  <span
                    class="tag {guess.developerStatuses?.[index] || 'default'}"
                    >{developer}</span
                  >
                {/each}
              </div>
            </td>
            <td>
              <div class="tags-container">
                {#each guess.publishers || [] as publisher, index}
                  <span
                    class="tag {guess.publisherStatuses?.[index] || 'default'}"
                    >{publisher}</span
                  >
                {/each}
              </div>
            </td>
            <td>
              <div class="tags-container">
                {#each guess.platforms || [] as platform, index}
                  <span
                    class="tag {guess.platformStatuses?.[index] || 'default'}"
                    >{platform}</span
                  >
                {/each}
              </div>
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
    max-width: 1300px;
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
    text-align: center;
    font-size: 22px;
    font-weight: bold;
    color: #2c3e50;
  }
  td {
    padding: 14px;
    font-size: 18px;
    font-weight: bold;
    color: #2c3e50;
    text-align: center;
  }
  .empty-message {
    text-align: center;
    font-size: 22px;
    font-weight: bold;
    color: #9ca3ab;
  }
  .cover-image img {
    width: 100px;
    height: 80px;
    object-fit: cover;
    border-radius: 10px;
    border: 1px solid #ddd;
  }
  .cover-image {
    text-align: center;
  }
  .tags-container {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
    align-items: center;
    justify-content: center;
  }
  .tag {
    display: inline-block;
    padding: 5px 9px;
    border-radius: 14px;
    font-size: 14px;
    font-weight: bold;
    white-space: nowrap;
    border: 1px solid transparent;
    transition: all 0.2s ease;
  }
  .tag.green {
    background-color: #50b973;
    color: white;
  }
  .tag.red {
    background-color: #ec5c5c;
    color: white;
    border: none;
  }
  .tag.default {
    background-color: #e0e0e0;
    color: #333;
    border: none;
  }
</style>
