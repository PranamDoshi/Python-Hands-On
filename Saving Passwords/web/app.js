// ──────────────────────────────────────────────────────────
// API client (endpoints unchanged — encryption is handled server-side)
// ──────────────────────────────────────────────────────────
async function request(url, options = {}, fallbackMsg = 'Request failed') {
  const r = await fetch(url, options);
  if (!r.ok) {
    const body = await r.json().catch(() => ({}));
    throw new Error(typeof body.detail === 'string' ? body.detail : fallbackMsg);
  }
  return r.json();
}
const json = (method, body) => ({
  method,
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(body),
});

const api = {
  all: () => request('/api/passwords', {}, 'Failed to load entries'),
  titles: () => request('/api/titles', {}, 'Failed to load entries'),
  get: (title) => request(`/api/password/${encodeURIComponent(title)}`, {}, 'Entry not found'),
  save: ({ title, password, email }) =>
    request('/api/password', json('POST', { title, password, email: email || null }), 'Failed to save'),
  remove: (title) =>
    request(`/api/password/${encodeURIComponent(title)}`, { method: 'DELETE' }, 'Failed to delete'),
  rename: (currentTitle, newTitle) =>
    request('/api/title', json('PATCH', { currentTitle, newTitle }), 'Failed to rename'),
  generate: (length) => request('/api/generate', json('POST', { length }), 'Failed to generate'),
};

// ──────────────────────────────────────────────────────────
// Helpers
// ──────────────────────────────────────────────────────────
const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

function el(tag, props = {}, ...children) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(props)) {
    if (k === 'class') node.className = v;
    else if (k === 'dataset') Object.assign(node.dataset, v);
    else if (k.startsWith('on')) node.addEventListener(k.slice(2), v);
    else if (v !== undefined && v !== null) node.setAttribute(k, v);
  }
  for (const c of children.flat()) {
    if (c != null) node.append(c instanceof Node ? c : document.createTextNode(String(c)));
  }
  return node;
}

function icon(name) {
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('class', 'ic');
  const use = document.createElementNS('http://www.w3.org/2000/svg', 'use');
  use.setAttribute('href', `#i-${name}`);
  svg.append(use);
  return svg;
}

function setIcon(button, name) {
  $('use', button)?.setAttribute('href', `#i-${name}`);
}

function toast(msg, type = 'ok') {
  const t = el('div', { class: `toast ${type}` }, icon(type === 'error' ? 'x' : 'check'), msg);
  $('#toasts').append(t);
  setTimeout(() => { t.classList.add('out'); setTimeout(() => t.remove(), 220); }, 2200);
}

async function copyText(text, button) {
  if (!text) return;
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
    } else {
      const ta = el('textarea', { style: 'position:fixed;opacity:0' });
      ta.value = text;
      document.body.append(ta);
      ta.select();
      document.execCommand('copy');
      ta.remove();
    }
    toast('Copied to clipboard');
    if (button) {
      setIcon(button, 'check');
      button.classList.add('ok');
      setTimeout(() => { setIcon(button, 'copy'); button.classList.remove('ok'); }, 1200);
    }
  } catch {
    toast('Copy failed', 'error');
  }
}

/** Stable hue per title so avatars keep their color. */
function hueFor(text) {
  let h = 0;
  for (const ch of text) h = (h * 31 + ch.codePointAt(0)) % 360;
  return h;
}
function avatar(title, cls = 'avatar') {
  const a = el('div', { class: cls }, (title.trim()[0] || '?').toUpperCase());
  a.style.setProperty('--h', hueFor(title));
  return a;
}

/** History entries are stored as "yy-mm-dd_value". */
function parseHistory(entry) {
  const s = String(entry);
  const m = s.match(/^(\d{2}-\d{2}-\d{2})_(.*)$/s);
  return m ? { date: m[1], value: m[2] } : { date: '', value: s };
}

const STRENGTH_TIERS = [
  [40, 1, 'Weak', 'var(--red)'],
  [64, 2, 'Fair', 'var(--amber)'],
  [100, 3, 'Strong', 'var(--green)'],
  [Infinity, 4, 'Excellent', 'var(--cyan)'],
];

function strengthOf(pwd) {
  if (!pwd) return { level: 0, name: '', bits: 0, pct: 0, label: '', color: '' };
  let pool = 0;
  if (/[a-z]/.test(pwd)) pool += 26;
  if (/[A-Z]/.test(pwd)) pool += 26;
  if (/\d/.test(pwd)) pool += 10;
  if (/[^A-Za-z0-9]/.test(pwd)) pool += 33;
  const bits = Math.round(pwd.length * Math.log2(Math.max(pool, 1)));
  const [, level, name, color] = STRENGTH_TIERS.find(([max]) => bits < max);
  return { level, name, bits, pct: Math.min(100, (bits / 128) * 100), label: `${name} · ${bits} bits`, color };
}
function renderStrength(node, pwd) {
  const s = strengthOf(pwd);
  node.dataset.level = s.level;
  const bar = $('.bar i', node);
  bar.style.width = `${s.pct}%`;
  bar.style.background = s.color || '';
  $('.label', node).textContent = s.label;
}

// ──────────────────────────────────────────────────────────
// State & elements
// ──────────────────────────────────────────────────────────
const app = $('#app');
const titlesWrap = $('#titles');
const tierFiltersWrap = $('#tierFilters');
const searchInput = $('#searchInput');
const entryCount = $('#entryCount');

let titlesCache = [];
let recordsCache = {};
let activeTierFilter = 0; // 0 = all, 1 = Weak, 2 = Fair, 3 = Strong, 4 = Excellent
let selectedTitle = null;
let currentRecord = null;

function setView(view) {
  app.dataset.view = view;
  $$('.nav-item').forEach((n) => n.classList.toggle('active', n.dataset.nav === view));
  if (view !== 'entry') {
    selectedTitle = null;
    currentRecord = null;
    highlightActive();
  }
  $('.main').scrollTop = 0;
}

// ──────────────────────────────────────────────────────────
// Sidebar list & strength tier filters
// ──────────────────────────────────────────────────────────
async function loadTitles() {
  try {
    const all = await api.all();
    recordsCache = all && typeof all === 'object' ? all : {};
    titlesCache = Object.keys(recordsCache);
  } catch (e) {
    try {
      titlesCache = await api.titles();
    } catch (err) {
      toast(err.message, 'error');
      titlesCache = [];
    }
  }
  titlesCache.sort((a, b) => a.localeCompare(b, undefined, { sensitivity: 'base' }));
  $('#titleOptions').replaceChildren(...titlesCache.map((t) => el('option', { value: t })));
  renderTierFilters();
  renderTitles();
}

function tierForTitle(title) {
  const pwd = recordsCache[title]?.password || '';
  return strengthOf(pwd);
}

function renderTierFilters() {
  if (!tierFiltersWrap) return;
  const counts = { 1: 0, 2: 0, 3: 0, 4: 0 };
  for (const t of titlesCache) {
    const { level } = tierForTitle(t);
    if (counts[level] !== undefined) counts[level] += 1;
  }
  const chips = [
    el(
      'button',
      {
        type: 'button',
        class: `tier-chip${activeTierFilter === 0 ? ' active' : ''}`,
        dataset: { tier: '0' },
        onclick: () => { activeTierFilter = 0; renderTierFilters(); renderTitles(); },
      },
      'All',
      el('span', { class: 'num' }, titlesCache.length)
    ),
    ...STRENGTH_TIERS.map(([, level, name]) =>
      el(
        'button',
        {
          type: 'button',
          class: `tier-chip${activeTierFilter === level ? ' active' : ''}`,
          dataset: { tier: String(level) },
          title: `Show ${name.toLowerCase()} passwords`,
          onclick: () => {
            activeTierFilter = activeTierFilter === level ? 0 : level;
            renderTierFilters();
            renderTitles();
          },
        },
        el('span', { class: 'dot' }),
        name,
        el('span', { class: 'num' }, counts[level])
      )
    ),
  ];
  tierFiltersWrap.replaceChildren(...chips);
}

function renderTitles() {
  const q = searchInput.value.toLowerCase().trim();
  const list = titlesCache.filter((t) => {
    if (q && !t.toLowerCase().includes(q)) return false;
    if (activeTierFilter && tierForTitle(t).level !== activeTierFilter) return false;
    return true;
  });
  entryCount.textContent =
    list.length !== titlesCache.length ? `${list.length}/${titlesCache.length}` : titlesCache.length;

  if (!list.length) {
    titlesWrap.replaceChildren(
      el('div', { class: 'none' }, titlesCache.length ? 'No matching entries' : 'No entries yet')
    );
    return;
  }
  titlesWrap.replaceChildren(
    ...list.map((title) => {
      const s = tierForTitle(title);
      return el(
        'button',
        {
          class: 'entry',
          role: 'option',
          title: s.label ? `${title} — ${s.label}` : title,
          dataset: { title, tier: String(s.level || 0) },
          onclick: () => openEntry(title),
        },
        avatar(title),
        el('span', { class: 'entry-name' }, title),
        s.name ? el('span', { class: 'entry-tier' }, s.name) : null
      );
    })
  );
  highlightActive();
}

function highlightActive() {
  $$('.entry', titlesWrap).forEach((n) => n.classList.toggle('active', n.dataset.title === selectedTitle));
}

// ──────────────────────────────────────────────────────────
// Entry detail
// ──────────────────────────────────────────────────────────
const entryPassword = $('#entryPassword');
const secretRow = $('#secretRow');
const pwToggle = $('#pwToggle');
const KNOWN_KEYS = new Set(['password', 'password_history', 'title_history']);

async function openEntry(title) {
  let data;
  try {
    data = await api.get(title);
  } catch (e) {
    toast(e.message, 'error');
    return;
  }
  setView('entry');
  selectedTitle = title;
  currentRecord = data;
  highlightActive();

  // Header
  $('#entryAvatar').replaceWith(Object.assign(avatar(title, 'avatar lg'), { id: 'entryAvatar' }));
  $('#entryTitle').textContent = title;
  const pwHist = (data.password_history || []).map(parseHistory);
  const meta = [];
  if (data.email) meta.push(data.email);
  const last = pwHist.at(-1)?.date;
  if (last) meta.push(`Updated ${last}`);
  meta.push(`${pwHist.length || 1} version${pwHist.length === 1 ? '' : 's'}`);
  $('#entryMeta').textContent = meta.join('  ·  ');

  // Password
  exitEditMode();
  setMasked(true);
  entryPassword.value = data.password || '';
  renderStrength($('#entryStrength'), entryPassword.value);

  // Every other field in the record (email + anything else stored in Saved.pkl)
  const fields = [];
  const email = data.email;
  fields.push(fieldCard('Email', 'mail', email));
  for (const [key, value] of Object.entries(data)) {
    if (KNOWN_KEYS.has(key) || key === 'email') continue;
    fields.push(fieldCard(humanize(key), 'braces', value));
  }
  $('#entryFields').replaceChildren(...fields);

  // Histories (newest first)
  const titleHist = (data.title_history || []).map(parseHistory);
  renderTimeline($('#titleHistory'), titleHist, false);
  renderTimeline($('#passwordHistory'), pwHist, true);
  $('#titleHistCount').textContent = titleHist.length || '';
  $('#pwHistCount').textContent = pwHist.length || '';
  setHistoryMasked(true);
}

function humanize(key) {
  return key.replace(/[_-]+/g, ' ').replace(/^\w/, (c) => c.toUpperCase());
}

function fieldCard(label, iconName, value) {
  const isEmpty = value === null || value === undefined || value === '';
  const isComplex = !isEmpty && typeof value === 'object';
  const text = isComplex ? JSON.stringify(value, null, 2) : String(value ?? '');
  let body;
  if (isEmpty) {
    body = el('div', { class: 'value' }, el('span', { class: 'empty-val' }, 'Not set'));
  } else if (isComplex) {
    body = el('pre', {}, text);
  } else {
    const btn = el('button', { class: 'icon-btn', title: 'Copy', 'aria-label': `Copy ${label}` }, icon('copy'));
    btn.addEventListener('click', () => copyText(text, btn));
    body = el('div', { class: 'value' }, el('span', {}, text), btn);
  }
  return el(
    'div',
    { class: 'panel field-card' },
    el('div', { class: 'panel-label' }, icon(iconName), label),
    body
  );
}

function renderTimeline(list, items, isSecret) {
  if (!items.length) {
    list.replaceChildren(el('li', { class: 'none' }, 'No history'));
    return;
  }
  const rows = [...items].reverse().map((item, i) => {
    const children = [
      el('span', { class: 'date' }, item.date || '—'),
      el('span', { class: `val${isSecret ? ' mono' : ''}`, title: isSecret ? '' : item.value }, item.value),
    ];
    if (isSecret) {
      const btn = el('button', { class: 'icon-btn', title: 'Copy', 'aria-label': 'Copy this version' }, icon('copy'));
      btn.addEventListener('click', () => copyText(item.value, btn));
      children.push(btn);
    }
    return el('li', { class: i === 0 ? 'current' : '' }, ...children);
  });
  list.replaceChildren(...rows);
}

function setMasked(masked) {
  entryPassword.type = masked ? 'password' : 'text';
  setIcon(pwToggle, masked ? 'eye' : 'eye-off');
  pwToggle.title = masked ? 'Show' : 'Hide';
}

function setHistoryMasked(masked) {
  $('#passwordHistory').classList.toggle('masked', masked);
  $('#pwHistToggle').textContent = masked ? 'Reveal' : 'Hide';
}

function enterEditMode() {
  secretRow.classList.add('editing');
  entryPassword.readOnly = false;
  setMasked(false);
  entryPassword.focus();
  entryPassword.select();
}
function exitEditMode() {
  secretRow.classList.remove('editing');
  entryPassword.readOnly = true;
}

pwToggle.addEventListener('click', () => setMasked(entryPassword.type === 'text'));
$('#pwCopy').addEventListener('click', (e) => copyText(entryPassword.value, e.currentTarget));
$('#pwEdit').addEventListener('click', enterEditMode);
$('#pwCancel').addEventListener('click', () => {
  entryPassword.value = currentRecord?.password || '';
  renderStrength($('#entryStrength'), entryPassword.value);
  exitEditMode();
  setMasked(true);
});
$('#pwGen').addEventListener('click', async (e) => {
  const btn = e.currentTarget;
  btn.classList.remove('spin'); void btn.offsetWidth; btn.classList.add('spin');
  try {
    const { password } = await api.generate(Number($('#lenRange').value) || 20);
    entryPassword.value = password;
    renderStrength($('#entryStrength'), password);
  } catch (err) { toast(err.message, 'error'); }
});
entryPassword.addEventListener('input', () => renderStrength($('#entryStrength'), entryPassword.value));
entryPassword.addEventListener('keydown', (e) => {
  if (secretRow.classList.contains('editing')) {
    if (e.key === 'Enter') $('#pwSave').click();
    if (e.key === 'Escape') $('#pwCancel').click();
  }
});
$('#pwSave').addEventListener('click', async () => {
  const pwd = entryPassword.value.trim();
  if (!pwd) { toast('Password cannot be empty', 'error'); return; }
  if (pwd === currentRecord?.password) { exitEditMode(); setMasked(true); return; }
  try {
    const title = selectedTitle;
    await api.save({ title, password: pwd, email: currentRecord?.email });
    toast('Password updated');
    await loadTitles();
    await openEntry(title);
  } catch (e) { toast(e.message, 'error'); }
});
$('#pwHistToggle').addEventListener('click', () =>
  setHistoryMasked(!$('#passwordHistory').classList.contains('masked'))
);

// Rename
const renameDialog = $('#renameDialog');
const renameInput = $('#renameInput');
$('#renameBtn').addEventListener('click', () => {
  if (!selectedTitle) return;
  renameInput.value = selectedTitle;
  renameDialog.returnValue = '';
  renameDialog.showModal();
  renameInput.select();
});
renameDialog.addEventListener('close', async () => {
  if (renameDialog.returnValue !== 'ok') return;
  const from = selectedTitle;
  const to = renameInput.value.trim();
  if (!to || to === from) return;
  if (titlesCache.includes(to)) { toast(`“${to}” already exists`, 'error'); return; }
  try {
    await api.rename(from, to);
    toast('Entry renamed');
    await loadTitles();
    await openEntry(to);
  } catch (e) { toast(e.message, 'error'); }
});

// Delete
const deleteDialog = $('#deleteDialog');
$('#deleteBtn').addEventListener('click', () => {
  if (!selectedTitle) return;
  $('#deleteName').textContent = selectedTitle;
  deleteDialog.returnValue = '';
  deleteDialog.showModal();
});
deleteDialog.addEventListener('close', async () => {
  if (deleteDialog.returnValue !== 'ok') return;
  try {
    await api.remove(selectedTitle);
    toast('Entry deleted');
    setView('empty');
    await loadTitles();
  } catch (e) { toast(e.message, 'error'); }
});

// ──────────────────────────────────────────────────────────
// Add / Update form
// ──────────────────────────────────────────────────────────
const saveForm = $('#saveForm');
const titleInput = $('#titleInput');
const passwordInput = $('#passwordInput');
const emailInput = $('#emailInput');
const titleHint = $('#titleHint');
const formPwToggle = $('#formPwToggle');

function syncFormMode() {
  const t = titleInput.value.trim();
  const exists = t && titlesCache.includes(t);
  titleHint.className = `hint ${exists ? 'update' : t ? 'new' : ''}`;
  titleHint.textContent = exists
    ? 'Existing entry — the password will be updated and the old one kept in history.'
    : t ? 'New entry' : '';
  // The backend keeps the original email when updating an existing entry.
  emailInput.disabled = !!exists;
  emailInput.placeholder = exists ? 'Kept from existing entry' : 'name@example.com';
  $('#saveBtn span').textContent = exists ? 'Update password' : 'Save entry';
}
titleInput.addEventListener('input', syncFormMode);
passwordInput.addEventListener('input', () => renderStrength($('#formStrength'), passwordInput.value));
formPwToggle.addEventListener('click', () => {
  const show = passwordInput.type === 'password';
  passwordInput.type = show ? 'text' : 'password';
  setIcon(formPwToggle, show ? 'eye-off' : 'eye');
});

$('#genQuickBtn').addEventListener('click', async () => {
  try {
    const { password } = await api.generate(Number($('#lenRange').value) || 20);
    passwordInput.value = password;
    passwordInput.type = 'text';
    setIcon(formPwToggle, 'eye-off');
    renderStrength($('#formStrength'), password);
  } catch (e) { toast(e.message, 'error'); }
});

saveForm.addEventListener('reset', () => {
  setTimeout(() => {
    syncFormMode();
    renderStrength($('#formStrength'), '');
  });
});

saveForm.addEventListener('submit', async (ev) => {
  ev.preventDefault();
  const title = titleInput.value.trim();
  const password = passwordInput.value.trim();
  const email = emailInput.disabled ? undefined : emailInput.value.trim();
  if (!title || !password) { toast('Title and password are required', 'error'); return; }
  try {
    await api.save({ title, password, email });
    toast(titlesCache.includes(title) ? 'Password updated' : 'Entry saved');
    saveForm.reset();
    await loadTitles();
    await openEntry(title);
  } catch (e) { toast(e.message, 'error'); }
});

// ──────────────────────────────────────────────────────────
// Generator
// ──────────────────────────────────────────────────────────
const lenRange = $('#lenRange');
const lenOut = $('#lenOut');
const genResult = $('#genResult');
let generated = '';

function paintGenerated(pwd) {
  generated = pwd;
  // Tint digits and symbols for readability.
  genResult.replaceChildren(
    ...[...pwd].map((ch) =>
      /\d/.test(ch) ? el('span', { class: 'd' }, ch)
        : /[^A-Za-z]/.test(ch) ? el('span', { class: 's' }, ch)
        : document.createTextNode(ch)
    )
  );
  renderStrength($('#genStrength'), pwd);
}

async function generate() {
  const btn = $('#genBtn');
  btn.classList.remove('spin'); void btn.offsetWidth; btn.classList.add('spin');
  try {
    const { password } = await api.generate(Number(lenRange.value));
    paintGenerated(password);
  } catch (e) { toast(e.message, 'error'); }
}

function syncRange() {
  lenOut.textContent = lenRange.value;
  const p = ((lenRange.value - lenRange.min) / (lenRange.max - lenRange.min)) * 100;
  lenRange.style.setProperty('--p', `${p}%`);
}
let rangeTimer;
lenRange.addEventListener('input', () => {
  syncRange();
  clearTimeout(rangeTimer);
  rangeTimer = setTimeout(generate, 120);
});
$('#genBtn').addEventListener('click', generate);
$('#copyBtn').addEventListener('click', (e) => copyText(generated, e.currentTarget));
$('#useGenBtn').addEventListener('click', () => {
  if (!generated) return;
  setView('editor');
  passwordInput.value = generated;
  passwordInput.type = 'text';
  setIcon(formPwToggle, 'eye-off');
  renderStrength($('#formStrength'), generated);
  titleInput.focus();
});

// ──────────────────────────────────────────────────────────
// Navigation & shortcuts
// ──────────────────────────────────────────────────────────
document.addEventListener('click', (e) => {
  const nav = e.target.closest('[data-nav]');
  if (!nav) return;
  const view = nav.dataset.nav;
  setView(view);
  if (view === 'editor') { syncFormMode(); titleInput.focus(); }
  if (view === 'generator' && !generated) generate();
});

searchInput.addEventListener('input', renderTitles);
searchInput.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') { searchInput.value = ''; renderTitles(); searchInput.blur(); }
  if (e.key === 'Enter') $('.entry', titlesWrap)?.click();
});
document.addEventListener('keydown', (e) => {
  const typing = /^(INPUT|TEXTAREA)$/.test(document.activeElement?.tagName);
  if (e.key === '/' && !typing) { e.preventDefault(); searchInput.focus(); }
});

$('#refreshBtn').addEventListener('click', async (e) => {
  const btn = e.currentTarget;
  btn.classList.remove('spin'); void btn.offsetWidth; btn.classList.add('spin');
  await loadTitles();
  if (selectedTitle && titlesCache.includes(selectedTitle)) await openEntry(selectedTitle);
});

// Init
syncRange();
loadTitles();
