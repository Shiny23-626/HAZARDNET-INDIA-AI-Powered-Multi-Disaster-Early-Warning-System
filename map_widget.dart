import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';

import '../model/hazard_model.dart';
import '../utils/constants.dart';

class MapWidget extends StatefulWidget {
  final HazardModel? hazardData;
  final double latitude;
  final double longitude;
  final String locationName;
  final void Function(LatLng latLng)? onTap;

  const MapWidget({
    super.key,
    required this.hazardData,
    required this.latitude,
    required this.longitude,
    required this.locationName,
    this.onTap,
  });

  @override
  State<MapWidget> createState() => _MapWidgetState();
}

class _MapWidgetState extends State<MapWidget> {
  GoogleMapController? _mapController;
  late LatLng _selectedPosition;

  Set<Marker> _markers = {};
  Set<Circle> _circles = {};

  bool _mapReady = false;

  @override
  void initState() {
    super.initState();
    _selectedPosition = LatLng(widget.latitude, widget.longitude);
    _refreshMapData(moveCamera: false);
  }

  @override
  void didUpdateWidget(covariant MapWidget oldWidget) {
    super.didUpdateWidget(oldWidget);

    final locationChanged = oldWidget.latitude != widget.latitude ||
        oldWidget.longitude != widget.longitude ||
        oldWidget.locationName != widget.locationName;

    final hazardChanged = oldWidget.hazardData?.overallRiskLevel !=
            widget.hazardData?.overallRiskLevel ||
        oldWidget.hazardData?.maxRiskDisaster !=
            widget.hazardData?.maxRiskDisaster ||
        oldWidget.hazardData?.maxRiskConfidence !=
            widget.hazardData?.maxRiskConfidence;

    if (locationChanged) {
      _selectedPosition = LatLng(widget.latitude, widget.longitude);
    }

    if (locationChanged || hazardChanged) {
      _refreshMapData(moveCamera: true);
    }
  }

  String _safeRiskLevel() {
    return widget.hazardData?.overallRiskLevel ?? 'Low';
  }

  Color _riskToColor(String level) {
    switch (level.toLowerCase()) {
      case 'high':
        return Colors.red;
      case 'medium':
      case 'moderate':
        return Colors.orange;
      default:
        return Colors.green;
    }
  }

  double _riskRadius(String level) {
    switch (level.toLowerCase()) {
      case 'high':
        return 1200;
      case 'medium':
      case 'moderate':
        return 900;
      default:
        return 700;
    }
  }

  void _refreshMapData({required bool moveCamera}) {
    final hazard = widget.hazardData;
    final overallRisk = _safeRiskLevel();
    final riskColor = _riskToColor(overallRisk);
    final fillOpacity = overallRisk.toLowerCase() == 'low' ? 0.08 : 0.18;

    final hazardMarkerPosition = LatLng(
      _selectedPosition.latitude + 0.006,
      _selectedPosition.longitude + 0.006,
    );

    final updatedMarkers = <Marker>{
      Marker(
        markerId: const MarkerId('selected_location'),
        position: _selectedPosition,
        infoWindow: InfoWindow(title: widget.locationName),
        icon: BitmapDescriptor.defaultMarkerWithHue(
          BitmapDescriptor.hueAzure,
        ),
      ),
    };

    if (hazard != null && overallRisk.toLowerCase() != 'low') {
      updatedMarkers.add(
        Marker(
          markerId: const MarkerId('hazard_marker'),
          position: hazardMarkerPosition,
          icon: BitmapDescriptor.defaultMarkerWithHue(
            overallRisk.toLowerCase() == 'high'
                ? BitmapDescriptor.hueRed
                : BitmapDescriptor.hueOrange,
          ),
          infoWindow: InfoWindow(
            title: '${hazard.maxRiskDisaster} Risk',
            snippet:
                '${hazard.overallRiskLevel} • ${hazard.maxRiskConfidence.toStringAsFixed(1)}%',
          ),
        ),
      );
    }

    final updatedCircles = <Circle>{
      Circle(
        circleId: const CircleId('risk_zone'),
        center: _selectedPosition,
        radius: _riskRadius(overallRisk),
        fillColor: riskColor.withOpacity(fillOpacity),
        strokeColor: riskColor.withOpacity(0.65),
        strokeWidth: 2,
      ),
    };

    if (mounted) {
      setState(() {
        _markers = updatedMarkers;
        _circles = updatedCircles;
      });
    }

    if (moveCamera && _mapReady && _mapController != null) {
      _mapController!.animateCamera(
        CameraUpdate.newLatLngZoom(_selectedPosition, 14),
      );
    }
  }

  void _zoomIn() {
    _mapController?.animateCamera(CameraUpdate.zoomIn());
  }

  void _zoomOut() {
    _mapController?.animateCamera(CameraUpdate.zoomOut());
  }

  void _goToSelectedLocation() {
    _mapController?.animateCamera(
      CameraUpdate.newLatLngZoom(_selectedPosition, 14),
    );
  }

  void _fitRiskZone() {
    _mapController?.animateCamera(
      CameraUpdate.newLatLngZoom(_selectedPosition, 13),
    );
  }

  @override
  void dispose() {
    _mapController?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 220,
      child: Stack(
        children: [
          GoogleMap(
            initialCameraPosition: CameraPosition(
              target: _selectedPosition,
              zoom: 12,
            ),
            markers: _markers,
            circles: _circles,
            myLocationEnabled: true,
            myLocationButtonEnabled: false,
            zoomControlsEnabled: false,
            mapToolbarEnabled: false,
            onTap: widget.onTap,
            onMapCreated: (controller) {
              _mapController = controller;
              _mapReady = true;
              controller.animateCamera(
                CameraUpdate.newLatLngZoom(_selectedPosition, 14),
              );
            },
          ),
          Positioned(
            right: 12,
            bottom: 16,
            child: Column(
              children: [
                _mapBtn(Icons.my_location_rounded, _goToSelectedLocation),
                const SizedBox(height: 8),
                _mapBtn(Icons.layers_rounded, _fitRiskZone),
                const SizedBox(height: 8),
                _mapBtn(Icons.add_rounded, _zoomIn),
                const SizedBox(height: 8),
                _mapBtn(Icons.remove_rounded, _zoomOut),
              ],
            ),
          ),
          Positioned(
            left: 12,
            bottom: 16,
            child: _buildLegend(),
          ),
          Positioned(
            left: 12,
            right: 68,
            top: 12,
            child: _buildTopInfoCard(),
          ),
        ],
      ),
    );
  }

  Widget _buildTopInfoCard() {
    final hazard = widget.hazardData;
    final level = _safeRiskLevel();
    final color = _riskToColor(level);

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
      decoration: BoxDecoration(
        color: AppColors.white.withOpacity(0.96),
        borderRadius: BorderRadius.circular(14),
        boxShadow: const [
          BoxShadow(color: AppColors.cardShadow, blurRadius: 8),
        ],
      ),
      child: Row(
        children: [
          Container(
            width: 10,
            height: 10,
            decoration: BoxDecoration(
              color: color,
              shape: BoxShape.circle,
            ),
          ),
          const SizedBox(width: 8),
          Expanded(
            child: Text(
              widget.locationName,
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
              style: const TextStyle(
                fontSize: 12,
                fontWeight: FontWeight.w800,
                color: AppColors.textDark,
              ),
            ),
          ),
          const SizedBox(width: 8),
          Text(
            hazard == null ? 'Loading' : level,
            style: TextStyle(
              fontSize: 11,
              fontWeight: FontWeight.w800,
              color: color,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildLegend() {
    final level = _safeRiskLevel().toLowerCase();

    String label;
    Color color;

    if (level == 'high') {
      label = 'High Risk Zone';
      color = Colors.red;
    } else if (level == 'medium' || level == 'moderate') {
      label = 'Moderate Risk Zone';
      color = Colors.orange;
    } else {
      label = 'Clear Zone';
      color = Colors.green;
    }

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(10),
        boxShadow: const [
          BoxShadow(color: AppColors.cardShadow, blurRadius: 6),
        ],
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Container(
            width: 10,
            height: 10,
            decoration: BoxDecoration(
              color: color.withOpacity(0.5),
              shape: BoxShape.circle,
              border: Border.all(color: color, width: 1.5),
            ),
          ),
          const SizedBox(width: 6),
          Text(
            label,
            style: TextStyle(
              fontSize: 11,
              fontWeight: FontWeight.w700,
              color: color,
            ),
          ),
        ],
      ),
    );
  }

  Widget _mapBtn(IconData icon, VoidCallback onTap) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        width: 38,
        height: 38,
        decoration: BoxDecoration(
          color: AppColors.white,
          borderRadius: BorderRadius.circular(10),
          boxShadow: const [
            BoxShadow(color: AppColors.cardShadow, blurRadius: 6),
          ],
        ),
        child: Icon(
          icon,
          color: AppColors.textDark,
          size: 18,
        ),
      ),
    );
  }
}
