import 'exoplanet.dart';
import 'mock_api.dart';

/// Service layer that turns raw API payloads into typed models.
class ExoplanetService {
  final MockApiClient _client;

  ExoplanetService(this._client);

  /// Returns null when the API sends back an empty payload.
  Future<Exoplanet?> fetchExoplanet(String id) async {
    final raw = await _client.fetchRawRecord(id);
    if (raw == null) return null;
    return Exoplanet.fromJson(raw);
  }

  /// Fetches several records in parallel and skips the nulls.
  Future<List<Exoplanet>> fetchMany(List<String> ids) async {
    final results = await Future.wait(ids.map(fetchExoplanet));
    return results.whereType<Exoplanet>().toList();
  }
}
