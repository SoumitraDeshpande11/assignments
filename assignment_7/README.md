# 3-Screen App with Named Routes & Form Validation

A Flutter app with three screens — Home, Register, Detail — wired together with named routes, plus a registration form with validation (required fields, email format, password length). Design matches the previous assignments: white background, one green accent, flat rounded surfaces.

## Concepts Demonstrated

- Named routes via `MaterialApp(routes: {...})` and `initialRoute`
- Navigation with `Navigator.pushNamed`, plus `Navigator.popUntil` to return home
- Passing data between screens with route `arguments` and `ModalRoute.of(context)!.settings.arguments`
- `User` data model class (immutable `name` + `email`)
- `Form` + `GlobalKey<FormState>` + `TextFormField` validators
- Email regex validation, 8-character minimum password, required-field checks
- Password visibility toggle via `setState`

## Run

```bash
flutter pub get
flutter run
```

## Author

**Soumitra Deshpande** — Roll No: `150096724035` — Cohort: Elon Musk
