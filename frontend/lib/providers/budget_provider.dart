import 'package:flutter/foundation.dart';
import 'package:indian_finance_app/config/api_config.dart';
import 'package:indian_finance_app/models/budget.dart';
import 'package:indian_finance_app/services/api_service.dart';

/// Budget Provider
class BudgetProvider with ChangeNotifier {
  final ApiService _apiService = ApiService();
  
  List<Budget> _budgets = [];
  bool _isLoading = false;
  String? _error;

  List<Budget> get budgets => _budgets;
  bool get isLoading => _isLoading;
  String? get error => _error;

  /// Fetch all budgets
  Future<void> fetchBudgets({String? financialYear}) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final queryParams = <String, dynamic>{};
      if (financialYear != null) queryParams['financial_year'] = financialYear;

      final response = await _apiService.get(
        ApiConfig.budgets,
        queryParameters: queryParams,
      );

      _budgets = (response.data as List)
          .map((json) => Budget.fromJson(json))
          .toList();
      
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
    }
  }

  /// Add new budget
  Future<bool> addBudget(Budget budget) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final response = await _apiService.post(
        ApiConfig.budgets,
        data: budget.toJson(),
      );

      final newBudget = Budget.fromJson(response.data);
      _budgets.insert(0, newBudget);
      
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

  /// Update budget
  Future<bool> updateBudget(String id, Budget budget) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final response = await _apiService.put(
        '${ApiConfig.budgets}/$id',
        data: budget.toJson(),
      );

      final updatedBudget = Budget.fromJson(response.data);
      final index = _budgets.indexWhere((b) => b.id == id);
      if (index != -1) {
        _budgets[index] = updatedBudget;
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

  /// Delete budget
  Future<bool> deleteBudget(String id) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      await _apiService.delete('${ApiConfig.budgets}/$id');
      _budgets.removeWhere((b) => b.id == id);
      
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
