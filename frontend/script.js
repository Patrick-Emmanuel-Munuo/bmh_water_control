function printDashboard() {
    // Temporarily hide the print button to prevent it from printing
    document.getElementById('print-button').style.display = 'none';

    // Create a print-friendly version of the page (clone the current content)
    const printContent = document.querySelector('.body').cloneNode(true);
    
    // Open a new window to print
    const printWindow = window.open('', '', 'height=600,width=800');

    printWindow.document.write('<html><head><title>Water Tank Levels Dashboard</title>');
    printWindow.document.write('<style>');
    printWindow.document.write('body { font-family: Arial, sans-serif; }');
    printWindow.document.write('.container { margin: 20px; padding: 20px; border-radius: 8px; background-color: #fff; }');
    printWindow.document.write('.chart-container { max-width: 100%; margin-bottom: 20px; }');
    printWindow.document.write('#print-button { display: none; }'); // Hide the print button in the print version
    printWindow.document.write('</style></head><body>');
    
    // Append the cloned content to the print window
    printWindow.document.write(printContent.outerHTML);

    printWindow.document.write('</body></html>');
    printWindow.document.close();  // Necessary for IE >= 10
    printWindow.print();  // Trigger print dialog
    // After printing (or cancel), restore the print button
    printWindow.onafterprint = function() {
        document.getElementById('print-button').style.display = 'block'; // Show the print button again after printing
    };

    // In case the user cancels the print, we still want to restore the print button
    printWindow.close = function() {
        document.getElementById('print-button').style.display = 'block'; // Restore the button if printing was aborted
    };
}



// Create the initial chart configuration
let chart = new ApexCharts(document.querySelector("#chart"), {
    chart: {
        type: 'bar', // We can use bar chart to represent water levels
        height: 350
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
        text: `Water Tank Percentages Levels at ${new Date().toLocaleString()}`, // Display current date and time
        align: 'center'
    },
    plotOptions: {
        bar: {
            horizontal: false,
            columnWidth: '50%'
        }
    },
    colors: ['#00A9E0', '#007D9F', '#005D7A', '#003D54', '#4C9FD7', '#006B8E'],//colors: ['#00A9E0', '#007D9F', '#005D7A', '#003D54', '#4C9FD7', '#006B8E'], // Water-like shades of blue
    dataLabels: {
        enabled: true,
        formatter: function (val) {
            return val.toFixed(2) + "%"; // Display percentage with 1 decimal place
        }
    }
});
// Render the initial chart
chart.render();


// Create the initial chart configuration
let chart2 = new ApexCharts(document.querySelector("#chart2"), {
    chart: {
        type: 'bar', // We can use bar chart to represent water levels
        height: 500
    },
    series: [],
    xaxis: {
        categories: []
    },
    yaxis: {
        labels: {
            formatter: function (value) {
                return value.toFixed(1) + "m³";  // Format Y-axis labels with one decimal place
            }
        }
    },
    title: {
        text: `Water Tanks Volume Levels at ${new Date().toLocaleString()}`, // Display current date and time
        align: 'center'
    },
    plotOptions: {
        bar: {
            horizontal: false,
            columnWidth: '60%'
        }
    },
    colors: ['#FF6347', '#FF4500', '#DC143C', '#B22222', '#8B0000', '#A52A2A'],//colors: ['#00A9E0', '#007D9F', '#005D7A', '#003D54', '#4C9FD7', '#006B8E'], // Water-like shades of blue
    dataLabels: {
        enabled: true,
        formatter: function (val) {
            return val.toFixed(1) + "m³"; // Display percentage with 1 decimal place
        }
    }
});

// Render the initial chart
chart2.render();


// Fetch water levels and update chart with try and catch
async function fetchWaterLevels() {
    try {
        var url = 'http://localhost:5000/water_levels';

        const response = await fetch(url);
        const data = await response.json();
        if (data.success) {
            console.log('succesfull fetching water levels: ');
            updateChartData(data.message);
            updateHeaderInfo(data.message);  // Update the header with total volume and average percentage
        } else {
            console.log('Error fetching water levels: ', data);
            throw new Error('Failed to fetch water levels: ' + (data.message || 'Unknown error'));
        }
    } catch (error) {
        // Log the error to the console
        console.log('Error fetching water levels:', error);
    }
}

// Update chart with new data
function updateChartData(tanks) {
    const tankNames = tanks.map(tank => tank.tank_name);
    const tankLevels = tanks.map(tank => tank.water_level_percentage);
    const volume = tanks.map(tank => tank.curent_water_volume);
    //percentage chart
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


    //volume chart
    // Update chart categories (x-axis)
    chart2.updateOptions({
        xaxis: {
            categories: tankNames,
        }
    });
    // Update chart series (y-axis values)
    chart2.updateSeries([{
        name: 'Water volume (m³)',
        data: volume
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
    // Update the percentage chart title with current time
    chart.updateOptions({
        title: {
            text: `Water Tank Prcentages Levels at ${new Date().toLocaleString()}` // Update title with current time
        }
    });

    //update volume chart time at header
    chart2.updateOptions({
        title: {
            text: `Water Tanks Volume Levels at ${new Date().toLocaleString()}` // Update title with current time
        }
    });
}, 2000); // Update every second


// Initial fetch
// Declare a variable to hold the interval reference
let fetchInterval;

// Function to start fetching data at regular intervals
function startFetching() {
    fetchWaterLevels(); // Fetch data immediately once
    fetchInterval = setInterval(fetchWaterLevels, 10000); // Fetch every 10 seconds
}

// Function to stop fetching data
function stopFetching() {
    clearInterval(fetchInterval); // Clear the fetch interval
}

// Listen for the visibilitychange event
document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        // Tab is inactive, stop fetching data
        stopFetching();
    } else {
        // Tab is active, start fetching data
        startFetching();
    }
});

// Initial fetch when the page loads
if (!document.hidden) {
    startFetching(); // Only start fetching if the tab is active when the page loads
}
