import random
from sqlalchemy.orm import sessionmaker
from db_models import Category, Product, ProductAttribute, ProductVariant, engine


Session = sessionmaker(bind=engine)
session = Session()

category_name = ["Electronics", "Clothing", "Books", "Furniture", "Toys"]
categories = [Category(name=name) for name in category_name]
session.add_all(categories)
session.commit()

categories = session.query(Category).all()
category_ids = [cat.id for cat in categories]

BATCH_SIZE = 10000
TOTAL_PRODUCTS = 1_000_000

def random_text(prefeix, id):
    return f"{prefeix}_{id}"

for batch_start in range(0, TOTAL_PRODUCTS, BATCH_SIZE):
    batch_products = []
    batch_attributes = []
    batch_variants = []
    
    for i in range(batch_start, batch_start+BATCH_SIZE):
        category_id = random.choice(category_ids)
        product = Product(
            name = random_text("Product", i),
            description=random_text("Description", i),
            category_id=category_id
        )
        batch_products.append(product)
        
    # session.bulk_save_objects(batch_products)
    session.add_all(batch_products)
    session.flush()
    
    for product in batch_products:
        batch_attributes.extend([
            ProductAttribute(
                product_id=product.id,
                attribute_name="Color",
                attribute_value=random.choice(["Red", "Green", "Blue"])
        ),
        ProductAttribute(
                product_id=product.id,
                attribute_name="Size",
                attribute_value=random.choice(["S", "M", "L", "XL"])
            )
        ])
        
        batch_variants.append(
            ProductVariant(
                product_id=product.id,
                variant_name="Default Variant",
                price=random.randint(10, 1000),
                stock_quantity=random.randint(1, 100)
            )
        )
        
        
    session.bulk_save_objects(batch_attributes)
    session.bulk_save_objects(batch_variants)
    session.commit()
    print(f"Inserted {batch_start + BATCH_SIZE} products...")
    
print("✅ Finished inserting 1 million records.")
