from flask import (
    Blueprint,
    render_template
)

from models import (
    Category
)


categories = Blueprint(
    "categories",
    __name__
)


@categories.route("/category/<int:category_id>")
def view_category(category_id):

    category = Category.query.get_or_404(
        category_id
    )

    posts = (
        category.posts
    )

    return render_template(
        "category.html",
        category=category,
        posts=posts
    )