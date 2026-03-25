// Supabase Configuration
// IMPORTANT: Replace with actual Supabase URL and Anon Key in production
const SUPABASE_URL = 'https://your-project.supabase.co';
const SUPABASE_ANON_KEY = 'your-anon-key';

// Initialize Supabase Client
const supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// DOM Elements
const authSection = document.getElementById('authSection');
const uploadSection = document.getElementById('uploadSection');
const userState = document.getElementById('userState');
const authMessage = document.getElementById('authMessage');
const uploadMessage = document.getElementById('uploadMessage');

// Auth Event Listeners
document.getElementById('loginBtn').addEventListener('click', (e) => handleAuth(e, 'login'));
document.getElementById('registerBtn').addEventListener('click', (e) => handleAuth(e, 'register'));
document.getElementById('logoutBtn').addEventListener('click', handleLogout);

// Upload Event Listener
document.getElementById('uploadForm').addEventListener('submit', handleUpload);

// Check current session on load
checkSession();

supabase.auth.onAuthStateChange((event, session) => {
    updateUI(session);
});

async function checkSession() {
    try {
        const { data: { session }, error } = await supabase.auth.getSession();
        if (error) throw error;
        updateUI(session);
    } catch (err) {
        console.error("Supabase not properly configured yet.", err);
        showMessage(authMessage, "⚠️ Supabase Verbindung konnte nicht hergestellt werden. (API Keys prüfen)", "error");
    }
}

function updateUI(session) {
    if (session) {
        authSection.classList.remove('active');
        uploadSection.classList.add('active');
        userState.textContent = `Angemeldet als: ${session.user.email}`;
    } else {
        uploadSection.classList.remove('active');
        authSection.classList.add('active');
        userState.textContent = 'Nicht angemeldet';
    }
}

async function handleAuth(event, type) {
    event.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    if(!email || !password) {
        showMessage(authMessage, "Bitte E-Mail und Passwort eingeben.", "error");
        return;
    }

    showMessage(authMessage, "Wird verarbeitet...", "");

    try {
        let error = null;
        if (type === 'register') {
            const { error: signUpError } = await supabase.auth.signUp({ email, password });
            error = signUpError;
            if(!error) showMessage(authMessage, "Registrierung erfolgreich! Bitte E-Mail bestätigen oder direkt einloggen.", "success");
        } else {
            const { error: signInError } = await supabase.auth.signInWithPassword({ email, password });
            error = signInError;
        }

        if (error) throw error;
    } catch (error) {
        showMessage(authMessage, `Fehler: ${error.message}`, "error");
    }
}

async function handleLogout() {
    await supabase.auth.signOut();
}

async function handleUpload(event) {
    event.preventDefault();
    
    const modData = {
        name: document.getElementById('modName').value,
        author: document.getElementById('modAuthor').value,
        version: document.getElementById('modVersion').value,
        description: document.getElementById('modDesc').value,
        download_url: document.getElementById('modUrl').value,
        is_verified: false 
    };
    
    // Auto-generate a simple string ID
    modData.id = modData.name.toLowerCase().replace(/[^a-z0-9]+/g, '-') + '-' + Math.floor(Math.random() * 10000);

    showMessage(uploadMessage, "Wird hochgeladen...", "");

    try {
        const { error } = await supabase.table('mods').insert([modData]);
        if (error) throw error;
        
        showMessage(uploadMessage, "Mod erfolgreich eingereicht! Sieht gut aus.", "success");
        document.getElementById('uploadForm').reset();
    } catch (error) {
        showMessage(uploadMessage, `Fehler: ${error.message}`, "error");
    }
}

function showMessage(element, text, type) {
    element.textContent = text;
    element.className = 'message ' + (type === 'error' ? 'msg-error' : (type === 'success' ? 'msg-success' : ''));
    
    if (type === 'success') {
        setTimeout(() => { element.textContent = ''; }, 5000);
    }
}
