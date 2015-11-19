{% extends "test/modals/resource.js" %}

{% block extend %}
{% for _import in imports %}
    {{ _import.render_resource()|safe }}
{% endfor %}
{% endblock %}