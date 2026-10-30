"""
NovaStruct AI - Load Calculator Engine
حساب الأحمال الميتة والحية التراكمية للمبنى
"""

class BuildingLoadCalculator:
    def __init__(self, width: float, length: float, stories: int, use_type: str = "office"):
        self.width = width          # عرض المبنى بالترتر (الواجهة)
        self.length = length        # نزال المبنى بالمتار
        self.stories = stories      # عدد الطوابق
        self.use_type = use_type    # غرض الاستخدام
        
        # المساحة الكلية للطابق الواحد
        self.floor_area = self.width * self.length
        
    def calculate_slab_loads(self):
        """حساب أحمال البلاطة والسقف (كيلونيوتن / م٢)"""
        # الوزن الذاتي لسقف خرساني بسمك 18 سم (الوزن النوعي 25 kN/m^3)
        self.self_weight = 0.18 * 25.0  # = 4.5 kN/m^2
        
        # الحمل الميت الإضافي (تشطيبات + قواطع + خدمات)
        self.sdl = 4.0  # kN/m^2
        
        # الحمل الحي حسب نوع الاستخدام (مكاتب = 3.5 kN/m^2)
        if self.use_type == "office":
            self.ll = 3.5
        else:
            self.ll = 3.0
            
        # إجمالي الحمل الميت للطابق الواحد
        total_dead_per_sqm = self.self_weight + self.sdl
        
        return {
            "self_weight_kn_m2": self.self_weight,
            "sdl_kn_m2": self.sdl,
            "ll_kn_m2": self.ll,
            "total_dead_kn_m2": total_dead_per_sqm
        }

    def total_building_loads_on_base(self):
        """حساب تجميع الأحمال الكلية على القاعدة وأسفل الأعمدة"""
        loads = self.calculate_slab_loads()
        
        # حمل الطابق الواحد الإجمالي (Dead + Live)
        floor_dead_total = (loads["total_dead_kn_m2"]) * self.floor_area
        floor_live_total = loads["ll_kn_m2"] * self.floor_area
        
        # تجميع الأحمال لكل الطوابق مع تطبيق معامل تخفيض الحمل الحي التراكمي
        cumulative_dead = floor_dead_total * self.stories
        
        # تخفيض الحمل الحي تدريجياً مع عدد الطوابق (بحد أدنى 50%)
        live_reduction_factor = max(0.5, 1.0 - (self.stories * 0.05))
        cumulative_live = (floor_live_total * self.stories) * live_reduction_factor
        
        # حساب الحمل التصميمي الأقصى (Factored Ultimate Load - Pu)
        pu_total = (1.2 * cumulative_dead) + (1.6 * cumulative_live)
        
        return {
            "floor_area_m2": self.floor_area,
            "cumulative_dead_kn": cumulative_dead,
            "cumulative_live_kn": cumulative_live,
            "ultimate_load_pu_kn": pu_total,
            "ultimate_load_tonnes": pu_total / 9.81
        }

# --- تجربة النظام ---
if __name__ == "__main__":
    # مبنى واجهة 15م، نزال 20م، 10 طوابق، مكاتب
    building = BuildingLoadCalculator(width=15.0, length=20.0, stories=10, use_type="office")
    
    print("=== NovaStruct AI - Engine Test ===")
    print(f"مساحة الطابق الواحد: {building.floor_area} م٢")
    
    results = building.total_building_loads_on_base()
    print(f"إجمالي الحمل الميت التراكمي: {results['cumulative_dead_kn']:.2f} kN")
    print(f"إجمالي الحمل الحي المخفّض: {results['cumulative_live_kn']:.2f} kN")
    print(f"الحمل التصميمي الأقصى عند القاعدة (Pu): {results['ultimate_load_pu_kn']:.2f} kN (~{results['ultimate_load_tonnes']:.1f} Tonnes)")
