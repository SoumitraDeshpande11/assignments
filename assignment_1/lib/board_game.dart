import 'game.dart';

/// A physical board game with player count and complexity details.
class BoardGame extends Game {
  final int playerCountMin;
  final int playerCountMax;
  final int playTimeMinutes;
  final double complexityRating;

  BoardGame({
    required super.id,
    required super.title,
    required super.publisher,
    required super.releaseYear,
    required super.genre,
    required this.playerCountMin,
    required this.playerCountMax,
    required this.playTimeMinutes,
    required this.complexityRating,
    super.isAvailable,
  });

  String get playerRange => '$playerCountMin-$playerCountMax';

  @override
  void describe() {
    print('[$id] $title — Board Game');
    print('  Publisher: $publisher | Year: $releaseYear | Genre: $genre');
    print('  Players: $playerRange | Playtime: ${playTimeMinutes}m | Complexity: $complexityRating/5');
    print('  Status: $availabilityStatus');
  }
}
