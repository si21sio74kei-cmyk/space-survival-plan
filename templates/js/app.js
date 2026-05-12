// 主入口模块 - 负责系统初始化和自动刷新
let currentModule = 'dashboard';
let refreshInterval = null;

// 初始化系统
async function init() {
    console.log('Initializing DeepSpace AI Survival System...');
    
    // 1. 初始化星空背景
    initStarfield();
    
    // 2. 初始化图表
    const charts = initCharts();
    
    // 3. 设置导航栏交互
    setupNavigation();
    
    // 4. 设置滑块输入监听
    setupSliderInputs();
    
    // 5. 启动自动刷新（每3秒）
    startAutoRefresh(charts);
    
    // 6. 立即执行一次数据刷新
    await refreshData(charts);
    
    console.log('System initialized successfully.');
}

// 设置导航栏交互
function setupNavigation() {
    const navItems = document.querySelectorAll('.sidebar li');
    
    navItems.forEach((item, index) => {
        item.addEventListener('click', function() {
            // 移除所有active状态
            navItems.forEach(n => n.classList.remove('active'));
            this.classList.add('active');
            
            const text = this.innerText.trim();
            let module;
            if (text.includes('食物')) module = 'food';
            else if (text.includes('医疗')) module = 'medical';
            else if (text.includes('能源')) module = 'energy';
            else if (text.includes('环境')) module = 'env';
            else if (text.includes('紧急')) module = 'emergency';
            else if (text.includes('时间线')) module = 'timeline';
            else if (text.includes('AI核心')) module = 'ai';
            else if (text.includes('自定义')) module = 'custom';
            else module = 'dashboard';
            
            currentModule = module;
            
            // 切换视图（淡入淡出效果）
            switchView(module);
        });
    });
}

// 视图切换函数
function switchView(module) {
    // 隐藏所有视图
    document.querySelectorAll('.view-panel').forEach(view => {
        view.style.transition = 'opacity 0.3s ease';
        view.style.opacity = '0';
        setTimeout(() => {
            view.style.display = 'none';
        }, 300);
    });
    
    // 显示目标视图
    setTimeout(() => {
        const targetView = document.getElementById(`view-${module}`);
        if (targetView) {
            targetView.style.display = 'block';
            // 强制重绘
            targetView.offsetHeight;
            setTimeout(() => {
                targetView.style.opacity = '1';
            }, 50);
        }
    }, 300);
}

// 设置滑块输入监听
function setupSliderInputs() {
    const sliders = ['food', 'energy', 'medical', 'oxygen'];
    sliders.forEach(id => {
        const slider = document.getElementById(`input-${id}`);
        const display = document.getElementById(`val-${id}`);
        if (slider && display) {
            slider.addEventListener('input', (e) => {
                display.textContent = e.target.value + '%';
            });
        }
    });
}

// 应用自定义输入
async function applyCustomInput() {
    const food = document.getElementById('input-food').value;
    const energy = document.getElementById('input-energy').value;
    const medical = document.getElementById('input-medical').value;
    const oxygen = document.getElementById('input-oxygen').value;
    
    try {
        const response = await fetch('/api/adjust-parameters', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                food_stability: parseFloat(food),
                energy_level: parseFloat(energy),
                medical_safety: parseFloat(medical),
                oxygen_level: parseFloat(oxygen)
            })
        });
        
        const result = await response.json();
        if (result.success) {
            showToast('✅ 参数已更新！');
            // 立即刷新数据
            refreshData({ mainChart, gaugeChart, predictionChart });
        }
    } catch (error) {
        console.error('Failed to apply custom input:', error);
        showToast('❌ 更新失败，请重试');
    }
}

// 重置为默认值
function resetToDefault() {
    document.getElementById('input-food').value = 80;
    document.getElementById('val-food').textContent = '80%';
    document.getElementById('input-energy').value = 70;
    document.getElementById('val-energy').textContent = '70%';
    document.getElementById('input-medical').value = 90;
    document.getElementById('val-medical').textContent = '90%';
    document.getElementById('input-oxygen').value = 95;
    document.getElementById('val-oxygen').textContent = '95%';
    showToast('🔄 已重置为默认值');
}
function startAutoRefresh(charts) {
    refreshInterval = setInterval(() => refreshData(charts), 3000);
    console.log('Auto-refresh started (interval: 3s)');
}

// 停止自动刷新
function stopAutoRefresh() {
    if (refreshInterval) {
        clearInterval(refreshInterval);
        refreshInterval = null;
        console.log('Auto-refresh stopped.');
    }
}

// 显示调整表单
function showAdjustmentForm(module) {
    const formContainer = document.getElementById('adjustment-form');
    formContainer.innerHTML = '';
    
    const fields = {
        food: [
            { key: 'food_stability', label: '食物稳定性', min: 0, max: 100, step: 1 },
            { key: 'water_reserve', label: '水资源储备', min: 0, max: 100, step: 1 },
            { key: 'protein_level', label: '蛋白质水平', min: 0, max: 100, step: 1 }
        ],
        medical: [
            { key: 'medical_safety', label: '医疗安全性', min: 0, max: 100, step: 1 },
            { key: 'medical_temp', label: '冷链温度 (°C)', min: -100, max: 0, step: 1 }
        ],
        energy: [
            { key: 'energy_level', label: '能源水平', min: 0, max: 100, step: 1 },
            { key: 'backup_power_hours', label: '备用电源 (小时)', min: 0, max: 200, step: 1 }
        ],
        env: [
            { key: 'oxygen_level', label: '氧气水平', min: 0, max: 100, step: 1 },
            { key: 'humidity', label: '湿度 (%)', min: 0, max: 100, step: 1 },
            { key: 'pressure', label: '气压 (kPa)', min: 80, max: 120, step: 0.1 }
        ]
    };
    
    const moduleFields = fields[module] || [];
    moduleFields.forEach(field => {
        const div = document.createElement('div');
        div.innerHTML = `
            <label style="color: var(--tech-cyan); font-size: 12px; display: block; margin-bottom: 5px;">${field.label}</label>
            <input type="range" min="${field.min}" max="${field.max}" step="${field.step}" 
                   id="adjust-${field.key}" 
                   style="width: 100%; accent-color: var(--tech-cyan);">
            <span id="value-${field.key}" style="color: #fff; font-size: 12px;">
                ${field.key === 'pressure' ? '101.3' : field.max / 2}
            </span>
        `;
        formContainer.appendChild(div);
        
        // 添加滑块事件监听
        const slider = document.getElementById(`adjust-${field.key}`);
        const valueDisplay = document.getElementById(`value-${field.key}`);
        slider.addEventListener('input', (e) => {
            valueDisplay.textContent = e.target.value;
        });
    });
}

// 应用手动调整
async function applyAdjustments() {
    const inputs = document.querySelectorAll('#adjustment-form input[type="range"]');
    const adjustments = {};
    
    inputs.forEach(input => {
        const key = input.id.replace('adjust-', '');
        adjustments[key] = parseFloat(input.value);
    });
    
    try {
        const response = await fetch('/api/adjust-parameters', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(adjustments)
        });
        
        const result = await response.json();
        if (result.success) {
            // 显示成功提示
            showToast('✅ 参数调整已应用！');
            // 立即刷新数据
            refreshData({ mainChart, gaugeChart, predictionChart });
        }
    } catch (error) {
        console.error('Failed to apply adjustments:', error);
        showToast('❌ 调整失败，请重试');
    }
}

// 发送AI对话
async function sendToAI() {
    const input = document.getElementById('ai-user-input');
    const chatContainer = document.getElementById('ai-chat-container');
    const query = input.value.trim();
    
    if (!query) {
        showToast('⚠️ 请输入您的问题');
        return;
    }
    
    // 添加用户消息
    const userMessage = document.createElement('div');
    userMessage.className = 'user-message';
    userMessage.style.cssText = 'margin-bottom: 15px; text-align: right;';
    userMessage.innerHTML = `
        <div style="color: #fff; font-weight: bold; margin-bottom: 5px;">
            <i class="fas fa-user"></i> You
        </div>
        <div style="color: #000; padding: 10px; background: rgba(0,243,255,0.8); border-radius: 5px; display: inline-block; max-width: 80%;">
            ${query}
        </div>
    `;
    chatContainer.appendChild(userMessage);
    
    // 滚动到底部
    chatContainer.scrollTop = chatContainer.scrollHeight;
    
    // 显示AI正在思考
    const thinkingMessage = document.createElement('div');
    thinkingMessage.className = 'ai-message';
    thinkingMessage.id = 'ai-thinking';
    thinkingMessage.style.cssText = 'margin-bottom: 15px;';
    thinkingMessage.innerHTML = `
        <div style="color: var(--tech-cyan); font-weight: bold; margin-bottom: 5px;">
            <i class="fas fa-robot"></i> AI Assistant
        </div>
        <div style="color: #fff; padding: 10px; background: rgba(0,243,255,0.1); border-radius: 5px;">
            ⏳ 正在分析...
        </div>
    `;
    chatContainer.appendChild(thinkingMessage);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    
    try {
        const response = await fetch('/api/generate-report', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                type: 'query',
                query: query 
            })
        });
        
        const result = await response.json();
        
        // 移除思考消息
        document.getElementById('ai-thinking').remove();
        
        // 添加AI回复
        const aiMessage = document.createElement('div');
        aiMessage.className = 'ai-message';
        aiMessage.style.cssText = 'margin-bottom: 15px;';
        aiMessage.innerHTML = `
            <div style="color: var(--tech-cyan); font-weight: bold; margin-bottom: 5px;">
                <i class="fas fa-robot"></i> AI Assistant
            </div>
            <div style="color: #fff; padding: 10px; background: rgba(0,243,255,0.1); border-radius: 5px; white-space: pre-wrap;">
                ${result.report || '抱歉，我暂时无法回答这个问题。'}
            </div>
        `;
        chatContainer.appendChild(aiMessage);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    } catch (error) {
        console.error('Failed to send query:', error);
        document.getElementById('ai-thinking').remove();
        
        const errorMessage = document.createElement('div');
        errorMessage.className = 'ai-message';
        errorMessage.style.cssText = 'margin-bottom: 15px;';
        errorMessage.innerHTML = `
            <div style="color: var(--tech-cyan); font-weight: bold; margin-bottom: 5px;">
                <i class="fas fa-robot"></i> AI Assistant
            </div>
            <div style="color: #ff4d4d; padding: 10px; background: rgba(255,77,77,0.1); border-radius: 5px;">
                ❌ AI响应失败，请重试
            </div>
        `;
        chatContainer.appendChild(errorMessage);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
    
    input.value = '';
}

// 触发AI分析
async function triggerAnalysis() {
    const responseDiv = document.getElementById('ai-response');
    responseDiv.style.display = 'block';
    responseDiv.innerHTML = '<p style="color: var(--tech-cyan);">⏳ 生成日报中...</p>';
    
    try {
        const result = await triggerAIAnalysis();
        if (result && result.report) {
            responseDiv.innerHTML = `
                <div style="color: var(--tech-cyan); margin-bottom: 10px;">
                    <i class="fas fa-file-alt"></i> 每日分析报告：
                </div>
                <div style="white-space: pre-wrap;">${result.report}</div>
            `;
        }
    } catch (error) {
        console.error('Failed to trigger analysis:', error);
        responseDiv.innerHTML = '<p style="color: #ff4d4d;">❌ 分析生成失败，请重试</p>';
    }
}

// 显示提示消息
function showToast(message) {
    const toast = document.createElement('div');
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 25px;
        background: rgba(0, 243, 255, 0.9);
        color: #000;
        border-radius: 5px;
        font-weight: bold;
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 2000);
}

// 刷新数据（核心函数）
async function refreshData(charts) {
    try {
        // 并行获取所有API数据
        const [survivalStatus, foodSystem, medicalSystem, environment, energy, aiLogs] = await Promise.all([
            fetchSurvivalStatus(),
            fetchFoodSystem(),
            fetchMedicalSystem(),
            fetchEnvironment(),
            fetchEnergy(),
            fetchAILogs()
        ]);
        
        if (!survivalStatus) {
            console.error('Failed to fetch survival status');
            return;
        }
        
        // 1. 更新紧急协议模式
        if (survivalStatus.emergency_mode) {
            triggerEmergencyAnimation();
        } else {
            exitEmergencyAnimation();
        }
        
        // 2. 更新仪表盘数据
        updateDashboardView(survivalStatus);
        
        // 3. 更新生存指数仪表盘
        if (gaugeChart) {
            gaugeChart.setOption({
                series: [{
                    data: [{ value: Math.round(survivalStatus.survival_index) }]
                }]
            });
        }
        
        // 4. 更新顶部状态栏
        document.getElementById('crew-display').innerText = survivalStatus.crew_count;
        document.getElementById('stability-display').innerText = Math.round(survivalStatus.survival_index) + '%';
        document.getElementById('day-display').innerText = String(survivalStatus.mission_day).padStart(3, '0');
        
        // 5. 更新预计生存时间（带动画）
        const survivalTimeEl = document.getElementById('est-survival-days');
        if (survivalTimeEl && survivalStatus.estimated_survival_days) {
            animateNumberWithSuffix(survivalTimeEl, survivalStatus.estimated_survival_days, ' DAYS');
        }
        
        // 6. 更新预测时间线
        if (predictionChart && survivalStatus.predictions) {
            predictionChart.setOption({
                xAxis: { data: ['D+30', 'D+60', 'D+90', 'D+120'] },
                series: [{ data: survivalStatus.predictions }]
            });
        }
        
        // 7. 根据当前模块更新对应图表
        if (currentModule === 'food' && foodSystem) {
            updateFoodView(foodSystem);
        } else if (currentModule === 'medical' && medicalSystem) {
            updateMedicalView(medicalSystem);
        } else if (currentModule === 'energy' && energy) {
            updateEnergyView(energy);
        } else if (currentModule === 'env' && environment) {
            updateEnvView(environment);
        }
        
        // 8. 更新AI日志
        if (aiLogs && aiLogs.length > 0) {
            updateAILogs(aiLogs);
        }
        
    } catch (error) {
        console.error('Error refreshing data:', error);
    }
}

// 页面加载完成后初始化
window.onload = () => {
    init();
};
