/**
 * Created by user on 09.10.15.
 */


//(function(w, $) {
//    debugger
//
//    var version = 1;
//    var KEY_VERSION_STATIC = "KEY_VERSION_STATIC";
//
//    var currentVersion = getVersion();
//
//    if (!currentVersion || currentVersion < version) {
//        console.log("NEED UPDATE CACHE");
//        $('body').prepend('<nav class="frame" style="padding-top: 5px; padding-bottom: 5px;"><div class="container-fluid">Для корректной работы приложения нажмите кнопку <button id="UpdateBUTTON" class="btn btn-primary">Обновить</button></div></nav>');
//
//        $("#UpdateBUTTON").click(function() {
//            console.log("UPDATES");
////            window.reloadIgnoringCache()
//            w.location = w.location.href+'?eraseCache=true';
//        });
//    }
//
//    function getVersion() {
//        return w.localStorage.getItem(KEY_VERSION_STATIC);
//    }
//
//    function setVersion(vers) {
//        w.localStorage.setItem(KEY_VERSION_STATIC, vers);
//    }
//})(window, $);