
fetch(`/api/report-data?year=${selectedYear}`)
  .then(res => res.json())
  .then(data => {
    //  類型分佈
    new Chart(document.getElementById("genreChart"), {
      type: 'pie',
      data: {
        labels: data.genre.labels,
        datasets: [{
          data: data.genre.data,
          backgroundColor: ['#f06292', '#4fc3f7', '#ffca28', '#81c784']
        }]
      }
    });

    // 每月觀影圖
    new Chart(document.getElementById("monthlyChart"), {
      type: 'bar',
      data: {
        labels: data.monthly.labels,
        datasets: [{
          label: '每月觀影次數',
          data: data.monthly.data,
          backgroundColor: '#42a5f5'
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
            ticks: { stepSize: 1 }
          }
        }
      }
    });

    // 情緒雷達
    new Chart(document.getElementById("emotionChart"), {
      type: 'radar',
      data: {
        labels: data.emotion.labels,
        datasets: [{
          label: '觀影後情緒豐富程度',
          data: data.emotion.data,
          fill: true,
          backgroundColor: 'rgba(54, 162, 235, 0.2)',
          borderColor: 'rgba(54, 162, 235, 1)',
          pointBackgroundColor: 'rgba(54, 162, 235, 1)'
        }]
      },
      options: {
        scales: {
            r: {
            suggestedMin: 0,
            suggestedMax: 100,
            ticks: {
                callback: function(value) {
                return value + '%';
                }
            }
            }
        }
    }

    });
  })
  .catch(err => {
    console.error('載入圖表資料失敗:', err);
  });
