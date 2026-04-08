document.addEventListener("DOMContentLoaded", function () {
  const exerciseCards = document.getElementById("exercise-cards");

  let lastFocusedElement = null;

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
      card.className = "card border-0 shadow-sm rounded-4 p-4 mb-4 exercise-card";
      card.innerHTML = `
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <a href="javascript:void(0);" class="h5 fw-bold mb-0 text-brand-primary text-decoration-none view-exercise-detail" data-id="${id}" data-name="${name}">
                        ${name} <i class="fas fa-external-link-alt small opacity-50 ms-1"></i>
                    </a>
                    <button type="button" class="btn btn-sm btn-outline-danger border-0 remove-exercise"><i class="fas fa-times"></i></button>
                </div>
                <div class="sets-container" id="sets-for-${id}">
                    <!-- Set rows go here -->
                </div>
                <button type="button" class="btn btn-sm btn-link text-brand-primary text-decoration-none mt-2 add-set" data-id="${id}" data-is-bw="${isBw}">
                    <i class="fas fa-plus-circle me-1"></i> Add Set
                </button>
            `;
      exerciseCards.appendChild(card);

      // Add initial set
      addSetRow(id, isBw);

      const modalElement = document.getElementById("addExerciseModal");
      if (modalElement) {
        const modal = bootstrap.Modal.getInstance(modalElement);
        if (modal) modal.hide();
      }
    });
  }

  // --- Helper: Update Set Numbers ---
  function updateSetNumbers(container) {
    const setRows = container.querySelectorAll(".set-row");
    setRows.forEach((row, index) => {
      const label = row.querySelector(".set-number-label");
      if (label) {
        label.textContent = `#${index + 1}`;
      }
    });
  }

  // --- Add Set Row ---
  function addSetRow(exerciseId, isBw) {
    const container = document.getElementById(`sets-for-${exerciseId}`);
    if (!container) return;

    const setCount = container.children.length + 1;
    const weightValue = isBw ? "0" : "";
    const weightDisabled = isBw ? "readonly" : "";

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

  // --- Handle Clicks in Exercise Card Area ---
  if (exerciseCards) {
    exerciseCards.addEventListener("click", function (e) {
      // 1. Add Set
      if (e.target.closest(".add-set")) {
        const btn = e.target.closest(".add-set");
        addSetRow(btn.dataset.id, btn.dataset.isBw === "true");
      }

      // 2. Remove Set
      if (e.target.closest(".remove-set")) {
        const setRow = e.target.closest(".set-row");
        const container = setRow.closest(".sets-container");
        const remainingSets = container.querySelectorAll(".set-row").length;

        if (remainingSets > 1) {
          setRow.remove();
          updateSetNumbers(container);
        } else {
          alert("An exercise must have at least one set.");
        }
      }

      // 3. Remove Exercise Card
      if (e.target.closest(".remove-exercise")) {
        e.target.closest(".exercise-card").remove();
      }

      // 4. View Exercise Detail Modal
      if (e.target.closest(".view-exercise-detail")) {
        e.preventDefault();
        const link = e.target.closest(".view-exercise-detail");
        lastFocusedElement = link;
        const exId = link.dataset.id;
        const exName = link.dataset.name;

        const modalElement = document.getElementById("exerciseDetailModal");
        if (modalElement) {
          let modal = bootstrap.Modal.getOrCreateInstance(modalElement);
          document.getElementById("detailModalTitle").textContent = exName;
          const body = document.getElementById("detailModalBody");

          body.innerHTML = '<div class="text-center py-5"><div class="spinner-border text-brand-primary"></div></div>';
          modal.show();

          fetch(`/workouts/exercises/${exId}/`, {
            headers: { "X-Requested-With": "XMLHttpRequest" },
          })
            .then((response) => response.text())
            .then((html) => {
              body.innerHTML = html;
              if (typeof window.initExerciseChart === "function") {
                window.initExerciseChart(exId);
              }
            })
            .catch((error) => {
              body.innerHTML = '<div class="alert alert-danger">Error loading exercise details.</div>';
              console.error("Error fetching exercise details:", error);
            });
        }
      }
    });
  }

  // --- Restore Focus After Modal Close ---
  const detailModalEl = document.getElementById('exerciseDetailModal');
  if (detailModalEl) {
    detailModalEl.addEventListener('hide.bs.modal', function () {
      if (document.activeElement) {
        document.activeElement.blur();
      }
    });
    detailModalEl.addEventListener('hidden.bs.modal', function () {
      if (lastFocusedElement) {
        lastFocusedElement.focus();
      }
    });
  }
});