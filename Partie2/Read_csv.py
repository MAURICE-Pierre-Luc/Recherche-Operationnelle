import pandas as pd

def lire_inventaire(chemin_csv: str) -> list[dict]:
    df = pd.read_csv(chemin_csv)

    # Nettoyage des noms de colonnes
    df.columns = [col.strip() for col in df.columns]
    df = df.rename(columns={"Numéro": "id"})

    # Passage en int via cm (évite les floats)
    df["id"] = df["id"].astype(int)
    df["Désignation"] = df["Désignation"].astype(str).str.strip()

    # Conversion mètres -> milimètres (int)
    df["Longueur"] = (df["Longueur"].astype(float) * 1000).round().astype(int)
    df["Largeur"] = (df["Largeur"].astype(float) * 1000).round().astype(int)
    df["Hauteur"] = (df["Hauteur"].astype(float) * 1000).round().astype(int)

    # Calculs en mm² et mm³ (entiers)
    df["Surface_mm2"] = df["Longueur"] * df["Largeur"]
    df["Volume_mm3"] = df["Longueur"] * df["Largeur"] * df["Hauteur"]

    return df.to_dict(orient="records")


if __name__ == "__main__":
    inventaire = lire_inventaire("./Partie2/DonnesMarchandise.csv")
    for article in inventaire:
        print(article)