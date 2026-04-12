
// ... (Previous Game State code remains the same until Camera Logic) ...

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
    detectionPaused: true, // New: Pause AI until button clicked
    targetLetter: null     // New: Track what we are looking for
};

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
    alphabets: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L'],
    // Disable others for now as model only supports A-L
    numbers: [],
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
}

function switchSection(section) {
    const sectionToNavText = {
        'lesson': 'Lesson',
        'practice': 'Practice',
        'setting': 'Setting',
        'challenge': 'Challenge',
        'shop': 'Shop',
        'leaderboard': 'Leaderboard'
    };
    const targetText = sectionToNavText[section];
    const links = document.querySelectorAll('.nav-link');
    links.forEach(l => {
        if (l.innerText.trim() === targetText) {
            l.classList.add('active');
        } else {
            l.classList.remove('active');
        }
    });

    if (window.CURRENT_PAGE_TYPE !== 'quiz' && window.CURRENT_PAGE_TYPE !== 'practice') {

        showSection(section);
        if (section === 'leaderboard') fetchLeaderboard();
        if (section === 'setting') showSubMenu('main');
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
            const text = link.innerText.trim();
            const textToSection = {
                'Lesson': 'lesson',
                'Practice': 'practice',
                'Leaderboard': 'leaderboard',
                'Setting': 'setting',
                'Challenge': 'challenge',
                'Shop': 'shop'
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

    // 3. Load Model (Crucial for Practice and Quizzes)
    loadModel();

    // 4. Handle Practice URL Parameters
    if (window.CURRENT_PAGE_TYPE === 'practice') {
        const urlParams = new URLSearchParams(window.location.search);
        const type = urlParams.get('type') || 'alphabets';
        renderPracticeButtons(type);
        
        // Immediate Number Notice: If numbers, show the overlay right away
        if (type === 'numbers') {
            const maintenanceOverlay = document.getElementById('maintenance-overlay');
            if (maintenanceOverlay) maintenanceOverlay.style.display = 'flex';
        }
    }
});

function updateGameState(userData) {
    if (!userData) return;
    gameState.hearts = userData.hearts;
    gameState.diamonds = userData.diamonds;
    gameState.streak = userData.streak;
    gameState.level = userData.level;
    gameState.xp = userData.xp;
    gameState.nextHeartIn = userData.next_heart_in_seconds || 0;
    gameState.username = userData.username;
    if (userData.topic_progress) {
        gameState.topicProgress = typeof userData.topic_progress === 'string' ? JSON.parse(userData.topic_progress) : userData.topic_progress;
    }
    updateDashboardStats();
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
        if ((gameState.currentTopicId === 1 && gameState.currentLessonId === 8) || 
            (gameState.currentTopicId === 2 && gameState.currentLessonId === 9)) {
            currentRemainingTime = 180;
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
                        </div>
                    </td>
                    <td style="padding: 15px 10px; border-bottom: 1px solid #f0f0f0; text-align: center;">${user.level}</td>
                    <td style="padding: 15px 10px; border-bottom: 1px solid #f0f0f0; text-align: center; color: var(--accent-yellow); font-weight: bold;">${user.xp} XP</td>
                `;
                tbody.appendChild(tr);
            });
        });
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
        ? ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
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
                if (maintenanceOverlay) maintenanceOverlay.style.display = 'flex';
                if (cameraIndicator) cameraIndicator.style.display = 'none';
                
                // Do not open camera
                gameState.targetLetter = null;
                gameState.detectionPaused = true;
                
                // If camera is running, stop it
                if (camera) {
                    camera.stop();
                    const videoElement = document.getElementById('webcam');
                    if (videoElement) videoElement.style.opacity = '0.3';
                }
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
    const currentItem = practiceSession.items[practiceSession.currentIndex];
    const total = practiceSession.items.length;
    const progressPercent = ((practiceSession.currentIndex + 1) / total) * 100;

    // Handle Dashboard Modal UI
    const prompt = document.getElementById('camera-prompt');
    if (prompt) {
        prompt.innerHTML = `
            <strong>${practiceSession.currentIndex + 1}/${total}</strong><br>
            Please sign: <span style="font-size: 1.5em; color: var(--accent-blue); display:block; margin: 10px 0;">
            ${currentItem}
            </span>
            <small>Using <em>A_to_L_model_best.h5</em> (Real Time)</small>
        `;
    }

    // Handle Standalone Practice Page UI
    const targetWordEl = document.getElementById('target-word');
    const progressTextEl = document.getElementById('practice-progress-text');
    const progressBarEl = document.getElementById('practice-session-bar');
    if (targetWordEl) targetWordEl.innerText = currentItem;
    if (progressTextEl) progressTextEl.innerText = `${practiceSession.currentIndex + 1}/${total}`;
    if (progressBarEl) progressBarEl.style.width = `${progressPercent}%`;
}

// ... (Quiz & Dashboard Logic same as before) ...
function updateQuizUI() {
    const currentQ = gameState.questions[gameState.currentQuestionIndex];
    const progress = ((gameState.currentQuestionIndex + 1) / gameState.totalQuestions) * 100;
    document.getElementById('quiz-progress-bar').style.width = `${progress}%`;
    document.getElementById('question-counter').innerText = gameState.currentQuestionIndex + 1;
    const totalQEl = document.getElementById('total-questions');
    if (totalQEl) totalQEl.innerText = gameState.totalQuestions;
    document.getElementById('heart-count').innerText = gameState.hearts;

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
    if (diamondEl) diamondEl.innerText = gameState.diamonds;
    if (streakEl) streakEl.innerText = gameState.streak;
    if (levelEl) levelEl.innerText = `Level ${gameState.level}`;

    // XP Bar Logic (Dynamic Scaling)
    if (xpFill && xpText) {
        const L = gameState.level || 1;
        const currentTotalXp = gameState.xp || 0;
        
        // Cumulative XP required for current level L
        const xpAtLStart = 25 * (L - 1) * (L + 2);
        // XP required to reach next level L+1 from L
        const xpForNextGoal = 100 + (L - 1) * 50;
        
        const progressInLevel = Math.max(0, currentTotalXp - xpAtLStart);
        const percentage = Math.min(100, (progressInLevel / xpForNextGoal) * 100);
        
        xpFill.style.width = `${percentage}%`;
        xpText.innerText = `${Math.floor(progressInLevel)} / ${xpForNextGoal} XP to level up`;
    }
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
    } catch(e) { console.error('Audio failed:', e); }
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
        playSound('correct');
        btnElement.classList.add('correct');
        // Submit Correct
        fetch('/api/quiz/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ correct: true })
        }).then(res => res.json()).then(data => {
            updateGameState(data);
            showQuizFeedback(true, answerValue, currentQ.correct_option);
        });
    } else {
        playSound('incorrect');
        btnElement.classList.add('incorrect');
        // Submit Incorrect
        fetch('/api/quiz/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ correct: false })
        }).then(res => res.json()).then(data => {
            updateGameState(data);
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
                // If it's a full user object under 'user' key (like some endpoints return)
                // or just the user properties directly
                const userData = data.user || data;
                updateGameState(userData);
                
                if (window.CURRENT_PAGE_TYPE === 'quiz') {
                    showFloatMessage(data.message || "Lesson Completed! +50 XP", 'success', () => {
                        window.location.href = '/';
                    });
                } else {
                    showFloatMessage(data.message || "Lesson Completed! +50 XP", 'success');
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
                updateGameState(data.user);
                
                const gameOverModal = document.getElementById('game-over-modal');
                if(gameOverModal) {
                     gameOverModal.classList.remove('active');
                     if(window.CURRENT_PAGE_TYPE === 'quiz') gameOverModal.style.display = 'none';
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
        playSound('correct');
        const selectedBtns = document.querySelectorAll('.quiz-options .quiz-btn.selected');
        selectedBtns.forEach(b => b.classList.add('correct'));
        
        fetch('/api/quiz/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ correct: true })
        }).then(res => res.json()).then(data => {
            updateGameState(data);
            showQuizFeedback(true, gameState.selectedSequence.join(' '), currentQ.correct_sequence.join(' '));
        });
    } else {
        playSound('incorrect');
        const selectedBtns = document.querySelectorAll('.quiz-options .quiz-btn.selected');
        selectedBtns.forEach(b => b.classList.add('incorrect'));
        
        fetch('/api/quiz/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ correct: false })
        }).then(res => res.json()).then(data => {
            updateGameState(data);
            showQuizFeedback(false, gameState.selectedSequence.join(' '), currentQ.correct_sequence.join(' '));
        });
    }
}

function showQuizFeedback(isCorrect, userAnswer, correctAnswer) {
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
            nextQuestion();
            // Only resume timer for Mastery Review lessons
            if ((gameState.currentTopicId === 1 && gameState.currentLessonId === 8) || 
                (gameState.currentTopicId === 2 && gameState.currentLessonId === 9)) {
                startQuizTimer();
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
    } else {
        document.getElementById('settings-main-menu').style.display = 'block';
    }
}

function previewAvatar(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
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

let model = null;
let hands = null;
let camera = null;
let sequence = []; // Buffer for 30 frames
let isPredicting = false;
const ACTIONS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']; // Based on prediction.py

async function loadModel() {
    try {
        console.log("Loading model...");
        // Load the converted TFJS model
        model = await tf.loadLayersModel('static/web_model/model.json');
        console.log("Model Loaded Successfully!");
    } catch (err) {
        console.error("Failed to load model:", err);
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

    if (sequence.length === 30 && model && (isModalActive || isPracticePage) && !gameState.detectionPaused) {
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
        const prediction = model.predict(inputTensor);
        const values = await prediction.data();
        const maxIndex = values.indexOf(Math.max(...values));
        const confidence = values[maxIndex];
        const predictedAction = ACTIONS[maxIndex];

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

        // Check if anything was detected (Requirement of specific alphabet removed)
        if (!gameState.detectionPaused && confidence > 0.7) {
            sequence = [];
            handleCorrectAnswer(predictedAction);
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
    showFloatMessage(`Correct! That is ${action}. +10 XP`);
    
    // Notify Backend
    fetch('/api/practice/complete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ word: action })
    }).then(res => res.json()).then(data => {
        updateGameState(data.user || data);
    });

    practiceSession.currentIndex++;

    if (practiceSession.currentIndex >= practiceSession.items.length) {
        showFloatMessage(`Session Complete! +20 Diamonds`);
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
                body: JSON.stringify({ fully_completed: fullyCompleted })
            })
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        gameState.streak = data.user.streak;
                        gameState.xp = data.user.xp;
                        gameState.diamonds = data.user.diamonds;
                        if (fullyCompleted && data.message) {
                            showFloatMessage(data.message);
                        }
                        if (window.CURRENT_PAGE_TYPE !== 'quiz') {
                            updateDashboardStats();
                            renderLessonCards();
                        }
                    }
                });

            if (window.CURRENT_PAGE_TYPE === 'quiz' || window.CURRENT_PAGE_TYPE === 'practice') {
                showFloatMessage("Practice session complete! Well done.", 'success', () => {
                    window.location.href = '/';
                }, true);
            } else {
                gameState.currentLessonId = null;
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
        if (prompt) prompt.innerText = customText;
    }

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
    fetch('/api/user/buy_time', { method: 'POST' })
        .then(res => {
            if (res.ok) return res.json();
            throw new Error("Not enough diamonds");
        })
        .then(data => {
            if (data.success) {
                gameState.diamonds = data.user.diamonds;
                const modal = document.getElementById('time-up-modal');
                if (modal) {
                    modal.classList.remove('active');
                    modal.style.display = 'none';
                }
                
                currentRemainingTime += 30;
                startQuizTimer();
            }
        })
        .catch(err => showFloatMessage(err.message, 'danger'));
}
