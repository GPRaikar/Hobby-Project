/// API Configuration
class ApiConfig {
  // Base URL - Change this for production
  static const String baseUrl = 'http://localhost:8000';
  
  // Endpoints
  static const String authRegister = '/auth/register';
  static const String authLogin = '/auth/login';
  static const String authMe = '/auth/me';
  
  static const String transactions = '/transactions';
  static const String investments = '/investments';
  static const String budgets = '/budgets';
  
  static const String taxSection80C = '/tax/section-80c';
  static const String taxSection80D = '/tax/section-80d';
  static const String taxCalculate = '/tax/calculate';
  static const String taxCompare = '/tax/compare';
  
  static const String dashboard = '/dashboard';
  
  static const String smsParse = '/sms/parse';
  static const String smsParseBulk = '/sms/parse-bulk';
  
  static const String marketStock = '/market/stock';
  static const String marketMutualFund = '/market/mutual-fund';
  
  // Timeouts
  static const Duration connectTimeout = Duration(seconds: 30);
  static const Duration receiveTimeout = Duration(seconds: 30);
  
  // Storage Keys
  static const String accessTokenKey = 'access_token';
  static const String refreshTokenKey = 'refresh_token';
  static const String userIdKey = 'user_id';
}
