import React, {useState} from "react";
import { failureAPI } from "../api/api";

function Failure(){

  const [result,setResult] = useState("");

  const predict = async () => {

    const res = await failureAPI.get("/predict");

    setResult(res.data);
  };

  return(
    <div>

      <h2>EV Failure Prediction</h2>

      <button onClick={predict}>Predict</button>

      <pre>{JSON.stringify(result,null,2)}</pre>

    </div>
  )
}

export default Failure;
