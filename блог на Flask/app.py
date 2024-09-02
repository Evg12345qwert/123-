from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Пример списка постов с комментариями
posts = [
    {"id": 1, "title": "Первый пост", "content": "Содержимое первого поста", "comments": []},
    {"id": 2, "title": "Второй пост", "content": "Содержимое второго поста", "comments": []},
]

@app.route("/")
def index():
    return render_template("index.html", posts=posts)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/post/<int:post_id>")
def post(post_id):
    post = next((p for p in posts if p["id"] == post_id), None)
    return render_template("post.html", post=post)

@app.route("/create", methods=["GET", "POST"])
def create_post():
    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        new_post = {"id": len(posts) + 1, "title": title, "content": content, "comments": []}
        posts.append(new_post)
        return redirect(url_for("index"))
    return render_template("create_post.html")

@app.route("/edit/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post = next((p for p in posts if p["id"] == post_id), None)
    if request.method == "POST":
        post["title"] = request.form['title']
        post["content"] = request.form['content']
        return redirect(url_for("index"))
    return render_template("edit_post.html", post=post)

@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    global posts
    posts = [p for p in posts if p["id"] != post_id]
    return redirect(url_for("index"))

# Комментарии
@app.route("/post/<int:post_id>/comment", methods=["POST"])
def add_comment(post_id):
    post = next((p for p in posts if p["id"] == post_id), None)
    if post:
        comment_content = request.form['comment']
        post["comments"].append(comment_content)
    return redirect(url_for("post", post_id=post_id))

@app.route("/post/<int:post_id>/delete_comment/<int:comment_id>")
def delete_comment(post_id, comment_id):
    post = next((p for p in posts if p["id"] == post_id), None)
    if post:
        post["comments"].pop(comment_id)  # Удаляем комментарий по индексу
    return redirect(url_for("post", post_id=post_id))

if __name__ == "__main__":
    app.run(debug=True)