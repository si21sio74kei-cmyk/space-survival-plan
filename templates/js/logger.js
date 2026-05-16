// 日志控制工具 - 生产环境禁用console输出
const DEBUG = false; // 设置为true启用调试日志

const Logger = {
    log: (...args) => {
        if (DEBUG) {
            console.log('[DEBUG]', ...args);
        }
    },
    
    error: (...args) => {
        // 错误始终记录，但生产环境可以发送到错误追踪服务
        console.error('[ERROR]', ...args);
    },
    
    warn: (...args) => {
        if (DEBUG) {
            console.warn('[WARN]', ...args);
        }
    },
    
    info: (...args) => {
        if (DEBUG) {
            console.info('[INFO]', ...args);
        }
    }
};

// 导出供其他模块使用
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Logger;
}
