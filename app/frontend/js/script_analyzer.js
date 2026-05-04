// Frontend script for connecting to backend

const applianceIds = ['fridge','ac','washer','fan','computer','kitchen','lighting','tv','heater'];
const selected = { fridge:false, ac:false, washer:false, fan:false, computer:false, kitchen:false, lighting:false, tv:false, heater:false };
const enabled = { fridge:false, ac:false, washer:false, fan:false, computer:false, kitchen:false, lighting:false, tv:false, heater:false };
let pieChartInstance = null;
let barChartInstance = null;

function renderSelectedEquipment() {
  const visibleIds = applianceIds.filter(id => selected[id]);

  // Show/hide parameters for each equipment
  applianceIds.forEach(id => {
    const params = document.getElementById('panel-' + id);
    if (params) {
      params.classList.toggle('active', selected[id]);
    }
  });
}

function selectEquipment(id, checked) {
  selected[id] = checked;
  enabled[id] = checked;

  const toggle = document.getElementById('tog-' + id);
  if (toggle) toggle.classList.toggle('on', checked);

  renderSelectedEquipment();
}

function toggleAppliance(id, el) {
  if (!selected[id]) return;
  enabled[id] = !enabled[id];
  el.classList.toggle('on', enabled[id]);
}

function gv(id) { return parseFloat(document.getElementById(id).value) || 0; }

async function calculate() {
  const tariff = gv('tariff');
  const data = {};

  if (selected.fridge && enabled.fridge) {
    data.fridge = {
      watts: gv('fridge-watts'),
      duty: parseFloat(document.getElementById('fridge-star').value),
      qty: gv('fridge-qty'),
      age_factor: gv('fridge-age'),
      ambient_factor: gv('fridge-ambient'),
      door_factor: gv('fridge-door')
    };
  }
  if (selected.ac && enabled.ac) {
    data.ac = {
      watts: gv('ac-ton'),
      eer: gv('ac-eer'),
      star_factor: parseFloat(document.getElementById('ac-star').value),
      hours: gv('ac-hours'),
      qty: gv('ac-qty'),
      temp_factor: gv('ac-temp'),
      setpoint_factor: gv('ac-setpoint'),
      maintenance_factor: gv('ac-maintenance')
    };
  }
  if (selected.washer && enabled.washer) {
    data.washer = {
      watts: gv('washer-watts'),
      duration: gv('washer-duration'),
      cycles: gv('washer-cycles'),
      temp_factor: gv('washer-temp'),
      load_factor: gv('washer-load'),
      spin_factor: gv('washer-spin')
    };
  }
  if (selected.fan && enabled.fan) {
    data.fan = {
      watts: gv('fan-watts'),
      qty: gv('fan-qty'),
      hours: gv('fan-hours'),
      speed: gv('fan-speed'),
      motor_factor: gv('fan-motor')
    };
  }
  if (selected.computer && enabled.computer) {
    data.computer = {
      watts: gv('comp-watts'),
      monitor: gv('comp-monitor'),
      hours: gv('comp-hours'),
      router: gv('comp-router'),
      qty: gv('comp-qty'),
      standby: gv('comp-standby')
    };
  }
  if (selected.kitchen && enabled.kitchen) {
    data.kitchen = {
      micro_watts: gv('kit-micro'),
      micro_mins: gv('kit-micro-h'),
      induction_watts: gv('kit-induction'),
      induction_hours: gv('kit-induction-h'),
      kettle_watts: gv('kit-kettle'),
      kettle_mins: gv('kit-kettle-h'),
      rice_watts: gv('kit-rice'),
      rice_hours: gv('kit-rice-h'),
      mixer_watts: gv('kit-mixer'),
      mixer_mins: gv('kit-mixer-h')
    };
  }
  if (selected.lighting && enabled.lighting) {
    data.lighting = {
      watts: gv('light-type'),
      qty: gv('light-qty'),
      hours: gv('light-hours'),
      daylight_factor: gv('light-daylight'),
      occupancy_factor: gv('light-occupancy')
    };
  }
  if (selected.tv && enabled.tv) {
    data.tv = {
      watts: gv('tv-size'),
      qty: gv('tv-qty'),
      hours: gv('tv-hours'),
      standby: gv('tv-standby')
    };
  }
  if (selected.heater && enabled.heater) {
    data.heater = {
      liters: gv('heat-liters'),
      uses: gv('heat-uses'),
      target_temp: 25 + gv('heat-dt'),  // assuming inlet 25
      inlet_temp: 25,
      efficiency: gv('heat-eff'),
      insulation_factor: gv('heat-insulation')
    };
  }

  if (!Object.keys(data).length) {
    alert('Select and enable at least one equipment item for analysis.');
    return;
  }

  data.tariff = tariff;

  try {
    const response = await fetch('/api/calculate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.error || 'Calculation request failed');
    }

    displayResults(result);
  } catch (error) {
    console.error('Error:', error);
    alert(`Failed to calculate: ${error.message}`);
  }
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
  if (pieChartInstance) pieChartInstance.destroy();
  pieChartInstance = new Chart(pieCtx, {
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
  if (barChartInstance) barChartInstance.destroy();
  barChartInstance = new Chart(barCtx, {
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

document.addEventListener('DOMContentLoaded', () => {
  renderSelectedEquipment();
});
