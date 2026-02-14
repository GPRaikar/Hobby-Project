import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:indian_finance_app/config/api_config.dart';

/// Secure storage service for sensitive data
class StorageService {
  final FlutterSecureStorage _storage = const FlutterSecureStorage();

  // Save access token
  Future<void> saveAccessToken(String token) async {
    await _storage.write(key: ApiConfig.accessTokenKey, value: token);
  }

  // Get access token
  Future<String?> getAccessToken() async {
    return await _storage.read(key: ApiConfig.accessTokenKey);
  }

  // Save refresh token
  Future<void> saveRefreshToken(String token) async {
    await _storage.write(key: ApiConfig.refreshTokenKey, value: token);
  }

  // Get refresh token
  Future<String?> getRefreshToken() async {
    return await _storage.read(key: ApiConfig.refreshTokenKey);
  }

  // Save user ID
  Future<void> saveUserId(String userId) async {
    await _storage.write(key: ApiConfig.userIdKey, value: userId);
  }

  // Get user ID
  Future<String?> getUserId() async {
    return await _storage.read(key: ApiConfig.userIdKey);
  }

  // Clear all stored data
  Future<void> clearAll() async {
    await _storage.deleteAll();
  }

  // Check if user is logged in
  Future<bool> isLoggedIn() async {
    final token = await getAccessToken();
    return token != null && token.isNotEmpty;
  }
}
