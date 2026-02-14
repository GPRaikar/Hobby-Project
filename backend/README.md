# Indian Personal Finance Management App - Backend

A comprehensive FastAPI backend for managing personal finances with Rich Dad principles and Indian tax planning.

## Features

- **User Authentication**: JWT-based authentication with secure password hashing
- **Transaction Management**: Track income and expenses with Rich Dad categorization
- **Investment Tracking**: Monitor investments with tax-saving classifications (80C, 80D, etc.)
- **Budget Management**: Set and track monthly spending limits by category
- **Tax Planning**: Calculate taxes under both Old and New regimes, Section 80C/80D utilization
- **Rich Dad Dashboard**: Track active/passive income, assets/liabilities, financial freedom ratio
- **SMS Parser**: Extract transaction details from Indian bank SMS (HDFC, SBI, ICICI, Axis, Kotak)
- **Market Data**: Fetch stock prices using yfinance (free, 15-min delayed data)

## Tech Stack

- **Framework**: FastAPI 0.109
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT with python-jose, bcrypt password hashing
- **Migrations**: Alembic
- **Market Data**: yfinance (free tier)
- **Testing**: pytest with httpx

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI application entry point
│   ├── config.py                # Configuration and settings
│   ├── database.py              # Database connection and session
│   ├── models/                  # SQLAlchemy models
│   │   ├── user.py
│   │   ├── transaction.py
│   │   ├── investment.py
│   │   ├── budget.py
│   │   └── tax_deduction.py
│   ├── schemas/                 # Pydantic schemas
│   │   ├── user.py
│   │   ├── transaction.py
│   │   ├── investment.py
│   │   ├── budget.py
│   │   ├── tax.py
│   │   └── dashboard.py
│   ├── routers/                 # API endpoints
│   │   ├── auth.py              # Registration, login
│   │   ├── transactions.py      # Transaction CRUD
│   │   ├── investments.py       # Investment CRUD
│   │   ├── budget.py            # Budget management
│   │   ├── tax.py               # Tax calculations
│   │   ├── dashboard.py         # Dashboard data
│   │   ├── sms_parser.py        # SMS parsing
│   │   └── market_data.py       # Stock/MF data
│   ├── services/                # Business logic
│   │   ├── auth_service.py      # Authentication logic
│   │   ├── tax_calculator.py    # Tax calculations
│   │   ├── sms_parser.py        # SMS parsing logic
│   │   ├── market_data.py       # yfinance integration
│   │   └── dashboard_service.py # Dashboard calculations
│   └── utils/
│       ├── constants.py         # Tax limits, patterns
│       └── dependencies.py      # FastAPI dependencies
├── alembic/                     # Database migrations
│   ├── env.py
│   └── versions/
├── tests/                       # Test suite
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_sms_parser.py
│   └── test_tax.py
├── requirements.txt
├── .env.example
├── Dockerfile
└── docker-compose.yml
```

## Prerequisites

- Python 3.11+
- PostgreSQL 15+
- pip

## Setup Instructions

### 1. Clone the Repository

```bash
cd backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

```bash
cp .env.example .env
# Edit .env with your configuration
```

**Important**: Generate a secure SECRET_KEY:
```bash
openssl rand -hex 32
```

### 5. Set Up Database

**Option A: Using Docker Compose (Recommended)**

```bash
docker-compose up -d
```

This will start both PostgreSQL and the backend service.

**Option B: Local PostgreSQL**

1. Install PostgreSQL locally
2. Create database:
```bash
createdb financedb
createuser financeuser
psql -c "ALTER USER financeuser WITH PASSWORD 'financepass';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE financedb TO financeuser;"
```

### 6. Run Database Migrations

```bash
alembic upgrade head
```

### 7. Run the Application

**Development Mode:**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Using Docker Compose:**
```bash
docker-compose up
```

The API will be available at:
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Documentation

Once running, visit http://localhost:8000/docs for interactive API documentation.

### Key Endpoints

#### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT tokens
- `GET /auth/me` - Get current user info

#### Transactions
- `POST /transactions/` - Create transaction
- `GET /transactions/` - List transactions with filters
- `GET /transactions/{id}` - Get specific transaction
- `PUT /transactions/{id}` - Update transaction
- `DELETE /transactions/{id}` - Delete transaction

#### Investments
- `POST /investments/` - Create investment
- `GET /investments/` - List investments
- `GET /investments/{id}` - Get specific investment
- `PUT /investments/{id}` - Update investment
- `DELETE /investments/{id}` - Delete investment

#### Budget
- `POST /budgets/` - Create budget
- `GET /budgets/` - List budgets with spending info
- `GET /budgets/{id}` - Get specific budget
- `PUT /budgets/{id}` - Update budget
- `DELETE /budgets/{id}` - Delete budget

#### Tax Planning
- `GET /tax/section-80c` - Get Section 80C utilization
- `GET /tax/section-80d` - Get Section 80D utilization
- `POST /tax/calculate` - Calculate tax for given income
- `GET /tax/compare` - Compare New vs Old regime

#### Dashboard
- `GET /dashboard/` - Get Rich Dad dashboard data

#### SMS Parser
- `POST /sms/parse` - Parse single SMS
- `POST /sms/parse-bulk` - Parse multiple SMS

#### Market Data
- `GET /market/stock/{ticker}` - Get stock price (NSE/BSE)
- `GET /market/mutual-fund/{code}` - Get mutual fund NAV

## Database Migrations

### Create a New Migration

```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply Migrations

```bash
alembic upgrade head
```

### Rollback Migration

```bash
alembic downgrade -1
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| DATABASE_URL | PostgreSQL connection string | postgresql://financeuser:financepass@localhost:5432/financedb |
| SECRET_KEY | JWT secret key (generate with openssl) | - |
| JWT_ALGORITHM | JWT algorithm | HS256 |
| ACCESS_TOKEN_EXPIRE_MINUTES | Access token expiration | 30 |
| REFRESH_TOKEN_EXPIRE_DAYS | Refresh token expiration | 7 |
| APP_NAME | Application name | Indian Personal Finance App |
| DEBUG | Debug mode | True |
| ALLOWED_ORIGINS | CORS allowed origins | http://localhost:3000,http://localhost:8080 |

## Tax Calculation Logic

### New Regime (FY 2025-26)
- Up to ₹3,00,000: Nil
- ₹3,00,001 - ₹7,00,000: 5%
- ₹7,00,001 - ₹10,00,000: 10%
- ₹10,00,001 - ₹12,00,000: 15%
- ₹12,00,001 - ₹15,00,000: 20%
- Above ₹15,00,000: 30%
- Standard Deduction: ₹75,000
- Rebate 87A: Full rebate if income ≤ ₹7,00,000

### Old Regime
- Up to ₹2,50,000: Nil
- ₹2,50,001 - ₹5,00,000: 5%
- ₹5,00,001 - ₹10,00,000: 20%
- Above ₹10,00,000: 30%
- Rebate 87A: Full rebate if income ≤ ₹5,00,000

### Section 80C
- Maximum deduction: ₹1,50,000
- Eligible: PPF, ELSS, NPS, NSC, LIC, Tuition Fees, Home Loan Principal

### Section 80D
- Individual: ₹25,000 (₹50,000 for senior citizens)
- Parents: ₹25,000 (₹50,000 for senior citizens)

## SMS Parser Patterns

Supports SMS from:
- HDFC Bank
- SBI
- ICICI Bank
- Axis Bank
- Kotak Mahindra Bank
- Credit Cards

Extracts: amount, transaction type, account number, merchant, date, reference number, balance

## Rich Dad Dashboard Metrics

1. **Active Income**: Salary, freelance income
2. **Passive Income**: Dividends, rental income, interest
3. **Assets**: Investments that generate income
4. **Liabilities**: Investments that cost money
5. **Financial Freedom Ratio**: (Passive Income / Total Expenses) × 100
6. **Cash Flow**: Total Income - Total Expenses
7. **Savings Rate**: ((Income - Expenses) / Income) × 100

## Docker Deployment

### Build and Run

```bash
docker-compose up --build
```

### Stop Services

```bash
docker-compose down
```

### View Logs

```bash
docker-compose logs -f backend
```

## Troubleshooting

### Database Connection Issues

1. Check PostgreSQL is running: `pg_isready`
2. Verify credentials in `.env`
3. Ensure database exists: `psql -l`

### Migration Issues

1. Check database connection
2. Reset migrations: `alembic downgrade base`
3. Re-run: `alembic upgrade head`

### Import Errors

Ensure you're in the virtual environment and dependencies are installed:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Contributing

1. Create a feature branch
2. Make changes
3. Add tests
4. Run tests: `pytest`
5. Submit pull request

## License

MIT License

## Security Notes

- Never commit `.env` file with real credentials
- Always use strong SECRET_KEY in production
- Use HTTPS in production
- Encrypt sensitive data (PAN numbers) in production
- Implement rate limiting for production
- Regular security audits recommended

## Support

For issues and questions, please create an issue in the GitHub repository.
