from models import User, CodePost, Comment


def create_user(username, email, password):
    return User.create(
        username=username,
        email=email,
        password=password
    )


def get_user_by_email(email):
    return User.get_or_none(User.email == email)


def get_user_by_id(user_id):
    return User.get_or_none(User.id == user_id)


def create_post(title, description, code, image, user):
    return CodePost.create(
        title=title,
        description=description,
        code=code,
        image=image,
        user=user
    )


def get_all_posts():
    return CodePost.select().order_by(CodePost.created_at.desc())


def get_user_posts(user):
    return CodePost.select().where(CodePost.user == user).order_by(CodePost.created_at.desc())


def get_post(post_id):
    return CodePost.get_or_none(CodePost.id == post_id)


def update_post(post, title, description, code, image):
    post.title = title
    post.description = description
    post.code = code
    post.image = image
    post.save()


def delete_post(post):
    post.delete_instance()


def create_comment(text, user, post):
    return Comment.create(
        text=text,
        user=user,
        post=post
    )
def delete_comment(comment):
    comment.delete_instance()


def get_comment(comment_id):
    return Comment.get_or_none(Comment.id == comment_id)


def get_post_comments(post):
    return Comment.select().where(Comment.post == post).order_by(Comment.created_at.desc())