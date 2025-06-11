import { render, fireEvent, screen } from '@testing-library/svelte';
import { vi } from 'vitest';
import GameStatus from '../GameStatus.svelte';

describe('GameStatus', () => {
  beforeEach(() => {
    // stub confirm() to always return true
    vi.stubGlobal('confirm', () => true);
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('displays remaining attempts and emits giveUp when the "GIVE UP" button is clicked', async () => {
    const { component } = render(GameStatus, {
      props: { remainingAttempts: 3, correctGame: null }
    });

    expect(screen.getByText(/Remaining Attempts:\s*3/i)).toBeInTheDocument();
    const giveUpButton = screen.getByRole('button', { name: /give up/i });
    const giveUpPromise = new Promise(resolve => component.$on('giveUp', resolve));

    await fireEvent.click(giveUpButton);
    await expect(giveUpPromise).resolves.toBeDefined();
  });
});
