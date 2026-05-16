// 图表逻辑模块 - 负责ECharts图表的初始化和更新
let mainChart, gaugeChart, predictionChart;

const initCharts = () => {
    mainChart = echarts.init(document.getElementById('main-chart-container'));
    gaugeChart = echarts.init(document.getElementById('gauge-chart'));
    predictionChart = echarts.init(document.getElementById('prediction-chart'));
    
    // 初始化仪表盘配置
    const gaugeOption = {
        series: [{
            type: 'gauge',
            startAngle: 180,
            endAngle: 0,
            min: 0,
            max: 100,
            splitNumber: 5,
            itemStyle: { color: '#00f3ff' },
            progress: {
                show: true,
                width: 18
            },
            pointer: {
                icon: 'path://M12.8,0.7l12,40.1H0.7L12.8,0.7z',
                length: '12%',
                width: 20,
                offsetCenter: [0, '-60%'],
                itemStyle: { color: 'auto' }
            },
            axisLine: {
                lineStyle: {
                    width: 18,
                    color: [[1, 'rgba(0,243,255,0.3)']]
                }
            },
            axisTick: { show: false },
            splitLine: { show: false },
            axisLabel: { show: false },
            title: { show: false },
            detail: {
                valueAnimation: true,
                fontSize: 40,
                offsetCenter: [0, '0%'],
                color: '#00f3ff',
                formatter: '{value}%'
            },
            data: [{ value: 85 }]
        }]
    };
    gaugeChart.setOption(gaugeOption);
    
    // 初始化预测时间线配置
    const predictionOption = {
        title: { text: '生存指数预测', textStyle: { color: '#fff', fontSize: 14 } },
        tooltip: { trigger: 'axis' },
        xAxis: {
            type: 'category',
            data: ['D+30', 'D+60', 'D+90', 'D+120'],
            axisLabel: { color: '#fff' }
        },
        yAxis: {
            type: 'value',
            min: 0,
            max: 100,
            axisLabel: { color: '#fff' },
            splitLine: { lineStyle: { color: '#333' } }
        },
        series: [{
            type: 'line',
            smooth: true,
            data: [70, 60, 50, 40],
            itemStyle: { color: '#00f3ff' },
            areaStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    { offset: 0, color: 'rgba(0, 243, 255, 0.5)' },
                    { offset: 1, color: 'rgba(0, 243, 255, 0.1)' }
                ])
            },
            markLine: {
                symbol: ['none', 'none'],
                label: { formatter: '生存警戒线 (30%)', position: 'insideEndTop', color: '#ff4d4d', fontSize: 10 },
                lineStyle: { color: '#ff4d4d', type: 'dashed', width: 2 },
                data: [{ yAxis: 30 }]
            }
        }]
    };
    predictionChart.setOption(predictionOption);
    
    updateDashboardView();
    return { mainChart, gaugeChart, predictionChart };
};

const updateDashboardView = (data) => {
    document.getElementById('module-title').innerText = "总控制台 DASHBOARD";
    
    // 如果没有传入数据，使用默认值（首次加载时）
    const values = data ? [
        data.food_stability || 80,
        data.medical_safety || 90,
        data.energy_level || 70,
        data.oxygen_level || 95,
        data.water_reserve || 85
    ] : [80, 90, 70, 95, 85];
    
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
            data: [{ value: values, name: '当前状态' }],
            itemStyle: { color: '#00f3ff' },
            areaStyle: { color: 'rgba(0, 243, 255, 0.3)' }
        }]
    };
    mainChart.setOption(option);
};

const updateFoodView = (data) => {
    document.getElementById('module-title').innerText = "食物资源系统 FOOD RESOURCES";
    
    // 从categories中提取动态数据，如果没有则使用计算值
    const categories = data.categories || [];
    const frozenFood = categories.find(c => c.name === '冷冻食品')?.value || (data.food_stability * 0.6);
    const dehydratedFood = categories.find(c => c.name === '脱水食品')?.value || (data.food_stability * 0.4);
    
    const option = {
        title: { text: '分类库存与营养分析', textStyle: { color: '#fff' } },
        tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
        xAxis: { type: 'category', data: ['冷冻储备', '干粮库存', '高蛋白', '紧急营养', '水资源'], axisLabel: { color: '#fff' } },
        yAxis: { type: 'value', axisLabel: { color: '#fff' }, splitLine: { lineStyle: { color: '#333' } } },
        series: [{
            data: [
                { value: data.food_stability || 70, itemStyle: { color: '#00f3ff' } },
                { value: dehydratedFood || 85, itemStyle: { color: '#0066ff' } },
                { value: data.protein_level || 60, itemStyle: { color: '#ff9f43' } },
                { value: frozenFood || 95, itemStyle: { color: '#ff4d4d' } },
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
            data: [
                data.temperature || -70,
                (data.temperature || -70) + 5,
                -196,
                4
            ],
            type: 'bar',
            itemStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{ offset: 0, color: '#00f3ff' }, { offset: 1, color: '#0066ff' }]) }
        }]
    };
    mainChart.setOption(option, true);
};

const updateEnergyView = (data) => {
    document.getElementById('module-title').innerText = "能源与环境系统 ENERGY & ENV";
    
    // 使用动态的能源分配数据
    const distribution = data.energy_distribution || {
        medical: 30,
        food: 25,
        environment: 25,
        other: 20
    };
    
    const option = {
        title: { text: `备用能源剩余: ${data.backup_power_hours}h | 宇航员食谱: ${data.diet_advice}`, textStyle: { color: '#fff', fontSize: 12 } },
        legend: { top: 'bottom', textStyle: { color: '#fff' } },
        series: [{
            type: 'pie',
            radius: ['40%', '70%'],
            data: [
                { value: distribution.medical || 30, name: '医疗冷链' },
                { value: distribution.food || 25, name: '食物系统' },
                { value: distribution.environment || 25, name: '环境控制' },
                { value: distribution.other || 20, name: '其他系统' }
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
                data.co2 || 0.04,
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

const updateAllCharts = (data) => {
    // 更新雷达图
    const radarOption = {
        series: [{
            data: [{
                value: [
                    data.food_stability || 80,
                    data.medical_safety || 90,
                    data.energy_level || 70,
                    data.oxygen_level || 95,
                    data.water_reserve || 85
                ],
                name: '当前状态'
            }]
        }]
    };
    mainChart.setOption(radarOption);
    
    // 更新仪表盘 - 使用完整配置
    gaugeChart.setOption({
        series: [{
            type: 'gauge',
            detail: {
                valueAnimation: true,
                fontSize: 40,
                offsetCenter: [0, '0%'],
                color: '#00f3ff',
                formatter: '{value}%'
            },
            data: [{ value: Math.round(data.survival_index || 85) }]
        }]
    });
    
    // 更新预测时间线 - 使用完整配置
    predictionChart.setOption({
        xAxis: { 
            type: 'category',
            data: ['D+30', 'D+60', 'D+90', 'D+120'],
            axisLabel: { color: '#fff' }
        },
        yAxis: {
            type: 'value',
            min: 0,
            max: 100,
            axisLabel: { color: '#fff' },
            splitLine: { lineStyle: { color: '#333' } }
        },
        series: [{
            type: 'line',
            smooth: true,
            data: data.predictions || [70, 60, 50, 40],
            itemStyle: { color: '#00f3ff' },
            areaStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    { offset: 0, color: 'rgba(0, 243, 255, 0.5)' },
                    { offset: 1, color: 'rgba(0, 243, 255, 0.1)' }
                ])
            }
        }]
    });
};
