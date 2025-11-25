def generate_bibtex(references):
    entries = []

    for ref in references:
        entries.append(format_into_bibtex(ref))

    return "\n\n".join(entries)



def format_into_bibtex(reference):
    ref_type = reference.reference_type
    cite_key = reference.cite_key

    lines = [f"@{ref_type}{{{cite_key},"]

    authors = reference.author.split(";")
    formatted_authors = []

    # muuttaa authorit bibtex formaattiin
    for author in authors:
        if "," in author:
            lastname, firstname = author.split(",")
            formatted_authors.append(f"{firstname.strip()} {lastname.strip()}")
        else:
            formatted_authors.append(author)

    reference.author = " and ".join(formatted_authors)

    for key, value in reference:
        if key not in ["reference_type", "cite_key", "id"] and value:
            lines.append(f"  {key} = {{{value}}},")

    # Tämä poistaa pilkun viimeiseltä riviltä. Saa parantaa.
    lines[-1] = lines[-1][:-1]

    lines.append("}")

    return "\n".join(lines)
