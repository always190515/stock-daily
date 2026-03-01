// 股票热点日报 - 简单的交互
console.log('股票热点日报已加载');

// 添加点击效果
document.querySelectorAll('.sector-item, .news-item').forEach(item => {
    item.addEventListener('click', function() {
        this.style.transform = 'scale(0.98)';
        setTimeout(() => {
            this.style.transform = '';
        }, 150);
    });
});
