import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000'; // Backend URL

export const initializeGrid = async (playerName: string, gridConfig: object) => {
  const response = await axios.post(`${API_BASE_URL}/initialize-grid/${playerName}`, gridConfig);
  return response.data;
};

export const fireShot = async (playerName: string, coord: [number, number]) => {
  const response = await axios.post(`${API_BASE_URL}/fire-shot/${playerName}`, { coord });
  return response.data;
};

export const checkWin = async (playerName: string) => {
  const response = await axios.get(`${API_BASE_URL}/check-win/${playerName}`);
  return response.data;
};

export const nextTurn = async () => {
  const response = await axios.post(`${API_BASE_URL}/next-turn`);
  return response.data;
};
