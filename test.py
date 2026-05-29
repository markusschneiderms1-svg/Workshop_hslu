def starte_workshop(teilnehmer_liste):
    """Begrüsst alle Teilnehmer des HSLU-Workshops."""
    print("Willkommen zum Python-Workshop an der HSLU! 🚀")
    
    # Eine kompakte List Comprehension zur Formatierung
    formatierte_namen = [name.capitalize() for name in teilnehmer_liste]
    
    for name in formatierte_namen:
        print(f"Hallo {name}, viel Spass beim Programmieren!")

# Beispielaufruf
hslu_teilnehmer = ["anna", "beat", "claudia", "david"]
starte_workshop(hslu_teilnehmer)