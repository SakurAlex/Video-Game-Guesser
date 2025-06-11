import '@testing-library/jest-dom';
import { vi } from 'vitest';

// Mock fetch globally
global.fetch = vi.fn();

// Mock localStorage
const localStorageMock = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  clear: vi.fn(),
  removeItem: vi.fn(),
  length: 0,
  key: vi.fn(),
};

global.localStorage = localStorageMock as Storage;

// Mock window.alert
global.alert = vi.fn();

// Mock window.confirm
global.confirm = vi.fn();

// Clean up after each test
afterEach(() => {
  vi.clearAllMocks();
}); 