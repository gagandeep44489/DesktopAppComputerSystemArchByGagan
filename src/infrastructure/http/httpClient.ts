import axios from 'axios';
export const httpClient = axios.create({ baseURL: import.meta.env.VITE_API_BASE_URL ?? '/', timeout: 10000 });
httpClient.interceptors.response.use((response) => response, (error: unknown) => Promise.reject(error));
