function initScrollProgress() {
    var root = document.querySelector('.scroll-progress');
    var fill = root && root.querySelector('.scroll-progress__fill');
    if (!fill) return;

    var ticking = false;
    function update() {
        ticking = false;
        var el = document.documentElement;
        var scrollable = el.scrollHeight - el.clientHeight;
        var p = scrollable <= 0 ? 0 : el.scrollTop / scrollable;
        if (p < 0) p = 0;
        if (p > 1) p = 1;
        fill.style.transform = 'scaleX(' + p + ')';
    }

    function onViewportChange() {
        if (!ticking) {
            ticking = true;
            requestAnimationFrame(update);
        }
    }

    window.addEventListener('scroll', onViewportChange, { passive: true });
    window.addEventListener('resize', onViewportChange, { passive: true });
    update();
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initScrollProgress);
} else {
    initScrollProgress();
}

// Mobile nav toggle
const toggle = document.querySelector('.nav-toggle');
const navLinks = document.querySelector('.nav-links');
if (toggle && navLinks) {
    toggle.addEventListener('click', () => navLinks.classList.toggle('open'));
}

// Auto-dismiss messages
document.querySelectorAll('.message').forEach(el => {
    setTimeout(() => el.style.opacity = '0', 4000);
    setTimeout(() => el.remove(), 4500);
});
