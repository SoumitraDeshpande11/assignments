/// Data model for an exoplanet record.
/// Several fields are nullable because real catalog data is incomplete.
class Exoplanet {
  final String id;
  final String name;
  final String hostStar;
  final int? discoveryYear;
  final double? massEarths;
  final double orbitalPeriodDays;

  Exoplanet({
    required this.id,
    required this.name,
    required this.hostStar,
    this.discoveryYear,
    this.massEarths,
    required this.orbitalPeriodDays,
  });

  factory Exoplanet.fromJson(Map<String, dynamic> json) {
    return Exoplanet(
      id: json['id'] as String,
      name: json['name'] as String,
      hostStar: json['hostStar'] as String,
      discoveryYear: json['discoveryYear'] as int?,
      massEarths: (json['massEarths'] as num?)?.toDouble(),
      orbitalPeriodDays: (json['orbitalPeriodDays'] as num).toDouble(),
    );
  }

  /// Null-safe display helpers with fallbacks.
  String get discoveryLabel => discoveryYear != null ? '$discoveryYear' : 'unknown';
  String get massLabel => massEarths != null ? '${massEarths!.toStringAsFixed(2)} Earth masses' : 'not measured';

  void display() {
    print('[$id] $name (orbits $hostStar)');
    print('  Discovery year: $discoveryLabel');
    print('  Mass: $massLabel');
    print('  Orbital period: ${orbitalPeriodDays.toStringAsFixed(1)} days');
  }
}
