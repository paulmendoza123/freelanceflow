const BASE_URL = 'http://127.0.0.1:8000/api';

// Save & get token from localStorage
const getToken     = () => localStorage.getItem('access_token');
const saveToken    = (token) => localStorage.setItem('access_token', token);
const saveRefresh  = (token) => localStorage.setItem('refresh_token', token);
const getRefresh   = () => localStorage.getItem('refresh_token');
const logout       = () => { localStorage.clear(); window.location.href = '/'; }; // ✅ Fixed


async function apiRequest(endpoint, method = 'GET', body = null) {
    const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${getToken()}`
    };
    const config = { method, headers };
    if (body) config.body = JSON.stringify(body);

    let response = await fetch(`${BASE_URL}${endpoint}`, config);


    if (response.status === 401) {
        const refreshToken = getRefresh();
        if (refreshToken) {
            const refreshRes = await fetch(`${BASE_URL}/auth/refresh/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ refresh: refreshToken })
            });

            if (refreshRes.ok) {
                const data = await refreshRes.json();
                saveToken(data.access);
                // Retry original request with new token
                config.headers['Authorization'] = `Bearer ${data.access}`;
                response = await fetch(`${BASE_URL}${endpoint}`, config);
            } else {
                logout(); // Refresh failed — send to login
                return;
            }
        } else {
            logout(); // No refresh token — send to login
            return;
        }
    }

    return response.json();
}

// Auth
async function login(username, password) {
    const res = await fetch(`${BASE_URL}/auth/login/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });
    const data = await res.json();
    if (data.access) {
        saveToken(data.access);      // ✅ Save access token
        saveRefresh(data.refresh);   // ✅ Save refresh token
    }
    return data;
}

// Clients
const getClients    = ()         => apiRequest('/clients/');
const createClient  = (data)     => apiRequest('/clients/', 'POST', data);
const updateClient  = (id, data) => apiRequest(`/clients/${id}/`, 'PUT', data);
const deleteClient  = (id)       => apiRequest(`/clients/${id}/`, 'DELETE');

// Projects
const getProjects   = ()         => apiRequest('/projects/');
const createProject = (data)     => apiRequest('/projects/', 'POST', data);
const updateProject = (id, data) => apiRequest(`/projects/${id}/`, 'PUT', data);
const deleteProject = (id)       => apiRequest(`/projects/${id}/`, 'DELETE');

// Invoices
const getInvoices   = ()         => apiRequest('/invoices/');
const createInvoice = (data)     => apiRequest('/invoices/', 'POST', data);
const updateInvoice = (id, data) => apiRequest(`/invoices/${id}/`, 'PUT', data);
const deleteInvoice = (id)       => apiRequest(`/invoices/${id}/`, 'DELETE');

// Timelogs
const getTimeLogs   = ()         => apiRequest('/timelogs/');
const createTimeLog = (data)     => apiRequest('/timelogs/', 'POST', data);
const deleteTimeLog = (id)       => apiRequest(`/timelogs/${id}/`, 'DELETE');