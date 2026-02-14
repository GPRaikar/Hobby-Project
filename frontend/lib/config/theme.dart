import 'package:flutter/material.dart';

/// App Theme Configuration
class AppTheme {
  // Primary Colors
  static const Color primaryColor = Color(0xFF1565C0); // Blue
  static const Color secondaryColor = Color(0xFF43A047); // Green for positive
  static const Color errorColor = Color(0xFFD32F2F); // Red for negative
  static const Color warningColor = Color(0xFFFFA000); // Amber for warnings
  
  // Background Colors
  static const Color backgroundColor = Color(0xFFF5F5F5);
  static const Color surfaceColor = Colors.white;
  
  // Text Colors
  static const Color textPrimary = Color(0xFF212121);
  static const Color textSecondary = Color(0xFF757575);
  
  // Chart Colors
  static const Color incomeColor = Color(0xFF4CAF50);
  static const Color expenseColor = Color(0xFFE53935);
  static const Color assetColor = Color(0xFF2196F3);
  static const Color liabilityColor = Color(0xFFFF5722);
  static const Color passiveIncomeColor = Color(0xFF9C27B0);
  
  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(
        seedColor: primaryColor,
        brightness: Brightness.light,
      ),
      scaffoldBackgroundColor: backgroundColor,
      appBarTheme: const AppBarTheme(
        elevation: 0,
        centerTitle: true,
        backgroundColor: primaryColor,
        foregroundColor: Colors.white,
      ),
      cardTheme: CardTheme(
        elevation: 2,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
        ),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
        ),
        filled: true,
        fillColor: surfaceColor,
      ),
    );
  }
  
  // Currency formatter for INR
  static String formatCurrency(double amount) {
    // Indian numbering system: 1,00,000 instead of 100,000
    String amountStr = amount.toStringAsFixed(2);
    List<String> parts = amountStr.split('.');
    String integerPart = parts[0];
    String decimalPart = parts[1];
    
    // Add commas in Indian format
    if (integerPart.length > 3) {
      String lastThree = integerPart.substring(integerPart.length - 3);
      String otherDigits = integerPart.substring(0, integerPart.length - 3);
      
      if (otherDigits.isNotEmpty) {
        RegExp reg = RegExp(r'(\d)(?=(\d{2})+$)');
        otherDigits = otherDigits.replaceAllMapped(reg, (match) => '${match.group(1)},');
      }
      
      integerPart = '$otherDigits,$lastThree';
    }
    
    return '₹$integerPart.$decimalPart';
  }
}
