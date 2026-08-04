import React from "react"
import GaugeChart from "react-gauge-chart"

function FailureGauge({risk}){

return(

<div style={{width:"400px"}}>

<h2>🚨 Failure Risk</h2>

<GaugeChart
id="gauge-chart"
nrOfLevels={20}
percent={risk/100}
textColor="#ffffff"
/>

<h3>{risk}% Risk</h3>

</div>

)

}

export default FailureGauge