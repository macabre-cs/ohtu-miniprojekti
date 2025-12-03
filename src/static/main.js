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
      });
  }

  if (refTypeSelect) {
    refTypeSelect.addEventListener("change", () => {
      loadTemplate(refTypeSelect.value, REFERENCE_ID);
    });

    // initial load
    loadTemplate(refTypeSelect.value, REFERENCE_ID);
  }

  // ------------------------------
  // Select All Checkbox
  // ------------------------------

  const selectAllCheckbox = document.getElementById("select-all");

  function getReferenceCheckboxes() {
    return Array.from(document.querySelectorAll('input[name="reference_ids"]'));
  }

  if (selectAllCheckbox) {
    selectAllCheckbox.addEventListener("change", () => {
      const checked = selectAllCheckbox.checked;
      getReferenceCheckboxes().forEach((cb) => (cb.checked = checked));
    });

    document.addEventListener("change", (e) => {
      if (e.target && e.target.name === "reference_ids") {
        const boxes = getReferenceCheckboxes();
        if (boxes.length === 0) {
          selectAllCheckbox.checked = false;
          selectAllCheckbox.indeterminate = false;
          return;
        }
        const allChecked = boxes.every((b) => b.checked);
        selectAllCheckbox.checked = allChecked;
        selectAllCheckbox.indeterminate = false;
      }
    });
  }
});
