"""
drug_dictionary.py - Curated Drug/Chemical Dictionary for CORD-19
Contains drugs mentioned in COVID-19 research with their efficacy labels
"""

# =============================================================================
# DRUG DICTIONARY: {drug_name: [list of efficacies]}
# =============================================================================
# Each drug can have multiple efficacy labels
# Names are lowercase for matching

DRUG_EFFICACY_MAP = {
    # ANTIVIRALS
    "remdesivir": ["antiviral", "rna polymerase inhibitor"],
    "favipiravir": ["antiviral", "rna polymerase inhibitor"],
    "molnupiravir": ["antiviral", "mutagenic agent"],
    "ribavirin": ["antiviral", "nucleoside analog"],
    "oseltamivir": ["antiviral", "neuraminidase inhibitor"],
    "arbidol": ["antiviral", "membrane fusion inhibitor"],
    "umifenovir": ["antiviral", "membrane fusion inhibitor"],
    "baloxavir": ["antiviral", "endonuclease inhibitor"],
    "sofosbuvir": ["antiviral", "ns5b polymerase inhibitor"],
    "galidesivir": ["antiviral", "nucleoside analog"],
    
    # HIV PROTEASE INHIBITORS (repurposed)
    "lopinavir": ["antiviral", "hiv protease inhibitor"],
    "ritonavir": ["antiviral", "hiv protease inhibitor", "cyp3a4 inhibitor"],
    "darunavir": ["antiviral", "hiv protease inhibitor"],
    "atazanavir": ["antiviral", "hiv protease inhibitor"],
    "nelfinavir": ["antiviral", "hiv protease inhibitor"],
    
    # ANTIMALARIALS
    "hydroxychloroquine": ["antimalarial", "immunomodulator", "autophagy inhibitor"],
    "chloroquine": ["antimalarial", "immunomodulator", "autophagy inhibitor"],
    "mefloquine": ["antimalarial"],
    "artemisinin": ["antimalarial", "anti-inflammatory"],
    
    # CORTICOSTEROIDS
    "dexamethasone": ["corticosteroid", "anti-inflammatory", "immunosuppressant"],
    "methylprednisolone": ["corticosteroid", "anti-inflammatory"],
    "prednisone": ["corticosteroid", "anti-inflammatory"],
    "prednisolone": ["corticosteroid", "anti-inflammatory"],
    "hydrocortisone": ["corticosteroid", "anti-inflammatory"],
    "budesonide": ["corticosteroid", "anti-inflammatory"],
    
    # IMMUNOMODULATORS / BIOLOGICS
    "tocilizumab": ["immunomodulator", "il-6 inhibitor", "monoclonal antibody"],
    "sarilumab": ["immunomodulator", "il-6 inhibitor", "monoclonal antibody"],
    "siltuximab": ["immunomodulator", "il-6 inhibitor", "monoclonal antibody"],
    "baricitinib": ["immunomodulator", "jak inhibitor"],
    "ruxolitinib": ["immunomodulator", "jak inhibitor"],
    "tofacitinib": ["immunomodulator", "jak inhibitor"],
    "anakinra": ["immunomodulator", "il-1 inhibitor"],
    "canakinumab": ["immunomodulator", "il-1 inhibitor", "monoclonal antibody"],
    "infliximab": ["immunomodulator", "tnf inhibitor", "monoclonal antibody"],
    "adalimumab": ["immunomodulator", "tnf inhibitor", "monoclonal antibody"],
    
    # MONOCLONAL ANTIBODIES (COVID-specific)
    "bamlanivimab": ["monoclonal antibody", "neutralizing antibody"],
    "etesevimab": ["monoclonal antibody", "neutralizing antibody"],
    "casirivimab": ["monoclonal antibody", "neutralizing antibody"],
    "imdevimab": ["monoclonal antibody", "neutralizing antibody"],
    "sotrovimab": ["monoclonal antibody", "neutralizing antibody"],
    "bebtelovimab": ["monoclonal antibody", "neutralizing antibody"],
    "tixagevimab": ["monoclonal antibody", "neutralizing antibody"],
    "cilgavimab": ["monoclonal antibody", "neutralizing antibody"],
    "regdanvimab": ["monoclonal antibody", "neutralizing antibody"],
    
    # ANTICOAGULANTS
    "heparin": ["anticoagulant", "antithrombotic"],
    "enoxaparin": ["anticoagulant", "antithrombotic", "lmwh"],
    "fondaparinux": ["anticoagulant", "factor xa inhibitor"],
    "rivaroxaban": ["anticoagulant", "factor xa inhibitor"],
    "apixaban": ["anticoagulant", "factor xa inhibitor"],
    "warfarin": ["anticoagulant", "vitamin k antagonist"],
    "aspirin": ["antiplatelet", "anti-inflammatory", "nsaid"],
    
    # ANTIBIOTICS
    "azithromycin": ["antibiotic", "macrolide", "anti-inflammatory"],
    "doxycycline": ["antibiotic", "tetracycline", "anti-inflammatory"],
    "ivermectin": ["antiparasitic", "antiviral"],
    "nitazoxanide": ["antiparasitic", "antiviral"],
    "clarithromycin": ["antibiotic", "macrolide"],
    "amoxicillin": ["antibiotic", "penicillin"],
    "ceftriaxone": ["antibiotic", "cephalosporin"],
    "meropenem": ["antibiotic", "carbapenem"],
    "vancomycin": ["antibiotic", "glycopeptide"],
    "linezolid": ["antibiotic", "oxazolidinone"],
    
    # ACE INHIBITORS / ARBs
    "losartan": ["antihypertensive", "arb", "angiotensin receptor blocker"],
    "valsartan": ["antihypertensive", "arb"],
    "telmisartan": ["antihypertensive", "arb"],
    "lisinopril": ["antihypertensive", "ace inhibitor"],
    "enalapril": ["antihypertensive", "ace inhibitor"],
    "ramipril": ["antihypertensive", "ace inhibitor"],
    
    # STATINS
    "atorvastatin": ["statin", "lipid-lowering", "anti-inflammatory"],
    "rosuvastatin": ["statin", "lipid-lowering"],
    "simvastatin": ["statin", "lipid-lowering"],
    "pravastatin": ["statin", "lipid-lowering"],
    
    # SUPPLEMENTS / VITAMINS
    "vitamin d": ["vitamin", "immunomodulator"],
    "vitamin c": ["vitamin", "antioxidant"],
    "zinc": ["mineral", "immunomodulator"],
    "quercetin": ["flavonoid", "antioxidant", "anti-inflammatory"],
    "melatonin": ["hormone", "antioxidant", "anti-inflammatory"],
    "colchicine": ["anti-inflammatory", "gout treatment"],
    
    # RESPIRATORY / BRONCHODILATORS
    "salbutamol": ["bronchodilator", "beta-2 agonist"],
    "albuterol": ["bronchodilator", "beta-2 agonist"],
    "formoterol": ["bronchodilator", "beta-2 agonist"],
    "ipratropium": ["bronchodilator", "anticholinergic"],
    "tiotropium": ["bronchodilator", "anticholinergic"],
    "montelukast": ["leukotriene inhibitor", "anti-inflammatory"],
    
    # ANTIHISTAMINES
    "famotidine": ["h2 blocker", "antihistamine"],
    "cetirizine": ["antihistamine", "h1 blocker"],
    "loratadine": ["antihistamine", "h1 blocker"],
    "diphenhydramine": ["antihistamine", "h1 blocker"],
    
    # INTERFERONS
    "interferon alpha": ["interferon", "antiviral", "immunomodulator"],
    "interferon beta": ["interferon", "antiviral", "immunomodulator"],
    "interferon gamma": ["interferon", "immunomodulator"],
    "peginterferon": ["interferon", "antiviral"],
    
    # PLASMA / BLOOD PRODUCTS
    "convalescent plasma": ["passive immunotherapy", "antibody therapy"],
    "ivig": ["immunoglobulin", "passive immunotherapy"],
    "immunoglobulin": ["immunoglobulin", "passive immunotherapy"],
    
    # OTHER
    "fluvoxamine": ["antidepressant", "ssri", "anti-inflammatory"],
    "famotidine": ["h2 blocker", "antacid"],
    "camostat": ["protease inhibitor", "tmprss2 inhibitor"],
    "nafamostat": ["protease inhibitor", "anticoagulant"],
    "pirfenidone": ["antifibrotic", "anti-inflammatory"],
    "nintedanib": ["antifibrotic", "tyrosine kinase inhibitor"],
    "n-acetylcysteine": ["mucolytic", "antioxidant"],
    "bromhexine": ["mucolytic", "tmprss2 inhibitor"],
    "niclosamide": ["anthelmintic", "antiviral"],
    "nitric oxide": ["vasodilator", "antimicrobial"],
    "sildenafil": ["pde5 inhibitor", "vasodilator"],
    "paxlovid": ["antiviral", "protease inhibitor"],
    "nirmatrelvir": ["antiviral", "protease inhibitor"],
}

# =============================================================================
# EFFICACY CATEGORIES (for grouping)
# =============================================================================
EFFICACY_CATEGORIES = {
    "Antivirals": ["antiviral", "rna polymerase inhibitor", "protease inhibitor", 
                   "neuraminidase inhibitor", "ns5b polymerase inhibitor"],
    "Anti-inflammatory": ["anti-inflammatory", "corticosteroid", "nsaid"],
    "Immunomodulators": ["immunomodulator", "il-6 inhibitor", "il-1 inhibitor", 
                         "jak inhibitor", "tnf inhibitor", "interferon"],
    "Antibodies": ["monoclonal antibody", "neutralizing antibody", "antibody therapy"],
    "Anticoagulants": ["anticoagulant", "antithrombotic", "antiplatelet"],
    "Antibiotics": ["antibiotic", "macrolide", "cephalosporin", "carbapenem"],
    "Cardiovascular": ["antihypertensive", "ace inhibitor", "arb", "statin"],
    "Respiratory": ["bronchodilator", "mucolytic", "antifibrotic"],
    "Supplements": ["vitamin", "mineral", "antioxidant"],
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def get_all_drugs():
    """Return list of all drug names."""
    return list(DRUG_EFFICACY_MAP.keys())

def get_all_efficacies():
    """Return set of all unique efficacies."""
    efficacies = set()
    for eff_list in DRUG_EFFICACY_MAP.values():
        efficacies.update(eff_list)
    return sorted(efficacies)

def get_drugs_by_efficacy(efficacy):
    """Return list of drugs with given efficacy."""
    drugs = []
    efficacy_lower = efficacy.lower()
    for drug, effs in DRUG_EFFICACY_MAP.items():
        if efficacy_lower in [e.lower() for e in effs]:
            drugs.append(drug)
    return drugs

def get_efficacies_for_drug(drug):
    """Return efficacies for a given drug."""
    return DRUG_EFFICACY_MAP.get(drug.lower(), [])
