import 'game.dart';
import 'member.dart';
import 'board_game.dart';

/// Central controller for the board game lending library.
class GameLibrary {
  final List<Game> catalog = [];
  final Map<String, Member> members = {};

  void addGame(Game game) => catalog.add(game);

  void registerMember(Member member) => members[member.memberId] = member;

  void listCatalog() {
    print('\n=== GAME CATALOG ===');
    for (int i = 0; i < catalog.length; i++) {
      print('${i + 1}.');
      catalog[i].describe();
    }
  }

  Game? findGameById(String id) {
    for (final game in catalog) {
      if (game.id == id) return game;
    }
    return null;
  }

  bool borrowGame({required String memberId, required String gameId}) {
    final member = members[memberId];
    final game = findGameById(gameId);

    if (member == null) {
      print('Member not found.');
      return false;
    }
    if (game == null) {
      print('Game not found.');
      return false;
    }
    if (!game.isAvailable) {
      print('${game.title} is already borrowed.');
      return false;
    }

    game.isAvailable = false;
    member.borrowedGames.add(game);
    print('${member.name} borrowed ${game.title}.');
    return true;
  }

  bool returnGame({required String memberId, required String gameId}) {
    final member = members[memberId];
    final game = findGameById(gameId);

    if (member == null || game == null) {
      print('Invalid member or game.');
      return false;
    }
    if (!member.borrowedGames.contains(game)) {
      print('${member.name} did not borrow ${game.title}.');
      return false;
    }

    game.isAvailable = true;
    member.borrowedGames.remove(game);
    print('${member.name} returned ${game.title}.');
    return true;
  }

  void recommendForPlayers(int playerCount) {
    print('\n=== RECOMMENDATIONS FOR $playerCount PLAYERS ===');
    bool found = false;
    int index = 0;

    while (index < catalog.length) {
      final game = catalog[index];
      if (game is BoardGame &&
          game.isAvailable &&
          game.playerCountMin <= playerCount &&
          game.playerCountMax >= playerCount) {
        print('  • ${game.title} (${game.playerRange} players, ${game.playTimeMinutes}m)');
        found = true;
      }
      index++;
    }

    if (!found) {
      print('  No available board games found for $playerCount players.');
    }
  }
}
