import axios from 'axios';

const API_URL = 'http://localhost:8000';

export interface SensorData {
    id: number;
    fecha: string;
    temperatura: number;
    humedad: number;
    ph: number;
}

export interface WeatherData {
    date: string;
    tavg: number;
    tmin: number;
    tmax: number;
    prcp: number;
    wdir: number;
    wspd: number;
    pres: number;
}

export const getSensorData = async (skip = 0, limit = 50): Promise<SensorData[]> => {
    const response = await axios.get(`${API_URL}/data/?skip=${skip}&limit=${limit}`);
    return response.data;
};

export const getLatestSensorData = async (): Promise<SensorData | null> => {
    const response = await axios.get(`${API_URL}/data/latest`);
    return response.data;
};

export const getExternalWeather = async (): Promise<WeatherData[] | null> => {
    try {
        const response = await axios.get(`${API_URL}/weather`);
        return response.data;
    } catch (error) {
        console.error("Error fetching weather:", error);
        return null;
    }
};
