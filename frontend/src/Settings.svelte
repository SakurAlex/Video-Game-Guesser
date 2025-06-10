<script lang="ts">
  import { createEventDispatcher, onMount } from 'svelte';
  import { filters, platformCategories, allPlatforms as platformsList } from './stores/filterStore';

  const dispatch = createEventDispatcher();

  // By default, all platforms and genres are selected
  const allPlatforms = [
    'PC','Mac','Linux','iOS','Android',
    'PlayStation 1','PlayStation 2','PlayStation 3','PlayStation 4','PlayStation 5','PlayStation Portable (PSP)','PlayStation Vita',
    'Xbox','Xbox 360','Xbox One','Xbox Series X',
    'Nintendo Entertainment System (NES)','Super Nintendo (SNES)','Nintendo 64','GameCube',
    'Wii','Wii U','Nintendo Switch',
    'Game Boy','Game Boy Advance','Nintendo DS','Nintendo 3DS',
    'Arcade','Dreamcast'
  ];

  const allGenres = [
    'Action','Adventure','Role-playing (RPG)','Shooter','Platform','Puzzle','Racing','Sports','Strategy','Simulation',
    'Fighting','Stealth','Survival','Sandbox','Pinball','Educational','Indie','Arcade','Family','Music'
  ];

  // Year range constants
  const MIN_YEAR = 1981;
  const MAX_YEAR = new Date().getFullYear(); // Current year (2025)

  // Local copy so we only commit on "Apply"
  let local: {
    yearStart: number,
    yearEnd: number,
    platforms: string[],
    genres: string[],
    topTier: number | null,
    attempts: number
  } = {
    yearStart: MIN_YEAR,
    yearEnd: MAX_YEAR,
    platforms: [...allPlatforms],
    genres: [...allGenres],
    topTier: null,
    attempts: 10
  };

  // UI state for messages
  let isApplying = false;
  let message = '';
  let messageType: 'success' | 'error' | '' = '';

  // Store the original filters state when Settings opens
  let originalFilters: typeof local;

  // Seed `local` from the store when the modal opens
  onMount(() => {
    const unsubscribe = filters.subscribe((f: any) => {
      if (f.platforms.length > 0 || f.genres.length > 0 || f.yearStart || f.yearEnd || f.topTier || f.attempts) {
        local = {
          yearStart: f.yearStart,
          yearEnd: f.yearEnd,
          platforms: [...f.platforms],
          genres: [...f.genres],
          topTier: f.topTier,
          attempts: f.attempts
        };
      }
      // Save the original state for comparison
      originalFilters = {
        yearStart: local.yearStart,
        yearEnd: local.yearEnd,
        platforms: [...local.platforms],
        genres: [...local.genres],
        topTier: local.topTier,
        attempts: local.attempts
      };
      
      console.log('🎯 Settings opened - Original state saved:', originalFilters);
    });
    unsubscribe();
  });

  function toggleArray(arr: string[], val: string) {
    const i = arr.indexOf(val);
    if (i >= 0) arr.splice(i, 1);
    else arr.push(val);
  }

  function togglePlatformCategory(category: string) {
    const categoryPlatforms = platformCategories[category].platforms;
    const allSelected = categoryPlatforms.every(p => local.platforms.includes(p));
    
    if (allSelected) {
      // Remove all platforms in this category
      local.platforms = local.platforms.filter(p => !categoryPlatforms.includes(p));
    } else {
      // Add all missing platforms from this category
      const missingPlatforms = categoryPlatforms.filter(p => !local.platforms.includes(p));
      local.platforms = [...local.platforms, ...missingPlatforms];
    }
  }

  function isPlatformCategorySelected(category: string): boolean {
    const categoryPlatforms = platformCategories[category].platforms;
    return categoryPlatforms.every(p => local.platforms.includes(p));
  }

  function isPlatformCategoryPartiallySelected(category: string): boolean {
    const categoryPlatforms = platformCategories[category].platforms;
    const selectedCount = categoryPlatforms.filter(p => local.platforms.includes(p)).length;
    return selectedCount > 0 && selectedCount < categoryPlatforms.length;
  }

  // Genre selection functions
  function toggleAllGenres() {
    if (local.genres.length === allGenres.length) {
      local.genres = [];
    } else {
      local.genres = [...allGenres];
    }
  }

  // Handle year input blur events
  function handleYearStartBlur() {
    if (!local.yearStart || local.yearStart < MIN_YEAR) {
      local.yearStart = MIN_YEAR;
    } else if (local.yearStart > local.yearEnd) {
      local.yearStart = local.yearEnd;
    }
  }

  function handleYearEndBlur() {
    if (!local.yearEnd || local.yearEnd > MAX_YEAR) {
      local.yearEnd = MAX_YEAR;
    } else if (local.yearEnd < local.yearStart) {
      local.yearEnd = local.yearStart;
    }
  }

  // Handle attempts input
  function handleAttemptsChange(event: Event) {
    const value = parseInt((event.target as HTMLInputElement).value);
    if (value < 1) {
      local.attempts = 1;
    } else if (value > 999) {
      local.attempts = 999;
    }
  }

  async function applyFilters() {
    isApplying = true;
    message = '';
    messageType = '';

    try {
      // Validation: Check if any platforms or genres are selected
      if (local.platforms.length === 0 && local.genres.length === 0) {
        message = 'Please select at least one platform or game type';
        messageType = 'error';
        return;
      }

      // Check if settings actually changed compared to original state
      const hasChanged = JSON.stringify(originalFilters) !== JSON.stringify(local);
      
      console.log('🔍 Filter change detection:');
      console.log('Original filters:', originalFilters);
      console.log('New local filters:', local);  
      console.log('Has changed:', hasChanged);

      if (!hasChanged) {
        message = 'Settings did not change';
        messageType = 'success';
        return;
      }

      // Test if the new filters can find games
      const testParams = new URLSearchParams();
      if (local.yearStart) testParams.append('yearStart', local.yearStart.toString());
      if (local.yearEnd) testParams.append('yearEnd', local.yearEnd.toString());
      local.platforms.forEach(p => testParams.append('platforms', p));
      local.genres.forEach(g => testParams.append('genres', g));
      if (local.topTier) testParams.append('topTier', local.topTier.toString());

      const testResponse = await fetch(`/api/games/random?${testParams.toString()}`);
      
      if (!testResponse.ok) {
        if (testResponse.status === 404) {
          message = 'No games found with current filters, please adjust settings';
          messageType = 'error';
          return;
        } else {
          throw new Error('Error testing filters');
        }
      }

      // Apply the filters since they changed and are valid
      filters.set({ ...local } as any);
      
      // Update original filters to current state for next comparison with deep copy
      originalFilters = {
        yearStart: local.yearStart,
        yearEnd: local.yearEnd,
        platforms: [...local.platforms], // Deep copy array
        genres: [...local.genres],       // Deep copy array
        topTier: local.topTier,
        attempts: local.attempts
      };
      
      message = 'Filter settings updated successfully! New random game will be selected based on new settings.';
      messageType = 'success';

    } catch (error) {
      console.error('Apply filters error:', error);
      message = 'Error applying filters, please try again';
      messageType = 'error';
    } finally {
      isApplying = false;
    }
  }
</script>

<div class="settings-overlay" on:click={(e) => e.target === e.currentTarget && dispatch('close')}>
  <div class="settings-content">
    <div class="settings-header">
    <h2>Game Filters</h2>
      <button class="close-button" on:click={() => dispatch('close')}
        >&times;</button
      >
    </div>
    <div class="settings-body">
      <!-- Number of Attempts -->
      <div class="filter-section">
        <h3>Number of Attempts</h3>
        <div class="attempts-container">
          <input
            type="number"
            bind:value={local.attempts}
            on:change={handleAttemptsChange}
            min="1"
            max="999"
            class="attempts-input"
          />
        </div>
      </div>
      <!-- Year Range selector -->
      <div class="filter-section">
        <h3>Year Range</h3>
        <div class="year-range-container">
          <input 
            type="number" 
            bind:value={local.yearStart} 
            on:blur={handleYearStartBlur}
            placeholder="Start year" 
            class="year-input" />
          <span class="year-separator">to</span>
          <input 
            type="number" 
            bind:value={local.yearEnd} 
            on:blur={handleYearEndBlur}
            placeholder="End year" 
            class="year-input" />
        </div>
      </div>

    <!-- Platform checkboxes -->
      <div class="filter-section">
        <div class="section-header">
          <h3>Platforms <span class="selection-count">({local.platforms.length}/{platformsList.length})</span></h3>
        </div>
        <div class="platform-categories">
          {#each Object.entries(platformCategories) as [key, category]}
            <div class="platform-category">
              <label class="checkbox-label category-label">
                <input
                  type="checkbox"
                  checked={isPlatformCategorySelected(key)}
                  indeterminate={isPlatformCategoryPartiallySelected(key)}
                  on:change={() => togglePlatformCategory(key)}
                />
                <span class="checkmark {isPlatformCategoryPartiallySelected(key) ? 'partial' : ''}"></span>
                {category.name}
              </label>
              <div class="platform-list">
                {#each category.platforms as platform}
                  <label class="checkbox-label platform-item">
                    <input
                      type="checkbox"
                      checked={local.platforms.includes(platform)}
                      on:change={() => toggleArray(local.platforms, platform)}
                    />
                    <span class="checkmark"></span>
                    {platform}
        </label>
      {/each}
              </div>
            </div>
          {/each}
        </div>
      </div>

    <!-- Genre checkboxes -->
      <div class="filter-section">
        <div class="section-header">
          <h3>Genres <span class="selection-count">({local.genres.length}/{allGenres.length})</span></h3>
          <div class="toggle-action">
            <button 
              class="toggle-btn" 
              on:click={toggleAllGenres}
              class:selected={local.genres.length === allGenres.length}
            >
              {local.genres.length === allGenres.length ? 'Clear All' : 'Select All'}
            </button>
          </div>
        </div>
        <div class="checkbox-grid">
          {#each allGenres as g}
            <label class="checkbox-label">
          <input type="checkbox"
                 checked={local.genres.includes(g)}
                 on:change={() => toggleArray(local.genres, g)} />
              <span class="checkmark"></span>
          {g}
        </label>
      {/each}
        </div>
      </div>

    <!-- Top-N tier -->
      <div class="filter-section">
        <h3>"Top N" Tier</h3>
        <div class="radio-group">
      {#each [100, 500, 1000, 5000, 10000] as tier}
            <label class="radio-label">
          <input type="radio"
                 name="topTier"
                 value={tier}
                 bind:group={local.topTier} />
              <span class="radio-mark"></span>
          Top {tier}
        </label>
      {/each}
          <label class="radio-label">
        <input type="radio"
               name="topTier"
               value={null}
               bind:group={local.topTier} />
            <span class="radio-mark"></span>
        Unlimited
      </label>
        </div>
      </div>
    </div>

    <!-- Message display -->
    {#if message}
      <div class="message-bar" class:success={messageType === 'success'} class:error={messageType === 'error'}>
        {message}
      </div>
    {/if}

    <div class="settings-footer">
      <button class="apply-button" on:click={applyFilters} disabled={isApplying}>
        {#if isApplying}
          Applying...
        {:else}
          Apply Settings
        {/if}
      </button>
      <button class="close-button-footer" on:click={() => dispatch('close')}>Close</button>
    </div>
  </div>
</div>

<style>
  .settings-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }

  .settings-content {
    background: white;
    border-radius: 16px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    max-width: 800px;
    max-height: 80vh;
    width: 90%;
    display: flex;
    flex-direction: column;
  }

  .settings-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 24px 12px 24px;
    border-bottom: 1px solid #e5e5e5;
    flex-shrink: 0;
  }

  .settings-header h2 {
    margin: 0;
    font-size: 24px;
    font-weight: 700;
    color: #2c3e50;
  }

  .close-button {
    background: none;
    border: none;
    font-size: 32px;
    color: #9ca3ab;
    cursor: pointer;
    padding: 0;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: background-color 0.2s ease;
  }

  .close-button:hover {
    background-color: #f5f5f5;
  }

  .settings-body {
    padding: 24px;
    overflow-y: auto;
    flex: 1;
  }

  .filter-section {
    margin-bottom: 24px;
  }

  .filter-section:last-child {
    margin-bottom: 0;
  }

  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
  }

  .filter-section h3 {
    margin: 0;
    font-size: 18px;
    font-weight: 600;
    color: #2c3e50;
  }

  .selection-count {
    font-size: 14px;
    font-weight: 400;
    color: #666;
    margin-left: 8px;
  }

  .year-range-container {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
  }

  .year-input {
    width: 100%;
    max-width: 150px;
    padding: 8px 12px;
    border: 2px solid #e1e5e9;
    border-radius: 8px;
    font-size: 14px;
    color: #2c3e50;
    transition: border-color 0.2s ease;
  }

  /* Remove number input spinners */
  .year-input::-webkit-outer-spin-button,
  .year-input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }

  .year-input[type=number] {
    -moz-appearance: textfield;
  }

  .year-input:focus {
    outline: none;
    border-color: #b9dbf3;
  }

  .year-separator {
    font-size: 14px;
    color: #666;
    font-weight: 500;
  }

  .checkbox-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 8px;
    max-height: 200px;
    overflow-y: auto;
    padding: 8px;
    border: 1px solid #e5e5e5;
    border-radius: 8px;
    background: #fafafa;
  }

  .checkbox-label {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    padding: 4px 8px;
    border-radius: 6px;
    transition: background-color 0.2s ease;
    font-size: 14px;
    color: #2c3e50;
  }

  .checkbox-label:hover {
    background-color: #f0f7ff;
  }

  .checkbox-label input[type="checkbox"] {
    display: none;
  }

  .checkmark {
    width: 16px;
    height: 16px;
    border: 2px solid #b9dbf3;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
    flex-shrink: 0;
  }

  .checkbox-label input[type="checkbox"]:checked + .checkmark {
    background-color: #b9dbf3;
    border-color: #a5d0e8;
  }

  .checkbox-label input[type="checkbox"]:checked + .checkmark::after {
    content: "✓";
    color: white;
    font-size: 12px;
    font-weight: bold;
  }

  .radio-group {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
  }

  .radio-label {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    padding: 8px 12px;
    border: 2px solid #e1e5e9;
    border-radius: 20px;
    transition: all 0.2s ease;
    font-size: 14px;
    color: #2c3e50;
  }

  .radio-label:hover {
    border-color: #b9dbf3;
    background-color: #f0f7ff;
  }

  .radio-label input[type="radio"] {
    display: none;
  }

  .radio-mark {
    width: 16px;
    height: 16px;
    border: 2px solid #b9dbf3;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
    flex-shrink: 0;
  }

  .radio-label input[type="radio"]:checked + .radio-mark {
    border-color: #a5d0e8;
  }

  .radio-label input[type="radio"]:checked + .radio-mark::after {
    content: "";
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: #b9dbf3;
  }

  .radio-label input[type="radio"]:checked {
    background-color: #f0f7ff;
    border-color: #b9dbf3;
  }

  .message-bar {
    padding: 12px 24px;
    margin: 0;
    font-size: 14px;
    font-weight: 500;
    border-top: 1px solid #e5e5e5;
    animation: slideIn 0.3s ease;
  }

  .message-bar.success {
    background-color: #d4edda;
    color: #155724;
    border-left: 4px solid #28a745;
  }

  .message-bar.error {
    background-color: #f8d7da;
    color: #721c24;
    border-left: 4px solid #dc3545;
  }

  @keyframes slideIn {
    from {
      opacity: 0;
      transform: translateY(-10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .settings-footer {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    padding: 16px 24px;
    border-top: 1px solid #e5e5e5;
    flex-shrink: 0;
  }

  .apply-button, .close-button-footer {
    padding: 10px 20px;
    border: none;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .apply-button {
    background: #28a745;
    color: white;
    border: 2px solid #28a745;
  }

  .apply-button:hover:not(:disabled) {
    background: #218838;
    border-color: #1e7e34;
  }

  .apply-button:disabled {
    background: #6c757d;
    border-color: #6c757d;
    cursor: not-allowed;
    opacity: 0.7;
  }

  .close-button-footer {
    background: #f8f9fa;
    color: #67666e;
    border: 2px solid #e1e5e9;
  }

  .close-button-footer:hover {
    background: #e9ecef;
    border-color: #d3d3d3;
  }

  .platform-categories {
    display: flex;
    flex-direction: column;
    gap: 16px;
    max-height: 400px;
    overflow-y: auto;
    padding: 12px;
    border: 1px solid #e5e5e5;
    border-radius: 8px;
    background: #fafafa;
  }

  .platform-category {
    border: 1px solid #e1e5e9;
    border-radius: 8px;
    padding: 8px;
    background: white;
  }

  .category-label {
    font-weight: 600;
    padding: 8px;
    background-color: #f8f9fa;
    border-radius: 6px;
    margin-bottom: 8px;
  }

  .platform-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 4px;
    padding-left: 24px;
  }

  .platform-item {
    font-size: 13px;
  }

  .checkmark.partial::after {
    content: "";
    position: absolute;
    left: 4px;
    top: 7px;
    width: 8px;
    height: 2px;
    background-color: white;
  }

  .toggle-action {
    display: flex;
    align-items: center;
  }

  .toggle-btn {
    padding: 6px 16px;
    font-size: 13px;
    font-weight: 500;
    border: 2px solid #b9dbf3;
    background: white;
    color: #2c3e50;
    border-radius: 20px;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .toggle-btn:hover {
    background: #f0f7ff;
  }

  .toggle-btn.selected {
    background: #b9dbf3;
    color: white;
  }

  .toggle-btn:active {
    transform: scale(0.95);
  }

  .attempts-container {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-top: 8px;
  }

  .attempts-input {
    width: 100px;
    padding: 8px 12px;
    border: 2px solid #e1e5e9;
    border-radius: 8px;
    font-size: 14px;
    color: #2c3e50;
    transition: border-color 0.2s ease;
  }

  .attempts-input::-webkit-outer-spin-button,
  .attempts-input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }

  .attempts-input[type=number] {
    -moz-appearance: textfield;
  }

  .attempts-input:focus {
    outline: none;
    border-color: #b9dbf3;
  }

  .attempts-description {
    font-size: 14px;
    color: #666;
  }

  @media (max-width: 768px) {
    .settings-content {
      width: 95%;
      max-height: 85vh;
    }

    .settings-header,
    .settings-body,
    .settings-footer {
      padding: 16px;
    }

    .settings-header h2 {
      font-size: 20px;
    }

    .filter-section h3 {
      font-size: 16px;
    }

    .checkbox-grid {
      grid-template-columns: 1fr;
      max-height: 150px;
    }

    .radio-group {
      flex-direction: column;
    }

    .settings-footer {
      flex-direction: column;
    }

    .apply-button, .close-button-footer {
      width: 100%;
    }

    .section-header {
      flex-direction: column;
      align-items: flex-start;
      gap: 8px;
    }

    .year-range-container {
      flex-direction: column;
      align-items: stretch;
    }

    .year-input {
      max-width: none;
    }

    .platform-list {
      grid-template-columns: 1fr;
      padding-left: 12px;
    }

    .platform-categories {
      max-height: 300px;
    }

    .toggle-action {
      margin-top: 8px;
    }

    .toggle-btn {
      width: 100%;
    }

    .attempts-container {
      flex-direction: column;
      align-items: flex-start;
    }

    .attempts-input {
      width: 100%;
    }
  }
</style>
