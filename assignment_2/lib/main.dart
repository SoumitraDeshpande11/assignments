import 'exoplanet_service.dart';
import 'mock_api.dart';

void main() async {
  final service = ExoplanetService(MockApiClient());

  final ids = ['proxima-b', 'trappist-1e', 'kepler-22b', 'hd-40307g'];

  print('=== FETCHING EXOPLANET RECORDS ===');
  for (final id in ids) {
    try {
      final planet = await service.fetchExoplanet(id);
      if (planet == null) {
        print('[$id] API returned a null payload — nothing to display.');
      } else {
        planet.display();
      }
    } on ApiException catch (e) {
      print('[$id] API error: ${e.message} (HTTP ${e.statusCode})');
    } catch (e) {
      print('[$id] Unexpected error: $e');
    }
    print('');
  }

  print('=== PARALLEL BATCH FETCH ===');
  try {
    final planets = await service.fetchMany(['proxima-b', 'trappist-1e', 'kepler-22b']);
    print('Fetched ${planets.length} valid records:');
    for (final planet in planets) {
      print('  • ${planet.name} — discovery: ${planet.discoveryLabel}');
    }
  } catch (e) {
    print('Batch fetch failed: $e');
  }
}
