class HazardModel {
  final Confidence confidence;
  final List<FutureAlert> futureAlerts;
  final HazardRiskLevels hazardRiskLevels;
  final double maxRiskConfidence;
  final String maxRiskDisaster;
  final String overallRiskLevel;
  final Predictions predictions;
  final ResolvedLocation resolvedLocation;
  final SelectedDayWeather? selectedDayWeather;

  HazardModel({
    required this.confidence,
    required this.futureAlerts,
    required this.hazardRiskLevels,
    required this.maxRiskConfidence,
    required this.maxRiskDisaster,
    required this.overallRiskLevel,
    required this.predictions,
    required this.resolvedLocation,
    required this.selectedDayWeather,
  });

  factory HazardModel.fromJson(Map<String, dynamic> json) {
    return HazardModel(
      confidence: Confidence.fromJson(
        Map<String, dynamic>.from(json['confidence'] ?? {}),
      ),
      futureAlerts: (json['future_alerts'] as List<dynamic>? ?? [])
          .map((e) => FutureAlert.fromJson(Map<String, dynamic>.from(e)))
          .toList(),
      hazardRiskLevels: HazardRiskLevels.fromJson(
        Map<String, dynamic>.from(json['hazard_risk_levels'] ?? {}),
      ),
      maxRiskConfidence: _toDouble(json['max_risk_confidence']),
      maxRiskDisaster: json['max_risk_disaster']?.toString() ?? '',
      overallRiskLevel: json['overall_risk_level']?.toString() ?? '',
      predictions: Predictions.fromJson(
        Map<String, dynamic>.from(json['predictions'] ?? {}),
      ),
      resolvedLocation: ResolvedLocation.fromJson(
        Map<String, dynamic>.from(json['resolved_location'] ?? {}),
      ),
      selectedDayWeather: json['selected_day_weather'] != null
          ? SelectedDayWeather.fromJson(
              Map<String, dynamic>.from(json['selected_day_weather']),
            )
          : null,
    );
  }
}

class Confidence {
  final double cyclone;
  final double flood;
  final double heatwave;
  final double landslide;

  Confidence({
    required this.cyclone,
    required this.flood,
    required this.heatwave,
    required this.landslide,
  });

  factory Confidence.fromJson(Map<String, dynamic> json) {
    return Confidence(
      cyclone: _toDouble(json['Cyclone']),
      flood: _toDouble(json['Flood']),
      heatwave: _toDouble(json['Heatwave']),
      landslide: _toDouble(json['Landslide']),
    );
  }
}

class HazardRiskLevels {
  final String cyclone;
  final String flood;
  final String heatwave;
  final String landslide;

  HazardRiskLevels({
    required this.cyclone,
    required this.flood,
    required this.heatwave,
    required this.landslide,
  });

  factory HazardRiskLevels.fromJson(Map<String, dynamic> json) {
    return HazardRiskLevels(
      cyclone: json['Cyclone']?.toString() ?? 'Low',
      flood: json['Flood']?.toString() ?? 'Low',
      heatwave: json['Heatwave']?.toString() ?? 'Low',
      landslide: json['Landslide']?.toString() ?? 'Low',
    );
  }
}

class Predictions {
  final String cyclone;
  final String flood;
  final String heatwave;
  final String landslide;

  Predictions({
    required this.cyclone,
    required this.flood,
    required this.heatwave,
    required this.landslide,
  });

  factory Predictions.fromJson(Map<String, dynamic> json) {
    return Predictions(
      cyclone: json['Cyclone']?.toString() ?? 'No Risk',
      flood: json['Flood']?.toString() ?? 'No Risk',
      heatwave: json['Heatwave']?.toString() ?? 'No Risk',
      landslide: json['Landslide']?.toString() ?? 'No Risk',
    );
  }
}

class ResolvedLocation {
  final String name;
  final String admin2;
  final String admin1;
  final String country;
  final double latitude;
  final double longitude;

  ResolvedLocation({
    required this.name,
    required this.admin2,
    required this.admin1,
    required this.country,
    required this.latitude,
    required this.longitude,
  });

  factory ResolvedLocation.fromJson(Map<String, dynamic> json) {
    return ResolvedLocation(
      name: json['name']?.toString() ?? '',
      admin2: json['admin2']?.toString() ?? '',
      admin1: json['admin1']?.toString() ?? '',
      country: json['country']?.toString() ?? '',
      latitude: _toDouble(json['latitude']),
      longitude: _toDouble(json['longitude']),
    );
  }
}

class FutureAlert {
  final String alertMessage;
  final Confidence confidence;
  final String date;
  final int daysRemaining;
  final HazardRiskLevels hazardRiskLevels;
  final double maxRiskConfidence;
  final String maxRiskDisaster;
  final String overallRiskLevel;
  final Predictions predictions;

  FutureAlert({
    required this.alertMessage,
    required this.confidence,
    required this.date,
    required this.daysRemaining,
    required this.hazardRiskLevels,
    required this.maxRiskConfidence,
    required this.maxRiskDisaster,
    required this.overallRiskLevel,
    required this.predictions,
  });

  factory FutureAlert.fromJson(Map<String, dynamic> json) {
    return FutureAlert(
      alertMessage: json['alert_message']?.toString() ?? '',
      confidence: Confidence.fromJson(
        Map<String, dynamic>.from(json['confidence'] ?? {}),
      ),
      date: json['date']?.toString() ?? '',
      daysRemaining: _toInt(json['days_remaining']),
      hazardRiskLevels: HazardRiskLevels.fromJson(
        Map<String, dynamic>.from(json['hazard_risk_levels'] ?? {}),
      ),
      maxRiskConfidence: _toDouble(json['max_risk_confidence']),
      maxRiskDisaster: json['max_risk_disaster']?.toString() ?? '',
      overallRiskLevel: json['overall_risk_level']?.toString() ?? '',
      predictions: Predictions.fromJson(
        Map<String, dynamic>.from(json['predictions'] ?? {}),
      ),
    );
  }
}

class SelectedDayWeather {
  final double rainfallMm;
  final double temperatureC;
  final double humidityPercent;
  final double forecastTempMax;
  final double forecastTempMin;
  final double forecastWindMax;
  final double surfacePressure;
  final double windSpeed;

  SelectedDayWeather({
    required this.rainfallMm,
    required this.temperatureC,
    required this.humidityPercent,
    required this.forecastTempMax,
    required this.forecastTempMin,
    required this.forecastWindMax,
    required this.surfacePressure,
    required this.windSpeed,
  });

  factory SelectedDayWeather.fromJson(Map<String, dynamic> json) {
    return SelectedDayWeather(
      rainfallMm: _toDouble(json['Rainfall (mm)']),
      temperatureC: _toDouble(json['Temperature (°C)']),
      humidityPercent: _toDouble(json['Humidity (%)']),
      forecastTempMax: _toDouble(json['Forecast Temp Max']),
      forecastTempMin: _toDouble(json['Forecast Temp Min']),
      forecastWindMax: _toDouble(json['Forecast Wind Max']),
      surfacePressure: _toDouble(json['Surface Pressure']),
      windSpeed: _toDouble(json['Wind Speed']),
    );
  }
}

double _toDouble(dynamic value) {
  if (value == null) return 0.0;
  if (value is double) return value;
  if (value is int) return value.toDouble();
  if (value is num) return value.toDouble();
  return double.tryParse(value.toString()) ?? 0.0;
}

int _toInt(dynamic value) {
  if (value == null) return 0;
  if (value is int) return value;
  if (value is double) return value.toInt();
  if (value is num) return value.toInt();
  return int.tryParse(value.toString()) ?? 0;
}
