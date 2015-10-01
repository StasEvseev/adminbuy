/**
 * Created by user on 20.08.15.
 */

angular.module("mails.module", ['ui.router'])
.config(function($stateProvider) {
     $stateProvider.state('index.mailbox', {
            data: {
                 roles: ['user']
            },
            abstract: true,
            url: "/mailbox",
            views: {
                'content': {
                    templateUrl: "static/newadmin/app/mail/template/base.html"
                }
            }
        })

        .state('index.mailbox.list', {
            url: "?_new&filter&page",
            views: {
                'head': {
                    templateUrl: "static/newadmin/app/mail/template/list.head.html",
                    controller: "MailListController"
                },
                'item': {
                    templateUrl: "static/newadmin/app/mail/template/list.html",
                    controller: "MailListController"
                }
            },
            resolve: {
                mailitems: ['mails', '$stateParams',
                    function (mails, $stateParams) {
                        return mails.filterToStateParams($stateParams);
                    }]
            }
        })

        .state('index.mailbox.list.read', {
            url: "/{mailId:[0-9]{1,10}}",

            resolve: {
                item: function ($stateParams, mails) {
                    return mails.getById(parseInt($stateParams.mailId));
                }
            },
            views: {
                'head@index.mailbox': {
                    templateUrl: "static/newadmin/app/mail/template/read.head.html",
                    controller: function ($scope, item, mails) {
                        $scope.item = item;
                    }
                },
                '': {
                    templateUrl: "static/newadmin/app/mail/template/read.html",
                    controller: function ($scope, $stateParams, $state, item, mails, mailLoading) {
                        mails.setCurrent(item);
                        $scope.item = item;

                        $scope.loading = mailLoading;

                        $scope.hasNext = mails.hasNext;
                        $scope.hasPrev = mails.hasPrev;

                        $scope.rashod = function(event, index) {
                            showSpinner();
//                            var btn = $(event.target);
//                            btn.button('loading');

                            mails.handle_mail($scope.item.id, index, 'R').then(function(data) {
                                $state.go('index.invoice.view', {id: data.data.invoice_id}).then(function() {
                                    hideSpinner();
                                });
                            }).catch(function() {
                                showError("Не удалось обработать накладную как расход. Обратитесь к администратору.");
                            });
                        };

                        $scope.prev = function() {
                            if (mails.hasPrev()) {
                                showSpinner();
                                $state.go('index.mailbox.list.read', {mailId: mails.getPrev()}).then(function() {
                                    hideSpinner();
                                });
                            }
                        };

                        $scope.next = function() {
                            if (mails.hasNext()) {
                                showSpinner();
                                $state.go('index.mailbox.list.read', {mailId: mails.getNext()}).then(function() {
                                    hideSpinner();
                                });
                            }
                        };

                        function showError(message) {
                            toastr.error(message, "Ошибка!");
                            $scope.loading.listLoading = false;
                        }

                        function showSpinner() {
                            $scope.loading.listLoading = false;
                        }

                        function hideSpinner() {
                            $scope.loading.listLoading = true;
                        }
                    }
                }
            }

        });
})
.value("mailLoading", {
    listLoading: true
})
.factory('MailItems', function() {
    var items = [];
    return {
        setItems: function(itms) {
            items = itms;
        },
        getItems: function() {
            return items;
        }
    }
})
.controller("MailListController", function ($scope, $state, $timeout, mailitems, mailLoading, MailItems, mails, $stateParams) {

        $scope.loading = mailLoading;
        $scope.mailitems = MailItems;
        hideSpinner();

        $scope.page = 1;
        $scope.countPerPage = 10;

        setItems(mailitems);

        $scope.checkMail = function ($event) {
            var button = $event.target;
            disableButton(button, true);
            showSpinner();
            mails.checkMail().then(function(res) {
                disableButton(button, false);
                mails.filterToStateParams($stateParams).then(function(items) {

                    setItems(items);

                    disableButton(button, false);
                    hideSpinner();
                    if(res == "ok") {
                        toastr.info("Есть новые письма. Для просмотра перейдите по <a href='/admin#/mailbox?_new=true&page=1'>ссылке</a>", "Оповещения");
                    } else if (res == "nothing") {
                        toastr.info("Нету новых писем", "Оповещения");
                    }
                }).catch(function() {
                    showError("Не удалось загрузить письма. Обратитесь к администратору.")
                });
            }).catch(function() {
                showError("Не удалось проверить почту. Обратитесь к администратору.");
                disableButton(button, false);
            });
        };

        if ($stateParams.filter) {
            $scope.searchText = $stateParams.filter;
        }
        if ($stateParams.page) {
            $scope.page = parseInt($stateParams.page);
        }

        $scope.boxTitle = $stateParams._new === "true" ? "Новые" : "Inbox";

        $scope.next = function () {
            if ($scope.hasNext()) {
                showSpinner();
                $state.go('index.mailbox.list', {filter: $scope.searchText, page: $scope.page + 1});
            }
        };

        $scope.prev = function () {
            if ($scope.hasPrev()) {
                showSpinner();
                $state.go('index.mailbox.list', {filter: $scope.searchText, page: $scope.page - 1});
            }
        };

        $scope.hasPrev = function () {
            return $scope.page > 1;
        };

        $scope.hasNext = function () {
            return $scope.page < mails.count() / $scope.countPerPage;
        };

        $scope.filter = function (text) {
            showSpinner();
            $state.go('index.mailbox.list', {filter: text, page: 1});
        };

        $scope.count = function () {
            return mails.count();
        };

        $scope.countNew = function () {
            return mails.countNew();
        };

        $scope.countNewM = function () {
            return mails.countNew();
        };

        function disableButton(element, comp) {
            $(element).prop('disabled', comp);
        }

        function showError(message) {
            toastr.error(message, "Ошибка!");
            hideSpinner();
        }

        function setItems(items) {
            $scope.mailitems.setItems(items);
        }

        function showSpinner() {
            $scope.loading.listLoading = false;
        }

        function hideSpinner() {
            $scope.loading.listLoading = true;
        }
    }
);