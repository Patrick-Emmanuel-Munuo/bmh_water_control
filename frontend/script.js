// Function to fetch the water tank levels using fetch
function fetchWaterLevels() {
    document.getElementById('loading').style.display = 'block'; // Show loading

    fetch('http://localhost:5000/water_levels')  // Flask API endpoint
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                displayGraph(data.message);
                displayTankInfo(data.message);
            } else {
                console.error('Error fetching water levels:', data.message);
                alert('Failed to fetch water levels.');
            }
        })
        .catch(error => {
            console.error('API Error:', error);
            alert('Failed to fetch water tank data. Please try again.');
        })
        .finally(() => {
            document.getElementById('loading').style.display = 'none'; // Hide loading
        });
}

// Function to display the water levels on the graph using ApexCharts
function displayGraph(tankData) {
    const tankNames = tankData.map(tank => tank.tank_name);
    const waterLevels = tankData.map(tank => parseFloat(tank.water_level_percentage.toFixed(2)));

    const options = {
        series: [{
            name: 'Water Level (%)',
            data: waterLevels
        }],
        chart: {
            type: 'bar',
            height: 350,
            background: '#f4f4f4'
        },
        title: {
            text: 'Water Tank Levels (%)',
            align: 'center',
            style: {
                fontSize: '24px',
                fontWeight: 'bold',
                color: '#1E90FF'
            }
        },
        xaxis: {
            categories: tankNames,
            title: {
                text: 'Tanks'
            },
            labels: {
                style: {
                    fontSize: '14px',
                    colors: ['#555']
                }
            }
        },
        yaxis: {
            title: {
                text: 'Water Level (%)'
            },
            max: 100,
            min: 0,
            tickAmount: 5
        },
        colors: ['#1E90FF'], // Water-like blue color
        plotOptions: {
            bar: {
                horizontal: false,
                columnWidth: '50%'
            }
        },
        dataLabels: {
            enabled: true,
            style: {
                fontSize: '14px',
                colors: ['#fff']
            },
            formatter: function (value) {
                return value.toFixed(2) + '%';  // Show percentage with 2 decimals
            }
        },
        tooltip: {
            y: {
                formatter: function (val) {
                    return val.toFixed(2) + '%';
                }
            }
        }
    };

    const chart = new ApexCharts(document.querySelector("#chart"), options);
    chart.render();
}

// Function to display the tank information below the graph
function displayTankInfo(tankData) {
    const tankInfoContainer = document.getElementById('tankInfo');
    tankInfoContainer.innerHTML = '';  // Clear any previous data

    tankData.forEach(tank => {
        const tankDiv = document.createElement('div');
        tankDiv.classList.add('tank');
        tankDiv.innerHTML = `
            <h3>${tank.tank_name}</h3>
            <p>Current Water Level: <span class="volume">${tank.water_level_percentage.toFixed(2)}%</span></p>
            <p>Current Volume: <span class="volume">${tank.curent_water_volume.toFixed(2)}L</span></p>
            <p>Total Volume: <span class="volume">${tank.tank_total_volume}L</span></p>
            <p>Height: <span class="volume">${tank.height.toFixed(2)} m</span></p>
        `;
        tankInfoContainer.appendChild(tankDiv);
    });
}

// Fetch water levels every 60 seconds (setInterval)
setInterval(fetchWaterLevels, 600000);  // 600000ms = 60 seconds
window.onload = fetchWaterLevels;  // Fetch on initial load
