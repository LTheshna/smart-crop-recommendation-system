import axios from "axios";

const API = axios.create({
  baseURL: "https://smart-crop-backend-l8p2.onrender.com",
});

export const predictCrop = async (formData) => {
    const response = await API.post("/recommend", formData);
  return response.data;
};