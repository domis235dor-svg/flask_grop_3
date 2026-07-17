from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

all_products = {}


@app.route('/', methods=['GET', 'POST'])
@app.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'POST':
        title = request.form.get('title')
        price = request.form.get('price')
        category = request.form.get('category')

        if not title or not price or not category:
            flash('Please fill in all fields!')
            return redirect(url_for('products'))

        try:
            price = float(price)
        except ValueError:
            flash('Price must be a number!')
            return redirect(url_for('products'))

        if title in all_products:
            flash(f'Product "{title}" already exists!')
        else:
            all_products[title] = {
                'price': price,
                'category': category
            }
            flash(f'Product "{title}" added successfully!')

        return redirect(url_for('products'))

    return render_template('product.html', products=all_products)


@app.route('/delete/<name_product>')
def delete(name_product):
    if name_product in all_products:
        all_products.pop(name_product)
        flash(f'Product "{name_product}" was deleted!')
    else:
        flash(f'Product "{name_product}" not found!')

    return redirect(url_for('products'))


@app.route('/edit/<name>', methods=['GET', 'POST'])
def edit(name):
    if name not in all_products:
        flash('Product not found!')
        return redirect(url_for('products'))

    if request.method == 'POST':
        price = request.form.get('price')
        category = request.form.get('category')

        if not price or not category:
            flash('Please fill in all fields!')
            return redirect(url_for('edit', name=name))

        try:
            price = float(price)
        except ValueError:
            flash('Price must be a number!')
            return redirect(url_for('edit', name=name))

        all_products[name]['price'] = price
        all_products[name]['category'] = category

        flash('Товар оновлено!')
        return redirect(url_for('products'))

    return render_template(
        'edit.html',
        name=name,
        product=all_products[name]
    )


if __name__ == '__main__':
    app.run(debug=True)