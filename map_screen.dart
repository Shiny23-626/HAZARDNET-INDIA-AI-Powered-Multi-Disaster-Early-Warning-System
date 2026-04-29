import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';

import '../model/hazard_model.dart';
import '../utils/constants.dart';
import 'map_widget.dart';

class MapScreen extends StatefulWidget {
  const MapScreen({super.key});

  @override
  State<MapScreen> createState() => _MapScreenState();
}

class _MapScreenState extends State<MapScreen> {
  double _latitude = 13.0827;
  double _longitude = 80.2707;
  String _locationName = 'Selected Location';

  void _handleMapTap(LatLng latLng) {
    setState(() {
      _latitude = latLng.latitude;
      _longitude = latLng.longitude;
      _locationName =
          '${latLng.latitude.toStringAsFixed(4)}, ${latLng.longitude.toStringAsFixed(4)}';
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        backgroundColor: AppColors.white,
        elevation: 0,
        title: const Text(
          'Risk Map',
          style: TextStyle(
            color: AppColors.textDark,
            fontWeight: FontWeight.w800,
          ),
        ),
        iconTheme: const IconThemeData(color: AppColors.textDark),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: ClipRRect(
          borderRadius: const BorderRadius.all(Radius.circular(24)),
          child: MapWidget(
            hazardData: null,
            latitude: _latitude,
            longitude: _longitude,
            locationName: _locationName,
            onTap: _handleMapTap,
          ),
        ),
      ),
    );
  }
}
