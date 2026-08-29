import 'game.dart';

/// A library member who can borrow games.
class Member {
  final String memberId;
  final String name;
  final List<Game> borrowedGames;

  Member({required this.memberId, required this.name}) : borrowedGames = [];

  void showBorrowedGames() {
    if (borrowedGames.isEmpty) {
      print('  $name has no borrowed games.');
      return;
    }
    print('  $name has borrowed:');
    for (final game in borrowedGames) {
      print('    • ${game.title}');
    }
  }
}
