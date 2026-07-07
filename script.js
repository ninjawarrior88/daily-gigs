let allJobs = [];
let savedJobs = JSON.parse(localStorage.getItem('savedJobs') || '[]');

async function loadJobs() {
  const el = document.getElementById('job-list');
  el.innerHTML = '<div class="loading"><div class="loading-dots">Loading jobs</div></div>';
  try {
    const r = await fetch('data/jobs.json?' + Date.now());
    if (!r.ok) throw new Error('Not found');
    allJobs = await r.json();
    document.getElementById('last-updated').textContent = new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    populateFilter();
    filter();
  } catch (e) {
    el.innerHTML = '<div class="no-results">No jobs loaded yet. The first scrape runs at 6 AM UTC.</div>';
  }
}

function populateFilter() {
  const sel = document.getElementById('source-filter');
  const s = new Set(allJobs.map(j => j.source));
  s.forEach(v => {
    const o = document.createElement('option');
    o.value = v;
    o.textContent = v;
    sel.appendChild(o);
  });
}

function filter() {
  const q = document.getElementById('search').value.toLowerCase();
  const src = document.getElementById('source-filter').value;
  const sort = document.getElementById('sort-select').value;
  let jobs = allJobs;
  if (src !== 'all') jobs = jobs.filter(j => j.source === src);
  if (q) jobs = jobs.filter(j => (j.title + ' ' + j.company + ' ' + j.description).toLowerCase().includes(q));
  if (sort === 'title') jobs.sort((a, b) => a.title.localeCompare(b.title));
  else jobs.sort((a, b) => new Date(b.date || 0) - new Date(a.date || 0));
  document.getElementById('job-count').textContent = jobs.length + ' jobs';
  render(jobs);
}

function render(jobs) {
  const el = document.getElementById('job-list');
  if (!jobs.length) { el.innerHTML = '<div class="no-results">No jobs match your search.</div>'; return; }
  el.innerHTML = jobs.map(j => {
    const isSaved = savedJobs.includes(j.url);
    const date = j.date ? (() => { try { return new Date(j.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }); } catch(e) { return ''; } })() : '';
    return `<div class="job-card">
      <div class="job-title"><a href="${esc(j.url)}" target="_blank" rel="noopener noreferrer">${esc(j.title)}</a></div>
      <div class="job-meta">
        <span class="company">${esc(j.company || 'Unknown')}</span>
        <span>📍 ${esc(j.location || 'Remote')}</span>
        ${date ? `<span>📅 ${date}</span>` : ''}
        <span class="job-source ${esc(j.source).replace(/\s/g,'')}">${esc(j.source)}</span>
      </div>
      <div class="job-desc">${esc((j.description || '').substring(0, 300))}</div>
      <div class="job-actions">
        <a href="${esc(j.url)}" target="_blank" rel="noopener noreferrer" class="apply-btn">Apply Now →</a>
        <button class="save-btn" onclick="toggleSave('${esc(j.url)}')">${isSaved ? '⭐ Saved' : '☆ Save'}</button>
      </div>
    </div>`;
  }).join('');
}

function toggleSave(url) {
  const i = savedJobs.indexOf(url);
  if (i > -1) savedJobs.splice(i, 1); else savedJobs.push(url);
  localStorage.setItem('savedJobs', JSON.stringify(savedJobs));
  filter();
}

function emailSignup(e) {
  e.preventDefault();
  const email = document.getElementById('email-input').value;
  const msg = document.getElementById('email-msg');
  msg.textContent = '📩 Thanks! You\'ll get jobs at ' + email;
  msg.style.color = '#16a34a';
  document.getElementById('email-form').reset();
  return false;
}

function nlSignup(e) {
  e.preventDefault();
  const email = document.getElementById('nl-email').value;
  const msg = document.getElementById('nl-msg');
  msg.textContent = '✅ Done! Check your inbox at ' + email;
  msg.style.color = '#22c55e';
  document.getElementById('nl-form').reset();
  return false;
}

function esc(s) {
  if (!s) return '';
  const d = document.createElement('div');
  d.textContent = s;
  return d.innerHTML;
}

loadJobs();
