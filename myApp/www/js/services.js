angular.module('starter.services', [])

.factory('Chats', function() {
  // Might use a resource here that returns a JSON array

  // Some fake testing data
  var chats = [{
    id: 0,
    name: 'Ben Sparrow',
    lastText: 'You on your way?',
    face: 'https://pbs.twimg.com/profile_images/514549811765211136/9SgAuHeY.png'
  }, {
    id: 1,
    name: 'Max Lynx',
    lastText: 'Hey, it\'s me',
    face: 'https://avatars3.githubusercontent.com/u/11214?v=3&s=460'
  },{
    id: 2,
    name: 'Adam Bradleyson',
    lastText: 'I should buy a boat',
    face: 'https://pbs.twimg.com/profile_images/479090794058379264/84TKj_qa.jpeg'
  }, {
    id: 3,
    name: 'Perry Governor',
    lastText: 'Look at my mukluks!',
    face: 'https://pbs.twimg.com/profile_images/598205061232103424/3j5HUXMY.png'
  }, {
    id: 4,
    name: 'Mike Harrington',
    lastText: 'This is wicked good ice cream.',
    face: 'https://pbs.twimg.com/profile_images/578237281384841216/R3ae1n61.png'
  }];

  return {
    all: function() {
      return chats;
    },
    remove: function(chat) {
      chats.splice(chats.indexOf(chat), 1);
    },
    get: function(chatId) {
      for (var i = 0; i < chats.length; i++) {
        if (chats[i].id === parseInt(chatId)) {
          return chats[i];
        }
      }
      return null;
    }
  };
})

.directive('backImg', function(){
    return function(scope, element, attrs){
        var url = attrs.backImg;
        var content = element.find('a');
        content.css({
            'background': 'url(' + url +')',
            'background-size' : 'cover',
	    'line-height' : '15vh'
        });
    };
})

.factory('Dishes', function() {
    var dishes = [{
	id: 1,
	name: 'Stovetop Lasagna',
	lastText: 'Cook the noodles and sauce on the stovetop, then assemble and broil it for three to give minutes until the cheese is golden and bubbling',
	thumbnail_img: 'http://foodnetwork.sndimg.com/content/dam/images/food/fullset/2012/7/25/2/FNM_090112-Weeknight-Lasagna-Dinner-Recipe_s4x3.jpg'
        },{
	id: 2,
	name: 'Chicken Spaghetti',
	lastText: "With spaghetti and mushroom sauce, and light and dark meat chicken with bell peppers, Ree Drummond's casserole is like two meals in one. Cooking the spaghetti in the same liquid as the chicken infuses it with flavor, and the Cheddar thickens the sauce so it coats each piece of meat.",
	thumbnail_img: 'http://foodnetwork.sndimg.com/content/dam/images/food/fullset/2013/9/12/1/FN_Ree-Drummond-Chicken-Spaghetti_s4x3.jpg'
        },{
	id: 3,
	name: 'Spanish Chicken & Potato Roast',
	lastText: 'Neat dish!',
	thumbnail_img: 'http://foodnetwork.sndimg.com/content/dam/images/food/fullset/2012/1/24/3/FNM_030112-WNDinners-048_s4x3.jpg'
        },{
	id: 4,
	name: "30 minute Shepherd's Pie",
	lastText: 'Neat dish!',
	thumbnail_img: 'http://foodnetwork.sndimg.com/content/dam/images/food/fullset/2003/10/28/3/tm1c19_shepherds_pie.jpg'
        },{
	id: 5,
	name: 'Beef & Cheddar Casserole',
	lastText: 'Neat dish!',
	thumbnail_img: 'http://foodnetwork.sndimg.com/content/dam/images/food/fullset/2012/12/19/0/FNK_Beef-and-Cheddar-Casserole_s4x3.jpg'
        },{
	id: 6,
	name: 'Chicken Tortilla Casserole',
	lastText: 'Neat dish!',
	thumbnail_img: 'http://foodnetwork.sndimg.com/content/dam/images/food/fullset/2013/7/11/0/YW0305H_chicken-tortilla-casserole-recipe_s4x3.jpg.rend.sni12col.landscape.jpeg'
        },{
	id: 7,
	name: 'Salmon Cakes with Salad',
	lastText: 'Neat dish!',
	thumbnail_img: 'http://foodnetwork.sndimg.com/content/dam/images/food/fullset/2012/11/13/6/FNM_120112-Salmon-Cakes-With-Salad-Recipe_s4x3.jpg'
        },{
	id: 8,
	name: 'Roasted Tomato Bisque',
	lastText: 'Neat dish!',
	thumbnail_img: 'http://foodnetwork.sndimg.com/content/dam/images/food/fullset/2012/2/24/1/ZB0202H_roasted-tomato-bisque_s4x3.jpg'
        },{
	id: 9,
	name: 'Pork Chops with Roasted Kale & Walnut Pesto',
	lastText: 'Neat dish!',
	thumbnail_img: 'http://foodnetwork.sndimg.com/content/dam/images/food/fullset/2012/12/19/0/FNK_Pork-Chops-With-Kale-Pesto_s4x3.jpg.rend.sni12col.landscape.jpeg'
        },{
	id: 10,
	name: 'Spicy Turkey and Green Bean Stir-Fry',
	lastText: 'Neat dish!',
	thumbnail_img: 'http://foodnetwork.sndimg.com/content/dam/images/food/fullset/2012/11/13/6/FNM_120112-Spicy-Turkey-and-Green-Bean-Stir-Fry-Recipe_s4x3.jpg'
	}];

    return {
	all: function() {
	    return dishes;
	},
	remove: function(dish) {
	    dishes.splice(dishes.indexOf(dish), 1);
	},
	get: function(dishId) {
	    for (var i = 0; i < dishes.length; i++) {
		if (dishes[i].id == dishId) {
		    return dishes[i];
		}
	    }
	    return null;
	},
    }
});
