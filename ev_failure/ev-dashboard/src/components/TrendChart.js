import React from "react"
import {BarChart,Bar,XAxis,YAxis,Tooltip,CartesianGrid} from "recharts"

function TrendChart({trends}){

const data = Object.keys(trends).map(key=>({

name:key,
value:trends[key]

}))

return(

<div style={{marginTop:"40px"}}>

<h2>📈 Vehicle Trend Summary</h2>

<BarChart width={500} height={300} data={data}>

<CartesianGrid strokeDasharray="3 3" />

<XAxis dataKey="name" />

<YAxis />

<Tooltip />

<Bar dataKey="value" />

</BarChart>

</div>

)

}

export default TrendChart