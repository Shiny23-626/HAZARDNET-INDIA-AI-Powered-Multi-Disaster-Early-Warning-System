import 'package:flutter/material.dart';

class AppColors {
  static const Color background = Color(0xFFF4F6FA);
  static const Color white = Colors.white;
  static const Color orange = Color(0xFFFF6B35);
  static const Color red = Color(0xFFE53935);
  static const Color blue = Color(0xFF1565C0);
  static const Color darkBlue = Color(0xFF0D1B4B);
  static const Color lightGrey = Color(0xFFF0F0F0);
  static const Color textDark = Color(0xFF1A1A2E);
  static const Color textGrey = Color(0xFF8E8E93);
  static const Color safeGreen = Color(0xFF2ECC71);
  static const Color cardShadow = Color(0x1A000000);
  static const Color moderate = Color(0xFFFFA726);
}

class AppStrings {
  static const String appName = 'HazardNet India';

  // ONLY base domain here
  static const String apiBaseUrl = 'https://disaster-alert-api.onrender.com';

  // endpoint separately here
  static const String predictEndpoint = '/predict';
}

class AppTextStyles {
  static const TextStyle heading = TextStyle(
    fontSize: 22,
    fontWeight: FontWeight.w800,
    color: AppColors.textDark,
  );

  static const TextStyle subheading = TextStyle(
    fontSize: 16,
    fontWeight: FontWeight.w600,
    color: AppColors.textDark,
  );

  static const TextStyle body = TextStyle(
    fontSize: 14,
    color: AppColors.textGrey,
  );

  static const TextStyle label = TextStyle(
    fontSize: 11,
    fontWeight: FontWeight.w700,
    letterSpacing: 1.2,
  );
}
