from app import app, db
from models import Product

def init_products():
    """Initialize database with sample skincare products"""
    products = [
        Product(
            name="Gentle Foam Cleanser",
            category="cleanse",
            skin_types="oily,combination",
            concerns="acne,sensitive",
            ingredients="Salicylic Acid, Tea Tree Oil, Aloe Vera",
            description="A gentle foaming cleanser that removes excess oil without stripping the skin",
            weather_conditions="humid,hot"
        ),
        Product(
            name="Hydrating Cream Cleanser",
            category="cleanse",
            skin_types="dry,normal",
            concerns="sensitive,dryness",
            ingredients="Ceramides, Hyaluronic Acid, Glycerin",
            description="A creamy cleanser that cleanses while maintaining skin's moisture barrier",
            weather_conditions="dry,cold"
        ),
        Product(
            name="Hyaluronic Acid Toner",
            category="tone",
            skin_types="all",
            concerns="dryness,sensitive",
            ingredients="Hyaluronic Acid, Panthenol, Niacinamide",
            description="Alcohol-free hydrating toner suitable for all skin types",
            weather_conditions="all"
        ),
        Product(
            name="BHA Treatment",
            category="treat",
            skin_types="oily,combination",
            concerns="acne",
            ingredients="Salicylic Acid, Niacinamide, Green Tea",
            description="Unclogs pores and reduces breakouts",
            weather_conditions="humid"
        ),
        Product(
            name="Vitamin C Serum",
            category="treat",
            skin_types="all",
            concerns="aging,pigmentation",
            ingredients="Vitamin C, Ferulic Acid, Vitamin E",
            description="Brightens and protects against environmental damage",
            weather_conditions="all"
        ),
        Product(
            name="Light Gel Moisturizer",
            category="moisturize",
            skin_types="oily,combination",
            concerns="acne,sensitive",
            ingredients="Niacinamide, Hyaluronic Acid, Aloe",
            description="Lightweight hydration that won't clog pores",
            weather_conditions="humid,hot"
        ),
        Product(
            name="Rich Cream Moisturizer",
            category="moisturize",
            skin_types="dry,normal",
            concerns="aging,dryness",
            ingredients="Ceramides, Peptides, Shea Butter",
            description="Rich moisturizer that provides lasting hydration",
            weather_conditions="dry,cold"
        ),
        Product(
            name="Lightweight Sunscreen SPF 50",
            category="protect",
            skin_types="oily,combination",
            concerns="sensitive,aging",
            ingredients="Zinc Oxide, Titanium Dioxide",
            description="Non-greasy mineral sunscreen with high protection",
            weather_conditions="hot,humid"
        ),
        Product(
            name="Moisturizing Sunscreen SPF 50",
            category="protect",
            skin_types="dry,normal",
            concerns="aging,dryness",
            ingredients="Zinc Oxide, Hyaluronic Acid, Ceramides",
            description="Hydrating mineral sunscreen with high protection",
            weather_conditions="dry,cold"
        )
    ]
    
    # Add products to database
    for product in products:
        existing = Product.query.filter_by(name=product.name).first()
        if not existing:
            db.session.add(product)
    
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        init_products()
