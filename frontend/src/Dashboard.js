import React, { useEffect, useState } from 'react';
import Chart from 'react-apexcharts';

const WaterDashboard = () => {
    const [tanks, setTanks] = useState([]);
    const [totalVolume, setTotalVolume] = useState('Loading...');
    const [averagePercentage, setAveragePercentage] = useState('Loading...');
    const percentageChartOptions = {
        chart: {
            type: 'bar',
            height: 350,
            toolbar: { show: true }
        },
        xaxis: {
            categories: tanks.map(tank => tank.tank_name),
            title: { text: 'Tanks' }
        },
        yaxis: {
            labels: {
                formatter: (value) => value.toFixed(1) + "%"
            },
            title: { text: 'Water Level Percentage' }
        },
        title: {
            text: 'Water Level Percentage Bar Graph',
            align: 'center',
            style: { fontSize: '18px', fontWeight: 'bold', color: '#333' }
        },
        plotOptions: {
            bar: {
                horizontal: false,
                columnWidth: '60%',
                colors: {
                    ranges: [
                        {
                            from: 0,
                            to: 25,
                            color: '#FF0000' // Red for 0-25%
                        },
                        {
                            from: 26,
                            to: 50,
                            color: '#FFA500' // Orange for 26-50%
                        },
                        {
                            from: 51,
                            to: 75,
                            color: '#FFFF00' // Yellow for 51-75%
                        },
                        {
                            from: 76,
                            to: 100,
                            color: '#008000' // Green for 76-100%
                        }
                    ]
                }
            }
        },
        dataLabels: {
            enabled: true,
            formatter: (val) => val.toFixed(2) + "%",
            style: {
                fontSize: '12px',
                fontWeight: 'bold',
                colors: ['#fff']
            }
        },
        grid: { borderColor: '#e1e1e1' },
        tooltip: {
            y: { formatter: (value) => value.toFixed(1) + "%" }
        }
    };
    const volumeChartOptions = {
        chart: {
            type: 'bar',
            height: 500,
            toolbar: { show: true }
        },
        xaxis: {
            categories: tanks.map(tank => tank.tank_name),
            title: { text: 'Tanks' }
        },
        yaxis: {
            labels: {
                formatter: (value) => value.toFixed(1) + " Lt"
            },
            title: { text: 'Water Volume (Litres)' }
        },
        title: {
            text: 'Volume Level Bar Graph',
            align: 'center',
            style: { fontSize: '18px', fontWeight: 'bold', color: '#333' }
        },
        plotOptions: {
            bar: {
                horizontal: false,
                columnWidth: '75%',
                colors: {
                    ranges: [
                        {
                            from: 0,
                            to: 1000,
                            color: '#FF0000' // Red for low volume (< 1000L)
                        },
                        {
                            from: 1001,
                            to: 5000,
                            color: '#FFA500' // Orange for medium volume (1001L - 5000L)
                        },
                        {
                            from: 5001,
                            to: 10000,
                            color: '#FFFF00' // Yellow for higher volume (5001L - 10000L)
                        },
                        {
                            from: 10001,
                            to: 50000,
                            color: '#008000' // Green for high volume (> 10000L)
                        }
                    ]
                }
            }
        },
        dataLabels: {
            enabled: true,
            formatter: (val) => val.toFixed(1) + " Lt", // Show the volume in Litres
            style: {
                fontSize: '12px',
                fontWeight: 'bold',
                colors: ['#fff']
            }
        },
        grid: { borderColor: '#e1e1e1' },
        tooltip: {
            y: { formatter: (value) => value.toFixed(1) + " Litres" }
        }
    };
    const fetchWaterLevels = async () => {
        try {
            const response = await fetch('http://127.0.0.1:5000/water_levels');
            const data = await response.json();
            if (data.success) {
                console.log('Successfully fetched water levels:', data.message);
                setTanks(data.message);
                updateHeaderInfo(data.message);
            } else {
                console.error('Failed to fetch water levels:', data.message);
            }
        } catch (error) {
            console.error('Error fetching water levels:', error);
        }
    };
    const updateHeaderInfo = (tanksData) => {
        const totalVolume = tanksData.reduce((acc, tank) => acc + tank.curent_water_volume, 0);
        const averagePercentage = (tanksData.reduce((acc, tank) => acc + tank.water_level_percentage, 0) / tanksData.length).toFixed(2);

        setTotalVolume(totalVolume.toLocaleString() + " Litres");
        setAveragePercentage(averagePercentage + " %");
    };
    useEffect(() => {
        fetchWaterLevels();  // initial fetch
        const interval = setInterval(fetchWaterLevels, 30000);  // fetch every 30 seconds
        return () => clearInterval(interval);  // cleanup on unmount
    }, []);

    const printDashboard = () => {
        const printContent = document.querySelector('.dashboard-container').cloneNode(true);
        const printWindow = window.open('', '', 'height=600,width=800');
        printWindow.document.write('<html><head><title>Water Tank Levels Dashboard</title>');
        printWindow.document.write('<style>body { font-family: Arial, sans-serif; }</style>');
        printWindow.document.write('</head><body>');
        printWindow.document.body.appendChild(printContent);
        printWindow.document.close();
        printWindow.print();
    };

    return (
        <div className="dashboard-container p-6 font-sans bg-gray-100 min-h-screen">
            <header className="text-center mb-8">
                <h1 className="text-3xl font-semibold text-gray-800">BMH Block I Water Tank Levels</h1>
            </header>

            <section className="info-section mb-8">
                <h3 className="text-lg">Volume Available: <span className="font-semibold text-xl">{totalVolume}</span></h3>
                <h3 className="text-lg">Percentage: <span className="font-semibold text-xl">{averagePercentage}</span></h3>
            </section>

            <section className="chart-container mb-8">
                <Chart options={percentageChartOptions} series={[{
                    name: 'Water Level (%)',
                    data: tanks.map(tank => tank.water_level_percentage)
                }]} type="bar" height={450} />
            </section>

            <section className="chart-container mb-8">
                <Chart options={volumeChartOptions} series={[{
                    name: 'Water volume (Litres)',
                    data: tanks.map(tank => tank.curent_water_volume)
                }]} type="bar" height={600} />
            </section>

            <div className="print-container mt-8 text-center">
                <button
                    className="bg-blue-500 text-white px-6 py-3 rounded-md font-semibold shadow-lg hover:bg-blue-600 transition"
                    onClick={printDashboard}
                >
                    Print Dashboard
                </button>
            </div>
        </div>
    );
};

export default WaterDashboard;
