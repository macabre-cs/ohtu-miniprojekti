from datetime import datetime
from flask import redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from repositories.reference_repository import get_references, create_reference
from config import app, test_env
from util import validate_reference
from entities.reference import Reference

@app.route("/")
def index():
    references = get_references()
    return render_template("index.html", references=references)

@app.route("/new_reference")
def new():
    return render_template("new_reference.html", curr_year=datetime.now().year)

@app.route("/create_reference", methods=["POST"])
def reference_creation():
    title = request.form.get("title")
    cite_key = request.form.get("cite_key")
    year = request.form.get("year")
    publisher = request.form.get("publisher")
    author = request.form.get("authors_formatted")

    try:
        validate_reference(cite_key, title, author, year, publisher)
        reference = Reference({
            "cite_key": cite_key,
            "title": title,
            "author": author,
            "year": year,
            "publisher": publisher
        })
        create_reference(reference)
        return redirect("/")
    except Exception as error:
        flash(str(error))
        return redirect("/new_reference")

# testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })
