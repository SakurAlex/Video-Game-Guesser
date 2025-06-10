import { writable } from 'svelte/store';

interface PlatformCategory {
  name: string;
  platforms: string[];
}

interface PlatformCategories {
  [key: string]: PlatformCategory;
}

// Platform categories and their platforms
const platformCategories: PlatformCategories = {
  PC: {
    name: "PC/Desktop",
    platforms: ['PC', 'Mac', 'Linux']
  },
  Mobile: {
    name: "Mobile",
    platforms: ['iOS', 'Android']
  },
  PlayStation: {
    name: "PlayStation",
    platforms: [
      'PlayStation 1',
      'PlayStation 2',
      'PlayStation 3',
      'PlayStation 4',
      'PlayStation 5',
      'PlayStation Portable (PSP)',
      'PlayStation Vita'
    ]
  },
  Xbox: {
    name: "Xbox",
    platforms: [
      'Xbox',
      'Xbox 360',
      'Xbox One',
      'Xbox Series X'
    ]
  },
  Nintendo: {
    name: "Nintendo Home Consoles",
    platforms: [
      'Nintendo Entertainment System (NES)',
      'Super Nintendo (SNES)',
      'Nintendo 64',
      'GameCube',
      'Wii',
      'Wii U',
      'Nintendo Switch'
    ]
  },
  NintendoHandheld: {
    name: "Nintendo Handhelds",
    platforms: [
      'Game Boy',
      'Game Boy Advance',
      'Nintendo DS',
      'Nintendo 3DS'
    ]
  },
  Other: {
    name: "Other Platforms",
    platforms: [
      'Arcade',
      'Dreamcast'
    ]
  }
};

// Flatten platforms array for store
const allPlatforms = Object.values(platformCategories).flatMap(category => category.platforms);

const allGenres = [
  'Action','Adventure','Role-playing (RPG)','Shooter','Platform','Puzzle','Racing','Sports','Strategy','Simulation',
  'Fighting','Stealth','Survival','Sandbox','Pinball','Educational','Indie','Arcade','Family','Music'
];

// Year range constants
const MIN_YEAR = 1981;
const MAX_YEAR = new Date().getFullYear(); // Current year (2025)

export const filters = writable({
  yearStart: MIN_YEAR,
  yearEnd: MAX_YEAR,
  platforms: [...allPlatforms],  // default select all platforms
  genres: [...allGenres],        // default select all genres
  topTier: null,                 // e.g. one of [100, 500, 1000, 5000, 10000, null=unlimited]
  attempts: 10                   // default number of attempts
});

export { platformCategories, allPlatforms, allGenres }; 