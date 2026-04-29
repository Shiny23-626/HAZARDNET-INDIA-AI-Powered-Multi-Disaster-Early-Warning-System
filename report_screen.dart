import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import '../utils/constants.dart';

class ReportScreen extends StatefulWidget {
  const ReportScreen({super.key});

  @override
  State<ReportScreen> createState() => _ReportScreenState();
}

class _ReportScreenState extends State<ReportScreen> {
  String? _selected;
  bool _submitted = false;
  final List<File> _images = [];
  final ImagePicker _picker = ImagePicker();

  final List<Map<String, dynamic>> _hazards = [
    {'label': 'Flood', 'icon': Icons.water},
    {'label': 'Fire', 'icon': Icons.local_fire_department_rounded},
    {'label': 'Landslide', 'icon': Icons.landscape_rounded},
    {'label': 'Blocked Road', 'icon': Icons.do_not_disturb_on_rounded},
    {'label': 'Water Logging', 'icon': Icons.water_damage_rounded},
    {'label': 'Cyclone', 'icon': Icons.cyclone_rounded},
    {'label': 'Heatwave', 'icon': Icons.wb_sunny_rounded},
    {'label': 'Other', 'icon': Icons.warning_amber_rounded},
  ];

  Future<void> _pickImage(ImageSource source) async {
    try {
      final XFile? picked = await _picker.pickImage(
        source: source,
        imageQuality: 80,
        maxWidth: 1200,
      );
      if (picked != null) {
        setState(() => _images.add(File(picked.path)));
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Could not access camera/gallery.')),
        );
      }
    }
  }

  void _showImageSourceSheet() {
    showModalBottomSheet(
      context: context,
      backgroundColor: AppColors.white,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (_) => SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Container(
                width: 40,
                height: 4,
                decoration: BoxDecoration(
                  color: AppColors.lightGrey,
                  borderRadius: BorderRadius.circular(2),
                ),
              ),
              const SizedBox(height: 16),
              const Text(
                'Add Photo',
                style: TextStyle(
                  fontWeight: FontWeight.w800,
                  fontSize: 16,
                  color: AppColors.textDark,
                ),
              ),
              const SizedBox(height: 16),
              Row(
                children: [
                  Expanded(
                    child: _imageSourceOption(
                      icon: Icons.camera_alt_rounded,
                      label: 'Camera',
                      color: AppColors.orange,
                      onTap: () {
                        Navigator.pop(context);
                        _pickImage(ImageSource.camera);
                      },
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: _imageSourceOption(
                      icon: Icons.photo_library_rounded,
                      label: 'Gallery',
                      color: AppColors.blue,
                      onTap: () {
                        Navigator.pop(context);
                        _pickImage(ImageSource.gallery);
                      },
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _imageSourceOption({
    required IconData icon,
    required String label,
    required Color color,
    required VoidCallback onTap,
  }) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 18),
        decoration: BoxDecoration(
          color: color.withOpacity(0.08),
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: color.withOpacity(0.2)),
        ),
        child: Column(
          children: [
            Icon(icon, color: color, size: 28),
            const SizedBox(height: 8),
            Text(
              label,
              style: TextStyle(
                color: color,
                fontWeight: FontWeight.w700,
                fontSize: 13,
              ),
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: SafeArea(
        child: Column(
          children: [
            _buildHeader(),
            Expanded(
              child: _submitted ? _buildSuccess() : _buildForm(),
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
        children: [
          Container(
            padding: const EdgeInsets.all(10),
            decoration: BoxDecoration(
              color: AppColors.orange.withOpacity(0.15),
              borderRadius: BorderRadius.circular(12),
            ),
            child: const Icon(Icons.campaign_rounded,
                color: AppColors.orange, size: 24),
          ),
          const SizedBox(width: 12),
          const Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Report Hazard',
                style: TextStyle(
                  fontWeight: FontWeight.w800,
                  fontSize: 20,
                  color: AppColors.textDark,
                ),
              ),
              Text(
                'Help your community stay safe',
                style: TextStyle(color: AppColors.textGrey, fontSize: 13),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildForm() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'Select Hazard Type',
            style: TextStyle(
              fontWeight: FontWeight.w700,
              fontSize: 16,
              color: AppColors.textDark,
            ),
          ),
          const SizedBox(height: 12),
          GridView.builder(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
              crossAxisCount: 2,
              crossAxisSpacing: 12,
              mainAxisSpacing: 12,
              childAspectRatio: 2.8,
            ),
            itemCount: _hazards.length,
            itemBuilder: (_, i) {
              final h = _hazards[i];
              final isSelected = _selected == h['label'];
              return GestureDetector(
                onTap: () => setState(() => _selected = h['label']),
                child: AnimatedContainer(
                  duration: const Duration(milliseconds: 200),
                  padding: const EdgeInsets.symmetric(horizontal: 14),
                  decoration: BoxDecoration(
                    color: isSelected ? AppColors.orange : AppColors.white,
                    borderRadius: BorderRadius.circular(14),
                    border: Border.all(
                      color: isSelected ? AppColors.orange : Colors.transparent,
                      width: 1.5,
                    ),
                    boxShadow: const [
                      BoxShadow(color: AppColors.cardShadow, blurRadius: 6),
                    ],
                  ),
                  child: Row(
                    children: [
                      Icon(
                        h['icon'] as IconData,
                        color: isSelected ? Colors.white : AppColors.orange,
                        size: 20,
                      ),
                      const SizedBox(width: 8),
                      Text(
                        h['label'] as String,
                        style: TextStyle(
                          fontWeight: FontWeight.w600,
                          color: isSelected ? Colors.white : AppColors.textDark,
                          fontSize: 13,
                        ),
                      ),
                    ],
                  ),
                ),
              );
            },
          ),
          const SizedBox(height: 24),

          // ── PHOTO SECTION ──────────────────────────────
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: AppColors.white,
              borderRadius: BorderRadius.circular(16),
              boxShadow: const [
                BoxShadow(color: AppColors.cardShadow, blurRadius: 6)
              ],
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Text(
                      'Add Photos',
                      style: TextStyle(
                          fontWeight: FontWeight.w700,
                          color: AppColors.textDark,
                          fontSize: 14),
                    ),
                    Text(
                      '${_images.length}/5',
                      style: AppTextStyles.body.copyWith(fontSize: 12),
                    ),
                  ],
                ),
                const SizedBox(height: 4),
                Text(
                  'Attach photos of the hazard for better reporting.',
                  style: AppTextStyles.body.copyWith(fontSize: 12),
                ),
                const SizedBox(height: 12),
                SizedBox(
                  height: 90,
                  child: ListView(
                    scrollDirection: Axis.horizontal,
                    children: [
                      if (_images.length < 5)
                        GestureDetector(
                          onTap: _showImageSourceSheet,
                          child: Container(
                            width: 80,
                            height: 80,
                            margin: const EdgeInsets.only(right: 10),
                            decoration: BoxDecoration(
                              color: AppColors.orange.withOpacity(0.07),
                              borderRadius: BorderRadius.circular(12),
                              border: Border.all(
                                color: AppColors.orange.withOpacity(0.3),
                                width: 1.5,
                              ),
                            ),
                            child: const Column(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Icon(Icons.add_a_photo_rounded,
                                    color: AppColors.orange, size: 24),
                                SizedBox(height: 4),
                                Text(
                                  'Add',
                                  style: TextStyle(
                                    color: AppColors.orange,
                                    fontSize: 11,
                                    fontWeight: FontWeight.w600,
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),
                      ..._images.asMap().entries.map((entry) {
                        final idx = entry.key;
                        final file = entry.value;
                        return Stack(
                          children: [
                            Container(
                              width: 80,
                              height: 80,
                              margin: const EdgeInsets.only(right: 10),
                              decoration: BoxDecoration(
                                borderRadius: BorderRadius.circular(12),
                                image: DecorationImage(
                                  image: FileImage(file),
                                  fit: BoxFit.cover,
                                ),
                              ),
                            ),
                            Positioned(
                              top: 2,
                              right: 12,
                              child: GestureDetector(
                                onTap: () =>
                                    setState(() => _images.removeAt(idx)),
                                child: Container(
                                  width: 20,
                                  height: 20,
                                  decoration: const BoxDecoration(
                                    color: AppColors.red,
                                    shape: BoxShape.circle,
                                  ),
                                  child: const Icon(Icons.close,
                                      color: Colors.white, size: 12),
                                ),
                              ),
                            ),
                          ],
                        );
                      }).toList(),
                    ],
                  ),
                ),
              ],
            ),
          ),

          const SizedBox(height: 16),

          // ── DESCRIPTION ────────────────────────────────
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: AppColors.white,
              borderRadius: BorderRadius.circular(16),
              boxShadow: const [
                BoxShadow(color: AppColors.cardShadow, blurRadius: 6)
              ],
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  'Add Description (Optional)',
                  style: TextStyle(
                      fontWeight: FontWeight.w600, color: AppColors.textDark),
                ),
                const SizedBox(height: 10),
                TextField(
                  maxLines: 3,
                  decoration: InputDecoration(
                    hintText: 'Describe what you see...',
                    hintStyle: const TextStyle(color: AppColors.textGrey),
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                      borderSide: const BorderSide(color: AppColors.lightGrey),
                    ),
                    enabledBorder: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                      borderSide: const BorderSide(color: AppColors.lightGrey),
                    ),
                    focusedBorder: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                      borderSide: const BorderSide(color: AppColors.orange),
                    ),
                    contentPadding: const EdgeInsets.all(12),
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 24),
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: _selected == null
                  ? null
                  : () => setState(() => _submitted = true),
              style: ElevatedButton.styleFrom(
                backgroundColor: AppColors.orange,
                disabledBackgroundColor: AppColors.lightGrey,
                padding: const EdgeInsets.all(16),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(16),
                ),
              ),
              child: const Text(
                'Submit Report',
                style: TextStyle(
                  color: Colors.white,
                  fontWeight: FontWeight.w700,
                  fontSize: 16,
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSuccess() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Container(
            width: 80,
            height: 80,
            decoration: BoxDecoration(
              color: AppColors.safeGreen.withOpacity(0.15),
              shape: BoxShape.circle,
            ),
            child: const Icon(Icons.check_circle_rounded,
                color: AppColors.safeGreen, size: 48),
          ),
          const SizedBox(height: 20),
          const Text(
            'Report Submitted!',
            style: TextStyle(
                fontWeight: FontWeight.w800,
                fontSize: 22,
                color: AppColors.textDark),
          ),
          const SizedBox(height: 8),
          Text(
            'Thank you for keeping your community safe.',
            style: AppTextStyles.body,
          ),
          const SizedBox(height: 30),
          ElevatedButton(
            onPressed: () => setState(() {
              _submitted = false;
              _selected = null;
              _images.clear();
            }),
            style: ElevatedButton.styleFrom(
              backgroundColor: AppColors.orange,
              padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 14),
              shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(14)),
            ),
            child: const Text(
              'Report Another',
              style:
                  TextStyle(color: Colors.white, fontWeight: FontWeight.w700),
            ),
          ),
        ],
      ),
    );
  }
}
