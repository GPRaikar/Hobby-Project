import 'package:indian_finance_app/config/api_config.dart';
import 'package:indian_finance_app/models/user.dart';
import 'package:indian_finance_app/services/api_service.dart';
import 'package:indian_finance_app/services/storage_service.dart';

/// Authentication service
class AuthService {
  final ApiService _apiService = ApiService();
  final StorageService _storageService = StorageService();

  /// Register a new user
  Future<User> register({
    required String email,
    required String password,
    String? fullName,
    String? phone,
  }) async {
    final response = await _apiService.post(
      ApiConfig.authRegister,
      data: {
        'email': email,
        'password': password,
        'full_name': fullName,
        'phone': phone,
      },
    );

    return User.fromJson(response.data);
  }

  /// Login user and save tokens
  Future<User> login({
    required String email,
    required String password,
  }) async {
    final response = await _apiService.post(
      ApiConfig.authLogin,
      data: {
        'email': email,
        'password': password,
      },
    );

    // Save tokens
    await _storageService.saveAccessToken(response.data['access_token']);
    await _storageService.saveRefreshToken(response.data['refresh_token']);

    // Get user info
    return await getCurrentUser();
  }

  /// Get current user info
  Future<User> getCurrentUser() async {
    final response = await _apiService.get(ApiConfig.authMe);
    final user = User.fromJson(response.data);
    await _storageService.saveUserId(user.id);
    return user;
  }

  /// Logout user
  Future<void> logout() async {
    await _storageService.clearAll();
  }

  /// Check if user is logged in
  Future<bool> isLoggedIn() async {
    return await _storageService.isLoggedIn();
  }
}
