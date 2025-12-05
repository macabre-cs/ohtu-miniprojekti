from datetime import datetime
from flask import redirect, render_template, request, jsonify, flash, Response
from db_helper import reset_db
from repositories.reference_repository import (
    get_references,
    get_reference,
    create_reference,
    delete_reference,
    edit_reference,
    search_references_by_query,
)
from config import app, test_env
from util import validate_reference, validate_cite_key
from entities.reference import Reference
from bibtex_generator import generate_bibtex


def format_authors(authors):
    cleaned = [a.strip() for a in authors if a.strip()]
    return "; ".join(cleaned)


@app.route("/")
def index():
    references = get_references()
    return render_template("index.html", references=references)


@app.route("/new_reference")
def new():
    return render_template("new_reference.html", curr_year=datetime.now().year)


@app.route("/load_fields/<ref_type>/<ref_id>", methods=["GET"])
def load_fields(ref_type, ref_id):
    reference = get_reference(ref_id) if ref_id != "none" else None
    templates = {
        "book": "new_book.html",
        "article": "new_article.html",
        "inproceedings": "new_inproceedings.html",
        "misc": "new_misc.html",
    }
    if ref_type not in templates:
        return "Invalid reference type", 400

    return render_template(templates[ref_type], reference=reference)


@app.route("/create_reference", methods=["POST"])
def reference_creation():
    authors_raw = request.form.getlist("authors")
    form_data = request.form.to_dict()
    formatted = format_authors(authors_raw)
    form_data["author"] = formatted
    form_data["authors"] = authors_raw

    def render_form():
        return render_template(
            "new_reference.html",
            curr_year=datetime.now().year,
            **form_data,
        )

    try:
        validate_cite_key(form_data.get("cite_key"))
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

    authors_raw = request.form.getlist("authors")
    form_data = request.form.to_dict()
    formatted = format_authors(authors_raw)
    form_data["author"] = formatted

    def render_edit(data):
        return render_template(
            "edit_reference.html",
            reference=Reference({**data, "id": ref_id}),
            curr_year=datetime.now().year,
        )

    try:
        validate_cite_key(form_data.get("cite_key"), exclude_id=ref_id)
        validate_reference(form_data)
        updated_reference = Reference(form_data)
        edit_reference(ref_id, updated_reference)
        return redirect(f"/reference/{ref_id}")
    except Exception as error:
        flash(str(error))
        return render_edit(form_data)


@app.route("/search_references")
def search_references_route():
    query = request.args.get("query")
    if query:
        results = search_references_by_query(query)

    else:
        query = ""
        results = []

    return render_template("search_references.html", query=query, results=results)


@app.route("/export_bibtex", methods=["POST"])
def export_bibtex():
    reference_ids = request.form.getlist("reference_ids")
    from_search = request.form.get("from_search") == "true"
    query = request.form.get("query", "")

    if not reference_ids:
        flash("No references selected")
        if from_search:
            return redirect(f"/search_references?query={query}")
        return redirect("/")

    references = [get_reference(ref_id) for ref_id in reference_ids]

    bibtex = generate_bibtex(references)

    return Response(
        bibtex,
        mimetype="text/plain",
        headers={"Content-Disposition": "attachment;filename=references.bib"},
    )


# testausta varten oleva reitti
if test_env:

    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({"message": "db reset"})
