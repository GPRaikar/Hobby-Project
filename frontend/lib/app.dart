import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:indian_finance_app/config/theme.dart';
import 'package:indian_finance_app/providers/auth_provider.dart';
import 'package:indian_finance_app/providers/transaction_provider.dart';
import 'package:indian_finance_app/providers/investment_provider.dart';
import 'package:indian_finance_app/providers/budget_provider.dart';
import 'package:indian_finance_app/providers/dashboard_provider.dart';
import 'package:indian_finance_app/screens/splash_screen.dart';
import 'package:indian_finance_app/screens/auth/login_screen.dart';
import 'package:indian_finance_app/screens/auth/register_screen.dart';
import 'package:indian_finance_app/screens/dashboard/dashboard_screen.dart';

class IndianFinanceApp extends StatelessWidget {
  const IndianFinanceApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AuthProvider()),
        ChangeNotifierProvider(create: (_) => TransactionProvider()),
        ChangeNotifierProvider(create: (_) => InvestmentProvider()),
        ChangeNotifierProvider(create: (_) => BudgetProvider()),
        ChangeNotifierProvider(create: (_) => DashboardProvider()),
      ],
      child: MaterialApp(
        title: 'Indian Finance App',
        theme: AppTheme.lightTheme,
        debugShowCheckedModeBanner: false,
        home: const SplashScreen(),
        routes: {
          '/login': (context) => const LoginScreen(),
          '/register': (context) => const RegisterScreen(),
          '/dashboard': (context) => const DashboardScreen(),
        },
      ),
    );
  }
}
