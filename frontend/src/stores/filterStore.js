import { writable } from 'svelte/store';

export const filters = writable({
  year: null,          // e.g. 2020
  platforms: [],       // e.g. ['PC', 'PS5']
  genres: [],          // e.g. ['Action', 'RPG']
  topTier: null        // e.g. one of [100, 500, 1000, 5000, 10000, null=unlimited]
});
