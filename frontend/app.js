// 初始化 Three.js 星空背景
const initStarfield = () => {
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ alpha: true });
    
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.getElementById('starfield').appendChild(renderer.domElement);

    const geometry = new THREE.BufferGeometry();
    const vertices = [];
    for (let i = 0; i < 1000; i++) {
        vertices.push(THREE.MathUtils.randFloatSpread(2000));
        vertices.push(THREE.MathUtils.randFloatSpread(2000));
        vertices.push(THREE.MathUtils.randFloatSpread(2000));
    }
    geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
    const material = new THREE.PointsMaterial({ color: 0x88ccff, size: 2 });
    const stars = new THREE.Points(geometry, material);
    scene.add(stars);

    camera.position.z = 500;

    const animate = () => {
        requestAnimationFrame(animate);
        stars.rotation.x += 0.0005;
        stars.rotation.y += 0.0005;
        renderer.render(scene, camera);
    };
    animate();
};

// 初始化 ECharts 图表
let currentModule = 'dashboard';
let mainChart, gaugeChart, predictionChart;

const initCharts = () => {
    mainChart = echarts.init(document.getElementById('main-chart-container'));
    gaugeChart = echarts.init(document.getElementById('gauge-chart'));
    predictionChart = echarts.init(document.getElementById('prediction-chart'));
    
    updateDashboardView();
    return { mainChart, gaugeChart, predictionChart };
};

const updateDashboardView = () => {
    document.getElementById('module-title').innerText = "总控制台 DASHBOARD";
    const option = {
        radar: {
            indicator: [
                { name: '食物稳定性', max: 100 },
                { name: '医疗安全性', max: 100 },
                { name: '能源持续性', max: 100 },
                { name: '氧气安全', max: 100 },
                { name: '水资源', max: 100 }
            ],
            axisName: { color: '#00f3ff' },
            splitArea: { areaStyle: { color: ['rgba(0,243,255,0.1)', 'rgba(0,243,255,0.2)'] } }
        },
        series: [{
            type: 'radar',
            data: [{ value: [80, 90, 70, 95, 85], name: '当前状态' }],
            itemStyle: { color: '#00f3ff' },
            areaStyle: { color: 'rgba(0, 243, 255, 0.3)' }
        }]
    };
    mainChart.setOption(option);
};

const updateFoodView = (data) => {
    document.getElementById('module-title').innerText = "食物资源系统 FOOD RESOURCES";
    const option = {
        title: { text: '分类库存与营养分析', textStyle: { color: '#fff' } },
        tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
        xAxis: { type: 'category', data: ['冷冻储备', '干粮库存', '高蛋白', '紧急营养', '水资源'], axisLabel: { color: '#fff' } },
        yAxis: { type: 'value', axisLabel: { color: '#fff' }, splitLine: { lineStyle: { color: '#333' } } },
        series: [{
            data: [
                { value: data.food_stability || 70, itemStyle: { color: '#00f3ff' } },
                { value: 85, itemStyle: { color: '#0066ff' } },
                { value: data.protein_level || 60, itemStyle: { color: '#ff9f43' } },
                { value: 95, itemStyle: { color: '#ff4d4d' } },
                { value: data.water_reserve || 80, itemStyle: { color: '#00ccff' } }
            ],
            type: 'bar',
            label: { show: true, position: 'top', color: '#fff' }
        }]
    };
    mainChart.setOption(option, true);
};

const updateMedicalView = (data) => {
    document.getElementById('module-title').innerText = "医疗冷链系统 MEDICAL COLD-CHAIN";
    const option = {
        title: { text: '关键物资温控状态', textStyle: { color: '#fff' } },
        xAxis: { type: 'category', data: ['疫苗', '血浆', '生物样本', '急救药'], axisLabel: { color: '#fff' } },
        yAxis: { type: 'value', name: '温度 (°C)', axisLabel: { color: '#fff' }, splitLine: { lineStyle: { color: '#333' } } },
        series: [{
            data: [-70, -40, -196, 4],
            type: 'bar',
            itemStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{ offset: 0, color: '#00f3ff' }, { offset: 1, color: '#0066ff' }]) }
        }]
    };
    mainChart.setOption(option, true);
};

const updateEnergyView = (data) => {
    document.getElementById('module-title').innerText = "能源与环境系统 ENERGY & ENV";
    const option = {
        title: { text: `备用能源剩余: ${data.backup_power_hours}h | 宇航员食谱: ${data.diet_advice}`, textStyle: { color: '#fff', fontSize: 12 } },
        legend: { top: 'bottom', textStyle: { color: '#fff' } },
        series: [{
            type: 'pie',
            radius: ['40%', '70%'],
            data: [
                { value: 40, name: '冷链系统' },
                { value: 30, name: '生命维持' },
                { value: 20, name: 'AI 核心' },
                { value: 10, name: '通讯导航' }
            ],
            label: { color: '#fff' }
        }]
    };
    mainChart.setOption(option, true);
};

const updateEnvView = (data) => {
    document.getElementById('module-title').innerText = "环境控制系统 ENVIRONMENTAL CONTROL";
    const option = {
        title: { text: '舱内环境实时波形', textStyle: { color: '#fff' } },
        xAxis: { type: 'category', data: ['O2', 'CO2', 'HUM', 'PRES', 'RAD'], axisLabel: { color: '#fff' } },
        yAxis: { type: 'value', splitLine: { lineStyle: { color: '#333' } }, axisLabel: { color: '#fff' } },
        series: [{
            data: [
                data.oxygen_level,
                0.04,
                data.humidity,
                data.pressure,
                data.radiation_level
            ],
            type: 'line',
            smooth: true,
            areaStyle: { opacity: 0.3 },
            itemStyle: { color: '#00f3ff' }
        }]
    };
    mainChart.setOption(option, true);
};

// WebSocket 连接与数据更新
const connectWebSocket = (charts) => {
    const ws = new WebSocket('ws://localhost:8001/ws');
    const logContainer = document.getElementById('ai-logs');

    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        // 1. 紧急协议模式切换
        if (data.emergency_mode) {
            document.body.classList.add('emergency-mode');
            document.getElementById('emergency-overlay').style.display = 'block';
            gsap.fromTo("#emergency-overlay", { opacity: 0 }, { opacity: 1, duration: 0.5, yoyo: true, repeat: -1 });
        } else {
            document.body.classList.remove('emergency-mode');
            document.getElementById('emergency-overlay').style.display = 'none';
        }

        // 2. 更新仪表盘
        charts.gaugeChart.setOption({ series: [{ data: [{ value: Math.round(data.survival_index) }] }] });
        
        // 2.1 更新顶部状态栏数据
        document.getElementById('crew-display').innerText = data.crew_count;
        document.getElementById('stability-display').innerText = Math.round(data.survival_index) + '%';
        
        // 2.2 计算并显示预计生存时间
        const estSurvivalDays = Math.floor(data.survival_index * 1.8);
        const survivalTimeEl = document.getElementById('est-survival-days');
        if (survivalTimeEl) {
            gsap.to(survivalTimeEl, {
                innerText: estSurvivalDays,
                duration: 1.5,
                snap: { innerText: 1 },
                onUpdate: function() {
                    this.targets()[0].innerText = Math.ceil(this.targets()[0].innerText) + ' DAYS';
                }
            });
        }
        
        // 3. 更新预测时间线
        charts.predictionChart.setOption({
            xAxis: { data: ['D+30', 'D+60', 'D+90', 'D+120'] },
            series: [{ data: data.predictions }]
        });

        // 4. 更新当前模块视图
        if (currentModule === 'food') updateFoodView(data);
        else if (currentModule === 'medical') updateMedicalView(data);
        else if (currentModule === 'energy') updateEnergyView(data);
        else if (currentModule === 'env') updateEnvView(data);
        else updateDashboardView();
        
        // 5. 更新天数 (增加数字滚动动画)
        const dayDisplay = document.getElementById('day-display');
        gsap.to(dayDisplay, {
            innerText: data.mission_day,
            duration: 1,
            snap: { innerText: 1 },
            onUpdate: function() {
                this.targets()[0].innerText = String(Math.ceil(this.targets()[0].innerText)).padStart(3, '0');
            }
        });

        // 6. 更新日志（增加 AI 执行动作高亮）
        data.logs.forEach(log => {
            const div = document.createElement('div');
            div.className = 'log-entry';
            
            // 根据日志类型设置不同样式
            if (log.startsWith('✓')) {
                div.style.color = '#00f3ff';
                div.style.fontWeight = 'bold';
            } else if (log.includes('警告') || log.includes('⚠️')) {
                div.style.color = '#ff9f43';
            } else if (log.includes('能源联动') || log.includes('辐射联动') || log.includes('食物联动')) {
                div.style.color = '#ff4d4d';
                div.style.borderLeft = '3px solid #ff4d4d';
                div.style.paddingLeft = '10px';
            }
            
            div.innerText = `> ${log}`;
            logContainer.prepend(div);
            if (logContainer.children.length > 15) logContainer.lastChild.remove();
        });

        // 7. 更新历史时间线
        const historyList = document.getElementById('history-list');
        const historyItem = document.createElement('li');
        historyItem.innerText = `Day ${data.mission_day}: ${data.logs[0] || 'System Check'}`;
        historyList.prepend(historyItem);
        if (historyList.children.length > 10) historyList.lastChild.remove();
    };
};

// 导航栏交互逻辑
document.addEventListener('DOMContentLoaded', () => {
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
        });
    });
});

window.onload = () => {
    initStarfield();
    const charts = initCharts();
    connectWebSocket(charts);
};
