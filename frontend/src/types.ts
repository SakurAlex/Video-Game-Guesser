export interface GameGuess {
  gameName: string;
  releaseYear: string | number;
  genres: string[];
  developers: string[];
  publishers: string[];
  platforms: string[];
  cover_url?: string;
  arrow: string;
  genreStatus: string;
  developerStatus: string;
  publisherStatus: string;
  platformStatus: string;
  genreStatuses?: string[];
  developerStatuses?: string[];
  publisherStatuses?: string[];
  platformStatuses?: string[];
}

export interface User {
  id: number;
  username: string;
  email: string;
}

export interface UserStats {
  total_games: number;
  games_won: number;
  total_attempts: number;
  best_attempts: number | null;
  win_rate: number;
}

export interface Filters {
  yearStart: number | null;
  yearEnd: number | null;
  platforms: string[];
  genres: string[];
  topTier: number | null;
  attempts: number;
}