import re

def extract_number(value):
    """
    extract numbers from string and convert to float
    example: '180kcal' -> 180.0
    """
    if isinstance(value, (int, float)):
        return float(value)
    match = re.search(r'(\d+\.?\d*)', str(value))
    return float(match.group(1)) if match else 0.0

def get_recommended_daily_values():
    """
    return daily recommended intake
    based on 2020 Korean Dietary Reference Intakes for Koreans
    adult male standard (19-29 years old)
    """
    return {
        'calories': 2600,        # kcal
        'carbohydrates': 360,    # g (총 에너지의 약 55-65%)
        'protein': 65,           # g
        'fat': 65,              # g (총 에너지의 약 20-25%)
        'fiber': 25,            # g
        'sodium': 2300          # mg
    }

def create_food_card(food_info, confidence):
    """
    Create a card for food information
    """
    # 섭취 시간 포맷팅
    consumption_time = food_info['created_at'].strftime("%Y-%m-%d %H:%M")
    
    return f"""
    <div style="padding: 15px; border-radius: 15px; border: 1px solid #e0e0e0; margin-bottom: 20px; overflow: hidden;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
            <div style="font-size: 1.1em; font-weight: bold;">{food_info.get('food_name', '알 수 없음')}</div>
            <div style="font-size: 0.9em; color: #666;">신뢰도: {confidence:.1f}%</div>
        </div>
        <div style="font-size: 0.9em; color: #666; margin-bottom: 10px;">섭취 시간: {consumption_time}</div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)); gap: 10px;">
            <div>
                <div style="font-size: 0.75em; color: #666;">에너지</div>
                <div style="font-size: 0.9em; margin-top: 2px;">{food_info.get('Energy', '정보 없음')}</div>
            </div>
            <div>
                <div style="font-size: 0.75em; color: #666;">탄수화물</div>
                <div style="font-size: 0.9em; margin-top: 2px;">{food_info.get('Carbohydrates', '정보 없음')}</div>
            </div>
            <div>
                <div style="font-size: 0.75em; color: #666;">단백질</div>
                <div style="font-size: 0.9em; margin-top: 2px;">{food_info.get('Protein', '정보 없음')}</div>
            </div>
            <div>
                <div style="font-size: 0.75em; color: #666;">지방</div>
                <div style="font-size: 0.9em; margin-top: 2px;">{food_info.get('Fat', '정보 없음')}</div>
            </div>
            <div>
                <div style="font-size: 0.75em; color: #666;">식이섬유</div>
                <div style="font-size: 0.9em; margin-top: 2px;">{food_info.get('Dietary_Fiber', '정보 없음')}</div>
            </div>
            <div>
                <div style="font-size: 0.75em; color: #666;">나트륨</div>
                <div style="font-size: 0.9em; margin-top: 2px;">{food_info.get('Sodium', '정보 없음')}</div>
            </div>
        </div>
    </div>
    """

def create_warning_section(totals):
    """
    create warning section for nutritional components intake
    """
    recommended = get_recommended_daily_values()
    warnings = []
    
    # calculate intake percentage for each nutritional component and check if it exceeds 100%
    percentages = {
        '에너지': (totals['calories'] / recommended['calories']) * 100,
        '탄수화물': (totals['carbohydrates'] / recommended['carbohydrates']) * 100,
        '단백질': (totals['protein'] / recommended['protein']) * 100,
        '지방': (totals['fat'] / recommended['fat']) * 100,
        '식이섬유': (totals['fiber'] / recommended['fiber']) * 100,
        '나트륨': (totals['sodium'] / recommended['sodium']) * 100
    }
    
    # collect over items 100%
    over_items = [f"{name}({int(pct)}%)" for name, pct in percentages.items() if pct > 100]
    
    if not over_items:
        return ""  # if no over items, return empty string
    
    warning_text = ", ".join(over_items) + " 항목에서 권장섭취량을 초과했습니다."
    
    return f"""
    <div style="padding: 15px; border-radius: 15px; border: 1px solid #FFB74D; margin-bottom: 20px; 
         background-color: #FFF3E0; overflow: hidden;">
        <h3 style="margin: 0 0 15px 0; font-size: 1.1em; color: #F57C00;">⚠️ 섭취량 경고</h3>
        <div style="font-size: 0.9em; color: #E65100;">
            {warning_text}
        </div>
    </div>
    """

def create_summary_section(totals):
    """
    create summary section for nutritional components
    """
    recommended = get_recommended_daily_values()
    
    return f"""
    <div style="padding: 15px; border-radius: 15px; border: 1px solid #e0e0e0; margin-bottom: 20px; overflow: hidden;">
        <h3 style="margin: 0 0 15px 0; font-size: 1.1em;">📊 하루 권장 영양성분 총계</h3>
        <div style="display: grid; grid-template-columns: 1fr 3fr 1fr; gap: 10px; align-items: center;">
            <div style="font-size: 0.9em; color: #666;">에너지</div>
            <div style="width: 100%; height: 24px; background-color: #f0f0f0; border-radius: 12px; overflow: hidden;">
                <div style="width: {(totals['calories'] / recommended['calories']) * 100}%; height: 100%; 
                     background-color: #4CAF50; transition: width 0.3s ease;"></div>
            </div>
            <div style="font-size: 0.9em; text-align: right;">{int((totals['calories'] / recommended['calories']) * 100)}%</div>

            <div style="font-size: 0.9em; color: #666;">탄수화물</div>
            <div style="width: 100%; height: 24px; background-color: #f0f0f0; border-radius: 12px; overflow: hidden;">
                <div style="width: {(totals['carbohydrates'] / recommended['carbohydrates']) * 100}%; height: 100%; 
                     background-color: #9C27B0; transition: width 0.3s ease;"></div>
            </div>
            <div style="font-size: 0.9em; text-align: right;">{int((totals['carbohydrates'] / recommended['carbohydrates']) * 100)}%</div>

            <div style="font-size: 0.9em; color: #666;">단백질</div>
            <div style="width: 100%; height: 24px; background-color: #f0f0f0; border-radius: 12px; overflow: hidden;">
                <div style="width: {(totals['protein'] / recommended['protein']) * 100}%; height: 100%; 
                     background-color: #FF9800; transition: width 0.3s ease;"></div>
            </div>
            <div style="font-size: 0.9em; text-align: right;">{int((totals['protein'] / recommended['protein']) * 100)}%</div>

            <div style="font-size: 0.9em; color: #666;">지방</div>
            <div style="width: 100%; height: 24px; background-color: #f0f0f0; border-radius: 12px; overflow: hidden;">
                <div style="width: {(totals['fat'] / recommended['fat']) * 100}%; height: 100%; 
                     background-color: #E91E63; transition: width 0.3s ease;"></div>
            </div>
            <div style="font-size: 0.9em; text-align: right;">{int((totals['fat'] / recommended['fat']) * 100)}%</div>

            <div style="font-size: 0.9em; color: #666;">식이섬유</div>
            <div style="width: 100%; height: 24px; background-color: #f0f0f0; border-radius: 12px; overflow: hidden;">
                <div style="width: {(totals['fiber'] / recommended['fiber']) * 100}%; height: 100%; 
                     background-color: #2196F3; transition: width 0.3s ease;"></div>
            </div>
            <div style="font-size: 0.9em; text-align: right;">{int((totals['fiber'] / recommended['fiber']) * 100)}%</div>

            <div style="font-size: 0.9em; color: #666;">나트륨</div>
            <div style="width: 100%; height: 24px; background-color: #f0f0f0; border-radius: 12px; overflow: hidden;">
                <div style="width: {(totals['sodium'] / recommended['sodium']) * 100}%; height: 100%; 
                     background-color: #FF5722; transition: width 0.3s ease;"></div>
            </div>
            <div style="font-size: 0.9em; text-align: right;">{int((totals['sodium'] / recommended['sodium']) * 100)}%</div>
        </div>
    </div>
    """ 