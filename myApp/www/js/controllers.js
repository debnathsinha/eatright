angular.module('starter.controllers', [])

.controller('ChatsCtrl', function($scope, Chats) {
  // With the new view caching in Ionic, Controllers are only called
  // when they are recreated or on app start, instead of every page change.
  // To listen for when this page is active (for example, to refresh data),
  // listen for the $ionicView.enter event:
  //
  //$scope.$on('$ionicView.enter', function(e) {
  //});
  
  $scope.chats = Chats.all();
  $scope.remove = function(chat) {
    Chats.remove(chat);
  }
})

.controller('DishCtrl', function($scope, $http, Dishes) {
  
  $scope.takeoutMode = false;

  $scope.dishes = Dishes.all();
  $scope.remove = function(chat) {
    Dishes.remove(dish);
  };

  $scope.doRefresh = function() {
      $http.get('https://eat-right.appspot.com').then(function(resp) {
	  console.log('Success', resp);
	  // For JSON responses, resp.data contains the result
	  $scope.dishes = resp['data'];
      }, function(err) {
	  console.error('ERR', err);
	  // err.status will contain the status code
      })
	  .finally(function() {
	      $scope.$broadcast('scroll.refreshComplete');
	  });

  };

  $scope.selectDishMode = function(mode) {
      if (mode === 0) {
	  $scope.takeoutMode = false;
      } else {
	  $scope.takeoutMode = true;
      }
  };
  
})

.controller('DishDetailCtrl', function($scope, $stateParams, Dishes) {
    console.log($stateParams.dishId);
  $scope.dish = Dishes.get($stateParams.dishId);
})

.controller('ChatDetailCtrl', function($scope, $stateParams, Chats) {
  $scope.chat = Chats.get($stateParams.chatId);
})

.controller('AnalyticsCtrl', function($scope) {
    $scope.monthlyChartSelected = false;
    $scope.selectTimePeriod = function(timePeriodEnum) {
	if (timePeriodEnum === 0) {
	    $scope.dailyChartSelected = true;
	    $scope.weeklyChartSelected = false;
	    $scope.monthlyChartSelected = false;
	    // Daily
	    $scope.chart = {
		labels : ["Breakfast", "Lunch", "Dinner"],
		datasets : [
		    {
			fillColor : "rgba(151,187,205,0)",
			strokeColor : "#e67e22",
			pointColor : "rgba(151,187,205,0)",
			pointStrokeColor : "#e67e22",
			data : [4, 3, 5]
		    },
		    {
			fillColor : "rgba(151,187,205,0)",
			strokeColor : "#f1c40f",
			pointColor : "rgba(151,187,205,0)",
			pointStrokeColor : "#f1c40f",
			data : [8, 3, 2]
		    }
		], 
	    };
	    $scope.myChartData = [
		{
		    value: 30,
		    color:"#F7464A"
		},
		{
		    value : 50,
		    color : "#E2EAE9"
		},
		{
		    value : 100,
		    color : "#D4CCC5"
		},
		{
		    value : 40,
		    color : "#949FB1"
		},
		{
		    value : 120,
		    color : "#4D5360"
		}
	    ];
	    $scope.options = {}
	    $scope.options['percentageInnerCutout'] = 90;
	    // var canvas = angular.element(document.querySelector( "#dailyChart" ) );
	    // var width = canvas.getContext("2d").canvas.style["width"];
	    // width = parseInt(width.substring(0,width.length-2));
	    // var height = canvas.getContext("2d").canvas.style["height"];
	    // height = parseInt(height.substring(0,height.length - 2));
	    // canvas.getContext("2d").fillText(3 + "%", width/2, height/2);
	} else if (timePeriodEnum === 1) {
	    $scope.dailyChartSelected = false;
	    $scope.weeklyChartSelected = true;
	    $scope.monthlyChartSelected = false;
	    $scope.chart = {
		labels : ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
		datasets : [
		    {
			fillColor : "rgba(151,187,205,0)",
			strokeColor : "#e67e22",
			pointColor : "rgba(151,187,205,0)",
			pointStrokeColor : "#e67e22",
			data : [4, 3, 5, 4, 6]
		    },
		    {
			fillColor : "rgba(151,187,205,0)",
			strokeColor : "#f1c40f",
			pointColor : "rgba(151,187,205,0)",
			pointStrokeColor : "#f1c40f",
			data : [8, 3, 2, 5, 4]
		    }
		], 
	    };
	} else {
	    $scope.dailyChartSelected = false;
	    $scope.weeklyChartSelected = false;
	    $scope.monthlyChartSelected = true;
	    $scope.chart = {
		labels : ["Week 1", "Week 2", "Week 3", "Week 4"],
		datasets : [
		    {
			fillColor : "rgba(151,187,205,0)",
			strokeColor : "#e67e22",
			pointColor : "rgba(151,187,205,0)",
			pointStrokeColor : "#e67e22",
			data : [4, 3, 5, 4]
		    }
		], 
	    };
	}
    }
    $scope.selectTimePeriod(0);
})

.controller('AccountCtrl', function($scope) {
    $scope.settings = {
	enableFriends: true
    };
    
})

.controller('OrderCtrl', function($scope) {
    $scope.freshorders = [
	{
	    name: 'Chicken Pizza',
	    qty: '2',
	},
	{
	    name: 'Rice Bowl',
	    qty: '2',
	    expires: '17d'
	}
    ];
    $scope.usesoonorders = [
	{
	    name: 'Spinach Pesto',
	    qty: '2',
	    expires: '5d'
	},
	{
	    name: 'Baklava',
	    qty: '2',
	    expires: '5d'
	}
    ];
    $scope.usenoworders = [
	{
	    name: 'Sour Cream',
	    qty: '2',
	    expires: '2d'
	},
	{
	    name: 'Pork Chops',
	    qty: '2',
	    expires: '1d'
	}
    ];

    $scope.reduceQty = function(order) {
	console.log("Reducing qty");
	console.log(order);
	order.qty = parseInt(order.qty) - 1;
    }
    $scope.increaseQty = function(order) {
	console.log("Increasing qty");
	console.log(order);
	order.qty = parseInt(order.qty) + 1;
    }
})

.controller('FirstTimeCtrl', ['$scope', '$state',  function($scope, $state) {
  
   $scope.endSlideShow = function() {
     window.localStorage['firstTimeUse'] = 'no';
     $state.go("tab.dish");  
   }
  
}]);
