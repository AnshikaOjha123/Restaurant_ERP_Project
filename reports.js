function loadReports(dailyLabels, dailyData, monthlyLabels, monthlyData, popularLabels, popularData) {
    // Daily Sales
    new Chart(document.getElementById('dailyChart'), {
        type: 'bar',
        data: {
            labels: dailyLabels,
            datasets: [{
                label: 'Daily Sales',
                data: dailyData,
                backgroundColor: 'rgba(54, 162, 235, 0.7)'
            }]
        }
    });

    // Monthly Sales
    new Chart(document.getElementById('monthlyChart'), {
        type: 'line',
        data: {
            labels: monthlyLabels,
            datasets: [{
                label: 'Monthly Sales',
                data: monthlyData,
                borderColor: 'rgba(75, 192, 192, 1)',
                fill: true,
                backgroundColor: 'rgba(75, 192, 192, 0.2)'
            }]
        }
    });

    // Popular Dishes
    new Chart(document.getElementById('popularChart'), {
        type: 'doughnut',
        data: {
            labels: popularLabels,
            datasets: [{
                data: popularData,
                backgroundColor: ['#ff6384','#36a2eb','#ffce56','#4bc0c0','#9966ff']
            }]
        }
    });
}