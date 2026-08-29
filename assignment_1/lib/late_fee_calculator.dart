/// Pure utility that calculates late fees based on overdue days and game type.
double calculateLateFee({
  required int overdueDays,
  required String gameType,
  double dailyRate = 1.5,
}) {
  if (overdueDays <= 0) return 0.0;

  double multiplier = 1.0;
  switch (gameType.toLowerCase()) {
    case 'rpgmanual':
      multiplier = 1.5;
    case 'boardgame':
      multiplier = 1.2;
    case 'cardgame':
      multiplier = 1.0;
  }

  return overdueDays * dailyRate * multiplier;
}
