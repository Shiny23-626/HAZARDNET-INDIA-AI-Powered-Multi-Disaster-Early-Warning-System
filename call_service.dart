import 'package:url_launcher/url_launcher.dart';

class CallService {
  static Future<void> makeCall(String number) async {
    final Uri phoneUri = Uri(scheme: 'tel', path: number);
    if (await canLaunchUrl(phoneUri)) {
      await launchUrl(phoneUri);
    }
  }

  static Future<void> openWebsite(String url) async {
    final Uri uri = Uri.parse('https://$url');
    if (await canLaunchUrl(uri)) {
      await launchUrl(uri, mode: LaunchMode.externalApplication);
    }
  }

  static Future<void> sendEmail(String email) async {
    final Uri emailUri = Uri(scheme: 'mailto', path: email);
    if (await canLaunchUrl(emailUri)) {
      await launchUrl(emailUri);
    }
  }
}
