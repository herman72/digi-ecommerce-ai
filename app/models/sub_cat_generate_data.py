import random
from sqlalchemy.orm import sessionmaker
from db_models import Category, Product, ProductAttribute, ProductVariant, engine

Session = sessionmaker(bind=engine)
session = Session()

# Step 1: Find "Electronics" category
electronics = session.query(Category).filter_by(name="Electronics").first()
if not electronics:
    raise ValueError("Electronics category not found. Run the main script first.")

# Step 2: Create "Phone" subcategory if it doesn't exist
phone_category = session.query(Category).filter_by(name="Phone", parent_id=electronics.id).first()
if not phone_category:
    phone_category = Category(name="Phone", parent_id=electronics.id)
    session.add(phone_category)
    session.commit()

# Step 3: Generate and insert 100,000 products under "Phone"
BATCH_SIZE = 5000
TOTAL_PRODUCTS = 100_000

for batch_start in range(0, TOTAL_PRODUCTS, BATCH_SIZE):
    products = []
    attributes = []
    variants = []

    for i in range(batch_start, batch_start + BATCH_SIZE):
        product = Product(
            name=f"Phone_{i}",
            description=f"Smartphone model {i}",
            category_id=phone_category.id
        )
        session.add(product)
        products.append(product)

    # Flush to assign product IDs
    session.flush()

    for product in products:
        # Add attributes (e.g., RAM and Storage)
        attributes.extend([
            ProductAttribute(
                product_id=product.id,
                attribute_name="RAM",
                attribute_value=random.choice(["4GB", "6GB", "8GB"])
            ),
            ProductAttribute(
                product_id=product.id,
                attribute_name="Storage",
                attribute_value=random.choice(["64GB", "128GB", "256GB"])
            )
        ])

        # Add a variant
        variants.append(
            ProductVariant(
                product_id=product.id,
                variant_name="Standard",
                price=random.randint(200, 1200),
                stock_quantity=random.randint(5, 50)
            )
        )

    session.add_all(attributes)
    session.add_all(variants)
    session.commit()

    print(f"Inserted {batch_start + BATCH_SIZE} phone products...")

print("✅ Finished inserting 100,000 'Phone' products.")
