import React from "react"

function Maintenance({data}){

return(

<div style={{marginTop:"30px"}}>

<h2>🔧 Maintenance Cost</h2>

<p>Estimated Cost Now: ₹{data.maintenance_cost.cost_now}</p>

<p>Cost if Delayed: ₹{data.maintenance_cost.cost_delayed}</p>

<h2>🔋 Range Prediction</h2>

<p>{data.range_prediction} km remaining</p>

<h2>⚡ Charging Advice</h2>

<p>{data.charging_advice}</p>

<h2>⚠ Component Risk</h2>

<ul>

<li>Battery: {data.component_risk.battery}</li>

<li>Motor: {data.component_risk.motor}</li>

<li>Brake: {data.component_risk.brake}</li>

</ul>

</div>

)

}

export default Maintenance