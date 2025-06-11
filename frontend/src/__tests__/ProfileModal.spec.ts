import { render, fireEvent, screen } from '@testing-library/svelte';
import ProfileModal from '../ProfileModal.svelte';
import { vi } from 'vitest';
import type { User, UserStats } from '../types';

describe('ProfileModal.svelte', () => {
  beforeEach(() => {
    // Stub fetch so logout() won’t error
    vi.stubGlobal('fetch', vi.fn(() =>
      Promise.resolve({ ok: true, json: async () => ({}) })
    ));
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('does not render content when isVisible is false', () => {
    render(ProfileModal, { props: { isVisible: false, user: null, stats: null } });
    expect(screen.queryByText('User Profile')).toBeNull();
  });

  it('shows placeholder when user is null', () => {
    render(ProfileModal, { props: { isVisible: true, user: null, stats: null } });
    expect(screen.getByText('No user information available')).toBeInTheDocument();
  });

  it('renders user details and hides stats when stats is null', () => {
    const mockUser: User = { username: 'Alice', email: 'alice@example.com' };
    render(ProfileModal, { props: { isVisible: true, user: mockUser, stats: null } });
    expect(screen.getByText('Alice')).toBeInTheDocument();
    expect(screen.getByText('alice@example.com')).toBeInTheDocument();
    // stats section should not render any stats text
    expect(screen.queryByText(/games won/i)).toBeNull();
  });

  it('renders statistics cards when stats provided', () => {
    const mockUser: User = { username: 'Alice', email: 'alice@example.com' };
    const mockStats: UserStats = {
      total_games: 4,
      games_won: 2,
      total_attempts: 20,
      best_attempts: 3,
      win_rate: 50
    };
    render(ProfileModal, { props: { isVisible: true, user: mockUser, stats: mockStats } });
    expect(screen.getByText('Game Statistics')).toBeInTheDocument();
    expect(screen.getByText('2 / 4 games won')).toBeInTheDocument();
    expect(screen.getByText('Avg. Attempts')).toBeInTheDocument();
  });

  it('emits close event when close button is clicked', async () => {
    const mockUser: User = { username: 'Alice', email: 'a@example.com' };
    const mockStats: UserStats = {
      total_games: 1,
      games_won: 1,
      total_attempts: 1,
      best_attempts: 1,
      win_rate: 100
    };
    const { component } = render(ProfileModal, { props: { isVisible: true, user: mockUser, stats: mockStats } });
    const closePromise = new Promise(resolve => component.$on('close', resolve));
    await fireEvent.click(screen.getByRole('button', { name: '×' }));
    await expect(closePromise).resolves.toBeDefined();
  });

  it('emits logout event when logout button is clicked', async () => {
    const mockUser: User = { username: 'Alice', email: 'a@example.com' };
    const mockStats: UserStats = {
      total_games: 1,
      games_won: 1,
      total_attempts: 1,
      best_attempts: 1,
      win_rate: 100
    };
    const { component } = render(ProfileModal, { props: { isVisible: true, user: mockUser, stats: mockStats } });
    const logoutBtn = screen.getByRole('button', { name: 'Logout' });
    const logoutPromise = new Promise(resolve => component.$on('logout', resolve));
    await fireEvent.click(logoutBtn);
    await expect(logoutPromise).resolves.toBeDefined();
  });

  it('does not emit close when clicking inside modal content', async () => {
    const mockUser: User = { username: 'Alice', email: 'a@example.com' };
    const mockStats: UserStats = {
      total_games: 1,
      games_won: 1,
      total_attempts: 1,
      best_attempts: 1,
      win_rate: 100
    };
    const { component } = render(ProfileModal, { props: { isVisible: true, user: mockUser, stats: mockStats } });
    const onClose = vi.fn();
    component.$on('close', onClose);
    await fireEvent.click(screen.getByText('User Profile'));
    expect(onClose).not.toHaveBeenCalled();
  });
});
