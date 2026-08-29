import 'game.dart';

/// A card game with deck size and quick-play stats.
class CardGame extends Game {
  final int deckSize;
  final int avgPlayTimeMinutes;

  CardGame({
    required super.id,
    required super.title,
    required super.publisher,
    required super.releaseYear,
    required super.genre,
    required this.deckSize,
    required this.avgPlayTimeMinutes,
    super.isAvailable,
  });

  @override
  void describe() {
    print('[$id] $title — Card Game');
    print('  Publisher: $publisher | Year: $releaseYear | Genre: $genre');
    print('  Deck size: $deckSize cards | Avg playtime: ${avgPlayTimeMinutes}m');
    print('  Status: $availabilityStatus');
  }
}
