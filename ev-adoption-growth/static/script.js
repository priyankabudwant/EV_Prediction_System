// Load categories on page load
document.addEventListener('DOMContentLoaded', function() {
    loadCategories();
    loadTop5Growth();
    loadCO2Reduction();
    load2wVs4wChart();
    loadYearlyTrend();
});

// Load available categories
async function loadCategories() {
    try {
        const response = await fetch('/api/categories');
        const categories = await response.json();
        
        const select = document.getElementById('category');
        select.innerHTML = categories.map(cat => 
            `<option value="${cat}">${cat}</option>`
        ).join('');
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

// Predict future values
async function predictFuture() {
    const category = document.getElementById('category').value;
    const year = document.getElementById('year').value;
    const resultDiv = document.getElementById('prediction-result');
    
    if (!category || !year) {
        resultDiv.innerHTML = '<div class="error-message">Please select category and year</div>';
        return;
    }
    
    resultDiv.innerHTML = '<div class="loader"></div>';
    
    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ category, year: parseInt(year) })
        });
        
        const data = await response.json();
        
        if (data.error) {
            resultDiv.innerHTML = `<div class="error-message">${data.error}</div>`;
        } else {
            resultDiv.innerHTML = `
                <div class="success-message">
                    <strong>${data.category}</strong><br>
                    Predicted registrations in ${data.year}: <br>
                    <span style="font-size: 1.5em;">${data.prediction.toLocaleString()}</span> vehicles
                </div>
            `;
        }
    } catch (error) {
        resultDiv.innerHTML = '<div class="error-message">Error making prediction</div>';
        console.error('Error:', error);
    }
}

// Load Top 5 Growth
async function loadTop5Growth() {
    const container = document.getElementById('top5-container');
    
    try {
        const response = await fetch('/api/top5-growth');
        const data = await response.json();
        
        container.innerHTML = data.map((item, index) => `
            <div class="stat-item" style="animation-delay: ${index * 0.1}s">
                <div>
                    <div class="stat-label">${item.category}</div>
                    <div style="font-size: 0.9em; color: #666;">
                        Current: ${item.current.toLocaleString()} → 
                        2035: ${item.future.toLocaleString()}
                    </div>
                </div>
                <div class="stat-value">+${item.growth.toLocaleString()}</div>
            </div>
        `).join('');
    } catch (error) {
        container.innerHTML = '<div class="error-message">Error loading data</div>';
        console.error('Error:', error);
    }
}

// Load CO2 Reduction
async function loadCO2Reduction() {
    const container = document.getElementById('co2-container');
    
    try {
        const response = await fetch('/api/co2-reduction');
        const data = await response.json();
        
        container.innerHTML = data.map((item, index) => `
            <div class="stat-item co2-item" style="animation-delay: ${index * 0.1}s">
                <div class="stat-label">${item.category}</div>
                <div class="stat-value">${item.co2_reduction.toLocaleString()} tons CO₂</div>
            </div>
        `).join('');
    } catch (error) {
        container.innerHTML = '<div class="error-message">Error loading data</div>';
        console.error('Error:', error);
    }
}

// Load 2W vs 4W Comparison Chart
async function load2wVs4wChart() {
    try {
        const response = await fetch('/api/2w-vs-4w');
        const data = await response.json();
        
        const ctx = document.getElementById('comparison-chart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.years,
                datasets: [
                    {
                        label: 'Two Wheeler',
                        data: data.two_wheeler,
                        borderColor: 'rgb(102, 126, 234)',
                        backgroundColor: 'rgba(102, 126, 234, 0.1)',
                        borderWidth: 3,
                        tension: 0.4,
                        fill: true
                    },
                    {
                        label: 'Four Wheeler',
                        data: data.four_wheeler,
                        borderColor: 'rgb(245, 87, 108)',
                        backgroundColor: 'rgba(245, 87, 108, 0.1)',
                        borderWidth: 3,
                        tension: 0.4,
                        fill: true
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                        labels: {
                            font: {
                                size: 14,
                                weight: 'bold'
                            }
                        }
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        callbacks: {
                            label: function(context) {
                                return context.dataset.label + ': ' + 
                                       context.parsed.y.toLocaleString() + ' vehicles';
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return value.toLocaleString();
                            }
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error loading chart:', error);
    }
}

// Load Yearly Trend Chart
async function loadYearlyTrend() {
    try {
        const response = await fetch('/api/yearly-trend');
        const data = await response.json();
        
        const ctx = document.getElementById('trend-chart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.years,
                datasets: [{
                    label: 'Total EV Registrations',
                    data: data.total,
                    backgroundColor: 'rgba(102, 126, 234, 0.8)',
                    borderColor: 'rgb(102, 126, 234)',
                    borderWidth: 2,
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                        labels: {
                            font: {
                                size: 14,
                                weight: 'bold'
                            }
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return 'Total: ' + context.parsed.y.toLocaleString() + ' vehicles';
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return value.toLocaleString();
                            }
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error loading trend chart:', error);
    }
}
