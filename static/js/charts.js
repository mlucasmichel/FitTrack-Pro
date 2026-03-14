/**
 * charts.js - Initializes Chart.js for the progress chart on the dashboard.
 * This script waits for the DOM to load, then retrieves the labels and data from hidden elements,
 * and renders a line chart showing the user's progress over time. If there is no data, it displays
 * an empty state message instead.
 */
document.addEventListener('DOMContentLoaded', function() {
    const canvasElement = document.getElementById('progressChart');
    const dataElement = document.getElementById('chart-data');
    let currentChart = null;

    if (canvasElement && dataElement) {
        try {
            const chartDataDict = JSON.parse(dataElement.textContent);
            const labels = chartDataDict.labels;

            const style = getComputedStyle(document.body);
            const primaryColor = style.getPropertyValue('--primary-100').trim() || '#eb9c64';
            const primaryColorTrans = primaryColor + '40';

            const ctx = canvasElement.getContext('2d');

            // Function to render the chart
            function renderChart(metricKey, labelName) {
                const data = chartDataDict[metricKey];

                // Destroy existing chart if it exists
                if (currentChart) {
                    currentChart.destroy();
                }

                if (labels.length > 0) {
                    currentChart = new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: labels,
                            datasets: [{
                                label: labelName,
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
                                    grid: { color: 'rgba(0,0,0,0.05)' }
                                },
                                x: {
                                    grid: { display: false }
                                }
                            }
                        }
                    });
                } else {
                    canvasElement.parentElement.innerHTML = `
                        <div class="d-flex flex-column align-items-center justify-content-center h-100 text-muted">
                            <i class="fas fa-clipboard-list fa-3x mb-3 opacity-25"></i>
                            <p class="mb-0">No data yet. Complete a workout to see your progress!</p>
                        </div>
                    `;
                    document.querySelector('.chart-toggle').parentElement.style.display = 'none';
                }
            }

            // Initialize with the first metric
            if (labels.length > 0) {
                renderChart('heaviest_weight', 'Heaviest Weight (kg)');
            } else {
                renderChart('heaviest_weight', '');
            }

            // Add Event Listeners to Buttons
            const buttons = document.querySelectorAll('.chart-toggle');
            buttons.forEach(btn => {
                btn.addEventListener('click', function() {
                    // Update Button Styles
                    buttons.forEach(b => {
                        b.classList.remove('btn-primary');
                        b.classList.add('btn-outline-primary');
                    });
                    this.classList.remove('btn-outline-primary');
                    this.classList.add('btn-primary');

                    // Update Title
                    document.getElementById('chartTitle').innerHTML = `<i class="fas fa-chart-line text-success me-2"></i> ${this.innerText}`;

                    // Render new chart
                    const metricMap = {
                        'heaviest_weight': 'Heaviest Weight (kg)',
                        'estimated_1rm': 'Estimated 1RM (kg)',
                        'best_set_volume': 'Best Set Volume (kg)',
                        'session_volume': 'Session Volume (kg)',
                        'total_reps': 'Total Reps'
                    };
                    renderChart(this.dataset.metric, metricMap[this.dataset.metric]);
                });
            });

        } catch (error) {
            console.error("Error initializing Chart.js:", error);
        }
    }
});