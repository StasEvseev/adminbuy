app.factory("{{ table_id }}RES_GET", function($resource, Base64) {
  return $resource("{{ url_get }}", {id: "@id"}, {
    meth: { method: "GET", isArray: false, headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
  });
})