// Create the initial chart configuration
let chart = new ApexCharts(document.querySelector("#chart"), {
    chart: {
        type: 'bar', // We can use bar chart to represent water levels
        height: 400
    },
    series: [],
    xaxis: {
        categories: []
    },
    yaxis: {
        labels: {
            formatter: function (value) {
                return value.toFixed(1) + "%";  // Format Y-axis labels with one decimal place
            }
        }
    },
    title: {
        text: `Water Tank Levels at ${new Date().toLocaleString()}`, // Display current date and time
        align: 'center'
    },
    plotOptions: {
        bar: {
            horizontal: false,
            columnWidth: '50%'
        }
    },
    colors: ['#00A9E0', '#007D9F', '#005D7A', '#003D54', '#4C9FD7', '#006B8E'], // Water-like shades of blue
    dataLabels: {
        enabled: true,
        formatter: function (val) {
            return val.toFixed(1) + "%"; // Display percentage with 1 decimal place
        }
    }
});

// Render the initial chart
chart.render();

// Fetch water levels and update chart
function fetchWaterLevels() {
    fetch('http://localhost:5000/water_levels')  // Adjust the URL if needed
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateChartData(data.message);
                updateHeaderInfo(data.message);  // Update the header with total volume and average percentage
            } else {
                console.error('Failed to fetch water levels');
            }
        })
        .catch(error => {
            console.error('Error fetching water levels:', error);
        });
}

// Update chart with new data
function updateChartData(tanks) {
    const tankNames = tanks.map(tank => tank.tank_name);
    const tankLevels = tanks.map(tank => tank.water_level_percentage);
    const volume = tanks.map(tank => tank.curent_water_volume);
    // Update chart categories (x-axis)
    chart.updateOptions({
        xaxis: {
            categories: tankNames,
        }
    });

    // Update chart series (y-axis values)
    chart.updateSeries([{
        name: 'Water Level (%)',
        data: tankLevels
    }]);
}


// Calculate and update the header info (Total Volume and Average Percentage)
function updateHeaderInfo(tanks) {
    let totalVolume = 0;
    let totalPercentage = 0;
    let totalTanks = tanks.length;

    // Calculate total volume and average percentage
    tanks.forEach(tank => {
        totalVolume += tank.curent_water_volume;
        totalPercentage += tank.water_level_percentage;
    });

    const averagePercentage = (totalPercentage / totalTanks).toFixed(2);  // Calculate average percentage with 1 decimal place

    // Update the HTML elements
    document.getElementById('total-volume').textContent = totalVolume.toFixed(2) + " m³";
    document.getElementById('average-percentage').textContent = averagePercentage + " %";
}

// Update the title every second
setInterval(function() {
    // Update the chart title with current time
    chart.updateOptions({
        title: {
            text: `Water Tank Levels at ${new Date().toLocaleString()}` // Update title with current time
        }
    });
}, 1000); // Update every second
// Initial fetch
fetchWaterLevels();

// Fetch the data every 10 seconds for real-time updates
setInterval(fetchWaterLevels, 10000);
