import axios from 'axios';

const serviceAPI = axios.create({
  baseURL: "http://localhost:8000/",
});

serviceAPI.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) config.headers.Authorization = `Bearer ${token}`;

  return config;
});

export default serviceAPI;
