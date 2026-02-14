# Indian Finance App - Flutter Frontend

## Overview

Cross-platform mobile app for iOS and Android that provides a beautiful UI for managing personal finances with Rich Dad principles and Indian tax planning.

## Features

- 📱 **Cross-platform**: Single codebase for iOS and Android
- 🔐 **Secure Authentication**: JWT token-based with secure local storage
- 📊 **Rich Dad Dashboard**: Visual representation of financial metrics
- 💰 **Transaction Management**: Manual entry, SMS import, OCR scanning
- 📈 **Investment Tracking**: Monitor all your investments in one place
- 💳 **Budget Management**: Set limits and track spending
- 🧮 **Tax Planning**: Section 80C, 80D calculations
- 📱 **SMS Auto-Import**: Parse bank SMS automatically
- 📷 **OCR Receipt Scanning**: Capture receipts with camera
- 📉 **Charts & Visualizations**: FL Chart for beautiful graphs

## Prerequisites

- Flutter SDK 3.0 or higher
- Dart SDK 3.0 or higher
- Android Studio (for Android development)
- Xcode (for iOS development, macOS only)
- An active backend API (see backend/README.md)

## Installation

1. **Install Flutter**: Follow the official [Flutter installation guide](https://docs.flutter.dev/get-started/install)

2. **Verify installation**:
   ```bash
   flutter doctor
   ```

3. **Clone the repository**:
   ```bash
   cd frontend
   ```

4. **Install dependencies**:
   ```bash
   flutter pub get
   ```

5. **Update API Configuration**:
   - Open `lib/config/api_config.dart`
   - Update `baseUrl` to your backend API URL
   - For Android emulator: `http://10.0.2.2:8000`
   - For iOS simulator: `http://localhost:8000`
   - For real device: Use your computer's IP or deployed API URL

## Running the App

### Android

```bash
# Run on connected Android device/emulator
flutter run

# Build APK for distribution
flutter build apk --release

# Build App Bundle for Play Store
flutter build appbundle --release
```

### iOS

```bash
# Run on connected iOS device/simulator
flutter run

# Build for iOS
flutter build ios --release

# Open in Xcode for signing and deployment
open ios/Runner.xcworkspace
```

## Permissions

### Android (AndroidManifest.xml)
- `INTERNET` - API calls
- `READ_SMS` / `RECEIVE_SMS` - SMS import
- `CAMERA` - Receipt scanning
- `READ_EXTERNAL_STORAGE` / `WRITE_EXTERNAL_STORAGE` - Image handling

### iOS (Info.plist)
- `NSCameraUsageDescription` - Receipt scanning
- `NSPhotoLibraryUsageDescription` - Image picking
- `NSLocationWhenInUseUsageDescription` - Optional

## Project Structure

```
lib/
├── config/
│   ├── api_config.dart       # API endpoints and configuration
│   └── theme.dart             # App theme and styling
├── models/
│   ├── user.dart              # User model
│   ├── transaction.dart       # Transaction model
│   ├── investment.dart        # Investment model
│   ├── budget.dart            # Budget model
│   └── tax_summary.dart       # Tax calculation model
├── services/
│   ├── api_service.dart       # HTTP client
│   ├── auth_service.dart      # Authentication
│   ├── storage_service.dart   # Secure local storage
│   ├── sms_service.dart       # SMS reading
│   └── ocr_service.dart       # OCR functionality
├── providers/
│   ├── auth_provider.dart     # Auth state management
│   ├── transaction_provider.dart
│   ├── investment_provider.dart
│   ├── budget_provider.dart
│   └── dashboard_provider.dart
├── screens/
│   ├── splash_screen.dart
│   ├── auth/
│   │   ├── login_screen.dart
│   │   └── register_screen.dart
│   └── dashboard/
│       └── dashboard_screen.dart
├── widgets/
│   └── common/
└── main.dart                  # App entry point
```

## State Management

This app uses **Provider** for state management. Each feature has its own provider that manages the state and business logic.

Example usage:
```dart
// Access provider
final authProvider = Provider.of<AuthProvider>(context);

// Use provider data
if (authProvider.isAuthenticated) {
  // User is logged in
}

// Listen to changes
Consumer<TransactionProvider>(
  builder: (context, provider, child) {
    return ListView.builder(
      itemCount: provider.transactions.length,
      itemBuilder: (context, index) {
        // Build list item
      },
    );
  },
)
```

## API Integration

All API calls are centralized in service classes:

```dart
// Example: Fetching transactions
final transactionProvider = Provider.of<TransactionProvider>(context);
await transactionProvider.fetchTransactions();
```

The `ApiService` automatically:
- Adds JWT token to requests
- Handles 401 (unauthorized) errors
- Manages timeouts
- Provides consistent error handling

## SMS Import Flow

1. User taps "Import from SMS" button
2. App requests SMS permission (if not granted)
3. `SmsService` reads inbox messages
4. Filters bank-related SMS
5. User selects SMS to import
6. Backend API parses SMS text
7. Extracted data pre-fills transaction form
8. User confirms and saves

## OCR Flow

1. User taps "Scan Receipt" button
2. App requests camera permission
3. User captures receipt photo
4. Google ML Kit extracts text on-device
5. Simple regex extracts amount and merchant
6. Data pre-fills transaction form
7. User confirms and saves

## Building for Production

### Android

1. **Update version** in `pubspec.yaml`
2. **Create signing key**:
   ```bash
   keytool -genkey -v -keystore ~/android-keystore.jks -keyalg RSA -keysize 2048 -validity 10000 -alias upload
   ```

3. **Configure signing** in `android/key.properties`

4. **Build**:
   ```bash
   flutter build appbundle --release
   ```

5. **Upload to Play Store**

### iOS

1. **Update version** in `pubspec.yaml`
2. **Open in Xcode**:
   ```bash
   open ios/Runner.xcworkspace
   ```

3. **Configure signing** with your Apple Developer account

4. **Archive and upload to App Store**

## Testing

```bash
# Run all tests
flutter test

# Run with coverage
flutter test --coverage

# Generate coverage report
genhtml coverage/lcov.info -o coverage/html
open coverage/html/index.html
```

## Common Issues

### Issue: "Failed to connect to backend"
**Solution**: Check API URL in `api_config.dart`. For Android emulator, use `10.0.2.2` instead of `localhost`.

### Issue: "Permission denied for SMS"
**Solution**: Check that permissions are declared in AndroidManifest.xml and requested at runtime.

### Issue: "Cannot read SMS on iOS"
**Solution**: iOS doesn't allow reading SMS programmatically. SMS import is Android-only.

### Issue: "OCR not extracting text"
**Solution**: Ensure good lighting and clear receipt image. Google ML Kit works best with high-contrast text.

## Dependencies

Key packages used:
- `dio` - HTTP client
- `provider` - State management
- `flutter_secure_storage` - Secure token storage
- `flutter_sms_inbox` - SMS reading (Android only)
- `google_ml_kit` - On-device ML for OCR
- `fl_chart` - Charts and graphs
- `intl` - Date/currency formatting
- `image_picker` - Camera and gallery access
- `permission_handler` - Runtime permissions

## Contributing

See main [CONTRIBUTING.md](../CONTRIBUTING.md)

## License

MIT License
