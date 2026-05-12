// tutorial.js - Onboarding logic using Driver.js

document.addEventListener('DOMContentLoaded', () => {
    // Check if tutorial is active via URL or localStorage
    const urlParams = new URLSearchParams(window.location.search);
    let isTutorialActive = urlParams.get('tutorial') === 'true' || localStorage.getItem('saybim_tutorial_active') === 'true';
    
    if (urlParams.get('tutorial') === 'true') {
        localStorage.setItem('saybim_tutorial_active', 'true');
        localStorage.setItem('saybim_tutorial_step', 'home_intro');
    }

    if (!isTutorialActive) return;

    // Remove URL param to clean up URL
    if (urlParams.has('tutorial')) {
        const newUrl = window.location.pathname + (window.location.search.replace(/[\?&]tutorial=true/, '') || '');
        window.history.replaceState({}, '', newUrl);
    }

    const currentStep = localStorage.getItem('saybim_tutorial_step');
    const path = window.location.pathname;
    
    // Check if driver is loaded
    if (!window.driver || !window.driver.js) {
        console.error("Driver.js not loaded.");
        return;
    }

    // Custom Driver variables for programmatic management
    window.isProgrammatic = false;
    window.driverObj = window.driver.js.driver({
        showProgress: true,
        allowClose: false,
        overlayColor: 'rgba(0,0,0,0.6)',
        onDestroyStarted: () => {
            if (isProgrammatic) {
                driverObj.destroy();
                return;
            }
            if(confirm('Are you sure you want to skip the tutorial?')) {
                localStorage.removeItem('saybim_tutorial_active');
                localStorage.removeItem('saybim_tutorial_step');
                driverObj.destroy();
            }
        }
    });

    const markStepDone = (nextStep) => {
        localStorage.setItem('saybim_tutorial_step', nextStep);
    };

    const endTutorial = () => {
        localStorage.removeItem('saybim_tutorial_active');
        localStorage.removeItem('saybim_tutorial_step');
        
        if (typeof showFloatMessage === 'function') {
            showFloatMessage("Tutorial Complete! Have fun learning Sign Language!", 'success');
        } else {
            alert("Tutorial Complete! Have fun learning Sign Language!");
        }
    };

    // --- Phase 1: Home Page Intro ---
    if (path === '/' && currentStep === 'home_intro') {
        setTimeout(() => {
            // Find Practice Nav Link
            const navLinks = Array.from(document.querySelectorAll('.nav-link'));
            const practiceNav = navLinks.find(el => el.textContent.includes('Practice'));
            
            // Bind click listener for Practice Nav directly
            if (practiceNav) {
                practiceNav.addEventListener('click', function onPracticeClick() {
                    // Ensure we only trigger when on the right step
                    if (localStorage.getItem('saybim_tutorial_step') !== 'home_intro') return;

                    isProgrammatic = true;
                    driverObj.destroy();
                    isProgrammatic = false;
                    
                    // Wait for section to be visible
                    setTimeout(() => {
                        const alphabetsCard = document.querySelector('.lesson-card[onclick*="practice?type=alphabets"]');
                        driverObj.setSteps([
                            {
                                element: alphabetsCard || '#practice-section',
                                popover: {
                                    title: 'Alphabets Practice',
                                    description: 'Here you can explore various practice modules. Click on "Alphabets" to continue.',
                                    side: "bottom",
                                    align: 'center',
                                    showButtons: [] // Remove buttons
                                }
                            }
                        ]);
                        driverObj.drive();
                        
                        // Bind click listener for Alphabets Card directly
                        if (alphabetsCard) {
                            alphabetsCard.addEventListener('click', function onAlphaClick() {
                                markStepDone('practice_alphabets');
                                isProgrammatic = true;
                                driverObj.destroy();
                                isProgrammatic = false;
                            }, { once: true });
                        }
                    }, 500);
                }, { once: true });
            }

            driverObj.setSteps([
                {
                    popover: {
                        title: 'Welcome to SayBIM!',
                        description: 'SayBIM is your interactive AI-powered Sign Language learning companion. Let\'s show you around!',
                        side: "bottom",
                        align: 'center'
                    }
                },
                {
                    element: practiceNav || '.sidebar',
                    popover: {
                        title: 'Practice Mode',
                        description: 'To begin, let\'s show you how to practice your signing. Click on the "Practice" tab.',
                        side: window.innerWidth < 768 ? "top" : "right",
                        align: 'start',
                        showButtons: [] // Remove buttons, force user to click
                    }
                }
            ]);
            driverObj.drive();
        }, 1000);
    }
    
    // --- Phase 2: Practice Page ---
    if (path === '/practice' && currentStep === 'practice_alphabets') {
        setTimeout(() => {
            // Bind listener to practice selection cards
            const practicePanel = document.getElementById('practice-selection-panel');
            if (practicePanel) {
                practicePanel.addEventListener('click', (e) => {
                    const card = e.target.closest('.quiz-btn');
                    if (card && localStorage.getItem('saybim_tutorial_step') === 'practice_alphabets') {
                        if (driverObj.getActiveIndex() === 0) { // If on "Choose a Sign"
                            driverObj.moveNext();
                        }
                    }
                });
            }

            // Bind listener for Back button
            const backBtn = document.getElementById('practice-back-btn');
            if (backBtn) {
                backBtn.addEventListener('click', () => {
                    if (localStorage.getItem('saybim_tutorial_step') === 'practice_alphabets') {
                        markStepDone('home_leaderboard');
                        isProgrammatic = true;
                        driverObj.destroy();
                        isProgrammatic = false;
                    }
                });
            }

            driverObj.setSteps([
                {
                    element: '#practice-selection-panel',
                    popover: {
                        title: 'Choose a Sign',
                        description: 'Select any letter from the grid that you would like to practice.',
                        side: "left",
                        align: 'start',
                        showButtons: [] // User must click a card
                    }
                },
                {
                    popover: {
                        title: 'Privacy First',
                        description: 'Don\'t worry! The camera processing happens completely locally on your device. We do not record or upload your video anywhere. Your privacy is 100% safe.',
                        side: "bottom",
                        align: 'center',
                        showButtons: ['next'], // Remove previous/close
                        nextBtnText: 'OK', // Rename next to OK
                        onNextClick: () => {
                            driverObj.moveNext();
                        }
                    }
                },
                {
                    element: '#practice-camera-container',
                    popover: {
                        title: 'Your Turn!',
                        description: 'Try signing the letter to the camera! Once you get it right, you will earn your first badge.',
                        side: "bottom",
                        align: 'center',
                        showButtons: [] // User must earn the badge, no buttons
                    }
                }
            ]);
            driverObj.drive();
            
            // Global function to show the back arrow tutorial
            // This is called from script.js after the user clicks "OK" on the success prompt
            window.showBackTutorial = () => {
                if (localStorage.getItem('saybim_tutorial_step') !== 'practice_alphabets') return;
                
                setTimeout(() => {
                    window.driverObj.setSteps([
                        {
                            element: '#practice-back-btn',
                            popover: {
                                title: 'Great Job!',
                                description: 'You\'ve practiced your first sign! Now click the back arrow to return to the Dashboard.',
                                side: "bottom",
                                align: 'start',
                                showButtons: [] // Remove buttons, force user to click the back arrow
                            }
                        }
                    ]);
                    window.driverObj.drive();
                }, 800);
            };

            // Wait for badge modal to pop up to hide the equip button
            const observer = new MutationObserver((mutations) => {
                const modal = document.getElementById('badge-celebration-modal');
                if (modal && modal.classList.contains('active')) {
                    // Hide Equip Now during tutorial to encourage return to dashboard
                    const equipBtn = document.getElementById('equip-now-btn');
                    if (equipBtn) equipBtn.style.display = 'none';

                    // When it closes, we can restore the button style for future use
                    const closeObserver = new MutationObserver(() => {
                        if (!modal.classList.contains('active')) {
                            closeObserver.disconnect();
                            if (equipBtn) equipBtn.style.display = '';
                        }
                    });
                    closeObserver.observe(modal, { attributes: true, attributeFilter: ['class'] });
                }
            });
            observer.observe(document.body, { childList: true, subtree: true, attributes: true });
        }, 1500); // Wait a bit longer for models to load and render
    }

    // --- Phase 3 & 6: Home Page (Leaderboard & Shop) ---
    if (path === '/') {
        if (currentStep === 'home_leaderboard') {
            setTimeout(() => {
                const navLinks = Array.from(document.querySelectorAll('.nav-link'));
                const lessonNav = navLinks.find(el => el.textContent.includes('Lesson'));
                const topic1Card = document.getElementById('lesson-card-1');

                // Bind listener for Lesson Tab
                if (lessonNav) {
                    lessonNav.addEventListener('click', () => {
                        if (driverObj.getActiveIndex() === 2) { // "Start Learning" step
                            driverObj.moveNext();
                        }
                    }, { once: true });
                }

                // Bind listener for Topic 1 Card
                if (topic1Card) {
                    topic1Card.addEventListener('click', () => {
                        if (driverObj.getActiveIndex() === 3) { // "Topic 1" step
                            markStepDone('topic_lessons');
                            window.isProgrammatic = true;
                            driverObj.destroy();
                            window.isProgrammatic = false;
                        }
                    }, { once: true });
                }

                // Ensure we are on leaderboard section
                switchSection('leaderboard');
                
                driverObj.setSteps([
                    {
                        element: '#leaderboard-section',
                        popover: {
                            title: 'Leaderboard',
                            description: 'This is where you can see top learners. You earn XP by doing lessons and practicing.',
                            side: "bottom",
                            align: 'start'
                        }
                    },
                    {
                        element: '#leaderboard-body',
                        popover: {
                            title: 'Weekly Rewards',
                            description: 'The top 3 players at the end of the week will receive special Gold, Silver, and Bronze badges!',
                            side: "bottom",
                            align: 'start'
                        }
                    },
                    {
                        element: lessonNav || '.sidebar',
                        popover: {
                            title: 'Start Learning',
                            description: 'Let\'s earn some XP! Click on the "Lesson" tab to see your curriculum.',
                            side: window.innerWidth < 768 ? "top" : "right",
                            align: 'start',
                            showButtons: [] // User must click Lesson tab
                        }
                    },
                    {
                        element: '#lesson-card-1',
                        popover: {
                            title: 'Topic 1',
                            description: 'Click here to open the lessons for Topic 1.',
                            side: "bottom",
                            align: 'center',
                            showButtons: [] // User must click the card
                        }
                    }
                ]);
                driverObj.drive();
            }, 1000);
        } else if (currentStep === 'home_shop') {
            setTimeout(() => {
                switchSection('shop');
                driverObj.setSteps([
                    {
                        element: '#shop-section',
                        popover: {
                            title: 'The SayBIM Shop',
                            description: 'Welcome to the shop! Here you can spend diamonds earned from leveling up and completing lessons.',
                            side: "bottom",
                            align: 'center'
                        }
                    },
                    {
                        element: '#shop-items-grid',
                        popover: {
                            title: 'Power-ups',
                            description: 'You can buy Heart Refills, Timer Freezes, Shields, and more.',
                            side: "bottom",
                            align: 'center'
                        }
                    },
                    {
                        element: '.shop-card[data-item="timer_freeze"]',
                        popover: {
                            title: 'Mastery Challenges',
                            description: 'IMPORTANT: Note that items like Timer Freeze can ONLY be used during the final Mastery Challenge of each topic, where things get tough!',
                            side: "bottom",
                            align: 'center'
                        }
                    },
                    {
                        popover: {
                            title: 'You\'re All Set!',
                            description: 'That concludes the tutorial. You are now ready to master Sign Language with SayBIM! Good luck!',
                            side: "bottom",
                            align: 'center',
                            onNextClick: () => {
                                endTutorial();
                                isProgrammatic = true;
                                driverObj.destroy();
                                isProgrammatic = false;
                                window.location.href = '/';
                            }
                        }
                    }
                ]);
                driverObj.drive();
            }, 1000);
        }
    }

    // --- Phase 4: Topic Lessons Page ---
    if (path.startsWith('/topic/') && currentStep === 'topic_lessons') {
        setTimeout(() => {
            const lesson1Btn = document.querySelector('.lesson-step:first-child');
            
            if (lesson1Btn) {
                lesson1Btn.addEventListener('click', () => {
                    markStepDone('quiz_first');
                    window.isProgrammatic = true;
                    driverObj.destroy();
                    window.isProgrammatic = false;
                }, { once: true });
            }

            driverObj.setSteps([
                {
                    element: '.lesson-step:first-child',
                    popover: {
                        title: 'Your First Lesson',
                        description: 'Click on Lesson 1 to begin the quiz. Good luck!',
                        side: "bottom",
                        align: 'center',
                        showButtons: [] // User must click the lesson
                    }
                }
            ]);
            driverObj.drive();
        }, 1500); // Ensure everything is loaded
    }

    // --- Phase 5: Quiz Page ---
    if (path.startsWith('/quiz/') && currentStep === 'quiz_first') {
        setTimeout(() => {
            driverObj.setSteps([
                {
                    element: '.quiz-image',
                    popover: {
                        title: 'Learn the Sign',
                        description: 'Look at the image carefully. This is the sign you need to identify.',
                        side: window.innerWidth < 768 ? "bottom" : "top", 
                        align: 'center'
                    }
                },
                {
                    element: '.hint-btn',
                    popover: {
                        title: 'Need Help?',
                        description: 'If you are stuck, you can click the Hint button for more understanding.',
                        side: "right", // Changed from bottom
                        align: 'start'
                    }
                },
                {
                    element: '.quiz-util-card',
                    popover: {
                        title: 'Hearts System',
                        description: 'You have 5 hearts. If you answer incorrectly, a heart is deducted. If you run out, you will need to refill using diamonds or quit the lesson.',
                        side: "left", // Changed from bottom
                        align: 'center'
                    }
                },
                {
                    popover: {
                        title: 'Start Answering!',
                        description: 'Select the correct answer below. Finish the lesson to continue the tutorial.',
                        side: "top",
                        align: 'center',
                        onNextClick: () => {
                            markStepDone('quiz_finish');
                            window.isProgrammatic = true;
                            window.driverObj.destroy();
                            window.isProgrammatic = false;
                        }
                    }
                }
            ]);
            driverObj.drive();
        }, 1500); // Ensure everything is loaded
    }

    // Intercept Quiz Completion to go to Shop
    if (path.startsWith('/quiz/') && currentStep === 'quiz_finish') {
        // Hijack the final exit
        const originalConfirmExit = window.confirmExit;
        if(originalConfirmExit) {
            window.confirmExit = function(onConfirm) {
                // If it's at the end of the lesson (hearts > 0), redirect to Shop
                if (gameState.hearts > 0) {
                    markStepDone('home_shop');
                    window.location.href = '/?section=shop';
                } else {
                    originalConfirmExit(onConfirm);
                }
            }
        }
        
        // Also observe the completion modal button just in case
        const observer = new MutationObserver(() => {
            const feedbackOverlay = document.getElementById('quiz-feedback-overlay');
            if (feedbackOverlay && feedbackOverlay.style.display !== 'none') {
                const btn = feedbackOverlay.querySelector('.feedback-ok-btn');
                if (btn && btn.textContent.includes('Continue')) {
                    // Check if it's the last question
                    if (gameState.currentQuestionIndex >= gameState.totalQuestions - 1) {
                        btn.addEventListener('click', (e) => {
                            e.preventDefault();
                            e.stopPropagation();
                            markStepDone('home_shop');
                            window.location.href = '/?section=shop';
                        }, { once: true });
                    }
                }
            }
        });
        observer.observe(document.body, { childList: true, subtree: true });
    }

});
