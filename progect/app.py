from werkzeug import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from actions_db import *
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'codeshare_secret'

UPLOAD_FOLDER = 'static/image/posts'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)


@app.route('/')
def index():
    posts = get_all_posts()
    return render_template('index.html', posts=posts)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if get_user_by_email(email):
            flash('Email already exists')
            return redirect(url_for('register'))

        create_user(username, email, password)
        flash('Registration successful')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = get_user_by_email(email)

        if user and user.password == password:
            login_user(user)
            flash('Logged in')
            return redirect(url_for('index'))

        flash('Invalid email or password')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out')
    return redirect(url_for('index'))


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_post_page():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        code = request.form['code']

        print(request.files)

        image_file = request.files.get('image')
        image_name = None

        if image_file and image_file.filename != "":
            filename = secure_filename(image_file.filename)

            image_path = os.path.join(
                app.root_path,
                'static',
                'image',
                'posts',
                filename
            )

            image_file.save(image_path)

            print("Saved:", image_path)

            image_name = filename

        create_post(
            title=title,
            description=description,
            code=code,
            image=image_name,
            user=current_user
        )

        flash("Project published")
        return redirect(url_for("index"))

    return render_template("create_post.html")

    return render_template('create_post.html')


@app.route('/my-posts')
@login_required
def my_posts():
    posts = get_user_posts(current_user)
    return render_template('my_posts.html', posts=posts)


@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = get_post(post_id)

    if not post or post.user.id != current_user.id:
        return redirect(url_for('index'))

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        code = request.form['code']

        image_file = request.files.get('image')
        image_name = post.image

        if image_file and image_file.filename != "":
            filename = secure_filename(image_file.filename)

            image_path = os.path.join(
                app.root_path,
                'static',
                'image',
                'posts',
                filename
            )

            image_file.save(image_path)
            image_name = filename

        update_post(
            post=post,
            title=title,
            description=description,
            code=code,
            image=image_name
        )

        flash('Post updated')
        return redirect(url_for('my_posts'))

    return render_template('edit_post.html', post=post)


@app.route('/delete/<int:post_id>')
@login_required
def delete_post_page(post_id):
    post = get_post(post_id)

    if post and post.user.id == current_user.id:
        delete_post(post)
        flash('Post deleted')

    return redirect(url_for('my_posts'))

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)


@app.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        username = request.form['username']
        bio = request.form['bio']

        current_user.username = username
        current_user.bio = bio

        avatar_file = request.files.get('avatar')

        if avatar_file and avatar_file.filename:
            filename = secure_filename(avatar_file.filename)
            avatar_path = os.path.join(
                app.root_path,
                'static',
                'image',
                'avatars',
                filename
            )

            avatar_file.save(avatar_path)
            current_user.avatar = filename

        current_user.save()

        flash('Profile updated')
        return redirect(url_for('profile'))

    return render_template('edit_profile.html')

@app.route('/comment/<int:post_id>', methods=['POST'])
@login_required
def add_comment(post_id):
    post = get_post(post_id)

    if post:
        text = request.form['text']

        if text.strip():
            create_comment(text, current_user, post)

    return redirect(url_for('index'))
@app.route('/delete-comment/<int:comment_id>')
@login_required
def delete_comment_page(comment_id):
    comment = get_comment(comment_id)

    if comment:
        is_comment_owner = comment.user.id == current_user.id
        is_post_owner = comment.post.user.id == current_user.id

        if is_comment_owner or is_post_owner:
            delete_comment(comment)
            flash('Comment deleted')

    return redirect(url_for('index'))






if __name__ == '__main__':
    app.run(debug=True)