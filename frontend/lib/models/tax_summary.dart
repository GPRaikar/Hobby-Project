/// Tax Summary model
class TaxSummary {
  final double grossIncome;
  final double standardDeduction;
  final double totalDeductions;
  final double taxableIncome;
  final double taxBeforeRebate;
  final double rebate87a;
  final double totalTax;
  final double cess;
  final double finalTax;
  final String regime;

  TaxSummary({
    required this.grossIncome,
    required this.standardDeduction,
    required this.totalDeductions,
    required this.taxableIncome,
    required this.taxBeforeRebate,
    required this.rebate87a,
    required this.totalTax,
    required this.cess,
    required this.finalTax,
    required this.regime,
  });

  factory TaxSummary.fromJson(Map<String, dynamic> json) {
    return TaxSummary(
      grossIncome: (json['gross_income'] as num).toDouble(),
      standardDeduction: (json['standard_deduction'] as num).toDouble(),
      totalDeductions: (json['total_deductions'] as num).toDouble(),
      taxableIncome: (json['taxable_income'] as num).toDouble(),
      taxBeforeRebate: (json['tax_before_rebate'] as num).toDouble(),
      rebate87a: (json['rebate_87a'] as num).toDouble(),
      totalTax: (json['total_tax'] as num).toDouble(),
      cess: (json['cess'] as num).toDouble(),
      finalTax: (json['final_tax'] as num).toDouble(),
      regime: json['regime'],
    );
  }
}

class Section80CResponse {
  final double totalInvested;
  final double utilized;
  final double remaining;
  final double percentageUsed;
  final double taxSaved;
  final double limit;

  Section80CResponse({
    required this.totalInvested,
    required this.utilized,
    required this.remaining,
    required this.percentageUsed,
    required this.taxSaved,
    required this.limit,
  });

  factory Section80CResponse.fromJson(Map<String, dynamic> json) {
    return Section80CResponse(
      totalInvested: (json['total_invested'] as num).toDouble(),
      utilized: (json['utilized'] as num).toDouble(),
      remaining: (json['remaining'] as num).toDouble(),
      percentageUsed: (json['percentage_used'] as num).toDouble(),
      taxSaved: (json['tax_saved'] as num).toDouble(),
      limit: (json['limit'] as num).toDouble(),
    );
  }
}
