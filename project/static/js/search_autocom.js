document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("search-input");
  const list = document.getElementById("autocomplete-list");
  let timeoutId;

  input.addEventListener("input", () => {
    const query = input.value.trim();
    list.innerHTML = "";

    if (timeoutId) clearTimeout(timeoutId);
    if (query.length < 2) return;

    timeoutId = setTimeout(() => {
      fetch(`/api/autocomplete?q=${encodeURIComponent(query)}`)
        .then(res => res.json())
        .then(data => {
          list.innerHTML = "";
          if (!data.length) {
            const item = document.createElement("li");
            item.classList.add("list-group-item", "text-muted");
            item.textContent = "找不到相關建議";
            list.appendChild(item);
            return;
          }
          data.forEach(movie => {
            const item = document.createElement("li");
            item.classList.add("list-group-item", "list-group-item-action");
            item.textContent = movie.title;
            item.style.cursor = "pointer";
            item.addEventListener("click", () => {
              input.value = movie.title;
              list.innerHTML = "";
              input.form.submit();
            });
            list.appendChild(item);
          });
        })
        .catch(console.error);
    }, 300);
  });

  document.addEventListener("click", (e) => {
    if (!input.contains(e.target) && !list.contains(e.target)) {
      list.innerHTML = "";
    }
  });
});
