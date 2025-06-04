document.addEventListener('DOMContentLoaded', function() {
    // Function to calculate average for a single card
    function calculateAverage(card) {
        const totalPoints = parseFloat(card.querySelector('.total-points').dataset.total);
        const gamesPlayed = parseInt(card.querySelector('.games-played').dataset.games);
        const avgElement = card.querySelector('.avg-points');
        
        if (totalPoints && gamesPlayed) {
            const average = (totalPoints / gamesPlayed).toFixed(1);
            avgElement.textContent = average;
        } else {
            avgElement.textContent = '--';
        }
    }

    // Calculate averages for all cards when the page loads
    document.querySelectorAll('.draft-pick-card').forEach(calculateAverage);

    // Set up observers for each card
    document.querySelectorAll('.draft-pick-card').forEach(card => {
        const observer = new MutationObserver(() => calculateAverage(card));
        const statsContainer = card.querySelector('.pick-stats');
        
        if (statsContainer) {
            observer.observe(statsContainer, { 
                subtree: true, 
                characterData: true,
                childList: true,
                attributes: true,
                attributeFilter: ['data-total', 'data-games'] 
            });
        }
    });
}); 