import pandas as pd

def lire_inventaire(chemin_csv: str) -> list[dict]:
    df = pd.read_csv(chemin_csv)

    # Nettoyage des noms de colonnes
    df.columns = [col.strip() for col in df.columns]
    df = df.rename(columns={"Numéro": "id"})

    # Typage explicite
    df["id"] = df["id"].astype(int)
    df["Désignation"] = df["Désignation"].astype(str).str.strip()
    df["Longueur"] = df["Longueur"].astype(float)
    df["Largeur"] = df["Largeur"].astype(float)
    df["Hauteur"] = df["Hauteur"].astype(float)

    # Colonnes dérivées
    df["Surface_m2"] = (df["Longueur"] * df["Largeur"]).round(4)
    df["Volume_m3"] = (df["Longueur"] * df["Largeur"] * df["Hauteur"]).round(4)

    return df.to_dict(orient="records")


if __name__ == "__main__":
    inventaire = lire_inventaire("DonnesMarchandise.csv")
    for article in inventaire:
        print(article)