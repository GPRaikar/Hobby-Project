import 'package:google_ml_kit/google_ml_kit.dart';
import 'package:image_picker/image_picker.dart';

/// OCR Service using Google ML Kit
class OcrService {
  final ImagePicker _picker = ImagePicker();
  final TextRecognizer _textRecognizer = GoogleMlKit.vision.textRecognizer();

  /// Pick image from camera
  Future<XFile?> pickImageFromCamera() async {
    return await _picker.pickImage(source: ImageSource.camera);
  }

  /// Pick image from gallery
  Future<XFile?> pickImageFromGallery() async {
    return await _picker.pickImage(source: ImageSource.gallery);
  }

  /// Extract text from image
  Future<String> extractText(String imagePath) async {
    final inputImage = InputImage.fromFilePath(imagePath);
    final RecognizedText recognizedText = await _textRecognizer.processImage(inputImage);
    return recognizedText.text;
  }

  /// Extract transaction details from receipt
  Future<Map<String, dynamic>> extractReceiptData(String imagePath) async {
    final text = await extractText(imagePath);
    
    // Simple regex patterns to extract amount and merchant
    final amountPattern = RegExp(r'(?:Rs\.?|₹)\s*([0-9,]+\.?\d*)');
    final datePattern = RegExp(r'(\d{2}[-/]\d{2}[-/]\d{2,4})');
    
    final amountMatch = amountPattern.firstMatch(text);
    final dateMatch = datePattern.firstMatch(text);
    
    // Extract merchant name (usually at the top of receipt)
    final lines = text.split('\n');
    String? merchantName;
    if (lines.isNotEmpty) {
      merchantName = lines.first.trim();
    }
    
    return {
      'amount': amountMatch?.group(1)?.replaceAll(',', ''),
      'merchant': merchantName,
      'date': dateMatch?.group(1),
      'raw_text': text,
    };
  }

  /// Dispose resources
  void dispose() {
    _textRecognizer.close();
  }
}
