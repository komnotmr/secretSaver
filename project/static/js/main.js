'use strict;'

require.config({
    baseUrl: '../static/',
    paths:{
        jquery: 'thirdParty/jquery-3.4.1.min',
        knockout: 'thirdParty/knockout-3.5.1',
        domReady: 'thirdParty/domReady',
        model: 'js/model'
    }
});

require(['domReady!', 'knockout', 'model'],
(doc, ko, Model) => {
    console.log('inited');   
    ko.applyBindings(new Model());
});

