import os
from datetime import datetime

from flask import Flask, request, render_template, redirect, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api
from werkzeug.security import check_password_hash

import data.db_session as db_session
from api.__all_resources import *
from api.other_api_parts import login_api, get_img_api, send_img_api
from data.__all_models import *
from data.utils.upload_image import upload_image
from data.utils.Logger import *
from forms.__all_forms import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'wtf_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
api = Api(app)
hashed_admin_key = "pbkdf2:sha256:150000$phWNreer$470eaca149f9a2c60bf848a614915b890e26015c5ed47ab69a7e5fa533d7cacf"

login_manager = LoginManager()
login_manager.init_app(app)

all_category_names = []
all_role_names = []


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        if form.password.data != form.password_again.data:
            return render_template(
                'register.html', title='Регистрация', form=form,
                message="Пароли не совпадают")

        session = db_session.create_session()

        if session.query(User).filter(User.email == form.email.data).first():
            return render_template(
                'register.html', title='Регистрация', form=form,
                message="Такой пользователь уже есть")

        user = User()
        user.name = form.name.data
        user.email = form.email.data
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/")
@app.route("/index")
def index():
    return redirect("/categories/0")


@app.route("/categories/<int:category_id>")
def categories(category_id):
    if category_id not in range(0, len(all_category_names)):
        abort(404)
    session = db_session.create_session()
    if category_id == 0:
        products = session.query(Product).all()
    else:
        products = session.query(Product).filter(Product.category_id == category_id)
    return render_template('index.html', category_id=category_id,
                           products=products, all_category_names=all_category_names)


@app.route("/search_products", methods=['GET', 'POST'])
def search_products():
    form = ProductSearchForm()
    session = db_session.create_session()
    search_request = str(form.search.data).lower() if form.search.data else ''

    # sqlalchemy.func.lower не работает с кириллицей
    # products = session.query(Product).filter(func.lower(Product.name).like(f'%{search_request}%'))

    if form.category.data and int(form.category.data):
        products = session.query(Product).filter(Product.category_id == int(form.category.data))
    else:
        products = session.query(Product).all()

    filtered_products = [
        product for product in products
        if search_request.lower() in product.name.lower()
    ]

    return render_template('product_search.html', form=form,
                           products=filtered_products, all_category_names=all_category_names)


@app.route("/search_users", methods=['GET', 'POST'])
def search_users():
    form = UserSearchForm()
    session = db_session.create_session()
    search_request = str(form.search.data).lower() if form.search.data else ''

    if form.role.data and int(form.role.data):
        users = session.query(User).filter(User.role_id == int(form.role.data))
    else:
        users = session.query(User).all()

    filtered_users = [
        user for user in users
        if search_request in user.email.lower() or search_request in user.name.lower()
    ]

    return render_template('user_search.html', form=form,
                           users=filtered_users)


@app.route("/user_page")
def user_page():
    if not current_user.is_authenticated:
        return redirect("/register")
    return redirect(f"/profile/{current_user.id}")


@app.route("/user_balance/<int:user_id>", methods=['GET', 'POST'])
def user_balance(user_id):
    if not current_user.is_authenticated:
        return redirect("/register")
    if not (current_user.id == user_id):
        return abort(403)

    session = db_session.create_session()
    user = session.query(User).filter(User.id == user_id).first()

    form = BalanceForm()
    if request.method == "GET":
        return render_template('balance.html', form=form, user=user)
    else:
        if isinstance(form.count.data, int) and 0 < form.count.data < 100001:
            user.add_to_balance(int(form.count.data))
            session.commit()
            return redirect(f'/profile/{user.id}')
        return render_template(
            'balance.html', form=form, user=user,
            message="Ошибка ввода: Сумма пополнения должна быть числом в диапазоне от 1 до 100000")


@app.route("/admin_verification/<int:user_id>", methods=['GET', 'POST'])
def admin_verification(user_id):
    if not current_user.is_authenticated:
        return redirect("/register")
    if not (current_user.id == user_id):
        return abort(403)

    session = db_session.create_session()
    user = session.query(User).filter(User.id == user_id).first()

    form = AdminKeyForm()
    if request.method == "GET":
        return render_template('user_adminkey.html', form=form, user=user)
    else:
        input_key = form.admin_key.data
        if check_password_hash(hashed_admin_key, str(input_key)):
            user.role_id = 1
            session.commit()
            return redirect(f'/profile/{user.id}')
        return render_template('user_adminkey.html',
                               form=form, user=user, message="Неверный admin_key")


@app.route('/profile/<int:user_id>')
def profile(user_id):
    session = db_session.create_session()
    user = session.query(User).filter(User.id == user_id).first()
    role = session.query(Role).filter(Role.id == user.role_id).first()
    return render_template('user_profile.html', user=user, role=role)


@app.route('/edit_profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_profile(user_id):
    if current_user.id == user_id:
        form = UserForm()
        session = db_session.create_session()
        user = session.query(User).filter(User.id == user_id).first()
        if request.method == "GET":
            form.name.data = user.name
            form.about.data = user.about
            return render_template('user_edit.html', form=form, user=user)
        else:
            if not form.delete_img.data:
                img_path = upload_image(form.profile_img.data)
                if img_path:
                    user.profile_img_path = img_path
            else:
                user.profile_img_path = r"static\imgs\noimg.jpg"
            user.name = form.name.data
            user.about = form.about.data
            session.add(user)
            session.commit()
            return redirect(f'/profile/{user.id}')
    else:
        return redirect('/')


def get_current_user_cart_info() -> (int, list[dict]):
    cart_entries_data = []
    total_cart_price = 0
    session = db_session.create_session()
    cart_entries = session.query(CartEntry).filter(CartEntry.user_id == current_user.id)
    for cart_entry in cart_entries:
        product = session.query(Product).filter(Product.id == cart_entry.product_id).first()
        cart_entries_data.append({
            "product_id": product.id,
            "product_name": product.name,
            "profile_img_path": product.profile_img_path,
            "count": cart_entry.count,
            "total_price": cart_entry.count * product.price
        })
        total_cart_price += cart_entry.count * product.price
    return total_cart_price, cart_entries_data


@app.route("/to_cart")
def to_cart():
    if not current_user.is_authenticated:
        return redirect("/register")
    return redirect(f"/user_cart/{current_user.id}")


@app.route("/user_cart/<int:user_id>")
def user_cart(user_id):
    if not current_user.is_authenticated:
        return redirect("/register")
    if not current_user.id == user_id:
        return abort(403)
    total_cart_price, cart_entries_data = get_current_user_cart_info()
    return render_template('user_cart.html',
                           cart_entries_data=cart_entries_data,
                           total_cart_price=total_cart_price)


@app.route("/add_to_user_cart/<int:product_id>", methods=['GET', 'POST'])
def add_to_user_cart(product_id):
    if not current_user.is_authenticated:
        return redirect("/register")

    session = db_session.create_session()
    cart_entry = session.query(CartEntry).filter(
        CartEntry.product_id == product_id,
        CartEntry.user_id == current_user.id).first()
    if cart_entry:
        cart_entry.add()
    else:
        cart_entry = CartEntry()
        cart_entry.product_id = product_id
        cart_entry.user_id = current_user.id

    session.add(cart_entry)
    session.commit()

    if cart_entry.count == 1:
        return redirect(f"/product/{product_id}")
    return redirect(f"/user_cart/{current_user.id}")


@app.route("/remove_from_user_cart/<int:product_id>", methods=['GET', 'POST'])
def remove_from_user_cart(product_id):
    if not current_user.is_authenticated:
        return redirect("/register")

    session = db_session.create_session()
    cart_entry = session.query(CartEntry).filter(
        CartEntry.product_id == product_id,
        CartEntry.user_id == current_user.id).first()
    if cart_entry:
        cart_entry.sub()

    session.add(cart_entry)
    if cart_entry.count == 0:
        session.delete(cart_entry)
    session.commit()

    return redirect(f"/user_cart/{current_user.id}")


@app.route("/user_orders")
def user_orders():
    if not current_user.is_authenticated:
        return redirect("/register")
    session = db_session.create_session()
    orders = session.query(OrderEntry).filter(OrderEntry.user_id == current_user.id)
    return render_template('orders.html', orders=orders)


@app.route("/do_order", methods=['GET', 'POST'])
def do_order():
    if not current_user.is_authenticated:
        return redirect("/register")

    form = OrderSubmitForm()
    total_cart_price, cart_entries_data = get_current_user_cart_info()
    if request.method == "GET":
        return render_template(
            'order_submit.html', cart_entries_data=cart_entries_data,
            total_cart_price=total_cart_price, form=form)
    else:
        if current_user.balance < total_cart_price:
            return render_template(
                'order_submit.html', cart_entries_data=cart_entries_data,
                total_cart_price=total_cart_price, form=form,
                message=f"Недостаточно у.е. на балансе для подтверждения заказа. Баланс: {current_user.balance} у.е.")
        session = db_session.create_session()

        user = session.query(User).filter(User.id == current_user.id).first()
        user.balance -= total_cart_price

        order = OrderEntry()
        order.user_id = current_user.id
        order_description_strings = [
            f"Название: {entry['product_name']}, Количетсво: {entry['count']}, Стоимость: {entry['total_price']} у.е."
            for entry in cart_entries_data
        ]
        order_description_strings.append(f"Общая стоимость: {total_cart_price} у.е.")
        order_description_strings.append(f"Адресс доставки: {form.address.data}")
        order_description_strings.append(f"Комментарий к заказу: {form.comment.data}")

        order.description = "\n".join(order_description_strings)
        session.add(order)

        for cart_entry in session.query(CartEntry).filter(CartEntry.user_id == current_user.id):
            session.delete(cart_entry)

        session.commit()
        return redirect("/to_cart")


@app.route("/order_description/<int:order_id>")
def order_description(order_id):
    if not current_user.is_authenticated:
        return redirect("/register")
    session = db_session.create_session()
    order = session.query(OrderEntry).filter(OrderEntry.id == order_id).first()
    if not order:
        abort(404)
    if order.user_id != current_user.id:
        abort(403)
    order_text = str(order.description).split("\n")
    return render_template('order_description.html', order=order, order_text=order_text)


@app.route("/product/<int:product_id>", methods=['GET', 'POST'])
def product_page(product_id):
    session = db_session.create_session()
    product = session.query(Product).filter(Product.id == product_id).first()
    if not product:
        abort(404)

    category_name = session.query(Category).filter(Category.id == product.category_id).first().name
    seller = session.query(User).filter(User.id == product.user_id).first()
    seller_name = seller.name if seller else "Notfound"
    reviews = session.query(Review).filter(Review.product_id == product_id)
    reviews_users_names = [
        session.query(User).filter(User.id == elem.user_id).first().name
        for elem in reviews
    ]

    is_user_review_exists = False
    if current_user.is_authenticated and reviews.filter(Review.user_id == current_user.id).first():
        is_user_review_exists = True

    is_in_user_cart = False
    if current_user.is_authenticated:
        cart_entry = session.query(CartEntry).filter(
            CartEntry.product_id == product_id,
            CartEntry.user_id == current_user.id).first()
        if cart_entry:
            is_in_user_cart = True

    return render_template('product.html', product=product,
                           category_name=category_name, seller_name=seller_name,
                           user=current_user, reviews=reviews,
                           is_user_review_exists=is_user_review_exists,
                           is_in_user_cart=is_in_user_cart,
                           reviews_users_names=reviews_users_names)


@app.route("/add_product/<int:user_id>", methods=['GET', 'POST'])
def add_product(user_id):
    if current_user.id != user_id:
        return redirect('/')
    if current_user.role_id != 1:
        return redirect('/')

    form = ProductForm()
    if request.method == "GET":
        return render_template('product_add.html', form=form, user=current_user)
    else:
        product = Product()
        product.user_id = user_id
        product.category_id = int(form.category.data)
        product.name = form.name.data
        if isinstance(form.price.data, int) and 0 < form.price.data < 999_999_999:
            product.price = int(form.price.data)
        else:
            return render_template('product_add.html', form=form,
                                   user=current_user, message=form.error_price_message)
        img_path = upload_image(form.profile_img.data)
        if img_path:
            product.profile_img_path = img_path
        if form.long_description.data:
            product.long_description = form.long_description.data
        if form.short_description.data:
            product.short_description = form.short_description.data
        if form.specifications.data:
            product.specifications = form.specifications.data
        if form.promo.data:
            product.promo = form.promo.data

        session = db_session.create_session()
        session.add(product)
        session.commit()

        return redirect(f'/product/{product.id}')


@app.route("/edit_product/<int:product_id>", methods=['GET', 'POST'])
def edit_product(product_id):
    if not current_user.is_authenticated:
        return redirect("/register")

    session = db_session.create_session()
    product = session.query(Product).filter(Product.id == product_id).first()

    if not product:
        abort(404)
    if current_user.id != product.user_id:
        abort(403)

    form = ProductForm()
    if request.method == "GET":
        form.name.data = product.name
        form.price.data = product.price
        form.long_description.data = product.long_description
        form.short_description.data = product.short_description
        form.specifications.data = product.specifications
        form.promo.data = product.promo
        return render_template('product_edit.html', product=product, form=form)
    else:
        if form.name.data:
            product.name = form.name.data
        if isinstance(form.price.data, int) and 0 < form.price.data < 999_999_999:
            product.price = int(form.price.data)
        else:
            return render_template('product_add.html', product=product, form=form,
                                   user=current_user, message=form.error_price_message)
        if not form.delete_img.data:
            img_path = upload_image(form.profile_img.data)
            if img_path:
                product.profile_img_path = img_path
        else:
            product.profile_img_path = r"static\imgs\noimg.jpg"
        if form.long_description.data:
            product.long_description = form.long_description.data
        if form.short_description.data:
            product.short_description = form.short_description.data
        if form.specifications.data:
            product.specifications = form.specifications.data
        if form.promo.data:
            product.promo = form.promo.data
        product.last_edit_time = datetime.now()

        session.add(product)
        session.commit()

        return redirect(f'/product/{product_id}')


@app.route("/delete_product/<int:product_id>", methods=['GET', 'POST'])
def delete_product(product_id):
    if not current_user.is_authenticated:
        return redirect("/register")

    session = db_session.create_session()
    product = session.query(Product).filter(Product.id == product_id).first()

    if not product:
        abort(404)
    if current_user.id != product.user_id:
        abort(403)

    session.delete(product)
    reviews = session.query(Review).filter(Review.product_id == product_id)
    for review in reviews:
        session.delete(review)
    session.commit()

    return redirect('/index')


@app.route("/add_review/<int:product_id>", methods=['GET', 'POST'])
def add_review(product_id):
    if not current_user.is_authenticated:
        return redirect("/register")

    session = db_session.create_session()
    product = session.query(Product).filter(Product.id == product_id).first()

    if not product:
        abort(404)

    form = ReviewForm()
    if request.method == "GET":
        return render_template('review_add.html', product=product, form=form)
    else:
        review = Review()
        review.product_id = product_id
        review.user_id = current_user.id
        img_path = upload_image(form.profile_img.data)
        if img_path:
            review.profile_img_path = img_path
        if form.about.data:
            review.about = form.about.data
        review.score = int(form.score.data)

        session.add(review)
        session.commit()

        return redirect(f'/product/{product_id}')


@app.route("/edit_review/<int:review_id>", methods=['GET', 'POST'])
def edit_review(review_id):
    if not current_user.is_authenticated:
        return redirect("/register")

    session = db_session.create_session()
    review = session.query(Review).filter(Review.id == review_id).first()

    if not review:
        abort(404)
    if current_user.id != review.user_id:
        abort(403)

    form = ReviewForm()
    if request.method == "GET":
        form.score.data = review.score
        form.about.data = review.about
        return render_template('review_edit.html', review=review, form=form)
    else:
        if form.score.data:
            review.score = int(form.score.data)
        if not form.delete_img.data:
            img_path = upload_image(form.profile_img.data)
            if img_path:
                review.profile_img_path = img_path
        else:
            review.profile_img_path = r"static\imgs\noimg.jpg"
        if form.about.data:
            review.about = form.about.data
        review.score = int(form.score.data)

        session.add(review)
        session.commit()

        return redirect(f'/product/{review.product_id}')


@app.route("/delete_review/<int:review_id>", methods=['GET', 'POST'])
def delete_review(review_id):
    if not current_user.is_authenticated:
        return redirect("/register")

    session = db_session.create_session()
    review = session.query(Review).filter(Review.id == review_id).first()

    if not review:
        abort(404)
    if current_user.id != review.user_id:
        abort(403)

    session.delete(review)
    session.commit()

    return redirect(f'/product/{review.product_id}')


def add_temp_data():
    global all_category_names, all_role_names
    session = db_session.create_session()
    all_category_names = ["Все"] + [elem.name for elem in session.query(Category).all()]
    all_role_names = ["Все"] + [elem.role for elem in session.query(Role).all()]


def generate_routes():
    api.add_resource(CartEntryResource, '/api/cart_entries/<int:user_id>/<int:product_id>')
    api.add_resource(CartEntryListResource, '/api/cart_entries')
    api.add_resource(CategoryResource, '/api/categories/<int:category_id>')
    api.add_resource(CategoryListResource, '/api/categories')
    api.add_resource(OrderEntryResource, '/api/order_entries/<int:order_id>')
    api.add_resource(OrderEntryListResource, '/api/order_entries')
    api.add_resource(ProductResource, '/api/products/<int:product_id>')
    api.add_resource(ProductListResource, '/api/products')
    api.add_resource(ReviewResource, '/api/reviews/<int:review_id>')
    api.add_resource(ReviewListResource, '/api/reviews')
    api.add_resource(UserResource, '/api/users/<int:user_id>')
    api.add_resource(UserListResource, '/api/users')


def main():
    db_file = os.path.join(os.path.dirname(__file__), 'db/store.db')
    if not os.path.exists(db_file):
        print(f"Файл базы данных не найден: {db_file}")
    db_session.global_init(db_file)
    app.register_blueprint(login_api.blueprint)
    app.register_blueprint(get_img_api.blueprint)
    app.register_blueprint(send_img_api.blueprint)
    generate_routes()

    # from db.petstore_init_data.init_basic_data import init_basic_data
    # init_basic_data()

    add_temp_data()
    app.run(port=8000, host='127.0.0.1')


if __name__ == '__main__':
    main()
