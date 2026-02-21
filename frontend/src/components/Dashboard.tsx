import React, { useEffect, useState } from 'react';
import { getSensorData, getLatestSensorData, getExternalWeather } from '../api';
import type { SensorData, WeatherData } from '../api';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { format } from 'date-fns';
import { AlertTriangle, Droplets, Thermometer, FlaskConical, History, CloudSun, CloudRain, Wind } from 'lucide-react';

const Dashboard: React.FC = () => {
    const [data, setData] = useState<SensorData[]>([]);
    const [latest, setLatest] = useState<SensorData | null>(null);
    const [weather, setWeather] = useState<WeatherData | null>(null);
    const [lastUpdated, setLastUpdated] = useState<Date>(new Date());
    const [error, setError] = useState<string | null>(null);
    const [anomalies, setAnomalies] = useState<string[]>([]);
    const [loading, setLoading] = useState<boolean>(true);

    const checkAnomalies = (sensorDisplay: SensorData) => {
        const issues: string[] = [];
        if (sensorDisplay.temperatura > 40 || sensorDisplay.temperatura < 0) {
            issues.push(`Temperatura crítica: ${sensorDisplay.temperatura.toFixed(1)}°C`);
        }
        if (sensorDisplay.ph < 4 || sensorDisplay.ph > 9) {
            issues.push(`pH inestable: ${sensorDisplay.ph.toFixed(1)}`);
        }
        if (sensorDisplay.humedad < 20 || sensorDisplay.humedad > 90) {
            issues.push(`Humedad fuera de rango: ${sensorDisplay.humedad.toFixed(1)}%`);
        }

        const dataTime = new Date(sensorDisplay.fecha).getTime();
        const now = new Date().getTime();
        if (now - dataTime > 300000) {
            const diffMinutes = ((now - dataTime) / 60000).toFixed(0);
            issues.push(`Datos desactualizados: Último registro hace ${diffMinutes} min`);
        }

        setAnomalies(issues);
    };

    const fetchWeather = async () => {
        try {
            console.log("Fetching weather...");
            const wData = await getExternalWeather();
            console.log("Weather data received:", wData);

            if (wData && wData.length > 0) {
                // Get the last item (most recent day available)
                const lastDay = wData[wData.length - 1];
                setWeather(lastDay);
            } else {
                console.warn("No weather data available or empty array.");
            }
        } catch (e) {
            console.error("Failed to fetch weather:", e);
        }
    }

    const fetchData = async () => {
        try {
            const history = await getSensorData(0, 50);
            const sortedHistory = [...history].reverse();
            setData(sortedHistory);

            const current = await getLatestSensorData();
            if (current) {
                setLatest(current);
                setLastUpdated(new Date());
                checkAnomalies(current);
                setError(null);
            } else {
                setLatest(null);
            }
        } catch (err) {
            console.error(err);
            setError("Error de conexión. Reintentando...");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
        fetchWeather();
        const interval = setInterval(fetchData, 2000);
        return () => clearInterval(interval);
    }, []);

    if (loading && !latest) return <div className="card">Cargando monitor de vermicompost...</div>;

    const tableData = [...data].reverse();

    return (
        <div className="dashboard">
            {error && (
                <div className="alert">
                    <AlertTriangle size={20} />
                    <span>{error}</span>
                </div>
            )}

            {anomalies.map((issue, idx) => (
                <div key={idx} className="alert">
                    <AlertTriangle size={20} />
                    <span>{issue}</span>
                </div>
            ))}

            <div className="grid-container">
                <div className="card">
                    <div className="stat-header">
                        <Thermometer size={24} color="#ff6b6b" />
                        <span className="stat-label">Temperatura</span>
                    </div>
                    <div className="stat-value">{latest ? latest.temperatura.toFixed(1) : '--'} °C</div>
                </div>
                <div className="card">
                    <div className="stat-header">
                        <Droplets size={24} color="#4dabf7" />
                        <span className="stat-label">Humedad</span>
                    </div>
                    <div className="stat-value">{latest ? latest.humedad.toFixed(1) : '--'} %</div>
                </div>
                <div className="card">
                    <div className="stat-header">
                        <FlaskConical size={24} color="#69db7c" />
                        <span className="stat-label">pH</span>
                    </div>
                    <div className="stat-value">{latest ? latest.ph.toFixed(2) : '--'}</div>
                </div>
            </div>

            {/* Weather Widget Force Render Check */}
            <div className="card weather-card-bg" style={{ marginBottom: '1rem', marginTop: '1rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '15px' }}>
                    <h3 style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '10px', fontSize: '1.1rem', color: '#f1f1f1' }}>
                        <CloudSun color="#f1c40f" size={24} />
                        Clima Exterior (KM 18)
                    </h3>
                    <span style={{ fontSize: '0.9rem', color: '#aaa' }}>
                        {weather ? format(new Date(weather.date), 'dd/MM/yyyy') : 'Cargando...'}
                    </span>
                </div>

                {weather ? (
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '10px', textAlign: 'center' }}>
                        <div>
                            <span style={{ display: 'block', color: '#aaa', fontSize: '0.8rem', marginBottom: '4px' }}>Promedio</span>
                            <span style={{ fontSize: '1.4rem', fontWeight: 'bold', color: '#fff' }}>{weather.tavg != null ? weather.tavg.toFixed(1) : '--'} °C</span>
                        </div>
                        <div>
                            <span style={{ display: 'block', color: '#aaa', fontSize: '0.8rem', marginBottom: '4px' }}>Precipitación</span>
                            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '6px' }}>
                                <CloudRain size={16} color="#4dabf7" />
                                <span style={{ fontSize: '1.4rem', fontWeight: 'bold', color: '#fff' }}>{weather.prcp != null ? weather.prcp : '0'} mm</span>
                            </div>
                        </div>
                        <div>
                            <span style={{ display: 'block', color: '#aaa', fontSize: '0.8rem', marginBottom: '4px' }}>Viento</span>
                            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '6px' }}>
                                <Wind size={16} color="#a5d8ff" />
                                <span style={{ fontSize: '1.4rem', fontWeight: 'bold', color: '#fff' }}>{weather.wspd != null ? weather.wspd : '--'} km/h</span>
                            </div>
                        </div>
                    </div>
                ) : (
                    <div style={{ textAlign: 'center', color: '#aaa', padding: '10px' }}>
                        Obteniendo datos del clima...
                    </div>
                )}
            </div>

            <div className="card" style={{ height: '400px' }}>
                <h3 style={{ marginBottom: '1rem', textAlign: 'left' }}>Histórico en Tiempo Real (Gráfica)</h3>
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={data} margin={{ top: 5, right: 20, left: 10, bottom: 5 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                        <XAxis
                            dataKey="fecha"
                            tickFormatter={(str) => {
                                try {
                                    return format(new Date(str), 'HH:mm:ss');
                                } catch { return ''; }
                            }}
                            stroke="#888"
                        />
                        <YAxis stroke="#888" domain={['auto', 'auto']} />
                        <Tooltip
                            contentStyle={{ backgroundColor: '#242424', border: '1px solid #444', color: '#fff' }}
                            labelFormatter={(label) => {
                                try {
                                    return format(new Date(label), 'dd/MM/yyyy HH:mm:ss');
                                } catch { return label; }
                            }}
                        />
                        <Legend />
                        <Line type="monotone" dataKey="temperatura" stroke="#ff6b6b" strokeWidth={3} dot={false} activeDot={{ r: 6 }} name="Temp" isAnimationActive={false} />
                        <Line type="monotone" dataKey="humedad" stroke="#4dabf7" strokeWidth={3} dot={false} name="Humedad" isAnimationActive={false} />
                        <Line type="monotone" dataKey="ph" stroke="#69db7c" strokeWidth={3} dot={false} name="pH" isAnimationActive={false} />
                    </LineChart>
                </ResponsiveContainer>
            </div>

            <div className="card">
                <div className="stat-header">
                    <History size={24} color="#aaa" />
                    <h3 style={{ margin: 0 }}>Registro de Datos (Últimos 50)</h3>
                </div>
                <div className="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Fecha / Hora</th>
                                <th>Temperatura (°C)</th>
                                <th>Humedad (%)</th>
                                <th>pH</th>
                            </tr>
                        </thead>
                        <tbody>
                            {tableData.map((row) => (
                                <tr key={row.id}>
                                    <td>
                                        {(() => {
                                            try {
                                                return format(new Date(row.fecha), 'dd/MM/yyyy HH:mm:ss');
                                            } catch {
                                                return row.fecha;
                                            }
                                        })()}
                                    </td>
                                    <td style={{ color: row.temperatura > 40 || row.temperatura < 0 ? '#ff6b6b' : 'inherit' }}>
                                        {row.temperatura.toFixed(2)}
                                    </td>
                                    <td style={{ color: row.humedad < 20 || row.humedad > 90 ? '#4dabf7' : 'inherit' }}>
                                        {row.humedad.toFixed(2)}
                                    </td>
                                    <td style={{ color: row.ph < 4 || row.ph > 9 ? '#69db7c' : 'inherit' }}>
                                        {row.ph.toFixed(2)}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>

            <p style={{ color: '#666', fontSize: '0.8rem', marginTop: '2rem' }}>
                Actualizando cada 2 segundos... Última sincronización: {format(lastUpdated, 'HH:mm:ss')}
            </p>
        </div>
    );
};

export default Dashboard;
