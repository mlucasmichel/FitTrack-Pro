document.addEventListener("DOMContentLoaded", function () {
  const canvasElement = document.getElementById("weeklyActivityChart");
  const labelsElement = document.getElementById("dash-labels");
  const dataElement = document.getElementById("dash-data");

  if (canvasElement && labelsElement && dataElement) {
    try {
      const labels = JSON.parse(labelsElement.textContent);
      const data = JSON.parse(dataElement.textContent);
      const hasData = data.some(val => val > 0);

      if (!hasData) {
          const container = canvasElement.parentElement;
          container.innerHTML = `
            <div class="d-flex flex-column align-items-center justify-content-center h-100 text-muted">
                <i class="fas fa-calendar-check fa-3x mb-3 opacity-25"></i>
                <p class="mb-0">No activity this week. Time to hit the gym!</p>
            </div>
          `;
          return;
      }

      const style = getComputedStyle(document.body);
      const primaryColor = style.getPropertyValue("--primary-100").trim() || "#FF5722";
      const primaryColorHover = style.getPropertyValue("--primary-200").trim() || "#ff8a50";

      const ctx = canvasElement.getContext("2d");

      new Chart(ctx, {
        type: "bar",
        data: {
          labels: labels,
          datasets: [
            {
              label: "Sets Completed",
              data: data,
              backgroundColor: primaryColor,
              hoverBackgroundColor: primaryColorHover,
              borderRadius: 6,
              borderSkipped: false,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              backgroundColor: "rgba(53, 53, 53, 0.9)",
              titleFont: { family: "'Lexend', sans-serif", size: 14 },
              bodyFont: { family: "'Roboto Flex', sans-serif", size: 14 },
              padding: 10,
              cornerRadius: 8,
            },
          },
          scales: {
            y: {
              beginAtZero: true,
              grid: { color: "rgba(0,0,0,0.05)" },
              ticks: { precision: 0 },
            },
            x: {
              grid: { display: false },
            },
          },
        },
      });
    } catch (error) {
      console.error("Error initializing Dashboard Chart:", error);
    }
  }
});
