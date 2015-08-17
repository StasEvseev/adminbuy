app.factory("{{ import_id }}RES_CREATE", function($resource, Base64) {
  return $resource("{{ url_create }}", {inner_id: "@inner_id"}, {
    meth: { method: "PUT", isArray: false , headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
  });
})

.factory("{{ import_id }}RES_GETALL", function($resource, Base64) {
  return $resource("{{ url_getall }}", {inner_id: "@inner_id"}, {
    meth: { method: "GET", isArray: false, headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
  });
})

.factory("{{ import_id }}RES_GET", function($resource, Base64) {
  return $resource("{{ url_get }}", {id: "@id", inner_id: "@inner_id"}, {
    meth: { method: "GET", isArray: false, headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
  });
})

.factory("{{ import_id }}RES_UPDATE", function($resource, Base64) {
  return $resource("{{ url_update }}", {id: "@id", inner_id: "@inner_id"}, {
    meth: { method: "POST", isArray: false, headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
  });
})

.factory("{{ import_id }}RES_DELETE", function($resource, Base64) {
  return $resource("{{ url_delete }}", {id: "@id", inner_id: "@inner_id"}, {
    meth: { method: "DELETE", isArray: false, headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
  });
});