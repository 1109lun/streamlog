document.addEventListener("DOMContentLoaded", function () {
  const todayRadio = document.getElementById("trendTodayBs");
  const totalRadio = document.getElementById("trendTotalBs");
  const notesContainer = document.getElementById("top-notes");

  function loadTopNotes(range) {
    fetch(`/api/top_notes?range=${range}`)
      .then(res => res.json())
      .then(data => {
        if (!Array.isArray(data) || data.length === 0) {
          notesContainer.innerHTML = "<p>目前尚無任何按讚筆記。</p>";
          return;
        }

        const listItems = data.map(note => `
          <li class="list-group-item">
            <strong>${note.user_name}</strong> 對 <em>${note.title}</em> 的筆記：<br>
            ${note.content.substring(0, 100)}...<br>
            <span class="text-muted">👍 ${note.like_count} 個讚</span>
          </li>
        `).join("");

        notesContainer.innerHTML = `
          <ol class="list-group list-group-numbered">
            ${listItems}
          </ol>
        `;
      })
      .catch(err => {
        notesContainer.innerHTML = "<p class='text-danger'>載入資料失敗。</p>";
        console.error(err);
      });
  }

  // 初次載入 today
  loadTopNotes("today");

  todayRadio.addEventListener("change", () => loadTopNotes("today"));
  totalRadio.addEventListener("change", () => loadTopNotes("total"));
});
