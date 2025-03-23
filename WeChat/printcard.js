// 直接<script>...</script>没问题但是直接放在js中，可能会导致DOMContentLoaded事件在脚本加载之前触发。
// 为了解决这个问题，将脚本放在DOMContentLoaded事件的回调函数中，确保DOM已经加载完成后再执行脚本。
document.addEventListener('DOMContentLoaded', function() {
    // 检测暗黑模式
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        document.documentElement.classList.add('dark');
    }

    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', event => {
        if (event.matches) {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }
    });

    // 获取DOM元素
    const loadingOverlay = document.getElementById('loadingOverlay');
    const loadingText = document.getElementById('loadingText');
    const previewModal = document.getElementById('previewModal');
    const previewImage = document.getElementById('previewImage');
    const closePreview = document.getElementById('closePreview');
    const downloadButton = document.getElementById('downloadButton');
    const exportAllButton = document.getElementById('exportAllButton');

    // 当前预览的数据URL
    let currentImageDataUrl = '';
    let currentFilename = '';

    // 设置导出按钮事件
    document.querySelectorAll('.export-button').forEach((button, index) => {
        button.addEventListener('click', async (e) => {
            e.stopPropagation(); // 阻止事件冒泡
            const paperCard = button.closest('.paper-card');
            await exportCard(paperCard, index);
        });
    });

    // 导出全部按钮事件
    exportAllButton.addEventListener('click', async () => {
        const paperCards = document.querySelectorAll('.paper-card');
        loadingOverlay.style.display = 'flex';
        loadingText.textContent = '正在导出所有卡片...';
        
        for (let i = 0; i < paperCards.length; i++) {
            const paperCard = paperCards[i];
            
            // 隐藏导出按钮，以免显示在导出的图片中
            const exportButton = paperCard.querySelector('.export-button');
            exportButton.style.display = 'none';
            
            try {
                loadingText.textContent = `正在导出第 ${i + 1}/${paperCards.length} 个卡片...`;
                
                // 等待一小段时间让UI更新
                await new Promise(resolve => setTimeout(resolve, 100));
                
                const canvas = await html2canvas(paperCard, {
                    scale: 4, // 提高分辨率，从2增加到4
                    useCORS: true, // 跨域图片支持
                    logging: false,
                    backgroundColor: document.documentElement.classList.contains('dark') ? '#2d2d2d' : '#ffffff'
                });
                
                // 将canvas转换为数据URL
                const dataUrl = canvas.toDataURL('image/png');
                
                // 获取论文标题作为文件名
                const titleElement = paperCard.querySelector('.paper-title');
                let title = titleElement ? titleElement.textContent.trim() : `论文卡片_${i + 1}`;
                
                // 确保文件名长度适中且不包含特殊字符
                title = title.substring(0, 30).replace(/[^\w\u4e00-\u9fa5]/gi, '_');
                const filename = `${title}.png`;
                
                // 使用a标签模拟下载
                const link = document.createElement('a');
                link.href = dataUrl;
                link.download = filename;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                
                // 等待一小段时间以确保浏览器处理完下载请求
                await new Promise(resolve => setTimeout(resolve, 500));
            } catch (error) {
                console.error('导出卡片时出错:', error);
            } finally {
                // 恢复导出按钮显示
                exportButton.style.display = 'block';
            }
        }
        
        loadingOverlay.style.display = 'none';
    });

    // 导出单个卡片
    async function exportCard(paperCard, index) {
        // 隐藏导出按钮，以免显示在导出的图片中
        const exportButton = paperCard.querySelector('.export-button');
        exportButton.style.display = 'none';
        
        loadingOverlay.style.display = 'flex';
        loadingText.textContent = '正在生成卡片图片...';
        
        try {
            const canvas = await html2canvas(paperCard, {
                scale: 4, // 提高分辨率，从2增加到4
                useCORS: true, // 跨域图片支持
                logging: false,
                backgroundColor: document.documentElement.classList.contains('dark') ? '#2d2d2d' : '#ffffff'
            });
            
            // 将canvas转换为数据URL
            const dataUrl = canvas.toDataURL('image/png');
            
            // 获取论文标题作为文件名
            const titleElement = paperCard.querySelector('.paper-title');
            let title = titleElement ? titleElement.textContent.trim() : `论文卡片_${index + 1}`;
            
            // 确保文件名长度适中且不包含特殊字符
            title = title.substring(0, 30).replace(/[^\w\u4e00-\u9fa5]/gi, '_');
            const filename = `${title}.png`;
            
            // 保存当前预览的数据URL和文件名
            currentImageDataUrl = dataUrl;
            currentFilename = filename;
            
            // 显示预览
            previewImage.src = dataUrl;
            previewModal.style.display = 'flex';
        } catch (error) {
            console.error('导出卡片时出错:', error);
            alert('导出卡片时出错: ' + error.message);
        } finally {
            // 恢复导出按钮显示
            exportButton.style.display = 'block';
            loadingOverlay.style.display = 'none';
        }
    }

    // 下载按钮事件
    downloadButton.addEventListener('click', () => {
        if (currentImageDataUrl) {
            const link = document.createElement('a');
            link.href = currentImageDataUrl;
            link.download = currentFilename;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    });

    // 关闭预览
    closePreview.addEventListener('click', () => {
        previewModal.style.display = 'none';
    });

    // 点击预览模态框外部关闭
    previewModal.addEventListener('click', (e) => {
        if (e.target === previewModal) {
            previewModal.style.display = 'none';
        }
    });

    // 按ESC键关闭预览
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && previewModal.style.display === 'flex') {
            previewModal.style.display = 'none';
        }
    });
});