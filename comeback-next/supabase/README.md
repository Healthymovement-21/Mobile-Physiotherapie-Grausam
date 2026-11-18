# Backend-Einrichtung

1. Supabase-Projekt in einer EU-Region anlegen.
2. `supabase/migrations/001_patient_records.sql` und danach `supabase/migrations/002_training_workflow.sql` im SQL-Editor ausführen.
3. `.env.example` nach `.env.local` kopieren und `VITE_SUPABASE_URL` sowie den öffentlichen `VITE_SUPABASE_ANON_KEY` eintragen.
4. Authentifizierung für Patient:in und Therapeut:in einrichten, bevor echte Gesundheitsdaten verwendet werden.

Der Client bleibt ohne diese Variablen vollständig lokal. Der Service-Role-Key darf niemals in Vite, GitHub Pages oder den Browser gelangen.

Die Migration enthält Row-Level-Security, aber die Anwendung muss vor dem Live-Betrieb noch mit den jeweiligen Auth-User-IDs der Patient:innen und Therapeut:innen verbunden werden. Das ist absichtlich kein anonymer Token-Zugriff.

Die Trainingsmigration trennt Planversionen, konkrete Termine, Übungsprotokolle und Rückmeldungen. `completion_key` verhindert doppelte Abschlüsse; abgeschlossene Termine werden bei späteren Planversionen nicht überschrieben.
