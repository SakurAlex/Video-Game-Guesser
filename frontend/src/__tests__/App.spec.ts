import { render, screen, waitFor } from '@testing-library/svelte';
import App from '../App.svelte';
import { vi } from 'vitest';

describe('App.svelte', () => {
  beforeEach(() => {
    //Mock /auth/me to return a 401 (no session)
    vi.stubGlobal('fetch', vi.fn((url: string) => {
      if (url.endsWith('/auth/me')) {
        return Promise.resolve(new Response(null, { status: 401 }));
      }
      //Mock /games/random to return one game immediately
      if (url.includes('/games/random')) {
        return Promise.resolve(
          new Response(
            JSON.stringify({
              id: 123,
              name: 'Mock Game',
              first_release_date: 1609459200, // 2021-01-01
              genres: [{ name: 'Action' }],
              platforms: [{ name: 'PC' }],
              involved_companies: [],
              cover: { url: '//image.url/cover.jpg' },
              screenshots: [],
              popularity: 42
            }),
            { status: 200 }
          )
        );
      }
      return Promise.reject(new Error(`Unexpected fetch: ${url}`));
    }));
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('shows loading spinner, then renders the navigation bar', async () => {
    const { container } = render(App);

    //Initially the loading spinner should be in the document
    expect(screen.getByText('Loading GameGuesser...')).toBeInTheDocument();
    expect(container.querySelector('.loading-spinner')).toBeInTheDocument();

    //After both fetches resolve, the loading screen disappears
    await waitFor(() => {
      expect(screen.queryByText('Loading GameGuesser...')).not.toBeInTheDocument();
    });

    //The Login button from NavigationBar should now be visible
    expect(screen.getByText('Login')).toBeInTheDocument();

    //And your mock game name should _not_ yet appear until you guess
    expect(screen.queryByText('Mock Game')).not.toBeInTheDocument();
  });
});
