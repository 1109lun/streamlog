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
    })
    .catch(err => {
      console.error('載入圖表資料失敗:', err);
    });

    
});
