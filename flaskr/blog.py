from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort
import markdown
import os
from werkzeug.utils import secure_filename
from flask_babel import _

from .auth import login_required
from .db import get_db

bp = Blueprint("blog", __name__)

POSTS_PER_PAGE = 10
UPLOAD_FOLDER = 'flaskr/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route("/")
def index():
    """Show all the posts, most recent first."""
    page = request.args.get('page', 1, type=int)
    db = get_db()
    posts = db.execute(
        "SELECT p.id, title, body, image, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC"
        " LIMIT ? OFFSET ?",
        (POSTS_PER_PAGE, (page - 1) * POSTS_PER_PAGE)
    ).fetchall()
    # Convert the immutable cursor to a list of dictionaries
    posts = [dict(post) for post in posts]
    # Convert markdown to HTML for each post body
    for post in posts:
        post['body'] = markdown.markdown(post['body'])

    # Get the total number of posts to calculate pagination
    total_posts = db.execute("SELECT COUNT(id) FROM post").fetchone()[0]
    total_pages = (total_posts + POSTS_PER_PAGE - 1) // POSTS_PER_PAGE

    return render_template("blog/index.html", posts=posts, page=page, total_pages=total_pages)


def get_post(id, check_author=True):
    """Get a post and its author by id.

    Checks that the id exists and optionally that the current user is
    the author.

    :param id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    post = (
        get_db()
        .execute(
            "SELECT p.id, title, body, image, created, author_id, username"
            " FROM post p JOIN user u ON p.author_id = u.id"
            " WHERE p.id = ?",
            (id,),
        )
        .fetchone()
    )

    if post is None:
        abort(404, _("Post id {id} doesn't exist.").format(id=id))

    if check_author and post["author_id"] != g.user["id"]:
        abort(403)

    return post


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    """Create a new post for the current user."""
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        image = request.files.get("image")
        error = None

        if not title:
            error = _("Title is required.")

        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(UPLOAD_FOLDER, filename))
        else:
            filename = None

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO post (title, body, image, author_id) VALUES (?, ?, ?, ?)",
                (title, body, filename, g.user["id"]),
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/create.html")


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    """Update a post if the current user is the author."""
    post = get_post(id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        image = request.files.get("image")
        error = None

        if not title:
            error = _("Title is required.")

        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(UPLOAD_FOLDER, filename))
        else:
            filename = post['image']

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE post SET title = ?, body = ?, image = ? WHERE id = ?", (title, body, filename, id)
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/update.html", post=post)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    get_post(id)
    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("blog.index"))
