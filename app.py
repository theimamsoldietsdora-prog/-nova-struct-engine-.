"""
NovaStruct AI - Main Application Runner
الملف الرئيسي لتشغيل محرك التصميم الإنشائي المتكامل
"""

from loads import BuildingLoadCalculator
from columns import ColumnDesigner
from foundation import RaftFoundationDesigner

def run_nova_struct_system(width: float, length: float, stories: int, use_type: str = "office"):
    print("==================================================")
    print("      NOVA-STRUCT AI | النظام الهندسي الذكي        ")
    print("==================================================")
    print(f"-> بيانات المبنى: واجهة {width}م × نزال {length}م | {stories} طوابق | الغرض: {use_type}")
    print("--------------------------------------------------\n--- 1. نتائج حسابات الأحمال الأفقية والتراكمية ---")
    
    # 1. تشغيل حسابات الأحمال
    load_engine = BuildingLoadCalculator(width, length, stories, use_type)
    slab_loads = load_engine.calculate_slab_loads()
    total_loads = load_engine.total_building_loads_on_base()
    
    print(f"• مساحة الطابق الواحد: {total_loads['floor_area_m2']} م٢")
    print(f"• إجمالي الحمل الميت التراكمي: {total_loads['cumulative_dead_kn']:.2f} kN")
    print(f"• إجمالي الحمل الحي المخفّض: {total_loads['cumulative_live_kn']:.2f} kN")
    print(f"• الحمل التصميمي الأقصى عند القاعدة (Pu): {total_loads['ultimate_load_pu_kn']:.2f} kN (~{total_loads['ultimate_load_tonnes']:.1f} طن)")
    
    # 2. تشغيل تصميم الأعمدة للطوابق السفلى
    print("\n--- 2. نتائج تصميم الأعمدة (الطوابق السفلى الحرجة) ---")
    col_engine = ColumnDesigner(pu_load_kn=total_loads['ultimate_load_pu_kn'] / 20, story_level=1)
    col_res = col_engine.design_column_section()
    print(f"• أبعاد قطاع العمود المقترح: {col_res['width_mm']} × {col_res['depth_mm']} ملم")
    print(f"• الحديد الطولي: {col_res['longitudinal_rebar']}")
    print(f"• الأطواق والعارضات: {col_res['ties_stirrups']}")
    
    # 3. تشغيل تصميم اللبشة الأساسية (Raft Foundation)
    print("\n--- 3. نتائج تصميم اللبشة الخرسانية والتربة ---")
    raft_width = width + 1.0  # مع بروز 0.5م من كل اتجاه
    raft_length = length + 1.0
    raft_engine = RaftFoundationDesigner(total_load_kn=total_loads['ultimate_load_pu_kn'] / 1.4, width=raft_width, length=raft_length)
    raft_res = raft_engine.check_soil_bearing_and_raft(allowable_soil_pressure_kpa=180.0)
    
    print(f"• مساحة اللبشة الكلية: {raft_res['raft_area_m2']} م٢ (بأبعاد {raft_width}×{raft_length} م)")
    print(f"• إجهاد التلامس الفعلي مع التربة: {raft_res['actual_soil_pressure_kpa']:.2f} kPa")
    print(f"• حالة التربة: {raft_res['soil_status']}")
    print(f"• سمك اللبشة المعتمد: {raft_res['recommended_thickness_mm']} ملم")
    print(f"• تسليح الشبكة السفلية: {raft_res['bottom_mesh']}")
    print(f"• تسليح الشبكة العلوية: {raft_res['top_mesh']}")
    print("\n==================================================")
    print("           تم إعداد التصميم بنجاح تام!            ")
    print("==================================================")

if __name__ == "__main__":
    # تشغيل النظام على مبنى المكاتب الخاص بنا (15م × 20م، 10 طوابق)
    run_nova_struct_system(width=15.0, length=20.0, stories=10, use_type="office")
