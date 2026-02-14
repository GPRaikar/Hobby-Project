import 'package:flutter_sms_inbox/flutter_sms_inbox.dart';
import 'package:permission_handler/permission_handler.dart';

/// SMS Service for reading SMS messages
class SmsService {
  final SmsQuery _query = SmsQuery();

  /// Request SMS permission
  Future<bool> requestPermission() async {
    final status = await Permission.sms.request();
    return status.isGranted;
  }

  /// Check if SMS permission is granted
  Future<bool> hasPermission() async {
    return await Permission.sms.isGranted;
  }

  /// Get all SMS messages
  Future<List<SmsMessage>> getAllSms() async {
    if (!await hasPermission()) {
      final granted = await requestPermission();
      if (!granted) return [];
    }

    return await _query.querySms(
      kinds: [SmsQueryKind.inbox],
      count: 500, // Fetch last 500 messages
    );
  }

  /// Get SMS from specific senders (banks)
  Future<List<SmsMessage>> getBankSms() async {
    final allSms = await getAllSms();
    
    // Filter SMS from known banks
    final bankKeywords = [
      'HDFC', 'SBI', 'ICICI', 'AXIS', 'KOTAK', 
      'debited', 'credited', 'UPI', 'a/c', 'Acct'
    ];

    return allSms.where((sms) {
      final body = sms.body?.toLowerCase() ?? '';
      final sender = sms.address?.toLowerCase() ?? '';
      
      return bankKeywords.any((keyword) => 
        body.contains(keyword.toLowerCase()) || 
        sender.contains(keyword.toLowerCase())
      );
    }).toList();
  }

  /// Parse SMS for transaction data (to be sent to backend)
  String extractSmsText(SmsMessage sms) {
    return sms.body ?? '';
  }
}
