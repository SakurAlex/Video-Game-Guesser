<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import type { User } from './types';

  export let isVisible = false;
  
  let isLogin = true;
  let username = '';
  let email = '';
  let password = '';
  let confirmPassword = '';
  let loading = false;
  let error = '';
  let success = '';

  const dispatch = createEventDispatcher<{
    close: void;
    success: User;
  }>();
  const API_BASE_URL = "http://localhost:8000/api";

  function switchMode() {
    isLogin = !isLogin;
    clearForm();
  }

  function clearForm() {
    username = '';
    email = '';
    password = '';
    confirmPassword = '';
    error = '';
    success = '';
  }

  function validateForm() {
    if (!username.trim()) {
      error = 'Username is required';
      return false;
    }
    
    if (username.length < 3) {
      error = 'Username must be at least 3 characters long';
      return false;
    }

    if (!isLogin && !email.trim()) {
      error = 'Email is required';
      return false;
    }

    if (!password) {
      error = 'Password is required';
      return false;
    }

    if (password.length < 6) {
      error = 'Password must be at least 6 characters long';
      return false;
    }

    if (!isLogin && password !== confirmPassword) {
      error = 'Passwords do not match';
      return false;
    }

    return true;
  }

  async function handleSubmit() {
    error = '';
    success = '';

    if (!validateForm()) {
      return;
    }

    loading = true;

    try {
      const endpoint = isLogin ? '/auth/login' : '/auth/register';
      const payload = isLogin 
        ? { username: username.trim(), password }
        : { username: username.trim(), email: email.trim(), password };

      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify(payload)
      });

      const data = await response.json();

      if (response.ok) {
        success = data.message;
        dispatch('success', data.user);
        setTimeout(() => {
          close();
        }, 1000);
      } else {
        error = data.error || 'An error occurred';
      }
    } catch (err) {
      error = 'Network error. Please check if the backend is running.';
      console.error('Auth error:', err);
    } finally {
      loading = false;
    }
  }

  function close() {
    isVisible = false;
    clearForm();
    dispatch('close');
  }

  function handleOverlayClick(event: MouseEvent) {
    if (event.target === event.currentTarget) {
      close();
    }
  }

  function handleKeydown(event: KeyboardEvent) {
    if (event.key === 'Escape') {
      close();
    } else if (event.key === 'Enter') {
      handleSubmit();
    }
  }
</script>

{#if isVisible}
  <div class="overlay" on:click={handleOverlayClick} on:keydown={handleKeydown}>
    <div class="auth-modal">
      <div class="auth-header">
        <h2>{isLogin ? 'Login' : 'Register'}</h2>
        <button class="close-button" on:click={close}>&times;</button>
      </div>

      <div class="auth-body">
        <form on:submit|preventDefault={handleSubmit}>
          <div class="form-group">
            <label for="username">Username</label>
            <input
              id="username"
              type="text"
              bind:value={username}
              placeholder="Enter your username"
              required
              disabled={loading}
            />
          </div>

          {#if !isLogin}
            <div class="form-group">
              <label for="email">Email</label>
              <input
                id="email"
                type="email"
                bind:value={email}
                placeholder="Enter your email"
                required
                disabled={loading}
              />
            </div>
          {/if}

          <div class="form-group">
            <label for="password">Password</label>
            <input
              id="password"
              type="password"
              bind:value={password}
              placeholder="Enter your password"
              required
              disabled={loading}
            />
          </div>

          {#if !isLogin}
            <div class="form-group">
              <label for="confirmPassword">Confirm Password</label>
              <input
                id="confirmPassword"
                type="password"
                bind:value={confirmPassword}
                placeholder="Confirm your password"
                required
                disabled={loading}
              />
            </div>
          {/if}

          {#if error}
            <div class="error-message">{error}</div>
          {/if}

          {#if success}
            <div class="success-message">{success}</div>
          {/if}

          <button 
            type="submit" 
            class="auth-button" 
            disabled={loading}
          >
            {#if loading}
              <div class="loading-spinner"></div>
              {isLogin ? 'Logging in...' : 'Registering...'}
            {:else}
              {isLogin ? 'Login' : 'Register'}
            {/if}
          </button>
        </form>

        <div class="auth-switch">
          <p>
            {isLogin ? "Don't have an account?" : "Already have an account?"}
            <button type="button" class="switch-button" on:click={switchMode}>
              {isLogin ? 'Register' : 'Login'}
            </button>
          </p>
        </div>
      </div>
    </div>
  </div>
{/if}

<style>
  .overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.6);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }

  .auth-modal {
    background: white;
    border-radius: 16px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    width: 100%;
    max-width: 400px;
    margin: 20px;
  }

  .auth-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 24px 0 24px;
    border-bottom: 1px solid #e5e5e5;
    margin-bottom: 20px;
  }

  .auth-header h2 {
    margin: 0;
    font-size: 24px;
    font-weight: 700;
    color: #2c3e50;
  }

  .close-button {
    background: none;
    border: none;
    font-size: 28px;
    color: #9ca3ab;
    cursor: pointer;
    padding: 0;
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: background-color 0.2s ease;
  }

  .close-button:hover {
    background-color: #f5f5f5;
  }

  .auth-body {
    padding: 0 24px 24px 24px;
  }

  .form-group {
    margin-bottom: 16px;
  }

  .form-group label {
    display: block;
    margin-bottom: 6px;
    font-weight: 600;
    color: #2c3e50;
    font-size: 14px;
  }

  .form-group input {
    width: 100%;
    padding: 12px 16px;
    border: 2px solid #e1e5e9;
    border-radius: 8px;
    font-size: 16px;
    transition: border-color 0.2s ease;
    box-sizing: border-box;
  }

  .form-group input:focus {
    outline: none;
    border-color: #b9dbf3;
  }

  .form-group input:disabled {
    background-color: #f5f5f5;
    cursor: not-allowed;
  }

  .error-message {
    background-color: #fee;
    color: #c33;
    padding: 12px;
    border-radius: 8px;
    margin-bottom: 16px;
    font-size: 14px;
    border: 1px solid #fcc;
  }

  .success-message {
    background-color: #efe;
    color: #363;
    padding: 12px;
    border-radius: 8px;
    margin-bottom: 16px;
    font-size: 14px;
    border: 1px solid #cfc;
  }

  .auth-button {
    width: 100%;
    background-color: #b9dbf3;
    color: #2c3e50;
    border: none;
    padding: 14px;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
  }

  .auth-button:hover:not(:disabled) {
    background-color: #a5d0e8;
  }

  .auth-button:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }

  .loading-spinner {
    width: 16px;
    height: 16px;
    border: 2px solid #e1e5e9;
    border-top: 2px solid #2c3e50;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  .auth-switch {
    margin-top: 20px;
    text-align: center;
    padding-top: 16px;
    border-top: 1px solid #e5e5e5;
  }

  .auth-switch p {
    margin: 0;
    color: #666;
    font-size: 14px;
  }

  .switch-button {
    background: none;
    border: none;
    color: #b9dbf3;
    cursor: pointer;
    font-weight: 600;
    text-decoration: underline;
    font-size: 14px;
    margin-left: 4px;
  }

  .switch-button:hover {
    color: #a5d0e8;
  }

  @media (max-width: 480px) {
    .auth-modal {
      margin: 10px;
    }

    .auth-header {
      padding: 16px 20px 0 20px;
    }

    .auth-body {
      padding: 0 20px 20px 20px;
    }

    .auth-header h2 {
      font-size: 20px;
    }
  }
</style>
