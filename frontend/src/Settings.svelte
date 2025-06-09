<script>
  import { createEventDispatcher, onMount } from 'svelte';
  import { filters } from './stores/filterStore.js';

  const dispatch = createEventDispatcher();

  // Local copy so we only commit on “Apply”
  let local = {
    year: null,
    platforms: [],
    genres: [],
    topTier: null
  };

  // Seed `local` from the store when the modal opens
  onMount(() => {
    filters.subscribe(f => {
      local = { ...f };
    });
  });

  function toggleArray(arr, val) {
    const i = arr.indexOf(val);
    if (i >= 0) arr.splice(i, 1);
    else arr.push(val);
  }

  function applyFilters() {
    filters.set({ ...local });
    dispatch('close');
  }
</script>

<div class="modal-backdrop">
  <div class="modal">
    <h2>Game Filters</h2>

    <!-- Year selector -->
    <label>
      Year:
      <input type="number" bind:value={local.year} placeholder="e.g. 2023" />
    </label>

    <!-- Platform checkboxes -->
    <fieldset>
      <legend>Platforms</legend>
      {#each [
        'PC','Mac','Linux','iOS','Android',
        'PlayStation 1','PlayStation 2','PlayStation 3','PlayStation 4','PlayStation 5','PlayStation Portable (PSP)','PlayStation Vita',
        'Xbox','Xbox 360','Xbox One','Xbox Series X',
        'Nintendo Entertainment System (NES)','Super Nintendo (SNES)','Nintendo 64','GameCube',
        'Wii','Wii U','Nintendo Switch',
        'Game Boy','Game Boy Advance','Nintendo DS','Nintendo 3DS',
        'Arcade','Dreamcast'] as p}
        <label>
          <input type="checkbox"
                 checked={local.platforms.includes(p)}
                 on:change={() => toggleArray(local.platforms, p)} />
          {p}
        </label>
      {/each}
    </fieldset>

    <!-- Genre checkboxes -->
    <fieldset>
      <legend>Genres</legend>
      {#each [
        'Action','Adventure','Role-playing (RPG)','Shooter','Platform','Puzzle','Racing','Sports','Strategy','Simulation',
        'Fighting','Stealth','Survival','Sandbox','Pinball','Educational','Indie','Arcade','Family','Music'] as g}
        <label>
          <input type="checkbox"
                 checked={local.genres.includes(g)}
                 on:change={() => toggleArray(local.genres, g)} />
          {g}
        </label>
      {/each}
    </fieldset>

    <!-- Top-N tier -->
    <fieldset>
      <legend>“Top N” tier</legend>
      {#each [100, 500, 1000, 5000, 10000] as tier}
        <label>
          <input type="radio"
                 name="topTier"
                 value={tier}
                 bind:group={local.topTier} />
          Top {tier}
        </label>
      {/each}
      <label>
        <input type="radio"
               name="topTier"
               value={null}
               bind:group={local.topTier} />
        Unlimited
      </label>
    </fieldset>

    <div class="buttons">
      <button on:click={() => dispatch('close')}>Cancel</button>
      <button on:click={applyFilters}>Apply</button>
    </div>
  </div>
</div>

<style>
  /* your modal styling here */
</style>
