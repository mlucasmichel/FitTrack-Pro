/**
 * charts.js - Initializes Chart.js for the progress chart on the dashboard.
 * This script waits for the DOM to load, then retrieves the labels and data from hidden elements,
 * and renders a line chart showing the user's progress over time. If there is no data, it displays
 * an empty state message instead.
 */
window.activeCharts = {};

window.initExerciseChart = function (exerciseId) {
  const canvasElement = document.getElementById(`progressChart-${exerciseId}`);
  const dataElement = document.getElementById(`chart-data-${exerciseId}`);

  if (canvasElement && dataElement) {
    try {
      const chartDataDict = JSON.parse(dataElement.textContent);
      const labels = chartDataDict.labels;

      const style = getComputedStyle(document.body);
      const primaryColor =
        style.getPropertyValue("--primary-100").trim() || "#eb9c64";
      const primaryColorTrans = primaryColor + "40";

      const ctx = canvasElement.getContext("2d");

      function renderChart(metricKey, labelName) {
        const data = chartDataDict[metricKey];

        if (window.activeCharts[exerciseId]) {
          window.activeCharts[exerciseId].destroy();
        }

        if (labels.length > 0) {
          window.activeCharts[exerciseId] = new Chart(ctx, {
            type: "line",
            data: {
              labels: labels,
              datasets: [
                {
                  label: labelName,
                  data: data,
                  borderColor: primaryColor,
                  backgroundColor: primaryColorTrans,
                  borderWidth: 3,
                  pointBackgroundColor: primaryColor,
                  pointRadius: 4,
                  fill: true,
                  tension: 0.4,
                },
              ],
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              plugins: { legend: { display: false } },
            },
          });
        } else {
          canvasElement.parentElement.innerHTML = `
                        <div class="d-flex flex-column align-items-center justify-content-center h-100 text-muted">
                            <i class="fas fa-clipboard-list fa-3x mb-3 opacity-25"></i>
                            <p class="mb-0">No data yet. Complete a workout to see your progress!</p>
                        </div>
                    `;
        }
      }

      // Initialize
      if (labels.length > 0) {
        renderChart("heaviest_weight", "Heaviest Weight (kg)");
      } else {
        renderChart("heaviest_weight", "");
      }

      // Button Logic specific to this exercise
      const buttons = document.querySelectorAll(
        `.chart-toggle[data-eid="${exerciseId}"]`,
      );

      buttons.forEach((btn) => {
        // Remove old listeners to prevent duplicates by cloning
        const newBtn = btn.cloneNode(true);
        btn.parentNode.replaceChild(newBtn, btn);

        newBtn.addEventListener("click", function () {
          const currentButtons = document.querySelectorAll(
            `.chart-toggle[data-eid="${exerciseId}"]`,
          );

          currentButtons.forEach((b) => {
            b.classList.remove("btn-brand-primary");
            b.classList.add("btn-outline-brand-primary");
          });

          this.classList.remove("btn-outline-brand-primary");
          this.classList.add("btn-brand-primary");

          document.getElementById(`chartTitle-${exerciseId}`).innerHTML =
            `<i class="fas fa-chart-line text-success me-2"></i> ${this.innerText}`;

          const metricMap = {
            heaviest_weight: "Heaviest Weight (kg)",
            estimated_1rm: "Estimated 1RM (kg)",
            best_set_volume: "Best Set Volume (kg)",
            session_volume: "Session Volume (kg)",
            total_reps: "Total Reps",
          };
          renderChart(this.dataset.metric, metricMap[this.dataset.metric]);
        });
      });
    } catch (error) {
      console.error("Error initializing Chart.js:", error);
    }
  }
};
