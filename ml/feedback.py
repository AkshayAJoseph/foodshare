def generate_food_feedback(food_item):
    return {
        'storage_tip': FOOD_CATEGORIES.get(food_item, {}).get('storage_advice', ''),
        'recipe': FOOD_CATEGORIES.get(food_item, {}).get('recipe_suggestion', ''),
        'preservation_method': get_preservation_method(food_item)
    }