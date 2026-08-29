import 'board_game.dart';
import 'card_game.dart';
import 'rpg_manual.dart';
import 'member.dart';
import 'game_library.dart';
import 'late_fee_calculator.dart';

void main() {
  final library = GameLibrary();

  // Populate catalog with sample games.
  library.addGame(BoardGame(
    id: 'BG001',
    title: 'Catan',
    publisher: 'Kosmos',
    releaseYear: 1995,
    genre: 'Strategy',
    playerCountMin: 3,
    playerCountMax: 4,
    playTimeMinutes: 90,
    complexityRating: 2.3,
  ));

  library.addGame(BoardGame(
    id: 'BG002',
    title: 'Wingspan',
    publisher: 'Stonemaier Games',
    releaseYear: 2019,
    genre: 'Strategy',
    playerCountMin: 1,
    playerCountMax: 5,
    playTimeMinutes: 70,
    complexityRating: 2.4,
  ));

  library.addGame(CardGame(
    id: 'CG001',
    title: 'Love Letter',
    publisher: 'Z-Man Games',
    releaseYear: 2012,
    genre: 'Bluffing',
    deckSize: 16,
    avgPlayTimeMinutes: 20,
  ));

  library.addGame(RPGManual(
    id: 'RPG001',
    title: 'D&D Player\'s Handbook',
    publisher: 'Wizards of the Coast',
    releaseYear: 2014,
    genre: 'RPG',
    edition: '5th Edition',
    pageCount: 320,
  ));

  // Register members.
  library.registerMember(Member(memberId: 'M001', name: 'Soumitra Deshpande'));
  library.registerMember(Member(memberId: 'M002', name: 'Alex Chen'));

  // Demonstrate catalog listing.
  library.listCatalog();

  // Demonstrate borrowing.
  library.borrowGame(memberId: 'M001', gameId: 'BG002');
  library.borrowGame(memberId: 'M002', gameId: 'CG001');

  // Recommend available board games for 3 players.
  library.recommendForPlayers(3);

  // Demonstrate returning.
  library.returnGame(memberId: 'M001', gameId: 'BG002');

  // Show all member borrow records.
  print('\n=== MEMBER BORROWS ===');
  for (final member in library.members.values) {
    member.showBorrowedGames();
  }

  // Demonstrate late fee calculation.
  print('\n=== LATE FEE EXAMPLES ===');
  final cardFee = calculateLateFee(overdueDays: 5, gameType: 'cardgame');
  final rpgFee = calculateLateFee(
    overdueDays: 3,
    gameType: 'rpgmanual',
    dailyRate: 2.0,
  );
  print('Card game 5 days late: \$${cardFee.toStringAsFixed(2)}');
  print('RPG manual 3 days late: \$${rpgFee.toStringAsFixed(2)}');
}
