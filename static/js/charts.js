/**
* charts.js - Initializes interactive progress charts for exercises.
*/
window.activeCharts = {};

window.initExerciseChart = function (exerciseId) {
  const triggerEl = document.querySelector(`[data-eid="${exerciseId}"], [data-id="${exerciseId}"]`);
  const isBodyweight = triggerEl?.dataset.isBw === 'true';
  const canvasElement = document.getElementById(`progressChart-${exerciseId}`);
  const dataElement = document.getElementById(`chart-data-${exerciseId}`);

  if (canvasElement && dataElement) {
    try {
      const chartDataDict = JSON.parse(dataElement.textContent);
      const labels = chartDataDict.labels;
      const ctx = canvasElement.getContext("2d");

      // Get brand colors
      const style = getComputedStyle(document.body);
      const primaryColor = style.getPropertyValue("--primary-100").trim() || "#eb9c64";
      const primaryColorTrans = primaryColor + "40";

      function renderChart(metricKey, labelName) {
        if (window.activeCharts[exerciseId]) {
          window.activeCharts[exerciseId].destroy();
        }

        if (labels.length > 0) {
          window.activeCharts[exerciseId] = new Chart(ctx, {
            type: "line",
            data: {
              labels: labels,
              datasets: [{
                label: labelName,
                data: chartDataDict[metricKey],
                borderColor: primaryColor,
                backgroundColor: primaryColorTrans,
                borderWidth: 3,
                pointBackgroundColor: primaryColor,
                pointRadius: 4,
                fill: true,
                tension: 0.4,
              }],
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              plugins: {
                legend: { display: false },
                tooltip: {
                  callbacks: {
                    label: function(context) {
                      let value = context.parsed.y;
                      let unit = metricKey.includes('reps') ? ' reps' : ' kg';
                      return `${value}${unit}`;
                    }
                  }
                }
              },
              scales: {
                y: {
                  beginAtZero: true,
                  min: 0,
                  grid: { color: "rgba(0,0,0,0.05)" },
                  ticks: {
                    callback: function(value) {
                      let unit = metricKey.includes('reps') ? ' reps' : ' kg';
                      return value + unit;
                    }
                  }
                },
                x: { grid: { display: false } }
              }
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
      const defaultMetric = isBodyweight ? "session_volume" : "heaviest_weight";
      const defaultLabel = isBodyweight ? "Session Volume (reps)" : "Heaviest Weight (kg)";
      renderChart(defaultMetric, defaultLabel);

      // --- Button Logic ---
      const buttons = document.querySelectorAll(`.chart-toggle[data-eid="${exerciseId}"]`);

      buttons.forEach((btn) => {
        if (isBodyweight && (btn.dataset.metric === 'heaviest_weight' || btn.dataset.metric === 'estimated_1rm')) {
            btn.style.display = 'none';
        }

        const newBtn = btn.cloneNode(true);
        btn.parentNode.replaceChild(newBtn, btn);

        newBtn.addEventListener("click", function () {
          const currentButtons = document.querySelectorAll(`.chart-toggle[data-eid="${exerciseId}"]`);
          currentButtons.forEach((b) => {
            b.classList.remove("btn-brand-primary");
            b.classList.add("btn-outline-brand-primary");
          });

          this.classList.remove("btn-outline-brand-primary");
          this.classList.add("btn-brand-primary");

          const metricMap = {
            heaviest_weight: "Heaviest Weight (kg)",
            estimated_1rm: "Estimated 1RM (kg)",
            best_set_volume: "Best Set Volume",
            session_volume: "Session Volume",
            total_reps: "Total Reps",
          };

          const metric = this.dataset.metric;
          const label = metricMap[metric];

          // Update the Title above the chart
          const titleEl = document.getElementById(`chartTitle-${exerciseId}`);
          if (titleEl) titleEl.innerHTML = `<i class="fas fa-chart-line text-success me-2"></i> ${label}`;

          renderChart(metric, label);
        });
      });
    } catch (error) {
      console.error("Error initializing Chart.js:", error);
    }
  }
};