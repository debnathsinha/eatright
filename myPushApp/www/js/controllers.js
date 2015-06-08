angular.module('starter.controllers', [])

.controller('AppCtrl', function($scope, $rootScope, $ionicPush, $ionicUser) {
  $rootScope.$on('$cordovaPush:tokenReceived', function(event, data) {
    console.log('Got token', data.token, data.platform);
  });
  //Basic registration
  $scope.pushRegister = function() {
    alert('Registering...');

    $ionicPush.register({
      canShowAlert: false,
      onNotification: function(notification) {
        // Called for each notification for custom handling
        $scope.lastNotification = JSON.stringify(notification);
      }
    }).then(function(deviceToken) {
      $scope.token = deviceToken;
    });
  }
  $scope.identifyUser = function() {
    alert('Identifying');
    console.log('Identifying user');

    var user = $ionicUser.get();
    if(!user.user_id) {
      // Set your user_id here, or generate a random one
      user.user_id = $ionicUser.generateGUID()
    };

    angular.extend(user, {
      name: 'Test User',
      message: 'I come from planet Ion'
    });

    $ionicUser.identify(user);
    
  }
})

