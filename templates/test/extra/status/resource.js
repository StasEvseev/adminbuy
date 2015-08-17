app.factory("{{ name }}RES_STATUS", function($resource, Base64) {
  return $resource("{{ url }}", {id: "@id"}, {
    meth: { method: "POST", isArray: false , headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
  });
})