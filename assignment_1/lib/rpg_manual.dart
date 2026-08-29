import 'game.dart';

/// A tabletop RPG sourcebook or manual.
class RPGManual extends Game {
  final String edition;
  final int pageCount;

  RPGManual({
    required super.id,
    required super.title,
    required super.publisher,
    required super.releaseYear,
    required super.genre,
    required this.edition,
    required this.pageCount,
    super.isAvailable,
  });

  @override
  void describe() {
    print('[$id] $title — RPG Manual');
    print('  Publisher: $publisher | Year: $releaseYear | Genre: $genre');
    print('  Edition: $edition | Pages: $pageCount');
    print('  Status: $availabilityStatus');
  }
}
