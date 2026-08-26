/* Must load AFTER designesia.js. Site-specific behaviour for the Bo Meubles mockup. */

jQuery(function ($) {

    /* ---------------------------------------------------------------
     * Project galleries
     * The template initialises magnificPopup with English UI strings.
     * Re-bind each .images-group so the counter and controls read in French.
     * Pages without project galleries simply match nothing.
     * --------------------------------------------------------------- */
    $('.images-group').each(function () {
        $(this).magnificPopup({
            delegate: 'a',
            type: 'image',
            tClose: 'Fermer (Échap)',
            tLoading: 'Chargement...',
            gallery: {
                enabled: true,
                tCounter: '%curr% sur %total%',
                tPrev: 'Précédent',
                tNext: 'Suivant'
            },
            image: {
                tError: '<a href="%url%">L’image</a> n’a pas pu être chargée.'
            }
        });
    });
});
