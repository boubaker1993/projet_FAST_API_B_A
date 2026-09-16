
import pandas as pd
import io
import os
import glob

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Preformatted,
    PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet


def analyser_csv(fichier_csv, fichier_pdf):

    # ==============================
    # CHARGEMENT
    # ==============================
    df = pd.read_csv(fichier_csv)

    styles = getSampleStyleSheet()
    elements = []

    pdf = SimpleDocTemplate(
        fichier_pdf,
        pagesize=A4
    )

    # ==============================
    # TITRE
    # ==============================
    elements.append(
        Paragraph(
            f"Rapport d'analyse : {os.path.basename(fichier_csv)}",
            styles["Title"]
        )
    )

    elements.append(Spacer(1, 20))

    # ==============================
    # 1. DIMENSIONS
    # ==============================
    elements.append(
        Paragraph("1. Dimensions du fichier", styles["Heading2"])
    )

    elements.append(
        Paragraph(
            f"Nombre de lignes : {df.shape[0]}<br/>"
            f"Nombre de colonnes : {df.shape[1]}",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 15))

    # ==============================
    # 2. IDENTIFIANTS UNIQUES
    # ==============================
    elements.append(
        Paragraph("2. Identification des colonnes uniques", styles["Heading2"])
    )

    colonnes_uniques = []

    for colonne in df.columns:

        # Une colonne est considérée comme identifiant potentiel
        # si toutes ses valeurs non nulles sont uniques
        valeurs = df[colonne].dropna()

        if len(valeurs) > 0 and valeurs.nunique() == len(valeurs):
            colonnes_uniques.append(colonne)

    if colonnes_uniques:
        texte = "\n".join(
            f"- {colonne}" for colonne in colonnes_uniques
        )
    else:
        texte = "Aucune colonne avec des valeurs uniques."

    elements.append(
        Preformatted(texte, styles["Code"])
    )

    elements.append(Spacer(1, 15))

    # ==============================
    # 3. VALEURS NULL
    # ==============================
    elements.append(
        Paragraph("3. Valeurs nulles", styles["Heading2"])
    )

    nulles = df.isnull().sum()

    nulles = nulles[nulles > 0]

    if len(nulles) > 0:

        texte = "\n".join(
            f"{colonne} : {nombre} valeurs nulles"
            for colonne, nombre in nulles.items()
        )

    else:
        texte = "Aucune valeur nulle."

    elements.append(
        Preformatted(texte, styles["Code"])
    )

    elements.append(Spacer(1, 15))

    # ==============================
    # 4. DOUBLONS
    # ==============================
    elements.append(
        Paragraph("4. Doublons", styles["Heading2"])
    )

    nombre_doublons = df.duplicated().sum()

    elements.append(
        Paragraph(
            f"Nombre total de lignes dupliquées : "
            f"{nombre_doublons}",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 15))

    # ==============================
    # 5. VALEURS ABERRANTES
    # ==============================
    elements.append(
        Paragraph(
            "5. Valeurs aberrantes",
            styles["Heading2"]
        )
    )

    texte_aberrantes = []

    # Seulement les colonnes numériques
    colonnes_numeriques = df.select_dtypes(
        include="number"
    ).columns

    for colonne in colonnes_numeriques:

        # Quartiles
        Q1 = df[colonne].quantile(0.25)
        Q3 = df[colonne].quantile(0.75)

        # Écart interquartile
        IQR = Q3 - Q1

        # Limites
        limite_basse = Q1 - 1.5 * IQR
        limite_haute = Q3 + 1.5 * IQR

        # Détection
        aberrantes = df[
            (df[colonne] < limite_basse) |
            (df[colonne] > limite_haute)
        ]

        nombre = len(aberrantes)

        if nombre > 0:
            texte_aberrantes.append(
                f"{colonne} : {nombre} valeurs aberrantes "
                f"(limites : {limite_basse:.2f} / "
                f"{limite_haute:.2f})"
            )

    if texte_aberrantes:

        texte = "\n".join(texte_aberrantes)

    else:

        texte = "Aucune valeur aberrante détectée."

    elements.append(
        Preformatted(texte, styles["Code"])
    )

    elements.append(Spacer(1, 15))

    # ==============================
    # 6. TYPES DES VARIABLES
    # ==============================
    elements.append(
        Paragraph(
            "6. Types des variables",
            styles["Heading2"]
        )
    )

    elements.append(
        Preformatted(
            df.dtypes.to_string(),
            styles["Code"]
        )
    )

    elements.append(Spacer(1, 15))

    # ==============================
    # 7. STATISTIQUES
    # ==============================
    elements.append(
        Paragraph(
            "7. Statistiques descriptives",
            styles["Heading2"]
        )
    )

    elements.append(
        Preformatted(
            df.describe(include="all").to_string(),
            styles["Code"]
        )
    )

    # ==============================
    # CRÉATION DU PDF
    # ==============================
    pdf.build(elements)

    print(f"PDF créé : {fichier_pdf}")


# ============================================
# ANALYSER TOUS LES CSV DU DOSSIER
# ============================================


fichiers = glob.glob("data/*.csv")

for fichier in fichiers:

    nom = os.path.splitext(
        os.path.basename(fichier)
    )[0]

    fichier_pdf = f"data/{nom}_rapport.pdf"

    analyser_csv(fichier, fichier_pdf)