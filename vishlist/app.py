from flask import Flask, render_template, request, redirect, flash

app = Flask(__name__)
app.secret_key = "secret"

gifts = ""


@app.route("/", methods=["GET", "POST"])
def index():
    search_result = ""

    if request.method == "POST":
        gift = request.form.get("gift")

        if gift.strip() == "":
            flash("Порожній подарунок не можна додати!")
        else:
            gifts.append(gift)
            flash("Подарунок додано!")

        return redirect("/")

    user_request = request.args.get("search")

    if user_request:
        if user_request in gifts:
            search_result = "Такий подарунок вже є у списку"
        else:
            search_result = "Такого подарунка ще немає у списку"

    return render_template(
        "index.html",
        gifts=gifts,
        search_result=search_result
    )


app.run(debug=True)