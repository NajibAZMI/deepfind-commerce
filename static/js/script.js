// JavaScript pour afficher/masquer la fenêtre modale
const cameraButton = document.getElementById('cameraButton');
const uploadModal = document.getElementById('uploadModal');
const closeModal = document.getElementById('closeModal');

// Afficher la fenêtre modale
cameraButton.addEventListener('click', function () {
    uploadModal.style.display = 'flex'; // Affiche la fenêtre modale
});

// Fermer la fenêtre modale
closeModal.addEventListener('click', function () {
    uploadModal.style.display = 'none'; // Masque la fenêtre modale
});

// Fermer la fenêtre modale en cliquant en dehors de celle-ci
window.addEventListener('click', function (event) {
    if (event.target === uploadModal) {
        uploadModal.style.display = 'none';
    }
});

// Liste des produits dans le panier
let cart = [];

// Fonction pour ajouter un produit au panier
function addToCart(product) {
    cart.push(product);
    alert('Produit ajouté au panier : ' + product);
}

// Afficher le panier
document.getElementById('cartButton').addEventListener('click', function () {
    const cartModal = document.getElementById('cartModal');
    const cartItems = document.getElementById('cartItems');

    // Vider la liste actuelle des articles du panier
    cartItems.innerHTML = '';

    // Ajouter chaque article dans le panier
    cart.forEach(function (product) {
        const li = document.createElement('li');
        li.textContent = product;
        cartItems.appendChild(li);
    });

    // Afficher la modale du panier
    cartModal.style.display = 'flex';
});

// Fermer le panier
function closeCart() {
    document.getElementById('cartModal').style.display = 'none';
}

// Fonction pour la recherche
document.getElementById('searchButton').addEventListener('click', function () {
    const query = document.getElementById('searchInput').value;
    alert('Rechercher : ' + query);
});
