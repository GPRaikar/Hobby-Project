/// Budget model
class Budget {
  final String id;
  final String userId;
  final String category;
  final double monthlyLimit;
  final String financialYear;
  final DateTime createdAt;
  final DateTime updatedAt;
  final double? spent;
  final double? remaining;
  final double? percentageUsed;

  Budget({
    required this.id,
    required this.userId,
    required this.category,
    required this.monthlyLimit,
    required this.financialYear,
    required this.createdAt,
    required this.updatedAt,
    this.spent,
    this.remaining,
    this.percentageUsed,
  });

  factory Budget.fromJson(Map<String, dynamic> json) {
    return Budget(
      id: json['id'],
      userId: json['user_id'],
      category: json['category'],
      monthlyLimit: (json['monthly_limit'] as num).toDouble(),
      financialYear: json['financial_year'],
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: DateTime.parse(json['updated_at']),
      spent: json['spent'] != null ? (json['spent'] as num).toDouble() : null,
      remaining: json['remaining'] != null ? (json['remaining'] as num).toDouble() : null,
      percentageUsed: json['percentage_used'] != null 
          ? (json['percentage_used'] as num).toDouble() 
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'category': category,
      'monthly_limit': monthlyLimit,
      'financial_year': financialYear,
    };
  }
}
