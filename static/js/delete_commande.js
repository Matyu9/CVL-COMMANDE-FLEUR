function delete_commande() {
    if (confirm('Êtes vous sur de vouloir supprimer cette commande ? ')){
        document.getElementById('delete_commande').submit();
    } else {
        console.log('Annulation de la requete.')
    }
}
