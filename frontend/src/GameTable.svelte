<script lang="ts">
  import type { GameGuess } from "./types";
  import gameCover from "./assets/default_game.svg";
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
                <img src={gameCover} alt="cover" class="cover-image" />
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
    background-color: #b5b5b5;
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
    background-color: #BFF4D1;
    color: #62AC7E;
  }
  .tag.red {
    background-color: #ED8181;
    color: #BF3939;
    border: none;
  }
  .tag.default {
    background-color: #e0e0e0;
    color: #353535;
    border: none;
  }

  /* responsive design */
  @media (max-width: 767px) {
    .table-container {
      margin: 10px;
      border-radius: 8px;
      overflow-x: auto;
    }

    table {
      font-size: 14px;
    }

    th {
      padding: 8px 12px;
      font-size: 16px;
      white-space: nowrap;
    }

    td {
      padding: 8px;
      font-size: 14px;
    }

    .empty-message {
      font-size: 16px;
      padding: 20px 10px;
    }

    .cover-image img {
      width: 60px;
      height: 48px;
    }

    .tag {
      padding: 3px 6px;
      font-size: 12px;
      margin: 2px;
    }

    .tags-container {
      gap: 2px;
    }
  }

  @media (max-width: 480px) {
    .table-container {
      margin: 5px;
      box-shadow: -2px 2px 2px 0px rgba(0, 0, 0, 0.1);
    }

    th {
      padding: 6px 8px;
      font-size: 14px;
    }

    td {
      padding: 6px;
      font-size: 12px;
    }

    .empty-message {
      font-size: 14px;
      padding: 15px 8px;
    }

    .cover-image img {
      width: 40px;
      height: 32px;
      border-radius: 6px;
    }

    .tag {
      padding: 2px 4px;
      font-size: 10px;
      border-radius: 10px;
    }

    .tags-container {
      gap: 1px;
    }
  }
</style>
