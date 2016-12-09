/**
 * Created by user on 17.09.15.
 */
importScripts('/static/js/lib/index.js');

var CACHE_MAIN = 'admin-main-v6';
var CACHE_STATIC = 'admin-static-v6';
var CACHE_APP = 'admin-app-v19';

var expectedCaches = [
  CACHE_MAIN,
  CACHE_STATIC,
  CACHE_APP
];

var urlCacheMain = [
    '/admin'
];

var urlCacheStatic = [
    'https://code.ionicframework.com/ionicons/2.0.1/css/ionicons.min.css',
    "/static/css/lib/font-awesome-4.1.0/fonts/fontawesome-webfont.woff?v=4.1.0",
    "https://fonts.gstatic.com/s/sourcesanspro/v9/toadOcfmlt9b38dHJxOBGCOFnW3Jk0f09zW_Yln67Ac.woff2",
    '/static/css/fonts/glyphicons-halflings-regular.woff2',
    '/static/css/fonts/glyphicons-halflings-regular.woff',
    '/static/css/fonts/glyphicons-halflings-regular.ttf',
    '/static/css/lib/bootstrap.min.css',
    '/static/css/lib/font-awesome-4.1.0/css/font-awesome.min.css',
    '/static/newadmin/css/minimal/_all.css',
    '/static/newadmin/css/square/_all.css',
    '/static/newadmin/css/flat/_all.css',
    '/static/newadmin/css/line/_all.css',
    '/static/newadmin/css/main.css',
    '/static/newadmin/css/AdminLTE.css',
    '/static/newadmin/css/dataTables.bootstrap.css',
    '/static/newadmin/css/skins/_all-skins.min.css',
    '/static/css/lib/toastr.min.css',
    '/static/newadmin/css/all.css',
    '/static/js/lib/jquery.js',
    '/static/js/lib/icheck.min.js',
    '/static/js/lib/underscore-min.1.8.3.js',
    '/static/js/lib/angular1.4.js',
    '/static/gen/angularjs-utils.min.js?3c9b3d82',
    '/static/gen/spin.min.js?67f9a9dd',
    '/static/js/lib/ui-bootstrap-tpls-0.13.3.js',
    '/static/js/lib/ng-table.min.js',
    '/static/css/lib/ng-table.min.css',
    '/static/js/lib/select.js',
    '/static/css/lib/select.css',
    '/static/css/lib/select2.css',
    '/static/css/lib/angular-clock.css',
    '/static/js/lib/toastr.min.js',
];

var urlCacheApp = [

    {% assets 'NAjs' %}
        '{{ ASSET_URL }}',
    {% endassets %}

    '/static/newadmin/template/admin.html',
    '/static/newadmin/template/dash.html',
    '/static/newadmin/template/load.html',
    '/static/newadmin/template/login.html',
    '/static/newadmin/template/403.html',

    '/static/newadmin/js/applications/mail/template/base.html',
    '/static/newadmin/js/applications/mail/template/list.head.html',
    '/static/newadmin/js/applications/mail/template/list.html',
    "/static/newadmin/js/applications/mail/template/read.head.html",
    "/static/newadmin/js/applications/mail/template/read.html",

    "/static/newadmin/js/applications/invoice/template/form.html",
    "/static/newadmin/js/applications/invoice/template/list.html",
    "/static/newadmin/js/applications/invoice/template/create.html",
    "/static/newadmin/js/applications/invoice/template/view.html",
    "/static/newadmin/js/applications/invoice/template/edit.html",

    "/static/newadmin/js/applications/collect/template/form.html",
    "/static/newadmin/js/applications/collect/template/list.html",
    "/static/newadmin/js/applications/collect/template/create.html",
    "/static/newadmin/js/applications/collect/template/view.html",
    "/static/newadmin/js/applications/collect/template/edit.html",

    "/static/newadmin/js/applications/good/template/form.html",
    "/static/newadmin/js/applications/good/template/list.html",
    "/static/newadmin/js/applications/good/template/create.html",
    "/static/newadmin/js/applications/good/template/view.html",
    "/static/newadmin/js/applications/good/template/edit.html",

    "/static/newadmin/js/applications/commodity/template/form.html",
    "/static/newadmin/js/applications/commodity/template/list.html",
    "/static/newadmin/js/applications/commodity/template/create.html",
    "/static/newadmin/js/applications/commodity/template/view.html",
    "/static/newadmin/js/applications/commodity/template/edit.html",

    "/static/newadmin/js/applications/acceptance/template/form.html",
    "/static/newadmin/js/applications/acceptance/template/list.html",
    "/static/newadmin/js/applications/acceptance/template/create.html",
    "/static/newadmin/js/applications/acceptance/template/view.html",
    "/static/newadmin/js/applications/acceptance/template/edit.html",

    "/static/newadmin/js/applications/pointsale/template/form.html",
    "/static/newadmin/js/applications/pointsale/template/list.html",
    "/static/newadmin/js/applications/pointsale/template/create.html",
    "/static/newadmin/js/applications/pointsale/template/view.html",
    "/static/newadmin/js/applications/pointsale/template/edit.html",

    "/static/newadmin/js/applications/provider/template/form.html",
    "/static/newadmin/js/applications/provider/template/list.html",
    "/static/newadmin/js/applications/provider/template/create.html",
    "/static/newadmin/js/applications/provider/template/view.html",
    "/static/newadmin/js/applications/provider/template/edit.html",

    "/static/newadmin/js/applications/receiver/template/form.html",
    "/static/newadmin/js/applications/receiver/template/list.html",
    "/static/newadmin/js/applications/receiver/template/create.html",
    "/static/newadmin/js/applications/receiver/template/view.html",
    "/static/newadmin/js/applications/receiver/template/edit.html",

    "/static/newadmin/js/applications/session/template/view.html",
    "/static/newadmin/js/applications/session/template/menu.html",
    "/static/newadmin/js/applications/session/template/menumodal.html",

    "/static/newadmin/js/applications/user/template/form.html",
    "/static/newadmin/js/applications/user/template/list.html",
    "/static/newadmin/js/applications/user/template/create.html",
    "/static/newadmin/js/applications/user/template/view.html",
    "/static/newadmin/js/applications/user/template/edit.html",

    "/static/newadmin/js/applications/waybill/template/form_.html",
    "/static/newadmin/js/applications/waybill/template/selectgood.html",
    "/static/newadmin/js/applications/waybill/template/page_bulk.html",
    "/static/newadmin/js/applications/waybill/template/list_.html",
    "/static/newadmin/js/applications/waybill/template/create_.html",
    "/static/newadmin/js/applications/waybill/template/read_.html",
    "/static/newadmin/js/applications/waybill/template/read_create.html",

    '/static/newadmin/template/directive/dsf.html',
];

var MAP_CACHE = {};
MAP_CACHE[CACHE_MAIN] = urlCacheMain;
MAP_CACHE[CACHE_STATIC] = urlCacheStatic;
MAP_CACHE[CACHE_APP] = urlCacheApp;

// Set the callback for the install step
self.addEventListener('install', function(event) {
    // Perform install steps
    console.log("Install " + CACHE_STATIC + " " + CACHE_MAIN + " " + CACHE_APP);
    event.waitUntil(
        Promise.all([
            caches.open(CACHE_STATIC).then(function(cache) {
                return cache.addAll(MAP_CACHE[CACHE_STATIC]);
            }),
            caches.open(CACHE_MAIN).then(function(cache) {
                return cache.addAll(MAP_CACHE[CACHE_MAIN]);
            }),
            caches.open(CACHE_APP).then(function(cache) {
                return cache.addAll(MAP_CACHE[CACHE_APP]);
            })
        ])
      );
});

self.addEventListener('fetch', function(event) {
    event.respondWith(
        caches.match(event.request)
      .then(function(response) {
        // Cache hit - return response
        if (response) {
          return response;
        }

        return fetch(event.request);
      }
    )
  );
});

self.addEventListener('activate', function(event) {
    console.log("Active " + CACHE_STATIC + " " + CACHE_MAIN + " " + CACHE_APP);
    event.waitUntil(
        caches.keys().then(function(cacheNames) {
          return Promise.all(
            cacheNames.filter(function(cacheName) {
                return expectedCaches.indexOf(cacheName) == -1;
              // Return true if you want to remove this cache,
              // but remember that caches are shared across
              // the whole origin
            }).map(function(cacheName) {
              return caches.delete(cacheName);
            })
          );
        })
      );
});
