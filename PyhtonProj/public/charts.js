document.addEventListener('DOMContentLoaded', () => {
  Promise.all([
    fetch('/api/data').then(response => response.json()),
    fetch('/api/activities').then(response => response.json())
  ])
  .then(([azureData, activities]) => {
    displayServiceData(azureData.services);
    displaySecurityPractices(azureData.security_practices);
    displayActivityData(activities);
    displayAnomalyData(activities);
    displaySecurityFindings(azureData.security_practices, activities);
    loadAndDisplayCSVFindings(); // <- new call
  })
  .catch(error => {
    console.error('Error loading data:', error);
    document.body.innerHTML += `<div class="error">Error loading data: ${error.message}</div>`;
  });
});

function displayServiceData(services) {
  const categoryCounts = {};
  services.forEach(service => {
    categoryCounts[service.category] = (categoryCounts[service.category] || 0) + 1;
  });
  const ctx = document.getElementById('servicesChart').getContext('2d');
  new Chart(ctx, {
    type: 'pie',
    data: {
      labels: Object.keys(categoryCounts),
      datasets: [{
        data: Object.values(categoryCounts),
        backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40']
      }]
    }
  });
}

function displaySecurityPractices(practices) {
  const categoryCounts = {};
  practices.forEach(practice => {
    categoryCounts[practice.category] = (categoryCounts[practice.category] || 0) + 1;
  });
  const ctx = document.getElementById('securityChart').getContext('2d');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: Object.keys(categoryCounts),
      datasets: [{
        label: 'Number of Practices',
        data: Object.values(categoryCounts),
        backgroundColor: '#36A2EB'
      }]
    },
    options: {
      scales: { y: { beginAtZero: true } }
    }
  });
}

function displayActivityData(activities) {
  const hourCounts = {};
  activities.forEach(activity => {
    if (activity.timestamp) {
      const hour = new Date(activity.timestamp).getHours();
      hourCounts[hour] = (hourCounts[hour] || 0) + 1;
    }
  });
  const hours = [], counts = [];
  for (let i = 0; i < 24; i++) {
    hours.push(i);
    counts.push(hourCounts[i] || 0);
  }
  const ctx = document.getElementById('activityChart').getContext('2d');
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: hours,
      datasets: [{
        label: 'Activity Count',
        data: counts,
        borderColor: '#4BC0C0',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        tension: 0.1
      }]
    },
    options: {
      scales: {
        y: { beginAtZero: true },
        x: { title: { display: true, text: 'Hour of Day' } }
      }
    }
  });
}

function displayAnomalyData(activities) {
  let normalCount = 0, anomalyCount = 0;
  activities.forEach(activity => {
    if (activity.is_anomaly === 'True') anomalyCount++;
    else normalCount++;
  });
  const ctx = document.getElementById('anomalyChart').getContext('2d');
  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Normal', 'Anomalous'],
      datasets: [{
        data: [normalCount, anomalyCount],
        backgroundColor: ['#36A2EB', '#FF6384']
      }]
    }
  });
}

function displaySecurityFindings(practices, activities) {
  const container = document.getElementById('securityFindings');
  const importantPractices = practices.filter(practice =>
    practice.description.toLowerCase().includes('important') ||
    practice.description.toLowerCase().includes('critical') ||
    practice.description.toLowerCase().includes('recommend')
  );
  const anomalyByType = {};
  activities.forEach(activity => {
    if (activity.is_anomaly === 'True') {
      const type = determineAnomalyType(activity);
      anomalyByType[type] = (anomalyByType[type] || 0) + 1;
    }
  });

  let html = '<h3>Security Recommendations</h3><ul>';
  importantPractices.slice(0, 5).forEach(practice => {
    html += `<li>
      <strong>${practice.title || 'Security Practice'}</strong>
      <p>${practice.description.substring(0, 150)}...</p>
      <a href="${practice.url}" target="_blank">Learn more</a>
    </li>`;
  });

  html += '</ul><h3>Detected Anomalies</h3><ul>';
  Object.entries(anomalyByType).forEach(([type, count]) => {
    html += `<li><strong>${type}:</strong> ${count} instances detected</li>`;
  });
  html += '</ul>';
  container.innerHTML = html;
}

function determineAnomalyType(activity) {
  const hour = new Date(activity.timestamp).getHours();
  if (hour >= 22 || hour <= 5) return 'After-Hours Access';
  if (activity.action === 'Delete' && activity.is_successful === 'False') return 'Failed Delete Attempt';
  return 'Unusual Access Pattern';
}

async function loadAndDisplayCSVFindings() {
  try {
    const response = await fetch('/data/security_practices');
    const data = await response.json();
    const container = document.getElementById('securityFindings');
    const section = document.createElement('div');
    section.innerHTML = '<h3>Raw CSV Security Practices</h3>';
    data.forEach(row => {
      const div = document.createElement('div');
      div.className = 'csv-entry';
      div.textContent = Object.entries(row).map(([k, v]) => `${k}: ${v}`).join(' | ');
      section.appendChild(div);
    });
    container.appendChild(section);
  } catch (err) {
    console.error('Failed to load CSV:', err);
  }
}
