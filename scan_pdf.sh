#!/bin/bash
#
# ┌───────────────────────────────────────────────┐
# │            scan_pdf.sh - v1.0                │
# └───────────────────────────────────────────────┘
# Script d'analyse simple pour un fichier PDF.
# ⚙️  Étapes :
#   - Scan antivirus avec ClamAV
#   - Extraction des infos du fichier avec pdfinfo
#   - Aperçu du texte avec pdftotext
#   - Analyse de la structure du PDF avec pdfid.py
#
# 📌 Usage :
#   ./scan_pdf.sh fichier.pdf
#
# 💡 Pré-requis :
#   - clamscan (ClamAV)
#   - pdfinfo (poppler-utils)
#   - pdftotext (poppler-utils)
#   - pdfid.py dans le même dossier (et exécutable)
#
# Date : avril 2025


# === Couleurs ANSI ===
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# === Entrée ===
PDF="$1"

if [ -z "$PDF" ]; then
    echo -e "${RED}❌ Usage: $0 fichier.pdf${NC}"
    exit 1
fi

if [ ! -f "$PDF" ]; then
    echo -e "${RED}❌ Fichier introuvable : $PDF${NC}"
    exit 2
fi

echo -e "${CYAN}🔍 Analyse de : $PDF${NC}"
echo -e "${CYAN}-----------------------------------${NC}"

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
pdftotext "$PDF" - | head -n 20
echo

# Analyse pdfid.py
if [ -x "./pdfid.py" ]; then
    echo -e "${YELLOW}🧠 Analyse structurelle avec pdfid.py${NC}"
    ./pdfid.py "$PDF"
else
    echo -e "${RED}⚠️  pdfid.py non trouvé ou non exécutable, skipping...${NC}"
fi

echo -e "${GREEN}✅ Analyse terminée.${NC}"
