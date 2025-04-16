#!/bin/bash
#
# ┌───────────────────────────────────────────────────────┐
# │              scan_all_pdfs.sh - v1.0                 │
# └───────────────────────────────────────────────────────┘
# Script d'analyse automatique de tous les fichiers PDF dans un dossier.
# ⚙️  Étapes pour chaque fichier :
#   - Scan antivirus avec ClamAV
#   - Extraction des infos (pdfinfo)
#   - Aperçu texte (pdftotext)
#   - Analyse structurelle (pdfid.py)
#
# 📌 Usage :
#   ./scan_all_pdfs.sh [dossier]
#   Par défaut : dossier courant
#
# 💡 Pré-requis :
#   - clamscan
#   - pdfinfo
#   - pdftotext
#   - pdfid.py dans le même dossier (chmod +x)
#
# Date : avril 2025


# === Couleurs ANSI ===
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# === Dossier à scanner ===
DIR="${1:-.}"  # Par défaut : dossier courant

if [ ! -d "$DIR" ]; then
    echo -e "${RED}❌ Dossier introuvable : $DIR${NC}"
    exit 1
fi

PDFID="./pdfid.py"
if [ ! -x "$PDFID" ]; then
    echo -e "${RED}⚠️  pdfid.py non trouvé ou non exécutable dans le dossier courant.${NC}"
    echo -e "${YELLOW}➡️  Place-le ici ou fais : chmod +x pdfid.py${NC}"
fi

echo -e "${CYAN}📂 Scan de tous les fichiers PDF dans : $DIR${NC}"
echo

shopt -s nullglob
FILES=("$DIR"/*.pdf)

if [ ${#FILES[@]} -eq 0 ]; then
    echo -e "${RED}❌ Aucun fichier PDF trouvé dans ce dossier.${NC}"
    exit 2
fi

for PDF in "${FILES[@]}"; do
    echo -e "${CYAN}===========================================${NC}"
    echo -e "${CYAN}🔍 Analyse de : $PDF${NC}"
    echo -e "${CYAN}-------------------------------------------${NC}"

    # Antivirus
    echo -e "${YELLOW}🛡️  Scan antivirus avec ClamAV${NC}"
    clamscan "$PDF"
    echo

    # Infos PDF
    echo -e "${YELLOW}📄 Informations PDF (pdfinfo)${NC}"
    pdfinfo "$PDF"
    echo

    # Contenu texte
    echo -e "${YELLOW}📝 Extraction du contenu texte (pdftotext)${NC}"
    pdftotext "$PDF" - | head -n 10
    echo

    # Analyse pdfid.py
    if [ -x "$PDFID" ]; then
        echo -e "${YELLOW}🧠 Analyse structurelle avec pdfid.py${NC}"
        "$PDFID" "$PDF"
    else
        echo -e "${RED}⚠️  pdfid.py indisponible, skipping...${NC}"
    fi

    echo -e "${GREEN}✅ Analyse terminée pour : $PDF${NC}"
    echo
done

echo -e "${GREEN}🏁 Scan complet terminé !${NC}"
