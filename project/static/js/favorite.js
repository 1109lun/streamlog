async function loadFavorites() {
  try {
    const response = await fetch('/api/favorites');
    const favorites = await response.json();
    
    const favoritesList = document.getElementById('favoritesList');
    const defaultImage = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjMwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMjAwIiBoZWlnaHQ9IjMwMCIgZmlsbD0iI2VlZSIvPjx0ZXh0IHg9IjUwJSIgeT0iNTAlIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMjAiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuM2VtIiBmaWxsPSIjNjY2Ij5ObyBJbWFnZTwvdGV4dD48L3N2Zz4=';

    favoritesList.innerHTML = favorites.map(movie => {
      const imagePath = movie.image_url ? movie.image_url.replace(/^static\//, '') : '';
      const imageUrl = imagePath ? window.location.origin + '/static/' + imagePath : defaultImage;
      console.log('Movie:', movie.title);
      console.log('Original image_url:', movie.image_url);
      console.log('Image path:', imagePath);
      console.log('Full image URL:', imageUrl);
      
      return `
      <div class="col-md-3 mb-4">
        <div class="card h-100">
          <img src="${imageUrl}" 
               class="card-img-top" 
               alt="${movie.title}"
               style="height: 300px; object-fit: cover;"
               onerror="console.log('Image load error:', this.src); this.onerror=null; this.src='${defaultImage}';">
          <div class="card-body">
            <h5 class="card-title" style="font-size: 1.1rem;">${movie.title}</h5>
            <p class="card-text" style="font-size: 0.9rem;">
              <small class="text-muted">類型：${movie.genre}</small><br>
              <small class="text-muted">年份：${movie.release_year}</small><br>
              <small class="text-muted">評分：${movie.rating || '尚未評分'}</small>
            </p>
            <button class="btn btn-danger btn-sm" onclick="removeFavorite(${movie.movie_id})">
              <i class="bi bi-star"></i> 取消收藏
            </button>
          </div>
        </div>
      </div>
    `}).join('');
  } catch (error) {
    console.error('Error loading favorites:', error);
    alert('載入收藏列表失敗');
  }
}

async function removeFavorite(movieId) {
  if (!confirm('確定要取消收藏這部電影嗎？')) return;
  
  try {
    const response = await fetch(`/api/favorites/${movieId}`, {
      method: 'DELETE'
    });
    
    if (response.ok) {
      alert('已取消收藏');
      loadFavorites(); // 重新載入列表
    } else {
      const data = await response.json();
      alert(data.error || '取消收藏失敗');
    }
  } catch (error) {
    console.error('Error removing favorite:', error);
    alert('取消收藏失敗');
  }
}

async function showAddFavoriteModal() {
  try {
    const response = await fetch('/api/movies');
    const movies = await response.json();
    
    // Load favorites movies
    const favoritesResponse = await fetch('/api/favorites');
    const favorites = await favoritesResponse.json();
    const favoriteIds = new Set(favorites.map(f => f.movie_id));
    
    // Filter out already favorited movies
    const availableMovies = movies.filter(movie => !favoriteIds.has(movie.movie_id));
    
    // Update the dropdown menu
    const select = document.querySelector('#addFavoriteForm select[name="movie_id"]');
    select.innerHTML = `
      <option value="">選擇電影</option>
      ${availableMovies.map(movie => `
        <option value="${movie.movie_id}">${movie.title}</option>
      `).join('')}
    `;
    
    const modal = new bootstrap.Modal(document.getElementById('addFavoriteModal'));
    modal.show();
  } catch (error) {
    console.error('Error showing add favorite modal:', error);
    alert('載入電影列表失敗');
  }
}

async function addFavorite() {
  const form = document.getElementById('addFavoriteForm');
  const movieId = form.movie_id.value;
  
  if (!movieId) {
    alert('請選擇電影');
    return;
  }
  
  try {
    const response = await fetch(`/api/favorites/${movieId}`, {
      method: 'POST'
    });
    
    if (response.ok) {
      alert('成功加入收藏');
      const modal = bootstrap.Modal.getInstance(document.getElementById('addFavoriteModal'));
      modal.hide();
      loadFavorites();
    } else {
      const data = await response.json();
      alert(data.error || '加入收藏失敗');
    }
  } catch (error) {
    console.error('Error adding favorite:', error);
    alert('加入收藏失敗');
  }
}

document.addEventListener('DOMContentLoaded', loadFavorites); 