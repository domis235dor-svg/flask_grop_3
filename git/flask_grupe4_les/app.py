from flask import Flask, render_template, request, flash, redirect, url_for
from progect.models import init_db
from progect.actions_db import *

app = Flask(__name__)
app.secret_key = 'secret_key'

init_db()


@app.route('/', methods=['GET', 'POST'])
@app.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'POST':
        title = request.form.get('title')
        price = request.form.get('price')
        category = request.form.get('category')

        price = float(price)

        if product_exists(title):
            flash(f'Product {title} already exists!', category='error')
        else:
            add_product(title, price, category)
            flash(f'Product {title} was added!', category='success')

        return redirect(url_for('products'))

    all_categories = get_categories()

    choose_category = request.args.get('category', 'all')

    if choose_category == 'all':
        filter_products = get_products()
    else:
        filter_products = get_products_by_category(choose_category)

    return render_template('product.html',
                           products=filter_products,
                           categories=all_categories,
                           choose_category=choose_category)


@app.route('/edit/<name_product>', methods=['GET', 'POST'])
def edit(name_product):
    product = get_product_by_name(name_product)

    if not product:
        flash(f'Product {name_product} not found!', category='error')
        return redirect(url_for('products'))

    if request.method == 'POST':
        price = float(request.form.get('price'))
        category = request.form.get('category')

        edit_product(name_product, price, category)
        flash('Відредаговано!', category='success')
        return redirect(url_for('edit', name_product=name_product))

    return render_template('edit_product.html', product=product)


@app.route('/delete/<name_product>')
def delete(name_product):
    delete_product(name_product)
    flash(f'Product {name_product} was deleted!', category='success')

    return redirect(url_for('products'))

app.run(debug=True)