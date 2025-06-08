export interface GameGuess {
  name?: string;
  gameName?: string;  
  releaseYear: number | string;
  genre?: string;
  genres?: string[];  
  developer?: string;
  developers?: string[];  
  publisher?: string;
  publishers?: string[];  
  platform?: string;
  platforms?: string[];  
  cover_url?: string;
  
  arrow?: string;
  genreStatus?: string;
  developerStatus?: string;
  publisherStatus?: string;
  platformStatus?: string;
}