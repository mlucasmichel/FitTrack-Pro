/**
 * charts.js - Initializes Chart.js for the progress chart on the dashboard.
 * This script waits for the DOM to load, then retrieves the labels and data from hidden elements,
 * and renders a line chart showing the user's progress over time. If there is no data, it displays
 * an empty state message instead.
 */
document.addEventListener('DOMContentLoaded', function() {
    const canvasElement = document.getElementById('progressChart');
    const labelsElement = document.getElementById('labels-data');
    const dataElement = document.getElementById('volume-data');

    if (canvasElement && labelsElement && dataElement) {
        try {
            // Parse JSON data
            const labels = JSON.parse(labelsElement.textContent);
            const data = JSON.parse(dataElement.textContent);

            // Get colors from CSS variables
            const style = getComputedStyle(document.body);
            const primaryColor = style.getPropertyValue('--primary-100').trim() || '#eb9c64';
            const primaryColorTrans = primaryColor + '40';

            const ctx = canvasElement.getContext('2d');

            if (data.length > 0) {
                // Render Chart
                new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'Total Volume (kg)',
                            data: data,
                            borderColor: primaryColor,
                            backgroundColor: primaryColorTrans,
                            borderWidth: 3,
                            pointBackgroundColor: primaryColor,
                            pointRadius: 4,
                            fill: true,
                            tension: 0.4
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { display: false },
                            tooltip: {
                                backgroundColor: 'rgba(53, 53, 53, 0.9)',
                                titleFont: { family: "'Lexend', sans-serif", size: 14 },
                                bodyFont: { family: "'Roboto Flex', sans-serif", size: 14 },
                                padding: 10,
                                cornerRadius: 8,
                            }
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                grid: { color: 'rgba(0,0,0,0.05)' },
                                ticks: { font: { family: "'Roboto Flex', sans-serif" } }
                            },
                            x: {
                                grid: { display: false },
                                ticks: { font: { family: "'Roboto Flex', sans-serif" } }
                            }
                        }
                    }
                });
            } else {
                // Show empty state inside the canvas container
                const canvasContainer = canvasElement.parentElement;
                canvasContainer.innerHTML = `
                    <div class="d-flex flex-column align-items-center justify-content-center h-100 text-muted">
                        <i class="fas fa-clipboard-list fa-3x mb-3 opacity-25"></i>
                        <p class="mb-0">No data yet. Complete a workout to see your progress!</p>
                    </div>
                `;
            }
        } catch (error) {
            console.error("Error initializing Chart.js:", error);
        }
    }
});