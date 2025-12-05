from config import app
from entities.reference import Reference
from repositories.reference_repository import create_reference


def populate_test_data():
    test_references = [
        # BOOKS
        {
            "reference_type": "book",
            "cite_key": "Silakkabotti2012",
            "title": "Silakkabottien salaliitto: Totuus vedenalaisesta ohjelmistokehityksestä",
            "author": "Silakkainen, Silakka",
            "year": 2012,
            "publisher": "Merisalaatti Kustannus",
            "chapter": "5: Kun silakka optimoi itse itsensä",
        },
        {
            "reference_type": "book",
            "cite_key": "KissaQuantum2021",
            "title": "Kvanttikissa ja superpositiokoodin ongelmat",
            "author": "Nöpötassu, Nöpö",
            "year": 2021,
            "publisher": "Schrödinger Books",
            "chapter": "7: Kissa on sekä bugi että feature",
        },
        {
            "reference_type": "book",
            "cite_key": "SöpöOps2018",
            "title": "SöpöOps: Pehmeä tuotantoputki pehmeälle tiimille",
            "author": "Pehmola, Pulla; Pehmola, Purri",
            "year": 2018,
            "publisher": "Höpönassu Press",
            "chapter": "2: CI/CD = Cuddle Integration / Cuddle Delivery",
        },
        # ARTICLES
        {
            "reference_type": "article",
            "cite_key": "LohiAI2020",
            "title": "Lohen vaellus ja tekoälyn hyperparametrien viritys",
            "author": "Lohi, Lauri",
            "year": 2020,
            "journal": "Kalateknologian Katsaus",
            "volume": "9",
            "pages": "1-12",
        },
        {
            "reference_type": "article",
            "cite_key": "Kissafyysiikka2016",
            "title": "Miksi kissa valitsee aina syliin väärällä hetkellä? Empiirinen katsaus",
            "author": "Murr, Miau; Purr, Pörrö",
            "year": 2016,
            "journal": "Kissadynamiikan Arkisto",
            "volume": "3",
            "pages": "55-70",
        },
        {
            "reference_type": "article",
            "cite_key": "Kalatietokoneet2025",
            "title": "Kalatietokoneet: Vedenalainen laskenta ja sen haasteet",
            "author": "Ahven, Aku; Hauki, Heikki",
            "year": 2025,
            "journal": "Vedenalaisen Laskennan Lehti",
            "volume": "7",
            "pages": "101-115",
        },
        # INPROCEEDINGS
        {
            "reference_type": "inproceedings",
            "cite_key": "TurskaSoft2018",
            "title": "Turskakoodin refaktorointi: vähemmän suolaa, enemmän logiikkaa",
            "author": "Turska, Teemu",
            "year": 2018,
            "booktitle": "Pohjoisten Kalojen Teknologiakongressi",
        },
        {
            "reference_type": "inproceedings",
            "cite_key": "KissaScrum2020",
            "title": "Scrum kissojen kanssa: ketterät metodit karvaisille tiimeille",
            "author": "Kuono, Kisu; Miau, Mirri",
            "year": 2020,
            "booktitle": "Ammatillisen Kissaohjelmiston Päivät 2020",
        },
        {
            "reference_type": "inproceedings",
            "cite_key": "MaaliMM2022",
            "title": "Maalin kuivumisen MM-kilpailut 2022: Tylsyyttä ja turhanpäiväistä odettelua",
            "author": "Hiiri, Mikki; Ankka, Aku",
            "year": 2022,
            "booktitle": "Kansainvälinen Maalin Kuivumisen Symposium",
        },
        # MISC
        {
            "reference_type": "misc",
            "cite_key": "KisuCLI2024",
            "title": "KissaCLI: Komentorivityökalut, jotka kehräävät",
            "author": "Terminal, Tassu",
            "year": 2024,
            "url": "https://example.com/kissacli",
        },
        {
            "reference_type": "misc",
            "cite_key": "OHPEMOOC2025",
            "title": "Ohjelmoinnin perusteet ja jatkokurssi",
            "author": "Kaila, Erkki; Laaksonen, Antti; Luukkainen, Matti; Hellas, Arto",
            "year": 2025,
            "url": "https://ohjelmointi-25.mooc.fi/",
        },
        {
            "reference_type": "misc",
            "cite_key": "OHTU2025",
            "title": "Ohjelmistotuotanto",
            "author": "Luukkainen, Matti; Ilves, Kalle",
            "year": 2025,
            "url": "https://ohjelmistotuotanto-hy.github.io/",
        },
    ]

    with app.app_context():
        print("Luodaan testidataa... :3")

        for ref_data in test_references:
            try:
                reference = Reference(ref_data)
                create_reference(reference)
                print(f"✓ Luotu: {ref_data['cite_key']} - {ref_data['title']}")
            except Exception as e:
                print(f"✗ Luominen epäonnistui: {ref_data['cite_key']}: {str(e)}")

        print(
            f"\nTietokantaan tykitetty onnistuneesti {len(test_references)} testiviitettä! UwU\n"
        )


if __name__ == "__main__":
    populate_test_data()
