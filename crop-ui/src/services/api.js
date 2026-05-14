import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000",
});

export const predictCrop = async (formData) => {
    const response = await API.post("/recommend", formData);
  return response.data;
};