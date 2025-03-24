# Color-Coding Erklärungen

Dieses Skript verwendet ein konsistentes Farb- und Stil-Konzept, um verschiedene Arten von Nachrichten visuell hervorzuheben:

- **Gelb (`colors.header`)**: Für Header und wichtige Informationen.
- **Cyan (`colors.prompt`)**: Für alle Eingabeaufforderungen.
- **Grün (`colors.success`)**: Für Erfolgsmeldungen oder abgeschlossene Aktionen.
- **Rot (`colors.error`)**: Für Fehlermeldungen oder ungültige Eingaben.
- **Blau (`colors.info`)**: Für allgemeine Informationsanzeigen und Statusmeldungen.
- **Magenta (`colors.highlight`)**: Für das Hervorheben von wichtigen oder besonderen Optionen.

Diese Farbcodierung sorgt für ein konsistentes und leicht verständliches visuelles Feedback im gesamten Programm.

```python
from color_config import colors

print(colors.header + "Dies ist ein Header" + colors.reset)
print(colors.success + "Erfolgreich ausgeführt!" + colors.reset)
```