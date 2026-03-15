/**
 * This JavaScript file handles the dynamic functionality of the workout logging page, allowing users to add exercises and sets on the fly without needing to reload the page.
 * It listens for clicks on the exercise selection modal to add new exercise cards, and also manages adding/removing sets within each exercise card.
 * The code ensures that bodyweight exercises have their weight input pre-filled and disabled, while allowing users to freely input weights for other exercises.
 */
document.addEventListener("DOMContentLoaded", function () {
  const exerciseCards = document.getElementById("exercise-cards");

  // --- Add Exercise Card from Modal ---
  const exerciseList = document.getElementById("exercise-list");
  if (exerciseList) {
    exerciseList.addEventListener("click", function (e) {
      const btn = e.target.closest("button");
      if (!btn) return;

      const id = btn.dataset.id;
      const name = btn.dataset.name;
      const isBw = btn.dataset.isBw === "true";

      // Create Exercise Card
      const card = document.createElement("div");
      card.className =
        "card border-0 shadow-sm rounded-4 p-4 mb-4 exercise-card";
      card.innerHTML = `
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <h5 class="fw-bold mb-0 text-primary">${name}</h5>
                    <button type="button" class="btn btn-sm btn-outline-danger border-0 remove-exercise"><i class="fas fa-times"></i></button>
                </div>
                <div class="sets-container" id="sets-for-${id}">
                    <!-- Set rows go here -->
                </div>
                <button type="button" class="btn btn-sm btn-link text-decoration-none mt-2 add-set" data-id="${id}" data-is-bw="${isBw}">
                    <i class="fas fa-plus-circle me-1"></i> Add Set
                </button>
            `;
      exerciseCards.appendChild(card);

      // Add initial set
      addSetRow(id, isBw);

      const modalElement = document.getElementById("addExerciseModal");
      if (modalElement) {
        bootstrap.Modal.getInstance(modalElement).hide();
      }
    });
  }

  // --- Helper: Update Set Numbers ---
  function updateSetNumbers(container) {
    // Find all set rows within this specific exercise container
    const setRows = container.querySelectorAll(".set-row");
    // Loop through them and update their text label based on their new index
    setRows.forEach((row, index) => {
      const label = row.querySelector(".set-number-label");
      if (label) {
        label.textContent = `#${index + 1}`;
      }
    });
  }

  // --- add Set Row ---
  function addSetRow(exerciseId, isBw) {
    const container = document.getElementById(`sets-for-${exerciseId}`);
    const setCount = container.children.length + 1;
    const weightValue = isBw ? "0" : "";
    const weightDisabled = isBw ? "readonly" : "";

    // Added the 'set-number-label' class to the div containing the #number so we can easily target it later
    const row = `
                <div class="row g-2 mb-2 set-row align-items-center">
                    <div class="col-1 text-muted small fw-bold set-number-label">#${setCount}</div>
                    <div class="col-5">
                        <input type="number" name="weight_${exerciseId}[]" class="form-control form-control-sm border-0 bg-light rounded-pill px-3"
                            value="${weightValue}" ${weightDisabled} placeholder="Weight" step="0.5" min="0" required>
                    </div>
                    <div class="col-4">
                        <input type="number" name="reps_${exerciseId}[]" class="form-control form-control-sm border-0 bg-light rounded-pill px-3"
                            placeholder="Reps" min="1" required>
                    </div>
                    <div class="col-2 text-end">
                        <button type="button" class="btn btn-sm text-danger remove-set"><i class="fas fa-minus-circle"></i></button>
                    </div>
                    <input type="hidden" name="exercise_id_order[]" value="${exerciseId}">
                </div>
            `;
    container.insertAdjacentHTML("beforeend", row);
  }

  // --- Handle Clicks in Exercise Card ---
  if (exerciseCards) {
    exerciseCards.addEventListener("click", function (e) {
      // Add Set
      if (e.target.closest(".add-set")) {
        const btn = e.target.closest(".add-set");
        addSetRow(btn.dataset.id, btn.dataset.isBw === "true");
      }

      // Remove Set
      if (e.target.closest(".remove-set")) {
        const setRow = e.target.closest(".set-row");
        const container = setRow.closest(".sets-container");

        // Check how many sets are left before removing
        const remainingSets = container.querySelectorAll(".set-row").length;

        if (remainingSets > 1) {
          setRow.remove();
          updateSetNumbers(container);
        } else {
          alert(
            "An exercise must have at least one set. If you didn't do this exercise, remove the entire card using the 'X' button at the top.",
          );
        }
      }

      // Remove Exercise Card
      if (e.target.closest(".remove-exercise")) {
        e.target.closest(".exercise-card").remove();
      }
    });
  }
});
