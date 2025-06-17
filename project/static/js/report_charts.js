document.addEventListener("DOMContentLoaded", function () {
  // 載入圖表資料
  fetch(`/api/report-data?year=${selectedYear}`)
    .then(res => res.json())
    .then(data => {
      // 類型分佈圖
      new Chart(document.getElementById("genreChart"), {
        type: 'pie',
        data: {
          labels: data.genre.labels,
          datasets: [{
            data: data.genre.data,
            backgroundColor: [
              'rgba(0, 123, 255, 0.8)',
              'rgba(0, 172, 237, 0.8)',
              'rgba(100, 181, 246, 0.8)',
              'rgba(33, 150, 243, 0.8)',
              'rgba(3, 169, 244, 0.8)',
              'rgba(0, 188, 212, 0.8)'
            ],
            borderColor: '#ffffff',
            borderWidth: 2
          }]
        },
        options: {
          plugins: {
            legend: {
              labels: {
                color: '#000000',
                font: { weight: 'bold' }
              }
            }
          }
        }
      });

      // 每月觀影次數圖
      new Chart(document.getElementById("monthlyChart"), {
        type: 'bar',
        data: {
          labels: data.monthly.labels,
          datasets: [{
            label: '每月觀影次數',
            data: data.monthly.data,
            backgroundColor: 'rgba(0, 172, 237, 0.8)',
            borderColor: '#00bfff',
            borderWidth: 2
          }]
        },
        options: {
          plugins: {
            legend: {
              labels: {
                color: '#000000',
                font: { weight: 'bold' }
              }
            }
          },
          scales: {
            x: { ticks: { color: '#000000' } },
            y: {
              beginAtZero: true,
              ticks: { color: '#000000', stepSize: 1 }
            }
          }
        }
      });

      // 情緒雷達圖
      new Chart(document.getElementById("emotionChart"), {
        type: 'radar',
        data: {
          labels: data.emotion.labels,
          datasets: [{
            label: '觀影後情緒豐富程度',
            data: data.emotion.data,
            fill: true,
            backgroundColor: 'rgba(0, 191, 255, 0.2)',
            borderColor: 'rgba(0, 191, 255, 1)',
            pointBackgroundColor: 'rgba(0, 191, 255, 1)',
            pointBorderColor: '#ffffff',
            pointHoverBackgroundColor: '#ffffff',
            pointHoverBorderColor: 'rgba(0, 191, 255, 1)'
          }]
        },
        options: {
          plugins: {
            legend: {
              labels: {
                color: '#000000',
                font: { weight: 'bold' }
              }
            }
          },
          scales: {
            r: {
              suggestedMin: 0,
              suggestedMax: 100,
              angleLines: { color: 'rgba(0,0,0,0.15)' },
              grid: { color: 'rgba(0,0,0,0.05)' },
              pointLabels: { color: '#000000', padding: 12 },
              ticks: {
                color: '#000000',
                backdropColor: 'transparent',
                callback: value => value + '%'
              }
            }
          }
        }
      });

      // 推薦電影區塊
      const recommendationsContainer = document.getElementById("recommendations");
      recommendationsContainer.innerHTML = ""; // 清空舊內容

      if (data.recommendations.length > 0) {
        data.recommendations.forEach(movie => {
          const col = document.createElement("div");
          col.className = "col";
          col.innerHTML = `
            <div class="card h-100 recommended-card">
              <div class="card-body">
                <h5 class="card-title">${movie.title}</h5>
                <p class="card-text">類型：${movie.genre}</p>
              </div>
              <div class="card-footer text-center text-muted border-0" 
                  style="background: rgba(255, 255, 255, 0.6); border-bottom-left-radius: 1rem; border-bottom-right-radius: 1rem;">
                <small>⭐ ${movie.rating.toFixed(1)} / 10</small>
              </div>
            </div>

          `;
          recommendationsContainer.appendChild(col);
        });
      } else {
        recommendationsContainer.innerHTML = `
          <div class="col text-center text-muted">目前沒有推薦的電影，請多看幾部吧！</div>
        `;
      }
    })
    .catch(err => {
      console.error('載入圖表資料失敗:', err);
    });
});
