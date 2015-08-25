/**
 * Created by user on 31.07.15.
 */

angular.module('filters', [])
.filter('range', function() {
  return function(input, total) {
    total = parseInt(total);
    for (var i=0; i<total; i++)
      input.push(i);
    return input;
  };
})
.filter('yesNo', function() {
    return function(input) {
        return input ? 'Да' : 'Нет';
    }
})

.filter('rub', function() {
  return function(input) {
      if (_.isNaN(input)) {
          return "";
      }
      else if (_.isNull(input)) {
          return "";
      }
      else if (_.isUndefined(input)) {
          return "";
      }
      else if (input == "") {
          return "";
      }
       else {
          return parseFloat(input).toFixed(2) + "<span class=\"min-spn\"> руб.</span>";
      }
      //return input;
  };
})

.filter('propsFilter', function() {
    return function(items, props) {
        var out = [];

        if (angular.isArray(items)) {
          items.forEach(function(item) {
            var itemMatches = false;

            var keys = Object.keys(props);
            for (var i = 0; i < keys.length; i++) {
              var prop = keys[i];
              var text = props[prop].toLowerCase();
              if (item[prop].toString().toLowerCase().indexOf(text) !== -1) {
                itemMatches = true;
                break;
              }
            }

            if (itemMatches) {
              out.push(item);
            }
          });
        } else {
          // Let the output be the input untouched
          out = items;
        }

        return out;
    }
});