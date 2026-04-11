
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
    username: ''
};

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

// Navigation
let userProgress = {
    1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0
};

function renderLessonCards() {
    for (let i = 1; i <= 6; i++) {
        const card = document.getElementById(`lesson-card-${i}`);
        const progressBar = document.getElementById(`progress-bar-${i}`);
        const icon = document.getElementById(`lesson-icon-${i}`);
        const text = document.getElementById(`lesson-text-${i}`);
        if (!card) continue;
        
        let progress = userProgress[i] || 0;
        progressBar.style.width = `${(progress / 5) * 100}%`;
        
        let isUnlocked = (i === 1) || (userProgress[i-1] >= 5);
        
        if (isUnlocked) {
            card.classList.remove('locked');
            card.style.pointerEvents = "auto";
            if (icon) {
                if (i === 3) {
                    icon.className = 'fas fa-camera';
                } else {
                    icon.className = 'fas fa-book-open';
                }
                icon.style.color = 'var(--accent-blue)';
            }
            if (text) text.style.color = 'var(--accent-blue)';
        } else {
            card.classList.add('locked');
            card.style.pointerEvents = "none";
            if (icon) {
                 icon.className = 'fas fa-lock';
                 icon.style.color = 'var(--text-secondary)';
            }
            if (text) text.style.color = 'var(--text-secondary)';
        }
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
        if (section === 'practice') {
            window.location.href = '/practice';
            return;
        }
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
});

async function initGame() {
    try {
        let quizUrl = '/api/quiz/1';
        if (window.CURRENT_PAGE_TYPE === 'quiz') {
            quizUrl = `/api/quiz/${window.CURRENT_LESSON_ID || 1}`;
        }

        const [userRes, quizRes] = await Promise.all([
            fetch('/api/user'),
            fetch(quizUrl)
        ]);
        const userData = await userRes.json();
        const quizData = await quizRes.json();

        gameState.hearts = userData.hearts;
        gameState.diamonds = userData.diamonds;
        gameState.streak = userData.streak;
        gameState.nextHeartIn = userData.next_heart_in_seconds || 0;
        gameState.username = userData.username;
        
        let stored = localStorage.getItem('saybim_lesson_progress_' + userData.username);
        if (stored) {
            userProgress = JSON.parse(stored);
        } else {
            userProgress = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0 };
        }
        
        gameState.questions = quizData;
        gameState.totalQuestions = quizData.length;

        if (window.CURRENT_PAGE_TYPE !== 'quiz') {
            const nameDisplay = document.getElementById('user-name-display');
            const levelDisplay = document.getElementById('user-level-display');
            if (nameDisplay) nameDisplay.innerText = userData.username;
            if (levelDisplay) levelDisplay.innerText = `Level ${userData.level}`;
            updateDashboardStats();
            startHeartTimer();
        } else {
            // It's a quiz page
            gameState.currentLessonId = window.CURRENT_LESSON_ID;
            
            // Check if it's camera lesson (Lesson 3)
            if (gameState.currentLessonId === 3) {
                startPractice('alphabets');
                const camModal = document.getElementById('camera-modal');
                if(camModal) camModal.style.display = 'flex';
            } else {
                gameState.currentQuestionIndex = 0;
                updateQuizUI();
            }
        }

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
    if (lessonId === 3 || lessonName === 'Gesture Practice') {
        startPractice('alphabets');
        return;
    }
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
    document.getElementById('heart-count').innerText = gameState.hearts;

    // Update Question
    const quizContent = document.querySelector('.modal-content h3');
    if (quizContent) quizContent.innerText = currentQ.text;

    // Update Options
    const optionsContainer = document.querySelector('.quiz-options');
    optionsContainer.innerHTML = ''; // Clear previous options

    currentQ.options.forEach(opt => {
        const btn = document.createElement('button');
        btn.className = 'quiz-btn';
        btn.innerText = opt;
        btn.onclick = () => checkAnswer(btn, opt);
        optionsContainer.appendChild(btn);
    });

    // Update Image/Video
    const imageContainer = document.querySelector('.quiz-image');
    imageContainer.innerHTML = ''; // Clear existing

    if (currentQ.media_url) {
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
        // Fallback Icon
        imageContainer.innerHTML = '<i class="fas fa-hands-asl-interpreting" style="font-size: 4em; color: var(--text-secondary);"></i>';
        imageContainer.style.background = '#ebf8ff'; // Restore default bg
        imageContainer.style.boxShadow = '';
    }

    updateDashboardStats();
}

function updateDashboardStats() {
    const heartEl = document.getElementById('main-heart-count');
    const diamondEl = document.getElementById('main-diamond-count');
    const streakEl = document.getElementById('main-streak-count');
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
        });
        setTimeout(() => nextQuestion(), 1500);
    } else {
        playSound('incorrect');
        btnElement.classList.add('incorrect');
        // Submit Incorrect
        fetch('/api/quiz/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ correct: false })
        }).then(res => res.json()).then(data => {
            gameState.hearts = data.hearts;
            gameState.nextHeartIn = data.next_heart_in_seconds || 0;
            // updateQuizUI(); // Don't redraw yet, wait for delay logic
            document.getElementById('heart-count').innerText = gameState.hearts;

            if (gameState.hearts <= 0) {
                setTimeout(() => {
                    if (window.CURRENT_PAGE_TYPE !== 'quiz') {
                        closeModal('quiz-modal');
                    }
                    showGameOver();
                }, 1500);
            } else {
                setTimeout(() => nextQuestion(), 1500);
                // Move next even on wrong? Or let them retry? 
                // Generally in Duolingo style you get corrected and move on.
            }
        });
    }
}

function nextQuestion() {
    gameState.currentQuestionIndex++;
    if (gameState.currentQuestionIndex >= gameState.totalQuestions) {
        let fullyCompleted = false;
        if (gameState.currentLessonId) {
            if (userProgress[gameState.currentLessonId] < 5) {
                userProgress[gameState.currentLessonId]++;
                localStorage.setItem('saybim_lesson_progress_' + gameState.username, JSON.stringify(userProgress));
                if (userProgress[gameState.currentLessonId] === 5) {
                    fullyCompleted = true;
                }
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
                    
                    if (window.CURRENT_PAGE_TYPE === 'quiz') {
                        showFloatMessage(data.message || "Lesson Completed! +50 XP", 'success', () => {
                            window.location.href = '/';
                        });
                    } else {
                        showFloatMessage(data.message || "Lesson Completed! +50 XP", 'success');
                        updateDashboardStats();
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
                gameState.hearts = data.user.hearts;
                gameState.diamonds = data.user.diamonds;
                gameState.nextHeartIn = data.user.next_heart_in_seconds || 0;
                if (window.CURRENT_PAGE_TYPE !== 'quiz') {
                    updateDashboardStats();
                } else {
                    document.getElementById('heart-count').innerText = gameState.hearts;
                }
                
                const gameOverModal = document.getElementById('game-over-modal');
                if(gameOverModal) {
                     gameOverModal.classList.remove('active');
                     if(window.CURRENT_PAGE_TYPE === 'quiz') gameOverModal.style.display = 'none';
                }
                
                if (gameState.currentQuestionIndex < gameState.totalQuestions) {
                    if (window.CURRENT_PAGE_TYPE !== 'quiz') {
                        document.getElementById('quiz-modal').classList.add('active');
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
    const text = document.getElementById('feedback-text').value;
    if (text.trim() === '') {
        showFloatMessage("Please enter some feedback first!");
        return;
    }
    showFloatMessage("Thank you for your feedback! We've received it.");
    document.getElementById('feedback-text').value = '';
    closeModal('feedback-modal');
    document.getElementById('feedback-modal').style.display = 'none';
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
    const isPracticePage = window.CURRENT_PAGE_TYPE === 'practice' && practiceSession.active;

    if (sequence.length === 30 && model && (isModalActive || isPracticePage)) {
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

        // Check against target (Only if practice is active)
        if (practiceSession.active) {
            const currentTarget = practiceSession.items[practiceSession.currentIndex];
            if (predictedAction === currentTarget && confidence > 0.7) {
                sequence = [];
                handleCorrectAnswer(predictedAction);
            }
        }

    } catch (err) {
        console.error("Prediction error:", err);
    }

    isPredicting = false;
}

function handleCorrectAnswer(action) {
    playSound('correct');
    showFloatMessage(`Correct! That is ${action}.`);

    // Notify Backend
    fetch('/api/practice/complete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ word: action })
    }).then(res => res.json()).then(data => {
        gameState.diamonds = data.user.diamonds; // Update diamonds from backend response
        gameState.xp = data.user.xp;
        updateDashboardStats();
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
