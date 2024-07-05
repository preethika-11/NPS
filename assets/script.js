document.addEventListener('DOMContentLoaded', async () => {
    const csvUrl = 'data.csv'; // Correct the file path
    const csvData = await fetchCSV(csvUrl);
    const parsedData = parseCSV(csvData);
    populateTable(parsedData);

    initializeCharts();
});
// Extract data from the table
const labels = [];
const quantities = [];
const skusCount = [];

const table = document.getElementById('dataTable');
for (let i = 1; i < table.rows.length; i++) {
    labels.push(table.rows[i].cells[3].innerText);
    quantities.push(table.rows[i].cells[4].innerText);
    skusCount.push(table.rows[i].cells[5].innerText);
}

// Create the chart
const ctx = document.getElementById('myChart').getContext('2d');
const myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: labels,
        datasets: [
            {
                label: 'Quantity',
                data: quantities,
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            },
            {
                label: 'sKUs Count',
                data: skusCount,
                backgroundColor: 'rgba(60, 179, 113, 0.2)',
                borderColor: 'rgba(60, 179, 113, 1)',
                borderWidth: 1
            }
        ]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

//Download Graph
document.querySelector('.download-btn').addEventListener('click', function() {
    const link = document.createElement('a');
    link.href = myChart.toBase64Image();
    link.download = 'graph.png';
    link.click();
});

//Download Table
document.querySelector('.download-btn-table').addEventListener('click', function() {
    let csvContent = 'data:text/csv;charset=utf-8,';
    const rows = document.querySelectorAll('table tr');
    rows.forEach(row => {
        const cols = row.querySelectorAll('td, th');
        const data = Array.from(cols).map(col => col.innerText).join(',');
        csvContent += data + '\n';
    });
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', 'table.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
});
