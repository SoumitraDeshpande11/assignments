/// Abstract base class for every item in the lending library.
abstract class Game {
  final String id;
  final String title;
  final String publisher;
  final int releaseYear;
  final String genre;
  bool isAvailable;

  Game({
    required this.id,
    required this.title,
    required this.publisher,
    required this.releaseYear,
    required this.genre,
    this.isAvailable = true,
  });

  /// Polymorphic detail printer implemented by all subclasses.
  void describe();

  String get availabilityStatus => isAvailable ? 'Available' : 'Borrowed';
}
