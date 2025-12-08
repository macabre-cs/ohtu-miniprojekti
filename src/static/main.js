// -------------------------------
// Info Icon Tooltip Component
// -------------------------------
class InfoTooltip extends HTMLElement {
    connectedCallback() {
        const info = this.getAttribute("info");
        this.innerHTML = `
            <span class="info-container">
                <span class="info-icon">i</span>
                <span class="tooltip">${info}</span>
            </span>
        `;
    }
}
customElements.define("info-tooltip", InfoTooltip);
// ------------------------------



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

  if (refTypeSelect && typeof REFERENCE_ID !== 'undefined') {
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

  // ------------------------------
  // Smooth Scroll to Results
  // ------------------------------

  if (window.location.hash === '#results') {
    setTimeout(() => {
      document.getElementById('results')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
  }

  // ------------------------------
  // Bouncing Cat
  // ------------------------------

  document.getElementById('bounce-cat').onclick = function() {
    const catContainer = document.getElementById('cat-container');
    catContainer.style.display = 'block';
    setTimeout(() => {
      catContainer.style.display = 'none';
    }, 3000); // Hide after 3 seconds
  };
});

// ------------------------------
// Tag Management Functions
// ------------------------------

async function addTag(referenceId) {
  const input = document.getElementById(`tag-input-${referenceId}`);
  const tagName = input.value.trim();
  
  if (!tagName) {
    return;
  }

  try {
    const response = await fetch(`/reference/${referenceId}/tag`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ tag_name: tagName })
    });

    if (response.ok) {
      const data = await response.json();
      
      // Add the new tag to the display
      const tagsDisplay = input.closest('.tags-section').querySelector('.tags-display');
      const tagBadge = document.createElement('span');
      tagBadge.className = 'tag-badge';
      tagBadge.setAttribute('data-tag-id', data.tag_id);
      tagBadge.setAttribute('data-reference-id', referenceId);
      tagBadge.innerHTML = `
        ${tagName}
        <button type="button" class="tag-remove" onclick="removeTag(${referenceId}, ${data.tag_id})">&times;</button>
      `;
      tagsDisplay.appendChild(tagBadge);
      
      // Clear input
      input.value = '';
    } else {
      const error = await response.json();
      alert(error.error || 'Failed to add tag');
    }
  } catch (error) {
    console.error('Error adding tag:', error);
    alert('Failed to add tag');
  }
}

async function removeTag(referenceId, tagId) {
  if (!confirm('Remove this tag?')) {
    return;
  }

  try {
    const response = await fetch(`/reference/${referenceId}/tag/${tagId}`, {
      method: 'DELETE'
    });

    if (response.ok) {
      // Remove the tag badge from the display
      const tagBadge = document.querySelector(`[data-tag-id="${tagId}"][data-reference-id="${referenceId}"]`);
      if (tagBadge) {
        tagBadge.remove();
      }
    } else {
      const error = await response.json();
      alert(error.error || 'Failed to remove tag');
    }
  } catch (error) {
    console.error('Error removing tag:', error);
    alert('Failed to remove tag');
  }
}
