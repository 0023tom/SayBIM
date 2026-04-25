// Game State
let gameState = {
    hearts: 5,
    diamonds: 500,
    streak: 0,
    nextHeartIn: 0,
    currentQuestionIndex: 0,
    totalQuestions: 10,
    questions: [],
    questions: [],
    username: '',
    detectionPaused: true, 
    targetLetter: null,    
    sessionXp: 0,          // Track XP gained in current session
    badges: [],
    equippedBadge: null
};

// Lesson Steps Progress (0-5 steps per lesson)
let userProgress = {};

let quizTimerInterval = null;
let currentRemainingTime = 180;

let heartTimer = null;

let toastQueue = [];
let isToastShowing = false;

function showFloatMessage(message, type = 'info', callback = null, forceBlur = false) {
    // Add request to queue
    toastQueue.push({ message, type, callback, forceBlur });
    processToastQueue();
}

function processToastQueue() {
    if (isToastShowing || toastQueue.length === 0) return;

    isToastShowing = true;
    const { message, type, callback, forceBlur } = toastQueue.shift();

    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        document.body.appendChild(container);
    }

    const msg = document.createElement('div');
    msg.className = `alert alert-${type} float-msg`;

    // Auto-detect warning/success levels from content if needed
    if (message.toLowerCase().includes('error') || message.toLowerCase().includes('failed') || message.toLowerCase().includes('incorrect')) {
        msg.className = `alert alert-danger float-msg`;
    } else if (message.toLowerCase().includes('success') || message.toLowerCase().includes('correct') || message.toLowerCase().includes('+')) {
        msg.className = `alert alert-success float-msg`;
    }

    // Apply blur for a premium experience
    container.classList.add('blur-active');
    msg.dataset.blur = "true";

    msg.innerHTML = `<div style="margin-bottom: 20px;">${message}</div><button class="toast-ok-btn" style="padding: 10px 30px; border: none; border-radius: 12px; font-weight: bold; cursor: pointer; background: white; color: var(--text-primary); box-shadow: var(--shadow-soft); transition: all 0.2s;">OK</button>`;

    const okBtn = msg.querySelector('.toast-ok-btn');
    if (okBtn) {
        okBtn.addEventListener('click', () => {
            msg.style.animation = 'fadeOutToast 0.4s forwards';
            setTimeout(() => {
                if (msg.parentElement) msg.remove();

                // Cleanup blur if no more messages
                if (!container.querySelector('.float-msg')) {
                    container.classList.remove('blur-active');
                }

                if (callback) callback();

                // Process next in queue
                isToastShowing = false;
                processToastQueue();
            }, 400);
        });

        // Hover effect for button
        okBtn.onmouseover = () => okBtn.style.transform = 'scale(1.05)';
        okBtn.onmouseout = () => okBtn.style.transform = 'scale(1)';
    }

    container.appendChild(msg);
}

function showFloatConfirm(message, onConfirm) {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        document.body.appendChild(container);
    }
    const msg = document.createElement('div');
    msg.className = `alert alert-danger float-msg`;

    msg.innerHTML = `
        <div style="margin-bottom: 10px;">${message}</div>
        <div style="display: flex; gap: 10px;">
            <button class="toast-cancel-btn" style="padding: 8px 15px; border: 1px solid #ccc; border-radius: 8px; font-weight: bold; cursor: pointer; background: white; color: #333;">Cancel</button>
            <button class="toast-confirm-btn" style="padding: 8px 15px; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; background: var(--accent-red); color: white; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">Delete</button>
        </div>
    `;

    container.classList.add('blur-active');
    msg.dataset.blur = "true";

    const cancelBtn = msg.querySelector('.toast-cancel-btn');
    const confirmBtn = msg.querySelector('.toast-confirm-btn');

    cancelBtn.addEventListener('click', () => {
        msg.style.animation = 'fadeOutToast 0.4s forwards';
        setTimeout(() => {
            if (msg.parentElement) msg.remove();
            if (!container.querySelector('[data-blur="true"]')) {
                container.classList.remove('blur-active');
            }
        }, 400);
    });

    confirmBtn.addEventListener('click', () => {
        msg.style.animation = 'fadeOutToast 0.4s forwards';
        setTimeout(() => {
            if (msg.parentElement) msg.remove();
            if (!container.querySelector('[data-blur="true"]')) {
                container.classList.remove('blur-active');
            }
            if (onConfirm) onConfirm();
        }, 400);
    });

    container.appendChild(msg);
}

function showQuitConfirmation(message, onConfirm, onCancel) {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        document.body.appendChild(container);
    }
    const msg = document.createElement('div');
    msg.className = `alert alert-warning float-msg`;

    msg.innerHTML = `
        <div style="margin-bottom: 20px; font-weight: bold; font-size: 1.1em;">${message}</div>
        <div style="display: flex; gap: 15px; justify-content: center;">
            <button class="toast-cancel-btn" style="padding: 10px 25px; border: 1px solid #ccc; border-radius: 12px; font-weight: bold; cursor: pointer; background: white; color: #333; transition: all 0.2s;">No</button>
            <button class="toast-confirm-btn" style="padding: 10px 25px; border: none; border-radius: 12px; font-weight: bold; cursor: pointer; background: var(--accent-red); color: white; box-shadow: 0 4px 10px rgba(239, 68, 68, 0.2); transition: all 0.2s;">Yes</button>
        </div>
    `;

    container.classList.add('blur-active');
    msg.dataset.blur = "true";

    const cancelBtn = msg.querySelector('.toast-cancel-btn');
    const confirmBtn = msg.querySelector('.toast-confirm-btn');

    const closeToast = () => {
        msg.style.animation = 'fadeOutToast 0.4s forwards';
        setTimeout(() => {
            if (msg.parentElement) msg.remove();
            if (!container.querySelector('[data-blur="true"]')) {
                container.classList.remove('blur-active');
            }
        }, 400);
    };

    cancelBtn.onclick = () => {
        closeToast();
        if (onCancel) onCancel();
    };

    confirmBtn.onclick = () => {
        closeToast();
        if (onConfirm) onConfirm();
    };

    container.appendChild(msg);
}

function confirmExit(onConfirm) {
    const isMastery = (window.CURRENT_TOPIC_ID === 1 && window.CURRENT_LESSON_ID === 8) || 
                      (window.CURRENT_TOPIC_ID === 2 && window.CURRENT_LESSON_ID === 9) || 
                      (window.CURRENT_TOPIC_ID === 3 && window.CURRENT_LESSON_ID === 24);
    
    if (isMastery) {
        pauseQuizTimer();
    }

    showQuitConfirmation("Are you sure you want to quit?", () => {
        if (onConfirm) onConfirm();
    }, () => {
        if (isMastery) {
            startQuizTimer();
        }
    });
}

function startHeartTimer() {
    if (heartTimer) clearInterval(heartTimer);
    heartTimer = setInterval(() => {
        if (gameState.hearts < 5 && gameState.nextHeartIn > 0) {
            gameState.nextHeartIn--;
            updateDashboardStats();

            if (gameState.nextHeartIn <= 0) {
                fetch('/api/user')
                    .then(res => res.json())
                    .then(data => {
                        gameState.hearts = data.hearts;
                        gameState.nextHeartIn = data.next_heart_in_seconds || 0;
                        updateDashboardStats();
                    });
            }
        }
    }, 1000);
}

// Practice State & Config
let practiceSession = {
    active: false,
    category: null,
    items: [],
    currentIndex: 0,
    score: 0
};

const practiceConfig = {
    alphabets: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'],
    // Disable others for now as models only support Alphabets & Numbers
    numbers: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
    objects: [],
    foods: [],
    beverages: [],
    actions: [],
    emotions: [],
    greetings: [],
    school: []
};

function renderLessonCards() {
    let t1Prog = gameState.topicProgress ? (gameState.topicProgress['1'] || 1) : 1;
    let t2Prog = gameState.topicProgress ? (gameState.topicProgress['2'] || 1) : 1;
    let t3Prog = gameState.topicProgress ? (gameState.topicProgress['3'] || 18) : 18;

    let bar1 = document.getElementById('progress-bar-1');
    let card1 = document.getElementById('lesson-card-1');
    if (bar1) {
        if (t1Prog > 8) {
            bar1.style.width = '100%';
            bar1.style.background = 'var(--accent-green)';
        } else {
            bar1.style.width = `${((t1Prog - 1) / 8) * 100}%`;
        }
    }

    let bar2 = document.getElementById('progress-bar-2');
    let card2 = document.getElementById('lesson-card-2');
    let icon2 = document.getElementById('lesson-icon-2');
    let text2 = document.getElementById('lesson-text-2');
    if (bar2) {
        if (t2Prog > 9) {
            bar2.style.width = '100%';
            bar2.style.background = 'var(--accent-green)';
        } else {
            bar2.style.width = `${((t2Prog - 1) / 9) * 100}%`;
        }
    }

    let bar3 = document.getElementById('progress-bar-3');
    let card3 = document.getElementById('lesson-card-3');
    let icon3 = document.getElementById('lesson-icon-3');
    let text3 = document.getElementById('lesson-text-3');
    if (bar3) {
        if (t3Prog > 24) {
            bar3.style.width = '100%';
            bar3.style.background = 'var(--accent-green)';
        } else {
            bar3.style.width = `${((t3Prog - 18) / 7) * 100}%`;
        }
    }

    // Topic 1 Unlocks Topic 2
    let isT2Unlocked = t1Prog > 8;
    if (isT2Unlocked) {
        if (card2) {
            card2.classList.remove('locked');
            card2.style.pointerEvents = "auto";
        }
        if (icon2) {
            icon2.className = 'fas fa-book-open';
            icon2.style.color = 'var(--accent-blue)';
        }
        if (text2) text2.style.color = 'var(--accent-blue)';
    } else {
        if (card2) {
            card2.classList.add('locked');
            card2.style.pointerEvents = "none";
        }
        if (icon2) {
            icon2.className = 'fas fa-lock';
            icon2.style.color = 'var(--text-secondary)';
        }
        if (text2) text2.style.color = 'var(--text-secondary)';
    }

    // Topic 2 Unlocks Topic 3
    let isT3Unlocked = t2Prog > 9;
    if (isT3Unlocked) {
        if (card3) {
            card3.classList.remove('locked');
            card3.style.pointerEvents = "auto";
        }
        if (icon3) {
            icon3.className = 'fas fa-book-open';
            icon3.style.color = 'var(--accent-blue)';
        }
        if (text3) text3.style.color = 'var(--accent-blue)';
    } else {
        if (card3) {
            card3.classList.add('locked');
            card3.style.pointerEvents = "none";
        }
        if (icon3) {
            icon3.className = 'fas fa-lock';
            icon3.style.color = 'var(--text-secondary)';
        }
        if (text3) text3.style.color = 'var(--text-secondary)';
    }
}

function switchSection(section) {
    const sectionToNavText = {
        'lesson': 'Lesson',
        'practice': 'Practice',
        'setting': 'Setting',
        'challenge': 'Challenge',
        'shop': 'Shop',
        'leaderboard': 'Leaderboard',
        'badges': 'Badges'
    };
    const targetText = sectionToNavText[section];
    const links = document.querySelectorAll('.nav-link');
    links.forEach(l => {
        if (l.textContent.trim() === targetText) {
            l.classList.add('active');
        } else {
            l.classList.remove('active');
        }
    });

    if (window.CURRENT_PAGE_TYPE !== 'quiz' && window.CURRENT_PAGE_TYPE !== 'practice') {

        showSection(section);
        if (section === 'leaderboard') fetchLeaderboard();
        if (section === 'setting') showSubMenu('main');
        if (section === 'badges') renderBadgeSection();
    } else {
        // Redirect to home with section parameter
        window.location.href = `/?section=${section}`;
    }
}

document.addEventListener('DOMContentLoaded', async () => {
    await initGame();
    startLeaderboardTimer();

    // Handle URL parameters for section switching
    const params = new URLSearchParams(window.location.search);
    const targetSection = params.get('section');
    if (targetSection) {
        switchSection(targetSection);
    }

    // Auto-collapse sidebar on mobile/narrow screens
    if (window.innerWidth <= 1024 || /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
        const sidebar = document.querySelector('.sidebar');
        if (sidebar) {
            sidebar.classList.add('collapsed');
        }
    }

    // 1. Page-Specific Rendering
    if (window.CURRENT_PAGE_TYPE === 'quiz') {
        startHeartTimer();
    } else if (window.CURRENT_PAGE_TYPE === 'practice') {
        // Practice page specialized UI is handled in its template
    } else {
        renderLessonCards();
    }

    // 2. Shared Setup (Runs on ALL pages)
    const links = document.querySelectorAll('.nav-link');
    links.forEach(link => {
        link.addEventListener('click', (e) => {
            const text = link.textContent.trim();
            const textToSection = {
                'Lesson': 'lesson',
                'Practice': 'practice',
                'Leaderboard': 'leaderboard',
                'Setting': 'setting',
                'Challenge': 'challenge',
                'Shop': 'shop',
                'Badges': 'badges'
            };
            if (textToSection[text]) {
                e.preventDefault();
                switchSection(textToSection[text]);
            }
        });
    });

    // Initialize Settings Toggles
    const soundToggle = document.getElementById('sound-toggle');
    const cameraToggle = document.getElementById('camera-toggle');

    if (soundToggle) {
        soundToggle.checked = localStorage.getItem('saybim_sound') !== 'false';
        soundToggle.addEventListener('change', (e) => {
            localStorage.setItem('saybim_sound', e.target.checked);
        });
    }

    if (cameraToggle) {
        cameraToggle.checked = localStorage.getItem('saybim_camera') !== 'false';
        cameraToggle.addEventListener('change', (e) => {
            localStorage.setItem('saybim_camera', e.target.checked);
        });
    }

    // 3. Load Model (Only on Practice page)
    if (window.CURRENT_PAGE_TYPE === 'practice') {
        loadModel();
    }

    // 4. Handle Practice URL Parameters
    if (window.CURRENT_PAGE_TYPE === 'practice') {
        const urlParams = new URLSearchParams(window.location.search);
        const type = urlParams.get('type') || 'alphabets';
        renderPracticeButtons(type);

        // Immediate Number Notice: Handled by practice logic
        if (type === 'numbers') {
            const maintenanceOverlay = document.getElementById('maintenance-overlay');
            if (maintenanceOverlay) maintenanceOverlay.style.display = 'none';
        }
    }
});

function updateGameState(data) {
    if (!data) return;
    
    // Support both direct user object or wrap with full response
    const userData = data.user || data;
    const newBadges = data.new_badges || userData.new_badges;

    if (userData.username) gameState.username = userData.username;
    if (userData.xp !== undefined) gameState.xp = userData.xp;
    if (userData.level !== undefined) gameState.level = userData.level;
    if (userData.hearts !== undefined) gameState.hearts = userData.hearts;
    if (userData.diamonds !== undefined) gameState.diamonds = userData.diamonds;
    if (userData.streak !== undefined) gameState.streak = userData.streak;
    if (userData.shield_count !== undefined) gameState.shieldCount = userData.shield_count;
    if (userData.timer_freeze_count !== undefined) gameState.timerFreezeCount = userData.timer_freeze_count;
    if (userData.xp_boost_active !== undefined) gameState.xpBoostActive = userData.xp_boost_active;
    if (userData.xp_boost_expiry !== undefined) gameState.xpBoostExpiry = userData.xp_boost_expiry;
    
    if (userData.badges) gameState.badges = userData.badges;
    if (userData.equipped_badge !== undefined) gameState.equippedBadge = userData.equipped_badge;

    if (userData.topic_progress) {
        try {
            gameState.topicProgress = typeof userData.topic_progress === 'string' 
                ? JSON.parse(userData.topic_progress) 
                : userData.topic_progress;
        } catch(e) { console.error("Parse progress error", e); }
    }

    // Initialize/Sync userProgress (lesson steps)
    const storedProgress = localStorage.getItem('saybim_lesson_progress_' + gameState.username);
    if (storedProgress) {
        try {
            userProgress = JSON.parse(storedProgress);
        } catch(e) { userProgress = {}; }
    }

    // UI Updates
    updateDashboardStats();
    updateInventoryUI();
    updateShopUI();
    renderBadgeEquipUI();
    renderBadgeSection();

    // Sidebar Badge Icon update
    const sidebarBadge = document.getElementById('sidebar-badge-icon');
    if (sidebarBadge) {
        if (gameState.equippedBadge) {
            sidebarBadge.innerText = gameState.equippedBadge.emoji || '🏅';
            sidebarBadge.style.display = 'flex';
        } else {
            sidebarBadge.style.display = 'none';
        }
    }

    // Badge celebration check
    if (newBadges && Array.isArray(newBadges)) {
        newBadges.forEach(badgeName => {
            const badge = BADGE_DEFS.find(b => b.name === badgeName || b.key === badgeName);
            if (badge) {
                // If it's a quiz or practice completion, we might want to delay it
                // For now, we always queue it to ensure sequential display
                queueBadgeCelebration(badge.key);
            }
        });
        
        // If we are NOT in a quiz/practice result flow, process immediately
        // Otherwise, the result flow will call processBadgeQueue()
        if (window.CURRENT_PAGE_TYPE !== 'quiz' && !practiceSession.active) {
            processBadgeQueue();
        }
    }
}

async function initGame() {
    try {
        // 1. Fetch User Data (Always needed)
        const userRes = await fetch('/api/user');
        const userData = await userRes.json();
        updateGameState(userData);

        if (window.CURRENT_PAGE_TYPE !== 'quiz') {
            const nameDisplay = document.getElementById('user-name-display');
            if (nameDisplay) nameDisplay.innerText = gameState.username;
            startHeartTimer();
            return; // Exit early if not a quiz
        }

        // 2. Fetch Quiz Data (Only on quiz page)
        const quizUrl = `/api/quiz/${window.CURRENT_TOPIC_ID || 1}/${window.CURRENT_LESSON_ID || 1}`;
        const quizRes = await fetch(quizUrl);
        const quizData = await quizRes.json();

        gameState.questions = quizData;
        gameState.totalQuestions = quizData.length;
        gameState.currentLessonId = window.CURRENT_LESSON_ID;
        gameState.currentTopicId = window.CURRENT_TOPIC_ID;
        gameState.currentQuestionIndex = 0;

        // Mastery Quizzes: Topic 1 (L8) or Topic 2 (L9)
        if ((gameState.currentTopicId === 1 && gameState.currentLessonId === 8) || (gameState.currentTopicId === 2 && gameState.currentLessonId === 9) || (gameState.currentTopicId === 3 && gameState.currentLessonId === 24)) {
            if (gameState.currentTopicId === 3 && gameState.currentLessonId === 24) {
                currentRemainingTime = 300;
                document.getElementById('quiz-timer-display').innerText = '05:00';
            } else {
                currentRemainingTime = 180;
                document.getElementById('quiz-timer-display').innerText = '03:00';
            }
            startQuizTimer();
        }
        updateQuizUI();

    } catch (err) {
        console.error("Failed to init game:", err);
    }
}

function showSection(section) {
    const lessonSec = document.getElementById('lesson-section');
    const practiceSec = document.getElementById('practice-section');
    const leaderboardSec = document.getElementById('leaderboard-section');
    const settingSec = document.getElementById('setting-section');
    const challengeSec = document.getElementById('challenge-section');
    const shopSec = document.getElementById('shop-section');

    if (lessonSec) lessonSec.style.display = (section === 'lesson') ? 'block' : 'none';
    if (practiceSec) practiceSec.style.display = (section === 'practice') ? 'block' : 'none';
    if (leaderboardSec) leaderboardSec.style.display = (section === 'leaderboard') ? 'block' : 'none';
    if (settingSec) settingSec.style.display = (section === 'setting') ? 'block' : 'none';
    if (challengeSec) challengeSec.style.display = (section === 'challenge') ? 'block' : 'none';
    if (shopSec) shopSec.style.display = (section === 'shop') ? 'block' : 'none';
    const badgeSec = document.getElementById('badges-section');
    if (badgeSec) badgeSec.style.display = (section === 'badges') ? 'block' : 'none';
}

function fetchLeaderboard() {
    fetch('/api/leaderboard')
        .then(res => res.json())
        .then(users => {
            const tbody = document.getElementById('leaderboard-body');
            tbody.innerHTML = '';
            users.forEach((user, index) => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td style="padding: 15px 10px; border-bottom: 1px solid #f0f0f0; text-align: center; font-size: 1.6em; font-weight: bold; color: var(--text-secondary);">
                        ${index + 1 === 1 ? '🥇' : index + 1 === 2 ? '🥈' : index + 1 === 3 ? '🥉' : index + 1}
                    </td>
                    <td style="padding: 15px 10px; border-bottom: 1px solid #f0f0f0; font-weight: bold; display: flex; align-items: center; gap: 10px;">
                        <div style="width: 30px; height: 30px; border-radius: 50%; background: var(--accent-blue); color: white; display: flex; align-items: center; justify-content: center; overflow: hidden; font-size: 0.9em;">
                            ${user.avatar ? `<img src="${user.avatar}" style="width: 100%; height: 100%; object-fit: cover;">` : user.username.charAt(0).toUpperCase()}
                        </div>
                        <div>
                            ${user.username}
                            ${user.username === gameState.username ? '<span style="font-size:0.8em; color:var(--accent-blue)">(You)</span>' : ''}
                            ${user.equipped_badge ? `<span style="margin-left:8px; font-size:0.75em; background:#edf2ff; color:#3f51b5; border-radius:999px; padding:2px 8px; font-weight:700; white-space:nowrap;">${formatBadgeLabel(user.equipped_badge)}</span>` : ''}
                        </div>
                    </td>
                    <td style="padding: 15px 10px; border-bottom: 1px solid #f0f0f0; text-align: center;">${user.level}</td>
                    <td style="padding: 15px 10px; border-bottom: 1px solid #f0f0f0; text-align: center; color: var(--accent-yellow); font-weight: bold;">${user.xp} XP</td>
                `;
                tbody.appendChild(tr);
            });
        });
}

function formatBadgeLabel(badge) {
    if (!badge) return '';
    return `${badge.emoji || ''} ${badge.name || ''}`.trim();
}

function formatBadgeExpiry(expiresAtIso) {
    if (!expiresAtIso) return '';
    const expiry = new Date(expiresAtIso);
    const now = new Date();
    const diff = expiry - now;
    if (diff <= 0) return 'expired';
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
    const minutes = Math.floor((diff / (1000 * 60)) % 60);
    return `${days}d ${String(hours).padStart(2, '0')}h ${String(minutes).padStart(2, '0')}m`;
}

function startLeaderboardTimer() {
    function updateTimer() {
        const now = new Date();
        const nextMonday = new Date();
        nextMonday.setDate(now.getDate() + ((7 - now.getDay()) % 7 + 1));
        nextMonday.setHours(0, 0, 0, 0);

        const diffTime = nextMonday - now;
        const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
        const diffHours = Math.floor((diffTime / (1000 * 60 * 60)) % 24);
        const diffMinutes = Math.floor((diffTime / 1000 / 60) % 60);

        const timerSpan = document.getElementById('leaderboard-timer');
        if (timerSpan) {
            timerSpan.innerText = `${diffDays}d ${diffHours.toString().padStart(2, '0')}h ${diffMinutes.toString().padStart(2, '0')}m`;
        }
    }

    updateTimer();
    setInterval(updateTimer, 60000);
}

function openLesson(lessonId, lessonName) {
    gameState.currentLessonId = lessonId;
    gameState.currentQuestionIndex = 0;
    gameState.sessionXp = 0; // Reset session XP
    if (gameState.hearts <= 0) {
        showGameOver();
        return;
    }
    updateQuizUI();
    document.getElementById('quiz-modal').classList.add('active');
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.remove('active');
}

function renderPracticeButtons(type) {
    const container = document.getElementById('practice-target-btns');
    if (!container) return;

    container.innerHTML = '';
    const items = type === 'alphabets'
        ? ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        : ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'];

    items.forEach(item => {
        const btn = document.createElement('button');
        btn.className = 'quiz-btn';
        btn.style.padding = '15px';
        btn.innerText = item;
        btn.onclick = () => {
            // Remove previous selections
            container.querySelectorAll('.quiz-btn').forEach(b => b.classList.remove('selected'));
            btn.classList.add('selected');

            const maintenanceOverlay = document.getElementById('maintenance-overlay');
            const cameraIndicator = document.getElementById('camera-active-status');

            if (type === 'numbers') {
                if (maintenanceOverlay) maintenanceOverlay.style.display = 'none';
                startSinglePractice(type, item);
            } else {
                if (maintenanceOverlay) maintenanceOverlay.style.display = 'none';
                startSinglePractice(type, item);
            }
        };
        container.appendChild(btn);
    });
}

function startSinglePractice(category, target) {
    gameState.targetLetter = target;
    gameState.detectionPaused = false;

    // UI Updates
    const placeholder = document.getElementById('practice-placeholder');
    const cameraContainer = document.getElementById('practice-camera-container');
    const maintenanceOverlay = document.getElementById('maintenance-overlay');

    // On standalone page, we stay in the same view but update components
    if (placeholder) placeholder.style.display = 'none';
    if (cameraContainer) cameraContainer.style.display = 'block';
    if (maintenanceOverlay) maintenanceOverlay.style.display = 'none'; // Hide overlay when active

    // Ensure camera is open
    openCameraModal(`Sign the letter/number: ${target}`);

    // Update Reference Image
    const refContainer = document.getElementById('reference-sign-container');
    const refImg = document.getElementById('reference-sign-img');
    if (refContainer && refImg) {
        refContainer.style.display = 'block';
        refImg.src = `/static/quiz_media/lesson2/${target.toLowerCase()}.jpg`;
        refImg.onerror = () => { refContainer.style.display = 'none'; }; // Hide if image missing
    }
}

function startPractice(category) {
    const pool = practiceConfig[category];
    if (!pool) return;

    let sessionItems = [];
    for (let i = 0; i < 10; i++) {
        const item = pool[Math.floor(Math.random() * pool.length)];
        sessionItems.push(item);
    }

    practiceSession = {
        active: true,
        category: category,
        items: sessionItems,
        currentIndex: 0,
        score: 0
    };

    if (window.CURRENT_PAGE_TYPE === 'practice') {
        // Transition UI on standalone page
        const categories = document.getElementById('practice-categories');
        const activeUI = document.getElementById('active-session-ui');
        const placeholder = document.getElementById('practice-placeholder');
        const cameraContainer = document.getElementById('practice-camera-container');

        if (categories) categories.style.display = 'none';
        if (activeUI) activeUI.style.display = 'block';
        if (placeholder) placeholder.style.display = 'none';
        if (cameraContainer) cameraContainer.style.display = 'block';

        // Update Category Header Info
        const catName = document.getElementById('active-cat-name');
        const catIconBox = document.getElementById('active-cat-icon-box');
        if (catName) catName.innerText = category.charAt(0).toUpperCase() + category.slice(1);
        if (catIconBox) {
            if (category === 'alphabets') {
                catIconBox.innerHTML = '<i class="fas fa-font"></i>';
                catIconBox.style.background = '#fff5f5';
                catIconBox.style.color = '#FF6B6B';
            } else {
                catIconBox.innerHTML = '<i class="fas fa-sort-numeric-up"></i>';
                catIconBox.style.background = '#f0fff4';
                catIconBox.style.color = '#48BB78';
            }
        }
    }

    updatePracticeUI();
    openCameraModal();
}

function updatePracticeUI() {
    // Determine the current item and progress info
    let currentItem = "";
    let total = 0;
    let currentIndexText = "";
    let progressPercent = 0;

    if (practiceSession && practiceSession.active && practiceSession.items && practiceSession.items.length > 0) {
        currentItem = practiceSession.items[practiceSession.currentIndex] || "";
        total = practiceSession.items.length;
        currentIndexText = `${practiceSession.currentIndex + 1}/${total}`;
        progressPercent = ((practiceSession.currentIndex + 1) / total) * 100;
    } else {
        // Fallback for Single Letter Practice (Standalone Page buttons)
        currentItem = gameState.targetLetter ? gameState.targetLetter.toUpperCase() : "";
        total = 1;
        currentIndexText = "1/1";
        progressPercent = 100;
    }

    // Handle Dashboard Modal UI
    const prompt = document.getElementById('camera-prompt');
    if (prompt) {
        prompt.innerHTML = `
            <strong>${practiceSession.currentIndex + 1}/${total}</strong><br>
            Please sign: <span style="font-size: 1.5em; color: var(--accent-blue); display:block; margin: 10px 0;">
            ${currentItem}
            </span>
            <small>Using <em>${currentModelName || 'Loading...'}</em> (Real Time)</small>
        `;
    }

    // Handle Standalone Practice Page UI
    const targetWordEl = document.getElementById('target-word');
    const progressTextEl = document.getElementById('practice-progress-text');
    const progressBarEl = document.getElementById('practice-session-bar');
    if (targetWordEl) targetWordEl.innerText = currentItem;
    if (progressTextEl && practiceSession.active) {
        progressTextEl.innerText = currentIndexText;
    } else if (progressTextEl) {
        progressTextEl.innerText = ""; // Hide progress text for single practice
    }
    if (progressBarEl && practiceSession.active) {
        progressBarEl.style.width = `${progressPercent}%`;
    } else if (progressBarEl) {
        progressBarEl.style.width = "0%"; // Keep bar empty or hide it
    }

    // Update Reference Image for Randomized Sessions
    const refContainer = document.getElementById('reference-sign-container');
    const refImg = document.getElementById('reference-sign-img');
    if (refContainer && refImg && currentItem) {
        refContainer.style.display = 'block';
        refImg.src = `/static/quiz_media/lesson2/${currentItem.toLowerCase()}.jpg`;
        refImg.onerror = () => { refContainer.style.display = 'none'; };
    } else if (refContainer) {
        refContainer.style.display = 'none';
    }

    // Sync target letter for AI detection
    gameState.targetLetter = currentItem;
}

// ... (Quiz & Dashboard Logic same as before) ...

function updateQuizItems() {
    const utilsBar = document.getElementById('quiz-utils-bar'); // Utilities bar
    if (!utilsBar) return;

    // Remove existing shop item buttons in quiz
    utilsBar.querySelectorAll('.quiz-item-btn').forEach(b => b.remove());

    // Add Timer Freeze button if Mastery Lesson and have count
    const isMastery = (window.CURRENT_TOPIC_ID === 1 && window.CURRENT_LESSON_ID === 8) || 
                      (window.CURRENT_TOPIC_ID === 2 && window.CURRENT_LESSON_ID === 9) || 
                      (window.CURRENT_TOPIC_ID === 3 && window.CURRENT_LESSON_ID === 24);
    
    if (isMastery && gameState.timerFreezeCount > 0) {
        const powerupContainer = document.getElementById('quiz-powerup-container');
        if (powerupContainer) {
            powerupContainer.innerHTML = ''; // Clear existing buttons
            const freezeBtn = document.createElement('button');
            freezeBtn.className = 'power-up-btn';
            freezeBtn.onclick = useTimerFreeze;
            freezeBtn.innerHTML = `<i class="fas fa-snowflake"></i> Power Up: Freeze (${gameState.timerFreezeCount})`;
            powerupContainer.appendChild(freezeBtn);
        }
    }
}

function updateQuizUI() {
    const currentQ = gameState.questions[gameState.currentQuestionIndex];
    const progress = ((gameState.currentQuestionIndex + 1) / gameState.totalQuestions) * 100;
    document.getElementById('quiz-progress-bar').style.width = `${progress}%`;
    document.getElementById('question-counter').innerText = gameState.currentQuestionIndex + 1;
    const totalQEl = document.getElementById('total-questions');
    if (totalQEl) totalQEl.innerText = gameState.totalQuestions;
    document.getElementById('heart-count').innerText = gameState.hearts;

    // Update item usage buttons/indicators in Quiz
    updateQuizItems();

    // Update Question
    const quizContent = document.querySelector('.modal-content h3');
    if (quizContent) quizContent.innerText = currentQ.text;

    // Update Options
    const optionsContainer = document.querySelector('.quiz-options');
    optionsContainer.innerHTML = ''; // Clear previous options

    // Reset sequence for new questions
    if (!gameState.selectedSequence) gameState.selectedSequence = [];
    gameState.selectedSequence = [];

    // Check if we should use a 4-column layout
    let useFourColumns = false;
    if (!currentQ.media_url && currentQ.options.length === 4) {
        // If it's a visual option puzzle, make it 4 in a row
        useFourColumns = currentQ.options.some(opt => typeof opt !== 'string' && opt.media_url);
    }
    optionsContainer.style.gridTemplateColumns = useFourColumns ? 'repeat(4, 1fr)' : '';

    currentQ.options.forEach((optObj, idx) => {
        // optObj can be a string (from generic quiz) or an object {text, media_url}
        let text = typeof optObj === 'string' ? optObj : optObj.text;
        let media_url = typeof optObj === 'string' ? null : optObj.media_url;

        const btn = document.createElement('button');
        btn.className = 'quiz-btn';
        btn.dataset.index = idx;

        let innerHTML = '';
        if (media_url && !currentQ.media_url) {
            btn.style.display = 'flex';
            btn.style.flexDirection = 'column';
            btn.style.alignItems = 'center';
            btn.style.justifyContent = 'center';
            btn.style.gap = '15px';
            innerHTML += `<img src="${media_url}" style="width: 140px; height: 140px; object-fit: contain; border-radius: 8px;">`;
            if (!currentQ.hide_option_text) {
                innerHTML += `<span style="font-size: 1rem; text-align: center;">${text}</span>`;
            }
        } else {
            innerHTML = text;
        }

        btn.innerHTML = innerHTML;

        if (currentQ.type === 'Sequence') {
            btn.onclick = () => handleSequenceClick(btn, text);
        } else {
            btn.onclick = () => checkAnswer(btn, text);
        }
        optionsContainer.appendChild(btn);
    });

    // Add Confirm/Clear Buttons for Sequence mode
    if (currentQ.type === 'Sequence') {
        const confirmBtn = document.createElement('button');
        confirmBtn.id = 'confirm-sequence-btn';
        confirmBtn.className = 'confirm-sequence-btn';
        confirmBtn.innerText = 'Confirm Selection';
        confirmBtn.disabled = true;
        confirmBtn.onclick = () => checkSequenceAnswer();
        optionsContainer.appendChild(confirmBtn);

        const clearBtn = document.createElement('button');
        clearBtn.className = 'clear-sequence-btn';
        clearBtn.innerHTML = '<i class="fas fa-undo"></i> Clear Selection';
        clearBtn.onclick = () => resetSequence();
        optionsContainer.appendChild(clearBtn);
    }

    // Update Image/Video
    const imageContainer = document.querySelector('.quiz-image');
    imageContainer.innerHTML = ''; // Clear existing

    if (currentQ.media_url) {
        imageContainer.style.display = 'flex';
        if (currentQ.media_type === 'video') {
            const video = document.createElement('video');
            video.src = currentQ.media_url;
            video.controls = true;
            video.autoplay = true;
            video.loop = true;
            video.style.width = '100%';
            video.style.height = '100%';
            video.style.borderRadius = 'var(--radius-md)';
            imageContainer.appendChild(video);
        } else {
            const img = document.createElement('img');
            img.src = currentQ.media_url;
            img.style.width = '100%';
            img.style.height = '100%';
            img.style.objectFit = 'contain'; // or cover
            img.style.borderRadius = 'var(--radius-md)';
            imageContainer.appendChild(img);
        }
        // Remove icon styling if replacing with media, or keep as container
        imageContainer.style.background = 'transparent';
        imageContainer.style.boxShadow = 'none';
    } else {
        // Remove the image entirely if there is suppose no image for context questions
        imageContainer.style.display = 'none';
    }

    updateDashboardStats();
}

function updateDashboardStats() {
    const heartEl = document.getElementById('main-heart-count');
    const diamondEl = document.getElementById('main-diamond-count');
    const streakEl = document.getElementById('main-streak-count');
    const levelEl = document.getElementById('user-level-display');
    const xpFill = document.getElementById('sidebar-xp-fill');
    const xpText = document.getElementById('sidebar-xp-text');

    if (heartEl) {
        let text = gameState.hearts.toString();
        if (gameState.hearts < 5 && gameState.nextHeartIn > 0) {
            let h = Math.floor(gameState.nextHeartIn / 3600);
            let m = Math.floor((gameState.nextHeartIn % 3600) / 60);
            let s = Math.floor(gameState.nextHeartIn % 60);
            let timeStr = `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
            text += ` <span style="font-size: 0.6em; color: var(--text-secondary); margin-left: 5px;">(${timeStr})</span>`;
        }
        heartEl.innerHTML = text;
    }
    if (diamondEl) {
        diamondEl.innerText = gameState.diamonds;
        const shopDiamondEl = document.getElementById('shop-diamond-count');
        if (shopDiamondEl) shopDiamondEl.innerText = gameState.diamonds;
    }
    if (streakEl) streakEl.innerText = gameState.streak;
    if (levelEl) levelEl.innerText = `Level ${gameState.level}`;

    // XP Bar Logic (Dynamic Scaling)
    if (xpFill && xpText) {
        let L = gameState.level || 1;
        const currentTotalXp = gameState.xp || 0;

        if (L >= 100) {
            xpFill.style.width = '100%';
            xpText.innerText = "Level 100 - Max Level Reach!";
        } else {
            // Formula: XP = 25 * (L-1) * (L+2)
            const xpAtLStart = 25 * (L - 1) * (L + 2);
            
            // Goal XP at end of level L (which is xpAtLStart for level L+1)
            const goalXp = 25 * L * (L + 3);
            
            // Delta XP needed GROW from current level L to L+1
            const xpForNextGoal = goalXp - xpAtLStart; 

            // Current progress within the current level's bracket
            const progressInLevel = Math.max(0, currentTotalXp - xpAtLStart);
            const percentage = Math.min(100, (progressInLevel / xpForNextGoal) * 100);

            xpFill.style.width = `${percentage}%`;
            xpText.innerText = `${Math.floor(progressInLevel)} / ${Math.floor(xpForNextGoal)} XP to level up`;
        }
    }
}


function updateInventoryUI() {
    const headerContainer = document.getElementById('header-active-items');
    const divider = document.getElementById('header-items-divider');
    if (!headerContainer) return;

    headerContainer.innerHTML = '';

    const hasItems = gameState.xpBoostActive || gameState.shieldCount > 0 || gameState.timerFreezeCount > 0;
    if (divider) divider.style.display = hasItems ? 'block' : 'none';

    if (!hasItems) return;

    // 1. Double XP Boost
    if (gameState.xpBoostActive) {
        const item = document.createElement('div');
        item.style = "display: flex; align-items: center; gap: 5px; background: #f3f0ff; padding: 4px 10px; border-radius: 12px; font-size: 0.8em; font-weight: 700; color: #7c3aed; border: 1px solid #e9d5ff;";
        item.innerHTML = `<i class="fas fa-rocket"></i> <span id="header-xp-timer">...</span>`;
        headerContainer.appendChild(item);
        startXPBoostCountdown();
    }

    // 2. Shields
    if (gameState.shieldCount > 0) {
        const item = document.createElement('div');
        item.style = "display: flex; align-items: center; gap: 5px; background: #fffbeb; padding: 4px 10px; border-radius: 12px; font-size: 0.8em; font-weight: 700; color: #b45309; border: 1px solid #fef3c7;";
        item.innerHTML = `<i class="fas fa-shield-alt"></i> ${gameState.shieldCount}`;
        headerContainer.appendChild(item);
    }

    // 3. Timer Freezes
    if (gameState.timerFreezeCount > 0) {
        const item = document.createElement('div');
        item.style = "display: flex; align-items: center; gap: 5px; background: #f0f9ff; padding: 4px 10px; border-radius: 12px; font-size: 0.8em; font-weight: 700; color: #0369a1; border: 1px solid #e0f2fe;";
        item.innerHTML = `<i class="fas fa-snowflake"></i> ${gameState.timerFreezeCount}`;
        headerContainer.appendChild(item);
    }
}

let xpBoostTimerInterval = null;
function startXPBoostCountdown() {
    if (xpBoostTimerInterval) clearInterval(xpBoostTimerInterval);
    
    const timerDisplay = document.getElementById('header-xp-timer');
    if (!timerDisplay || !gameState.xpBoostExpiry) return;

    function update() {
        const now = new Date();
        const expiry = new Date(gameState.xpBoostExpiry);
        const diff = expiry - now;

        if (diff <= 0) {
            gameState.xpBoostActive = false;
            clearInterval(xpBoostTimerInterval);
            updateInventoryUI();
            return;
        }

        const m = Math.floor(diff / 1000 / 60);
        const s = Math.floor((diff / 1000) % 60);
        timerDisplay.innerText = `${m}:${s.toString().padStart(2, '0')}`;
    }

    update();
    xpBoostTimerInterval = setInterval(update, 1000);
}

function updateShopUI() {
    const shopContainer = document.getElementById('shop-items-grid');
    if (!shopContainer) return;

    // Update Streak Repair card visibility/availability
    // If streak > 0, we could disable it or mark as "Not Needed"
    const streakRepairCard = shopContainer.querySelector('[data-item="streak_repair"]');
    if (streakRepairCard) {
        const btn = streakRepairCard.querySelector('.buy-btn');
        if (gameState.streak > 0) {
            // Optional: Mark as not needed
        }
    }
}

function buyItem(itemId) {
    const btn = event ? event.target : null;
    if (btn) {
        btn.disabled = true;
        btn.textContent = 'Buying...';
    }

    fetch('/api/shop/purchase', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ item_id: itemId })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            showFloatMessage(data.message, 'success');
            updateGameState(data);
        } else {
            showFloatMessage(data.message, 'danger');
        }
    })
    .catch(err => {
        console.error("Purchase error:", err);
        showFloatMessage("Failed to connect to shop.", "danger");
    })
    .finally(() => {
        if (btn) {
            btn.disabled = false;
            btn.textContent = 'Buy Now';
        }
    });
}

// Audio Output function
function playSound(type) {
    if (localStorage.getItem('saybim_sound') === 'false') return;
    try {
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioCtx.createOscillator();
        const gainNode = audioCtx.createGain();

        oscillator.connect(gainNode);
        gainNode.connect(audioCtx.destination);

        if (type === 'correct') {
            oscillator.type = 'sine';
            oscillator.frequency.setValueAtTime(440, audioCtx.currentTime); // A4
            oscillator.frequency.setValueAtTime(554.37, audioCtx.currentTime + 0.1); // C#5
            gainNode.gain.setValueAtTime(1, audioCtx.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.3);
            oscillator.start(audioCtx.currentTime);
            oscillator.stop(audioCtx.currentTime + 0.3);
        } else if (type === 'incorrect') {
            oscillator.type = 'sawtooth';
            oscillator.frequency.setValueAtTime(300, audioCtx.currentTime);
            oscillator.frequency.setValueAtTime(250, audioCtx.currentTime + 0.1);
            gainNode.gain.setValueAtTime(1, audioCtx.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.4);
            oscillator.start(audioCtx.currentTime);
            oscillator.stop(audioCtx.currentTime + 0.4);
        }
    } catch (e) { console.error('Audio failed:', e); }
}

function checkAnswer(btnElement, answerValue) {
    const currentQ = gameState.questions[gameState.currentQuestionIndex];
    // answerValue is now the string selected by user
    const isCorrect = (answerValue === currentQ.correct_option);

    const allBtns = document.querySelectorAll('.quiz-options .quiz-btn');
    allBtns.forEach(b => {
        b.disabled = true; // Disable all after selection
        if (b.innerText === currentQ.correct_option) {
            b.classList.add('correct'); // Highlight answer
        }
    });

    if (isCorrect) {
        btnElement.classList.add('correct');
        // Submit Correct
        fetch('/api/quiz/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ correct: true })
        }).then(res => res.json()).then(data => {
            gameState.sessionXp += (data.xp_gain || 10);
            updateGameState(data);
            playSound('correct');
            showQuizFeedback(true, answerValue, currentQ.correct_option, data.message);
        });
    } else {
        btnElement.classList.add('incorrect');
        // Submit Incorrect
        fetch('/api/quiz/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ correct: false })
        }).then(res => res.json()).then(data => {
            updateGameState(data);
            playSound('incorrect');
            showQuizFeedback(false, answerValue, currentQ.correct_option);
        });
    }
}

function nextQuestion() {
    gameState.currentQuestionIndex++;
    if (gameState.currentQuestionIndex >= gameState.totalQuestions) {
        pauseQuizTimer();
        let fullyCompleted = true; // One completion is now enough for Topic lessons

        fetch('/api/lesson/complete', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                fully_completed: fullyCompleted,
                topic_id: window.CURRENT_TOPIC_ID || 1,
                lesson_id: window.CURRENT_LESSON_ID || 1
            })
        }).then(res => res.json()).then(data => {
            if (data.success) {
                const userData = data.user || data;
                updateGameState(data);

                if (window.CURRENT_PAGE_TYPE === 'quiz') {
                    showFloatMessage(data.message || "Lesson Completed! +50 XP", 'success', () => {
                        // Process any earned badges AFTER the toast is dismissed
                        if (badgeCelebrationQueue.length > 0) {
                            processBadgeQueue(() => {
                                window.location.href = '/';
                            });
                        } else {
                            window.location.href = '/';
                        }
                    });
                } else {
                    showFloatMessage(data.message || "Lesson Completed! +50 XP", 'success', () => {
                        processBadgeQueue();
                    });
                    renderLessonCards();
                    closeModal('quiz-modal');
                    gameState.currentQuestionIndex = 0;
                }
            }
        });
    } else {
        const allBtns = document.querySelectorAll('.quiz-options .quiz-btn');
        allBtns.forEach(b => b.classList.remove('correct', 'incorrect'));
        updateQuizUI();
    }
}

function showGameOver() {
    pauseQuizTimer();
    const gamemodal = document.getElementById('game-over-modal');
    if (gamemodal.classList.contains('modal-overlay')) {
        gamemodal.classList.add('active');
        if (window.CURRENT_PAGE_TYPE === 'quiz') {
            gamemodal.style.display = 'flex';
        }
    }
}

function refillHearts() {
    fetch('/api/user/refill_hearts', { method: 'POST' })
        .then(res => {
            if (res.ok) return res.json();
            throw new Error("Not enough diamonds");
        })
        .then(data => {
            if (data.success) {
                updateGameState(data);

                const gameOverModal = document.getElementById('game-over-modal');
                if (gameOverModal) {
                    gameOverModal.classList.remove('active');
                    if (window.CURRENT_PAGE_TYPE === 'quiz') gameOverModal.style.display = 'none';
                }

                if (gameState.currentQuestionIndex < gameState.totalQuestions) {
                    if (window.CURRENT_PAGE_TYPE !== 'quiz') {
                        document.getElementById('quiz-modal').classList.add('active');
                    } else if (window.CURRENT_LESSON_ID === 8 && currentRemainingTime > 0) {
                        startQuizTimer(); // Resume the timer
                    }
                    updateQuizUI();
                }
            }
        })
        .catch(err => {
            showFloatMessage(err.message);
        });
}

function quitLesson() {
    closeModal('game-over-modal');
}

function handleSequenceClick(btn, text) {
    if (btn.classList.contains('selected')) return;

    gameState.selectedSequence.push(text);
    btn.classList.add('selected');

    // Add number badge
    const badge = document.createElement('div');
    badge.className = 'sequence-badge';
    badge.innerText = gameState.selectedSequence.length;
    btn.appendChild(badge);

    const currentQ = gameState.questions[gameState.currentQuestionIndex];

    // Update Confirm Button
    const confirmBtn = document.getElementById('confirm-sequence-btn');
    if (confirmBtn) {
        if (gameState.selectedSequence.length > 0) {
            confirmBtn.classList.add('active');
        }
        if (gameState.selectedSequence.length === currentQ.correct_sequence.length) {
            confirmBtn.disabled = false;
        } else {
            confirmBtn.disabled = true;
        }
    }
}

function resetSequence() {
    gameState.selectedSequence = [];
    const btns = document.querySelectorAll('.quiz-options .quiz-btn');
    btns.forEach(btn => {
        btn.classList.remove('selected', 'correct', 'incorrect');
        const badge = btn.querySelector('.sequence-badge');
        if (badge) badge.remove();
        btn.disabled = false;
    });
}

function checkSequenceAnswer() {
    const currentQ = gameState.questions[gameState.currentQuestionIndex];
    const isCorrect = JSON.stringify(gameState.selectedSequence) === JSON.stringify(currentQ.correct_sequence);

    const allBtns = document.querySelectorAll('.quiz-options .quiz-btn');
    allBtns.forEach(b => b.disabled = true);

    const confirmBtn = document.getElementById('confirm-sequence-btn');
    if (confirmBtn) confirmBtn.disabled = true;

    if (isCorrect) {
        const selectedBtns = document.querySelectorAll('.quiz-options .quiz-btn.selected');
        selectedBtns.forEach(b => b.classList.add('correct'));

        fetch('/api/quiz/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ correct: true })
        }).then(res => res.json()).then(data => {
            gameState.sessionXp += (data.xp_gain || 10);
            updateGameState(data);
            playSound('correct');
            showQuizFeedback(true, gameState.selectedSequence.join(' '), currentQ.correct_sequence.join(' '), data.message);
        });
    } else {
        const selectedBtns = document.querySelectorAll('.quiz-options .quiz-btn.selected');
        selectedBtns.forEach(b => b.classList.add('incorrect'));

        fetch('/api/quiz/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ correct: false })
        }).then(res => res.json()).then(data => {
            updateGameState(data);
            playSound('incorrect');
            showQuizFeedback(false, gameState.selectedSequence.join(' '), currentQ.correct_sequence.join(' '));
        });
    }
}

function showQuizFeedback(isCorrect, userAnswer, correctAnswer, xpMessage = "") {
    pauseQuizTimer();
    const overlay = document.getElementById('quiz-feedback-overlay');
    overlay.className = `feedback-overlay ${isCorrect ? 'correct' : 'incorrect'}`;

    let html = `
        <div class="feedback-title">${isCorrect ? '<i class="fas fa-check-circle"></i> Brilliant!' : '<i class="fas fa-times-circle"></i> Not Quite...'}</div>
        <div class="feedback-details">
    `;

    if (!isCorrect) {
        html += `<div class="feedback-word">You chose: <span>${userAnswer}</span></div>`;
        html += `<div class="feedback-word">Correct answer: <span>${correctAnswer}</span></div>`;
    } else if (xpMessage) {
        html += `<div class="feedback-word" style="color: #48bb78; font-weight: 800; font-size: 1.2em;">${xpMessage}</div>`;
    }

    html += `</div>
        <button class="feedback-ok-btn" id="feedback-ok-btn">OK</button>
    `;

    overlay.innerHTML = html;
    overlay.style.display = 'flex';

    document.getElementById('feedback-ok-btn').onclick = () => {
        overlay.style.display = 'none';

        if (!isCorrect && gameState.hearts <= 0) {
            if (window.CURRENT_PAGE_TYPE !== 'quiz') {
                closeModal('quiz-modal');
            }
            showGameOver();
        } else {
            // Process any badges earned from the specific question (uncommon but possible)
            if (isCorrect && badgeCelebrationQueue.length > 0) {
                processBadgeQueue(() => {
                    nextQuestion();
                    if ((gameState.currentTopicId === 1 && gameState.currentLessonId === 8) ||
                        (gameState.currentTopicId === 2 && gameState.currentLessonId === 9) ||
                        (gameState.currentTopicId === 3 && gameState.currentLessonId === 24)) {
                        startQuizTimer();
                    }
                });
            } else {
                nextQuestion();
                // Only resume timer for Mastery Review lessons
                if ((gameState.currentTopicId === 1 && gameState.currentLessonId === 8) || (gameState.currentTopicId === 2 && gameState.currentLessonId === 9) || (gameState.currentTopicId === 3 && gameState.currentLessonId === 24)) {
                    startQuizTimer();
                }
            }
        }
    };
}

function toggleHint() {
    const hint = document.getElementById('hint-popup');

    if (gameState.questions && gameState.questions.length > 0) {
        const currentQ = gameState.questions[gameState.currentQuestionIndex];
        const hintText = hint.querySelector('p');
        if (hintText && currentQ && currentQ.hint) {
            hintText.innerText = currentQ.hint;
        }
    }

    hint.style.display = (hint.style.display === 'none' || hint.style.display === '') ? 'block' : 'none';
}

window.onclick = function (event) {
    if (event.target == document.getElementById('quiz-modal')) closeModal('quiz-modal');
    if (event.target == document.getElementById('camera-modal')) closeModal('camera-modal');
    if (event.target == document.getElementById('feedback-modal')) {
        closeModal('feedback-modal');
        document.getElementById('feedback-modal').style.display = 'none';
    }
}

// Settings Logic
function submitFeedback() {
    const feedbackText = document.getElementById('feedback-text');
    const text = feedbackText.value.trim();

    if (text === '') {
        showFloatMessage("Please enter some feedback first!", "warning");
        return;
    }

    showFloatMessage("Sending feedback...", "info");

    fetch('/api/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ feedback: text })
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                showFloatMessage("Thank you for your feedback! Sent to developer telegram bot.");
                feedbackText.value = '';
                closeModal('feedback-modal');
                document.getElementById('feedback-modal').style.display = 'none';
            } else {
                showFloatMessage(data.message || "Failed to send feedback.", "danger");
            }
        })
        .catch(err => {
            console.error("Feedback error:", err);
            showFloatMessage("Error connecting to feedback server.", "danger");
        });
}

function openFeedbackModal() {
    const modal = document.getElementById('feedback-modal');
    modal.classList.add('active');
    modal.style.display = 'flex';
}

function showSubMenu(menu) {
    document.getElementById('settings-main-menu').style.display = 'none';
    const prefBlock = document.getElementById('preferences-menu');
    const profBlock = document.getElementById('profile-menu');
    if (prefBlock) prefBlock.style.display = 'none';
    if (profBlock) profBlock.style.display = 'none';

    if (menu === 'preferences') {
        if (prefBlock) prefBlock.style.display = 'block';
    } else if (menu === 'profile') {
        if (profBlock) profBlock.style.display = 'block';
        renderBadgeEquipUI();
    } else {
        document.getElementById('settings-main-menu').style.display = 'block';
    }
}

function renderBadgeEquipUI() {
    const badgeSelect = document.getElementById('badge-select');
    const status = document.getElementById('badge-equip-status');
    if (!badgeSelect || !status) return;

    const badges = Array.isArray(gameState.badges) ? gameState.badges : [];
    const equipped = gameState.equippedBadge;

    badgeSelect.innerHTML = '<option value="">No badge equipped</option>';
    badges.forEach((badge) => {
        const option = document.createElement('option');
        option.value = badge.key;
        let label = formatBadgeLabel(badge);
        if (badge.is_weekly && badge.expires_at) {
            label += ` (expires in ${formatBadgeExpiry(badge.expires_at)})`;
        }
        option.innerText = label;
        if (equipped && equipped.key === badge.key) {
            option.selected = true;
        }
        badgeSelect.appendChild(option);
    });

    if (!badges.length) {
        status.innerText = 'No badges unlocked yet.';
    } else if (equipped) {
        const expiryText = equipped.is_weekly && equipped.expires_at
            ? ` (expires in ${formatBadgeExpiry(equipped.expires_at)})`
            : '';
        status.innerText = `Currently equipped: ${formatBadgeLabel(equipped)}${expiryText}`;
    } else {
        status.innerText = 'Choose one of your unlocked badges and press Equip.';
    }
}

function equipSelectedBadge() {
    const badgeSelect = document.getElementById('badge-select');
    if (!badgeSelect) return;

    fetch('/api/badges/equip', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ badge_key: badgeSelect.value || '' })
    })
        .then(res => res.json())
        .then(async (data) => {
            if (!data.success) {
                showFloatMessage(data.message || 'Failed to equip badge', 'danger');
                return;
            }

            const userRes = await fetch('/api/user');
            const userData = await userRes.json();
            updateGameState(userData);
            renderBadgeEquipUI();
            showFloatMessage('Badge updated successfully.', 'success');
            fetchLeaderboard();
        })
        .catch((err) => {
            showFloatMessage('Failed to equip badge: ' + err.message, 'danger');
        });
}

const BADGE_DEFS = [
    { key: 'first_practice_camera', name: 'First Camera Practice (1x)', emoji: '📷', description: 'Complete your first practice using the camera.', weekly: false },
    { key: 'topic_1_complete', name: 'Topic 1 Master (Lessons 1-8)', emoji: '📘', description: 'Complete all lessons in Topic 1 (Greetings).', weekly: false },
    { key: 'topic_2_complete', name: 'Topic 2 Master (Lessons 1-9)', emoji: '📙', description: 'Complete all lessons in Topic 2 (Self-Identity).', weekly: false },
    { key: 'topic_3_complete', name: 'Topic 3 Master (Lessons 18-24)', emoji: '👨‍👩‍👧‍👦', description: 'Complete all lessons in Topic 3 (Family & Relationships).', weekly: false },
    { key: 'weekly_top_1', name: 'Weekly Top 1', emoji: '🥇', description: 'Reach Rank 1 on the weekly leaderboard.', weekly: true },
    { key: 'weekly_top_2', name: 'Weekly Top 2', emoji: '🥈', description: 'Reach Rank 2 on the weekly leaderboard.', weekly: true },
    { key: 'weekly_top_3', name: 'Weekly Top 3', emoji: '🥉', description: 'Reach Rank 3 on the weekly leaderboard.', weekly: true }
];


let badgeCelebrationQueue = [];
let isCelebrationModalActive = false;
let currentCelebrationCallback = null;

function queueBadgeCelebration(badgeKey) {
    if (!badgeCelebrationQueue.includes(badgeKey)) {
        badgeCelebrationQueue.push(badgeKey);
    }
}

function processBadgeQueue(callback = null) {
    if (callback) currentCelebrationCallback = callback;
    
    if (badgeCelebrationQueue.length === 0) {
        if (currentCelebrationCallback) {
            const cb = currentCelebrationCallback;
            currentCelebrationCallback = null;
            cb();
        }
        return;
    }

    if (isCelebrationModalActive) return;

    const nextBadgeKey = badgeCelebrationQueue.shift();
    showBadgeCelebration(nextBadgeKey);
}

function showBadgeCelebration(badgeKey) {
    isCelebrationModalActive = true;
    // Clean key if it's a full record string
    let searchKey = badgeKey;
    if (badgeKey.startsWith('badge::')) {
        const parts = badgeKey.split('::');
        searchKey = parts[1];
    }

    const badge = BADGE_DEFS.find(b => b.key === searchKey || b.key === badgeKey);
    if (!badge) {
        isCelebrationModalActive = false;
        processBadgeQueue();
        return;
    }

    const modal = document.getElementById('badge-celebration-modal');
    const emojiEl = document.getElementById('celebration-emoji');
    const nameEl = document.getElementById('celebration-badge-name');
    const descEl = document.getElementById('celebration-badge-desc');
    const equipBtn = document.getElementById('equip-now-btn');

    if (!modal || !emojiEl || !nameEl || !descEl || !equipBtn) {
        isCelebrationModalActive = false;
        processBadgeQueue();
        return;
    }

    emojiEl.innerText = badge.emoji;
    nameEl.innerText = badge.name;
    descEl.innerText = badge.description;

    equipBtn.onclick = () => {
        equipBadgeByKey(badge.key);
        closeModal('badge-celebration-modal');
    };
    
    modal.classList.add('active');
    modal.style.display = 'flex';
    createConfetti();
    playSound('correct');
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
        // Wait for transition
        setTimeout(() => {
            modal.style.display = 'none';
            if (modalId === 'badge-celebration-modal') {
                isCelebrationModalActive = false;
                processBadgeQueue();
            }
        }, 300);
    }
}

function createConfetti() {
    const container = document.getElementById('confetti-container');
    if (!container) return;
    
    container.innerHTML = '';
    const colors = ['#667eea', '#764ba2', '#ff9a9e', '#fecfef', '#F6E05E', '#68D391'];
    
    for (let i = 0; i < 50; i++) {
        const piece = document.createElement('div');
        piece.className = 'confetti-piece';
        piece.style.left = Math.random() * 100 + '%';
        piece.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        piece.style.setProperty('--fall-duration', (Math.random() * 3 + 2) + 's');
        piece.style.animationDelay = Math.random() * 2 + 's';
        container.appendChild(piece);
    }
}

function renderBadgeSection() {
    const gallery = document.getElementById('badges-gallery');
    if (!gallery) return;

    gallery.innerHTML = '';
    
    // Use global BADGE_DEFS
    const allBadges = BADGE_DEFS;

    const ownedBadges = Array.isArray(gameState.badges) ? gameState.badges : [];
    const equipped = gameState.equippedBadge;

    allBadges.forEach(badge => {
        const userBadge = ownedBadges.find(b => b.key === badge.key);
        const isOwned = !!userBadge;
        const isEquipped = equipped && equipped.key === badge.key;

        const card = document.createElement('div');
        card.className = `lesson-card ${!isOwned ? 'locked' : ''}`;
        card.style.display = 'flex';
        card.style.flexDirection = 'column';
        card.style.alignItems = 'center';
        card.style.textAlign = 'center';
        card.style.padding = '25px';
        card.style.minHeight = '220px';

        let footerHtml = '';
        if (isOwned) {
            if (isEquipped) {
                footerHtml = `<div style="margin-top:auto; color:var(--accent-green); font-weight:800; font-size:0.9em;"><i class="fas fa-check-circle"></i> Equipped</div>`;
            } else {
                footerHtml = `<button onclick="equipBadgeByKey('${badge.key}')" class="buy-btn" style="margin-top:auto; width:100%; border-radius:12px; padding:8px;">Equip</button>`;
            }
        } else {
            footerHtml = `<div style="margin-top:auto; color:var(--text-secondary); font-size:0.85em; font-weight:700;"><i class="fas fa-lock"></i> Locked</div>`;
        }

        let expiryHtml = '';
        if (userBadge && userBadge.is_weekly && userBadge.expires_at) {
            expiryHtml = `<div style="font-size:0.7em; color:var(--accent-red); margin-top:5px;">Expires: ${formatBadgeExpiry(userBadge.expires_at)}</div>`;
        }

        card.innerHTML = `
            <div style="font-size: 3.5rem; margin-bottom: 15px; filter: ${isOwned ? 'none' : 'grayscale(1) opacity(0.4)'};">${badge.emoji}</div>
            <div style="font-weight: 800; font-size: 1.1rem; color: ${isOwned ? 'var(--text-primary)' : 'var(--text-secondary)'};">${badge.name}</div>
            <div style="font-size: 0.8em; color: var(--text-secondary); margin-top: 5px; line-height: 1.4;">${badge.description}</div>
            ${expiryHtml}
            ${footerHtml}
        `;
        gallery.appendChild(card);
    });
}

async function equipBadgeByKey(badgeKey) {
    try {
        const res = await fetch('/api/badges/equip', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ badge_key: badgeKey })
        });
        const data = await res.json();

        if (data.success) {
            showFloatMessage("Badge equipped successfully!", "success");
            // Refresh user data to sync across UI
            const userRes = await fetch('/api/user');
            const userData = await userRes.json();
            updateGameState(userData);
            renderBadgeSection(); // Re-render gallery
            fetchLeaderboard(); // Sync leaderboard if visible
        } else {
            showFloatMessage(data.message || "Failed to equip badge.", "danger");
        }
    } catch (err) {
        showFloatMessage("Error equipping badge: " + err.message, "danger");
    }
}

function previewAvatar(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function (e) {
            const preview = document.getElementById('profile-avatar-preview');
            preview.innerHTML = `<img src="${e.target.result}" style="width: 100%; height: 100%; object-fit: cover;">`;
        }
        reader.readAsDataURL(input.files[0]);
    }
}

function updateProfile(e) {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);

    fetch('/api/user/profile', {
        method: 'POST',
        body: formData
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                showFloatMessage(data.message);
                // Update UI elements if present
                const nameDisplay = document.getElementById('user-name-display');
                if (nameDisplay) nameDisplay.innerText = data.user.username;

                if (data.user.avatar) {
                    const sidebarAvatar = document.getElementById('sidebar-avatar');
                    if (sidebarAvatar) {
                        sidebarAvatar.style.background = 'transparent';
                        sidebarAvatar.innerHTML = `<img src="${data.user.avatar}" alt="avatar" style="width: 100%; height: 100%; object-fit: cover;">`;
                    }
                } else {
                    const sidebarAvatar = document.getElementById('sidebar-avatar');
                    if (sidebarAvatar) {
                        sidebarAvatar.innerHTML = data.user.username.charAt(0).toUpperCase();
                    }
                }

                form.password.value = ''; // Clear password field for safety
            } else {
                showFloatMessage("Error: " + data.message);
            }
        })
        .catch(err => {
            showFloatMessage("Failed to update profile: " + err.message);
        });
}

function confirmDeleteAccount() {
    showFloatConfirm("Are you absolutely sure you want to delete your account? This action cannot be undone.", () => {
        fetch('/api/user/account', {
            method: 'DELETE'
        })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    showFloatMessage(data.message, 'success', () => {
                        window.location.href = '/login';
                    });
                } else {
                    showFloatMessage("Error: " + data.message);
                }
            });
    });
}


// ==========================================
// TFJS & MediaPipe Implementation
// ==========================================

let loadedModels = {};
let currentModel = null;
let currentModelName = ""; // Added to track current model for display
let currentActions = [];

// Global MediaPipe & Prediction State
let hands = null;
let camera = null;
let sequence = [];
let isPredicting = false;
const ACTIONS_AL = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L'];
const ACTIONS_MZ = ['M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'];
const ACTIONS_UV = ['U', 'V'];
const ACTIONS_NUM = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'];

async function loadModel(target) {
    if (!target) target = 'A';
    target = target.toUpperCase();
    
    let modelPath = '';
    let labels = [];
    
    if (ACTIONS_AL.includes(target)) {
        modelPath = 'static/web_model/model.json';
        labels = ACTIONS_AL;
    } else if (ACTIONS_UV.includes(target)) {
        modelPath = 'static/web_model_uv/model.json';
        labels = ACTIONS_UV;
    } else if (ACTIONS_NUM.includes(target)) {
        modelPath = 'static/web_model_oneten/model.json';
        labels = ACTIONS_NUM;
    } else {
        modelPath = 'static/web_model_mz/model.json';
        labels = ACTIONS_MZ;
    }

    if (loadedModels[modelPath]) {
        currentModel = loadedModels[modelPath];
        currentActions = labels;
        currentModelName = modelPath.split('/').slice(-2, -1)[0] || "Default";
        return currentModel;
    }

    try {
        console.log(`Loading model: ${modelPath} for target ${target}...`);
        const model = await tf.loadLayersModel(modelPath);
        loadedModels[modelPath] = model;
        currentModel = model;
        currentActions = labels;
        currentModelName = modelPath.split('/').slice(-2, -1)[0] || "Default";
        console.log(`Model ${modelPath} Loaded Successfully!`);
        return model;
    } catch (err) {
        console.error(`Failed to load model ${modelPath}:`, err);
        // Fallback to A-L if others fail (since they might not be converted yet)
        if (modelPath !== 'static/web_model/model.json') {
            return loadModel('A');
        }
    }
}

// MediaPipe Setup
function onResults(results) {
    const canvas = document.querySelector('#camera-overlay div'); // Using overlay to draw? 
    // Actually, we should draw on a canvas over the video, but for now we just process data.

    // 1. Extract Keypoints
    const keypoints = extractKeypoints(results);

    // 2. Manage Sequence
    sequence.push(keypoints);
    if (sequence.length > 30) sequence.shift(); // Keep last 30

    // 3. Predict if we have 30 frames
    const modal = document.getElementById('camera-modal');
    const isModalActive = modal && modal.classList.contains('active');
    const isPracticePage = window.CURRENT_PAGE_TYPE === 'practice';

    if (sequence.length === 30 && currentModel && (isModalActive || isPracticePage) && !gameState.detectionPaused) {
        predictGesture();
    }
}

function extractKeypoints(results) {
    // Logic matching utils_hand_only.py
    // Returns flattened array of 126 elements (lh + rh)

    let lh = new Array(21 * 3).fill(0);
    let rh = new Array(21 * 3).fill(0);

    if (results.multiHandLandmarks && results.multiHandedness) {
        for (let i = 0; i < results.multiHandLandmarks.length; i++) {
            const landmarks = results.multiHandLandmarks[i];
            const label = results.multiHandedness[i].label; // "Left" or "Right"

            // Flatten: [x, y, z, x, y, z...]
            const flatLandmarks = [];
            for (let lm of landmarks) {
                flatLandmarks.push(lm.x, lm.y, lm.z);
            }

            if (label === 'Left') {
                lh = flatLandmarks;
            } else {
                rh = flatLandmarks;
            }
        }
    }

    return [...lh, ...rh];
}

async function predictGesture() {
    if (isPredicting) return;
    isPredicting = true;

    try {
        const inputTensor = tf.tensor3d([sequence]); // Shape [1, 30, 126]
        const prediction = currentModel.predict(inputTensor);
        const values = await prediction.data();
        const maxIndex = values.indexOf(Math.max(...values));
        const confidence = values[maxIndex];
        const predictedAction = currentActions[maxIndex];

        inputTensor.dispose();
        prediction.dispose();

        console.log(`Prediction: ${predictedAction} (${confidence.toFixed(2)})`);

        // Update Overlay text to show what is detected (For Freestyle/Testing)
        const prompt = document.getElementById('camera-prompt');
        if (prompt && !practiceSession.active) {
            prompt.innerHTML = `
                <div style="text-align:center;">
                    <strong>Freestyle Testing</strong><br>
                    Detected: <span style="font-size: 2em; color: var(--accent-blue); display:block;">${predictedAction}</span>
                    <small>Confidence: ${(confidence * 100).toFixed(0)}%</small>
                </div>
            `;
        }

        // Enforce target matching if a specific target is set
        // Threshold: 50% for U and V, 70% for others
        const currentTarget = gameState.targetLetter ? gameState.targetLetter.toUpperCase() : null;
        const requiredConfidence = (currentTarget === 'U' || currentTarget === 'V') ? 0.5 : 0.7;

        if (!gameState.detectionPaused && confidence > requiredConfidence) {
            if (gameState.targetLetter) {
                // If we have a target, only trigger success if it matches
                if (predictedAction === gameState.targetLetter) {
                    sequence = [];
                    handleCorrectAnswer(predictedAction);
                }
            } else if (!practiceSession.active) {
                // If we are in Freestyle Testing (no target, no active session),
                // we don't trigger "Correct" automatically to avoid confusing feedback.
                // The overlay already shows the detected letter.
            }
        }

    } catch (err) {
        console.error("Prediction error:", err);
    }

    isPredicting = false;
}

function handleCorrectAnswer(action) {
    if (gameState.detectionPaused) return; // Prevent double trigger
    gameState.detectionPaused = true;

    // Stop Camera immediately for Alphabets Practice (as per user request: "camera off after complete 1 gesture")
    if (window.CURRENT_PAGE_TYPE === 'practice') {
        if (camera) {
            camera.stop();
            const videoElement = document.getElementById('webcam');
            if (videoElement) videoElement.style.opacity = '0.3';

            // Hide camera active indicator
            const indicator = document.getElementById('camera-active-status');
            if (indicator) indicator.style.display = 'none';
        }
    }

    playSound('correct');
    
    // Provide immediate feedback for a snappier experience (message removed as per user request)
    // showFloatMessage("Correct! Well done.", "success");

    // Notify Backend (XP and backend rewards handled here)
    fetch('/api/practice/complete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ word: action })
    }).then(res => res.json()).then(data => {
        updateGameState(data);
        if (data.message && data.message.includes('+')) {
            showFloatMessage(data.message, 'success', () => {
                processBadgeQueue();
            });
        } else {
            processBadgeQueue();
        }
    });

    if (practiceSession.active) {
        practiceSession.currentIndex++;
    }

    if (practiceSession.active && practiceSession.currentIndex >= practiceSession.items.length) {
        showFloatMessage(`Session Complete!`);
        closeModal('camera-modal');
        if (camera) camera.stop();

        if (gameState.currentLessonId) {
            let fullyCompleted = false;
            if (userProgress[gameState.currentLessonId] < 5) {
                userProgress[gameState.currentLessonId]++;
                localStorage.setItem('saybim_lesson_progress_' + gameState.username, JSON.stringify(userProgress));
                if (userProgress[gameState.currentLessonId] === 5) {
                    fullyCompleted = true;
                }
            }

            fetch('/api/lesson/complete', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    fully_completed: fullyCompleted,
                    topic_id: gameState.currentTopicId,
                    lesson_id: gameState.currentLessonId
                })
            })
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        updateGameState(data);
                        
                        // Show total XP gained in the final message
                        const totalGained = gameState.sessionXp + (data.reward_xp || 0);
                        const finalMsg = `Lesson Accomplished! You earned a total of ${totalGained} XP!`;
                        
                        if (fullyCompleted) {
                            showFloatMessage(finalMsg);
                        } else {
                            // If just a step completion
                            showFloatMessage(finalMsg);
                        }

                        if (window.CURRENT_PAGE_TYPE !== 'quiz') {
                            updateDashboardStats();
                            renderLessonCards();
                        }
                    }
                });

            if (window.CURRENT_PAGE_TYPE === 'quiz') {
                showFloatMessage("Practice session complete! Well done.", 'success', () => {
                    window.location.href = '/';
                }, true);
            } else {
                // On practice page, we don't force a reset/redirect
                gameState.detectionPaused = false; 
                if (practiceSession.active) {
                    practiceSession.currentIndex = 0; // Restart session if multi-gesture
                    updatePracticeUI();
                }
            }
        }
    } else {
        updatePracticeUI();
    }
}


// Camera Management
async function openCameraModal(customText) {
    if (localStorage.getItem('saybim_camera') === 'false') {
        showFloatMessage("Camera permission is disabled in Settings! Please turn it on to use this feature.", 'info', () => {
            if (window.CURRENT_PAGE_TYPE === 'practice') {
                window.location.href = '/';
            } else {
                switchSection('practice');
            }
        }, true);
        return;
    }

    const modal = document.getElementById('camera-modal');
    if (modal) modal.classList.add('active');

    // On standalone page, we just need to ensure the camera starts
    if (window.CURRENT_PAGE_TYPE === 'practice') {
        const cameraContainer = document.getElementById('practice-camera-container');
        if (cameraContainer) cameraContainer.style.display = 'block';

        // Show camera active indicator
        const indicator = document.getElementById('camera-active-status');
        if (indicator) indicator.style.display = 'flex';
    }

    if (customText) {
        const prompt = document.getElementById('camera-prompt');
        if (prompt) {
            prompt.style.display = 'block';
            prompt.innerHTML = `
                <div style="text-align:center;">
                    <div style="margin-bottom: 5px; opacity: 0.9;">${customText}</div>
                    <small style="opacity: 0.7; font-size: 0.8em;">AI Model: <em>${currentModelName || 'Loading...'}</em> (Real Time)</small>
                </div>
            `;
        }
    }

    // Load appropriate model for the current target
    await loadModel(gameState.targetLetter || 'A');

    const videoElement = document.getElementById('webcam');

    if (!hands) {
        hands = new Hands({
            locateFile: (file) => {
                return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
            }
        });
        hands.setOptions({
            maxNumHands: 2,
            modelComplexity: 1,
            minDetectionConfidence: 0.5,
            minTrackingConfidence: 0.5
        });
        hands.onResults(onResults);
    }

    if (!camera) {
        camera = new Camera(videoElement, {
            onFrame: async () => {
                await hands.send({ image: videoElement });
            },
            width: 640,
            height: 480
        });
    }

    try {
        await camera.start();
    } catch (err) {
        console.error("Camera failed to start:", err);
        closeModal('camera-modal');
        showFloatMessage("Camera access was denied or failed. Please check your browser permissions.", "danger", () => {
            switchSection('practice');
        }, true);
    }
}

// Override close to stop camera
const oldClose = closeModal;
closeModal = function (modalId) {
    oldClose(modalId);
    if (modalId === 'camera-modal') {
        if (camera) camera.stop();
        sequence = []; // Reset buffer
        if (practiceSession.active) practiceSession.active = false;
        // We keep loadedModels in cache for better performance next time
    }
}

// Placeholder for verification button if needing manual trigger
function verifyGesture() {
    // With real-time model, this button might be redundant or could force a prediction check
    // For now, let's leave it as a "Skip" or manual trigger
    if (practiceSession.active) {
        console.log("Manual verification clicked... relying on auto-prediction for now.");
    }
}

// --- Timer Functions ---

function startQuizTimer() {
    if (quizTimerInterval) clearInterval(quizTimerInterval);
    const container = document.getElementById('quiz-timer-container');
    if (container) container.style.display = 'flex';

    quizTimerInterval = setInterval(() => {
        if (isTimerFrozen) return; // Skip tick if frozen

        if (currentRemainingTime <= 0) {
            pauseQuizTimer();
            showTimeUp();
            return;
        }
        currentRemainingTime--;

        let m = Math.floor(currentRemainingTime / 60);
        let s = currentRemainingTime % 60;
        const display = document.getElementById('quiz-timer-display');
        if (display) display.innerText = `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
    }, 1000);
}

function pauseQuizTimer() {
    if (quizTimerInterval) {
        clearInterval(quizTimerInterval);
        quizTimerInterval = null;
    }
}

function showTimeUp() {
    const modal = document.getElementById('time-up-modal');
    if (modal) {
        modal.classList.add('active');
        modal.style.display = 'flex';
    }
}

function buyTime() {
    // Legacy buyTime now uses the shop refill logic for diamonds
    buyItem('timer_freeze');
    
    // Auto-close time-up if they have gems and just bought more time technically?
    // Actually, let's keep it separate or just use the Shop Item logic.
}

let isTimerFrozen = false;
function useTimerFreeze() {
    if (isTimerFrozen) return;
    if (gameState.timerFreezeCount <= 0) {
        showFloatMessage("You don't have any Timer Freezes!", "warning");
        return;
    }

    fetch('/api/shop/use_timer_freeze', { method: 'POST' })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            isTimerFrozen = true;
            gameState.timerFreezeCount--;
            updateDashboardStats();
            
            const display = document.getElementById('quiz-timer-display');
            const container = document.getElementById('quiz-timer-container');
            if (container) {
                container.style.background = '#e0f2fe';
                container.style.color = 'var(--accent-blue)';
                container.style.border = '2px solid var(--accent-blue)';
            }
            
            showFloatMessage("Time Frozen for 20 seconds!", "success");
            
            setTimeout(() => {
                isTimerFrozen = false;
                if (container) {
                    container.style.background = '#fee2e2';
                    container.style.color = 'var(--accent-red)';
                    container.style.border = 'none';
                }
            }, 20000);
        }
    });
}

function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) {
        sidebar.classList.toggle('collapsed');
    }
}