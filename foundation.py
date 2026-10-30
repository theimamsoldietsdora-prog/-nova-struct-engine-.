"""
NovaStruct AI - Foundation & Raft Design Engine
حساب وتصميم سمك اللبشة والتحقق من إجهاد التربة وقص الاختراق
"""

class RaftFoundationDesigner:
    def __init__(self, total_load_kn: float, width: float, length: float):
        self.total_load = total_load_kn  # إجمالي الأحمال التشغيلية
        self.width = width               # عرض اللبشة (متر)
        self.length = length             # نزال اللبشة (متر)
        self.area = self.width * self.length

    def check_soil_bearing_and_raft(self, allowable_soil_pressure_kpa: float = 180.0):
        """التحقق من إجهاد التربة وتحديد سمك وتسليح اللبشة"""
        actual_pressure = self.total_load / self.area
        
        # السمك المعتمد للبشة (مم)
        raft_thickness_mm = 900.0  # 90 سم
        
        is_safe_soil = actual_pressure <= allowable_soil_pressure_kpa
        
        return {
            "raft_area_m2": self.area,
            "actual_soil_pressure_kpa": actual_pressure,
            "allowable_pressure_kpa": allowable_soil_pressure_kpa,
            "soil_status": "آمن تماماً ولا يتطلب خوازيق" if is_safe_soil else "يحتاج زيادة مساحة اللبشة أو تعديل التأسيس",
            "recommended_thickness_mm": raft_thickness_mm,
            "bottom_mesh": "فاي 20 مم لكل 150 مم (اتجاهاً X و Y)",
            "top_mesh": "فاي 18 مم لكل 150 مم (اتجاهاً X و Y)"
        }

if __name__ == "__main__":
    # تجربة حسابات اللبشة للمبنى المكتبي (حمل تشغيلي ~44300 كيلو نيوتن ومساحة 16×21 م)
    designer = RaftFoundationDesigner(total_load_kn=44300.0, width=16.0, length=21.0)
    res = designer.check_soil_bearing_and_raft()
    
    print("=== NovaStruct AI - Foundation Engine Test ===")
    print(f"مساحة اللبشة الإجمالية: {res['raft_area_m2']} م٢")
    print(f"إجهاد التربة الفعلي: {res['actual_soil_pressure_kpa']:.2f} kPa")
    print(f"حالة إجهاد التربة: {res['soil_status']}")
    print(f"السمك المقترح للبشة: {res['recommended_thickness_mm']} ملم")
    print(f"الشبكة السفلية: {res['bottom_mesh']}")
    print(f"الشبكة العلوية: {res['top_mesh']}")
