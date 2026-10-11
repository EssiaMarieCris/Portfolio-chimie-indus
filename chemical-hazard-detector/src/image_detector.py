import os
import cv2
import json
import numpy as np

class VisualHazardDetector:
    def __init__(self, templates_dir=None, json_path=None):
        base_dir = os.path.dirname(__file__)
        self.templates_dir = templates_dir or os.path.join(base_dir, "../data/templates")
        json_path = json_path or os.path.join(base_dir, "../data/hazards.json")

        with open(json_path, "r", encoding="utf-8") as f:
            self.hazards_db = {item["code"]: item for item in json.load(f)}

    def _extract_core_symbol(self, img):
        """استخراج الرمز الأسود الداخلي فقط وتجاهل الإطار الأحمر والخلفية"""
        if len(img.shape) == 3:
            # عزل العناصر الداكنة والسوداء داخل الصورة
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img

        # قص هوامش الصورة الخارجية بنسبة 15% للتركيز حصراً على منتصف المعين
        h, w = gray.shape
        margin_y = int(h * 0.15)
        margin_x = int(w * 0.15)
        center_crop = gray[margin_y:h-margin_y, margin_x:w-margin_x]

        # تحويل لوني ثنائي نقي (أبيض وأسود فقط)
        _, binary = cv2.threshold(center_crop, 120, 255, cv2.THRESH_BINARY_INV)
        
        # توحيد أبعاد الرمز المقصوص إلى 150x150 بكسل
        return cv2.resize(binary, (150, 150))

    def detect_hazard_from_image(self, input_image_path):
        if not os.path.exists(input_image_path):
            return None, f"Fichier introuvable : {input_image_path}"

        img_query = cv2.imread(input_image_path)
        if img_query is None:
            return None, "Format d'image non valide."

        core_query = self._extract_core_symbol(img_query)

        template_files = [f for f in os.listdir(self.templates_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if not template_files:
            return None, "Dossier data/templates vide."

        scores = {}

        for tf in template_files:
            code = os.path.splitext(tf)[0].upper()
            t_path = os.path.join(self.templates_dir, tf)
            img_tpl = cv2.imread(t_path)
            if img_tpl is None:
                continue

            core_tpl = self._extract_core_symbol(img_tpl)

            # حساب التشابه عبر نسبة البكسلات المتطابقة تماماً بين الرمزين
            intersection = np.logical_and(core_query > 0, core_tpl > 0).sum()
            union = np.logical_or(core_query > 0, core_tpl > 0).sum()
            
            # مؤشر جاوكارد (IoU) للتشابه البصري الحقيقي
            iou_score = intersection / union if union > 0 else 0.0

            # ارتباط القوالب المعياري المساعد
            match_res = cv2.matchTemplate(core_query, core_tpl, cv2.TM_CCOEFF_NORMED)[0][0]
            
            # الجمع الوزني بين التطابق البنيوي وارتباط القوالب
            final_score = (iou_score * 0.6) + (max(0, match_res) * 0.4)
            scores[code] = final_score

        # اختيار الرمز الحاصل على أعلى درجة مطابقة
        best_code = max(scores, key=scores.get)
        best_score = scores[best_code]

        if best_code in self.hazards_db:
            return self.hazards_db[best_code], f"Concordance optimale avec {best_code} (Score : {best_score * 100:.1f}%)"

        return None, "Echec de classification."

    def display_report(self, hazard_data):
        if not hazard_data:
            print("[-] Aucun danger identifie.")
            return

        print("\n==================================================")
        print(f" RAPPORT REGLEMENTAIRE : {hazard_data['code']} - {hazard_data['symbole'].upper()}")
        print("==================================================")
        print(f"Formule officielle INRS : « {hazard_data['mention_inrs']} »")
        print(f"Classe de danger        : {hazard_data['categorie']}")
        print(f"Description technique   : {hazard_data['description']}")
        print(f"Risques critiques       : {hazard_data['risques']}")
        print(f"Prescriptions stockage  : {hazard_data['mesures_stockage']}")
        print("==================================================\n")

if __name__ == "__main__":
    detector = VisualHazardDetector()
    print("--- CLASSIFICATION DIRECTE DES PICTOGRAMMES ---")
    user_path = input("Chemin de l'image a analyser : ").strip().replace('"', '').replace("'", "")

    res, msg = detector.detect_hazard_from_image(user_path)
    if res:
        detector.display_report(res)
        print(f"Validation : {msg}")
    else:
        print(f"[-] {msg}")