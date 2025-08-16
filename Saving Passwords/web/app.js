const api = {
  async titles() {
    const r = await fetch('/api/titles');
    if (!r.ok) throw new Error('Failed to load titles');
    return r.json();
  },
  async get(title) {
    const r = await fetch(`/api/password/${encodeURIComponent(title)}`);
    if (!r.ok) throw new Error('Title not found');
    return r.json();
  },
  async save({ title, password, email }) {
    const r = await fetch('/api/password', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, password, email: email || null })
    });
    if (!r.ok) throw new Error('Failed to save');
    return r.json();
  },
  async remove(title) {
    const r = await fetch(`/api/password/${encodeURIComponent(title)}`, { method: 'DELETE' });
    if (!r.ok) throw new Error('Failed to delete');
    return r.json();
  },
  async rename(currentTitle, newTitle) {
    const r = await fetch('/api/title', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ currentTitle, newTitle })
    });
    if (!r.ok) throw new Error('Failed to rename');
    return r.json();
  },
  async generate(length) {
    const r = await fetch('/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ length })
    });
    if (!r.ok) {
      const msg = await r.json().catch(() => ({}));
      throw new Error(msg.detail || 'Failed to generate');
    }
    return r.json();
  }
};

// UI helpers
const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

function toast(msg, type = 'info') {
  let t = document.createElement('div');
  t.className = `toast ${type}`;
  t.textContent = msg;
  Object.assign(t.style, {
    position: 'fixed', bottom: '16px', right: '16px', padding: '10px 12px',
    borderRadius: '10px', background: type === 'error' ? '#ef4444' : '#334155', color: 'white',
    zIndex: 1000, boxShadow: '0 8px 20px rgba(0,0,0,.35)'
  });
  document.body.appendChild(t);
  setTimeout(() => t.remove(), 2200);
}

function copyToClipboard(text) {
  navigator.clipboard?.writeText(text).then(() => toast('Copied'))
    .catch(() => { toast('Copy failed', 'error'); });
}

// Elements
const titlesWrap = $('#titles');
const searchInput = $('#searchInput');
const detailsCard = $('#detailsCard');
const detailsTitle = $('#detailsTitle');
const detailsBody = $('#detailsBody');
const renameBtn = $('#renameBtn');
const deleteBtn = $('#deleteBtn');

const saveForm = $('#saveForm');
const titleInput = $('#titleInput');
const passwordInput = $('#passwordInput');
const emailInput = $('#emailInput');
const genQuickBtn = $('#genQuickBtn');
const refreshBtn = $('#refreshBtn');

const lenRange = $('#lenRange');
const lenOut = $('#lenOut');
const genBtn = $('#genBtn');
const genResult = $('#genResult');
const copyBtn = $('#copyBtn');

let titlesCache = [];
let selectedTitle = null;

async function renderTitles() {
  try {
    titlesCache = await api.titles();
  } catch (e) {
    toast(e.message || 'Failed to load titles', 'error');
    titlesCache = [];
  }
  const q = (searchInput.value || '').toLowerCase().trim();
  const list = q ? titlesCache.filter(t => t.toLowerCase().includes(q)) : titlesCache;

  titlesWrap.innerHTML = '';
  const tpl = $('#titleItemTpl');
  list.forEach(title => {
    const node = tpl.content.firstElementChild.cloneNode(true);
    node.textContent = title;
    node.addEventListener('click', () => openDetails(title));
    titlesWrap.appendChild(node);
  });
}

async function openDetails(title) {
  try {
    const data = await api.get(title);
    selectedTitle = title;
    detailsTitle.textContent = `Details · ${title}`;
    detailsCard.hidden = false;

    // Build details from template
    detailsBody.innerHTML = '';
    const tpl = $('#detailsTpl');
    const frag = tpl.content.cloneNode(true);

    // Fill fields
    $('[data-k="title"]', frag).textContent = title;

    const pwdInput = $('[data-k="password"]', frag);
    pwdInput.value = data.password || '';

    const emailEl = $('[data-k="email"]', frag);
    emailEl.textContent = data.email || '';

    $('[data-k="title_history"]', frag).textContent = (data.title_history || []).join('\n');
    $('[data-k="password_history"]', frag).textContent = (data.password_history || []).join('\n');

    // Actions for password
    $('[data-action="toggle"]', frag).addEventListener('click', () => {
      pwdInput.type = pwdInput.type === 'password' ? 'text' : 'password';
    });
    $('[data-action="copy"]', frag).addEventListener('click', () => copyToClipboard(pwdInput.value));
    $('[data-action="update"]', frag).addEventListener('click', async () => {
      const newPwd = (pwdInput.value || '').trim();
      if (!newPwd) { toast('Password cannot be empty', 'error'); return; }
      try {
        await api.save({ title, password: newPwd, email: data.email });
        toast('Updated');
        await openDetails(title);
      } catch (e) {
        toast(e.message || 'Update failed', 'error');
      }
    });

    detailsBody.appendChild(frag);
  } catch (e) {
    toast(e.message || 'Unable to load details', 'error');
  }
}

// Search filter
searchInput.addEventListener('input', () => renderTitles());

// Save form
saveForm.addEventListener('submit', async (ev) => {
  ev.preventDefault();
  const title = titleInput.value.trim();
  const password = passwordInput.value.trim();
  const email = emailInput.value.trim();
  if (!title || !password) { toast('Title and Password required', 'error'); return; }
  try {
    await api.save({ title, password, email });
    toast('Saved');
    await renderTitles();
    if (selectedTitle === title) await openDetails(title);
    saveForm.reset();
  } catch (e) {
    toast(e.message || 'Save failed', 'error');
  }
});

// Quick generate for form
genQuickBtn.addEventListener('click', async () => {
  try {
    const length = parseInt(lenRange.value, 10) || 12;
    const { password } = await api.generate(length);
    passwordInput.value = password;
  } catch (e) { toast(e.message || 'Generate failed', 'error'); }
});

// Generator section
lenRange.addEventListener('input', () => { lenOut.textContent = lenRange.value; });
genBtn.addEventListener('click', async () => {
  try {
    const length = parseInt(lenRange.value, 10);
    const { password } = await api.generate(length);
    genResult.value = password;
  } catch (e) { toast(e.message || 'Generate failed', 'error'); }
});
copyBtn.addEventListener('click', () => { if (genResult.value) copyToClipboard(genResult.value); });

// Rename & delete
renameBtn.addEventListener('click', async () => {
  if (!selectedTitle) return;
  const newTitle = prompt('Enter new title', selectedTitle)?.trim();
  if (!newTitle || newTitle === selectedTitle) return;
  try {
    await api.rename(selectedTitle, newTitle);
    toast('Renamed');
    await renderTitles();
    await openDetails(newTitle);
  } catch (e) { toast(e.message || 'Rename failed', 'error'); }
});

deleteBtn.addEventListener('click', async () => {
  if (!selectedTitle) return;
  if (!confirm(`Delete \"${selectedTitle}\"?`)) return;
  try {
    await api.remove(selectedTitle);
    toast('Deleted');
    selectedTitle = null;
    detailsCard.hidden = true;
    await renderTitles();
  } catch (e) { toast(e.message || 'Delete failed', 'error'); }
});

refreshBtn.addEventListener('click', () => renderTitles());

// Initial load
renderTitles();
