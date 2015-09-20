/**
 * Created by user on 18.09.15.
 */

function register_____________________() {
    navigator.serviceWorker.register('sw.js', {scope: './'}).then(function(registration) {
        //debugger
        // Registration was successful
        console.log('ServiceWorker registration successful with scope: ',    registration.scope);
    }).catch(function(err) {
        // registration failed :(
        console.log('ServiceWorker registration failed: ', err);
    });
}

if ('serviceWorker' in navigator) {
    register_____________________();

//    navigator.serviceWorker.getRegistration().then(function(reg) {
//        if (reg) {
//            reg.unregister().then(function() {
//                debugger
//                register_____________________();
//            });
//        } else {
//            register_____________________();
//        }

//    });
}