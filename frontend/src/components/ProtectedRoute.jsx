import {Navigate} from 'react-router-dom';
import {jwtDecode} from 'jwt-decode';
import api from '../api';
import { ACCESS_TOKEN, REFRESH_TOKEN } from '../constants';
import { useState, useEffect } from 'react';

function ProtectedRoute({children}) {
    const [isAuthored, setIsAuthored] = useState(null);


    useEffect(() => {
        auth().catch(() => setIsAuthored(false));
    }, []);

    const refreshToken = async () => {
        const refreshToken = localStorage.getItem(REFRESH_TOKEN);
        try {
            const res = await api.post('/api/token/refresh/', {
                refresh: refreshToken
            });
            if (res.status === 200) {
                localStorage.setItem(ACCESS_TOKEN, res.data.access);
                setIsAuthored(true);
            } else {
                setIsAuthored(false);
            }
        } catch (error) {
            console.log(error);
            setIsAuthored(false);
        }
    }

    const auth = async () => {
        const token = localStorage.getItem(ACCESS_TOKEN);
        if (!token) {
            setIsAuthored(false);
            return;
        }
        const decoded = jwtDecode(token);
        const tokenExpiration = decoded.exp;
        const now = Date.now() / 1000;

        if (tokenExpiration < now) {
            await refreshToken();
        } else {
            setIsAuthored(true);
        }
    }

    if (isAuthored === null) {
        return <div>Loading...</div>
    }
    return isAuthored ? children : <Navigate to="/login" />
}

export default ProtectedRoute;


