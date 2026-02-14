import 'package:flutter/foundation.dart';
import 'package:indian_finance_app/config/api_config.dart';
import 'package:indian_finance_app/models/transaction.dart';
import 'package:indian_finance_app/services/api_service.dart';

/// Transaction Provider
class TransactionProvider with ChangeNotifier {
  final ApiService _apiService = ApiService();
  
  List<Transaction> _transactions = [];
  bool _isLoading = false;
  String? _error;

  List<Transaction> get transactions => _transactions;
  bool get isLoading => _isLoading;
  String? get error => _error;

  /// Fetch all transactions
  Future<void> fetchTransactions({
    TransactionType? type,
    String? category,
    DateTime? startDate,
    DateTime? endDate,
  }) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final queryParams = <String, dynamic>{};
      if (type != null) queryParams['transaction_type'] = type.name;
      if (category != null) queryParams['category'] = category;
      if (startDate != null) queryParams['start_date'] = startDate.toIso8601String().split('T')[0];
      if (endDate != null) queryParams['end_date'] = endDate.toIso8601String().split('T')[0];

      final response = await _apiService.get(
        ApiConfig.transactions,
        queryParameters: queryParams,
      );

      _transactions = (response.data as List)
          .map((json) => Transaction.fromJson(json))
          .toList();
      
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
    }
  }

  /// Add new transaction
  Future<bool> addTransaction(Transaction transaction) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final response = await _apiService.post(
        ApiConfig.transactions,
        data: transaction.toJson(),
      );

      final newTransaction = Transaction.fromJson(response.data);
      _transactions.insert(0, newTransaction);
      
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

  /// Update transaction
  Future<bool> updateTransaction(String id, Transaction transaction) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final response = await _apiService.put(
        '${ApiConfig.transactions}/$id',
        data: transaction.toJson(),
      );

      final updatedTransaction = Transaction.fromJson(response.data);
      final index = _transactions.indexWhere((t) => t.id == id);
      if (index != -1) {
        _transactions[index] = updatedTransaction;
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

  /// Delete transaction
  Future<bool> deleteTransaction(String id) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      await _apiService.delete('${ApiConfig.transactions}/$id');
      _transactions.removeWhere((t) => t.id == id);
      
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
