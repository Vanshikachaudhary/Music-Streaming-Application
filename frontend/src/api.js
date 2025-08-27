import axios from "axios";

const API_BASE = "/api"; // goes to gateway-service

export const getHealth = async () => {
  try {
    const response = await axios.get(`${API_BASE}/health`);
    return response.data;
  } catch (err) {
    return { status: "error" };
  }
};
