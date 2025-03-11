import React, { useState } from "react";
import LiquidFillGauge from "react-liquid-gauge";

const GaugeComponent = () => {
  const [value, setValue] = useState(50.02); // Change this value dynamically
  
  // Function to format the decimal value
  const formatDecimalValue = (value) => {
    return value.toFixed(2); // Format value to 2 decimal places
  };

  // Function to get color based on value
  const getColor = (value) => {
    if (value < 20) {
      return { start: '#ff0000', stop: '#ff6666' }; // Red for low values
    } else if (value >= 20 && value < 60) {
      return { start: '#ffff00', stop: '#ffff99' }; // Yellow for medium values
    } else {
      return { start: '#00ff00', stop: '#66ff66' }; // Green for high values
    }
  };

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <LiquidFillGauge
        style={{ margin: "0 auto" }}
        width={150}
        height={400}
        value={value}
        textSize={1}
        textOffsetX={0}
        textOffsetY={0}
        riseAnimation
        waveAnimation
        waveFrequency={1}
        waveAmplitude={1}
        gradient={getColor(value)}  // Set the gradient based on value
        formatValue={formatDecimalValue}
      />
      <br />
      <button onClick={() => setValue(Math.random() * 100.00)}>
        Change Value
      </button>
    </div>
  );
};

export default GaugeComponent;
