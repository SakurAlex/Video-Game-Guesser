import { render, fireEvent, waitFor, screen } from '@testing-library/svelte';
import SearchBar from '../SearchBar.svelte';
import { vi } from 'vitest';
import type { GameGuess } from '../types';

describe('SearchBar.svelte', () => {
  const mockSuggestions = [
    { id: 1, name: 'Game One', release_year: 2020, cover_url: null },
    { id: 2, name: 'Game Two', release_year: 2021, cover_url: null }
  ];

  beforeEach(() => {
    // stub fetch for both search and detail
    vi.stubGlobal('fetch', vi.fn((input: RequestInfo) => {
      const url = input.toString();
      if (url.includes('/games/search')) {
        return Promise.resolve(new Response(
          JSON.stringify({ results: mockSuggestions }),
          { status: 200 }
        ));
      }
      if (url.includes('/games/1')) {
        return Promise.resolve(new Response(
          JSON.stringify({
            id: 1,
            name: 'Game One',
            release_year: 2020,
            genres: ['Action'],
            developers: ['DevA'],
            publishers: ['PubA'],
            platforms: ['PC'],
            cover_url: null
          }),
          { status: 200 }
        ));
      }
      return Promise.reject(new Error('Unexpected fetch'));
    }));
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('renders no suggestions by default', () => {
    render(SearchBar);
    expect(screen.queryByText('Game One')).toBeNull();
  });

  it('fetches and displays suggestions when typing', async () => {
    render(SearchBar);
    const input = screen.getByPlaceholderText(
      'Search for the game you want to guess...'
    );
    await fireEvent.input(input, { target: { value: 'Game' } });

    // wait for debounce + fetch to complete
    await waitFor(() => {
      expect(screen.getByText('Game One')).toBeInTheDocument();
      expect(screen.getByText('Game Two')).toBeInTheDocument();
    });
  });

  it('emits gameGuessed with full details when suggestion clicked', async () => {
    const { component } = render(SearchBar);
    const input = screen.getByPlaceholderText(
      'Search for the game you want to guess...'
    );
    await fireEvent.input(input, { target: { value: 'Game' } });

    // wait for suggestions
    await waitFor(() => {
      expect(screen.getByText('Game One')).toBeInTheDocument();
    });

    // listen for gameGuessed event
    const promise = new Promise<GameGuess>(resolve =>
      component.$on('gameGuessed', (e: CustomEvent<GameGuess>) => resolve(e.detail))
    );

    // click the first suggestion
    await fireEvent.click(screen.getByText('Game One'));

    const detail = await promise;
    expect(detail.gameName).toBe('Game One');
    expect(detail.releaseYear).toBe(2020);
    expect(detail.genres).toEqual(['Action']);
    expect(detail.developers).toEqual(['DevA']);
    expect(detail.publishers).toEqual(['PubA']);
    expect(detail.platforms).toEqual(['PC']);
  });
});
