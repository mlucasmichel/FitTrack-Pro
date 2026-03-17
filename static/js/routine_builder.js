/**
 * This script handles the drag-and-drop functionality for the routine builder page,
 */

document.addEventListener("DOMContentLoaded", function () {
  const libraryZone = document.getElementById("exercise-library-zone");
  const builderZone = document.getElementById("routine-builder-zone");
  const emptyState = document.getElementById("empty-builder-state");
  const summaryExercises = document.getElementById("summary-exercises");
  const summarySets = document.getElementById("summary-sets");
  const form = document.getElementById("routine-form");
  const dataInput = document.getElementById("routine-data-input");
  const searchInput = document.getElementById("library-search");

  // --- Search Functionality for the Library ---
  if (searchInput) {
    searchInput.addEventListener("input", function (e) {
      const query = e.target.value.toLowerCase();
      document.querySelectorAll(".draggable-exercise").forEach((item) => {
        const name = item.dataset.name.toLowerCase();
        item.style.display = name.includes(query) ? "block" : "none";
      });
    });
  }

  // --- Initialize SortableJS for the Library (Clone Mode) ---
  new Sortable(libraryZone, {
    group: {
      name: "shared",
      pull: "clone",
      put: false,
    },
    animation: 150,
    sort: false,
  });

  // --- Initialize SortableJS for the Builder Zone ---
  new Sortable(builderZone, {
    group: "shared",
    animation: 150,
    handle: ".drag-handle",

    onAdd: function (evt) {
      emptyState.style.display = "none";

      builderZone.classList.remove('card', 'bg-white', 'shadow-sm', 'p-4');

      const itemEl = evt.item;
      const exId = itemEl.dataset.id;
      const exName = itemEl.dataset.name;
      const exImg = itemEl.dataset.img;

      itemEl.className =
        "card shadow-sm rounded-4 p-3 mb-3 built-exercise bg-white";
      itemEl.innerHTML = `
                <div class="d-flex align-items-center mb-3">
                    <i class="fas fa-grip-vertical text-muted drag-handle me-3 pe-auto" style="cursor: grab; font-size: 1.2rem;"></i>
                    <div class="bg-light rounded-circle p-1 me-3 view-exercise-detail cursor-pointer" data-id="${exId}" data-name="${exName}" style="width: 45px; height: 45px;">
                        <img src="${exImg}" class="w-100 h-100 object-fit-cover rounded-circle">
                    </div>
                    <div class="flex-grow-1 view-exercise-detail cursor-pointer" data-id="${exId}" data-name="${exName}">
                        <h5 class="fw-bold mb-0 text-dark">${exName}</h5>
                    </div>
                    <button type="button" class="btn btn-sm btn-light text-danger rounded-circle remove-builder-exercise" title="Remove">
                        <i class="fas fa-times"></i>
                    </button>
                </div>

                <div class="row g-2 px-4 ms-2">
                    <div class="col-6">
                        <label class="form-label small fw-bold text-muted mb-1">Target Sets</label>
                        <div class="input-group input-group-sm">
                            <span class="input-group-text border-0 bg-light rounded-start-pill"><i class="fas fa-layer-group text-muted"></i></span>
                            <input type="number" class="form-control border-0 bg-light rounded-end-pill target-sets-input" value="3" min="1" required>
                        </div>
                    </div>
                    <div class="col-6">
                        <label class="form-label small fw-bold text-muted mb-1">Target Reps</label>
                        <div class="input-group input-group-sm">
                            <span class="input-group-text border-0 bg-light rounded-start-pill"><i class="fas fa-redo text-muted"></i></span>
                            <input type="number" class="form-control border-0 bg-light rounded-end-pill target-reps-input" value="10" min="1" required>
                        </div>
                    </div>
                </div>
            `;
      updateSummary();
    },
    onSort: function (evt) {
      updateSummary();
    },
  });

  // --- Handle Removing Exercises and Updating Sets ---
  builderZone.addEventListener("click", function (e) {
    if (e.target.closest(".remove-builder-exercise")) {
      e.target.closest(".built-exercise").remove();

      if (builderZone.querySelectorAll(".built-exercise").length === 0) {
        emptyState.style.display = "block";
        builderZone.classList.add('card', 'bg-white', 'shadow-sm', 'p-4');
      }
      updateSummary();
    }
  });

  builderZone.addEventListener("input", function (e) {
    if (e.target.classList.contains("target-sets-input")) {
      updateSummary();
    }
  });

  // --- Summary Calculator ---
  function updateSummary() {
    const exercises = builderZone.querySelectorAll(".built-exercise");
    let totalSets = 0;

    exercises.forEach((ex) => {
      const setInput = ex.querySelector(".target-sets-input");
      if (setInput && setInput.value) {
        totalSets += parseInt(setInput.value);
      }
    });

    summaryExercises.textContent = exercises.length;
    summarySets.textContent = totalSets;
  }

  // --- Form Submission ---
  form.addEventListener("submit", function (e) {
    const exercises = builderZone.querySelectorAll(".built-exercise");

    if (exercises.length === 0) {
      e.preventDefault();
      alert("Please add at least one exercise to your routine.");
      return;
    }

    const routineData = [];

    exercises.forEach((ex) => {
      const id = ex.dataset.id;
      const sets = ex.querySelector(".target-sets-input").value;
      const reps = ex.querySelector(".target-reps-input").value;

      routineData.push({
        exercise_id: parseInt(id),
        sets: parseInt(sets),
        reps: parseInt(reps),
      });
    });

    dataInput.value = JSON.stringify(routineData);
  });

  // --- View Exercise Detail Modal (AJAX) ---
  document.body.addEventListener("click", function (e) {
    if (e.target.closest(".view-exercise-detail")) {
      e.preventDefault();

      const link = e.target.closest(".view-exercise-detail");
      const exId = link.dataset.id;
      const exName = link.dataset.name;

      const modalElement = document.getElementById("exerciseDetailModal");
      if (modalElement) {
        let modal = bootstrap.Modal.getInstance(modalElement);
        if (!modal) {
          modal = new bootstrap.Modal(modalElement);
        }

        document.getElementById("detailModalTitle").textContent = exName;
        const body = document.getElementById("detailModalBody");

        body.innerHTML =
          '<div class="text-center py-5"><div class="spinner-border text-primary"></div></div>';
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
            body.innerHTML =
              '<div class="alert alert-danger">Error loading exercise details.</div>';
            console.error("Error fetching details:", error);
          });
      }
    }
  });
});
