import React from "react"

function Alerts({alerts}){

return(

<div style={{marginTop:"40px"}}>

<h2>🚨 Alerts</h2>

{alerts.length===0 ? (

<p>No alerts</p>

):( 

<ul>

{alerts.map((a,i)=>(

<li key={i}>{a}</li>

))}

</ul>

)}

</div>

)

}

export default Alerts