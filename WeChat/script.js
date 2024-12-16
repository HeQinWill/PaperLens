// 获取页面元素
const contentDiv = document.getElementById("content");
const prevLink = document.getElementById("prev-link");
const nextLink = document.getElementById("next-link");
const lastUpdateSpan = document.getElementById("last-update");

// 获取格式化日期，格式为 YYYYMMDD
function getFormattedDate(offset = 0) {
    const date = new Date();
    
    // 获取当前 UTC 时间的小时（24小时制）
    const utcHour = date.getUTCHours();
    // 判断 UTC 时间是否在 05 点之前
    if (utcHour < 5) {
        // 如果在 05 点之前，使用前一天的日期
        offset = - 1;
    };
    
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

// 尝试加载指定日期的文件
function loadDateFile(date) {
    const fileName = `${date}.html`; // 日期文件名格式 YYYYMMDD.html

    fetch(fileName)
        .then(response => {
            if (response.ok) {
                return response.text(); // 文件存在
            } else {
                throw new Error("File not found");
            }
        })
        .then(html => {
            contentDiv.innerHTML = html; // 加载文件内容
            lastUpdateSpan.textContent = `${date}`;
            updateNavigation(date); // 更新导航链接
        })
        .catch(() => {
            // 如果文件不存在，尝试加载前一天
            const prevDate = new Date(
                `${date.slice(0, 4)}-${date.slice(4, 6)}-${date.slice(6, 8)}`
            );
            prevDate.setDate(prevDate.getDate() - 1);
            const prevDateString = getFormattedDateFromDate(prevDate);
            // loadDateFile(prevDateString); // 递归调用
        });
}

// 更新导航链接
function updateNavigation(currentDate) {
    const current = new Date(
        `${currentDate.slice(0, 4)}-${currentDate.slice(4, 6)}-${currentDate.slice(6, 8)}`
    );
    const prevDate = new Date(current);
    prevDate.setDate(current.getDate() - 1);
    const nextDate = new Date(current);
    nextDate.setDate(current.getDate() + 1);

    const prevDateString = getFormattedDateFromDate(prevDate);
    const nextDateString = getFormattedDateFromDate(nextDate);

    prevLink.href = `#${prevDateString}`;
    prevLink.onclick = () => {
        loadDateFile(prevDateString);
        return false;
    };

    nextLink.href = `#${nextDateString}`;
    nextLink.onclick = () => {
        loadDateFile(nextDateString);
        return false;
    };
}

// 初始化加载
const today = getFormattedDate(); // 获取今天日期
loadDateFile(today); // 加载对应日期的文件