<script>
  document.addEventListener('DOMContentLoaded', () => {
    const modal = new bootstrap.Modal(document.getElementById('movieNotesModal'));
    const modalBody = document.getElementById('movie-notes-content');
    const modalTitle = document.getElementById('movieNotesModalLabel');

    document.querySelectorAll('.movie-title-link').forEach(link => {
      link.addEventListener('click', async (e) => {
        e.preventDefault();
        const movieId = link.getAttribute('data-movie-id');
        const movieTitle = link.textContent;

        modalTitle.textContent = `電影筆記 - ${movieTitle}`;
        modalBody.innerHTML = `<p>載入中...</p>`;

        try {
          const response = await fetch(`/api/movie_notes/${movieId}`);
          if (!response.ok) throw new Error('載入失敗');

          const notes = await response.json();

          if (notes.length === 0) {
            modalBody.innerHTML = '<p>尚無筆記。</p>';
          } else {
            modalBody.innerHTML = notes.map(note => `
              <div class="mb-3 border-bottom pb-2">
                <strong>${note.user_name}</strong> <small class="text-muted">${note.created_at}</small>
                <p>${note.content}</p>
              </div>
            `).join('');
          }
        } catch (error) {
          modalBody.innerHTML = `<p class="text-danger">載入錯誤：${error.message}</p>`;
        }

        modal.show();
      });
    });
  });
</script>
