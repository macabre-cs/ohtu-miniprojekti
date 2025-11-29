// ------------------------------
// Dynamic Author Fields
// ------------------------------

document.addEventListener("DOMContentLoaded", () => {
  const authorContainer = document.getElementById("author-fields");
  const addAuthorBtn = document.getElementById("add-author");

  if (addAuthorBtn && authorContainer) {
    addAuthorBtn.addEventListener("click", () => {
      const row = document.createElement("div");
      row.className = "author-row";
      row.innerHTML = `
        <input id="author" type="text" name="authors" />
        <button type="button" class="remove-author">×</button>
      `;
      authorContainer.appendChild(row);
    });

    authorContainer.addEventListener("click", (e) => {
      if (e.target.classList.contains("remove-author")) {
        const row = e.target.closest(".author-row");
        if (row === authorContainer.firstElementChild) return;
        row.remove();
      }
    });
  }

  // ------------------------------
  // Dynamic Reference Type Fields
  // ------------------------------

  const refTypeSelect = document.getElementById("reference_type");

  function loadTemplate(type, ref_id) {
    fetch(`/load_fields/${type}/${ref_id}`)
      .then((r) => r.text())
      .then((html) => {
        const target = document.getElementById("dynamic-fields");
        if (target) target.innerHTML = html;
        // notify that dynamic fields have been loaded so callers can populate values
        document.dispatchEvent(new CustomEvent('dynamicFieldsLoaded', { detail: { type } }));
      });
  }

  if (refTypeSelect) {
    refTypeSelect.addEventListener("change", () => {
      loadTemplate(refTypeSelect.value, REFERENCE_ID);
    });

    // initial load: if server has already rendered dynamic fields, skip fetching
    const target = document.getElementById("dynamic-fields");
    if (target && target.innerHTML && target.innerHTML.trim()) {
      // notify listeners that dynamic fields are present
      document.dispatchEvent(new CustomEvent('dynamicFieldsLoaded', { detail: { type: refTypeSelect.value } }));
    } else {
      loadTemplate(refTypeSelect.value, REFERENCE_ID);
    }
  }
});
