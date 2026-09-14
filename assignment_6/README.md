# Product Listing with Search & Filter

A Flutter product catalog built with `ListView.builder` and a `Product` data model class, with live search and category filtering driven by `setState`. Design matches the previous assignments: white background, one green accent, flat rounded cards.

## Concepts Demonstrated

- `Product` data model class with immutable fields (`name`, `category`, `price`, `rating`, `emoji`)
- `ListView.builder` rendering one card per product in the filtered list
- Search via a `TextField` whose `onChanged` updates the query in `setState`
- Category filter via `ChoiceChip`s (All, Electronics, Clothing, Grocery, Books)
- A `_filteredProducts` getter that combines both filters on every rebuild
- Live "X of 12 products" counter and an empty-state message when nothing matches

## Run

```bash
flutter pub get
flutter run
```

## Author

**Soumitra Deshpande** — Roll No: `150096724035` — Cohort: Elon Musk
