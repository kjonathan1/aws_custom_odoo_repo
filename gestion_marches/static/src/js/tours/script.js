document.addEventListener('DOMContentLoaded', function() {
    var cards = document.querySelectorAll('.card');
    cards.forEach(function(card) {
        card.addEventListener('mouseover', function() {
            card.style.backgroundColor = '#f8f9fa'; /* Couleur de fond lors du survol */
            card.style.borderColor = '#007bff'; /* Couleur de bordure lors du survol */
            card.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.2)'; /* Ombre portée lors du survol */
            card.style.transform = 'scale(1.05)'; /* Agrandir légèrement le cadre lors du survol */
        });
        card.addEventListener('mouseout', function() {
            card.style.backgroundColor = ''; /* Réinitialiser la couleur de fond */
            card.style.borderColor = ''; /* Réinitialiser la couleur de bordure */
            card.style.boxShadow = ''; /* Réinitialiser l'ombre portée */
            card.style.transform = ''; /* Réinitialiser la transformation */
        });
    });
});