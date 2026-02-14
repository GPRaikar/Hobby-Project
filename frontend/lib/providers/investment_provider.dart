import 'package:flutter/foundation.dart';
import 'package:indian_finance_app/config/api_config.dart';
import 'package:indian_finance_app/models/investment.dart';
import 'package:indian_finance_app/services/api_service.dart';

/// Investment Provider
class InvestmentProvider with ChangeNotifier {
  final ApiService _apiService = ApiService();
  
  List<Investment> _investments = [];
  bool _isLoading = false;
  String? _error;

  List<Investment> get investments => _investments;
  bool get isLoading => _isLoading;
  String? get error => _error;

  /// Fetch all investments
  Future<void> fetchInvestments({bool isActive = true}) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final response = await _apiService.get(
        ApiConfig.investments,
        queryParameters: {'is_active': isActive},
      );

      _investments = (response.data as List)
          .map((json) => Investment.fromJson(json))
          .toList();
      
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
    }
  }

  /// Add new investment
  Future<bool> addInvestment(Investment investment) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final response = await _apiService.post(
        ApiConfig.investments,
        data: investment.toJson(),
      );

      final newInvestment = Investment.fromJson(response.data);
      _investments.insert(0, newInvestment);
      
      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  /// Update investment
  Future<bool> updateInvestment(String id, Investment investment) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final response = await _apiService.put(
        '${ApiConfig.investments}/$id',
        data: investment.toJson(),
      );

      final updatedInvestment = Investment.fromJson(response.data);
      final index = _investments.indexWhere((i) => i.id == id);
      if (index != -1) {
        _investments[index] = updatedInvestment;
      }
      
      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  /// Delete investment
  Future<bool> deleteInvestment(String id) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      await _apiService.delete('${ApiConfig.investments}/$id');
      _investments.removeWhere((i) => i.id == id);
      
      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  void clearError() {
    _error = null;
    notifyListeners();
  }
}
