// charts.js

function renderAppointmentsPieChart(chartId, dataObj) {
    const labels = [
        'Completed',
        'Cancelled',
        'No Show',
        'Requested',
        'Confirmed',
        'Checked In'
    ];

    const data = [
        dataObj.completed_appointments,
        dataObj.cancelled_appointments,
        dataObj.no_show_appointments,
        dataObj.requested_appointments,
        dataObj.confirmed_appointments,
        dataObj.checked_in_appointments
    ];

    const ctx = document.getElementById(chartId).getContext('2d');

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                label: 'Appointments',
                data: data,
                backgroundColor: [
                    'rgba(75, 192, 192, 0.6)',   // Completed
                    'rgba(255, 99, 132, 0.6)',   // Cancelled
                    'rgba(255, 206, 86, 0.6)',   // No Show
                    'rgba(153, 102, 255, 0.6)',  // Requested
                    'rgba(54, 162, 235, 0.6)',   // Confirmed
                    'rgba(255, 159, 64, 0.6)'    // Checked In
                ],
                borderColor: [
                    'rgba(255,255,255,1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                },
                title: {
                    display: true,
                    text: 'Appointments Status Distribution'
                }
            }
        }
    });
}