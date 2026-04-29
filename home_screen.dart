import 'dart:async';
import 'package:geocoding/geocoding.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:geolocator/geolocator.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:url_launcher/url_launcher.dart';

import '../model/hazard_model.dart';
import '../services/api_services.dart';
import '../utils/constants.dart';
import 'map_widget.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  bool _loading = false;
  bool _hasLoadedOnce = false;

  HazardModel? _hazardData;

  String _locationLabel = 'Detecting location...';
  String _selectedPlaceName = 'Selected Location';

  double? _selectedLatitude;
  double? _selectedLongitude;

  Timer? _autoRefreshTimer;
  final TextEditingController _searchController = TextEditingController();

  double? _displayTemperature;
  double? _displayHumidity;
  double? _displayRainfall;

  bool _simulationMode = false;
  String? _simulationDisaster;

  String _selectedLanguage = 'en';

  final Map<String, Map<String, String>> _translations = {
    'en': {
      'current_status': 'CURRENT STATUS',
      'simulation_status': 'SIMULATION STATUS',
      'search_hint': 'Search location on map',
      'demo_simulation': 'Demo Simulation',
      'exit_demo': 'Exit Demo',
      'conditions': 'Conditions',
      'temperature': 'Temperature',
      'humidity': 'Humidity',
      'rainfall': 'Rainfall',
      'live_alerts': 'Live Alerts',
      'current_hazard_risk': 'Current Hazard Risk',
      'confidence_analysis': 'Confidence Analysis',
      'based_on_selected_location': 'Based on selected location',
      'forecast_7day': '7-Day Disaster Forecast',
      'my_location': 'My Location',
      'go': 'Go',
      'all_clear': 'All Clear',
      'moderate_risk': 'Moderate Risk',
      'high_danger': 'High Danger',
      'no_significant_hazards':
          'No significant hazards detected at this selected location.',
      'stay_alert_risk': 'Stay alert — risk detected here.',
      'attention_needed': 'Immediate attention needed — risk is high here.',
      'location_denied': 'Location permission denied',
      'location_not_found': 'Location not found',
      'search_failed': 'Search failed',
      'live_weather_note':
          'Live backend weather values are shown here. Simulation values override them during demo.',
      'no_active_alerts': 'No active alerts for this location.',
      'could_not_fetch': 'Could not fetch hazard data',
      'pull_refresh': 'Pull down to refresh',
      'select_disaster': 'Select Disaster to Simulate',
      'take_me_safe': 'Take me to nearby safety location',
      'stay_here': 'Stay Here',
      'danger_detected': 'Risk Detected',
      'precautions_intro':
          'Take these immediate precautions before moving to a safety location:',
      'updated_for': 'Updated for',
    },
    'ta': {
      'current_status': 'தற்போதைய நிலை',
      'simulation_status': 'சோதனை நிலை',
      'search_hint': 'வரைபடத்தில் இடத்தை தேடவும்',
      'demo_simulation': 'டெமோ சிமுலேஷன்',
      'exit_demo': 'டெமோவை நிறுத்து',
      'conditions': 'நிலைமைகள்',
      'temperature': 'வெப்பநிலை',
      'humidity': 'ஈரப்பதம்',
      'rainfall': 'மழைப்பொழிவு',
      'live_alerts': 'நேரடி எச்சரிக்கைகள்',
      'current_hazard_risk': 'தற்போதைய அபாய நிலை',
      'confidence_analysis': 'நம்பகத்தன்மை பகுப்பாய்வு',
      'based_on_selected_location':
          'தேர்ந்தெடுக்கப்பட்ட இடத்தை அடிப்படையாகக் கொண்டு',
      'forecast_7day': '7 நாள் பேரிடர் முன்னறிவிப்பு',
      'my_location': 'என் இருப்பிடம்',
      'go': 'செல்',
      'all_clear': 'பாதுகாப்பாக உள்ளது',
      'moderate_risk': 'மிதமான அபாயம்',
      'high_danger': 'அதிக அபாயம்',
      'no_significant_hazards':
          'இந்த இடத்தில் குறிப்பிடத்தக்க அபாயம் கண்டறியப்படவில்லை.',
      'stay_alert_risk': 'எச்சரிக்கையாக இருங்கள் — அபாயம் கண்டறியப்பட்டது.',
      'attention_needed': 'உடனடி கவனம் அவசியம் — அபாயம் அதிகமாக உள்ளது.',
      'location_denied': 'இருப்பிட அனுமதி மறுக்கப்பட்டது',
      'location_not_found': 'இடம் கிடைக்கவில்லை',
      'search_failed': 'தேடல் தோல்வியடைந்தது',
      'live_weather_note':
          'லைவ் backend வானிலை மதிப்புகள் இங்கே காட்டப்படும். டெமோவில் simulation மதிப்புகள் மேலிடப்படும்.',
      'no_active_alerts': 'இந்த இடத்திற்கு செயலில் உள்ள எச்சரிக்கை இல்லை.',
      'could_not_fetch': 'அபாய தரவை பெற முடியவில்லை',
      'pull_refresh': 'புதுப்பிக்க கீழே இழுக்கவும்',
      'select_disaster': 'சோதிக்க பேரிடரை தேர்ந்தெடுக்கவும்',
      'take_me_safe': 'அருகிலுள்ள பாதுகாப்பான இடத்துக்கு அழைத்துச் செல்லவும்',
      'stay_here': 'இங்கேயே இரு',
      'danger_detected': 'அபாயம் கண்டறியப்பட்டது',
      'precautions_intro':
          'பாதுகாப்பான இடத்திற்குச் செல்லும் முன் இந்த முன்னெச்சரிக்கைகளை பின்பற்றவும்:',
      'updated_for': 'புதுப்பிக்கப்பட்ட இடம்',
    },
    'hi': {
      'current_status': 'वर्तमान स्थिति',
      'simulation_status': 'सिमुलेशन स्थिति',
      'search_hint': 'मानचित्र पर स्थान खोजें',
      'demo_simulation': 'डेमो सिमुलेशन',
      'exit_demo': 'डेमो बंद करें',
      'conditions': 'स्थिति',
      'temperature': 'तापमान',
      'humidity': 'नमी',
      'rainfall': 'वर्षा',
      'live_alerts': 'लाइव अलर्ट',
      'current_hazard_risk': 'वर्तमान खतरा स्तर',
      'confidence_analysis': 'विश्वसनीयता विश्लेषण',
      'based_on_selected_location': 'चयनित स्थान के आधार पर',
      'forecast_7day': '7-दिवसीय आपदा पूर्वानुमान',
      'my_location': 'मेरा स्थान',
      'go': 'जाएँ',
      'all_clear': 'सब सुरक्षित',
      'moderate_risk': 'मध्यम जोखिम',
      'high_danger': 'उच्च खतरा',
      'no_significant_hazards': 'इस स्थान पर कोई महत्वपूर्ण खतरा नहीं मिला।',
      'stay_alert_risk': 'सतर्क रहें — जोखिम पाया गया है।',
      'attention_needed': 'तुरंत ध्यान दें — जोखिम अधिक है।',
      'location_denied': 'स्थान अनुमति अस्वीकृत',
      'location_not_found': 'स्थान नहीं मिला',
      'search_failed': 'खोज विफल रही',
      'live_weather_note':
          'लाइव backend मौसम मान यहाँ दिखाए जाते हैं। डेमो के दौरान simulation मान इन्हें बदल देंगे।',
      'no_active_alerts': 'इस स्थान के लिए कोई सक्रिय अलर्ट नहीं है।',
      'could_not_fetch': 'खतरे का डेटा प्राप्त नहीं हो सका',
      'pull_refresh': 'रीफ्रेश करने के लिए नीचे खींचें',
      'select_disaster': 'सिमुलेशन के लिए आपदा चुनें',
      'take_me_safe': 'मुझे नज़दीकी सुरक्षित स्थान पर ले चलें',
      'stay_here': 'यहीं रहें',
      'danger_detected': 'जोखिम पाया गया',
      'precautions_intro':
          'सुरक्षित स्थान पर जाने से पहले ये सावधानियाँ बरतें:',
      'updated_for': 'इस स्थान के लिए अपडेट किया गया',
    },
  };

  String tr(String key) {
    return _translations[_selectedLanguage]?[key] ??
        _translations['en']?[key] ??
        key;
  }

  @override
  void initState() {
    super.initState();
    _loadCurrentLocationAndPredict();
    _startAutoRefresh();
  }

  @override
  void dispose() {
    _autoRefreshTimer?.cancel();
    _searchController.dispose();
    super.dispose();
  }

  void _startAutoRefresh() {
    _autoRefreshTimer?.cancel();
    _autoRefreshTimer = Timer.periodic(const Duration(seconds: 30), (_) {
      if (_simulationMode) return;

      if (_selectedLatitude != null && _selectedLongitude != null) {
        _predictForCoordinates(
          _selectedLatitude!,
          _selectedLongitude!,
          placeName: _selectedPlaceName,
          showLoader: false,
        );
      }
    });
  }

  Future<void> _loadCurrentLocationAndPredict() async {
    setState(() {
      _loading = true;
      _simulationMode = false;
      _simulationDisaster = null;
    });

    try {
      LocationPermission permission = await Geolocator.checkPermission();

      if (permission == LocationPermission.denied) {
        permission = await Geolocator.requestPermission();
      }

      if (permission == LocationPermission.denied ||
          permission == LocationPermission.deniedForever) {
        setState(() {
          _loading = false;
          _hasLoadedOnce = true;
          _locationLabel = tr('location_denied');
        });

        _showSnack(tr('location_denied'));
        return;
      }

      final position = await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.high,
      );

      final placeName = await _getReadablePlaceName(
        position.latitude,
        position.longitude,
      );

      await _predictForCoordinates(
        position.latitude,
        position.longitude,
        placeName: placeName,
        showLoader: true,
      );
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _loading = false;
        _hasLoadedOnce = true;
      });

      _showSnack('Could not detect current location');
    }
  }

  Future<void> _predictForCoordinates(
    double latitude,
    double longitude, {
    required String placeName,
    bool showLoader = true,
  }) async {
    if (showLoader) {
      setState(() => _loading = true);
    }

    try {
      final result = await ApiService.predictHazard(latitude, longitude);

      if (!mounted) return;

      setState(() {
        _selectedLatitude = latitude;
        _selectedLongitude = longitude;
        _selectedPlaceName = placeName;
        _locationLabel = placeName;
        _hazardData = result;
        _loading = false;
        _hasLoadedOnce = true;
        _simulationMode = false;
        _simulationDisaster = null;

        _displayTemperature = result?.selectedDayWeather?.temperatureC;
        _displayHumidity = result?.selectedDayWeather?.humidityPercent;
        _displayRainfall = result?.selectedDayWeather?.rainfallMm;
      });
    } catch (e, stack) {
      print('_predictForCoordinates error: $e');
      print(stack);

      if (!mounted) return;
      setState(() {
        _loading = false;
        _hasLoadedOnce = true;
      });

      _showSnack('Failed to fetch live hazard data');
    }
  }

  Future<String> _getReadablePlaceName(
    double latitude,
    double longitude,
  ) async {
    try {
      final placemarks = await placemarkFromCoordinates(latitude, longitude);

      if (placemarks.isNotEmpty) {
        final p = placemarks.first;
        final parts = <String>[
          if ((p.locality ?? '').isNotEmpty) p.locality!,
          if ((p.subAdministrativeArea ?? '').isNotEmpty)
            p.subAdministrativeArea!,
          if ((p.administrativeArea ?? '').isNotEmpty) p.administrativeArea!,
        ];

        if (parts.isNotEmpty) {
          return parts.join(', ');
        }
      }
    } catch (_) {}

    return '${latitude.toStringAsFixed(4)}, ${longitude.toStringAsFixed(4)}';
  }

  Future<void> _searchPlace() async {
    final query = _searchController.text.trim();
    if (query.isEmpty) return;

    FocusScope.of(context).unfocus();
    setState(() => _loading = true);

    try {
      final locations = await locationFromAddress(query);

      if (locations.isEmpty) {
        if (!mounted) return;
        setState(() => _loading = false);
        _showSnack(tr('location_not_found'));
        return;
      }

      final loc = locations.first;

      final placeName = await _getReadablePlaceName(
        loc.latitude,
        loc.longitude,
      );

      await _predictForCoordinates(
        loc.latitude,
        loc.longitude,
        placeName: placeName,
        showLoader: false,
      );

      if (!mounted) return;
      _showSnack('${tr('updated_for')} $placeName');
    } catch (_) {
      if (!mounted) return;
      setState(() => _loading = false);
      _showSnack(tr('search_failed'));
    }
  }

  Future<void> _handleMapTap(LatLng latLng) async {
    final placeName = await _getReadablePlaceName(
      latLng.latitude,
      latLng.longitude,
    );

    await _predictForCoordinates(
      latLng.latitude,
      latLng.longitude,
      placeName: placeName,
      showLoader: true,
    );

    if (!mounted) return;
    _showSnack('${tr('updated_for')} $placeName');
  }

  void _showSnack(String message) {
    if (!mounted) return;

    ScaffoldMessenger.of(context).hideCurrentSnackBar();
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(message)),
    );
  }

  void _openDemoDisasterDialog() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(tr('select_disaster')),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            _demoDisasterTile('Flood'),
            _demoDisasterTile('Cyclone'),
            _demoDisasterTile('Heatwave'),
            _demoDisasterTile('Landslide'),
          ],
        ),
      ),
    );
  }

  Widget _demoDisasterTile(String disaster) {
    return ListTile(
      contentPadding: EdgeInsets.zero,
      title: Text(
        disaster,
        style: const TextStyle(fontWeight: FontWeight.w700),
      ),
      onTap: () {
        Navigator.pop(context);
        _openSimulationInputDialog(disaster);
      },
    );
  }

  void _openSimulationInputDialog(String disaster) {
    final tempController = TextEditingController();
    final humidityController = TextEditingController();
    final rainController = TextEditingController();

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('$disaster Simulation'),
        content: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextField(
                controller: tempController,
                keyboardType: const TextInputType.numberWithOptions(
                  decimal: true,
                ),
                decoration: InputDecoration(
                  labelText: '${tr('temperature')} (°C)',
                ),
              ),
              const SizedBox(height: 12),
              TextField(
                controller: humidityController,
                keyboardType: const TextInputType.numberWithOptions(
                  decimal: true,
                ),
                decoration: InputDecoration(
                  labelText: '${tr('humidity')} (%)',
                ),
              ),
              const SizedBox(height: 12),
              TextField(
                controller: rainController,
                keyboardType: const TextInputType.numberWithOptions(
                  decimal: true,
                ),
                decoration: InputDecoration(
                  labelText: '${tr('rainfall')} (mm)',
                ),
              ),
            ],
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: () {
              final temp = double.tryParse(tempController.text.trim());
              final humidity = double.tryParse(humidityController.text.trim());
              final rainfall = double.tryParse(rainController.text.trim());

              if (temp == null || humidity == null || rainfall == null) {
                _showSnack('Enter valid numeric values');
                return;
              }

              Navigator.pop(context);
              _runSimulation(disaster, temp, humidity, rainfall);
            },
            child: const Text('Simulate'),
          ),
        ],
      ),
    );
  }

  void _runSimulation(
    String disaster,
    double temp,
    double humidity,
    double rainfall,
  ) {
    bool matched = false;

    switch (disaster.toLowerCase()) {
      case 'flood':
        matched = temp >= 20 &&
            temp <= 28 &&
            humidity >= 80 &&
            humidity <= 85 &&
            rainfall >= 180 &&
            rainfall <= 200;
        break;

      case 'cyclone':
        matched = temp >= 26 &&
            temp <= 32 &&
            humidity >= 70 &&
            humidity <= 75 &&
            rainfall >= 100 &&
            rainfall <= 120;
        break;

      case 'heatwave':
        matched = temp < 40 && humidity > 40 && rainfall == 0;
        break;

      case 'landslide':
        matched = temp >= 25 && temp <= 30 && humidity < 80 && rainfall < 100;
        break;
    }

    if (!matched) {
      _showSnack('Conditions do not satisfy $disaster simulation');
      return;
    }

    _triggerSimulationAlert(
      disaster: disaster,
      temperature: temp,
      humidity: humidity,
      rainfall: rainfall,
    );
  }

  Future<void> _triggerSimulationAlert({
    required String disaster,
    required double temperature,
    required double humidity,
    required double rainfall,
  }) async {
    try {
      final position = await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.high,
      );

      final currentPlaceName = await _getReadablePlaceName(
        position.latitude,
        position.longitude,
      );

      SystemSound.play(SystemSoundType.alert);

      final simulationModel = _buildSimulationHazardModel(
        disaster,
        position.latitude,
        position.longitude,
        currentPlaceName,
        temperature,
        humidity,
        rainfall,
      );

      if (!mounted) return;

      setState(() {
        _selectedLatitude = position.latitude;
        _selectedLongitude = position.longitude;
        _selectedPlaceName = currentPlaceName;
        _locationLabel = '$currentPlaceName • Simulation Mode';

        _simulationMode = true;
        _simulationDisaster = disaster;
        _hazardData = simulationModel;
        _displayTemperature = temperature;
        _displayHumidity = humidity;
        _displayRainfall = rainfall;
      });

      _showDangerPopup(disaster);
    } catch (e) {
      _showSnack('Current location not available for simulation');
    }
  }

  HazardModel _buildSimulationHazardModel(
    String disaster,
    double latitude,
    double longitude,
    String placeName,
    double temperature,
    double humidity,
    double rainfall,
  ) {
    final d = disaster.toLowerCase();

    final double cycloneConfidence = d == 'cyclone' ? 94.0 : 18.0;
    final double floodConfidence = d == 'flood' ? 95.0 : 16.0;
    final double heatwaveConfidence = d == 'heatwave' ? 93.0 : 14.0;
    final double landslideConfidence = d == 'landslide' ? 92.0 : 20.0;

    final confidence = Confidence(
      cyclone: cycloneConfidence,
      flood: floodConfidence,
      heatwave: heatwaveConfidence,
      landslide: landslideConfidence,
    );

    final hazardRiskLevels = HazardRiskLevels(
      cyclone: d == 'cyclone' ? 'High' : 'Low',
      flood: d == 'flood' ? 'High' : 'Low',
      heatwave: d == 'heatwave' ? 'High' : 'Low',
      landslide: d == 'landslide' ? 'High' : 'Low',
    );

    final predictions = Predictions(
      cyclone: d == 'cyclone' ? 'Risk' : 'No Risk',
      flood: d == 'flood' ? 'Risk' : 'No Risk',
      heatwave: d == 'heatwave' ? 'Risk' : 'No Risk',
      landslide: d == 'landslide' ? 'Risk' : 'No Risk',
    );

    final maxRiskDisaster = disaster;
    final maxRiskConfidence = d == 'flood'
        ? floodConfidence
        : d == 'cyclone'
            ? cycloneConfidence
            : d == 'heatwave'
                ? heatwaveConfidence
                : landslideConfidence;

    final futureAlerts = List.generate(3, (index) {
      final date = DateTime.now().add(Duration(days: index + 1));
      final dateText =
          '${date.year}-${date.month.toString().padLeft(2, '0')}-${date.day.toString().padLeft(2, '0')}';

      return FutureAlert(
        alertMessage:
            'High risk of $disaster detected. Move to a safer zone immediately.',
        confidence: confidence,
        date: dateText,
        daysRemaining: index + 1,
        hazardRiskLevels: hazardRiskLevels,
        maxRiskConfidence: maxRiskConfidence,
        maxRiskDisaster: maxRiskDisaster,
        overallRiskLevel: 'High',
        predictions: predictions,
      );
    });

    return HazardModel(
      confidence: confidence,
      futureAlerts: futureAlerts,
      hazardRiskLevels: hazardRiskLevels,
      maxRiskConfidence: maxRiskConfidence,
      maxRiskDisaster: maxRiskDisaster,
      overallRiskLevel: 'High',
      predictions: predictions,
      resolvedLocation: ResolvedLocation(
        name: placeName,
        admin2: '',
        admin1: '',
        country: 'India',
        latitude: latitude,
        longitude: longitude,
      ),
      selectedDayWeather: SelectedDayWeather(
        rainfallMm: rainfall,
        temperatureC: temperature,
        humidityPercent: humidity,
        forecastTempMax: temperature,
        forecastTempMin: temperature,
        forecastWindMax: 0,
        surfacePressure: 0,
        windSpeed: 0,
      ),
    );
  }

  List<String> _getPrecautions(String disaster) {
    switch (_selectedLanguage) {
      case 'ta':
        switch (disaster.toLowerCase()) {
          case 'flood':
            return [
              'உயரமான இடத்துக்கு உடனே செல்லுங்கள்.',
              'வெள்ளநீரில் நடக்கவோ வாகனம் ஓட்டவோ வேண்டாம்.',
              'வீட்டுக்குள் நீர் வந்தால் மின்சாரத்தை அணைக்கவும்.',
              'தொலைபேசி, விளக்கு, மருந்து, ஆவணங்கள் தயாராக வைத்திருங்கள்.',
            ];
          case 'cyclone':
            return [
              'வீட்டுக்குள் இருங்கள், ஜன்னல்களிலிருந்து விலகி இருங்கள்.',
              'தொலைபேசி மற்றும் power bank ஐ முழுமையாக சார்ஜ் செய்யுங்கள்.',
              'அவசர பொருட்களை தயார் வைத்திருங்கள்.',
              'அதிகாரப்பூர்வ எச்சரிக்கைகளை பின்பற்றுங்கள்.',
            ];
          case 'heatwave':
            return [
              'அடிக்கடி தண்ணீர் குடிக்கவும்.',
              'நேரடி வெயிலை தவிர்க்கவும்.',
              'குளிரான அல்லது நிழலான இடத்தில் இருங்கள்.',
              'தலைசுற்றல் அல்லது பலவீனம் இருந்தால் கவனமாக இருங்கள்.',
            ];
          case 'landslide':
            return [
              'சரிவுகள் மற்றும் நிலைத்தன்மையற்ற இடங்களில் இருந்து விலகுங்கள்.',
              'மலைப்பாதைகளை தவிர்க்கவும்.',
              'மண் சரிவு, கற்கள் விழுதல் போன்ற அறிகுறிகளை கவனியுங்கள்.',
              'உடனே பாதுகாப்பான தங்குமிடத்துக்குச் செல்லுங்கள்.',
            ];
        }
        break;
      case 'hi':
        switch (disaster.toLowerCase()) {
          case 'flood':
            return [
              'तुरंत ऊँचे स्थान पर जाएँ।',
              'बाढ़ के पानी में न चलें और न वाहन चलाएँ।',
              'घर में पानी घुसे तो बिजली बंद करें।',
              'फोन, टॉर्च, दवा और ज़रूरी दस्तावेज़ तैयार रखें।',
            ];
          case 'cyclone':
            return [
              'घर के अंदर रहें और खिड़कियों से दूर रहें।',
              'फोन और पावर बैंक पूरी तरह चार्ज रखें।',
              'आपातकालीन सामान तैयार रखें।',
              'आधिकारिक चेतावनियों का पालन करें।',
            ];
          case 'heatwave':
            return [
              'बार-बार पानी पिएँ।',
              'सीधी धूप और बाहर की गतिविधि से बचें।',
              'ठंडी या छायादार जगह पर रहें।',
              'चक्कर, सिरदर्द या कमजोरी पर ध्यान दें।',
            ];
          case 'landslide':
            return [
              'ढलानों और अस्थिर ज़मीन से दूर जाएँ।',
              'पहाड़ी रास्तों से बचें।',
              'मिट्टी खिसकने या पत्थर गिरने के संकेत देखें।',
              'तुरंत सुरक्षित स्थान पर जाएँ।',
            ];
        }
        break;
    }

    switch (disaster.toLowerCase()) {
      case 'flood':
        return [
          'Move to higher ground immediately.',
          'Avoid walking or driving through flood water.',
          'Switch off electricity if water enters the house.',
          'Keep phone, torch, medicines, and documents ready.',
        ];
      case 'cyclone':
        return [
          'Stay indoors and away from windows.',
          'Charge phone and power bank fully.',
          'Keep emergency supplies ready.',
          'Follow official warnings and avoid travel.',
        ];
      case 'heatwave':
        return [
          'Drink water frequently.',
          'Avoid direct sunlight and outdoor activity.',
          'Stay in shaded or cool places.',
          'Watch for dizziness, headache, or dehydration.',
        ];
      case 'landslide':
        return [
          'Move away from slopes and unstable ground.',
          'Avoid hill roads and steep areas.',
          'Watch for cracks, falling stones, or soil movement.',
          'Move to a safer shelter immediately.',
        ];
      default:
        return [
          'Stay calm and move to a safe area.',
          'Follow official alerts and safety instructions.',
        ];
    }
  }

  void _showDangerPopup(String disaster) {
    final precautions = _getPrecautions(disaster);

    showDialog(
      context: context,
      barrierDismissible: true,
      builder: (context) => AlertDialog(
        title: Text('$disaster ${tr('danger_detected')}'),
        content: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(
                tr('precautions_intro'),
                style: AppTextStyles.body.copyWith(
                  color: AppColors.textDark,
                  fontSize: 12,
                ),
              ),
              const SizedBox(height: 12),
              ...precautions.map(
                (step) => Padding(
                  padding: const EdgeInsets.only(bottom: 8),
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        '• ',
                        style: TextStyle(
                          fontWeight: FontWeight.w800,
                          color: AppColors.textDark,
                        ),
                      ),
                      Expanded(
                        child: Text(
                          step,
                          style: const TextStyle(
                            fontSize: 13,
                            color: AppColors.textDark,
                            fontWeight: FontWeight.w500,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: Text(tr('stay_here')),
          ),
          ElevatedButton(
            onPressed: () async {
              Navigator.pop(context);
              await _openFixedSafetyLocation();
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: AppColors.red,
              foregroundColor: Colors.white,
            ),
            child: Text(tr('take_me_safe')),
          ),
        ],
      ),
    );
  }

  Future<void> _openFixedSafetyLocation() async {
    final uri = Uri.parse('https://maps.app.goo.gl/vdsvJxCk2AvsFvBY7');

    final launched = await launchUrl(
      uri,
      mode: LaunchMode.externalApplication,
    );

    if (!launched) {
      _showSnack('Could not open Google Maps');
    }
  }

  Color _riskColor(String level) {
    switch (level.toLowerCase()) {
      case 'high':
        return AppColors.red;
      case 'medium':
      case 'moderate':
        return AppColors.moderate;
      case 'low':
        return AppColors.safeGreen;
      default:
        return AppColors.safeGreen;
    }
  }

  IconData _disasterIcon(String disaster) {
    switch (disaster.toLowerCase()) {
      case 'cyclone':
        return Icons.cyclone_rounded;
      case 'flood':
        return Icons.water_rounded;
      case 'heatwave':
        return Icons.wb_sunny_rounded;
      case 'landslide':
        return Icons.landscape_rounded;
      default:
        return Icons.warning_amber_rounded;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: SafeArea(
        child: RefreshIndicator(
          onRefresh: () async {
            if (_simulationMode) {
              _showSnack('Simulation mode active');
              return;
            }

            if (_selectedLatitude != null && _selectedLongitude != null) {
              await _predictForCoordinates(
                _selectedLatitude!,
                _selectedLongitude!,
                placeName: _selectedPlaceName,
                showLoader: false,
              );
            } else {
              await _loadCurrentLocationAndPredict();
            }
          },
          color: AppColors.orange,
          child: SingleChildScrollView(
            physics: const AlwaysScrollableScrollPhysics(),
            child: Column(
              children: [
                _buildHeader(),
                _buildLanguageBar(),
                _buildSearchBar(),
                _buildDemoControls(),
                if (_loading && !_hasLoadedOnce) _buildLoadingCard(),
                if (_hazardData != null) ...[
                  _buildRiskStatusBanner(),
                  const SizedBox(height: 12),
                  _buildMapCard(),
                  const SizedBox(height: 12),
                  _buildWeatherCard(),
                  const SizedBox(height: 12),
                  _buildAlertsWidget(),
                  const SizedBox(height: 12),
                  _buildCurrentRiskCards(),
                  _buildConfidenceAnalysis(),
                  _buildSevenDayForecast(),
                ],
                if (!_loading && _hazardData == null && _hasLoadedOnce)
                  _buildEmptyState(),
                const SizedBox(height: 90),
              ],
            ),
          ),
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        backgroundColor: AppColors.orange,
        onPressed: _loadCurrentLocationAndPredict,
        icon: const Icon(Icons.my_location, color: Colors.white),
        label: Text(
          tr('my_location'),
          style: const TextStyle(
            color: Colors.white,
            fontWeight: FontWeight.w700,
          ),
        ),
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.startFloat,
    );
  }

  Widget _buildHeader() {
    return Padding(
      padding: const EdgeInsets.fromLTRB(16, 14, 16, 8),
      child: Row(
        children: [
          const Icon(
            Icons.location_on_rounded,
            color: AppColors.orange,
            size: 22,
          ),
          const SizedBox(width: 6),
          Expanded(
            child: Text(
              _locationLabel,
              overflow: TextOverflow.ellipsis,
              style: const TextStyle(
                fontWeight: FontWeight.w800,
                fontSize: 16,
                color: AppColors.textDark,
              ),
            ),
          ),
          GestureDetector(
            onTap: () async {
              await _loadCurrentLocationAndPredict();
            },
            child: Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: AppColors.orange.withOpacity(0.12),
                borderRadius: BorderRadius.circular(10),
              ),
              child: const Icon(
                Icons.refresh_rounded,
                color: AppColors.orange,
                size: 20,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildLanguageBar() {
    return Padding(
      padding: const EdgeInsets.fromLTRB(16, 0, 16, 10),
      child: Row(
        children: [
          const Icon(Icons.language, size: 18, color: AppColors.textDark),
          const SizedBox(width: 8),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 12),
            decoration: BoxDecoration(
              color: AppColors.white,
              borderRadius: BorderRadius.circular(14),
            ),
            child: DropdownButton<String>(
              value: _selectedLanguage,
              underline: const SizedBox.shrink(),
              items: const [
                DropdownMenuItem(value: 'en', child: Text('English')),
                DropdownMenuItem(value: 'ta', child: Text('தமிழ்')),
                DropdownMenuItem(value: 'hi', child: Text('हिंदी')),
              ],
              onChanged: (value) {
                if (value == null) return;
                setState(() {
                  _selectedLanguage = value;
                });
              },
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSearchBar() {
    return Padding(
      padding: const EdgeInsets.fromLTRB(16, 4, 16, 12),
      child: Row(
        children: [
          Expanded(
            child: TextField(
              controller: _searchController,
              textInputAction: TextInputAction.search,
              onSubmitted: (_) => _searchPlace(),
              decoration: InputDecoration(
                hintText: tr('search_hint'),
                prefixIcon: const Icon(Icons.search),
                filled: true,
                fillColor: AppColors.white,
                contentPadding: const EdgeInsets.symmetric(vertical: 14),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(16),
                  borderSide: BorderSide.none,
                ),
              ),
            ),
          ),
          const SizedBox(width: 10),
          ElevatedButton(
            onPressed: _loading ? null : _searchPlace,
            style: ElevatedButton.styleFrom(
              backgroundColor: AppColors.orange,
              foregroundColor: Colors.white,
              padding: const EdgeInsets.symmetric(
                horizontal: 18,
                vertical: 16,
              ),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(16),
              ),
            ),
            child: Text(tr('go')),
          ),
        ],
      ),
    );
  }

  Widget _buildDemoControls() {
    return Padding(
      padding: const EdgeInsets.fromLTRB(16, 0, 16, 12),
      child: Row(
        children: [
          Expanded(
            child: ElevatedButton.icon(
              onPressed: _openDemoDisasterDialog,
              style: ElevatedButton.styleFrom(
                backgroundColor: AppColors.darkBlue,
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(vertical: 14),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(16),
                ),
              ),
              icon: const Icon(Icons.science_rounded),
              label: Text(
                tr('demo_simulation'),
                style: const TextStyle(fontWeight: FontWeight.w700),
              ),
            ),
          ),
          if (_simulationMode) ...[
            const SizedBox(width: 10),
            OutlinedButton(
              onPressed: _loadCurrentLocationAndPredict,
              style: OutlinedButton.styleFrom(
                padding: const EdgeInsets.symmetric(
                  horizontal: 14,
                  vertical: 14,
                ),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(16),
                ),
              ),
              child: Text(tr('exit_demo')),
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildLoadingCard() {
    return Container(
      margin: const EdgeInsets.all(16),
      padding: const EdgeInsets.all(32),
      decoration: BoxDecoration(
        color: AppColors.white,
        borderRadius: BorderRadius.circular(24),
        boxShadow: const [
          BoxShadow(color: AppColors.cardShadow, blurRadius: 10),
        ],
      ),
      child: Column(
        children: [
          const CircularProgressIndicator(color: AppColors.orange),
          const SizedBox(height: 16),
          Text(
            'Analysing disaster risk\nfor selected location...',
            textAlign: TextAlign.center,
            style: AppTextStyles.body,
          ),
        ],
      ),
    );
  }

  Widget _buildEmptyState() {
    return Container(
      margin: const EdgeInsets.all(16),
      padding: const EdgeInsets.all(32),
      decoration: BoxDecoration(
        color: AppColors.white,
        borderRadius: BorderRadius.circular(24),
      ),
      child: Column(
        children: [
          const Icon(
            Icons.cloud_off_rounded,
            color: AppColors.textGrey,
            size: 48,
          ),
          const SizedBox(height: 16),
          Text(
            tr('could_not_fetch'),
            style: const TextStyle(
              fontWeight: FontWeight.w700,
              color: AppColors.textDark,
              fontSize: 16,
            ),
          ),
          const SizedBox(height: 8),
          Text(
            tr('pull_refresh'),
            style: AppTextStyles.body,
          ),
        ],
      ),
    );
  }

  Widget _buildRiskStatusBanner() {
    final data = _hazardData!;
    final level = data.overallRiskLevel;
    final color = _riskColor(level);
    final icon = _disasterIcon(data.maxRiskDisaster);

    String statusText;
    String subText;

    if (level.toLowerCase() == 'low') {
      statusText = tr('all_clear');
      subText = tr('no_significant_hazards');
    } else if (level.toLowerCase() == 'medium' ||
        level.toLowerCase() == 'moderate') {
      statusText = tr('moderate_risk');
      subText = tr('stay_alert_risk');
    } else {
      statusText = tr('high_danger');
      subText = tr('attention_needed');
    }

    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 16),
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [color, color.withOpacity(0.75)],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(24),
        boxShadow: [
          BoxShadow(
            color: color.withOpacity(0.3),
            blurRadius: 12,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Row(
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  _simulationMode
                      ? tr('simulation_status')
                      : tr('current_status'),
                  style: const TextStyle(
                    color: Colors.white70,
                    fontSize: 11,
                    fontWeight: FontWeight.w700,
                    letterSpacing: 1.2,
                  ),
                ),
                const SizedBox(height: 8),
                Text(
                  statusText,
                  style: const TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.w900,
                    fontSize: 28,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  subText,
                  style: const TextStyle(
                    color: Colors.white70,
                    fontSize: 12,
                  ),
                ),
                const SizedBox(height: 8),
                Text(
                  '${data.maxRiskDisaster}  •  ${data.maxRiskConfidence.toStringAsFixed(1)}% confidence',
                  style: const TextStyle(
                    color: Colors.white60,
                    fontSize: 11,
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ],
            ),
          ),
          Icon(icon, color: Colors.white, size: 52),
        ],
      ),
    );
  }

  Widget _buildMapCard() {
    if (_selectedLatitude == null || _selectedLongitude == null) {
      return const SizedBox.shrink();
    }

    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 16),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(24),
        boxShadow: const [
          BoxShadow(color: AppColors.cardShadow, blurRadius: 10),
        ],
      ),
      child: ClipRRect(
        borderRadius: const BorderRadius.all(Radius.circular(24)),
        child: MapWidget(
          key: ValueKey(
            '${_selectedLatitude}_${_selectedLongitude}_${_hazardData?.maxRiskDisaster}_${_hazardData?.maxRiskConfidence}_${_simulationMode}_${_simulationDisaster}',
          ),
          hazardData: _hazardData,
          latitude: _selectedLatitude!,
          longitude: _selectedLongitude!,
          locationName: _selectedPlaceName,
          onTap: _handleMapTap,
        ),
      ),
    );
  }

  Widget _buildWeatherCard() {
    final tempText = _displayTemperature != null
        ? '${_displayTemperature!.toStringAsFixed(1)} °C'
        : '--';
    final humidityText = _displayHumidity != null
        ? '${_displayHumidity!.toStringAsFixed(1)} %'
        : '--';
    final rainfallText = _displayRainfall != null
        ? '${_displayRainfall!.toStringAsFixed(1)} mm'
        : '--';

    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 16),
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: AppColors.white,
        borderRadius: BorderRadius.circular(20),
        boxShadow: const [
          BoxShadow(color: AppColors.cardShadow, blurRadius: 8),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            tr('conditions'),
            style: const TextStyle(
              fontWeight: FontWeight.w800,
              fontSize: 16,
              color: AppColors.textDark,
            ),
          ),
          const SizedBox(height: 12),
          Row(
            children: [
              Expanded(
                child: _weatherItem(
                  icon: Icons.thermostat_rounded,
                  label: tr('temperature'),
                  value: tempText,
                  color: AppColors.orange,
                ),
              ),
              const SizedBox(width: 10),
              Expanded(
                child: _weatherItem(
                  icon: Icons.water_drop_rounded,
                  label: tr('humidity'),
                  value: humidityText,
                  color: AppColors.blue,
                ),
              ),
              const SizedBox(width: 10),
              Expanded(
                child: _weatherItem(
                  icon: Icons.grain_rounded,
                  label: tr('rainfall'),
                  value: rainfallText,
                  color: AppColors.moderate,
                ),
              ),
            ],
          ),
          const SizedBox(height: 10),
          Text(
            tr('live_weather_note'),
            style: AppTextStyles.body.copyWith(fontSize: 11),
          ),
        ],
      ),
    );
  }

  Widget _weatherItem({
    required IconData icon,
    required String label,
    required String value,
    required Color color,
  }) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: color.withOpacity(0.08),
        borderRadius: BorderRadius.circular(16),
      ),
      child: Column(
        children: [
          Icon(icon, color: color, size: 24),
          const SizedBox(height: 8),
          Text(
            label,
            textAlign: TextAlign.center,
            style: const TextStyle(
              fontSize: 11,
              fontWeight: FontWeight.w700,
              color: AppColors.textDark,
            ),
          ),
          const SizedBox(height: 4),
          Text(
            value,
            textAlign: TextAlign.center,
            style: TextStyle(
              fontSize: 12,
              fontWeight: FontWeight.w800,
              color: color,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildAlertsWidget() {
    final data = _hazardData!;
    final List<Map<String, dynamic>> alerts = [];

    void addAlert(
      String type,
      String risk,
      double confidence,
      IconData icon,
      Color color,
    ) {
      if (risk.toLowerCase() != 'low') {
        final msg = risk.toLowerCase() == 'high'
            ? '$type risk is critical at this location. Take immediate precautions.'
            : 'Moderate $type activity detected here. Stay alert and prepared.';

        alerts.add({
          'type': '$type Alert',
          'message': msg,
          'color': color,
          'icon': icon,
          'confidence': confidence,
        });
      }
    }

    addAlert(
      'Cyclone',
      data.hazardRiskLevels.cyclone,
      data.confidence.cyclone,
      Icons.cyclone_rounded,
      AppColors.blue,
    );
    addAlert(
      'Flood',
      data.hazardRiskLevels.flood,
      data.confidence.flood,
      Icons.water_rounded,
      AppColors.blue,
    );
    addAlert(
      'Heatwave',
      data.hazardRiskLevels.heatwave,
      data.confidence.heatwave,
      Icons.wb_sunny_rounded,
      AppColors.orange,
    );
    addAlert(
      'Landslide',
      data.hazardRiskLevels.landslide,
      data.confidence.landslide,
      Icons.landscape_rounded,
      AppColors.moderate,
    );

    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 16),
      decoration: BoxDecoration(
        color: AppColors.white,
        borderRadius: BorderRadius.circular(20),
        boxShadow: const [
          BoxShadow(color: AppColors.cardShadow, blurRadius: 8),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
            child: Text(
              tr('live_alerts'),
              style: const TextStyle(
                fontWeight: FontWeight.w800,
                fontSize: 16,
                color: AppColors.textDark,
              ),
            ),
          ),
          if (alerts.isEmpty)
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              child: Text(
                tr('no_active_alerts'),
                style: const TextStyle(
                  color: AppColors.textDark,
                  fontSize: 13,
                  fontWeight: FontWeight.w500,
                ),
              ),
            )
          else
            ...alerts.map((alert) {
              final color = alert['color'] as Color;

              return Padding(
                padding: const EdgeInsets.fromLTRB(16, 0, 16, 10),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Container(
                      width: 38,
                      height: 38,
                      decoration: BoxDecoration(
                        color: color.withOpacity(0.12),
                        borderRadius: BorderRadius.circular(10),
                      ),
                      child: Icon(
                        alert['icon'] as IconData,
                        color: color,
                        size: 18,
                      ),
                    ),
                    const SizedBox(width: 10),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            children: [
                              Expanded(
                                child: Text(
                                  alert['type'] as String,
                                  style: const TextStyle(
                                    fontWeight: FontWeight.w700,
                                    fontSize: 13,
                                    color: AppColors.textDark,
                                  ),
                                ),
                              ),
                              Text(
                                '${(alert['confidence'] as double).toStringAsFixed(1)}%',
                                style: TextStyle(
                                  color: color,
                                  fontWeight: FontWeight.w800,
                                  fontSize: 11,
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 2),
                          Text(
                            alert['message'] as String,
                            style: AppTextStyles.body.copyWith(fontSize: 11),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              );
            }),
          const SizedBox(height: 4),
        ],
      ),
    );
  }

  Widget _buildCurrentRiskCards() {
    final r = _hazardData!.hazardRiskLevels;
    final c = _hazardData!.confidence;

    final hazards = [
      {
        'label': 'Cyclone',
        'risk': r.cyclone,
        'confidence': c.cyclone,
        'icon': Icons.cyclone_rounded,
      },
      {
        'label': 'Flood',
        'risk': r.flood,
        'confidence': c.flood,
        'icon': Icons.water_rounded,
      },
      {
        'label': 'Heatwave',
        'risk': r.heatwave,
        'confidence': c.heatwave,
        'icon': Icons.wb_sunny_rounded,
      },
      {
        'label': 'Landslide',
        'risk': r.landslide,
        'confidence': c.landslide,
        'icon': Icons.landscape_rounded,
      },
    ];

    return Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            tr('current_hazard_risk'),
            style: const TextStyle(
              fontWeight: FontWeight.w800,
              fontSize: 17,
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
              childAspectRatio: 1.45,
            ),
            itemCount: hazards.length,
            itemBuilder: (_, i) {
              final h = hazards[i];
              final color = _riskColor(h['risk'] as String);

              return Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: AppColors.white,
                  borderRadius: BorderRadius.circular(20),
                  boxShadow: const [
                    BoxShadow(color: AppColors.cardShadow, blurRadius: 8),
                  ],
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Icon(h['icon'] as IconData, color: color, size: 26),
                        Container(
                          padding: const EdgeInsets.symmetric(
                            horizontal: 8,
                            vertical: 3,
                          ),
                          decoration: BoxDecoration(
                            color: color.withOpacity(0.12),
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: Text(
                            h['risk'] as String,
                            style: TextStyle(
                              color: color,
                              fontWeight: FontWeight.w800,
                              fontSize: 11,
                            ),
                          ),
                        ),
                      ],
                    ),
                    const Spacer(),
                    Text(
                      h['label'] as String,
                      style: const TextStyle(
                        fontWeight: FontWeight.w700,
                        fontSize: 14,
                        color: AppColors.textDark,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      '${(h['confidence'] as double).toStringAsFixed(1)}% confidence',
                      style: AppTextStyles.body.copyWith(fontSize: 11),
                    ),
                    const SizedBox(height: 6),
                    ClipRRect(
                      borderRadius: BorderRadius.circular(4),
                      child: LinearProgressIndicator(
                        value: (h['confidence'] as double) / 100,
                        backgroundColor: AppColors.lightGrey,
                        color: color,
                        minHeight: 5,
                      ),
                    ),
                  ],
                ),
              );
            },
          ),
        ],
      ),
    );
  }

  Widget _buildConfidenceAnalysis() {
    final c = _hazardData!.confidence;
    final p = _hazardData!.predictions;

    final items = [
      {
        'label': 'Cyclone',
        'value': c.cyclone,
        'prediction': p.cyclone,
        'icon': Icons.cyclone_rounded,
      },
      {
        'label': 'Flood',
        'value': c.flood,
        'prediction': p.flood,
        'icon': Icons.water_rounded,
      },
      {
        'label': 'Heatwave',
        'value': c.heatwave,
        'prediction': p.heatwave,
        'icon': Icons.wb_sunny_rounded,
      },
      {
        'label': 'Landslide',
        'value': c.landslide,
        'prediction': p.landslide,
        'icon': Icons.landscape_rounded,
      },
    ];

    return Container(
      margin: const EdgeInsets.all(16),
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: AppColors.white,
        borderRadius: BorderRadius.circular(24),
        boxShadow: const [
          BoxShadow(color: AppColors.cardShadow, blurRadius: 10),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            tr('confidence_analysis'),
            style: const TextStyle(
              fontWeight: FontWeight.w800,
              fontSize: 17,
              color: AppColors.textDark,
            ),
          ),
          const SizedBox(height: 4),
          Text(
            tr('based_on_selected_location'),
            style: AppTextStyles.body.copyWith(fontSize: 12),
          ),
          const SizedBox(height: 16),
          ...items.map((item) {
            final isRisk = (item['prediction'] as String) == 'Risk';
            final color = isRisk ? AppColors.red : AppColors.safeGreen;
            final value = item['value'] as double;

            return Padding(
              padding: const EdgeInsets.only(bottom: 14),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Icon(item['icon'] as IconData, size: 16, color: color),
                      const SizedBox(width: 6),
                      Text(
                        item['label'] as String,
                        style: const TextStyle(
                          fontWeight: FontWeight.w600,
                          fontSize: 13,
                          color: AppColors.textDark,
                        ),
                      ),
                      const Spacer(),
                      Container(
                        padding: const EdgeInsets.symmetric(
                          horizontal: 6,
                          vertical: 2,
                        ),
                        decoration: BoxDecoration(
                          color: color.withOpacity(0.1),
                          borderRadius: BorderRadius.circular(6),
                        ),
                        child: Text(
                          item['prediction'] as String,
                          style: TextStyle(
                            color: color,
                            fontWeight: FontWeight.w700,
                            fontSize: 10,
                          ),
                        ),
                      ),
                      const SizedBox(width: 8),
                      Text(
                        '${value.toStringAsFixed(1)}%',
                        style: TextStyle(
                          fontWeight: FontWeight.w700,
                          fontSize: 13,
                          color: color,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 6),
                  ClipRRect(
                    borderRadius: BorderRadius.circular(6),
                    child: LinearProgressIndicator(
                      value: value / 100,
                      backgroundColor: AppColors.lightGrey,
                      color: color,
                      minHeight: 8,
                    ),
                  ),
                ],
              ),
            );
          }),
        ],
      ),
    );
  }

  Widget _buildSevenDayForecast() {
    final alerts = _hazardData!.futureAlerts;
    if (alerts.isEmpty) return const SizedBox.shrink();

    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            tr('forecast_7day'),
            style: const TextStyle(
              fontWeight: FontWeight.w800,
              fontSize: 17,
              color: AppColors.textDark,
            ),
          ),
          const SizedBox(height: 12),
          ...alerts.map((alert) => _buildForecastCard(alert)).toList(),
        ],
      ),
    );
  }

  Widget _buildForecastCard(FutureAlert alert) {
    final overallColor = _riskColor(alert.overallRiskLevel);
    final icon = _disasterIcon(alert.maxRiskDisaster);

    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: AppColors.white,
        borderRadius: BorderRadius.circular(18),
        boxShadow: const [
          BoxShadow(color: AppColors.cardShadow, blurRadius: 8),
        ],
      ),
      child: Row(
        children: [
          Icon(icon, color: overallColor),
          const SizedBox(width: 10),
          Expanded(
            child: Text(
              '${alert.date} • ${alert.alertMessage}',
              style: const TextStyle(
                color: AppColors.textDark,
                fontWeight: FontWeight.w600,
                fontSize: 12,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
