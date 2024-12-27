def generate_routine(skin_type, sensitivity, concerns, weather):
    """Generate skincare routine based on skin type and weather conditions"""
    routine = []
    
    # Cleansing step
    if skin_type == "oily":
        routine.append({
            "step": "Cleanse",
            "product": "Gel or foam cleanser",
            "reason": "For oily skin, use a gel cleanser to remove excess oil"
        })
    else:
        routine.append({
            "step": "Cleanse",
            "product": "Cream or milk cleanser",
            "reason": "For dry/normal skin, use a gentle cream cleanser"
        })

    # Toner step
    if "sensitive" in sensitivity:
        routine.append({
            "step": "Tone",
            "product": "Alcohol-free calming toner",
            "reason": "Sensitive skin needs gentle, soothing ingredients"
        })
    else:
        routine.append({
            "step": "Tone",
            "product": "Hydrating toner",
            "reason": "Balance skin pH and prepare for next steps"
        })

    # Treatment step based on concerns
    if "acne" in concerns:
        routine.append({
            "step": "Treat",
            "product": "Salicylic acid serum",
            "reason": "Target breakouts and unclog pores"
        })
    elif "aging" in concerns:
        routine.append({
            "step": "Treat",
            "product": "Vitamin C serum",
            "reason": "Protect from environmental damage and boost collagen"
        })

    # Moisturizer based on weather and skin type
    if weather["humidity"] < 40:
        routine.append({
            "step": "Moisturize",
            "product": "Rich cream moisturizer",
            "reason": "Low humidity requires extra hydration"
        })
    elif weather["humidity"] > 70 and skin_type == "oily":
        routine.append({
            "step": "Moisturize",
            "product": "Light gel moisturizer",
            "reason": "High humidity means lighter hydration needed"
        })
    else:
        routine.append({
            "step": "Moisturize",
            "product": "Medium-weight moisturizer",
            "reason": "Balanced hydration for current conditions"
        })

    # Sunscreen based on UV index
    if weather.get("uv_index", 0) > 2:
        spf = "50+" if weather.get("uv_index", 0) > 5 else "30"
        routine.append({
            "step": "Protect",
            "product": f"Broad-spectrum SPF {spf}",
            "reason": f"UV index is {weather.get('uv_index')} - sun protection needed"
        })

    return routine
