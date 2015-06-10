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
	lastText: ['(1) Preheat the broiler. Fill a wide pot with 3 inches of salted water and bring to a boil.', '(2) Add the noodles and cook until al dente, about 11 minutes, then drain, transfer to a cutting board and halve crosswise.', '(3) Meanwhile, heat the olive oil in a large skillet over medium-high heat.', '(4) Add the ground meat and cook, stirring, until browned.', '(5) Add the tomato sauce and red pepper flakes and simmer 5 minutes.', '(6) Add the spinach and stir until it wilts, then add the ricotta and bring to a low simmer.', '(7) Season with salt and remove from the heat. Toss the mozzarella and 4 tablespoons parmesan in a bowl.', '(8) Cover the bottom of an 8-inch-square baking dish with a layer of slightly overlapping lasagna noodles.', '(9) Top with half of the meat sauce and half of the cheese mixture.', '(10) Repeat with another layer of noodles and the remaining meat sauce and cheese mixture.', '(11) Cover with the remaining noodles and sprinkle with the remaining 2 tablespoons parmesan.', '(12) Drizzle lightly with olive oil and broil until golden and bubbling, 3 to 5 minutes.', '(14) Top with the basil.', '(15) Read more at: http://www.foodnetwork.com/recipes/food-network-kitchens/stovetop-lasagna-recipe.html?oc=linkback'],
	thumbnail_img: 'http://eat-right.appspot.com/assets/img/spanish-chicken-overlay.png'
        },{
	id: 2,
	name: 'Chicken Spaghetti',
	lastText: ["(1) Preheat the oven to 350 degrees F.", "(2) Bring a large pot of water to a boil.", "(3) Add the chicken pieces to the boiling water and boil for a few minutes, and then turn the heat to medium-low and simmer, 30 to 45 minutes.", "(4) Remove the chicken and 2 cups of the chicken cooking broth from the pot.", "(5) When the chicken is cool, remove the skin and pick out the meat (a mix of dark and white) to make 2 generous cups.", "(6) Discard the bones and skin.", "(7) Cook the spaghetti in the chicken cooking broth until al dente.", "(8) Do not overcook. When the spaghetti is cooked, combine with the chicken, 1 1/2 cups of the cheese, the green peppers, red peppers, seasoned salt, cayenne, soup and onions, and sprinkle with salt and pepper.", "(9) Stir in 1 cup of the reserved chicken cooking broth, adding an additional cup if needed.", "(10) Place the mixture in a 9- by 13-inch casserole pan and top with the remaining 1 cup cheese.", "(11) Bake immediately until bubbly, about 45 minutes. (If the cheese on top starts to get too dark, cover with foil.)", "(12) 2012 Ree Drummond, All Rights Reserved", "(13) Read more at: http://www.foodnetwork.com/recipes/ree-drummond/chicken-spaghetti-recipe.html?oc=linkback"],
	thumbnail_img: 'http://foodnetwork.sndimg.com/content/dam/images/food/fullset/2013/9/12/1/FN_Ree-Drummond-Chicken-Spaghetti_s4x3.jpg'
        },{
	id: 3,
	name: 'Spanish Chicken & Potato Roast',
	lastText: ["(1) Position a rack in the upper third of the oven.", "(2) Place a large cast-iron baking dish or a rimmed baking sheet on the rack and preheat to 500 degrees F.", "(3) Put the potatoes, garlic, olive oil, 1 tablespoon water and 1/2 teaspoon salt in a large microwave-safe baking dish and toss to coat.", "(4) Cover with plastic wrap, pierce the plastic in a few places with a knife and microwave 8 minutes to partially cook.", "(5) Meanwhile, pat the chicken dry and transfer to a bowl.", "(6) Sprinkle with the paprika, 1 teaspoon salt and 1/2 teaspoon pepper.", "(7) Add 2 tablespoons parsley and the lemon juice; toss to coat. Set aside.", "(8) Remove the hot baking dish from the oven; carefully add the potatoes and spread in an even layer.", "(9) Scatter the onions on top. Roast until the potatoes start to brown, about 12 minutes.", "(10) Flip the potatoes and lay the chicken pieces on top, adding any accumulated juices from the bowl; return to the oven and roast until the potatoes are tender and the chicken is cooked through, about 12 more minutes.", "(11) Remove from the oven and top with the remaining 2 tablespoons parsley.", "(12) Serve with the lemon wedges.", "(13) Read more at: http://www.foodnetwork.com/recipes/food-network-kitchens/spanish-chicken-and-potato-roast-recipe.html?ic1=obinsite&oc=linkback"],
	thumbnail_img: 'http://foodnetwork.sndimg.com/content/dam/images/food/fullset/2012/1/24/3/FNM_030112-WNDinners-048_s4x3.jpg'
        },{
	id: 4,
	name: "30 minute Shepherd's Pie",
	lastText: ["(1) Boil potatoes in salted water until tender, about 12 minutes.", "(2) Drain potatoes and pour them into a bowl.", "(3) Combine sour cream, egg yolk and cream.", "(4) Add the cream mixture into potatoes and mash until potatoes are almost smooth.", "(5) While potatoes boil, preheat a large skillet over medium high heat.", "(6) Add oil to hot pan with beef or lamb.", "(7) Season meat with salt and pepper.", "(8) Brown and crumble meat for 3 or 4 minutes. If you are using lamb and the pan is fatty, spoon away some of the drippings.", "(9) Add chopped carrot and onion to the meat.", "(10) Cook veggies with meat 5 minutes, stirring frequently.", "(11) In a second small skillet over medium heat cook butter and flour together 2 minutes.", "(12) Whisk in broth and Worcestershire sauce.", "(13) Thicken gravy 1 minute.", "(14) Add gravy to meat and vegetables. Stir in peas.", "(15) Preheat broiler to high.", "(16) Fill a small rectangular casserole with meat and vegetable mixture.", "(17) Spoon potatoes over meat evenly.", "(18) Top potatoes with paprika and broil 6 to 8 inches from the heat until potatoes are evenly browned.", "(19) Top casserole dish with chopped parsley and serve.", "(20) Recipe courtesy of Rachael Ray", "(21) Read more at: http://www.foodnetwork.com/recipes/rachael-ray/30-minute-shepherds-pie-recipe.html?ic1=obinsite&oc=linkback"],
	thumbnail_img: 'http://foodnetwork.sndimg.com/content/dam/images/food/fullset/2003/10/28/3/tm1c19_shepherds_pie.jpg'
        },{
	id: 5,
	name: 'Salmon Cakes with Salad',
	lastText: ["(1) Preheat the oven to 400 degrees F.", "(2) Mix the salmon, corn, egg, 3 tablespoons each breadcrumbs and tartar sauce, the roasted red peppers, parsley, lemon zest and 3/4 teaspoon Old Bay in a bowl.", "(3) Gently form into eight 3/4-inch-thick patties and freeze until just firm, about 5 minutes.", "(4) Meanwhile, make the dressing: Whisk the remaining 2 tablespoons tartar sauce, the lemon juice, 1 tablespoon water, the remaining 1/4 teaspoon Old Bay, and pepper to taste in a large bowl.", "(5) Put the remaining 5 tablespoons breadcrumbs in a shallow bowl.", "(6) Press the salmon cakes in the breadcrumbs to coat both sides.", "(7) Heat the olive oil in a large ovenproof nonstick skillet over medium-high heat.", "(8) Add the salmon cakes and cook until golden brown, 3 to 4 minutes per side.", "(9) Transfer the skillet to the oven and bake until the cakes are heated through, 6 to 8 more minutes.", "(10) Add the greens to the bowl with the dressing and toss.", "(11) Serve the salmon cakes with the salad, more tartar sauce and lemon wedges.", "(12) Read more at: http://www.foodnetwork.com/recipes/food-network-kitchens/salmon-cakes-with-salad-recipe.html?oc=linkback"],
	thumbnail_img: 'http://foodnetwork.sndimg.com/content/dam/images/food/fullset/2012/11/13/6/FNM_120112-Salmon-Cakes-With-Salad-Recipe_s4x3.jpg'
        },{
	id: 6,
	name: 'Spicy Turkey and Green Bean Stir-Fry',
	lastText: ["(1) Bring a large pot of water to a boil.", "(2) Stir in the rice, cover and boil until tender, about 18 minutes; drain well and keep warm.", "(3) Meanwhile, preheat the broiler. Toss the green beans, 1 1/2 tablespoons vegetable oil and the sugar on a rimmed baking sheet.", "(4) Broil, stirring once, until the beans are tender and charred, about 8 minutes.", "(5) Heat the remaining 1 1/2 tablespoons vegetable oil in a large skillet over high heat.", "(6) Add the turkey and cook, breaking it up with a wooden spoon, until browned, 3 minutes.", "(7) Add the garlic, pickle and chile paste and cook until the garlic is slightly golden, about 3 minutes.", "(8) Whisk the chicken broth, soy sauce, sherry and cornstarch in a bowl.", "(9) Add the green beans to the skillet with the turkey mixture and cook, stirring, 1 minute.", "(10) Add the soy sauce mixture and cook, stirring occasionally, until the sauce thickens slightly, about 3 minutes.", "(11) Serve with the rice.", "(12) Photograph by Christopher Testani", "(13) Recipe courtesy Food Network Magazine", "(14) Read more at: http://www.foodnetwork.com/recipes/food-network-kitchens/spicy-turkey-and-green-bean-stir-fry-recipe.html?oc=linkback"],
	thumbnail_img: 'http://foodnetwork.sndimg.com/content/dam/images/food/fullset/2012/11/13/6/FNM_120112-Spicy-Turkey-and-Green-Bean-Stir-Fry-Recipe_s4x3.jpg'
	},{
	id: 7,
	name: 'Beef & Cheddar Casserole',
	lastText: ["(1) Preheat the oven to 425 degrees F.", "(2) Oil a 2-quart baking dish.", "(3) Bring a large pot of salted water to a boil.", "(4) Add the noodles and cook to al dente according to the package directions.", "(5) Drain and put in the prepared baking dish.", "(6) Toss with the sour cream, Parmesan and 1/4 teaspoon salt.", "(7) Meanwhile, heat the olive oil in a large skillet over medium-high heat.", "(8) Add the ground beef and cook, stirring, until no longer pink, about 4 minutes.", "(9) Add the bell peppers and scallions and cook until crisp-tender, about 3 minutes.", "(10) Make a space in the pan, add the tomato paste and toast for a minute.", "(11) Sprinkle with the Italian seasoning and 1/4 teaspoon salt.", "(12) Add the diced tomatoes, stir and bring to a simmer.", "(13) Cook until slightly thickened, about 2 minutes.", "(14) Pour the beef mixture over the noodles and sprinkle with the grated Cheddar.", "(15) Bake on the middle rack until the cheese is melted and the edges are bubbling, 15 to 20 minutes.", "(16) Let stand for 10 minutes before serving.", "(17) From Food Network Kitchens.", "(18) Read more at: http://www.foodnetwork.com/recipes/food-network-kitchens/beef-and-cheddar-casserole-recipe.html?ic1=obinsite&oc=linkback"],
	thumbnail_img: 'http://foodnetwork.sndimg.com/content/dam/images/food/fullset/2012/12/19/0/FNK_Beef-and-Cheddar-Casserole_s4x3.jpg'
        },{
	id: 8,
	name: 'Chicken Tortilla Casserole',
	lastText: ["(1) Add the chicken to a large stockpot, cover with water and add a large pinch of salt.", "(2) Bring to a boil and cook until tender, about 30 minutes.", "(3) Remove the chicken from the pot and set aside to cool.", "(4) When cool enough to handle, shred the chicken and set aside.", "(5) Reserve 3 1/3 cups of the broth", "(1 cup is for the chicken gravy, supplement with boxed stock if you don't have enough.)", "(6) Preheat the oven to 350 degrees F. Spray a 13- by 9-inch baking dish with cooking spray.", "(7) In a large saucepan, combine 2 1/3 cups of the reserved broth, the Chicken Gravy, green chiles, onions, garlic, sour cream, cumin, salt and pepper.", "(8) Bring the mixture to a boil, stirring constantly.", "(9) Remove from the heat.", "(10) Spread 1 cup of the mixture into the prepared baking dish.", "(11) Arrange a layer of 6 tortillas over the mixture, and then top with 1 cup shredded chicken and 1/2 cup of the Cheddar.", "(12) Repeat this layer three more times, ending with cheese.", "(13) Spread any remaining mixture over the cheese.", "(14) Make sure all of the tortillas are covered or they will get very hard during baking.", "(15) Bake uncovered for 30 minutes.", "(16) **Chicken Gravy:**", "(17) Melt the butter in a medium saucepan and whisk in the flour to make a roux.", "(18) Cook over medium heat, whisking constantly, until the mixture bubbles and the flour turns light brown in color.", "(19) Gradually whisk in the stock and milk and continue to stir while cooking over medium heat.", "(20) When the mixture thickens, after about 5 minutes, whisk in some salt and pepper.", "(21) Recipe courtesy Trisha Yearwood", "(22) Read more at: http://www.foodnetwork.com/recipes/trisha-yearwood/chicken-tortilla-casserole-recipe.html?ic1=obinsite&oc=linkback"],
	thumbnail_img: 'http://foodnetwork.sndimg.com/content/dam/images/food/fullset/2013/7/11/0/YW0305H_chicken-tortilla-casserole-recipe_s4x3.jpg.rend.sni12col.landscape.jpeg'
        },{
	id: 9,
	name: 'Pork Chops with Roasted Kale & Walnut Pesto',
	lastText: ["(1) Preheat the broiler.", "(2) Strip the kale leaves from the tough stems and discard the stems.", "(3) Toss the leaves on a rimmed baking sheet with 2 tablespoons of the olive oil and 1/4 teaspoon salt, and spread them out in an even layer.", "(4) Broil the greens, stirring once or twice until they turn a brighter green with bits of charred leaves, about 4 minutes.", "(5) Stir in the walnuts and broil until the walnuts are fragrant but not burned, about 2 minutes.", "(6) Set aside to cool.", "(7) Sprinkle both sides of the chops with 1/2 teaspoon salt, 1/4 teaspoon pepper and the rosemary.", "(8) Heat 2 tablespoons of the olive oil in a large skillet over medium heat and cook, turning once, until an instant-read thermometer inserted into the thickest part registers 145 degrees F, about 12 minutes.", "(9) Transfer to a cutting board to rest for 5 minutes.", "(10) While the chops are cooking, pulse the garlic and the cooled kale and walnuts in a food processor until chopped.", "(11) Add the pepper flakes, lemon juice, 1/4 teaspoon salt and the remaining 1/2 cup olive oil and continue to process to make a slightly chunky pesto.", "(12) Adjust the consistency as desired with up to 1/4 cup water.", "(13) Season to taste with salt and pepper.", "(14) Top each pork chop with about 2 tablespoons of the pesto and serve with a baked potato or soft polenta.", "(15) From Food Network Kitchens", "(16) Read more at: http://www.foodnetwork.com/recipes/food-network-kitchens/pork-chops-with-roasted-kale-and-walnut-pesto-recipe.html?oc=linkback"],
	thumbnail_img: 'http://foodnetwork.sndimg.com/content/dam/images/food/fullset/2012/12/19/0/FNK_Pork-Chops-With-Kale-Pesto_s4x3.jpg.rend.sni12col.landscape.jpeg'
        },{
	id: 10,
	name: 'Roasted Tomato Bisque',
	lastText: ["(1) Preheat the oven to 400 degrees F.", "(2) In a mixing bowl, combine the drained whole tomatoes, olive oil, light brown sugar, carrots and shallots, and toss to coat.", "(3) Season the vegetables with salt and pepper.", "(4) Place the vegetables on a silicone or parchment-lined baking sheet and roast until caramelized, about 30 minutes.", "(5) Heat a soup pot over medium heat.", "(6) Add the butter and cook until foaming.", "(7) Add the crushed red pepper and garlic and saute for 1 minute.", "(8) Add the tomato paste and cook for 1 to 2 minutes.", "(9) Then add the sherry.", "(10) Cook until all the liquid has evaporated and the alcohol has cooked off, 1 to 2 minutes.", "(11) Add the roasted vegetables, crushed tomatoes and 1 cup chicken stock.", "(12) Season with salt and pepper and bring to a simmer.", "(13) Let simmer for 15 minutes.", "(14) Add the heavy cream and, using an immersion blender, puree the soup until uniform in texture.", "(15) Add more chicken stock to adjust the consistency to how you like it.", "(16) Recipe courtesy Jeff Mauro", "(17) Read more at: http://www.foodnetwork.com/recipes/jeff-mauro/roasted-tomato-bisque-recipe.html?oc=linkback"],
	thumbnail_img: 'http://foodnetwork.sndimg.com/content/dam/images/food/fullset/2012/2/24/1/ZB0202H_roasted-tomato-bisque_s4x3.jpg'
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
