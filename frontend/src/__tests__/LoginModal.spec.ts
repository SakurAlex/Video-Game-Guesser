import { render, fireEvent, screen, waitFor } from '@testing-library/svelte';
import LoginModal from '../LoginModal.svelte';
import { vi } from 'vitest';
import type { User } from '../types';

describe('LoginModal.svelte', () => {
  beforeEach(() => {
    // Stub fetch globally
    vi.stubGlobal('fetch', vi.fn());
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('does not render the form when isVisible is false', () => {
    const { container } = render(LoginModal, { props: { isVisible: false } });

    // No form in DOM
    expect(container.querySelector('form')).toBeNull();
  });

  it('renders login inputs when visible', () => {
    render(LoginModal, { props: { isVisible: true } });

    // Header
    expect(screen.getByRole('heading', { name: 'Login' })).toBeInTheDocument();

    // Login fields
    expect(screen.getByLabelText('Username')).toBeInTheDocument();
    expect(screen.getByLabelText('Password')).toBeInTheDocument();

    // Should not show register‐only fields
    expect(screen.queryByLabelText('Email')).toBeNull();
    expect(screen.queryByLabelText('Confirm Password')).toBeNull();
  });

  it('toggles to registration mode when switch button clicked', async () => {
    render(LoginModal, { props: { isVisible: true } });

    // Click the “Register” switch button
    const switchBtn = screen.getByRole('button', { name: 'Register' });
    await fireEvent.click(switchBtn);

    // Now header should read “Register”
    expect(screen.getByRole('heading', { name: 'Register' })).toBeInTheDocument();

    // Registration fields appear
    expect(screen.getByLabelText('Email')).toBeInTheDocument();
    expect(screen.getByLabelText('Confirm Password')).toBeInTheDocument();
  });

  it('emits success event on successful login', async () => {
    const mockUser: User = { id: 1, username: 'test', email: 'test@example.com' };
    
    // Mock fetch to return OK and a user object
    (fetch as unknown as ReturnType<typeof vi.fn>).mockResolvedValue({
      ok: true,
      json: async () => ({ user: mockUser })
    });

    const { component } = render(LoginModal, { props: { isVisible: true } });

    // Fill in login form
    await fireEvent.input(screen.getByLabelText('Username'), { target: { value: 'test' } });
    await fireEvent.input(screen.getByLabelText('Password'), { target: { value: 'secret' } });

    // Listen for the success event and grab its detail
    const successPromise = new Promise<User>(resolve =>
      component.$on('success', (e: CustomEvent<User>) => resolve(e.detail))
    );

    // Submit the form (click the Login button)
    await fireEvent.click(screen.getByRole('button', { name: 'Login' }));

    // Wait for the success event payload
    const user = await successPromise;
    expect(user).toEqual(mockUser);
  });
});
