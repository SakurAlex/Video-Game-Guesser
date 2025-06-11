# Video Game Guesser Tests
Video Game Gueser incorporate both frontend test and backend test
## Backend Tests

Located in `backend/test_app.py`. Uses pytest framework to test Flask endpoints and utilities.

### Backend Tests
```bash
pip install pytest requests flask
cd backend
pytest test_app.py -v
```

### Test Coverage
- Authentication (register, login, logout)
- Game search and details
- User statistics
- API health checks
- Data processing functions
- Error handling

## Frontend Tests

Located in `frontend/src/__tests__/*.spec.ts`. Uses Vitest with Testing Library for Svelte components.

### Setup
```bash
cd frontend
npm install
npm run test
```

### Test Coverage
- App.spec.ts - Main application flow
- GameTable.spec.ts - Game table component
- GameStatus.spec.ts - Game status display
- SearchBar.spec.ts - Search functionality
- LoginModal.spec.ts - Authentication UI
- Result.spec.ts - Game result display
- Help.spec.ts - Help modal
- ProfileModal.spec.ts - User profile
- NavigationBar.spec.ts - Navigation
- Settings.spec.ts - Game settings 