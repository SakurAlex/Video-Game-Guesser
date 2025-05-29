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
      {/if}
      
    </tbody>
  </table>
</section>

<style>
  .table-container {
    background: #FFFFFF;
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
    background-color: #DDEBF5;
  }

  th {
    padding: 12px 30px;
    text-align: left;
    font-size: 22px;
    font-weight: bold;
  }

  td {
    padding: 16px;
    color: #777;
    text-align: left;
  }

  .empty-message {
    text-align: center;
    font-size: 22px;
    font-weight: bold;
    color: #9CA3AB;
  }
</style>
