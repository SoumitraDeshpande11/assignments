# API Data Fetcher with Local Cache

A Flutter app that fetches posts from the JSONPlaceholder REST API, renders them with `FutureBuilder`, and caches the last successful result with `SharedPreferences` so content survives offline. Matches the other assignments: white background, one green accent, flat rounded cards.

## Concepts Demonstrated

- `http` GET against `https://jsonplaceholder.typicode.com/posts`
- `Post` data model with `fromJson` / `toJson`
- `FutureBuilder` handling waiting / error / data states
- `SharedPreferences` cache: posts + timestamp saved as JSON after every successful fetch
- Offline fallback: network failure returns the cached result (with an amber "cached data" banner); errors only surface when no cache exists
- Refresh via AppBar icon / Retry button, re-running the future with `setState`

## Run

```bash
flutter pub get
flutter run
```

## Author

**Soumitra Deshpande** — Roll No: `150096724035` — Cohort: Elon Musk
