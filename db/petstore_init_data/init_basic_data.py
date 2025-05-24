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


def init_basic_data():  # launch at main1.py by import
    session = db_session.create_session()
    for role in session.query(Role).all():
        session.delete(role)
    for role_name in ROLES:
        role = Role()
        role.role = role_name
        session.add(role)

    for category in session.query(Category).all():
        session.delete(category)
    for category_name in CATEGORIES:
        category = Category()
        category.name = category_name
        session.add(category)

    for product in session.query(Product).all():
        session.delete(product)
    for product_entry in PRODUCTS:
        product = Product()
        product.user_id = product_entry[0]
        product.category_id = product_entry[1]
        product.name = product_entry[2]
        if product_entry[3]:
            product.profile_img_path = product_entry[3]
        product.short_description = product_entry[4]
        product.long_description = product_entry[5]
        product.specifications = product_entry[6]
        product.promo = product_entry[7]
        product.price = product_entry[8]
        session.add(product)

    for user in session.query(User).all():
        session.delete(user)
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
