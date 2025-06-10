import { writable } from 'svelte/store';

// Platform categories
export const platformCategories = {
  'PC/Desktop': {
    name: 'PC/Desktop',
    platforms: ['PC', 'Mac', 'Linux']
  },
  'Mobile': {
    name: 'Mobile',
    platforms: ['iOS', 'Android']
  },
  'PlayStation': {
    name: 'PlayStation',
    platforms: ['PlayStation 1', 'PlayStation 2', 'PlayStation 3', 'PlayStation 4', 'PlayStation 5', 'PlayStation Portable (PSP)', 'PlayStation Vita']
  },
  'Xbox': {
    name: 'Xbox',
    platforms: ['Xbox', 'Xbox 360', 'Xbox One', 'Xbox Series X']
  },
  'Nintendo Home Consoles': {
    name: 'Nintendo Home Consoles',
    platforms: ['Nintendo Entertainment System (NES)', 'Super Nintendo (SNES)', 'Nintendo 64', 'GameCube', 'Wii', 'Wii U', 'Nintendo Switch']
  },
  'Nintendo Handhelds': {
    name: 'Nintendo Handhelds',
    platforms: ['Game Boy', 'Game Boy Advance', 'Nintendo DS', 'Nintendo 3DS']
  },
  'Other': {
    name: 'Other',
    platforms: ['Arcade', 'Dreamcast']
  }
};

// All platforms list
export const allPlatforms = Object.values(platformCategories).reduce((acc, category) => {
  return [...acc, ...category.platforms];
}, []);

// All genres list
export const allGenres = [
  'Action', 'Adventure', 'Role-playing (RPG)', 'Shooter', 'Platform', 'Puzzle', 'Racing', 'Sports', 'Strategy', 'Simulation',
  'Fighting', 'Stealth', 'Survival', 'Sandbox', 'Pinball', 'Educational', 'Indie', 'Arcade', 'Family', 'Music'
];

// Create the filters store with default values
export const filters = writable({
  yearStart: 1981,
  yearEnd: new Date().getFullYear(),
  platforms: [...allPlatforms],
  genres: [...allGenres],
  topTier: null,
  attempts: 10
}); 