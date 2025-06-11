import { render, fireEvent, waitFor } from '@testing-library/svelte';
import Settings from '../Settings.svelte';
import { filters } from '../stores/filterStore';
import { vi } from 'vitest';

describe('Settings.svelte', () => {
  const defaultFilters = {
    yearStart: 1981,
    yearEnd: new Date().getFullYear(),
    platforms: [
      'PC','Mac','Linux','iOS','Android',
      'PlayStation 1','PlayStation 2','PlayStation 3','PlayStation 4','PlayStation 5',
      'PlayStation Portable (PSP)','PlayStation Vita',
      'Xbox','Xbox 360','Xbox One','Xbox Series X',
      'Nintendo Entertainment System (NES)','Super Nintendo (SNES)','Nintendo 64','GameCube',
      'Wii','Wii U','Nintendo Switch',
      'Game Boy','Game Boy Advance','Nintendo DS','Nintendo 3DS',
      'Arcade','Dreamcast'
    ],
    genres: [
      'Action','Adventure','Role-playing (RPG)','Shooter','Platform','Puzzle','Racing','Sports','Strategy','Simulation',
      'Fighting','Stealth','Survival','Sandbox','Pinball','Educational','Indie','Arcade','Family','Music'
    ],
    topTier: null,
    attempts: 10
  };

  beforeEach(() => {
    vi.spyOn(filters, 'subscribe').mockImplementation((run) => {
      run(defaultFilters as any);
      return () => {};
    });
    vi.spyOn(filters, 'set').mockImplementation(vi.fn());
    vi.stubGlobal('fetch', vi.fn());
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  test('renders the settings container', () => {
    const { container } = render(Settings);
    expect(container).toBeTruthy();
  });

  test('clicking the close button dispatches a close event', async () => {
    const { component, getByText } = render(Settings);
    const onClose = vi.fn();
    component.$on('close', onClose);

    const closeBtn = getByText('×');
    await fireEvent.click(closeBtn);
    expect(onClose).toHaveBeenCalled();
  });

  test('fetch returning 404 displays error message and does not call filters.set', async () => {
    (fetch as unknown as vi.Mock).mockResolvedValue({ ok: false, status: 404 });

    const { getByText, container } = render(Settings);
    const attemptsInput = container.querySelector('.attempts-input') as HTMLInputElement;
    await fireEvent.change(attemptsInput, { target: { value: '2' } });

    const applyBtn = getByText('Apply Settings');
    await fireEvent.click(applyBtn);

    await waitFor(() => {
      expect(getByText('No games found with current filters, please adjust settings')).toBeInTheDocument();
    });
    expect(filters.set).not.toHaveBeenCalled();
  });

  test('year-end blur clamps above MAX_YEAR to current year', async () => {
    const { container } = render(Settings);
    const yearInputs = container.querySelectorAll('.year-input') as NodeListOf<HTMLInputElement>;
    const endInput = yearInputs[1];

    await fireEvent.input(endInput, { target: { value: '3000' } });
    await fireEvent.blur(endInput);

    expect(endInput.value).toBe(`${new Date().getFullYear()}`);
  });

  test('year-end blur clamps below start year to start year', async () => {
    const { container } = render(Settings);
    const yearInputs = container.querySelectorAll('.year-input') as NodeListOf<HTMLInputElement>;
    const startInput = yearInputs[0];
    const endInput = yearInputs[1];

    await fireEvent.input(startInput, { target: { value: '2000' } });
    await fireEvent.input(endInput, { target: { value: '1990' } });
    await fireEvent.blur(endInput);

    expect(endInput.value).toBe('2000');
  });

  test('attempts input clamps below 1 to 1 and above 999 to 999', async () => {
    const { container } = render(Settings);
    const input = container.querySelector('.attempts-input') as HTMLInputElement;

    await fireEvent.change(input, { target: { value: '0' } });
    expect(input.value).toBe('1');

    await fireEvent.change(input, { target: { value: '1000' } });
    expect(input.value).toBe('999');
  });
});
