// 主入口模块 - 负责系统初始化和自动刷新
let currentModule = 'dashboard';
let refreshInterval = null;
let simulationTimer = null; // 模拟定时器

// ==================== localStorage状态管理 ====================
function saveStateToLocalStorage(state) {
    try {
        localStorage.setItem('spaceSurvivalState', JSON.stringify(state));
        console.log('State saved to localStorage');
    } catch (e) {
        console.error('Failed to save state:', e);
    }
}

function loadStateFromLocalStorage() {
    try {
        const saved = localStorage.getItem('spaceSurvivalState');
        return saved ? JSON.parse(saved) : null;
    } catch (e) {
        console.error('Failed to load state:', e);
        return null;
    }
}

function clearStateFromLocalStorage() {
    localStorage.removeItem('spaceSurvivalState');
}

// 初始化系统
async function init() {
    console.log('Initializing DeepSpace AI Survival System...');
    
    // 1. 初始化星空背景
    initStarfield();
    
    // 2. 初始化图表
    const charts = initCharts();
    // 将charts存储到window对象，供其他函数使用
    window.charts = charts;
    
    // 3. 设置导航栏交互
    setupNavigation();
    
    // 4. 设置滑块输入监听
    setupSliderInputs();
    
    // 5. 启动自动刷新（每10秒，降低频率以减少API调用）
    startAutoRefresh(charts);
    
    // 6. 启动模拟定时器（每分钟+1天）
    startSimulation();
    
    // 7. 立即执行一次数据刷新
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
            else if (text.includes('宇航员')) module = 'crew';
            else if (text.includes('AI预测')) module = 'ai-predict';
            else if (text.includes('通信')) module = 'communication';
            else if (text.includes('设置')) module = 'settings';
            else if (text.includes('AI对话')) module = 'ai';
            else if (text.includes('参数')) module = 'custom';
            else module = 'dashboard';
            
            currentModule = module;
            
            // 切换视图（淡入淡出效果）
            switchView(module);
        });
    });
}

// 视图切换函数
async function switchView(module) {
    // 隐藏所有视图
    document.querySelectorAll('.view-panel').forEach(view => {
        view.style.transition = 'opacity 0.3s ease';
        view.style.opacity = '0';
        setTimeout(() => {
            view.style.display = 'none';
        }, 300);
    });
    
    // 显示目标视图
    setTimeout(async () => {
        const targetView = document.getElementById(`view-${module}`);
        if (targetView) {
            targetView.style.display = 'block';
            // 强制重绘
            targetView.offsetHeight;
            setTimeout(() => {
                targetView.style.opacity = '1';
            }, 50);
            
            // 等待模块内容加载完成
            await loadModuleContent(module);
            
            // 内容加载完成后立即刷新数据以更新图表
            if (window.charts) {
                await refreshData(window.charts);
            }
        }
    }, 300);
}

// 加载模块内容
async function loadModuleContent(module) {
    switch(module) {
        case 'food':
            await loadFoodModule();
            break;
        case 'medical':
            await loadMedicalModule();
            break;
        case 'energy':
            await loadEnergyModule();
            break;
        case 'env':
            await loadEnvModule();
            break;
        case 'emergency':
            await loadEmergencyModule();
            break;
        case 'crew':
            await loadCrewModule();
            break;
        case 'ai-predict':
            await loadAIPredictModule();
            break;
        case 'communication':
            await loadCommunicationModule();
            break;
        case 'settings':
            await loadSettingsModule();
            break;
    }
}

// 食物资源模块
async function loadFoodModule() {
    const container = document.getElementById('food-content');
    container.innerHTML = `
        <div style="background: rgba(0,0,0,0.3); padding: 20px; border-radius: 8px; margin-bottom: 20px;">
            <h3 style="color: var(--tech-cyan); margin-bottom: 15px;">
                <i class="fas fa-plus-circle"></i> 添加食物
            </h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                <input type="text" id="food-name" placeholder="食物名称" style="padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                <input type="number" id="food-quantity" placeholder="数量" min="0" step="0.1" style="padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                <input type="date" id="food-expiry" placeholder="保质期" style="padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                <select id="food-nutrition" style="padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                    <option value="protein">蛋白质</option>
                    <option value="carb">碳水化合物</option>
                    <option value="fat">脂肪</option>
                    <option value="vitamin">维生素</option>
                </select>
                <button onclick="addFoodItem()" style="padding: 10px 20px; background: var(--tech-cyan); color: #000; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">
                    <i class="fas fa-plus"></i> 添加
                </button>
            </div>
        </div>
        
        <div style="background: rgba(0,0,0,0.3); padding: 20px; border-radius: 8px; margin-bottom: 20px;">
            <h3 style="color: var(--tech-cyan); margin-bottom: 15px;">
                <i class="fas fa-sliders-h"></i> 消耗控制
            </h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                <div>
                    <label style="color: #fff; font-size: 12px;">每日消耗速率</label>
                    <input type="range" id="food-consumption-rate" min="0.1" max="5" step="0.1" value="1" oninput="document.getElementById('val-consumption').textContent=this.value" style="width: 100%; accent-color: var(--tech-cyan);">
                    <span id="val-consumption" style="color: var(--tech-cyan);">1</span>
                </div>
                <select id="food-activity-level" style="padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                    <option value="low">低活动量</option>
                    <option value="normal" selected>正常活动</option>
                    <option value="high">高活动量</option>
                </select>
                <button onclick="updateConsumptionRate()" style="padding: 10px 20px; background: var(--tech-cyan); color: #000; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">
                    <i class="fas fa-check"></i> 应用
                </button>
            </div>
        </div>
        
        <div style="background: rgba(0,0,0,0.3); padding: 20px; border-radius: 8px; margin-bottom: 20px;">
            <h3 style="color: var(--tech-cyan); margin-bottom: 15px;">
                <i class="fas fa-exclamation-circle"></i> 紧急配给模式
            </h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                <label style="display: flex; align-items: center; color: #fff; cursor: pointer;">
                    <input type="checkbox" id="food-emergency-mode" style="margin-right: 10px; width: 20px; height: 20px; accent-color: var(--tech-cyan);">
                    启用紧急配给
                </label>
                <div>
                    <label style="color: #fff; font-size: 12px;">配给百分比 (%)</label>
                    <input type="range" id="food-ration-percent" min="10" max="100" value="100" oninput="document.getElementById('val-ration').textContent=this.value+'%'" style="width: 100%; accent-color: var(--tech-cyan);">
                    <span id="val-ration" style="color: var(--tech-cyan);">100%</span>
                </div>
                <button onclick="toggleEmergencyRation()" style="padding: 10px 20px; background: #ff9500; color: #000; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">
                    <i class="fas fa-toggle-on"></i> 切换模式
                </button>
            </div>
        </div>
        
        <div style="background: rgba(0,0,0,0.3); padding: 20px; border-radius: 8px; margin-bottom: 20px;">
            <h3 style="color: var(--tech-cyan); margin-bottom: 15px;">
                <i class="fas fa-thermometer-half"></i> 保鲜控制
            </h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                <div>
                    <label style="color: #fff; font-size: 12px;">过期预警天数</label>
                    <input type="number" id="food-expiry-warning" value="7" min="1" max="30" style="width: 100%; padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                </div>
                <div>
                    <label style="color: #fff; font-size: 12px;">最低库存预警 (%)</label>
                    <input type="number" id="food-min-stock" value="20" min="5" max="50" style="width: 100%; padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                </div>
                <button onclick="updateFoodWarnings()" style="padding: 10px 20px; background: var(--tech-cyan); color: #000; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; grid-column: 1 / -1;">
                    <i class="fas fa-check"></i> 应用预警设置
                </button>
            </div>
        </div>
        
        <div style="background: rgba(0,0,0,0.3); padding: 20px; border-radius: 8px; margin-bottom: 20px;">
            <h3 style="color: var(--tech-cyan); margin-bottom: 15px;">
                <i class="fas fa-list"></i> 库存列表
            </h3>
            <div id="food-inventory-list" style="max-height: 300px; overflow-y: auto;">
                <p style="color: #888;">加载中...</p>
            </div>
        </div>
        
        <div style="background: rgba(0,0,0,0.3); padding: 20px; border-radius: 8px;">
            <h3 style="color: var(--tech-cyan); margin-bottom: 15px;">
                <i class="fas fa-thermometer-half"></i> 保鲜温度区域
            </h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                <div>
                    <label style="color: #fff; font-size: 12px;">冷冻区 (°C)</label>
                    <input type="number" id="food-zone1-temp" value="-18" style="width: 100%; padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                </div>
                <div>
                    <label style="color: #fff; font-size: 12px;">冷藏区 (°C)</label>
                    <input type="number" id="food-zone2-temp" value="4" style="width: 100%; padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                </div>
                <div>
                    <label style="color: #fff; font-size: 12px;">深冷区 (°C)</label>
                    <input type="number" id="food-zone3-temp" value="-70" style="width: 100%; padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                </div>
                <button onclick="updateFoodZones()" style="padding: 10px 20px; background: var(--tech-cyan); color: #000; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; grid-column: 1 / -1;">
                    <i class="fas fa-check"></i> 应用温度设置
                </button>
            </div>
        </div>
    `;
    
    // 加载库存数据
    try {
        const response = await fetch('/api/food-inventory');
        const data = await response.json();
        displayFoodInventory(data);
    } catch (error) {
        console.error('Failed to load food inventory:', error);
    }
}

async function addFoodItem() {
    const name = document.getElementById('food-name').value;
    const quantity = document.getElementById('food-quantity').value;
    const nutrition = document.getElementById('food-nutrition').value;
    const expiry = document.getElementById('food-expiry').value;
    
    if (!name || !quantity) {
        showToast('⚠️ 请填写完整信息');
        return;
    }
    
    try {
        const response = await fetch('/api/food/add', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, quantity, nutrition_type: nutrition, expiry_date: expiry })
        });
        
        const result = await response.json();
        if (result.success) {
            showToast('✅ 食物添加成功！');
            // 清空表单
            document.getElementById('food-name').value = '';
            document.getElementById('food-quantity').value = '';
            document.getElementById('food-nutrition').value = 'protein';
            document.getElementById('food-expiry').value = '';
            // 重新加载模块并刷新数据
            await loadFoodModule();
            // 刷新总控制台数据以更新生存指数和预测
            await refreshData(window.charts);
        } else {
            showToast('❌ 添加失败: ' + (result.error || '未知错误'));
        }
    } catch (error) {
        console.error('Failed to add food:', error);
        showToast('❌ 添加失败');
    }
}

async function updateConsumptionRate() {
    const rate = document.getElementById('food-consumption-rate').value;
    const activity_level = document.getElementById('food-activity-level').value;
    
    try {
        const response = await fetch('/api/food/consumption', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ rate: parseFloat(rate), activity_level })
        });
        
        const result = await response.json();
        if (result.success) {
            showToast('✅ 消耗速率已更新！');
            // 刷新数据以显示最新状态
            await refreshData(window.charts);
        } else {
            showToast('❌ ' + (result.error || '更新失败'));
        }
    } catch (error) {
        console.error('Failed to update consumption:', error);
        showToast('❌ 更新失败');
    }
}

async function toggleEmergencyRation() {
    const enabled = document.getElementById('food-emergency-mode').checked;
    const percentage = document.getElementById('food-ration-percent').value;
    
    try {
        const response = await fetch('/api/food/emergency-ration', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ enabled, percentage: parseInt(percentage) })
        });
        
        const result = await response.json();
        if (result.success) {
            showToast(enabled ? '⚠️ 紧急配给模式已启用' : '✅ 已恢复正常配给');
            // 刷新数据以显示最新状态
            await refreshData(window.charts);
        }
    } catch (error) {
        console.error('Failed to toggle emergency ration:', error);
        showToast('❌ 操作失败');
    }
}

async function updateFoodWarnings() {
    const expiryWarning = document.getElementById('food-expiry-warning').value;
    const minStock = document.getElementById('food-min-stock').value;
    
    try {
        const response = await fetch('/api/food/warnings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ expiry_days: parseInt(expiryWarning), min_stock: parseInt(minStock) })
        });
        const result = await response.json();
        if (result.success) {
            showToast(`✅ 预警设置已保存：过期${expiryWarning}天，最低库存${minStock}%`);
            await refreshData(window.charts);
        } else {
            showToast('❌ 保存失败');
        }
    } catch (error) {
        console.error('Failed to update food warnings:', error);
        showToast('❌ 保存失败');
    }
}

async function updateFoodZones() {
    const zone1 = document.getElementById('food-zone1-temp').value;
    const zone2 = document.getElementById('food-zone2-temp').value;
    const zone3 = document.getElementById('food-zone3-temp').value;
    
    try {
        const response = await fetch('/api/food/zones', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ zone1: parseFloat(zone1), zone2: parseFloat(zone2), zone3: parseFloat(zone3) })
        });
        const result = await response.json();
        if (result.success) {
            showToast(`✅ 温度区域已设置：冷冻${zone1}°C, 冷藏${zone2}°C, 深冷${zone3}°C`);
            await refreshData(window.charts);
        } else {
            showToast('❌ 保存失败');
        }
    } catch (error) {
        console.error('Failed to update food zones:', error);
        showToast(' 保存失败');
    }
}

function displayFoodInventory(data) {
    const list = document.getElementById('food-inventory-list');
    if (!data || !data.categories || data.categories.length === 0) {
        list.innerHTML = '<p style="color: #888;">暂无库存数据</p>';
        return;
    }
    
    list.innerHTML = data.categories.map(cat => `
        <div style="padding: 10px; margin-bottom: 10px; background: rgba(0,243,255,0.1); border-radius: 5px; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <strong style="color: var(--tech-cyan);">${cat.name}</strong>
                <div style="color: #fff; font-size: 12px;">${cat.value}${cat.unit}</div>
            </div>
        </div>
    `).join('');
}

// 医疗冷链模块
async function loadMedicalModule() {
    const container = document.getElementById('medical-content');
    container.innerHTML = `
        <div style="background: rgba(0,0,0,0.3); padding: 20px; border-radius: 8px; margin-bottom: 20px;">
            <h3 style="color: var(--tech-cyan); margin-bottom: 15px;">
                <i class="fas fa-syringe"></i> 添加医疗物品
            </h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                <input type="text" id="medical-name" placeholder="物品名称" style="padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                <select id="medical-type" style="padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                    <option value="vaccine">疫苗</option>
                    <option value="medicine">药品</option>
                    <option value="sample">生物样本</option>
                </select>
                <input type="number" id="medical-quantity" placeholder="数量" style="padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                <input type="number" id="medical-temp" placeholder="存储温度 (°C)" style="padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                <select id="medical-urgency" style="padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                    <option value="low">低优先级</option>
                    <option value="normal" selected>正常</option>
                    <option value="high">高优先级</option>
                    <option value="critical">紧急</option>
                </select>
                <button onclick="addMedicalItem()" style="padding: 10px 20px; background: var(--tech-cyan); color: #000; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">
                    <i class="fas fa-plus"></i> 添加
                </button>
            </div>
        </div>
        
        <div style="background: rgba(0,0,0,0.3); padding: 20px; border-radius: 8px;">
            <h3 style="color: var(--tech-cyan); margin-bottom: 15px;">
                <i class="fas fa-thermometer-half"></i> 温度控制
            </h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                <div>
                    <label style="color: #fff; font-size: 12px;">最低温度 (°C)</label>
                    <input type="number" id="medical-temp-min" value="-80" style="width: 100%; padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                </div>
                <div>
                    <label style="color: #fff; font-size: 12px;">最高温度 (°C)</label>
                    <input type="number" id="medical-temp-max" value="-60" style="width: 100%; padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                </div>
                <button onclick="updateMedicalTempRange()" style="padding: 10px 20px; background: var(--tech-cyan); color: #000; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; grid-column: 1 / -1;">
                    <i class="fas fa-check"></i> 应用温度范围
                </button>
            </div>
        </div>
        
        <div style="background: rgba(0,0,0,0.3); padding: 20px; border-radius: 8px;">
            <h3 style="color: var(--tech-cyan); margin-bottom: 15px;">
                <i class="fas fa-list"></i> 医疗物品列表
            </h3>
            <div id="medical-items-list" style="max-height: 300px; overflow-y: auto;">
                <p style="color: #aaa;">加载中...</p>
            </div>
        </div>
    `;
    
    // 加载医疗物品列表
    await loadMedicalItemsList();
}

async function loadMedicalItemsList() {
    try {
        const response = await fetch('/api/medical');
        const data = await response.json();
        
        const listContainer = document.getElementById('medical-items-list');
        if (!listContainer) return;
        
        const items = data.medical_items || [];
        
        if (items.length === 0) {
            listContainer.innerHTML = '<p style="color: #aaa;">暂无医疗物品</p>';
            return;
        }
        
        let html = '<div style="display: grid; gap: 10px;">';
        items.forEach(item => {
            html += `
                <div style="background: rgba(0,243,255,0.1); padding: 15px; border-radius: 5px; border-left: 3px solid var(--tech-cyan);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong style="color: #fff;">${item.name}</strong>
                            <span style="color: #aaa; font-size: 12px; margin-left: 10px;">(${item.type})</span>
                        </div>
                        <button onclick="removeMedicalItem(${item.id})" style="padding: 5px 10px; background: #ff4d4d; color: #fff; border: none; border-radius: 3px; cursor: pointer; font-size: 12px;">
                            <i class="fas fa-trash"></i> 删除
                        </button>
                    </div>
                    <div style="color: #aaa; font-size: 12px; margin-top: 5px;">
                        数量: ${item.quantity} | 存储温度: ${item.storage_temp}°C | 优先级: ${item.urgency}
                    </div>
                </div>
            `;
        });
        html += '</div>';
        
        listContainer.innerHTML = html;
    } catch (error) {
        console.error('Failed to load medical items:', error);
        const listContainer = document.getElementById('medical-items-list');
        if (listContainer) {
            listContainer.innerHTML = '<p style="color: #ff4d4d;">加载失败</p>';
        }
    }
}

async function removeMedicalItem(itemId) {
    const reason = prompt('请输入移除原因:', '过期');
    if (!reason) return;
    
    try {
        const response = await fetch(`/api/medical/remove/${itemId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ reason })
        });
        
        const result = await response.json();
        if (result.success) {
            showToast('✅ 医疗物品已移除');
            await loadMedicalModule();
            await refreshData(window.charts);
        } else {
            showToast('❌ 移除失败: ' + result.error);
        }
    } catch (error) {
        console.error('Failed to remove medical item:', error);
        showToast('❌ 网络错误');
    }
}

async function addMedicalItem() {
    const name = document.getElementById('medical-name').value;
    const type = document.getElementById('medical-type').value;
    const quantity = document.getElementById('medical-quantity').value;
    const storage_temp = document.getElementById('medical-temp').value;
    const urgency = document.getElementById('medical-urgency').value;
    
    if (!name) {
        showToast('⚠️ 请输入物品名称');
        return;
    }
    
    try {
        const response = await fetch('/api/medical/add', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                name, 
                type, 
                quantity: parseFloat(quantity) || 1,
                storage_temp: parseFloat(storage_temp) || -70,
                urgency
            })
        });
        
        const result = await response.json();
        if (result.success) {
            showToast('✅ 医疗物品添加成功！');
            // 清空表单
            document.getElementById('medical-name').value = '';
            document.getElementById('medical-quantity').value = '1';
            document.getElementById('medical-temp').value = '-70';
            // 重新加载模块并刷新数据
            await loadMedicalModule();
            // 刷新总控制台数据以更新生存指数和预测
            await refreshData(window.charts);
        } else {
            showToast('❌ 添加失败: ' + (result.error || '未知错误'));
        }
    } catch (error) {
        console.error('Failed to add medical item:', error);
        showToast('❌ 添加失败');
    }
}

async function updateMedicalTempRange() {
    const min = document.getElementById('medical-temp-min').value;
    const max = document.getElementById('medical-temp-max').value;
    
    try {
        const response = await fetch('/api/medical/temp-range', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ min: parseFloat(min), max: parseFloat(max) })
        });
        
        const result = await response.json();
        if (result.success) {
            showToast('✅ 温度范围已更新！');
            // 刷新数据以显示最新状态
            await refreshData(window.charts);
        }
    } catch (error) {
        console.error('Failed to update temp range:', error);
        showToast('❌ 更新失败');
    }
}

// 能源管理模块
async function loadEnergyModule() {
    const container = document.getElementById('energy-content');
    container.innerHTML = `
        <div style="background: rgba(0,0,0,0.3); padding: 20px; border-radius: 8px;">
            <h3 style="color: var(--tech-cyan); margin-bottom: 15px;">
                <i class="fas fa-sliders-h"></i> 能源分配
            </h3>
            <div style="display: grid; gap: 15px;">
                <div>
                    <label style="color: #fff; font-size: 12px;">医疗区 (%)</label>
                    <input type="range" id="energy-medical" min="0" max="100" value="30" oninput="updateEnergyDist()" style="width: 100%; accent-color: var(--tech-cyan);">
                    <span id="val-energy-medical" style="color: var(--tech-cyan);">30%</span>
                </div>
                <div>
                    <label style="color: #fff; font-size: 12px;">食物区 (%)</label>
                    <input type="range" id="energy-food" min="0" max="100" value="25" oninput="updateEnergyDist()" style="width: 100%; accent-color: var(--tech-cyan);">
                    <span id="val-energy-food" style="color: var(--tech-cyan);">25%</span>
                </div>
                <div>
                    <label style="color: #fff; font-size: 12px;">环境控制 (%)</label>
                    <input type="range" id="energy-env" min="0" max="100" value="25" oninput="updateEnergyDist()" style="width: 100%; accent-color: var(--tech-cyan);">
                    <span id="val-energy-env" style="color: var(--tech-cyan);">25%</span>
                </div>
                <div>
                    <label style="color: #fff; font-size: 12px;">其他系统 (%)</label>
                    <input type="range" id="energy-other" min="0" max="100" value="20" oninput="updateEnergyDist()" style="width: 100%; accent-color: var(--tech-cyan);">
                    <span id="val-energy-other" style="color: var(--tech-cyan);">20%</span>
                </div>
                <div style="padding: 10px; background: rgba(0,0,0,0.3); border-radius: 5px; text-align: center;">
                    <label style="color: #fff; font-size: 14px;">当前总和：</label>
                    <span id="val-energy-total" style="color: var(--tech-cyan); font-size: 18px; font-weight: bold;">100%</span>
                </div>
                <button onclick="applyEnergyDistribution()" style="padding: 10px 20px; background: var(--tech-cyan); color: #000; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; margin-top: 10px;">
                    <i class="fas fa-check"></i> 应用分配
                </button>
            </div>
        </div>
        
        <div style="background: rgba(0,0,0,0.3); padding: 20px; border-radius: 8px; margin-bottom: 20px;">
            <h3 style="color: var(--tech-cyan); margin-bottom: 15px;">
                <i class="fas fa-solar-panel"></i> 充电策略
            </h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                <div>
                    <label style="color: #fff; font-size: 12px;">太阳能充电时间 (小时)</label>
                    <input type="number" id="solar-charging-hours" value="8" min="0" max="24" style="width: 100%; padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                </div>
                <div>
                    <label style="color: #fff; font-size: 12px;">备用电源启用条件 (%)</label>
                    <input type="number" id="backup-power-threshold" value="30" min="0" max="100" style="width: 100%; padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                </div>
                <button onclick="applyChargingStrategy()" style="padding: 10px 20px; background: var(--tech-cyan); color: #000; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; grid-column: 1 / -1;">
                    <i class="fas fa-check"></i> 应用策略
                </button>
            </div>
        </div>
        
        <div style="background: rgba(0,0,0,0.3); padding: 20px; border-radius: 8px; margin-bottom: 20px;">
            <h3 style="color: var(--tech-cyan); margin-bottom: 15px;">
                <i class="fas fa-battery-quarter"></i> 低电量响应
            </h3>
            <div style="display: grid; gap: 15px;">
                <div>
                    <label style="color: #fff; font-size: 12px;">自动关机顺序</label>
                    <textarea id="shutdown-sequence" rows="3" placeholder="例如：非关键系统→照明→空调→生命支持" style="width: 100%; padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff; resize: vertical;"></textarea>
                </div>
                <div>
                    <label style="color: #fff; font-size: 12px;">保留的核心功能</label>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; margin-top: 10px;">
                        <label style="display: flex; align-items: center; color: #fff; cursor: pointer;">
                            <input type="checkbox" id="keep-life-support" checked style="margin-right: 8px; width: 18px; height: 18px; accent-color: var(--tech-cyan);">
                            生命支持
                        </label>
                        <label style="display: flex; align-items: center; color: #fff; cursor: pointer;">
                            <input type="checkbox" id="keep-communications" checked style="margin-right: 8px; width: 18px; height: 18px; accent-color: var(--tech-cyan);">
                            通信系统
                        </label>
                        <label style="display: flex; align-items: center; color: #fff; cursor: pointer;">
                            <input type="checkbox" id="keep-medical" checked style="margin-right: 8px; width: 18px; height: 18px; accent-color: var(--tech-cyan);">
                            医疗设备
                        </label>
                        <label style="display: flex; align-items: center; color: #fff; cursor: pointer;">
                            <input type="checkbox" id="keep-navigation" style="margin-right: 8px; width: 18px; height: 18px; accent-color: var(--tech-cyan);">
                            导航系统
                        </label>
                    </div>
                </div>
                <button onclick="applyLowBatteryResponse()" style="padding: 10px 20px; background: #ff9500; color: #000; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">
                    <i class="fas fa-check"></i> 应用配置
                </button>
            </div>
        </div>
    `;
}

function updateEnergyDist() {
    let total = 0;
    ['medical', 'food', 'env', 'other'].forEach(id => {
        const slider = document.getElementById(`energy-${id}`);
        const display = document.getElementById(`val-energy-${id}`);
        if (slider && display) {
            display.textContent = slider.value + '%';
            total += parseInt(slider.value);
        }
    });
    
    // 更新总和显示
    const totalDisplay = document.getElementById('val-energy-total');
    if (totalDisplay) {
        totalDisplay.textContent = total + '%';
        totalDisplay.style.color = total === 100 ? 'var(--tech-cyan)' : '#ff4d4d';
    }
}

async function applyEnergyDistribution() {
    const distribution = {
        medical: parseInt(document.getElementById('energy-medical').value),
        food: parseInt(document.getElementById('energy-food').value),
        environment: parseInt(document.getElementById('energy-env').value),
        other: parseInt(document.getElementById('energy-other').value)
    };
    
    try {
        const response = await fetch('/api/energy/distribution', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(distribution)
        });
        
        const result = await response.json();
        if (result.success) {
            showToast('✅ 能源分配已更新！');
            // 刷新数据以显示最新状态
            await refreshData(window.charts);
        } else {
            showToast('❌ ' + result.error);
        }
    } catch (error) {
        console.error('Failed to update energy distribution:', error);
        showToast('❌ 更新失败');
    }
}

async function applyChargingStrategy() {
    const solarHours = document.getElementById('solar-charging-hours').value;
    const backupThreshold = document.getElementById('backup-power-threshold').value;
    
    try {
        const response = await fetch('/api/energy/charging-strategy', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ solar_hours: parseInt(solarHours), backup_threshold: parseInt(backupThreshold) })
        });
        const result = await response.json();
        if (result.success) {
            showToast(`✅ 充电策略已设置：太阳能${solarHours}小时，备用电源${backupThreshold}%`);
            await refreshData(window.charts);
        } else {
            showToast('❌ 保存失败');
        }
    } catch (error) {
        console.error('Failed to update charging strategy:', error);
        showToast(' 保存失败');
    }
}

async function applyLowBatteryResponse() {
    const sequence = document.getElementById('shutdown-sequence').value;
    const keepLifeSupport = document.getElementById('keep-life-support').checked;
    const keepCommunications = document.getElementById('keep-communications').checked;
    const keepMedical = document.getElementById('keep-medical').checked;
    const keepNavigation = document.getElementById('keep-navigation').checked;
    
    const retained = [];
    if (keepLifeSupport) retained.push('life_support');
    if (keepCommunications) retained.push('communications');
    if (keepMedical) retained.push('medical');
    if (keepNavigation) retained.push('navigation');
    
    const retainedText = [];
    if (keepLifeSupport) retainedText.push('生命支持');
    if (keepCommunications) retainedText.push('通信系统');
    if (keepMedical) retainedText.push('医疗设备');
    if (keepNavigation) retainedText.push('导航系统');
    
    try {
        const response = await fetch('/api/energy/low-battery-response', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ shutdown_sequence: sequence, retained_functions: retained })
        });
        const result = await response.json();
        if (result.success) {
            showToast(`✅ 低电量响应已配置：保留${retainedText.join('、')}`);
            await refreshData(window.charts);
        } else {
            showToast('❌ 保存失败');
        }
    } catch (error) {
        console.error('Failed to update low battery response:', error);
        showToast('❌ 保存失败');
    }
}

// 环境控制模块
async function loadEnvModule() {
    const container = document.getElementById('env-content');
    container.innerHTML = `
        <div style="background: rgba(0,0,0,0.3); padding: 20px; border-radius: 8px;">
            <h3 style="color: var(--tech-cyan); margin-bottom: 15px;">
                <i class="fas fa-thermometer-half"></i> 环境参数设置
            </h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                <div>
                    <label style="color: #fff; font-size: 12px;">氧气浓度目标 (%)</label>
                    <input type="number" id="env-oxygen" value="21" step="0.1" style="width: 100%; padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                </div>
                <div>
                    <label style="color: #fff; font-size: 12px;">温度目标 (°C)</label>
                    <input type="number" id="env-temp" value="22" step="0.1" style="width: 100%; padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                </div>
                <div>
                    <label style="color: #fff; font-size: 12px;">湿度目标 (%)</label>
                    <input type="number" id="env-humidity" value="45" step="1" style="width: 100%; padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                </div>
                <button onclick="applyEnvTargets()" style="padding: 10px 20px; background: var(--tech-cyan); color: #000; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; grid-column: 1 / -1;">
                    <i class="fas fa-check"></i> 应用设置
                </button>
            </div>
        </div>
        
        <div style="background: rgba(0,0,0,0.3); padding: 20px; border-radius: 8px; margin-bottom: 20px;">
            <h3 style="color: var(--tech-cyan); margin-bottom: 15px;">
                <i class="fas fa-exclamation-circle"></i> CO₂与警报设置
            </h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                <div>
                    <label style="color: #fff; font-size: 12px;">CO₂浓度上限 (%)</label>
                    <input type="number" id="env-co2-max" value="0.5" step="0.1" min="0" max="5" style="width: 100%; padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                </div>
                <div>
                    <label style="color: #fff; font-size: 12px;">氧气警报下限 (%)</label>
                    <input type="number" id="env-oxygen-alert" value="19.5" step="0.1" style="width: 100%; padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                </div>
                <div>
                    <label style="color: #fff; font-size: 12px;">温度警报范围 (°C)</label>
                    <input type="text" id="env-temp-alert" placeholder="例如: 18-26" style="width: 100%; padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                </div>
                <button onclick="applyEnvAlerts()" style="padding: 10px 20px; background: var(--tech-cyan); color: #000; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; grid-column: 1 / -1;">
                    <i class="fas fa-check"></i> 应用警报设置
                </button>
            </div>
        </div>
        
        <div style="background: rgba(0,0,0,0.3); padding: 20px; border-radius: 8px; margin-bottom: 20px;">
            <h3 style="color: var(--tech-cyan); margin-bottom: 15px;">
                <i class="fas fa-wind"></i> 通风控制
            </h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                <select id="ventilation-mode" style="padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                    <option value="auto">自动循环</option>
                    <option value="manual">手动控制</option>
                    <option value="emergency">应急模式</option>
                </select>
                <div>
                    <label style="color: #fff; font-size: 12px;">循环时间 (分钟)</label>
                    <input type="number" id="ventilation-interval" value="30" min="5" max="120" style="width: 100%; padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                </div>
                <button onclick="applyVentilationControl()" style="padding: 10px 20px; background: var(--tech-cyan); color: #000; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; grid-column: 1 / -1;">
                    <i class="fas fa-check"></i> 应用通风设置
                </button>
            </div>
        </div>
        
        <div style="background: rgba(0,0,0,0.3); padding: 20px; border-radius: 8px;">
            <h3 style="color: var(--tech-cyan); margin-bottom: 15px;">
                <i class="fas fa-first-aid"></i> 应急响应方案
            </h3>
            <div style="display: grid; gap: 15px;">
                <div>
                    <label style="color: #fff; font-size: 12px;">氧气泄漏处理方案</label>
                    <select id="oxygen-leak-response" style="width: 100%; padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                        <option value="isolate">隔离泄漏区域</option>
                        <option value="boost">增加氧气供应</option>
                        <option value="evacuate">紧急撤离</option>
                    </select>
                </div>
                <div>
                    <label style="color: #fff; font-size: 12px;">空气净化优先级</label>
                    <select id="air-purification-priority" style="width: 100%; padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                        <option value="co2">优先去除CO₂</option>
                        <option value="particles">优先过滤颗粒物</option>
                        <option value="balanced">平衡模式</option>
                    </select>
                </div>
                <button onclick="applyEmergencyResponse()" style="padding: 10px 20px; background: #ff9500; color: #000; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">
                    <i class="fas fa-check"></i> 应用应急方案
                </button>
            </div>
        </div>
    `;
}

async function applyEnvTargets() {
    const targets = {
        oxygen: parseFloat(document.getElementById('env-oxygen').value),
        temperature: parseFloat(document.getElementById('env-temp').value),
        humidity: parseFloat(document.getElementById('env-humidity').value)
    };
    
    try {
        const response = await fetch('/api/environment/targets', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(targets)
        });
        
        const result = await response.json();
        if (result.success) {
            showToast('✅ 环境参数已更新！');
            // 刷新数据以显示最新状态
            await refreshData(window.charts);
        } else {
            showToast('❌ ' + (result.error || '更新失败'));
        }
    } catch (error) {
        console.error('Failed to update env targets:', error);
        showToast('❌ 更新失败');
    }
}

async function applyEnvAlerts() {
    const co2Max = document.getElementById('env-co2-max').value;
    const oxygenAlert = document.getElementById('env-oxygen-alert').value;
    const tempAlert = document.getElementById('env-temp-alert').value;
    
    try {
        const response = await fetch('/api/environment/alerts-config', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ co2_max: parseFloat(co2Max), oxygen_alert: parseFloat(oxygenAlert), temp_alert: tempAlert })
        });
        const result = await response.json();
        if (result.success) {
            showToast(`✅ 警报设置已保存：CO₂上限${co2Max}%，氧气下限${oxygenAlert}%`);
            await refreshData(window.charts);
        } else {
            showToast('❌ 保存失败');
        }
    } catch (error) {
        console.error('Failed to update env alerts:', error);
        showToast('❌ 保存失败');
    }
}

async function applyVentilationControl() {
    const mode = document.getElementById('ventilation-mode').value;
    const interval = document.getElementById('ventilation-interval').value;
    
    try {
        const response = await fetch('/api/environment/ventilation-config', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mode, interval: parseInt(interval) })
        });
        const result = await response.json();
        if (result.success) {
            showToast(`✅ 通风控制已设置：${mode === 'auto' ? '自动' : mode === 'manual' ? '手动' : '应急'}模式，循环${interval}分钟`);
            await refreshData(window.charts);
        } else {
            showToast('❌ 保存失败');
        }
    } catch (error) {
        console.error('Failed to update ventilation:', error);
        showToast('❌ 保存失败');
    }
}

async function applyEmergencyResponse() {
    const leakResponse = document.getElementById('oxygen-leak-response').value;
    const purificationPriority = document.getElementById('air-purification-priority').value;
    
    const leakText = leakResponse === 'isolate' ? '隔离' : leakResponse === 'boost' ? '增氧' : '撤离';
    const purifyText = purificationPriority === 'co2' ? '去CO₂' : purificationPriority === 'particles' ? '过滤颗粒' : '平衡';
    
    try {
        const response = await fetch('/api/environment/emergency-response', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ leak_response: leakResponse, purification_priority: purificationPriority })
        });
        const result = await response.json();
        if (result.success) {
            showToast(`✅ 应急方案已配置：泄漏${leakText}，净化${purifyText}`);
            await refreshData(window.charts);
        } else {
            showToast('❌ 保存失败');
        }
    } catch (error) {
        console.error('Failed to update emergency response:', error);
        showToast('❌ 保存失败');
    }
}

// 紧急协议模块
async function loadEmergencyModule() {
    const container = document.getElementById('emergency-content');
    container.innerHTML = `
        <div style="background: rgba(255,0,0,0.1); padding: 20px; border-radius: 8px; border: 2px solid rgba(255,0,0,0.3); margin-bottom: 20px;">
            <h3 style="color: #ff4d4d; margin-bottom: 15px;">
                <i class="fas fa-exclamation-triangle"></i> 手动触发紧急协议
            </h3>
            <div style="display: grid; gap: 15px;">
                <select id="emergency-level" style="padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(255,0,0,0.3); border-radius: 5px; color: #fff;">
                    <option value="warning">警告 (Warning)</option>
                    <option value="critical">严重 (Critical)</option>
                </select>
                <button onclick="triggerEmergencyManual()" style="padding: 15px 30px; background: #ff4d4d; color: #fff; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; font-size: 16px;">
                    <i class="fas fa-bell"></i> 触发紧急协议
                </button>
            </div>
        </div>
        
        <div style="background: rgba(0,0,0,0.3); padding: 20px; border-radius: 8px; margin-bottom: 20px;">
            <h3 style="color: var(--tech-cyan); margin-bottom: 15px;">
                <i class="fas fa-cogs"></i> 协议触发器配置
            </h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                <div>
                    <label style="color: #fff; font-size: 12px;">氧气泄漏触发阈值 (%)</label>
                    <input type="number" id="trigger-oxygen" value="19" step="0.5" min="0" max="21" style="width: 100%; padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                </div>
                <div>
                    <label style="color: #fff; font-size: 12px;">能源危机触发阈值 (%)</label>
                    <input type="number" id="trigger-energy" value="15" min="0" max="100" style="width: 100%; padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                </div>
                <div>
                    <label style="color: #fff; font-size: 12px;">响应延迟 (秒)</label>
                    <input type="number" id="trigger-delay" value="5" min="0" max="60" style="width: 100%; padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                </div>
                <button onclick="applyTriggerConfig()" style="padding: 10px 20px; background: var(--tech-cyan); color: #000; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; grid-column: 1 / -1;">
                    <i class="fas fa-check"></i> 应用配置
                </button>
            </div>
        </div>
        
        <div style="background: rgba(0,0,0,0.3); padding: 20px; border-radius: 8px; margin-bottom: 20px;">
            <h3 style="color: var(--tech-cyan); margin-bottom: 15px;">
                <i class="fas fa-tasks"></i> 执行动作配置
            </h3>
            <div style="display: grid; gap: 15px;">
                <div>
                    <label style="color: #fff; font-size: 12px;">选择要执行的动作（多选）</label>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; margin-top: 10px;">
                        <label style="display: flex; align-items: center; color: #fff; cursor: pointer;">
                            <input type="checkbox" id="action-isolate" checked style="margin-right: 8px; width: 18px; height: 18px; accent-color: var(--tech-cyan);">
                            隔离危险区域
                        </label>
                        <label style="display: flex; align-items: center; color: #fff; cursor: pointer;">
                            <input type="checkbox" id="action-alert" checked style="margin-right: 8px; width: 18px; height: 18px; accent-color: var(--tech-cyan);">
                            发送警报通知
                        </label>
                        <label style="display: flex; align-items: center; color: #fff; cursor: pointer;">
                            <input type="checkbox" id="action-shutdown" style="margin-right: 8px; width: 18px; height: 18px; accent-color: var(--tech-cyan);">
                            关闭非关键系统
                        </label>
                        <label style="display: flex; align-items: center; color: #fff; cursor: pointer;">
                            <input type="checkbox" id="action-evacuate" style="margin-right: 8px; width: 18px; height: 18px; accent-color: var(--tech-cyan);">
                            启动撤离程序
                        </label>
                    </div>
                </div>
                <div>
                    <label style="color: #fff; font-size: 12px;">确认机制</label>
                    <select id="action-confirmation" style="width: 100%; padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                        <option value="auto">自动执行</option>
                        <option value="confirm" selected>需要确认</option>
                        <option value="manual">完全手动</option>
                    </select>
                </div>
                <button onclick="applyActionConfig()" style="padding: 10px 20px; background: var(--tech-cyan); color: #000; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">
                    <i class="fas fa-check"></i> 应用动作配置
                </button>
            </div>
        </div>
        
        <div style="background: rgba(0,0,0,0.3); padding: 20px; border-radius: 8px;">
            <h3 style="color: var(--tech-cyan); margin-bottom: 15px;">
                <i class="fas fa-flask"></i> 模拟测试面板
            </h3>
            <div style="display: grid; gap: 15px;">
                <div>
                    <label style="color: #fff; font-size: 12px;">选择测试场景</label>
                    <select id="test-scenario" style="width: 100%; padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                        <option value="oxygen-leak">氧气泄漏</option>
                        <option value="power-failure">能源故障</option>
                        <option value="cold-chain-break">冷链中断</option>
                        <option value="hull-damage">舱体损伤</option>
                    </select>
                </div>
                <div>
                    <label style="color: #fff; font-size: 12px;">模拟严重程度</label>
                    <input type="range" id="test-severity" min="1" max="10" value="5" oninput="document.getElementById('val-test-severity').textContent=this.value+'/10'" style="width: 100%; accent-color: var(--tech-cyan);">
                    <span id="val-test-severity" style="color: var(--tech-cyan);">5/10</span>
                </div>
                <button onclick="runEmergencyTest()" style="padding: 10px 20px; background: #ff9500; color: #000; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">
                    <i class="fas fa-play-circle"></i> 运行模拟测试
                </button>
            </div>
        </div>
    `;
}

async function triggerEmergencyManual() {
    const level = document.getElementById('emergency-level').value;
    
    if (!confirm(`确定要触发${level === 'critical' ? '严重' : '警告'}级别紧急协议吗？`)) {
        return;
    }
    
    try {
        const response = await fetch('/api/emergency/trigger-manual', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ level })
        });
        
        const result = await response.json();
        if (result.success) {
            showToast('⚠️ 紧急协议已触发！');
            await refreshData(window.charts);
        } else {
            showToast('❌ ' + (result.error || '触发失败'));
        }
    } catch (error) {
        console.error('Failed to trigger emergency:', error);
        showToast('❌ 触发失败');
    }
}

async function applyTriggerConfig() {
    const oxygenThreshold = document.getElementById('trigger-oxygen').value;
    const energyThreshold = document.getElementById('trigger-energy').value;
    const delay = document.getElementById('trigger-delay').value;
    
    try {
        const response = await fetch('/api/emergency/configure', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                triggers: {
                    survival_index_min: 30,
                    energy_level_min: parseFloat(energyThreshold),
                    oxygen_level_min: parseFloat(oxygenThreshold)
                },
                actions: ['alert_crew', 'conserve_energy', 'prioritize_life_support'],
                delay: parseInt(delay)
            })
        });
        const result = await response.json();
        if (result.success) {
            showToast(`✅ 触发器配置已保存：氧气${oxygenThreshold}%，能源${energyThreshold}%，延迟${delay}秒`);
            await refreshData(window.charts);
        } else {
            showToast('❌ 保存失败');
        }
    } catch (error) {
        console.error('Failed to update trigger config:', error);
        showToast('❌ 保存失败');
    }
}

async function applyActionConfig() {
    const actions = [];
    if (document.getElementById('action-isolate').checked) actions.push('isolate');
    if (document.getElementById('action-alert').checked) actions.push('alert_crew');
    if (document.getElementById('action-shutdown').checked) actions.push('shutdown_non_critical');
    if (document.getElementById('action-evacuate').checked) actions.push('evacuate');
    
    const confirmation = document.getElementById('action-confirmation').value;
    
    try {
        const response = await fetch('/api/emergency/configure', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                triggers: {},
                actions: actions.length > 0 ? actions : ['alert_crew'],
                delay: 0,
                confirmation: confirmation
            })
        });
        const result = await response.json();
        if (result.success) {
            const confirmText = confirmation === 'auto' ? '自动' : confirmation === 'confirm' ? '需确认' : '手动';
            showToast(`✅ 动作配置已保存：执行${actions.length > 0 ? actions.join('、') : '警报'}，确认方式：${confirmText}`);
            await refreshData(window.charts);
        } else {
            showToast('❌ 保存失败');
        }
    } catch (error) {
        console.error('Failed to update action config:', error);
        showToast(' 保存失败');
    }
}

async function runEmergencyTest() {
    const scenario = document.getElementById('test-scenario').value;
    const severity = document.getElementById('test-severity').value;
    
    const scenarioText = {
        'oxygen-leak': '氧气泄漏',
        'power-failure': '能源故障',
        'cold-chain-break': '冷链中断',
        'hull-damage': '舱体损伤'
    }[scenario];
    
    try {
        const response = await fetch('/api/emergency/simulate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ scenario, severity: parseFloat(severity), strategy: 'survival-first' })
        });
        const result = await response.json();
        if (result.success) {
            showToast(` 运行模拟测试：${scenarioText}（严重程度${severity}/10）`);
            await refreshData(window.charts);
        } else {
            showToast('❌ 模拟失败');
        }
    } catch (error) {
        console.error('Failed to run simulation:', error);
        showToast('❌ 模拟失败');
    }
}

// 宇航员管理模块
async function loadCrewModule() {
    const container = document.getElementById('crew-content');
    container.innerHTML = `
        <div style="background: rgba(0,0,0,0.3); padding: 20px; border-radius: 8px; margin-bottom: 20px;">
            <h3 style="color: var(--tech-cyan); margin-bottom: 15px;">
                <i class="fas fa-user-plus"></i> 添加宇航员
            </h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px;">
                <input type="text" id="crew-name" placeholder="姓名" style="padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                <input type="number" id="crew-age" placeholder="年龄" style="padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                <input type="number" id="crew-weight" placeholder="体重 (kg)" style="padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                <select id="crew-health" style="padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                    <option value="excellent">优秀</option>
                    <option value="good" selected>良好</option>
                    <option value="fair">一般</option>
                    <option value="poor">较差</option>
                </select>
                <button onclick="addCrewMember()" style="padding: 10px 20px; background: var(--tech-cyan); color: #000; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">
                    <i class="fas fa-plus"></i> 添加
                </button>
            </div>
        </div>
        
        <div style="background: rgba(0,0,0,0.3); padding: 20px; border-radius: 8px;">
            <h3 style="color: var(--tech-cyan); margin-bottom: 15px;">
                <i class="fas fa-users"></i> 宇航员列表
            </h3>
            <div id="crew-list" style="max-height: 300px; overflow-y: auto;">
                <p style="color: #888;">加载中...</p>
            </div>
        </div>
        
        <div style="background: rgba(0,0,0,0.3); padding: 20px; border-radius: 8px; margin-top: 20px;">
            <h3 style="color: var(--tech-cyan); margin-bottom: 15px;">
                <i class="fas fa-utensils"></i> 营养需求设置
            </h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                <div>
                    <label style="color: #fff; font-size: 12px;">每日热量需求 (千卡)</label>
                    <input type="number" id="crew-calories" value="2500" min="1500" max="4000" step="100" style="width: 100%; padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                </div>
                <div>
                    <label style="color: #fff; font-size: 12px;">特殊饮食要求</label>
                    <input type="text" id="crew-diet" placeholder="例如：素食、无乳糖" style="width: 100%; padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                </div>
                <div>
                    <label style="color: #fff; font-size: 12px;">过敏/禁忌</label>
                    <input type="text" id="crew-allergies" placeholder="例如：花生、海鲜" style="width: 100%; padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                </div>
                <button onclick="applyNutritionSettings()" style="padding: 10px 20px; background: var(--tech-cyan); color: #000; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; grid-column: 1 / -1;">
                    <i class="fas fa-check"></i> 应用营养设置
                </button>
            </div>
        </div>
        
        <div style="background: rgba(0,0,0,0.3); padding: 20px; border-radius: 8px; margin-top: 20px;">
            <h3 style="color: var(--tech-cyan); margin-bottom: 15px;">
                <i class="fas fa-calendar-alt"></i> 活动日程安排
            </h3>
            <div style="display: grid; gap: 15px;">
                <div>
                    <label style="color: #fff; font-size: 12px;">日常活动计划</label>
                    <textarea id="crew-daily-schedule" rows="3" placeholder="例如：06:00 起床，07:00 早餐，08:00 科研任务..." style="width: 100%; padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff; resize: vertical;"></textarea>
                </div>
                <div>
                    <label style="color: #fff; font-size: 12px;">休息时间设置 (小时/天)</label>
                    <input type="number" id="crew-rest-hours" value="8" min="4" max="12" step="0.5" style="width: 100%; padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                </div>
                <div>
                    <label style="color: #fff; font-size: 12px;">活动强度调整</label>
                    <select id="crew-activity-adjustment" style="width: 100%; padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                        <option value="low">低消耗模式</option>
                        <option value="normal" selected>正常模式</option>
                        <option value="high">高消耗模式</option>
                    </select>
                </div>
                <button onclick="applyActivitySchedule()" style="padding: 10px 20px; background: var(--tech-cyan); color: #000; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">
                    <i class="fas fa-check"></i> 应用日程安排
                </button>
            </div>
        </div>
    `;
    
    // 加载宇航员列表
    try {
        const response = await fetch('/api/crew/list');
        const crew = await response.json();
        displayCrewList(crew);
    } catch (error) {
        console.error('Failed to load crew:', error);
    }
}

async function addCrewMember() {
    const name = document.getElementById('crew-name').value;
    const age = document.getElementById('crew-age').value;
    const weight = document.getElementById('crew-weight').value;
    const health = document.getElementById('crew-health').value;
    
    if (!name) {
        showToast('⚠️ 请输入姓名');
        return;
    }
    
    try {
        const response = await fetch('/api/crew/add', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                name, 
                age: parseInt(age) || 30, 
                weight: parseFloat(weight) || 70,
                health_status: health
            })
        });
        
        const result = await response.json();
        if (result.success) {
            showToast('✅ 宇航员添加成功！');
            // 清空表单
            document.getElementById('crew-name').value = '';
            document.getElementById('crew-age').value = '30';
            document.getElementById('crew-weight').value = '70';
            document.getElementById('crew-health').value = 'good';
            // 重新加载模块并刷新数据
            await loadCrewModule();
            // 刷新总控制台数据以更新生存指数和预测
            await refreshData(window.charts);
        } else {
            showToast('❌ 添加失败: ' + (result.error || '未知错误'));
        }
    } catch (error) {
        console.error('Failed to add crew:', error);
        showToast('❌ 添加失败');
    }
}

async function applyNutritionSettings() {
    const calories = document.getElementById('crew-calories').value;
    const diet = document.getElementById('crew-diet').value;
    const allergies = document.getElementById('crew-allergies').value;
    
    try {
        const response = await fetch('/api/crew/nutrition', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ calories: parseInt(calories), diet, allergies })
        });
        const result = await response.json();
        if (result.success) {
            showToast(`✅ 营养设置已保存：${calories}千卡/天${diet ? '，饮食：'+diet : ''}${allergies ? '，过敏：'+allergies : ''}`);
            await refreshData(window.charts);
        } else {
            showToast('❌ 保存失败');
        }
    } catch (error) {
        console.error('Failed to update nutrition settings:', error);
        showToast('❌ 保存失败');
    }
}

async function applyActivitySchedule() {
    const schedule = document.getElementById('crew-daily-schedule').value;
    const restHours = document.getElementById('crew-rest-hours').value;
    const activityLevel = document.getElementById('crew-activity-adjustment').value;
    
    const levelText = activityLevel === 'low' ? '低消耗' : activityLevel === 'normal' ? '正常' : '高消耗';
    
    try {
        const response = await fetch('/api/crew/schedule', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ schedule, rest_hours: parseFloat(restHours), activity_adjustment: activityLevel })
        });
        const result = await response.json();
        if (result.success) {
            showToast(`✅ 日程安排已保存：休息${restHours}小时，${levelText}模式`);
            await refreshData(window.charts);
        } else {
            showToast('❌ 保存失败');
        }
    } catch (error) {
        console.error('Failed to update activity schedule:', error);
        showToast('❌ 保存失败');
    }
}

function displayCrewList(crew) {
    const list = document.getElementById('crew-list');
    if (!crew || crew.length === 0) {
        list.innerHTML = '<p style="color: #888;">暂无宇航员</p>';
        return;
    }
    
    list.innerHTML = crew.map(member => `
        <div style="padding: 10px; margin-bottom: 10px; background: rgba(0,243,255,0.1); border-radius: 5px; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <strong style="color: var(--tech-cyan);">${member.name}</strong>
                <div style="color: #fff; font-size: 12px;">年龄: ${member.age} | 体重: ${member.weight}kg</div>
            </div>
        </div>
    `).join('');
}

// AI预测与决策模块
async function loadAIPredictModule() {
    const container = document.getElementById('ai-predict-content');
    container.innerHTML = `
        <div style="background: rgba(0,0,0,0.3); padding: 20px; border-radius: 8px; margin-bottom: 20px;">
            <h3 style="color: var(--tech-cyan); margin-bottom: 15px;">
                <i class="fas fa-brain"></i> AI自动化级别
            </h3>
            <div style="display: grid; gap: 15px;">
                <select id="ai-level" style="padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                    <option value="manual">手动模式</option>
                    <option value="semi-auto" selected>半自动模式</option>
                    <option value="full-auto">全自动模式</option>
                </select>
                <button onclick="setAIAutomation()" style="padding: 10px 20px; background: var(--tech-cyan); color: #000; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">
                    <i class="fas fa-check"></i> 应用设置
                </button>
            </div>
        </div>
        
        <div style="background: rgba(0,0,0,0.3); padding: 20px; border-radius: 8px; margin-bottom: 20px;">
            <h3 style="color: var(--tech-cyan); margin-bottom: 15px;">
                <i class="fas fa-tasks"></i> 任务参数设置
            </h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                <div>
                    <label style="color: #fff; font-size: 12px;">宇航员人数</label>
                    <input type="number" id="task-crew-count" value="6" min="1" max="20" style="width: 100%; padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                </div>
                <div>
                    <label style="color: #fff; font-size: 12px;">任务时长 (天)</label>
                    <input type="number" id="task-duration" value="365" min="1" style="width: 100%; padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                </div>
                <div>
                    <label style="color: #fff; font-size: 12px;">活动强度</label>
                    <select id="task-activity-level" style="width: 100%; padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                        <option value="low">低强度</option>
                        <option value="normal" selected>正常</option>
                        <option value="high">高强度</option>
                    </select>
                </div>
                <div>
                    <label style="color: #fff; font-size: 12px;">补给间隔 (天)</label>
                    <input type="number" id="resupply-interval" value="90" min="7" style="width: 100%; padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                </div>
                <button onclick="applyTaskParameters()" style="padding: 10px 20px; background: var(--tech-cyan); color: #000; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; grid-column: 1 / -1;">
                    <i class="fas fa-check"></i> 应用参数
                </button>
            </div>
        </div>
        
        <div style="background: rgba(0,0,0,0.3); padding: 20px; border-radius: 8px; margin-bottom: 20px;">
            <h3 style="color: var(--tech-cyan); margin-bottom: 15px;">
                <i class="fas fa-flask"></i> 场景模拟器
            </h3>
            <div style="display: grid; gap: 15px;">
                <div>
                    <label style="color: #fff; font-size: 12px;">选择预设灾难场景</label>
                    <select id="scenario-preset" style="width: 100%; padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                        <option value="none">无场景</option>
                        <option value="solar-storm">太阳风暴</option>
                        <option value="oxygen-leak">氧气泄漏</option>
                        <option value="power-failure">能源危机</option>
                        <option value="cold-chain-failure">冷链故障</option>
                        <option value="hull-breach">舱体破损</option>
                    </select>
                </div>
                <div>
                    <label style="color: #fff; font-size: 12px;">风险概率 (%)</label>
                    <input type="range" id="scenario-risk" min="0" max="100" value="50" oninput="document.getElementById('val-scenario-risk').textContent=this.value+'%'" style="width: 100%; accent-color: var(--tech-cyan);">
                    <span id="val-scenario-risk" style="color: var(--tech-cyan);">50%</span>
                </div>
                <div>
                    <label style="color: #fff; font-size: 12px;">应对策略优先级</label>
                    <select id="response-strategy" style="width: 100%; padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                        <option value="survival-first">生存优先</option>
                        <option value="resource-preserve">资源保留</option>
                        <option value="mission-continue">任务继续</option>
                    </select>
                </div>
                <button onclick="runScenarioSimulation()" style="padding: 10px 20px; background: #ff9500; color: #000; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">
                    <i class="fas fa-play"></i> 运行模拟
                </button>
            </div>
        </div>
        
        <div style="background: rgba(0,0,0,0.3); padding: 20px; border-radius: 8px;">
            <h3 style="color: var(--tech-cyan); margin-bottom: 15px;">
                <i class="fas fa-sliders-h"></i> AI偏好配置
            </h3>
            <div style="display: grid; gap: 15px;">
                <div>
                    <label style="color: #fff; font-size: 12px;">风险承受度</label>
                    <input type="range" id="ai-risk-tolerance" min="0" max="100" value="50" oninput="document.getElementById('val-ai-risk').textContent=this.value+'%'" style="width: 100%; accent-color: var(--tech-cyan);">
                    <span id="val-ai-risk" style="color: var(--tech-cyan);">50%</span>
                </div>
                <button onclick="applyAIPreferences()" style="padding: 10px 20px; background: var(--tech-cyan); color: #000; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">
                    <i class="fas fa-check"></i> 应用偏好
                </button>
            </div>
        </div>
    `;
}

async function setAIAutomation() {
    const level = document.getElementById('ai-level').value;
    
    try {
        const response = await fetch('/api/ai/automation-level', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ level })
        });
        
        const result = await response.json();
        if (result.success) {
            showToast('✅ AI自动化级别已更新！');
            // 刷新数据以显示最新状态
            await refreshData(window.charts);
        }
    } catch (error) {
        console.error('Failed to set AI level:', error);
        showToast('❌ 更新失败');
    }
}

async function applyTaskParameters() {
    const crewCount = document.getElementById('task-crew-count').value;
    const duration = document.getElementById('task-duration').value;
    const activityLevel = document.getElementById('task-activity-level').value;
    const resupplyInterval = document.getElementById('resupply-interval').value;
    
    try {
        const response = await fetch('/api/ai/task-parameters', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                crew_count: parseInt(crewCount),
                duration: parseInt(duration),
                activity_level: activityLevel,
                resupply_interval: parseInt(resupplyInterval)
            })
        });
        const result = await response.json();
        if (result.success) {
            showToast(`✅ 任务参数已设置：${crewCount}人，${duration}天，${activityLevel === 'low' ? '低' : activityLevel === 'normal' ? '正常' : '高'}强度，补给间隔${resupplyInterval}天`);
            await refreshData(window.charts);
        } else {
            showToast('❌ 保存失败');
        }
    } catch (error) {
        console.error('Failed to update task parameters:', error);
        showToast(' 保存失败');
    }
}

async function runScenarioSimulation() {
    const scenario = document.getElementById('scenario-preset').value;
    const risk = document.getElementById('scenario-risk').value;
    const strategy = document.getElementById('response-strategy').value;
    
    if (scenario === 'none') {
        showToast('⚠️ 请先选择一个灾难场景');
        return;
    }
    
    const scenarioText = {
        'solar-storm': '太阳风暴',
        'oxygen-leak': '氧气泄漏',
        'power-failure': '能源危机',
        'cold-chain-failure': '冷链故障',
        'hull-breach': '舱体破损'
    }[scenario];
    
    const strategyText = {
        'survival-first': '生存优先',
        'resource-preserve': '资源保留',
        'mission-continue': '任务继续'
    }[strategy];
    
    try {
        const response = await fetch('/api/emergency/simulate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ scenario, severity: parseFloat(risk) / 10, strategy })
        });
        const result = await response.json();
        if (result.success) {
            showToast(`🧪 模拟运行完成：${scenarioText} | 策略：${strategyText}`);
            await refreshData(window.charts);
        } else {
            showToast('❌ 模拟失败');
        }
    } catch (error) {
        console.error('Failed to run simulation:', error);
        showToast('❌ 模拟失败');
    }
}

async function applyAIPreferences() {
    const riskTolerance = document.getElementById('ai-risk-tolerance').value;
    
    try {
        const response = await fetch('/api/ai/preferences', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ risk_tolerance: parseInt(riskTolerance) })
        });
        const result = await response.json();
        if (result.success) {
            showToast(`✅ AI偏好已设置：风险承受度${riskTolerance}%`);
            await refreshData(window.charts);
        } else {
            showToast('❌ 保存失败');
        }
    } catch (error) {
        console.error('Failed to update AI preferences:', error);
        showToast('❌ 保存失败');
    }
}

// 通信与报告模块
async function loadCommunicationModule() {
    const container = document.getElementById('communication-content');
    container.innerHTML = `
        <div style="background: rgba(0,0,0,0.3); padding: 20px; border-radius: 8px;">
            <h3 style="color: var(--tech-cyan); margin-bottom: 15px;">
                <i class="fas fa-file-alt"></i> 生成自定义报告
            </h3>
            <div style="display: grid; gap: 15px;">
                <select id="report-type" style="padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                    <option value="daily">每日报告</option>
                    <option value="weekly">每周报告</option>
                    <option value="survival">生存状态报告</option>
                    <option value="risk">风险分析报告</option>
                </select>
                <button onclick="generateCustomReport()" style="padding: 10px 20px; background: var(--tech-cyan); color: #000; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">
                    <i class="fas fa-file-export"></i> 生成报告
                </button>
                <div id="report-output" style="padding: 15px; background: rgba(0,0,0,0.5); border-radius: 5px; color: #fff; white-space: pre-wrap; min-height: 100px; display: none;"></div>
            </div>
        </div>
    `;
}

async function generateCustomReport() {
    const reportType = document.getElementById('report-type').value;
    const output = document.getElementById('report-output');
    
    output.style.display = 'block';
    output.innerHTML = '<p style="color: var(--tech-cyan);">⏳ 生成中...</p>';
    
    try {
        const response = await fetch('/api/reports/custom', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ type: reportType, depth: 'standard', focus_areas: ['survival', 'resources', 'crew'] })
        });
        
        const result = await response.json();
        if (result.success) {
            output.innerHTML = result.report;
        }
    } catch (error) {
        console.error('Failed to generate report:', error);
        output.innerHTML = '<p style="color: #ff4d4d;">❌ 生成失败</p>';
    }
}

// 系统设置模块
async function loadSettingsModule() {
    const container = document.getElementById('settings-content');
    container.innerHTML = `
        <div style="background: rgba(0,0,0,0.3); padding: 20px; border-radius: 8px;">
            <h3 style="color: var(--tech-cyan); margin-bottom: 15px;">
                <i class="fas fa-cog"></i> 系统设置
            </h3>
            <div style="display: grid; gap: 15px;">
                <div>
                    <label style="color: #fff; font-size: 12px;">刷新频率 (秒)</label>
                    <input type="number" id="setting-refresh" value="3" min="1" max="60" style="width: 100%; padding: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(0,243,255,0.3); border-radius: 5px; color: #fff;">
                </div>
                <button onclick="applySettings()" style="padding: 10px 20px; background: var(--tech-cyan); color: #000; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">
                    <i class="fas fa-check"></i> 保存设置
                </button>
            </div>
        </div>
    `;
}

async function applySettings() {
    const refreshRate = document.getElementById('setting-refresh').value;
    
    try {
        const response = await fetch('/api/system/settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refresh_rate: parseInt(refreshRate), display_mode: 'detailed' })
        });
        const result = await response.json();
        if (result.success) {
            showToast(`✅ 系统设置已保存：刷新频率${refreshRate}秒`);
            await refreshData(window.charts);
        } else {
            showToast('❌ 保存失败');
        }
    } catch (error) {
        console.error('Failed to update settings:', error);
        showToast('❌ 保存失败');
    }
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
            await refreshData(window.charts);
        } else {
            showToast('❌ ' + (result.error || '更新失败'));
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
    refreshInterval = setInterval(() => refreshData(charts), 10000);
    console.log('Auto-refresh started (interval: 10s)');
}

// 停止自动刷新
function stopAutoRefresh() {
    if (refreshInterval) {
        clearInterval(refreshInterval);
        refreshInterval = null;
        console.log('Auto-refresh stopped.');
    }
}

// ==================== 模拟控制 ====================
function startSimulation() {
    // 每分钟执行一次模拟（+1天）
    simulationTimer = setInterval(async () => {
        try {
            const response = await fetch('/api/simulate_step', { method: 'POST' });
            const data = await response.json();
            
            if (data.success) {
                console.log(`Simulation step completed: Day ${data.state.mission_day}`);
                // 保存状态到localStorage
                saveStateToLocalStorage(data.state);
                // 立即刷新界面
                if (window.charts) {
                    await refreshData(window.charts);
                }
            }
        } catch (error) {
            console.error('Simulation step failed:', error);
        }
    }, 300000); // 300秒 = 5分钟
    
    console.log('Simulation timer started (1 day per 5 minutes)');
}

function stopSimulation() {
    if (simulationTimer) {
        clearInterval(simulationTimer);
        simulationTimer = null;
        console.log('Simulation timer stopped.');
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
            await refreshData(window.charts);
        } else {
            showToast('❌ ' + (result.error || '调整失败'));
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
        
        console.log('=== 数据刷新 ===');
        console.log('生存状态:', survivalStatus);
        console.log('食物系统:', foodSystem);
        console.log('医疗系统:', medicalSystem);
        console.log('环境系统:', environment);
        console.log('能源系统:', energy);
        
        // 1. 更新紧急协议模式
        if (survivalStatus.emergency_mode) {
            triggerEmergencyAnimation();
        } else {
            exitEmergencyAnimation();
        }
        
        // 2. 更新仪表盘数据（总控制台雷达图）
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
        
        // 5.1 更新AI饮食建议
        const dietAdviceEl = document.getElementById('diet-advice-display');
        if (dietAdviceEl && survivalStatus.diet_advice) {
            dietAdviceEl.textContent = survivalStatus.diet_advice;
        }
        
        // 6. 更新预测时间线（基于后端计算的结果）
        if (predictionChart && survivalStatus.predictions) {
            predictionChart.setOption({
                xAxis: { data: ['D+30', 'D+60', 'D+90', 'D+120'] },
                series: [{ data: survivalStatus.predictions }]
            });
        }
        
        // 7. 根据当前模块更新对应图表（传递完整数据）
        if (currentModule === 'food') {
            // 食物页面：合并生存状态和食物系统数据
            updateFoodView({...survivalStatus, ...foodSystem});
        } else if (currentModule === 'medical') {
            updateMedicalView({...survivalStatus, ...medicalSystem});
        } else if (currentModule === 'energy') {
            updateEnergyView({...survivalStatus, ...energy});
        } else if (currentModule === 'env') {
            updateEnvView({...survivalStatus, ...environment});
        }
        
        // 8. 更新AI日志
        if (aiLogs && aiLogs.length > 0) {
            updateAILogs(aiLogs);
        }
        
        console.log('=== 数据刷新完成 ===');
        
    } catch (error) {
        console.error('Error refreshing data:', error);
    }
}

// 页面加载完成后初始化
window.onload = () => {
    init();
};
