from flask import Blueprint, redirect, request, render_template, session, url_for
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash
from .utils import save_uploaded_image, delete_image_by_filename
from .models import Admin, Property, db

user = Blueprint('user', __name__)
admin = Blueprint('admin', __name__)

@user.route('/')
def home():
    listings = Property.query.all()
    return render_template('home.html', listings=listings)

@user.route('/view-listing', methods=['POST','GET'])
def view_listing():
    if request.method == 'POST':
        listing_id = request.form['listing_id']
        listing = Property.query.filter_by(id=listing_id).first()
        return render_template('view_listing.html',listing=listing)

@admin.route('/admin-login', methods=['POST','GET'])
def login():
    if request.method == "POST":
        email = (request.form['email']).lower()
        password = request.form['password']
        check_admin = Admin.query.filter_by(email=email).first()
        if check_admin and check_password_hash(check_admin.password, password):
            session['admin_access'] = check_admin.id
            return redirect(url_for('admin.admin_control'))
    message = session.pop('message', None)
    return render_template('login.html', message=message)

@admin.route('/admin-register', methods=['POST','GET'])
def register():
    if request.method == "POST":
        email = (request.form['email']).lower()
        password = request.form['password']
        try:
            admin = Admin(email=email, password=generate_password_hash(password))
            db.session.add(admin)
            db.session.commit()
            session['message'] = "Account created successfully"
            return redirect(url_for('admin.login'))
        except IntegrityError:
            db.session.rollback()
            return "Error registering admin"
    return render_template('register.html')

@admin.route('/admin-control', methods=['POST','GET'])
def admin_control():
    if 'admin_access' in session:
        if 'listing' in session:
            session.pop('listing', None)
        if request.method == 'POST':
            button_clicked = request.form['button']
            if button_clicked == 'create_listing':
                return redirect(url_for('admin.create_listing'))
        properties = Property.query.all()
        message = session.pop('message', None)
        return render_template('admin_control.html',
                               properties=properties,
                               message=message)
    return redirect(url_for('admin.login'))

@admin.route('/create-listing', methods=['POST','GET'])
def create_listing():
    if 'admin_access' in session:
        admin_id = session.get('admin_access')
        if request.method == 'POST':
            title = (request.form['title']).upper()
            bedrooms = request.form['bedrooms']
            bathrooms = request.form['bathrooms']
            description = request.form['description']
            price = request.form['price']
            address = request.form['address']
            url_link = request.form.get('url_link')

            listing = Property(title=title,
                               bedrooms=bedrooms,
                               bathrooms=bathrooms,
                               description=description,
                               price=price,
                               address=address,
                               url_link=url_link,
                               admin_id=admin_id)

            db.session.add(listing)
            db.session.commit()
            session['message'] = f"Listing created: {title}"
            return redirect(url_for('admin.admin_control'))
        return render_template('create_listing.html')
    return redirect(url_for('admin.login'))

@admin.route('/edit-listing', methods=['POST','GET'])
def edit_listing():
    if 'admin_access' in session:
        if 'listing' not in session:
            listing_id = int(request.form.get('listing_id'))
            listing = Property.query.filter_by(id=listing_id).first()
            session['listing'] = listing_id
        else:
            listing_id = session.get('listing', None)
            listing = Property.query.filter_by(id=listing_id).first()
        if request.method == "POST":
            button_clicked = request.form.get('button')

            if button_clicked == 'update_listing':
                title = request.form.get('title')
                bedrooms = request.form.get('bedrooms')
                bathrooms = request.form.get('bathrooms')
                description = request.form.get('description')
                price = request.form.get('price')
                address = request.form.get('address')
                url_link = request.form.get('url_link')
                listing.title = title
                listing.bedrooms = bedrooms
                listing.bathrooms = bathrooms
                listing.description = description
                listing.price = price
                listing.address = address
                listing.url_link = url_link
                db.session.commit()
                session['message'] = f"Listing updated"
                return redirect(url_for('admin.edit_listing'))

            if button_clicked == 'upload_thumbnail':
                saved_filename = ''
                if 'image' in request.files:
                    uploaded_file = request.files['image']
                    filename = str(listing.id) + "-" + request.form.get('filename', None) + ".jpg"

                    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}

                    saved_filename = save_uploaded_image(uploaded_file,
                                                         upload_folder='website/static/property_images',
                                                         allowed_extensions=allowed_extensions,
                                                         filename=filename)

                if saved_filename:
                    listing.thumbnail = saved_filename
                    db.session.commit()
                    return redirect(url_for('admin.edit_listing'))
                session['message'] = "Error uploading thumbnail"

            if button_clicked == 'delete_thumbnail':
                filename = listing.thumbnail
                listing.thumbnail = ''
                db.session.commit()
                if filename:
                    upload_folder = 'website/static/property_images'
                    deleted = delete_image_by_filename(filename, upload_folder)
                    if deleted:
                        session['message'] = "Thumbnail deleted"
                        return redirect(url_for('admin.edit_listing'))
                    else:
                        session['message'] = "Failed to delete thumbnail"
                        return redirect(url_for('admin.edit_listing'))
                else:
                    session['message'] = "No thumbnail image to delete"
                    return redirect(url_for('admin.edit_listing'))


            if button_clicked == 'upload_image-2':
                saved_filename = ''
                if 'image' in request.files:
                    uploaded_file = request.files['image']
                    filename = str(listing.id) + "-" + request.form.get('filename', None) + ".jpg"

                    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}

                    saved_filename = save_uploaded_image(uploaded_file,
                                                         upload_folder='website/static/property_images',
                                                         allowed_extensions=allowed_extensions,
                                                         filename=filename)

                if saved_filename:
                    listing.image2 = saved_filename
                    db.session.commit()
                    return redirect(url_for('admin.edit_listing'))
                session['message'] = "Error uploading Image-2"

            if button_clicked == 'delete_image-2':
                filename = listing.image2
                listing.image2 = ''
                db.session.commit()
                if filename:
                    upload_folder = 'website/static/property_images'
                    deleted = delete_image_by_filename(filename, upload_folder)
                    if deleted:
                        session['message'] = "Image-2 deleted"
                        return redirect(url_for('admin.edit_listing'))
                    else:
                        session['message'] = "Failed to delete Image-2"
                        return redirect(url_for('admin.edit_listing'))
                else:
                    session['message'] = "No image-2 to delete"
                    return redirect(url_for('admin.edit_listing'))

            if button_clicked == 'upload_image-3':
                saved_filename = ''
                if 'image' in request.files:
                    uploaded_file = request.files['image']
                    filename = str(listing.id) + "-" + request.form.get('filename', None) + ".jpg"

                    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}

                    saved_filename = save_uploaded_image(uploaded_file,
                                                         upload_folder='website/static/property_images',
                                                         allowed_extensions=allowed_extensions,
                                                         filename=filename)

                if saved_filename:
                    listing.image3 = saved_filename
                    db.session.commit()
                    return redirect(url_for('admin.edit_listing'))
                session['message'] = "Error uploading Image-3"

            if button_clicked == 'delete_image-3':
                filename = listing.image3
                listing.image3 = ''
                db.session.commit()
                if filename:
                    upload_folder = 'website/static/property_images'
                    deleted = delete_image_by_filename(filename, upload_folder)
                    if deleted:
                        session['message'] = "Image-3 deleted"
                        return redirect(url_for('admin.edit_listing'))
                    else:
                        session['message'] = "Failed to delete Image-3"
                        return redirect(url_for('admin.edit_listing'))
                else:
                    session['message'] = "No image-3 to delete"
                    return redirect(url_for('admin.edit_listing'))

        message = session.pop('message', None)
        return render_template('edit_listing.html', listing=listing, message=message)
    return redirect(url_for('admin.login'))


@admin.route('/delete-listing', methods=['POST','GET'])
def delete_listing():
    if 'admin_access' in session:
        if request.method == 'POST':
            listing_id = request.form['listing_id']
            listing = Property.query.filter_by(id=listing_id).first()
            upload_folder = 'website/static/property_images'
            thumbnail_filename = listing.thumbnail
            if thumbnail_filename:
                deleted = delete_image_by_filename(thumbnail_filename, upload_folder)
            image2_filename = listing.image2
            if image2_filename:
                deleted = delete_image_by_filename(image2_filename, upload_folder)
            image3_filename = listing.image3
            if image3_filename:
                deleted = delete_image_by_filename(image3_filename, upload_folder)
            db.session.delete(listing)
            db.session.commit()
            return redirect(url_for('admin.admin_control'))
        return redirect(url_for('admin.admin_control'))
    return redirect(url_for('admin.login'))
