// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 初始化购物车相关功能
    initCartFunctions();

    // 初始化表单验证
    initFormValidation();

    // 添加页面滚动动画
    initScrollAnimations();

    // 关闭通知消息
    initAlertClosing();
});

// 购物车相关功能
function initCartFunctions() {
    // 为"加入购物车"按钮添加动画效果
    const addToCartButtons = document.querySelectorAll('form[action*="cart/add"] button');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const originalText = this.innerHTML;
            this.disabled = true;
            this.innerHTML = '<i class="bi bi-spinner bi-spin"></i> 加入中...';

            // 模拟加载延迟
            setTimeout(() => {
                this.innerHTML = '<i class="bi bi-check"></i> 已加入';
                setTimeout(() => {
                    this.innerHTML = originalText;
                    this.disabled = false;
                }, 1500);
            }, 800);
        });
    });

    // 为"移除"按钮添加确认提示
    const removeButtons = document.querySelectorAll('a[href*="cart/remove"]');
    removeButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('确定要从购物车中移除这件商品吗？')) {
                e.preventDefault();
            }
        });
    });
}

// 表单验证
function initFormValidation() {
    // 注册表单验证
    const registerForm = document.querySelector('form[action*="accounts/register"]');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            const password1 = this.querySelector('input[name="password1"]').value;
            const password2 = this.querySelector('input[name="password2"]').value;

            // 简单的密码匹配验证
            if (password1 !== password2) {
                e.preventDefault();
                alert('两次输入的密码不一致，请重新输入');
                return false;
            }

            // 密码长度验证
            if (password1.length < 8) {
                e.preventDefault();
                alert('密码长度不能少于8个字符');
                return false;
            }

            return true;
        });
    }
}

// 页面滚动动画
function initScrollAnimations() {
    // 监听滚动事件，为进入视口的元素添加动画
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    // 对产品卡片应用动画
    document.querySelectorAll('.card').forEach(card => {
        observer.observe(card);
    });
}

// 自动关闭通知消息
function initAlertClosing() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        // 5秒后自动关闭
        setTimeout(() => {
            alert.classList.add('fade');
            setTimeout(() => {
                alert.remove();
            }, 500);
        }, 5000);
    });
}

// 搜索框自动完成功能
function initSearchAutocomplete() {
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const query = this.value.trim();
            if (query.length < 2) return;

            // 这里可以添加AJAX请求获取搜索建议
            console.log('搜索建议:', query);
            // 实际项目中可以使用fetch发送请求到后端
            /*
            fetch(`/products/search-suggest/?q=${query}`)
                .then(response => response.json())
                .then(data => {
                    // 显示搜索建议
                    console.log(data);
                });
            */
        });
    }
}
