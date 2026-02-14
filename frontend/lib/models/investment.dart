/// Investment model
enum InvestmentType {
  PPF,
  ELSS,
  NPS,
  FD,
  MUTUAL_FUND,
  STOCK,
  REAL_ESTATE,
  GOLD,
  CRYPTO,
  LIC,
  SUKANYA_SAMRIDDHI,
  NSC,
  OTHER
}

enum TaxSection { 
  SEC_80C, 
  SEC_80CCC, 
  SEC_80CCD, 
  SEC_80D, 
  SEC_80E, 
  SEC_80G, 
  NONE 
}

enum AssetLiabilityCategory { ASSET, LIABILITY }

class Investment {
  final String id;
  final String userId;
  final String name;
  final InvestmentType investmentType;
  final double amountInvested;
  final double? currentValue;
  final double? annualReturnPct;
  final DateTime startDate;
  final DateTime? maturityDate;
  final bool isTaxSaving;
  final TaxSection taxSection;
  final String? folioNumber;
  final String? tickerSymbol;
  final bool isActive;
  final AssetLiabilityCategory richDadCategory;
  final double passiveIncomeAmount;
  final DateTime createdAt;
  final DateTime updatedAt;

  Investment({
    required this.id,
    required this.userId,
    required this.name,
    required this.investmentType,
    required this.amountInvested,
    this.currentValue,
    this.annualReturnPct,
    required this.startDate,
    this.maturityDate,
    this.isTaxSaving = false,
    this.taxSection = TaxSection.NONE,
    this.folioNumber,
    this.tickerSymbol,
    this.isActive = true,
    this.richDadCategory = AssetLiabilityCategory.ASSET,
    this.passiveIncomeAmount = 0,
    required this.createdAt,
    required this.updatedAt,
  });

  factory Investment.fromJson(Map<String, dynamic> json) {
    return Investment(
      id: json['id'],
      userId: json['user_id'],
      name: json['name'],
      investmentType: InvestmentType.values.byName(json['investment_type']),
      amountInvested: (json['amount_invested'] as num).toDouble(),
      currentValue: json['current_value'] != null 
          ? (json['current_value'] as num).toDouble() 
          : null,
      annualReturnPct: json['annual_return_pct'] != null
          ? (json['annual_return_pct'] as num).toDouble()
          : null,
      startDate: DateTime.parse(json['start_date']),
      maturityDate: json['maturity_date'] != null
          ? DateTime.parse(json['maturity_date'])
          : null,
      isTaxSaving: json['is_tax_saving'] ?? false,
      taxSection: TaxSection.values.byName(json['tax_section'].replaceAll('SEC_', '')),
      folioNumber: json['folio_number'],
      tickerSymbol: json['ticker_symbol'],
      isActive: json['is_active'] ?? true,
      richDadCategory: AssetLiabilityCategory.values.byName(json['rich_dad_category']),
      passiveIncomeAmount: (json['passive_income_amount'] as num).toDouble(),
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: DateTime.parse(json['updated_at']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'name': name,
      'investment_type': investmentType.name,
      'amount_invested': amountInvested,
      'current_value': currentValue,
      'annual_return_pct': annualReturnPct,
      'start_date': startDate.toIso8601String().split('T')[0],
      'maturity_date': maturityDate?.toIso8601String().split('T')[0],
      'is_tax_saving': isTaxSaving,
      'tax_section': taxSection.name,
      'folio_number': folioNumber,
      'ticker_symbol': tickerSymbol,
      'is_active': isActive,
      'rich_dad_category': richDadCategory.name,
      'passive_income_amount': passiveIncomeAmount,
    };
  }
}
