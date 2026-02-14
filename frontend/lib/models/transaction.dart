/// Transaction model
enum TransactionType { INCOME, EXPENSE, TRANSFER }
enum TransactionSource { MANUAL, SMS, OCR, BANK_SYNC }
enum RecurringFrequency { DAILY, WEEKLY, MONTHLY, YEARLY }
enum RichDadCategory { 
  ACTIVE_INCOME, 
  PASSIVE_INCOME, 
  ASSET_EXPENSE, 
  LIABILITY_EXPENSE, 
  NECESSITY 
}

class Transaction {
  final String id;
  final String userId;
  final TransactionType type;
  final String category;
  final String? subCategory;
  final double amount;
  final String currency;
  final String? description;
  final String? merchantName;
  final TransactionSource source;
  final String? accountIdentifier;
  final DateTime transactionDate;
  final bool isRecurring;
  final RecurringFrequency? recurringFrequency;
  final RichDadCategory? richDadCategory;
  final DateTime createdAt;
  final DateTime updatedAt;

  Transaction({
    required this.id,
    required this.userId,
    required this.type,
    required this.category,
    this.subCategory,
    required this.amount,
    this.currency = 'INR',
    this.description,
    this.merchantName,
    this.source = TransactionSource.MANUAL,
    this.accountIdentifier,
    required this.transactionDate,
    this.isRecurring = false,
    this.recurringFrequency,
    this.richDadCategory,
    required this.createdAt,
    required this.updatedAt,
  });

  factory Transaction.fromJson(Map<String, dynamic> json) {
    return Transaction(
      id: json['id'],
      userId: json['user_id'],
      type: TransactionType.values.byName(json['type']),
      category: json['category'],
      subCategory: json['sub_category'],
      amount: (json['amount'] as num).toDouble(),
      currency: json['currency'] ?? 'INR',
      description: json['description'],
      merchantName: json['merchant_name'],
      source: TransactionSource.values.byName(json['source']),
      accountIdentifier: json['account_identifier'],
      transactionDate: DateTime.parse(json['transaction_date']),
      isRecurring: json['is_recurring'] ?? false,
      recurringFrequency: json['recurring_frequency'] != null
          ? RecurringFrequency.values.byName(json['recurring_frequency'])
          : null,
      richDadCategory: json['rich_dad_category'] != null
          ? RichDadCategory.values.byName(json['rich_dad_category'])
          : null,
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: DateTime.parse(json['updated_at']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'type': type.name,
      'category': category,
      'sub_category': subCategory,
      'amount': amount,
      'currency': currency,
      'description': description,
      'merchant_name': merchantName,
      'source': source.name,
      'account_identifier': accountIdentifier,
      'transaction_date': transactionDate.toIso8601String().split('T')[0],
      'is_recurring': isRecurring,
      'recurring_frequency': recurringFrequency?.name,
      'rich_dad_category': richDadCategory?.name,
    };
  }
}
