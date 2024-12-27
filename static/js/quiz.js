document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('skinQuizForm');
    const steps = document.querySelectorAll('.quiz-step');
    const progressBar = document.querySelector('.progress-bar');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const submitBtn = document.getElementById('submit-btn');
    
    let currentStep = 1;
    const totalSteps = steps.length;

    function updateProgress() {
        const progress = ((currentStep - 1) / totalSteps) * 100;
        progressBar.style.width = progress + '%';
        progressBar.setAttribute('aria-valuenow', progress);
    }

    function showStep(stepNumber) {
        steps.forEach(step => {
            step.style.display = 'none';
        });
        document.querySelector(`[data-step="${stepNumber}"]`).style.display = 'block';
        
        // Update buttons
        prevBtn.style.display = stepNumber === 1 ? 'none' : 'block';
        nextBtn.style.display = stepNumber === totalSteps ? 'none' : 'block';
        submitBtn.style.display = stepNumber === totalSteps ? 'block' : 'none';
        
        updateProgress();
    }

    function validateCurrentStep() {
        const currentStepElement = document.querySelector(`[data-step="${currentStep}"]`);
        
        if (currentStep === 1 || currentStep === 2) {
            // Check radio buttons
            const radioButtons = currentStepElement.querySelectorAll('input[type="radio"]');
            const checked = Array.from(radioButtons).some(radio => radio.checked);
            return checked;
        } else if (currentStep === 3) {
            // At least one checkbox should be checked
            const checkboxes = currentStepElement.querySelectorAll('input[type="checkbox"]');
            const checked = Array.from(checkboxes).some(checkbox => checkbox.checked);
            return checked;
        }
        return true; // Location step is validated separately
    }

    nextBtn.addEventListener('click', () => {
        if (!validateCurrentStep()) {
            alert('Please make a selection before proceeding.');
            return;
        }
        currentStep++;
        showStep(currentStep);
    });

    prevBtn.addEventListener('click', () => {
        currentStep--;
        showStep(currentStep);
    });

    form.addEventListener('submit', (e) => {
        if (!validateCurrentStep()) {
            e.preventDefault();
            alert('Please complete all questions before submitting.');
        }
    });

    // Initialize first step
    showStep(1);
});
