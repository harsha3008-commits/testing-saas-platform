# Testing SaaS Platform

A comprehensive automated testing and code quality platform that integrates multiple testing engines, security scanners, and AI-powered fix suggestions.

## Features

### Core Functionality
- 🔍 **Multi-Engine Testing**: Support for ESLint, Pylint, PyTest, Jest, and more
- 🔒 **Security Scanning**: Integrated Snyk, Bandit, and OWASP ZAP
- 🤖 **AI-Powered Fixes**: OpenAI-powered suggestions for test failures
- 📊 **Comprehensive Reports**: Detailed test results and coverage analysis
- 🔗 **GitHub Integration**: Direct repository connection for seamless testing
- 💳 **Stripe Billing**: Flexible subscription plans

### Team Collaboration
- 👥 **Organizations**: Create teams and manage projects together
- 🔐 **Role-Based Access**: Admin, Developer, and Viewer roles
- ✉️ **Team Invitations**: Invite members via email
- 📈 **Shared Analytics**: Organization-wide test statistics

### Notifications
- 💬 **Slack Integration**: Real-time notifications to Slack channels
- 🎮 **Discord Integration**: Alert your Discord servers
- 📧 **Email Notifications**: Customizable email alerts
- 📱 **WhatsApp Support**: (Coming soon) SMS notifications

### Analytics & Insights
- 📈 **Test Trends**: Track pass/fail rates over time
- 📊 **Coverage Tracking**: Monitor code coverage improvements
- 🔍 **Failure Patterns**: Identify recurring test failures
- 📉 **Project Analytics**: Comprehensive project statistics

### CI/CD Integration
- 🔄 **GitHub Actions**: Pre-configured workflows
- 🚀 **Automated Deployment**: CI/CD pipelines included
- 🐳 **Docker Support**: Containerized deployment
- 🔐 **Security Scanning**: Automated vulnerability checks

## Tech Stack

### Frontend
- **Framework**: Next.js 15 with App Router
- **Language**: TypeScript
- **Styling**: TailwindCSS
- **UI Components**: shadcn/ui
- **Charts**: Recharts
- **State Management**: React Hooks

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **Cache**: Redis
- **Task Queue**: Celery with RabbitMQ
- **Authentication**: JWT
- **AI Integration**: OpenAI API

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **CI/CD**: GitHub Actions
- **Deployment**: Vercel (Frontend) + Custom (Backend)
- **Monitoring**: Built-in analytics

## Project Structure

```
testing-saas-platform/
├── frontend/                 # Next.js frontend application
│   ├── app/                 # App router pages
│   │   ├── dashboard/      # Main dashboard
│   │   ├── organizations/  # Team management
│   │   └── settings/       # User settings
│   ├── components/         # React components
│   └── lib/               # Utilities
│
├── backend/                # FastAPI backend
│   ├── main.py           # Application entry
│   ├── auth.py           # Authentication
│   ├── tasks.py          # Celery tasks
│   ├── engine_manager.py # Testing engines
│   ├── ai_fixes.py       # AI suggestions
│   ├── billing.py        # Stripe integration
│   ├── notifications.py  # Alert system
│   ├── analytics.py      # Analytics API
│   ├── team_collaboration.py  # Organizations
│   ├── project_handler.py     # Project management
│   └── report_generator.py    # Report generation
│
├── .github/
│   └── workflows/        # CI/CD pipelines
│       ├── frontend-ci.yml
│       ├── backend-ci.yml
│       └── docker-ci.yml
│
├── docker/               # Docker configurations
│   ├── docker-compose.yml
│   └── Dockerfile.*
│
└── docs/                # Documentation
    ├── DEPLOYMENT.md
    └── API.md
```

## Getting Started

### Prerequisites
- Node.js 20+
- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (optional)

### Environment Variables

#### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_STRIPE_PUBLIC_KEY=your_stripe_public_key
```

#### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@localhost:5432/testing_saas
REDIS_URL=redis://localhost:6379
JWT_SECRET=your_secret_key
OPENAI_API_KEY=your_openai_key
STRIPE_SECRET_KEY=your_stripe_secret_key
GITHUB_TOKEN=your_github_token

# SMTP Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
FROM_EMAIL=noreply@testingsaas.com
```

### Installation

#### Option 1: Docker (Recommended)
```bash
# Clone the repository
git clone https://github.com/yourusername/testing-saas-platform.git
cd testing-saas-platform

# Start all services
docker-compose up -d

# Run database migrations
docker-compose exec backend python -m alembic upgrade head
```

#### Option 2: Manual Setup

**Backend:**
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
psql -U postgres -d testing_saas -f schema.sql
psql -U postgres -d testing_saas -f schema_updates.sql
psql -U postgres -d testing_saas -f notification_schema.sql

# Start the backend
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

**Celery Worker:**
```bash
cd backend
celery -A tasks worker --loglevel=info
```

### Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Usage

### Creating a Project
1. Sign up and log in
2. Click "New Project" in the dashboard
3. Connect your GitHub repository or upload code
4. Configure testing preferences
5. Run your first test

### Setting Up Notifications
1. Navigate to Settings → Notifications
2. Add Slack webhook URL (get from Slack workspace settings)
3. Add Discord webhook URL (get from Discord server settings)
4. Enable email notifications
5. Choose when to receive alerts
6. Test your integrations

### Creating an Organization
1. Go to Organizations page
2. Click "Create Organization"
3. Enter organization name and billing email
4. Invite team members via email
5. Assign roles (Admin, Developer, Viewer)

### Viewing Analytics
1. Navigate to Analytics dashboard
2. Select time period (7d, 30d, 90d)
3. Filter by project
4. View trends, coverage, and failure patterns
5. Export reports as needed

## API Documentation

Full API documentation is available at `/docs` when running the backend server.

### Key Endpoints
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /projects` - List projects
- `POST /projects` - Create project
- `POST /test-runs` - Execute tests
- `GET /analytics/trends` - Get test trends
- `POST /notifications/settings` - Update notification preferences

## Deployment

### Frontend (Vercel)
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd frontend
vercel --prod
```

### Backend (Custom Server)
See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed deployment instructions.

## Testing

### Frontend Tests
```bash
cd frontend
npm test
npm run test:coverage
```

### Backend Tests
```bash
cd backend
pytest
pytest --cov=. --cov-report=html
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- Documentation: [docs/](docs/)
- Issues: [GitHub Issues](https://github.com/yourusername/testing-saas-platform/issues)
- Email: support@testingsaas.com

## Roadmap

- [ ] GitHub App integration
- [ ] GitLab support
- [ ] Bitbucket integration
- [ ] WhatsApp notifications via Twilio
- [ ] Advanced machine learning for test predictions
- [ ] Test replay functionality
- [ ] Performance benchmarking
- [ ] Mobile app
- [ ] Visual regression testing
- [ ] Load testing integration

## Acknowledgments

- Built with [Next.js](https://nextjs.org/)
- Backend powered by [FastAPI](https://fastapi.tiangolo.com/)
- UI components from [shadcn/ui](https://ui.shadcn.com/)
- Icons by [Lucide](https://lucide.dev/)

---

Made with ❤️ by the Testing SaaS Team