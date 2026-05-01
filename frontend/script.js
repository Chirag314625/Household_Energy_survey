// Frontend script for connecting to backend

const enabled = { fridge:true, ac:true, washer:true, fan:true, computer:true, kitchen:true, lighting:true, tv:true, heater:true };

function switchTab(id) {
  document.querySelectorAll('.tab').forEach((t,i) => {
    const ids = ['fridge','ac','washer','fan','computer','kitchen','lighting','tv','heater'];
    t.classList.toggle('active', ids[i] === id);
  });
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  document.getElementById('panel-' + id).classList.add('active');
}

function toggleAppliance(id, el) {
  enabled[id] = !enabled[id];
  el.classList.toggle('on', enabled[id]);
}

function gv(id) { return parseFloat(document.getElementById(id).value) || 0; }

function calculate() {
  const tariff = gv('tariff');
  const data = {};

  if (enabled.fridge) {
    data.fridge = {
      watts: gv('fridge-watts'),
      duty: parseFloat(document.getElementById('fridge-star').value),
      qty: gv('fridge-qty')
    };
  }
  if (enabled.ac) {
    data.ac = {
      watts: gv('ac-ton'),
      eer: gv('ac-eer'),
      star_factor: parseFloat(document.getElementById('ac-star').value),
      hours: gv('ac-hours'),
      qty: gv('ac-qty')
    };
  }
  if (enabled.washer) {
    data.washer = {
      watts: gv('washer-watts'),
      duration: gv('washer-duration'),
      cycles: gv('washer-cycles'),
      temp_factor: gv('washer-temp')
    };
  }
  if (enabled.fan) {
    data.fan = {
      watts: gv('fan-watts'),
      qty: gv('fan-qty'),
      hours: gv('fan-hours'),
      speed: gv('fan-speed')
    };
  }
  if (enabled.computer) {
    data.computer = {
      watts: gv('comp-watts'),
      monitor: gv('comp-monitor'),
      hours: gv('comp-hours'),
      router: gv('comp-router')
    };
  }
  if (enabled.kitchen) {
    data.kitchen = {
      micro_watts: gv('kit-micro'),
      micro_mins: gv('kit-micro-h'),
      induction_watts: gv('kit-induction'),
      induction_hours: gv('kit-induction-h')
    };
  }
  if (enabled.lighting) {
    data.lighting = {
      watts: gv('light-type'),
      qty: gv('light-qty'),
      hours: gv('light-hours')
    };
  }
  if (enabled.tv) {
    data.tv = {
      watts: gv('tv-size'),
      qty: 1,  // assuming 1 TV
      hours: gv('tv-hours'),
      tech: 1.0  // assuming standard
    };
  }
  if (enabled.heater) {
    data.heater = {
      liters: gv('heat-liters'),
      uses: gv('heat-uses'),
      target_temp: 25 + gv('heat-dt'),  // assuming inlet 25
      inlet_temp: 25,
      efficiency: gv('heat-eff')
    };
  }

  data.tariff = tariff;

  fetch('http://127.0.0.1:5000/api/calculate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(result => {
    displayResults(result);
  })
  .catch(error => {
    console.error('Error:', error);
    alert('Failed to calculate. Ensure backend is running.');
  });
}

function displayResults(result) {
  document.getElementById('placeholder').style.display = 'none';
  document.getElementById('output').style.display = 'block';

  document.getElementById('s-daily').textContent = result.total_daily.toFixed(2);
  document.getElementById('s-monthly').textContent = result.total_monthly.toFixed(1);
  document.getElementById('s-cost').textContent = result.monthly_cost.toFixed(0);
  document.getElementById('s-co2').textContent = result.co2_monthly.toFixed(1);

  // Rating based on daily consumption
  const rating = result.total_daily < 5 ? 'Excellent' : result.total_daily < 10 ? 'Good' : result.total_daily < 20 ? 'Average' : 'High';
  document.getElementById('rating-badge').textContent = rating;

  // Breakdown table
  const totalDaily = result.total_daily || 1;
  const tbody = document.getElementById('breakdown-body');
  tbody.innerHTML = '';
  result.appliances.forEach(app => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${app.icon} ${app.name}</td>
      <td>${app.daily.toFixed(3)}</td>
      <td>${(app.daily * 30).toFixed(1)}</td>
      <td>₹${(app.daily * 30 * result.tariff).toFixed(0)}</td>
      <td>
        <div style="display:flex; align-items:center; gap:8px;">
          <span>${((app.daily / totalDaily) * 100).toFixed(1)}%</span>
          <div class="progress-bar">
            <div class="progress-fill" style="width:${(app.daily / totalDaily) * 100}%"></div>
          </div>
        </div>
      </td>
    `;
    tbody.appendChild(tr);
  });

  // Pie chart
  const pieCtx = document.getElementById('pieChart').getContext('2d');
  if (window.pieChart) window.pieChart.destroy();
  window.pieChart = new Chart(pieCtx, {
    type: 'doughnut',
    data: {
      labels: result.appliances.map(a => a.name),
      datasets: [{
        data: result.appliances.map(a => a.daily),
        backgroundColor: ['#2563eb', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#0ea5e9', '#f97316', '#a855f7', '#14b8a6']
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'bottom' }
      }
    }
  });

  // Bar chart
  const barCtx = document.getElementById('barChart').getContext('2d');
  if (window.barChart) window.barChart.destroy();
  window.barChart = new Chart(barCtx, {
    type: 'bar',
    data: {
      labels: result.appliances.map(a => a.name),
      datasets: [{
        label: 'Daily kWh',
        data: result.appliances.map(a => a.daily),
        backgroundColor: '#000'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: { beginAtZero: true }
      }
    }
  });

  // Line chart for projection
  const lineCtx = document.getElementById('lineChart').getContext('2d');
  if (window.lineChart) window.lineChart.destroy();
  const months = Array.from({length:12}, (_,i) => `Month ${i+1}`);
  const cumulative = [];
  let cum = 0;
  for (let i = 0; i < 12; i++) {
    cum += result.total_monthly;
    cumulative.push(cum);
  }
  window.lineChart = new Chart(lineCtx, {
    type: 'line',
    data: {
      labels: months,
      datasets: [{
        label: 'Cumulative kWh',
        data: cumulative,
        borderColor: '#000',
        fill: false
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false
    }
  });

  // Recommendations
  const recoGrid = document.getElementById('reco-grid');
  recoGrid.innerHTML = '';
  const recommendations = [];
  if (result.total_daily > 10) recommendations.push({ title: 'Energy Audit', body: 'Consider professional energy audit to identify savings opportunities.' });
  if (result.appliances.find(a => a.name === 'Air Conditioner' && a.daily > 5)) recommendations.push({ title: 'AC Efficiency', body: 'Upgrade to higher EER rated AC or use smart thermostats.' });
  if (result.appliances.find(a => a.name === 'Refrigerator' && a.daily > 2)) recommendations.push({ title: 'Fridge Maintenance', body: 'Ensure proper ventilation and defrost regularly.' });
  if (!recommendations.length) recommendations.push({ title: 'Great Job!', body: 'Your energy usage is efficient. Keep monitoring.' });

  recommendations.forEach(r => {
    const card = document.createElement('div');
    card.className = 'reco-card';
    card.innerHTML = `<div class="reco-title">${r.title}</div><div class="reco-body">${r.body}</div>`;
    recoGrid.appendChild(card);
  });
}
