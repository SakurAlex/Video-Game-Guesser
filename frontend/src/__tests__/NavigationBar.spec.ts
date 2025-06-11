import { render, fireEvent, screen } from '@testing-library/svelte';
import NavigationBar from '../NavigationBar.svelte';
import { vi } from 'vitest';

describe('NavigationBar.svelte', () => {
  it('renders all nav icons and Login button when user is null', () => {
    render(NavigationBar, { props: { user: null } });

    // Gear/settings icon
    expect(screen.getByAltText('settings')).toBeInTheDocument();
    // Home icon
    expect(screen.getByAltText('home')).toBeInTheDocument();
    // Help/tutorials icon
    expect(screen.getByAltText('help')).toBeInTheDocument();
    // GitHub icon
    expect(screen.getByAltText('github')).toBeInTheDocument();
    // Login text
    expect(screen.getByText('Login')).toBeInTheDocument();
  });

  it('emits showLogin when Login button is clicked', async () => {
    const { component } = render(NavigationBar, { props: { user: null } });
    const loginBtn = screen.getByText('Login');
    const promise = new Promise(resolve => component.$on('showLogin', resolve));
    await fireEvent.click(loginBtn);
    await expect(promise).resolves.toBeDefined();
  });

  it('renders user avatar when user is provided and emits showProfile on click', async () => {
    const mockUser = { username: 'Alice', avatar_url: 'alice.png' };
    const { component } = render(NavigationBar, { props: { user: mockUser }});

    // Should render the username text
    const usernameEl = screen.getByText('Alice');
    expect(usernameEl).toBeInTheDocument();

    // Clicking the username emits showProfile
    const promise = new Promise(resolve => component.$on('showProfile', resolve));
    await fireEvent.click(usernameEl);
    await expect(promise).resolves.toBeDefined();
  });
});
