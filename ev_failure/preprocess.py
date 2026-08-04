# preprocess.py

import numpy as np

def prepare_input(data):
    return np.array([[ 
        data["SoC"],
        data["SoH"],
        data["Battery_Voltage"],
        data["Battery_Current"],
        data["Battery_Temperature"],
        data["Charge_Cycles"],
        data["Motor_Temperature"],
        data["Motor_Vibration"],
        data["Motor_Torque"],
        data["Motor_RPM"],
        data["Power_Consumption"],
        data["Brake_Pad_Wear"],
        data["Brake_Pressure"],
        data["Reg_Brake_Efficiency"],
        data["Tire_Pressure"],
        data["Tire_Temperature"],
        data["Suspension_Load"],
        data["Ambient_Temperature"],
        data["Ambient_Humidity"],
        data["Load_Weight"],
        data["Driving_Speed"],
        data["Distance_Traveled"],
        data["Idle_Time"],
        data["Route_Roughness"],
        data["Component_Health_Score"]
    ]])