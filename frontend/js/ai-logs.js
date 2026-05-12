// 日志显示模块 - 负责AI日志和历史时间线的显示
const addAILog = (message, type = 'INFO') => {
    const logContainer = document.getElementById('ai-logs');
    const div = document.createElement('div');
    div.className = 'log-entry';
    
    // 根据日志类型设置不同样式
    if (message.startsWith('✓')) {
        div.style.color = '#00f3ff';
        div.style.fontWeight = 'bold';
    } else if (message.includes('警告') || message.includes('⚠️')) {
        div.style.color = '#ff9f43';
    } else if (message.includes('能源联动') || message.includes('辐射联动') || message.includes('食物联动')) {
        div.style.color = '#ff4d4d';
        div.style.borderLeft = '3px solid #ff4d4d';
        div.style.paddingLeft = '10px';
    } else if (type === 'CRITICAL') {
        div.style.color = '#ff4d4d';
        div.style.fontWeight = 'bold';
    } else if (type === 'WARNING') {
        div.style.color = '#ff9f43';
    }
    
    div.innerText = `> ${message}`;
    logContainer.prepend(div);
    
    // 限制日志数量
    if (logContainer.children.length > 15) {
        logContainer.removeChild(logContainer.lastChild);
    }
};

// 批量更新AI日志（从API返回的日志数组）
const updateAILogs = (logs) => {
    const logContainer = document.getElementById('ai-logs');
    if (!logContainer || !logs || logs.length === 0) return;
    
    // 清空现有日志
    logContainer.innerHTML = '';
    
    // 添加新日志（倒序，最新的在前）
    logs.slice(0, 15).forEach(log => {
        const div = document.createElement('div');
        div.className = 'log-entry';
        
        const message = log.message || log.ai_decision || '';
        const logType = log.log_type || 'INFO';
        
        // 根据日志类型设置不同样式
        if (message.startsWith('✓')) {
            div.style.color = '#00f3ff';
            div.style.fontWeight = 'bold';
        } else if (message.includes('警告') || message.includes('⚠️')) {
            div.style.color = '#ff9f43';
        } else if (message.includes('能源联动') || message.includes('辐射联动') || message.includes('食物联动')) {
            div.style.color = '#ff4d4d';
            div.style.borderLeft = '3px solid #ff4d4d';
            div.style.paddingLeft = '10px';
        } else if (logType === 'CRITICAL') {
            div.style.color = '#ff4d4d';
            div.style.fontWeight = 'bold';
        } else if (logType === 'WARNING') {
            div.style.color = '#ff9f43';
        }
        
        div.innerText = `> ${message}`;
        logContainer.appendChild(div);
    });
};

const addHistoryItem = (day, message) => {
    const historyList = document.getElementById('history-list');
    const historyItem = document.createElement('li');
    historyItem.innerText = `Day ${day}: ${message || 'System Check'}`;
    historyList.prepend(historyItem);
    
    // 限制历史记录数量
    if (historyList.children.length > 10) {
        historyList.removeChild(historyList.lastChild);
    }
};

const clearLogs = () => {
    const logContainer = document.getElementById('ai-logs');
    if (logContainer) {
        logContainer.innerHTML = '';
    }
    
    const historyList = document.getElementById('history-list');
    if (historyList) {
        historyList.innerHTML = '';
    }
};
