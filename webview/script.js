// 函数：创建卡片元素
function createCard(paper) {
    const card = document.createElement('div');
    card.className = 'card';
    card.innerHTML = `
        <h3>${paper.title}</h3>
        <p class="explanation">${paper.explanation}</p>
        <div class="card-buttons">
            <button class="btn-interest" onclick="markInterested('${paper.doi}')">标记兴趣</button>
            <button class="btn-details" onclick="viewDetails('${paper.doi}')">查看详情</button>
        </div>
    `;
    return card;
}

// 函数：加载并显示论文
function loadPapers() {
    console.log('开始加载论文...');  // 添加日志
    window.pywebview.api.get_papers()
        .then(response => {
            console.log('收到响应:', response);  // 打印响应数据
            const papers = JSON.parse(response);
            console.log('解析后的数据:', papers);  // 打印解析后的数据
            const container = document.getElementById('paper-cards');
            container.innerHTML = '';  // 清空现有内容
            papers.forEach(paper => {
                const card = createCard(paper);
                container.appendChild(card);
            });
        })
        .catch(error => {
            console.error('加载论文失败:', error);
            console.error('错误详情:', {
                message: error.message,
                stack: error.stack
            });
            // 可以在页面上显示错误信息
            const container = document.getElementById('paper-cards');
            container.innerHTML = `<div class="error-message">加载失败: ${error.message}</div>`;
        });
}

// 函数：标记感兴趣
function markInterested(doi) {
    window.pywebview.api.mark_interested(doi)
        .then(response => {
            const result = JSON.parse(response);
            if (result) {
                alert('已标记为感兴趣');
                // 刷新论文列表以反映变化
                loadPapers();
            } else {
                alert('您已标记过此论文');
            }
        })
        .catch(error => {
            console.error('标记失败:', error);
            alert('标记失败，请重试。');
        });
}

// 函数：查看详情
function viewDetails(doi) {
    window.pywebview.api.get_paper_details(doi)
        .then(response => {
            const paper = JSON.parse(response);
            if (paper && paper.doi) {
                // 创建模态框显示详情
                showDetailModal(paper);
            } else {
                alert('未找到该论文的详细信息。');
            }
        })
        .catch(error => {
            console.error('获取详情失败:', error);
            alert('获取详情失败，请重试。');
        });
}

// 函数：显示详情模态框
function showDetailModal(paper) {
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-content">
            <span class="close">&times;</span>
            <div id="detail-content">
                <h2><a href="https://doi.org/${paper.doi}" target="_blank">${paper.title}</a></h2>
                <p><strong>作者：</strong>${paper.authors}</p>
                <p><strong>摘要：</strong>${paper.abstract}</p>
                <p><strong>说明：</strong>${paper.explanation}</p>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    modal.style.display = 'block';
    
    modal.querySelector('.close').onclick = () => {
        modal.style.display = 'none';
        modal.remove();
    };
    
    // 点击模态框外部关闭
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
            modal.remove();
        }
    };
}

// 初始化：页面加载完成后加载论文
document.addEventListener('DOMContentLoaded', loadPapers);
