import 'package:flutter/foundation.dart';
import 'package:indian_finance_app/config/api_config.dart';
import 'package:indian_finance_app/services/api_service.dart';

/// Dashboard Provider
class DashboardProvider with ChangeNotifier {
  final ApiService _apiService = ApiService();
  
  Map<String, dynamic>? _dashboardData;
  bool _isLoading = false;
  String? _error;

  Map<String, dynamic>? get dashboardData => _dashboardData;
  bool get isLoading => _isLoading;
  String? get error => _error;

  /// Fetch dashboard data
  Future<void> fetchDashboard({int months = 6}) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final response = await _apiService.get(
        ApiConfig.dashboard,
        queryParameters: {'months': months},
      );

      _dashboardData = response.data;
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
    }
  }

  void clearError() {
    _error = null;
    notifyListeners();
  }
}
