/// User model
class User {
  final String id;
  final String email;
  final String? phone;
  final String? fullName;
  final String? panNumber;
  final DateTime? dateOfBirth;
  final String financialYearStart;
  final DateTime createdAt;
  final DateTime updatedAt;

  User({
    required this.id,
    required this.email,
    this.phone,
    this.fullName,
    this.panNumber,
    this.dateOfBirth,
    required this.financialYearStart,
    required this.createdAt,
    required this.updatedAt,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'],
      email: json['email'],
      phone: json['phone'],
      fullName: json['full_name'],
      panNumber: json['pan_number'],
      dateOfBirth: json['date_of_birth'] != null 
          ? DateTime.parse(json['date_of_birth']) 
          : null,
      financialYearStart: json['financial_year_start'],
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: DateTime.parse(json['updated_at']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'email': email,
      'phone': phone,
      'full_name': fullName,
      'pan_number': panNumber,
      'date_of_birth': dateOfBirth?.toIso8601String(),
      'financial_year_start': financialYearStart,
    };
  }
}
