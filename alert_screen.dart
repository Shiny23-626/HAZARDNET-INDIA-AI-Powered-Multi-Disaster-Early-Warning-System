import 'package:flutter/material.dart';
import '../utils/constants.dart';

class AlertScreen extends StatelessWidget {
  const AlertScreen({super.key});

  static const List<Map<String, dynamic>> _alerts = [
    {
      'type': 'AQI Alert',
      'severity': 'High',
      'message':
          'Air Quality Index has reached 342 near Safdarjung. Avoid outdoor activity.',
      'time': '2 mins ago',
      'color': AppColors.red,
      'icon': Icons.air_rounded,
    },
    {
      'type': 'Heatwave Warning',
      'severity': 'Medium',
      'message':
          'Temperatures expected to reach 45°C in North Delhi. Stay hydrated.',
      'time': '1 hour ago',
      'color': AppColors.orange,
      'icon': Icons.wb_sunny_rounded,
    },
    {
      'type': 'Flood Watch',
      'severity': 'Low',
      'message':
          'Light flooding reported near Yamuna riverbanks. No immediate threat.',
      'time': '3 hours ago',
      'color': AppColors.blue,
      'icon': Icons.water_rounded,
    },
    {
      'type': 'Cyclone Advisory',
      'severity': 'Low',
      'message':
          'Cyclonic activity detected in Bay of Bengal. No impact expected for 72 hours.',
      'time': '6 hours ago',
      'color': AppColors.blue,
      'icon': Icons.cyclone_rounded,
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
            Expanded(
              child: ListView.builder(
                padding: const EdgeInsets.all(16),
                itemCount: _alerts.length,
                itemBuilder: (_, i) => _buildAlertCard(_alerts[i]),
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
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          const Text(
            'Live Alerts',
            style: TextStyle(
              fontWeight: FontWeight.w800,
              fontSize: 20,
              color: AppColors.textDark,
            ),
          ),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
            decoration: BoxDecoration(
              color: AppColors.red.withOpacity(0.12),
              borderRadius: BorderRadius.circular(20),
            ),
            child: Row(
              children: [
                Container(
                  width: 7,
                  height: 7,
                  decoration: const BoxDecoration(
                    color: AppColors.red,
                    shape: BoxShape.circle,
                  ),
                ),
                const SizedBox(width: 5),
                const Text(
                  'LIVE',
                  style: TextStyle(
                    color: AppColors.red,
                    fontWeight: FontWeight.w700,
                    fontSize: 11,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildAlertCard(Map<String, dynamic> alert) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.white,
        borderRadius: BorderRadius.circular(20),
        boxShadow: const [
          BoxShadow(color: AppColors.cardShadow, blurRadius: 8)
        ],
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            width: 46,
            height: 46,
            decoration: BoxDecoration(
              color: (alert['color'] as Color).withOpacity(0.12),
              borderRadius: BorderRadius.circular(14),
            ),
            child: Icon(alert['icon'] as IconData,
                color: alert['color'] as Color, size: 22),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      alert['type'] as String,
                      style: const TextStyle(
                        fontWeight: FontWeight.w700,
                        fontSize: 14,
                        color: AppColors.textDark,
                      ),
                    ),
                    _severityBadge(
                        alert['severity'] as String, alert['color'] as Color),
                  ],
                ),
                const SizedBox(height: 6),
                Text(
                  alert['message'] as String,
                  style: AppTextStyles.body.copyWith(fontSize: 12, height: 1.4),
                ),
                const SizedBox(height: 6),
                Text(
                  alert['time'] as String,
                  style: const TextStyle(
                      color: AppColors.textGrey,
                      fontSize: 11,
                      fontWeight: FontWeight.w500),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _severityBadge(String severity, Color color) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
      decoration: BoxDecoration(
        color: color.withOpacity(0.12),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Text(
        severity,
        style: TextStyle(
          color: color,
          fontWeight: FontWeight.w700,
          fontSize: 11,
        ),
      ),
    );
  }
}
