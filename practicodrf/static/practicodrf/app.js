const TOKEN_KEY = 'postit_token';

function getToken() {
    return localStorage.getItem(TOKEN_KEY);
}

function requireAuth() {
    if (!getToken()) {
        window.location.href = '/login/';
    }
}

async function apiRequest(url, options = {}) {
    const headers = options.headers || {};
    headers['Content-Type'] = 'application/json';
    const token = getToken();
    if (token) {
        headers['Authorization'] = `Token ${token}`;
    }
    const response = await fetch(url, { ...options, headers });
    if (response.status === 401) {
        localStorage.removeItem(TOKEN_KEY);
        window.location.href = '/login/';
        return null;
    }
    return response;
}

function logout() {
    localStorage.removeItem(TOKEN_KEY);
    window.location.href = '/login/';
}

async function loadNotes() {
    const board = document.getElementById('board');
    const response = await apiRequest('/api/notes/');
    if (!response) return;
    const notes = await response.json();

    board.innerHTML = '';
    notes.forEach((note) => {
        const card = document.createElement('div');
        card.className = `postit ${note.color}`;
        card.innerHTML = `
            <h3>${escapeHtml(note.title)}</h3>
            <p>${escapeHtml(note.content)}</p>
            <div class="actions">
                <button title="Borrar" data-id="${note.id}" class="delete-btn">🗑️</button>
            </div>
        `;
        board.appendChild(card);
    });

    document.querySelectorAll('.delete-btn').forEach((btn) => {
        btn.addEventListener('click', async (event) => {
            const id = event.target.dataset.id;
            await apiRequest(`/api/notes/${id}/`, { method: 'DELETE' });
            loadNotes();
        });
    });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

async function initBoard() {
    requireAuth();
    await loadNotes();

    const form = document.getElementById('note-form');
    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const title = document.getElementById('title').value;
        const content = document.getElementById('content').value;
        const color = document.getElementById('color').value;

        await apiRequest('/api/notes/', {
            method: 'POST',
            body: JSON.stringify({ title, content, color }),
        });

        form.reset();
        loadNotes();
    });

    document.getElementById('logout-btn').addEventListener('click', logout);
}

async function initLogin() {
    const form = document.getElementById('login-form');
    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const errorBox = document.getElementById('error-box');

        const response = await fetch('/api-token-auth/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password }),
        });

        if (!response.ok) {
            errorBox.textContent = 'Usuario o contraseña incorrectos';
            return;
        }

        const data = await response.json();
        localStorage.setItem(TOKEN_KEY, data.token);
        window.location.href = '/';
    });
}

async function initRegister() {
    const form = document.getElementById('register-form');
    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const errorBox = document.getElementById('error-box');

        const response = await fetch('/api/register/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password }),
        });

        if (!response.ok) {
            const data = await response.json();
            errorBox.textContent = JSON.stringify(data);
            return;
        }

        const data = await response.json();
        localStorage.setItem(TOKEN_KEY, data.token);
        window.location.href = '/';
    });
}
