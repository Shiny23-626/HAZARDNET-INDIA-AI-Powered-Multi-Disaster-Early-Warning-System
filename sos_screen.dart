import 'package:flutter/material.dart';
import '../services/call_service.dart';
import '../utils/constants.dart';

class SosScreen extends StatelessWidget {
  const SosScreen({super.key});

  static const List<Map<String, dynamic>> _contacts = [
    {
      'title': 'Disaster Management',
      'number': '1077',
      'subtitle': 'National Emergency Response',
      'icon': Icons.emergency_rounded,
      'color': Color(0xFFE53935),
    },
    {
      'title': 'Police',
      'number': '100',
      'subtitle': 'Law Enforcement',
      'icon': Icons.local_police_rounded,
      'color': Color(0xFF1565C0),
    },
    {
      'title': 'Fire Station',
      'number': '101',
      'subtitle': 'Fire & Rescue Services',
      'icon': Icons.local_fire_department_rounded,
      'color': Color(0xFFFF6B35),
    },
    {
      'title': 'Ambulance',
      'number': '108',
      'subtitle': 'Medical Emergency',
      'icon': Icons.medical_services_rounded,
      'color': Color(0xFF2ECC71),
    },
    {
      'title': 'Women Helpline',
      'number': '1091',
      'subtitle': 'Women Safety & Support',
      'icon': Icons.female_rounded,
      'color': Color(0xFF9C27B0),
    },
    {
      'title': 'Child Helpline',
      'number': '1098',
      'subtitle': 'Child Protection Services',
      'icon': Icons.child_care_rounded,
      'color': Color(0xFF00BCD4),
    },
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: SafeArea(
        child: Column(
          children: [
            _buildHeader(),
            _buildSOSBanner(),
            Expanded(
              child: ListView.builder(
                padding: const EdgeInsets.all(16),
                itemCount: _contacts.length,
                itemBuilder: (_, i) => _buildCallCard(_contacts[i]),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildHeader() {
    return Container(
      padding: const EdgeInsets.all(20),
      color: AppColors.white,
      child: const Row(
        children: [
          Icon(Icons.emergency_share_rounded, color: AppColors.red, size: 24),
          SizedBox(width: 12),
          Text(
            'Emergency SOS',
            style: TextStyle(
              fontWeight: FontWeight.w800,
              fontSize: 20,
              color: AppColors.textDark,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSOSBanner() {
    return Container(
      margin: const EdgeInsets.all(16),
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          colors: [Color(0xFFE53935), Color(0xFFB71C1C)],
        ),
        borderRadius: BorderRadius.circular(24),
      ),
      child: Row(
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: const [
                Text(
                  'In an Emergency?',
                  style: TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.w800,
                    fontSize: 20,
                  ),
                ),
                SizedBox(height: 4),
                Text(
                  'Tap any number below to call immediately.',
                  style: TextStyle(color: Colors.white70, fontSize: 13),
                ),
              ],
            ),
          ),
          const Icon(Icons.sos, color: Colors.white, size: 44),
        ],
      ),
    );
  }

  Widget _buildCallCard(Map<String, dynamic> contact) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.white,
        borderRadius: BorderRadius.circular(20),
        boxShadow: const [
          BoxShadow(color: AppColors.cardShadow, blurRadius: 8),
        ],
      ),
      child: Row(
        children: [
          Container(
            width: 48,
            height: 48,
            decoration: BoxDecoration(
              color: (contact['color'] as Color).withOpacity(0.12),
              borderRadius: BorderRadius.circular(14),
            ),
            child: Icon(
              contact['icon'] as IconData,
              color: contact['color'] as Color,
              size: 24,
            ),
          ),
          const SizedBox(width: 14),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  contact['title'] as String,
                  style: const TextStyle(
                    fontWeight: FontWeight.w700,
                    fontSize: 15,
                    color: AppColors.textDark,
                  ),
                ),
                Text(
                  contact['subtitle'] as String,
                  style: AppTextStyles.body.copyWith(fontSize: 12),
                ),
              ],
            ),
          ),
          GestureDetector(
            onTap: () => CallService.makeCall(contact['number'] as String),
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
              decoration: BoxDecoration(
                color: contact['color'] as Color,
                borderRadius: BorderRadius.circular(12),
              ),
              child: Text(
                contact['number'] as String,
                style: const TextStyle(
                  color: Colors.white,
                  fontWeight: FontWeight.w800,
                  fontSize: 16,
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
