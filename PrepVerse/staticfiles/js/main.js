// Theme Toggle
const themeBtn = document.getElementById('theme-toggle');
const body = document.body;

function setTheme(theme) {
    if (theme === 'dark') {
        body.classList.remove('light-mode');
        body.classList.add('dark-mode');
        themeBtn.textContent = '☀️';
    } else {
        body.classList.remove('dark-mode');
        body.classList.add('light-mode');
        themeBtn.textContent = '🌙';
    }
    localStorage.setItem('prepverse-theme', theme);
}

const savedTheme = localStorage.getItem('prepverse-theme') || 'light';
setTheme(savedTheme);

themeBtn.addEventListener('click', () => {
    const isDark = body.classList.contains('dark-mode');
    setTheme(isDark ? 'light' : 'dark');
});

// Search Spinner
const searchForm = document.getElementById('search-form');
const loader = document.getElementById('loader');

if (searchForm) {
    searchForm.addEventListener('submit', () => {
        loader.style.display = 'block';
    });
}

// Tabs
const tabBtns = document.querySelectorAll('.tab-btn');
const tabPanes = document.querySelectorAll('.tab-pane');

tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const target = btn.dataset.target;
        
        tabBtns.forEach(b => b.classList.remove('active'));
        tabPanes.forEach(p => p.classList.remove('active'));
        
        btn.classList.add('active');
        document.getElementById(target).classList.add('active');
    });
});

// MCQ Selection
document.querySelectorAll('.mcq-card .option-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        const mcqCard = e.currentTarget.closest('.mcq-card');
        const mcqId = mcqCard.dataset.id;
        const value = e.currentTarget.dataset.value;
        
        // Remove selection from others
        mcqCard.querySelectorAll('.option-btn').forEach(b => b.classList.remove('selected'));
        // Add to current
        e.currentTarget.classList.add('selected');
        
        // Set hidden input
        const hiddenInput = document.getElementById(`ans_${mcqId}`);
        if(hiddenInput) hiddenInput.value = value;
    });
});
