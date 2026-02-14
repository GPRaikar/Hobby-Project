# Indian Personal Finance Management App

A comprehensive personal finance management application combining **Rich Dad, Poor Dad** principles (Assets/Liabilities/Passive Income) with **Indian Tax Planning** (80C, 80D, New vs Old Regime). Built with FastAPI backend and Flutter frontend, using only **open-source and free-tier tools**.

## 🎯 Features

### Rich Dad Dashboard
- Track **Active Income** vs **Passive Income**
- Monitor **Assets** vs **Liabilities**
- Calculate **Financial Freedom Ratio** (Passive Income / Total Expenses × 100)
- Analyze **Cash Flow** and **Savings Rate**
- Visualize **Net Worth** over time

### Transaction Management
- Add income and expenses manually
- Import from SMS (HDFC, SBI, ICICI, Axis, Kotak)
- Scan receipts with OCR (Google ML Kit)
- Categorize with Rich Dad principles
- Track recurring transactions

### Investment Tracking
- Support for PPF, ELSS, NPS, FD, Mutual Funds, Stocks, Real Estate, Gold, LIC, NSC
- Real-time stock prices via yfinance (15-min delayed, free)
- Track tax-saving investments (80C, 80D)
- Monitor passive income generation
- Calculate returns and maturity dates

### Indian Tax Planning
- **Section 80C**: Track up to ₹1,50,000 deductions
- **Section 80D**: Health insurance deductions
- **New vs Old Regime**: Compare and recommend best option
- FY 2025-26 tax slabs with rebate 87A
- Estimate tax savings

### Budget Management
- Set monthly spending limits by category
- Track actual vs budgeted expenses
- Get overspending alerts
- Analyze spending patterns

### SMS Auto-Import
- Read bank SMS using `flutter_sms_inbox`
- Parse transactions with regex patterns
- Extract: amount, merchant, date, reference number
- On-device, private, and free

### OCR Receipt Scanning
- Capture receipts with camera
- Extract amount and merchant using Google ML Kit
- Auto-fill transaction forms
- On-device OCR, zero cost

## 🛠️ Tech Stack

| Layer | Technology | Why? |
|-------|-----------|------|
| **Frontend** | Flutter (Mobile) | Cross-platform, free, native performance |
| **Backend** | FastAPI (Python) | Fast, modern, easy to deploy |
| **Database** | PostgreSQL | Free, robust, production-ready |
| **SMS Reading** | `flutter_sms_inbox` | On-device, offline, private |
| **OCR** | Google ML Kit | On-device, zero API costs |
| **Market Data** | yfinance | Free, 15-min delayed acceptable |
| **Authentication** | JWT + bcrypt | Secure, stateless |
| **State Management** | Provider | Simple, official recommendation |
| **Charts** | FL Chart | Free, beautiful Flutter charts |

**Total Cost: ₹0** (excluding VPS hosting if self-hosted)

## 📁 Project Structure

```
Hobby-Project/
├── backend/                # FastAPI Backend
│   ├── app/
│   │   ├── models/        # SQLAlchemy models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── routers/       # API endpoints
│   │   ├── services/      # Business logic
│   │   └── utils/         # Helpers and constants
│   ├── alembic/           # Database migrations
│   ├── tests/             # pytest tests
│   ├── requirements.txt
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── frontend/              # Flutter App
│   ├── lib/
│   │   ├── models/        # Data models
│   │   ├── services/      # API & device services
│   │   ├── providers/     # State management
│   │   ├── screens/       # UI screens
│   │   ├── widgets/       # Reusable widgets
│   │   └── config/        # Configuration
│   ├── android/
│   ├── ios/
│   └── pubspec.yaml
│
└── README.md             # This file
```

## 🚀 Quick Start

### Prerequisites

- **Backend**: Python 3.11+, PostgreSQL 15+
- **Frontend**: Flutter 3.0+, Android Studio / Xcode
- **Optional**: Docker & Docker Compose

### Backend Setup

See [backend/README.md](backend/README.md) for detailed instructions.

Quick start:
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your settings
alembic upgrade head
uvicorn app.main:app --reload
```

API Documentation: http://localhost:8000/docs

### Frontend Setup

```bash
cd frontend
flutter pub get
# Update API URL in lib/config/api_config.dart
flutter run
```

### Docker Deployment (Easiest)

```bash
cd backend
docker-compose up -d
```

## 📱 Screenshots

_Coming soon_

## 🧪 Testing

### Backend
```bash
cd backend
pytest
pytest --cov=app --cov-report=html
```

### Frontend
```bash
cd frontend
flutter test
```

## 📊 Rich Dad Financial Metrics

- **Financial Freedom Ratio**: (Passive Income / Total Expenses) × 100 — Goal is 100%+
- **Cash Flow**: Total Income - Total Expenses
- **Savings Rate**: ((Total Income - Total Expenses) / Total Income) × 100
- **Net Worth**: Total Assets - Total Liabilities

## 🔐 Security

- Passwords hashed with bcrypt
- JWT tokens for authentication  
- Secure storage for tokens
- HTTPS recommended for production
- All sensitive data encrypted

## 🤝 Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

1. Fork the repository
2. Create a feature branch
3. Make changes and add tests
4. Submit a Pull Request

## 📄 License

MIT License - See [LICENSE](LICENSE) file

## ⚠️ Disclaimer

This app is for personal finance management and educational purposes. Tax calculations are estimates. Always consult a qualified Chartered Accountant for tax filing.

---

**Made with ❤️ for the Indian Personal Finance Community**

**Zero Cost | Open Source | Privacy First**