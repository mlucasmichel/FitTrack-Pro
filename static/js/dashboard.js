/**
 * Dashboard Chart Initialization
 * This script initializes the weekly activity bar chart on the dashboard page.
 * It retrieves the chart data and labels from hidden script tags, applies theme colors, and configures Chart.js options for a clean and responsive design.
 */
document.addEventListener("DOMContentLoaded", function () {
  const canvasElement = document.getElementById("weeklyActivityChart");
  const labelsElement = document.getElementById("dash-labels");
  const dataElement = document.getElementById("dash-data");

  if (canvasElement && labelsElement && dataElement) {
    try {
      const labels = JSON.parse(labelsElement.textContent);
      const data = JSON.parse(dataElement.textContent);

      const style = getComputedStyle(document.body);
      const primaryColor =
        style.getPropertyValue("--primary-100").trim() || "#eb9c64";
      const primaryColorHover =
        style.getPropertyValue("--primary-200").trim() || "#ff8789";

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
