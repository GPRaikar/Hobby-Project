import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:indian_finance_app/providers/auth_provider.dart';
import 'package:indian_finance_app/providers/dashboard_provider.dart';
import 'package:indian_finance_app/config/theme.dart';

/// Dashboard Screen - Rich Dad Dashboard
class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  @override
  void initState() {
    super.initState();
    _loadDashboard();
  }

  Future<void> _loadDashboard() async {
    final dashboardProvider = Provider.of<DashboardProvider>(context, listen: false);
    await dashboardProvider.fetchDashboard();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Dashboard'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _loadDashboard,
          ),
          PopupMenuButton<String>(
            onSelected: (value) {
              if (value == 'logout') {
                _handleLogout();
              }
            },
            itemBuilder: (context) => [
              const PopupMenuItem(
                value: 'logout',
                child: Row(
                  children: [
                    Icon(Icons.logout),
                    SizedBox(width: 8),
                    Text('Logout'),
                  ],
                ),
              ),
            ],
          ),
        ],
      ),
      body: Consumer<DashboardProvider>(
        builder: (context, provider, child) {
          if (provider.isLoading) {
            return const Center(child: CircularProgressIndicator());
          }

          if (provider.error != null) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.error, size: 64, color: Colors.red),
                  const SizedBox(height: 16),
                  Text('Error: ${provider.error}'),
                  const SizedBox(height: 16),
                  ElevatedButton(
                    onPressed: _loadDashboard,
                    child: const Text('Retry'),
                  ),
                ],
              ),
            );
          }

          final data = provider.dashboardData;
          if (data == null) {
            return const Center(child: Text('No data available'));
          }

          final incomeExpense = data['income_expense_summary'];
          final assetLiability = data['asset_liability_summary'];
          final financialFreedomRatio = data['financial_freedom_ratio'] ?? 0.0;
          final cashFlow = incomeExpense['total_income'] - incomeExpense['total_expenses'];
          final savingsRate = data['savings_rate'] ?? 0.0;

          return RefreshIndicator(
            onRefresh: _loadDashboard,
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Financial Freedom Card
                  Card(
                    color: AppTheme.primaryColor,
                    child: Padding(
                      padding: const EdgeInsets.all(20),
                      child: Column(
                        children: [
                          const Text(
                            'Financial Freedom Ratio',
                            style: TextStyle(
                              fontSize: 18,
                              color: Colors.white,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          const SizedBox(height: 16),
                          Text(
                            '${financialFreedomRatio.toStringAsFixed(1)}%',
                            style: const TextStyle(
                              fontSize: 48,
                              color: Colors.white,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          const SizedBox(height: 8),
                          const Text(
                            'Goal: 100% (Passive Income = Expenses)',
                            style: TextStyle(
                              fontSize: 12,
                              color: Colors.white70,
                            ),
                          ),
                          const SizedBox(height: 16),
                          LinearProgressIndicator(
                            value: financialFreedomRatio / 100,
                            backgroundColor: Colors.white30,
                            valueColor: const AlwaysStoppedAnimation<Color>(Colors.white),
                          ),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(height: 16),
                  
                  // Income & Expenses
                  Row(
                    children: [
                      Expanded(
                        child: _buildSummaryCard(
                          'Total Income',
                          incomeExpense['total_income'],
                          AppTheme.incomeColor,
                          Icons.trending_up,
                        ),
                      ),
                      const SizedBox(width: 16),
                      Expanded(
                        child: _buildSummaryCard(
                          'Total Expenses',
                          incomeExpense['total_expenses'],
                          AppTheme.expenseColor,
                          Icons.trending_down,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  
                  // Cash Flow & Savings Rate
                  Row(
                    children: [
                      Expanded(
                        child: _buildSummaryCard(
                          'Cash Flow',
                          cashFlow,
                          cashFlow >= 0 ? AppTheme.incomeColor : AppTheme.expenseColor,
                          Icons.account_balance_wallet,
                        ),
                      ),
                      const SizedBox(width: 16),
                      Expanded(
                        child: Card(
                          child: Padding(
                            padding: const EdgeInsets.all(16),
                            child: Column(
                              children: [
                                const Text('Savings Rate'),
                                const SizedBox(height: 8),
                                Text(
                                  '${savingsRate.toStringAsFixed(1)}%',
                                  style: const TextStyle(
                                    fontSize: 24,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  
                  // Assets & Liabilities
                  Row(
                    children: [
                      Expanded(
                        child: _buildSummaryCard(
                          'Assets',
                          assetLiability['total_assets_value'],
                          AppTheme.assetColor,
                          Icons.attach_money,
                        ),
                      ),
                      const SizedBox(width: 16),
                      Expanded(
                        child: _buildSummaryCard(
                          'Liabilities',
                          assetLiability['total_liabilities_value'],
                          AppTheme.liabilityColor,
                          Icons.money_off,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  
                  // Net Worth
                  Card(
                    child: Padding(
                      padding: const EdgeInsets.all(20),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          const Text(
                            'Net Worth',
                            style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          Text(
                            AppTheme.formatCurrency(assetLiability['net_worth']),
                            style: const TextStyle(
                              fontSize: 24,
                              fontWeight: FontWeight.bold,
                              color: AppTheme.primaryColor,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            ),
          );
        },
      ),
      bottomNavigationBar: BottomNavigationBar(
        type: BottomNavigationBarType.fixed,
        currentIndex: 0,
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.dashboard),
            label: 'Dashboard',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.receipt_long),
            label: 'Transactions',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.trending_up),
            label: 'Investments',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.account_balance),
            label: 'Tax',
          ),
        ],
        onTap: (index) {
          // TODO: Navigate to respective screens
        },
      ),
    );
  }

  Widget _buildSummaryCard(String title, double value, Color color, IconData icon) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            Icon(icon, color: color, size: 32),
            const SizedBox(height: 8),
            Text(
              title,
              style: const TextStyle(fontSize: 12),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 4),
            Text(
              AppTheme.formatCurrency(value),
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                color: color,
              ),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }

  Future<void> _handleLogout() async {
    final authProvider = Provider.of<AuthProvider>(context, listen: false);
    await authProvider.logout();
    
    if (!mounted) return;
    
    Navigator.of(context).pushReplacementNamed('/login');
  }
}
