/**
 * Created by user on 27.07.15.
 */

angular.module('form', ['ui.router'])

.factory("Form", function($q) {
    var form = undefined;
    return {
        setCurrentForm: function(fr) {
            form = fr;
        },
        isDirty: function(){
            return form && form.item && form.item.$dirty;
        },
        clearForm: function() {
            form = undefined;
        },
        updateView: function() {
            if (form && form.item) {
                form.item.$setPristine();
            }
        },
        isValid: function() {
            return form && form.item && form.item.$valid;
        },
        isSubmitted: function() {
            return form && form.item && form.item.$submitted;
        },
        setSubmitted: function() {
            form.item.$setSubmitted();
        },

        getForm: function() {
            return form;
        }
    }
})
.run(function($rootScope, $state, Form) {
    $rootScope.$on('$stateChangeStart', function(event, toState, toStateParams) {
        // if the principal is resolved, do an authorization check immediately. otherwise,
        // it'll be done when the state it resolved.
        if(Form.isDirty()) {
            event.preventDefault();
            if (confirm("Данные, которые Вы указали в формах, не будут сохранены. Вы хотите перейти?", "Вы собираетесь покинуть страницу.")) {
                Form.clearForm();
                $state.go(toState.name, toStateParams);
            }
        } else {
            Form.clearForm();
        }
    });
});