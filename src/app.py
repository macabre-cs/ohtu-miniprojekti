from datetime import datetime
from flask import redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from repositories.reference_repository import (
    get_references,
    get_reference,
    create_reference,
    delete_reference,
    edit_reference,
    get_reference_by_cite_key,
)
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
    form_data = request.form.to_dict()

    def render_form():
        return render_template(
            "new_reference.html",
            curr_year=datetime.now().year,
            **form_data,
        )

    try:
        validate_reference(form_data)
        reference = Reference(form_data)
        create_reference(reference)
    except Exception as error:
        flash(str(error))
        return render_form()

    return redirect("/")




@app.route("/reference/<ref_id>")
def show_reference(ref_id):
    reference = get_reference(ref_id)
    return render_template("show_reference.html", reference=reference)


@app.route("/reference/<ref_id>/delete", methods=["GET", "POST"])
def delete_reference_route(ref_id):
    reference = get_reference(ref_id)
    if not reference:
        return redirect("/")

    if request.method == "GET":
        return render_template("delete_reference.html", reference=reference)

    if request.method == "POST":
        if "delete" in request.form:
            delete_reference(ref_id)
            return redirect("/")

    return redirect("/reference/" + ref_id)


@app.route("/reference/<ref_id>/edit", methods=["GET", "POST"])
def edit_reference_route(ref_id):
    reference = get_reference(ref_id)
    if not reference:
        return redirect("/")

    if request.method == "GET":
        return render_template(
            "edit_reference.html",
            reference=reference,
            curr_year=datetime.now().year,
        )

    if "cancel" in request.form:
        return redirect("/")

    form_data = request.form.to_dict()

    def render_edit(data):
        return render_template(
            "edit_reference.html",
            reference=Reference({**data, "id": ref_id}),
            curr_year=datetime.now().year,
        )

    existing = get_reference_by_cite_key(form_data["cite_key"])
    if existing and str(existing.id) != str(ref_id):
        flash("Cite key already exists")
        return render_edit(form_data)

    try:
        validate_reference(form_data)
        updated_reference = Reference(form_data)
        edit_reference(ref_id, updated_reference)
        return redirect(f"/reference/{ref_id}")
    except Exception as error:
        flash(str(error))
        return render_edit(form_data)


# testausta varten oleva reitti
if test_env:

    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({"message": "db reset"})
