import axios from "axios";

export const failureAPI = axios.create({
  baseURL: "http://localhost:8003"
});

export const demandAPI = axios.create({
  baseURL: "http://localhost:8000"
});

export const adoptionAPI = axios.create({
  baseURL: "http://localhost:5000"
});