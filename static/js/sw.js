/**
 * Created by user on 17.09.15.
 */
importScripts('/static/js/lib/index.js');

//var CACHE_NAME = 'my-site-cache-v1';
//// The files we want to cache
//var urlsToCache = [
//    '/static/newadmin/app/mail/template/base.html',
//    '/static/newadmin/app/mail/template/list.head.html',
//    '/static/newadmin/app/mail/template/list.html',
//    "/static/newadmin/app/mail/template/read.head.html",
//    "/static/newadmin/app/mail/template/read.html",
//
//    "/static/newadmin/app/invoice/template/form.html",
//    "/static/newadmin/app/invoice/template/list.html",
//    "/static/newadmin/app/invoice/template/create.html",
//    "/static/newadmin/app/invoice/template/view.html",
//    "/static/newadmin/app/invoice/template/edit.html",
//
//    "/static/newadmin/app/good/template/form.html",
//    "/static/newadmin/app/good/template/list.html",
//    "/static/newadmin/app/good/template/create.html",
//    "/static/newadmin/app/good/template/view.html",
//    "/static/newadmin/app/good/template/edit.html",
//
//    "/static/newadmin/app/commodity/template/form.html",
//    "/static/newadmin/app/commodity/template/list.html",
//    "/static/newadmin/app/commodity/template/create.html",
//    "/static/newadmin/app/commodity/template/view.html",
//    "/static/newadmin/app/commodity/template/edit.html",
//];
//
////debugger
//
//// Set the callback for the install step
//self.addEventListener('install', function(event) {
//    debugger
//    // Perform install steps
//    event.waitUntil(
//        caches.open(CACHE_NAME)
//          .then(function(cache) {
//            console.log('Opened cache');
//            return cache.addAll(urlsToCache);
//          })
//      );
//});
//
//self.addEventListener('fetch', function(event) {
//    debugger
//    event.respondWith(
//        caches.match(event.request)
//      .then(function(response) {
//        // Cache hit - return response
//        if (response) {
//          return response;
//        }
//
//        return fetch(event.request);
//      }
//    )
//  );
//});
//
//self.addEventListener('activate', function(event) {
//
//  var cacheWhitelist = [CACHE_NAME];
//
//  event.waitUntil(
//    caches.keys().then(function(cacheNames) {
//      return Promise.all(
//        cacheNames.map(function(cacheName) {
//          if (cacheWhitelist.indexOf(cacheName) === -1) {
//            return caches.delete(cacheName);
//          }
//        })
//      );
//    })
//  );
//});


self.addEventListener('install', function(event) {
  console.log("SW installed");
});

self.addEventListener('activate', function(event) {
  console.log("SW activated");
});

self.addEventListener('fetch', function(event) {
  console.log("Caught a fetch!");
  event.respondWith(new Response("Hello world!"));
});