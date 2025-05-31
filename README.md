# GameGuesser

A game guessing application built with Svelte frontend and Flask backend.

## 🚀 Features

- Modern Svelte frontend with TypeScript
- Flask backend API
- Docker containerization
- Responsive design
- Health check endpoints

## 🛠️ Tech Stack

### Frontend
- **Svelte** - Modern reactive framework
- **TypeScript** - Type safety
- **Vite** - Fast build tool
- **Nginx** - Production server

### Backend
- **Flask** - Python web framework
- **Flask-CORS** - Cross-origin resource sharing
- **Python 3.11** - Latest Python features

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

## 📦 Project Structure

```
GameGuess/
├── frontend/           # Svelte frontend application
│   ├── src/
│   ├── Dockerfile
│   ├── nginx.conf
│   └── package.json
├── backend/            # Flask backend API
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml  # Docker orchestration
└── README.md
```

## 🚀 Quick Start

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/SakurAlex/Game-Guesser.git
cd Game-Guesser
```

2. Start the application:
```bash
docker-compose up --build
```

3. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

### Development Setup

#### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

#### Backend Development
```bash
cd backend
pip install -r requirements.txt
python app.py
```

## 📋 API Endpoints

- `GET /api/health` - Health check endpoint
- `GET /api/key` - API key status

## 🐳 Docker Commands

```bash
# Build and start services
docker-compose up --build

# Stop services
docker-compose down

# View logs
docker-compose logs

# Rebuild specific service
docker-compose build frontend
docker-compose build backend
```

## 🔧 Development

### Frontend
The frontend is built with Svelte and TypeScript. It features:
- Component-based architecture
- Responsive design
- Modern CSS with mobile-first approach
- Hot reload during development

### Backend
The backend provides REST API endpoints using Flask:
- Health monitoring
- CORS enabled for frontend communication
- Environment-based configuration

## 📝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🤝 Support

If you have any questions or need help, please open an issue on GitHub. 