
app.factory("{{ modal_cntr }}RES_CREATE", function($resource, Base64) {
  return $resource("{{ url_create }}", {}, {
    meth: { method: "PUT", isArray: false , headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
  });
})

.factory("{{ modal_cntr }}RES_GETALL", function($resource, Base64) {
  return $resource("{{ url_getall }}", {}, {
    meth: { method: "GET", isArray: false, headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
  });
})

.factory("{{ modal_cntr }}RES_GET", function($resource, Base64) {
  return $resource("{{ url_get }}", {id: "@id"}, {
    meth: { method: "GET", isArray: false, headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
  });
})

.factory("{{ modal_cntr }}RES_UPDATE", function($resource, Base64) {
  return $resource("{{ url_update }}", {id: "@id"}, {
    meth: { method: "POST", isArray: false, headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
  });
})

.factory("{{ modal_cntr }}RES_DELETE", function($resource, Base64) {
  return $resource("{{ url_delete }}", {id: "@id"}, {
    meth: { method: "DELETE", isArray: false, headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
  });
});

{{ table_res|safe }}

{% block extend %}
{% endblock %}