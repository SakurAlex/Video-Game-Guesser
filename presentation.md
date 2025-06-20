# GameGuesser: Full-Stack Video Game Guessing Application

**ECS 162 Web Programming**

---

## Introduction

### Project Overview
GameGuesser is a full-stack web game that allows user to guess the correct video game.

### Technical Stack
- **Frontend**: Svelte + TypeScript
- **Backend**: Flask (Python) + SQLite
- **External API**: IGDB (Internet Game Database)
- **Deployment**: Docker containerization

### Core Features
- User authentication and statistics tracking
- Game search with autocomplete functionality
- Interactive guessing interface with hints
- Personal performance analytics dashboard

---

## Prototype and UI/UX Design

### Design Philosophy
- **Mobile-first responsive design** using CSS flex and Flexbox
- **Component-based architecture** for consistent user interface
- **Progressive disclosure** - game information revealed incrementally

### User Flow
Registration/Login → Game Search → Guessing Interface → Results & Statistics

### Interface Components
- Clean authentication forms with validation
- Real-time search with autocomplete suggestions
- Interactive game cards with visual feedback
- Statistics dashboard with progress tracking

---

## Frontend Development

### Implementation Using Svelte and TypeScript
- Single-page application with reactive components
- Real-time game search with debounced API calls
- Dynamic user interface updates during gameplay
- Client-side routing for seamless navigation

### State Management
- Local component state for game data and user inputs
- Global authentication state management
- Browser localStorage for session persistence
- Reactive updates across all components

### API Integration
- RESTful API communication with backend
- Automatic error handling and retry logic
- Authentication token management
- Real-time search functionality

### Performance Features
- Route-based code splitting for faster loading
- Image lazy loading and asset optimization
- Responsive design for all device sizes

---

## Backend Development

### Flask RESTful API Implementation
- Authentication endpoints for user registration and login
- Game search and random game selection endpoints
- Statistics tracking for wins and losses
- Health check and monitoring endpoints

### Database Design Using SQLite
- Users table with unique usernames and hashed passwords
- User statistics table tracking games played and won
- Foreign key relationships for data integrity
- Efficient indexing for query performance

### External API Integration
- IGDB API integration using OAuth 2.0 authentication
- Automatic token refresh and caching mechanism
- Circuit breaker pattern for handling API failures
- Game data search and retrieval functionality

### Containerization with Docker
- Multi-container setup with Docker Compose
- Separate containers for frontend and backend services
- Environment-based configuration management
- Health checks and automatic restart policies

---

## Peer Feedback


