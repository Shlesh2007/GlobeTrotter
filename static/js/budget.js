(function () {
  const payload = window.traveloopBudgetData;
  if (!payload) return;

  const labels = payload.labels || [];
  const values = payload.values || [];

  const pieCtx = document.getElementById("budgetPie");
  const barCtx = document.getElementById("budgetBar");
  if (!pieCtx || !barCtx) return;

  // Professional color palette (slate, indigo, emerald, amber, rose)
  const bgColors = ["rgba(71, 85, 105, 0.8)", "rgba(99, 102, 241, 0.8)", "rgba(16, 185, 129, 0.8)", "rgba(245, 158, 11, 0.8)", "rgba(244, 63, 94, 0.8)"];
  const borderColors = ["#475569", "#6366f1", "#10b981", "#f59e0b", "#f43f5e"];

  // Modern Doughnut Chart
  new Chart(pieCtx, {
    type: "doughnut",
    data: { 
      labels, 
      datasets: [{ 
        data: values, 
        backgroundColor: bgColors,
        borderColor: "#1e293b", // match dark theme background roughly
        borderWidth: 3,
        hoverOffset: 4
      }] 
    },
    options: {
      cutout: '70%',
      plugins: { 
        legend: { 
          position: 'bottom',
          labels: { 
            color: "#94a3b8", 
            usePointStyle: true, 
            padding: 20,
            font: { family: "'Inter', sans-serif", size: 12 }
          } 
        },
        tooltip: {
          backgroundColor: 'rgba(15, 23, 42, 0.9)',
          titleFont: { size: 13, family: "'Inter', sans-serif" },
          bodyFont: { size: 14, weight: 'bold', family: "'Inter', sans-serif" },
          padding: 12,
          cornerRadius: 8,
          displayColors: true,
          callbacks: {
            label: function(context) {
              return ' ₹' + context.parsed.toLocaleString();
            }
          }
        }
      } 
    },
  });

  // Professional Bar Chart
  new Chart(barCtx, {
    type: "bar",
    data: { 
      labels, 
      datasets: [{ 
        label: "Estimated Budget", 
        data: values, 
        backgroundColor: bgColors,
        borderColor: borderColors,
        borderWidth: 1,
        borderRadius: 6,
        barPercentage: 0.6
      }] 
    },
    options: {
      responsive: true,
      scales: {
        x: { 
          ticks: { color: "#94a3b8", font: { family: "'Inter', sans-serif" } }, 
          grid: { display: false } 
        },
        y: { 
          beginAtZero: true,
          ticks: { 
            color: "#94a3b8", 
            font: { family: "'Inter', sans-serif" },
            callback: function(value) { return '₹' + value; }
          }, 
          border: { display: false },
          grid: { color: "rgba(148, 163, 184, 0.1)", borderDash: [5, 5] } 
        },
      },
      plugins: { 
        legend: { display: false },
        tooltip: {
          backgroundColor: 'rgba(15, 23, 42, 0.9)',
          titleFont: { size: 13, family: "'Inter', sans-serif" },
          bodyFont: { size: 14, weight: 'bold', family: "'Inter', sans-serif" },
          padding: 12,
          cornerRadius: 8,
          displayColors: false,
          callbacks: {
            label: function(context) {
              return ' ₹' + context.parsed.y.toLocaleString();
            }
          }
        }
      },
    },
  });
})();
