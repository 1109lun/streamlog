async function loadMovieOptions() {
  try {
    const response = await fetch('/api/movies');
    const movies = await response.json();
    const select = document.querySelector('select[name="movie_id"]');
    select.innerHTML = movies.map(movie => 
      `<option value="${movie.movie_id}">${movie.title}</option>`
    ).join('');
  } catch (error) {
    console.error('Failed to load movie options:', error);
  }
}

async function loadNotes() {
  try {
    const response = await fetch('/api/notes');
    const notes = await response.json();
    const tbody = document.getElementById('noteList');
    console.log('Current User ID:', window.currentUserId);
    console.log('Notes:', notes);
    
    tbody.innerHTML = notes.map(note => {
      const noteUserId = parseInt(note.user_id);
      const isOwner = noteUserId === window.currentUserId;
      const isLiked = note.liked_by && note.liked_by.includes(window.currentUserId);
      console.log(`Note ${note.note_id}: user_id=${noteUserId}, isOwner=${isOwner}`);
      
      return `
        <tr>
          <td>${note.title}</td>
          <td>${note.user_name}</td>
          <td>${note.content}</td>
          <td>${new Date(note.created_at).toLocaleDateString('zh-TW')}</td>
          <td>
            <button class="btn btn-sm ${isLiked ? 'btn-danger' : 'btn-outline-danger'} me-2" 
                    onclick="toggleLike(${note.note_id})">
              <i class="bi bi-heart${isLiked ? '-fill' : ''}"></i>
              <span class="like-count">${note.like_count || 0}</span>
            </button>
            ${isOwner ? `
              <button class="btn btn-sm btn-outline-primary me-1" onclick="showEditNoteModal(${note.note_id}, '${note.content.replace(/'/g, "\\'")}')">
                <i class="bi bi-pencil"></i>
              </button>
              <button class="btn btn-sm btn-outline-danger" onclick="deleteNote(${note.note_id})">
                <i class="bi bi-trash"></i>
              </button>
            ` : ''}
          </td>
        </tr>
      `;
    }).join('');
  } catch (error) {
    console.error('Failed to load notes:', error);
  }
}

function showAddNoteModal() {
  loadMovieOptions();
  const modal = new bootstrap.Modal(document.getElementById('addNoteModal'));
  modal.show();
}

async function addNote() {
  const form = document.getElementById('addNoteForm');
  const formData = new FormData(form);
  const data = {
    movie_id: parseInt(formData.get('movie_id')),
    content: formData.get('content'),
    user_id: window.currentUserId
  };

  try {
    const response = await fetch('/api/notes', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });

    if (response.ok) {
      const modal = bootstrap.Modal.getInstance(document.getElementById('addNoteModal'));
      modal.hide();
      form.reset();
      loadNotes();
    } else {
      const error = await response.json();
      alert(`新增日誌失敗: ${error.error || '未知錯誤'}`);
    }
  } catch (error) {
    console.error('新增日誌失敗:', error);
    alert('新增日誌失敗');
  }
}

function showEditNoteModal(noteId, content) {
  const form = document.getElementById('editNoteForm');
  form.querySelector('[name="note_id"]').value = noteId;
  form.querySelector('[name="content"]').value = content;
  const modal = new bootstrap.Modal(document.getElementById('editNoteModal'));
  modal.show();
}

async function updateNote() {
  const form = document.getElementById('editNoteForm');
  const noteId = form.querySelector('[name="note_id"]').value;
  const content = form.querySelector('[name="content"]').value;

  try {
    const response = await fetch(`/api/notes/${noteId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ content })
    });

    if (response.ok) {
      const modal = bootstrap.Modal.getInstance(document.getElementById('editNoteModal'));
      modal.hide();
      form.reset();
      loadNotes();
    } else {
      const error = await response.json();
      alert(`更新日誌失敗: ${error.error || '未知錯誤'}`);
    }
  } catch (error) {
    console.error('Failed to update note:', error);
    alert('更新日誌失敗');
  }
}

async function deleteNote(noteId) {
  if (!confirm('確定要刪除這則日誌嗎？')) {
    return;
  }

  try {
    const response = await fetch(`/api/notes/${noteId}`, {
      method: 'DELETE'
    });

    if (response.ok) {
      loadNotes();
    } else {
      const error = await response.json();
      alert(`刪除日誌失敗: ${error.error || '未知錯誤'}`);
    }
  } catch (error) {
    console.error('刪除日誌失敗:', error);
    alert('刪除日誌失敗');
  }
}

async function toggleLike(noteId) {
  try {
    const response = await fetch(`/api/notes/${noteId}/like`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        user_id: window.currentUserId
      })
    });

    if (response.ok) {
      const result = await response.json();
      // Update the like button status
      const button = document.querySelector(`button[onclick="toggleLike(${noteId})"]`);
      const icon = button.querySelector('i');
      const countSpan = button.querySelector('.like-count');
      
      if (result.liked_by.includes(window.currentUserId)) {
        button.classList.remove('btn-outline-danger');
        button.classList.add('btn-danger');
        icon.classList.remove('bi-heart');
        icon.classList.add('bi-heart-fill');
      } else {
        button.classList.remove('btn-danger');
        button.classList.add('btn-outline-danger');
        icon.classList.remove('bi-heart-fill');
        icon.classList.add('bi-heart');
      }
      
      countSpan.textContent = result.like_count;
    } else {
      const error = await response.json();
      alert(`按讚失敗: ${error.error || '未知錯誤'}`);
    }
  } catch (error) {
    console.error('Failed to like note:', error);
    alert('按讚失敗');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  loadNotes();
}); 