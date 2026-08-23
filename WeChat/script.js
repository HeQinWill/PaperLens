// 获取页面元素
const contentDiv = document.getElementById("content");
const prevLink = document.getElementById("prev-link");
const nextLink = document.getElementById("next-link");
const lastUpdateSpan = document.getElementById("last-update");
const datePicker = document.getElementById("date-picker");
const bannerContainer = document.getElementById("banner-container");
const toastContainer = document.getElementById("toast-container");
const brandLink = document.getElementById("brand-link");

// 运行时状态与缓存
let currentDate = null;
let isLoading = false;
const existingDates = new Set();
const missingDates = new Set();
const contentCache = new Map();

// 确保 wechat.css 样式表被加载到页面头部（解决 innerHTML 注入样式不生效问题）
function ensureWechatCss() {
    if (!document.querySelector('link[href="wechat.css"], link[href="./wechat.css"], link[data-role="wechat-css"]')) {
        const link = document.createElement("link");
        link.rel = "stylesheet";
        link.href = "wechat.css";
        link.setAttribute("data-role", "wechat-css");
        document.head.appendChild(link);
    }
}

// 获取格式化日期，格式为 YYYYMMDD
function getFormattedDate(offset = 0) {
    const date = new Date();
    
    // 获取当前 UTC 时间的小时（24小时制）
    const utcHour = date.getUTCHours();
    // 判断 UTC 时间是否在 05 点之前
    if (utcHour < 5) {
        // 如果在 05 点之前，使用前一天的日期
        offset = -1;
    }
    
    date.setDate(date.getDate() + offset); // 偏移日期
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");
    return `${year}${month}${day}`; // 返回 YYYYMMDD 格式
}

// 从 Date 对象生成 YYYYMMDD 格式
function getFormattedDateFromDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");
    return `${year}${month}${day}`;
}

// 解析 YYYYMMDD 为本地 Date 对象
function parseDateKey(dateKey) {
    const year = parseInt(dateKey.slice(0, 4), 10);
    const month = parseInt(dateKey.slice(4, 6), 10) - 1;
    const day = parseInt(dateKey.slice(6, 8), 10);
    return new Date(year, month, day);
}

// 格式化 YYYYMMDD 为 YYYY-MM-DD (用于 input[type="date"] 和显示)
function formatToInputDate(dateKey) {
    return `${dateKey.slice(0, 4)}-${dateKey.slice(4, 6)}-${dateKey.slice(6, 8)}`;
}

// 将 YYYY-MM-DD 转换为 YYYYMMDD
function parseFromInputDate(inputDate) {
    return inputDate.replace(/-/g, "");
}

// 显示轻量 Toast 提示
function showToast(message) {
    if (!toastContainer) return;
    const toast = document.createElement("div");
    toast.className = "toast-msg";
    toast.textContent = message;
    toastContainer.appendChild(toast);
    setTimeout(() => {
        if (toast.parentElement) {
            toast.parentElement.removeChild(toast);
        }
    }, 2500);
}

// 显示顶部提示横幅
function showBanner(message) {
    if (!bannerContainer) return;
    bannerContainer.innerHTML = `
        <div class="alert-banner">
            <div class="alert-banner-content">
                <span>ℹ️ ${message}</span>
            </div>
            <button class="banner-close-btn" aria-label="关闭提示" onclick="this.closest('.alert-banner').remove()">&times;</button>
        </div>
    `;
}

// 清除顶部提示横幅
function clearBanner() {
    if (bannerContainer) {
        bannerContainer.innerHTML = "";
    }
}

// 加载状态切换
function setLoading(loading) {
    isLoading = loading;
    if (prevLink) prevLink.style.pointerEvents = loading ? "none" : "";
    if (nextLink) nextLink.style.pointerEvents = loading ? "none" : "";
    if (datePicker) datePicker.disabled = loading;
}

// 拉取指定日期的 HTML 文件
async function fetchDateFile(dateKey) {
    if (contentCache.has(dateKey)) {
        return contentCache.get(dateKey);
    }
    if (missingDates.has(dateKey)) {
        return null;
    }

    try {
        const response = await fetch(`${dateKey}.html`);
        if (response.ok) {
            const html = await response.text();
            existingDates.add(dateKey);
            contentCache.set(dateKey, html);
            return html;
        } else {
            missingDates.add(dateKey);
            return null;
        }
    } catch (err) {
        missingDates.add(dateKey);
        return null;
    }
}

// 探测指定方向上最近存在的日期（最多探测 maxDays 天）
async function findExistingDate(startDateKey, direction, maxDays = 30) {
    const startDate = parseDateKey(startDateKey);
    const todayKey = getFormattedDate();
    const todayDate = parseDateKey(todayKey);

    for (let i = 1; i <= maxDays; i++) {
        const probeDate = new Date(startDate);
        probeDate.setDate(startDate.getDate() + i * direction);
        const probeKey = getFormattedDateFromDate(probeDate);

        // 如果向未来探测且超出了今天，直接终止探测
        if (direction > 0 && probeDate > todayDate) {
            break;
        }

        const html = await fetchDateFile(probeKey);
        if (html) {
            return { dateKey: probeKey, html };
        }
    }
    return null;
}

// 渲染注入指定日期的内容
function applyDateContent(dateKey, html) {
    currentDate = dateKey;
    ensureWechatCss();
    contentDiv.innerHTML = html;

    if (lastUpdateSpan) {
        lastUpdateSpan.textContent = dateKey;
    }
    if (datePicker) {
        datePicker.value = formatToInputDate(dateKey);
    }

    // 隐藏所有微信端导出按钮
    const exportButtons = contentDiv.querySelectorAll('.export-button, .export-all-container');
    exportButtons.forEach(button => {
        button.style.display = 'none';
    });

    updateNavigation(dateKey);
    window.scrollTo({ top: 0, behavior: 'instant' });
}

// 更新导航链接状态
function updateNavigation(currentDateStr) {
    const todayKey = getFormattedDate();
    if (currentDateStr >= todayKey) {
        nextLink.classList.add("disabled");
        nextLink.setAttribute("aria-disabled", "true");
    } else {
        nextLink.classList.remove("disabled");
        nextLink.removeAttribute("aria-disabled");
    }

    prevLink.href = `#${currentDateStr}`;
    nextLink.href = `#${currentDateStr}`;
}

// 向前翻页事件处理
async function handlePrev() {
    if (!currentDate || isLoading) return;
    setLoading(true);
    const result = await findExistingDate(currentDate, -1, 9999);
    setLoading(false);

    if (result) {
        clearBanner();
        applyDateContent(result.dateKey, result.html);
    } else {
        showToast("没有更早的推送了");
    }
}

// 向后翻页事件处理
async function handleNext() {
    if (!currentDate || isLoading) return;
    const todayKey = getFormattedDate();
    if (currentDate >= todayKey) {
        showToast("已是最新一期推送");
        return;
    }

    setLoading(true);
    const result = await findExistingDate(currentDate, 1, 9999);
    setLoading(false);

    if (result) {
        clearBanner();
        applyDateContent(result.dateKey, result.html);
    } else {
        showToast("没有更新的推送了");
    }
}

// 日期选择器切换事件处理
async function handleDatePickerChange() {
    if (!datePicker || !datePicker.value || isLoading) return;
    const selectedKey = parseFromInputDate(datePicker.value);
    if (selectedKey === currentDate) return;

    setLoading(true);
    const html = await fetchDateFile(selectedKey);
    setLoading(false);

    if (html) {
        clearBanner();
        applyDateContent(selectedKey, html);
    } else {
        showToast(`${datePicker.value} 暂无推送内容`);
        if (currentDate) {
            datePicker.value = formatToInputDate(currentDate);
        }
    }
}

// 尝试加载指定日期的文件
async function loadDateFile(date) {
    setLoading(true);
    const html = await fetchDateFile(date);
    if (html) {
        setLoading(false);
        clearBanner();
        applyDateContent(date, html);
        return;
    }

    // 文件不存在，尝试向过去回溯探测
    const fallback = await findExistingDate(date, -1, 9999);
    setLoading(false);
    if (fallback) {
        showBanner(`${formatToInputDate(date)} 暂无推送，已跳转至 ${formatToInputDate(fallback.dateKey)}`);
        applyDateContent(fallback.dateKey, fallback.html);
    } else {
        showToast(`${formatToInputDate(date)} 暂无推送`);
    }
}

// 初始化加载
async function init() {
    // 绑定事件监听
    if (prevLink) {
        prevLink.addEventListener("click", (e) => {
            e.preventDefault();
            handlePrev();
        });
    }

    if (nextLink) {
        nextLink.addEventListener("click", (e) => {
            e.preventDefault();
            handleNext();
        });
    }

    if (datePicker) {
        datePicker.addEventListener("change", handleDatePickerChange);
    }

    if (brandLink) {
        brandLink.addEventListener("click", (e) => {
            e.preventDefault();
            loadInitialDate();
        });
    }

    await loadInitialDate();
}

// 首次加载（当天若不存在则自动回退）
async function loadInitialDate() {
    const todayKey = getFormattedDate();
    if (datePicker) {
        datePicker.max = formatToInputDate(todayKey);
    }

    setLoading(true);
    const todayHtml = await fetchDateFile(todayKey);
    if (todayHtml) {
        setLoading(false);
        clearBanner();
        applyDateContent(todayKey, todayHtml);
        return;
    }

    // 当天 404，向过去回溯探测最近一期
    const fallback = await findExistingDate(todayKey, -1, 9999);
    setLoading(false);
    if (fallback) {
        showBanner(`今日（${formatToInputDate(todayKey)}）暂无推送，已跳转至 ${formatToInputDate(fallback.dateKey)}`);
        applyDateContent(fallback.dateKey, fallback.html);
    } else {
        contentDiv.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">📭</div>
                <div class="empty-state-title">暂无可用推送</div>
                <div class="empty-state-desc">未找到任何历史论文推送文件</div>
            </div>
        `;
        if (datePicker) {
            datePicker.value = formatToInputDate(todayKey);
        }
        updateNavigation(todayKey);
    }
}

// 启动
init();