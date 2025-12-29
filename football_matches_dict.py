# Football Matches Dictionary
# Data collected from https://fon.bet/sports/football?mode=1&dateInterval=6
# Only matches with favorite (odds < 1.56) are included

football_matches = {
    "Neom — Al-Najma": {
        "favorite": "Neom 1.40",
        "underdog": "Al-Najma 14.71%"
    },
    "Bnei Sakhnin — Maccabi Kabilio Jaffa": {
        "favorite": "Bnei Sakhnin 1.35",
        "underdog": "Maccabi Kabilio Jaffa 13.33%"
    },
    "Hapoel Petah Tikva — Hapoel Ironi Karmiel": {
        "favorite": "Hapoel Petah Tikva 1.25",
        "underdog": "Hapoel Ironi Karmiel 10.53%"
    },
    "Al Bourj Beirut — Al Ahed": {
        "favorite": "Al Ahed 1.50",
        "underdog": "Al Bourj Beirut 16.39%"
    },
    "Trabzonspor U19 — Eyupspor U19": {
        "favorite": "Trabzonspor U19 1.32",
        "underdog": "Eyupspor U19 11.76%"
    },
    "Pyramids — Ismaily": {
        "favorite": "Ismaily 1.30",
        "underdog": "Pyramids 12.50%"
    },
    "KYIZ — New King": {
        "favorite": "KYIZ 1.50",
        "underdog": "New King 15.38%"
    },
    "Al Ramtha (r) — Al Ahli Amman (r)": {
        "favorite": "Al Ahli Amman (r) 1.43",
        "underdog": "Al Ramtha (r) 16.67%"
    },
    "Al-Wehda Mecca — Al-Jubail": {
        "favorite": "Al-Wehda Mecca 1.47",
        "underdog": "Al-Jubail 16.95%"
    }
}

# Print the dictionary
for match, data in football_matches.items():
    print(f"{match}:")
    print(f"  Favorite: {data['favorite']}")
    print(f"  Underdog: {data['underdog']}")
    print()
