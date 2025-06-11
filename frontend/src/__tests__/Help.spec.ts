import { render, fireEvent, screen } from '@testing-library/svelte';
import Help from '../Help.svelte';
import { vi } from 'vitest';

describe('Help.svelte', () => {
  it('does not render help content when show is false', () => {
    render(Help, { props: { show: false, user: null } });
    // The header should not be in the document
    expect(
      screen.queryByText('How to use GameGuesser')
    ).not.toBeInTheDocument();
    // And the overlay should not be present
    expect(
      screen.queryByTestId('help-overlay')
    ).not.toBeInTheDocument();
  });

  it('displays the overlay and help content when show is true', () => {
    const { getByText } = render(Help, { props: { show: true, user: { username: 'Alex' } } });
    // Header
    expect(getByText('How to use GameGuesser')).toBeInTheDocument();
    // Body text
    expect(getByText('This is a small game to guess the game!')).toBeInTheDocument();
    expect(getByText('You have 10 chances (default) to guess the correct game.')).toBeInTheDocument();
  });

  it('emits close when the × button is clicked', async () => {
    const { getByText, component } = render(Help, { props: { show: true } });
    const closePromise = new Promise(resolve => component.$on('close', resolve));
    await fireEvent.click(getByText('×'));
    await expect(closePromise).resolves.toBeDefined();
  });

  it('emits close when clicking on the overlay background', async () => {
    const { container, component } = render(Help, { props: { show: true } });
    const overlay = container.querySelector('.tutorials-overlay')!;
    const closePromise = new Promise(resolve => component.$on('close', resolve));
    await fireEvent.click(overlay);
    await expect(closePromise).resolves.toBeDefined();
  });

  it('does not emit close when clicking inside the content area', async () => {
    const { getByText, component } = render(Help, { props: { show: true } });
    const paragraph = getByText('This is a small game to guess the game!');
    const onClose = vi.fn();
    component.$on('close', onClose);
    await fireEvent.click(paragraph);
    expect(onClose).not.toHaveBeenCalled();
  });
});
