from django.shortcuts import render
import random, string

MEDICAMENTS_DB = {
    "TY-2024-0042-A1": {
        "nom": "Artémisinine 80mg",
        "fabricant": "PharmaBF Ouagadougou",
        "lot": "LOT-2024-042",
        "fabrication": "12/01/2024",
        "expiration": "12/01/2026",
        "statut": "authentique",
        "classe": "Antipaludéen",
        "nb_verifications": 147,
        "dernier_scan": "Pharmacie Centrale, Ouagadougou",
    },
    "TY-2024-0099-B2": {
        "nom": "Amoxicilline 500mg",
        "fabricant": "MediImport SA",
        "lot": "LOT-2024-099",
        "fabrication": "03/05/2024",
        "expiration": "03/05/2026",
        "statut": "suspect",
        "classe": "Antibiotique",
        "nb_verifications": 3,
        "dernier_scan": "Marché Sankariare, Ouagadougou",
    },
    "TY-2025-0017-C3": {
        "nom": "Paracétamol 1000mg",
        "fabricant": "GénériquesBF",
        "lot": "LOT-2025-017",
        "fabrication": "22/08/2025",
        "expiration": "22/08/2027",
        "statut": "authentique",
        "classe": "Antidouleur",
        "nb_verifications": 892,
        "dernier_scan": "Pharmacie Gounghin, Ouagadougou",
    },
    "TY-2024-FAKE-XX": {
        "nom": "Artémisinine 80mg",
        "fabricant": "INCONNU",
        "lot": "INCONNU",
        "fabrication": "??",
        "expiration": "??",
        "statut": "contrefait",
        "classe": "Antipaludéen",
        "nb_verifications": 12,
        "dernier_scan": "Adresse inconnue",
    },
}

STOCKS_PHARMACIEN = [
    {"id": 1, "nom": "Artémisinine 80mg", "lot": "LOT-2024-042", "qte": 240, "seuil": 50, "expiration": "12/01/2026", "statut": "ok"},
    {"id": 2, "nom": "Amoxicilline 500mg", "lot": "LOT-2024-099", "qte": 12, "seuil": 30, "expiration": "03/05/2026", "statut": "alerte"},
    {"id": 3, "nom": "Paracétamol 1000mg", "lot": "LOT-2025-017", "qte": 530, "seuil": 100, "expiration": "22/08/2027", "statut": "ok"},
    {"id": 4, "nom": "Métronidazole 250mg", "lot": "LOT-2025-008", "qte": 8, "seuil": 20, "expiration": "01/03/2026", "statut": "critique"},
    {"id": 5, "nom": "Cotrimoxazole 480mg", "lot": "LOT-2024-077", "qte": 155, "seuil": 40, "expiration": "15/09/2026", "statut": "ok"},
]

STATS_GOUVERNEMENT = {
    "total_verifications": 1284592,
    "contrefaits_detectes": 8412,
    "pharmacies_connectees": 312,
    "vies_sauvees_estimees": 1840,
    "taux_couverture": 67,
    "alertes_actives": 14,
    "regions": [
        {"nom": "Centre (Ouaga)", "risque": "moyen", "verifications": 542000, "contrefaits": 2100},
        {"nom": "Hauts-Bassins (Bobo)", "risque": "eleve", "verifications": 210000, "contrefaits": 3200},
        {"nom": "Sahel", "risque": "critique", "verifications": 45000, "contrefaits": 1800},
        {"nom": "Est", "risque": "eleve", "verifications": 89000, "contrefaits": 890},
        {"nom": "Boucle du Mouhoun", "risque": "faible", "verifications": 120000, "contrefaits": 180},
        {"nom": "Cascades", "risque": "moyen", "verifications": 98000, "contrefaits": 142},
        {"nom": "Nord", "risque": "moyen", "verifications": 65000, "contrefaits": 68},
        {"nom": "Centre-Nord", "risque": "faible", "verifications": 55000, "contrefaits": 32},
    ],
    "alertes_recentes": [
        {"date": "10/06/2026", "zone": "Marché Sankariare, Ouaga", "produit": "Artémisinine 80mg", "gravite": "haute"},
        {"date": "08/06/2026", "zone": "Bobo-Dioulasso centre", "produit": "Amoxicilline 500mg", "gravite": "haute"},
        {"date": "05/06/2026", "zone": "Dori, Sahel", "produit": "Paracétamol générique", "gravite": "moyenne"},
        {"date": "02/06/2026", "zone": "Fada N'Gourma", "produit": "Métronidazole 250mg", "gravite": "moyenne"},
    ],
    "evolution_mensuelle": [
        {"mois": "Jan", "verifications": 85000, "contrefaits": 820},
        {"mois": "Fév", "verifications": 92000, "contrefaits": 750},
        {"mois": "Mar", "verifications": 105000, "contrefaits": 680},
        {"mois": "Avr", "verifications": 118000, "contrefaits": 610},
        {"mois": "Mai", "verifications": 134000, "contrefaits": 540},
        {"mois": "Jun", "verifications": 141000, "contrefaits": 490},
    ],
}

LOTS_FABRICANT = [
    {"id": "LOT-2026-001", "produit": "Artémisinine 80mg", "qte": 5000, "date": "01/06/2026", "statut": "enregistré", "codes_generes": 5000},
    {"id": "LOT-2026-002", "produit": "Amoxicilline 500mg", "qte": 3000, "date": "05/06/2026", "statut": "enregistré", "codes_generes": 3000},
    {"id": "LOT-2026-003", "produit": "Paracétamol 1000mg", "qte": 10000, "date": "10/06/2026", "statut": "en_cours", "codes_generes": 6200},
]


def accueil(request):
    return render(request, "tiim/accueil.html", {
        "stats": {
            "verifications": "1,28M+",
            "pharmacies": "312",
            "contrefaits": "8 412",
            "regions": "13",
        }
    })


def patient(request):
    resultat = None
    code_saisi = ""
    if request.method == "POST":
        code = request.POST.get("code_qr", "").strip().upper()
        code_saisi = code
        if code in MEDICAMENTS_DB:
            resultat = {"code": code, **MEDICAMENTS_DB[code]}
        elif code:
            resultat = {"code": code, "statut": "introuvable"}
    return render(request, "tiim/patient.html", {"resultat": resultat, "code_saisi": code_saisi})


def pharmacien(request):
    alerte = None
    scan_resultat = None
    code_scan = ""
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "scan":
            code = request.POST.get("code_scan", "").strip().upper()
            code_scan = code
            if code in MEDICAMENTS_DB:
                scan_resultat = {"code": code, **MEDICAMENTS_DB[code]}
            elif code:
                scan_resultat = {"code": code, "statut": "introuvable"}
        elif action == "commander":
            alerte = {"type": "succes", "message": "Commande envoyée avec succès au distributeur !"}
    return render(request, "tiim/pharmacien.html", {
        "stocks": STOCKS_PHARMACIEN,
        "alerte": alerte,
        "scan_resultat": scan_resultat,
        "code_scan": code_scan,
        "alertes_stock": [s for s in STOCKS_PHARMACIEN if s["statut"] in ("alerte", "critique")],
    })


def gouvernement(request):
    return render(request, "tiim/gouvernement.html", {"stats": STATS_GOUVERNEMENT})


def fabricant(request):
    nouveau_lot = None
    if request.method == "POST":
        produit = request.POST.get("produit", "")
        quantite = request.POST.get("quantite", "0")
        if produit and quantite:
            ref = "LOT-2026-" + "".join(random.choices(string.digits, k=3))
            nouveau_lot = {
                "ref": ref,
                "produit": produit,
                "quantite": quantite,
                "codes": [f"TY-2026-{random.randint(1000,9999)}-{''.join(random.choices(string.ascii_uppercase, k=2))}" for _ in range(5)],
            }
    return render(request, "tiim/fabricant.html", {
        "lots": LOTS_FABRICANT,
        "nouveau_lot": nouveau_lot,
    })