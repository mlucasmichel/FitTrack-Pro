/**
* This script handles the drag-and-drop functionality for the routine builder page,
* as well as the mobile-friendly modal selection.
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
  const modalSearch = document.getElementById("modal-library-search");
  const modalExerciseList = document.getElementById("modal-exercise-list");

  // --- Search Functionality (Desktop and Modal) ---
  function initFilter(searchInput, filterDropdown, selector) {
    function applyFilter() {
      const query = searchInput ? searchInput.value.toLowerCase() : "";
      const bodyPart = filterDropdown ? filterDropdown.value.toLowerCase() : "";

      document.querySelectorAll(selector).forEach((item) => {
        const name = item.dataset.name.toLowerCase();
        const part = item.dataset.bodypart.toLowerCase();

        const matchesSearch = name.includes(query);
        const matchesFilter = bodyPart === "" || part === bodyPart;

        item.style.display = (matchesSearch && matchesFilter) ? "block" : "none";

        if (item.nextElementSibling && item.nextElementSibling.tagName === 'HR') {
            item.nextElementSibling.style.display = (matchesSearch && matchesFilter) ? "block" : "none";
        }
      });
    }

    if (searchInput) searchInput.addEventListener("input", applyFilter);
    if (filterDropdown) filterDropdown.addEventListener("change", applyFilter);
  }

  initFilter(
    document.getElementById("library-search"),
    document.getElementById("library-filter"),
    ".draggable-exercise"
  );
  initFilter(
    document.getElementById("modal-library-search"),
    document.getElementById("modal-library-filter"),
    ".modal-draggable-item"
  );

  // --- 2. Initialize SortableJS ---
  if (libraryZone) {
    new Sortable(libraryZone, {
      group: { name: "shared", pull: "clone", put: false },
      animation: 150,
      sort: false,
      draggable: ".draggable-exercise",
      handle: ".drag-handle",
    });
  }

  if (builderZone) {
    new Sortable(builderZone, {
      group: "shared",
      animation: 150,
      draggable: ".built-exercise",
      handle: ".drag-handle",
      onAdd: function (evt) {
        const itemEl = evt.item;
        const exId = itemEl.dataset.id;
        const exName = itemEl.dataset.name;
        const exImg = itemEl.dataset.img;
        itemEl.remove();
        addExerciseToBuilder(exId, exName, exImg);
      },
      onSort: updateSummary,
    });
  }

  // --- Add Function ---
  function addExerciseToBuilder(exId, exName, exImg) {
    if (emptyState) emptyState.style.display = "none";
    builderZone.classList.remove("card", "bg-white", "shadow-sm", "p-4");

    const card = document.createElement("div");
    card.className = "card border border-primary shadow-sm rounded-4 p-3 mb-3 bg-white built-exercise";
    card.dataset.id = exId;
    card.innerHTML = `
        <div class="d-flex align-items-center mb-3">
            <i class="fas fa-grip-vertical text-muted drag-handle me-3" style="cursor: grab; font-size: 1.2rem;"></i>
            <div class="bg-light rounded-circle p-1 me-3" style="width: 45px; height: 45px;">
                <img src="${exImg}" class="w-100 h-100 object-fit-cover rounded-circle">
            </div>
            <div class="flex-grow-1">
                <a href="javascript:void(0);" class="h5 fw-bold mb-0 text-primary text-decoration-none view-exercise-detail" data-id="${exId}" data-name="${exName}">
                    ${exName}
                </a>
            </div>
            <button type="button" class="btn btn-sm btn-light text-danger rounded-circle remove-builder-exercise">
                <i class="fas fa-times"></i>
            </button>
        </div>
        <div class="row g-2 px-4 ms-2">
            <div class="col-6">
                <label class="form-label small fw-bold text-muted mb-1">Target Sets</label>
                <input type="number" class="form-control border-0 bg-light rounded-pill px-3 target-sets-input" value="3" min="1" required>
            </div>
            <div class="col-6">
                <label class="form-label small fw-bold text-muted mb-1">Target Reps</label>
                <input type="number" class="form-control border-0 bg-light rounded-pill px-3 target-reps-input" value="10" min="1" required>
            </div>
        </div>
    `;
    builderZone.appendChild(card);
    updateSummary();
  }

  // --- Modal Add Button ---
  if (modalExerciseList) {
    modalExerciseList.addEventListener("click", function (e) {
      const addBtn = e.target.closest(".add-to-routine-btn");
      if (!addBtn) return;

      const item = addBtn.closest(".modal-draggable-item");
      addExerciseToBuilder(item.dataset.id, item.dataset.name, item.dataset.img);

      const modal = bootstrap.Modal.getInstance(document.getElementById("addExerciseToRoutineModal"));
      if (modal) modal.hide();
    });
  }

  // --- Event Listeners for Builder Zone ---
  builderZone.addEventListener("click", function (e) {
    if (e.target.closest(".remove-builder-exercise")) {
      e.target.closest(".built-exercise").remove();
      if (builderZone.querySelectorAll(".built-exercise").length === 0) {
        if (emptyState) emptyState.style.display = "block";
        builderZone.classList.add("card", "bg-white", "shadow-sm", "p-4");
      }
      updateSummary();
    }
  });

  builderZone.addEventListener("input", function (e) {
    if (e.target.classList.contains("target-sets-input")) updateSummary();
  });

  // --- Summary Calculator ---
  function updateSummary() {
    const exercises = builderZone.querySelectorAll(".built-exercise");
    let totalSets = 0;
    exercises.forEach((ex) => {
      const setInput = ex.querySelector(".target-sets-input");
      if (setInput && setInput.value) totalSets += parseInt(setInput.value);
    });
    if (summaryExercises) summaryExercises.textContent = exercises.length;
    if (summarySets) summarySets.textContent = totalSets;
  }

  // --- Form Submission ---
  form.addEventListener("submit", function (e) {
    const exercises = builderZone.querySelectorAll(".built-exercise");
    if (exercises.length === 0) {
      e.preventDefault();
      alert("Please add at least one exercise.");
      return;
    }
    const routineData = Array.from(exercises).map((ex) => ({
      exercise_id: parseInt(ex.dataset.id),
      sets: parseInt(ex.querySelector(".target-sets-input").value),
      reps: parseInt(ex.querySelector(".target-reps-input").value),
    }));
    dataInput.value = JSON.stringify(routineData);
  });

  // --- Modal Detail (AJAX) ---
  document.body.addEventListener("click", function (e) {
    if (e.target.closest(".view-exercise-detail")) {
      e.preventDefault();
      const link = e.target.closest(".view-exercise-detail");
      const exId = link.dataset.id;
      const modalElement = document.getElementById("exerciseDetailModal");
      if (modalElement) {
        let modal = bootstrap.Modal.getOrCreateInstance(modalElement);
        document.getElementById("detailModalTitle").textContent = link.dataset.name;
        const body = document.getElementById("detailModalBody");
        body.innerHTML = '<div class="text-center py-5"><div class="spinner-border text-primary"></div></div>';
        modal.show();
        fetch(`/workouts/exercises/${exId}/`, { headers: { "X-Requested-With": "XMLHttpRequest" } })
          .then((r) => r.text())
          .then((html) => {
            body.innerHTML = html;
            if (typeof window.initExerciseChart === "function") window.initExerciseChart(exId);
          });
      }
    }
  });

  updateSummary();
});