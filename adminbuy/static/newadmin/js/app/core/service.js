/**
 * Created by user on 04.08.15.
 */

angular.module('core.service', ['core.utils'])
.factory('BaseModelService', function(remoteHelper, $q) {

    return {
        cnt: 0,
        _getPath: function() {
            return "";
        },
        _setCount: function(count) {
            this.cnt = count;
        },
        filter: function(text, page, count) {
            var self = this;
            var params = remoteHelper.createParams(text, undefined, page, count);
            return remoteHelper.filterItems(self._getPath(), params).then(function(resp) {
                self._setCount(resp.data.max);
                return resp;
            });
        },
        count: function() {
            return this.cnt;
        },
        getById: function(id) {
            return remoteHelper.itemById(this._getPath(), id);
        },

        getByIds: function(ids) {
            return remoteHelper.itemsByIds(this._getPath(), ids);
        },

        update: function(id, params) {
            var q = $q.defer();
            remoteHelper.update(this._getPath(), id, params).then(function(resp) {q.resolve(resp);}, function(resp) {
                toastr.error(resp.data.message, "Ошибка при редактировании записи!");
                q.reject();
            });
            return q.promise;
        },
        create: function(params) {
            var q = $q.defer();
            remoteHelper.create(this._getPath(), params).then(function(resp) {q.resolve(resp);}, function(resp) {
                toastr.error(resp.data.message, "Ошибка при создании записи!");
                q.reject();
            });
            return q.promise;
        },
        delete_: function(id) {
            var q = $q.defer();
            remoteHelper.delete_(this._getPath(), id).then(function(resp) {q.resolve(resp);}, function(resp) {
                toastr.error(resp.data.message, "Ошибка при удалении записи!");
                q.reject();
            });
            return q.promise;
        }
    }
})
.factory("BaseDictService", function($controller) {
    var ser = {
        records: function() {
            return [];
        },

        formInclude: function() {
            return "";
        },

        title: function(){
            return "I'm a modal!";
        },

        titleEdit: function() {
            return "Edit modal!";
        },

        controller: function() {
            return function ($scope, $modalInstance) {
                $scope.cancel = function() {
                    $modalInstance.dismiss('cancel');
                };

                $scope.ok = function() {
                    console.log("CONTROLLER CREATE!!");
                };
            }
        },

        controllerEdit: function() {
            return function($scope, $modalInstance, item) {
                $controller(ser.controller(), {$scope: $scope, $modalInstance: $modalInstance});
                $scope.ok = function() {
                    console.log("CONTROLLER EDIT!!");
                };

                $scope.model = item;
            }
        },

        resolve: function() {
            return {

            }
        },

        resolveEdit: function() {
            return {

            }
        },

        template: function() {
            return '<div class="modal-header">' +
                   '<h3 class="modal-title">' + this.title() + '</h3>' +
                   '</div>' +
                   '<div class="modal-body">' +
                   '<div ng-include="\'' + this.formInclude() + '\'">' +
                   '</div>' +
                   '</div>' +
                   '<div class="modal-footer">' +
                   '<button class="btn btn-flat btn-primary" ng-click="ok()">Сохранить</button>' +
                   '<button class="btn btn-flat btn-warning" ng-click="cancel()">Закрыть</button>' +
                   '</div>';
        },

        templateEdit: function() {
            return '<div class="modal-header">' +
                   '<h3 class="modal-title">' + this.titleEdit() + '</h3>' +
                   '</div>' +
                   '<div class="modal-body">' +
                   '<div ng-include="\'' + this.formInclude() + '\'">' +
                   '</div>' +
                   '</div>' +
                   '<div class="modal-footer">' +
                   '<button class="btn btn-flat btn-primary" ng-click="ok()">Изменить</button>' +
                   '<button class="btn btn-flat btn-warning" ng-click="cancel()">Закрыть</button>' +
                   '</div>';
        },

        size: function() {
            return 'lg';
        }
    };

    return ser;
});
