// API通信模块 - 负责与后端FastAPI通信
const API_BASE = 'http://localhost:8001/api';

async function fetchSurvivalStatus() {
    try {
        const response = await fetch(`${API_BASE}/survival-status`);
        return await response.json();
    } catch (error) {
        console.error('Failed to fetch survival status:', error);
        return null;
    }
}

async function fetchFoodSystem() {
    try {
        const response = await fetch(`${API_BASE}/food-system`);
        return await response.json();
    } catch (error) {
        console.error('Failed to fetch food system:', error);
        return null;
    }
}

async function fetchMedicalSystem() {
    try {
        const response = await fetch(`${API_BASE}/medical-system`);
        return await response.json();
    } catch (error) {
        console.error('Failed to fetch medical system:', error);
        return null;
    }
}

async function fetchEnvironment() {
    try {
        const response = await fetch(`${API_BASE}/environment`);
        return await response.json();
    } catch (error) {
        console.error('Failed to fetch environment:', error);
        return null;
    }
}

async function fetchEnergy() {
    try {
        const response = await fetch(`${API_BASE}/energy`);
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
        const response = await fetch(`${API_BASE}/ai-analysis`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        return await response.json();
    } catch (error) {
        console.error('Failed to trigger AI analysis:', error);
        return null;
    }
}
