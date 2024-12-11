from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import Product
from app.forms import ProductForm
import os

main = Blueprint('main', __name__)

def calculate_cart_total(cart):
    return sum(item['price'] * item['quantity'] for item in cart)

@main.route('/')
def home():
    products = Product.query.all()
    cart = session.get('cart', [])
    cart_total = calculate_cart_total(cart)
    return render_template('home.html', products=products, cart=cart, cart_total=cart_total)

@main.route('/cart')
def cart():
    cart = session.get('cart', [])
    products = Product.query.all()
    cart_total = calculate_cart_total(cart)
    return render_template('cart.html', cart=cart, products=products, cart_total=cart_total)

@main.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    cart = session.get('cart', [])
    
    for item in cart:
        if item['id'] == product_id:
            item['quantity'] += 1
            break
    else:
        cart.append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'quantity': 1
        })
    
    session['cart'] = cart
    flash(f'{product.name} added to cart!', 'success')
    return redirect(url_for('main.home'))

@main.route('/update_cart_quantity/<int:product_id>', methods=['POST'])
def update_cart_quantity(product_id):
    cart = session.get('cart', [])
    quantity = int(request.form.get('quantity', 1))
    
    for item in cart:
        if item['id'] == product_id:
            if quantity > 0:
                item['quantity'] = quantity
            else:
                cart.remove(item)
            break
    
    session['cart'] = cart
    return redirect(url_for('main.cart'))

@main.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != product_id]
    session['cart'] = cart
    return redirect(url_for('main.cart'))

@main.route('/admin/dashboard')
def admin_dashboard():
    products = Product.query.all()
    return render_template('admin_dashboard.html', products=products)

@main.route('/admin/add_product', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            available=form.available.data
        )
        db.session.add(product)
        db.session.commit()

        if form.image.data:
            product.save_image(form.image.data)
            db.session.commit()

        flash('Product added successfully!', 'success')
        return redirect(url_for('main.admin_dashboard'))
    
    return render_template('add_edit_item.html', form=form, title='Add Product')

@main.route('/admin/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    
    if form.validate_on_submit():
        form.populate_obj(product)
        
        if form.image.data:
            product.save_image(form.image.data)
        
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('main.admin_dashboard'))
    
    return render_template('add_edit_item.html', form=form, product=product, title='Edit Product')

@main.route('/admin/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    if product.image_filename:
        image_path = os.path.join('app', 'static', 'uploads', product.image_filename)
        if os.path.exists(image_path):
            os.remove(image_path)
    
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('main.admin_dashboard'))
