# Responsive Store Dashboard

A Flutter dashboard that adapts to screen size using `ListView`, `GridView`, `MediaQuery`, and `Flexible`/`Expanded`. Design is intentionally minimal: white background, one accent color, plain cards.

## Concepts Demonstrated

- `MediaQuery` breakpoints: 2 / 3 / 4 grid columns for phone / tablet / desktop widths
- `GridView.builder` of stat cards with a fixed cross-axis count
- `ListView.separated` for the recent activity feed
- `Expanded` in the header row and `Flexible`/`Expanded` to split space between grid and list
- Wide screens place the grid and list side by side; narrow screens stack them

## Run

```bash
flutter pub get
flutter run
```

## Author

**Soumitra Deshpande** — Roll No: `150096724035` — Cohort: Elon Musk
