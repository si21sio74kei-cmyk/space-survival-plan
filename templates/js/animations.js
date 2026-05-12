// 动画逻辑模块 - 负责Three.js星空背景和GSAP动画
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

const animateNumber = (element, targetValue, duration = 1.5) => {
    if (!element) return;
    
    gsap.to(element, {
        innerText: targetValue,
        duration: duration,
        snap: { innerText: 1 },
        onUpdate: function() {
            this.targets()[0].innerText = Math.ceil(this.targets()[0].innerText);
        }
    });
};

// 带动画和 suffix 的数字更新（例如 "143 DAYS"）
const animateNumberWithSuffix = (element, targetValue, suffix = '', duration = 1.5) => {
    if (!element) return;
    
    gsap.to(element, {
        innerText: targetValue,
        duration: duration,
        snap: { innerText: 1 },
        onUpdate: function() {
            this.targets()[0].innerText = Math.ceil(this.targets()[0].innerText) + suffix;
        }
    });
};

const triggerEmergencyAnimation = () => {
    document.body.classList.add('emergency-mode');
    const overlay = document.getElementById('emergency-overlay');
    if (overlay) {
        overlay.style.display = 'block';
        gsap.fromTo(overlay, 
            { opacity: 0 }, 
            { opacity: 1, duration: 0.5, yoyo: true, repeat: -1 }
        );
    }
};

const exitEmergencyAnimation = () => {
    document.body.classList.remove('emergency-mode');
    const overlay = document.getElementById('emergency-overlay');
    if (overlay) {
        overlay.style.display = 'none';
        gsap.killTweensOf(overlay);
    }
};
