import React from "react"

function HealthCards({health}){

return(

<div style={{display:"flex",gap:"20px",marginTop:"30px"}}>

<div style={cardStyle}>
<h3>Battery Health</h3>
<h2>{health.battery_health}%</h2>
</div>

<div style={cardStyle}>
<h3>Motor Health</h3>
<h2>{health.motor_health}%</h2>
</div>

<div style={cardStyle}>
<h3>Brake Health</h3>
<h2>{health.brake_health}%</h2>
</div>

<div style={cardStyle}>
<h3>Overall Health</h3>
<h2>{health.overall_health}%</h2>
</div>

</div>

)

}

const cardStyle = {

background:"#1e293b",
padding:"20px",
borderRadius:"10px",
width:"180px",
textAlign:"center"

}

export default HealthCards