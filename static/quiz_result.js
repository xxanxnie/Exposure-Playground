document.addEventListener('DOMContentLoaded', function () {
    const allButtons = document.querySelectorAll('.question-summary .btn');
    allButtons.forEach(button => {
        button.addEventListener('click', function () {
            // Remove active class from all buttons
            allButtons.forEach(btn => btn.classList.remove('active-question'));

            // Add active class to the clicked button
            const targetId = button.getAttribute('data-bs-target');
            const targetCollapse = document.querySelector(targetId);

            if (!targetCollapse.classList.contains('show')) {
                button.classList.add('active-question');
            }
        });
    });

    // Collapse hide event - remove active class
    const collapses = document.querySelectorAll('.accordion-collapse');
    collapses.forEach(collapse => {
        collapse.addEventListener('hidden.bs.collapse', () => {
            allButtons.forEach(btn => {
                const targetId = btn.getAttribute('data-bs-target');
                if (targetId === '#' + collapse.id) {
                    btn.classList.remove('active-question');
                }
            });
        });
    });
});
