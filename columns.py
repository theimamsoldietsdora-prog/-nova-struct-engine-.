"""
NovaStruct AI - Column Design Engine
تصميم مقاطع وتحديد تسليح الأعمدة بناءً على الحمل الأقصى Pu
"""

class ColumnDesigner:
    def __init__(self, pu_load_kn: float, story_level: int):
        self.pu = pu_load_kn             # الحمل التصميمي الأقصى (كيلونيوتن)
        self.story_level = story_level   # مستوى الطوابق

    def design_column_section(self):
        """تحديد أبعاد العمود وتسليحه بناءً على الأحمال"""
        if self.pu > 3000:
            # الطوابق السفلى (1 - 3) - أحمال عالية
            b, h = 500, 600
            rebar = "12 فاي 20 مم (12Phi20)"
            ties = "فاي 10 مم لكل 150 مم"
        elif self.pu > 1500:
            # الطوابق الوسطى (4 - 7)
            b, h = 450, 450
            rebar = "8 فاي 20 مم (8Phi20)"
            ties = "فاي 10 مم لكل 150 مم"
        else:
            # الطوابق العليا (8 - 10) - أحمال خفيفة
            b, h = 350, 350
            rebar = "8 فاي 16 مم (8Phi16)"
            ties = "فاي 10 مم لكل 200 مم"

        return {
            "width_mm": b,
            "depth_mm": h,
            "longitudinal_rebar": rebar,
            "ties_stirrups": ties
        }

if __name__ == "__main__":
    # تجربة تصميم عمود يحمل 3821 كيلو نيوتن (الأعمدة السفلية للمبنى المكتبي)
    designer = ColumnDesigner(pu_load_kn=3821.2, story_level=1)
    res = designer.design_column_section()
    
    print("=== NovaStruct AI - Column Engine Test ===")
    print(f"أبعاد مقطع العمود: {res['width_mm']} × {res['depth_mm']} ملم")
    print(f"حديد التسليح الطولي: {res['longitudinal_rebar']}")
    print(f"الأطواق والعارضات: {res['ties_stirrups']}")
