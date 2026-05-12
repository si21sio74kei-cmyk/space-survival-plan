// API通信模块 - 负责与后端Flask通信
// Vercel部署时使用相对路径
const API_BASE = '/api';

async function fetchSurvivalStatus() {
    try {
        console.log('Fetching from:', `${API_BASE}/survival-status`);
        const response = await fetch(`${API_BASE}/survival-status`);
        console.log('Response status:', response.status);
        const data = await response.json();
        console.log('Received data:', data);
        return data;
    } catch (error) {
        console.error('Failed to fetch survival status:', error);
        return null;
    }
}

async function fetchFoodSystem() {
    try {
        const response = await fetch(`${API_BASE}/food-inventory`);
        return await response.json();
    } catch (error) {
        console.error('Failed to fetch food system:', error);
        return null;
    }
}

async function fetchMedicalSystem() {
    try {
        const response = await fetch(`${API_BASE}/medical-status`);
        return await response.json();
    } catch (error) {
        console.error('Failed to fetch medical system:', error);
        return null;
    }
}

async function fetchEnvironment() {
    try {
        const response = await fetch(`${API_BASE}/environment-status`);
        return await response.json();
    } catch (error) {
        console.error('Failed to fetch environment:', error);
        return null;
    }
}

async function fetchEnergy() {
    try {
        const response = await fetch(`${API_BASE}/energy-status`);
        return await response.json();
    } catch (error) {
        console.error('Failed to fetch energy:', error);
        return null;
    }
}

async function fetchAILogs() {
    try {
        const response = await fetch(`${API_BASE}/ai-logs`);
        return await response.json();
    } catch (error) {
        console.error('Failed to fetch AI logs:', error);
        return [];
    }
}

async function triggerAIAnalysis() {
    try {
        const response = await fetch(`${API_BASE}/generate-report`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ type: 'daily' })
        });
        return await response.json();
    } catch (error) {
        console.error('Failed to trigger AI analysis:', error);
        return null;
    }
}
