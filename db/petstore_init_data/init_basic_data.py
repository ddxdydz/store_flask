import data.db_session as db_session
from data.__all_models import *
from db.petstore_init_data.products_data import PRODUCTS
from db.petstore_init_data.users_data import USERS

ROLES = ("Администратор", "Обычный пользователь")
CATEGORIES = (
    "Корма и ветеринарные диеты",
    "Уходовые средства",
    "Игрушки",
    "Амуниция",
    "Товары для гигиены",
    "Аксессуары для дрессировки и обучения",
    "Переноски и автогамаки",
    "Ветпрепараты"
)


def init_roles():
    session = db_session.create_session()
    for role in session.query(Role).all():
        session.delete(role)
    session.commit()
    for role_name in ROLES:
        role = Role()
        role.role = role_name
        session.add(role)
    session.commit()


def init_categories():
    session = db_session.create_session()
    for category in session.query(Category).all():
        session.delete(category)
    session.commit()
    for category_name in CATEGORIES:
        category = Category()
        category.name = category_name
        session.add(category)
    session.commit()


def init_users():
    session = db_session.create_session()
    for user in session.query(User).all():
        session.delete(user)
    session.commit()
    for user_data in USERS:
        user = User()
        user.name, user.email, _, user.role_id, user.balance, _, _ = user_data
        user.set_password(user_data[2])
        if user_data[-2]:
            user.about = user_data[-2]
        if user_data[-1]:
            user.profile_img_path = user_data[-1]
        session.add(user)
    session.commit()


def init_products():
    session = db_session.create_session()
    from db.petstore_init_data.products_data import PRODUCTS
    for product in session.query(Product).all():
        session.delete(product)
    session.commit()
    for product_entry in PRODUCTS:
        product = Product()
        product.user_id = product_entry[0]
        product.category_id = product_entry[1]
        product.name = product_entry[2]
        product.profile_img_path = product_entry[3]
        product.short_description = product_entry[4]
        product.long_description = product_entry[5]
        product.specifications = product_entry[6]
        product.promo = product_entry[7]
        product.price = product_entry[8]
        session.add(product)
    session.commit()


def init_basic_data():  # launch at main1.py by import
    init_roles()
    init_users()
    init_categories()
    init_products()
