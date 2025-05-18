let currentWatchId = null;
let addWatchLogModal;
let editWatchLogModal;

document.addEventListener('DOMContentLoaded', () => {
    addWatchLogModal = new bootstrap.Modal(document.getElementById('addWatchLogModal'));
    editWatchLogModal = new bootstrap.Modal(document.getElementById('editWatchLogModal'));
    loadWatchLogs();
});

function showAddWatchLogModal() {
    document.getElementById('addWatchLogForm').reset();
    loadMovieOptions();
    addWatchLogModal.show();
}

async function loadMovieOptions() {
    try {
        const response = await fetch('/movies');
        const movies = await response.json();
        const select = document.querySelector('select[name="movie_id"]');
        select.innerHTML = '<option value="">選擇電影</option>';
        movies.forEach(movie => {
            select.innerHTML += `<option value="${movie.movie_id}">${movie.title}</option>`;
        });
    } catch (error) {
        console.error('Error loading movies:', error);
    }
}

async function loadWatchLogs() {
    try {
        console.log('Start loading watch logs...');
        const response = await fetch('/api/watch-logs');
        console.log('API response status:', response.status);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const logs = await response.json();
        console.log('Received watch logs:', logs);
        
        const watchLogList = document.getElementById('watchLogList');
        watchLogList.innerHTML = '';
        
        if (!logs || logs.length === 0) {
            console.log('No watch logs found');
            watchLogList.innerHTML = `
                <tr>
                    <td colspan="5" class="text-center">目前沒有觀看紀錄</td>
                </tr>
            `;
            return;
        }
        
        console.log('Processing watch logs...');
        logs.forEach((log, index) => {
            console.log(`Processing record ${index + 1}:`, log);
            const row = `
                <tr>
                    <td>${log.title || '未知電影'}</td>
                    <td>${log.watch_date || '未知日期'}</td>
                    <td>${getMoodIcon(log.mood)} ${getMoodText(log.mood)}</td>
                    <td>${log.rating || 0}/10</td>
                    <td>
                        <button class="btn btn-sm btn-primary" onclick="showEditWatchLogModal(${log.watch_id})">
                            <i class="bi bi-pencil"></i>
                        </button>
                        <button class="btn btn-sm btn-danger" onclick="deleteWatchLog(${log.watch_id})">
                            <i class="bi bi-trash"></i>
                        </button>
                    </td>
                </tr>
            `;
            watchLogList.innerHTML += row;
        });
        console.log('Finished processing watch logs');
    } catch (error) {
        console.error('Error loading watch logs:', error);
        alert('觀看紀錄載入失敗: ' + error.message);
    }
}

async function addWatchLog() {
    const form = document.getElementById('addWatchLogForm');
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    data.user_id = window.currentUserId;
    
    try {
        const response = await fetch('/api/watch-logs', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            addWatchLogModal.hide();
            loadWatchLogs();
            alert('觀看紀錄新增成功');
        } else {
            const error = await response.json();
            alert(error.error || '新增失敗');
        }
    } catch (error) {
        console.error('Error adding watch log:', error);
        alert('新增失敗');
    }
}

async function showEditWatchLogModal(watchId) {
    try {
        const response = await fetch(`/api/watch-logs/${watchId}`);
        const log = await response.json();
        
        const form = document.getElementById('editWatchLogForm');
        form.elements['watch_id'].value = log.watch_id;
        form.elements['watch_date'].value = log.watch_date;
        form.elements['mood'].value = log.mood || '';
        form.elements['rating'].value = log.rating;
        
        currentWatchId = watchId;
        editWatchLogModal.show();
    } catch (error) {
        console.error('Error loading watch log:', error);
    }
}

async function updateWatchLog() {
    const form = document.getElementById('editWatchLogForm');
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    
    try {
        const response = await fetch(`/api/watch-logs/${currentWatchId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            editWatchLogModal.hide();
            loadWatchLogs();
            alert('觀看紀錄更新成功');
        } else {
            const error = await response.json();
            alert(error.error || '更新失敗');
        }
    } catch (error) {
        console.error('Error updating watch log:', error);
        alert('更新失敗');
    }
}

async function deleteWatchLog(watchId) {
    if (!confirm('確定要刪除這筆觀看紀錄嗎？')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/watch-logs/${watchId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            loadWatchLogs();
        } else {
            const error = await response.json();
            alert(error.error || '刪除失敗');
        }
    } catch (error) {
        console.error('Error deleting watch log:', error);
        alert('刪除失敗');
    }
}

function getMoodIcon(mood) {
    const icons = {
        'happy': '😊',
        'sad': '😢',
        'excited': '🤩',
        'relaxed': '😌'
    };
    return icons[mood] || '😐';
}

function getMoodText(mood) {
    const texts = {
        'happy': '開心',
        'sad': '難過',
        'excited': '興奮',
        'relaxed': '放鬆'
    };
    return texts[mood] || '未設定';
} 