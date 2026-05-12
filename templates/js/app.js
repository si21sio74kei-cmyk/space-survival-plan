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
    
    // 4. 启动自动刷新（每3秒）
    startAutoRefresh(charts);
    
    // 5. 立即执行一次数据刷新
    await refreshData(charts);
    
    console.log('System initialized successfully.');
}

// 设置导航栏交互
function setupNavigation() {
    const navItems = document.querySelectorAll('.sidebar li');
    navItems.forEach(item => {
        item.addEventListener('click', function() {
            navItems.forEach(n => n.classList.remove('active'));
            this.classList.add('active');
            
            const text = this.innerText.trim();
            if (text.includes('食物')) currentModule = 'food';
            else if (text.includes('医疗')) currentModule = 'medical';
            else if (text.includes('能源')) currentModule = 'energy';
            else if (text.includes('环境')) currentModule = 'env';
            else currentModule = 'dashboard';
            
            // 立即刷新当前模块视图
            refreshData({ mainChart, gaugeChart, predictionChart });
        });
    });
}

// 启动自动刷新
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
