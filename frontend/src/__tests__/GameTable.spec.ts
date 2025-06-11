import { render, screen } from '@testing-library/svelte';
import GameTable from '../GameTable.svelte';
import type { GameGuess } from '../types';

const mockGuesses: GameGuess[] = [
  {
    gameName: 'Test Game',
    releaseYear: '2020',
    genres: ['Action', 'RPG'],
    developers: ['Dev A', 'Dev B'],
    publishers: ['Pub A'],
    platforms: ['PC', 'Switch'],
    cover_url: 'cover.png',
    arrow: 'equal',
    genreStatuses: ['green', 'red'],
    developerStatuses: ['green', 'green'],
    publisherStatuses: ['green'],
    platformStatuses: ['green', 'red'],
  }
];

describe('GameTable', () => {
  it('renders no rows if guesses is empty', () => {
    render(GameTable, { props: { guesses: [] } });
    expect(screen.queryByText('Test Game')).not.toBeInTheDocument();
  });

  it('renders a row for each guess with correct data', () => {
    const { container } = render(GameTable, { props: { guesses: mockGuesses } });

    // Cover image
    const img = screen.getByAltText('cover') as HTMLImageElement;
    expect(img).toBeInTheDocument();
    expect(img.src).toContain('cover.png');

    // Game name and year with arrow icon
    expect(screen.getByText('Test Game')).toBeInTheDocument();
    expect(screen.getByText('2020')).toBeInTheDocument();
    // Arrow '=' is rendered as text sibling
    expect(container).toHaveTextContent('=');

    // Genre tags
    const actionTag = screen.getByText('Action');
    const rpgTag = screen.getByText('RPG');
    expect(actionTag).toHaveClass('tag', 'green');
    expect(rpgTag).toHaveClass('tag', 'red');

    // Developer tags
    const devA = screen.getByText('Dev A');
    const devB = screen.getByText('Dev B');
    expect(devA).toHaveClass('tag', 'green');
    expect(devB).toHaveClass('tag', 'green');

    // Publisher tag
    const pubA = screen.getByText('Pub A');
    expect(pubA).toHaveClass('tag', 'green');

    // Platform tags
    const pcTag = screen.getByText('PC');
    const swTag = screen.getByText('Switch');
    expect(pcTag).toHaveClass('tag', 'green');
    expect(swTag).toHaveClass('tag', 'red');
  });
});
