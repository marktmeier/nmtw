from models import Product
from app import db
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

def get_weather_condition(weather_data: Dict) -> List[str]:
    """Determine weather conditions based on temperature and humidity"""
    conditions = []

    temp = weather_data.get('temperature', 0)
    humidity = weather_data.get('humidity', 50)

    if temp > 25:
        conditions.append('hot')
    elif temp < 15:
        conditions.append('cold')

    if humidity > 70:
        conditions.append('humid')
    elif humidity < 40:
        conditions.append('dry')

    return conditions

def get_product_recommendations(
    skin_type: str,
    concerns: List[str],
    weather_data: Dict,
    category: str = None
) -> List[Product]:
    """
    Get personalized product recommendations based on user's skin profile and weather

    Args:
        skin_type: User's skin type (e.g., 'oily', 'dry')
        concerns: List of skin concerns (e.g., ['acne', 'aging'])
        weather_data: Current weather conditions
        category: Optional product category filter

    Returns:
        List of recommended products
    """
    try:
        logger.debug(f"Getting recommendations for skin_type={skin_type}, concerns={concerns}")

        # Base query
        query = Product.query

        # Filter by skin type
        query = query.filter(Product.skin_types.contains(skin_type))

        # Filter by category if specified
        if category:
            query = query.filter_by(category=category)

        # Get current weather conditions
        weather_conditions = get_weather_condition(weather_data)
        if weather_conditions:
            # Find products suitable for current weather
            conditions_filter = [
                Product.weather_conditions.contains(condition)
                for condition in weather_conditions
            ]
            query = query.filter(db.or_(*conditions_filter))

        # Consider skin concerns if any
        if concerns:
            concerns_filter = [
                Product.concerns.contains(concern)
                for concern in concerns
            ]
            query = query.filter(db.or_(*concerns_filter))

        # Get results
        products = query.all()
        logger.debug(f"Found {len(products)} matching products")

        return products

    except Exception as e:
        logger.error(f"Error getting product recommendations: {str(e)}")
        return []