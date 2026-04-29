import 'dart:convert';
import 'package:http/http.dart' as http;
import '../model/hazard_model.dart';
import '../utils/constants.dart';

class ApiService {
  static Future<HazardModel?> predictHazard(
    double latitude,
    double longitude,
  ) async {
    try {
      final uri = Uri.parse(
        '${AppStrings.apiBaseUrl}${AppStrings.predictEndpoint}',
      );

      print('API URL: $uri');
      print('Sending latitude=$latitude longitude=$longitude');

      final response = await http
          .post(
            uri,
            headers: const {
              'Content-Type': 'application/json',
              'Accept': 'application/json',
            },
            body: jsonEncode({
              'latitude': latitude,
              'longitude': longitude,
            }),
          )
          .timeout(const Duration(seconds: 30));

      print('Status code: ${response.statusCode}');
      print('Raw response body: ${response.body}');

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return HazardModel.fromJson(data);
      }

      if (response.statusCode == 405) {
        throw Exception(
          '405 Method Not Allowed: backend still not accepting POST on /predict',
        );
      }

      throw Exception(
        'API failed with status ${response.statusCode}: ${response.body}',
      );
    } catch (e, stack) {
      print('predictHazard error: $e');
      print(stack);
      rethrow;
    }
  }
}
