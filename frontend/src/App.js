import React from "react";
import Dashboard from './Dashboard';
import Gauge from "./Gauge";

function App() {
    return (
        <div>
            <Dashboard />
            <div>
                <h1>React Liquid Gauge</h1>
                <Gauge />
            </div>
        </div>
    );
}

export default App;
