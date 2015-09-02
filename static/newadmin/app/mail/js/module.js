/**
 * Created by user on 20.08.15.
 */

angular.module("mails.module", ['ui.router'])
.config(function($stateProvider) {
     $stateProvider.state('index.mailbox', {
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
                        return mails.filter($stateParams.filter, $stateParams.page, $stateParams.count, $stateParams._new);
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
                    controller: function ($scope, $stateParams, $state, item, mails) {
                        mails.setCurrent(item);
                        $scope.item = item;

                        $scope.hasNext = mails.hasNext;
                        $scope.hasPrev = mails.hasPrev;

                        $scope.rashod = function(event, index) {
                            $scope.loadingFinish = false;
                            var btn = $(event.target);
//                            btn.button('loading');

                            mails.handle_mail($scope.item.id, index, 'R').then(function(data) {
                                $state.go('index.invoice.view', {id: data.data.invoice_id}).then(function() {
                                    $scope.loadingFinish = true;
                                });
                            }, function() {
                                debugger
                            });
                        };

                        $scope.prev = function() {
                            if (mails.hasPrev()) {
                                $scope.loadingFinish = false;
                                $state.go('index.mailbox.list.read', {mailId: mails.getPrev()});
                            }
                        };

                        $scope.next = function() {
                            if (mails.hasNext()) {
                                $scope.loadingFinish = false;
                                $state.go('index.mailbox.list.read', {mailId: mails.getNext()});
                            }
                        };


                    }
                }
            }

        })

//        .state('index.mail_invoice_in', {
//            url: "/mailbox/invoice_in/{mailId:[0-9]{1,10}}",
//            resolve: {
//                item: function ($stateParams, mails) {
//                    return mails.getById(parseInt($stateParams.mailId));
//                },
//                items: function($stateParams, mails) {
//                    return mails.getRowInvoiceIn(parseInt($stateParams.mailId));
//                }
//            },
//            views: {
//                'content': {
//                    templateUrl: "static/newadmin/app/mail/template/mailinvoice.html",
//                    controller: "MailInvoiceCntrl"
//                }
//            }
//        })
     ;
})

.controller("MailListController", function ($scope, $state, mailitems, mails, $stateParams) {

        hideSpinner();

        $scope.page = 1;
        $scope.countPerPage = 10;
        $scope.items = mailitems;
        $scope.checkMail = function () {
            console.log("CHECK MAIL");
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

        function showSpinner() {
            $scope.loadingFinish = false;
        }

        function hideSpinner() {
            $scope.loadingFinish = true;
        }
    }
);