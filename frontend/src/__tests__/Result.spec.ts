import { render, fireEvent, screen } from '@testing-library/svelte';
import Result from '../Result.svelte';
import { vi } from 'vitest';
import type { GameGuess } from '../types';

describe('Result.svelte', () => {
  const mockGame: GameGuess = {
    gameName: 'Mock Game',
    releaseYear: '2021',
    genres: ['Action', 'RPG'],
    developers: ['Dev A'],
    publishers: ['Pub A'],
    platforms: ['PC'],
    cover_url: null, // test fallback
    arrow: '',
    genreStatus: '',
    developerStatus: '',
    publisherStatus: '',
    platformStatus: ''
  };

  it('does not render any result content when isVisible is false', () => {
    render(Result, {
      props: { isVisible: false, correctGame: null, isWin: false, attempts: 0 }
    });
    // No Game Over or Congratulations text
    expect(screen.queryByText('Game Over...')).toBeNull();
    expect(screen.queryByText('🎉 Congratulations! You won!')).toBeNull();
    // No correct answer text
    expect(screen.queryByText('The correct answer is:')).toBeNull();
  });

  it('renders Game Over message and Try Again when isWin is false', () => {
    render(Result, {
      props: { isVisible: true, correctGame: mockGame, isWin: false, attempts: 3 }
    });
    expect(screen.getByText('Game Over...')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Try Again' })).toBeInTheDocument();
  });

  it('renders Congratulations message and Play Again when isWin is true', () => {
    render(Result, {
      props: { isVisible: true, correctGame: mockGame, isWin: true, attempts: 2 }
    });
    expect(screen.getByText('🎉 Congratulations! You won!')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Play Again' })).toBeInTheDocument();
  });

  it('displays correctGame details', () => {
    render(Result, {
      props: { isVisible: true, correctGame: mockGame, isWin: false, attempts: 1 }
    });
    expect(screen.getByText('The correct answer is:')).toBeInTheDocument();
    expect(screen.getByText('Mock Game')).toBeInTheDocument();
    expect(screen.getByText('2021')).toBeInTheDocument();
    expect(screen.getByText('Action, RPG')).toBeInTheDocument();
    expect(screen.getByText('Dev A')).toBeInTheDocument();
    expect(screen.getByText('Pub A')).toBeInTheDocument();
    expect(screen.getByText('PC')).toBeInTheDocument();
  });

  it('emits close when close button clicked', async () => {
    const { component } = render(Result, {
      props: { isVisible: true, correctGame: mockGame, isWin: false, attempts: 0 }
    });
    const closePromise = new Promise(resolve => component.$on('close', resolve));
    await fireEvent.click(screen.getByRole('button', { name: '×' }));
    await expect(closePromise).resolves.toBeDefined();
  });

  it('emits close when overlay clicked outside content', async () => {
    const { container, component } = render(Result, {
      props: { isVisible: true, correctGame: mockGame, isWin: false, attempts: 0 }
    });
    const overlay = container.querySelector('.result-overlay')!;
    const closePromise = new Promise(resolve => component.$on('close', resolve));
    await fireEvent.click(overlay);
    await expect(closePromise).resolves.toBeDefined();
  });

  it('emits restart when Try/Play Again button clicked', async () => {
    const { component } = render(Result, {
      props: { isVisible: true, correctGame: mockGame, isWin: true, attempts: 0 }
    });
    const btn = screen.getByRole('button', { name: 'Play Again' });
    const restartPromise = new Promise(resolve => component.$on('restart', resolve));
    await fireEvent.click(btn);
    await expect(restartPromise).resolves.toBeDefined();
  });
});
