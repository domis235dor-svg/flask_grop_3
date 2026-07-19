from models import Product

#create'''
def add_product(name: str, price: float, category: str):
    Product.create(name=name, price=price, category=category)


def get_categories():
    products = Product.select(Product.category).distinct().order_by(Product.category)
    categories = [product.category for product in products]
    return categories

def get_products():
    return Product.select()

def get_products_by_category(category: str):
    return Product.select().where(Product.category == category)

def product_exists(name: str) -> bool:
    return Product.select().where(Product.name == name).exists()

#update'''
def edit_product(name: str, price: float, category: str):
    Product.update(
        price=price,
        category=category
    ).where(Product.name == name).execute()

#delete'''
def delete_product(name: str):
    Product.delete().where(Product.name == name).execute()