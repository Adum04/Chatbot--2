from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Suppliers(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contactinfo = db.Column(db.String(100), nullable=False)
    product_categories_offered = db.Column(db.String(400), nullable=False)


class Products(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id"), nullable=False)
    supplier = db.relationship("Suppliers", backref="products")


# Sample data population
def populate_sample_data():
    # Sample suppliers
    supplier1 = Suppliers(
        name="Tech World",
        contactinfo="contact@techworld.com",
        product_categories_offered="Laptops",
    )
    supplier2 = Suppliers(
        name="Gadget Hub",
        contactinfo="info@gadgethub.com",
        product_categories_offered="Laptops",
    )

    # Sample laptop products
    product1 = Products(
        name="Laptop Pro 15",
        brand="BrandTech",
        price=1200,
        category="Laptops",
        description="A powerful laptop designed for professionals.",
        supplier_id=1,
    )
    product2 = Products(
        name="Gaming Laptop X",
        brand="GamerZone",
        price=1500,
        category="Laptops",
        description="A high-performance laptop for gamers.",
        supplier_id=1,
    )
    product3 = Products(
        name="UltraBook Slim 14",
        brand="SlimTech",
        price=1000,
        category="Laptops",
        description="A lightweight and sleek ultrabook.",
        supplier_id=2,
    )
    product4 = Products(
        name="Laptop Max 17",
        brand="MaxCompute",
        price=1800,
        category="Laptops",
        description="A large screen laptop for multitasking.",
        supplier_id=2,
    )

    # Add to database
    db.session.add_all([supplier1, supplier2, product1, product2, product3, product4])
    db.session.commit()
