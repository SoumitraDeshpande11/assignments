/// Simulated failure thrown by the mock API.
class ApiException implements Exception {
  final String message;
  final int statusCode;

  ApiException(this.message, this.statusCode);

  @override
  String toString() => 'ApiException($statusCode): $message';
}

/// A fake remote API for the exoplanet catalog.
/// Delays, null payloads, and exceptions are baked in so the caller
/// must handle every async failure mode.
class MockApiClient {
  Future<Map<String, dynamic>?> fetchRawRecord(String id) async {
    // Simulated network latency.
    await Future.delayed(const Duration(milliseconds: 300));

    switch (id) {
      case 'proxima-b':
        return {
          'id': 'proxima-b',
          'name': 'Proxima Centauri b',
          'hostStar': 'Proxima Centauri',
          'discoveryYear': 2016,
          'massEarths': 1.27,
          'orbitalPeriodDays': 11.2,
        };
      case 'trappist-1e':
        // Missing optional fields — the model must tolerate nulls.
        return {
          'id': 'trappist-1e',
          'name': 'TRAPPIST-1e',
          'hostStar': 'TRAPPIST-1',
          'discoveryYear': null,
          'massEarths': null,
          'orbitalPeriodDays': 6.1,
        };
      case 'kepler-22b':
        // Simulated lost packet: the API returns null.
        return null;
      case 'hd-40307g':
        // Simulated server failure.
        throw ApiException('gateway timeout', 504);
      default:
        throw ApiException('record not found', 404);
    }
  }
}
