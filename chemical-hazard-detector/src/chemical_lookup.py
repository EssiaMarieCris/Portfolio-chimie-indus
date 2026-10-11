import os
import json
import urllib.request
import urllib.parse

class OfficialChemicalLookup:
    def __init__(self, hazards_path=None):
        base_dir = os.path.dirname(__file__)
        self.hazards_path = hazards_path or os.path.join(base_dir, "../data/hazards.json")

        # Chargement du référentiel officiel local INRS
        if os.path.exists(self.hazards_path):
            with open(self.hazards_path, "r", encoding="utf-8") as f:
                self.hazards_db = {item["code"]: item for item in json.load(f)}
        else:
            self.hazards_db = {}

    def fetch_from_pubchem(self, chemical_name):
        """
        Requête directe vers le registre officiel PubChem PUG REST API.
        """
        encoded_name = urllib.parse.quote(chemical_name.strip())
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{encoded_name}/property/MolecularFormula,MolecularWeight,IUPACName/JSON"

        headers = {"User-Agent": "ChemicalHazardDetector/1.0 (Master Chimique Project)"}
        req = urllib.request.Request(url, headers=headers)

        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode("utf-8"))
                props = data["PropertyTable"]["Properties"][0]
                cid = props["CID"]
                
                # Extraction des données toxicologiques et des dangers normalisés
                ghs_data = self._fetch_ghs_data(cid)
                
                return {
                    "cid": cid,
                    "nom": chemical_name,
                    "formule": props.get("MolecularFormula", "Non renseignee"),
                    "masse_molaire": props.get("MolecularWeight", "Non renseignee"),
                    "nom_iupac": props.get("IUPACName", "Non renseigne"),
                    "mentions_h": ghs_data.get("h_statements", []),
                    "pictogrammes": ghs_data.get("pictograms", [])
                }
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            print(f"Erreur HTTP : {e.code}")
            return None
        except Exception as e:
            print(f"Erreur de communication reseau : {e}")
            return None

    def _fetch_ghs_data(self, cid):
        """
        Extraction de la classification CLP / SGH depuis le registre officiel.
        """
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON?heading=GHS+Classification"
        headers = {"User-Agent": "ChemicalHazardDetector/1.0"}
        req = urllib.request.Request(url, headers=headers)

        h_statements = []
        pictograms = []

        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode("utf-8"))
                sections = data.get("Record", {}).get("Section", [])
                
                def search_sections(sec_list):
                    for sec in sec_list:
                        if sec.get("TOCHeading") == "GHS Classification":
                            for info in sec.get("Information", []):
                                if info.get("Name") == "GHS Hazard Statements":
                                    for str_val in info.get("Value", {}).get("StringWithMarkup", []):
                                        h_statements.append(str_val.get("String"))
                                elif info.get("Name") == "Pictogram(s)":
                                    for mark in info.get("Value", {}).get("StringWithMarkup", []):
                                        for m in mark.get("Markup", []):
                                            url_pic = m.get("URL", "")
                                            if "GHS0" in url_pic:
                                                code = "GHS0" + url_pic.split("GHS0")[1][:1]
                                                if code not in pictograms:
                                                    pictograms.append(code)
                        if "Section" in sec:
                            search_sections(sec["Section"])

                search_sections(sections)
        except Exception:
            pass

        return {"h_statements": h_statements[:8], "pictograms": pictograms}

    def display_sheet(self, chem):
        print("\n" + "=" * 70)
        print(f" FICHE OFFICIELLE DE SECURITE : {chem['nom'].upper()}")
        print("=" * 70)
        print(f"Identifiant officiel (CID)  : {chem['cid']}")
        print(f"Formule brute                : {chem['formule']}")
        print(f"Masse molaire                : {chem['masse_molaire']} g/mol")
        print(f"Nom systematique IUPAC       : {chem['nom_iupac']}")

        print("\n[-] PICTOGRAMMES DE DANGER IDENTIFIES (CLP / SGH) :")
        if chem["pictogrammes"]:
            for pic in chem["pictogrammes"]:
                h_info = self.hazards_db.get(pic, {})
                label = h_info.get("symbole", "Pictogramme reglementaire")
                inrs = h_info.get("mention_inrs", "")
                inrs_txt = f" - « {inrs} »" if inrs else ""
                print(f"   {pic} ({label}){inrs_txt}")
        else:
            print("   Aucun pictogramme critique repertorie ou donnees non harmonisees.")

        print("\n[-] MENTIONS DE DANGER OFFICIELLES (Phrases H) :")
        if chem["mentions_h"]:
            for h in chem["mentions_h"]:
                print(f"   {h}")
        else:
            print("   Aucune mention specifique repertoriee.")

        print("\n[-] PRESCRIPTIONS DE STOCKAGE ET INCOMPATIBILITES (INRS) :")
        print("   Confinement sur bac de (retention) etanche inerte.")
        print("   Ventilation mecanique continue pour prevenir l'(volatilite) des vapeurs.")
        print("   Separation des reactifs pour eviter toute reaction (exothermique) violente.")
        print("=" * 70 + "\n")

if __name__ == "__main__":
    lookup = OfficialChemicalLookup()
    print("--- RECHERCHE OFFICIELLE SUR REGISTRE TOXICOLOGIQUE (PUBCHEM / INRS) ---")
    substance = input("Entrez le nom de la substance (ex: Benzene, Acetone, Sulfuric acid) : ").strip()

    if substance:
        print(f"Interrogation du registre officiel pour '{substance}'...")
        res = lookup.fetch_from_pubchem(substance)
        if res:
            lookup.display_sheet(res)
        else:
            print(f"[-] Substance '{substance}' introuvable dans le registre officiel.")