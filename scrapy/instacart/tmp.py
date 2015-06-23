import json
import os
import re
import pdb
import difflib
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

department_prefixes = [
"Fresh Fruits",
"Fresh Vegetables",
"Fresh Herbs",
"Packaged Vegetables & Fruits",
"Tofu & Meat Alternatives",
"Meat Counter",
"Poultry Counter",
"Seafood Counter",
"Packaged Meat",
"Packaged Poultry",
"Packaged Seafood",
"Hot Dogs, Bacon & Sausage",
"Newly Added",
"Specialty Cheeses",
"Lunch Meat",
"Prepared Meals",
"Prepared Soups & Salads",
"Fresh Dips & Tapenades",
"Tofu & Meat Alternatives",
"Bread",
"Tortillas & Flat Bread",
"Buns & Rolls",
"Breakfast Bakery",
"Bakery Desserts",
"Milk",
"Cream",
"Eggs",
"Packaged Cheese",
"Yogurt",
"Butter",
"Other Creams & Cheeses",
"Soy & Lactose-Free",
"Refrigerated Pudding & Desserts",
"Specialty Cheeses",
"Bulk Grains, Rice & Dried Goods",
"Bulk Butters, Honey, Syrups & Spreads",
"Bulk Dried Fruits & Vegetables",
"Bulk Trail Mix & Snack Mix",
"Bulk Tea & Coffee",
"Bulk Flours & Powders",
"Bulk Nuts & Seeds",
"Other Bulk",
"Bulk Candies & Chocolates",
"Canned Fruit & Applesauce",
"Canned & Jarred Vegetables",
"Canned Meals & Beans",
"Canned Meat & Seafood",
"Soup, Broth & Bouillon",
"Dry Pasta",
"Fresh Pasta",
"Pasta Sauce",
"Instant Foods",
"Grains, Rice & Dried Goods",
"Condiments",
"Honeys, Syrups & Nectars",
"Spices & Seasonings",
"Spreads",
"Salad Dressing & Toppings",
"Oils & Vinegars",
"Pickled Goods & Olives",
"Marinades & Meat Preparation",
"Preserved Dips & Spreads",
"Doughs, Gelatins & Bake Mixes",
"Baking Ingredients",
"Baking Supplies & Decor",
"Asian Foods",
"Latino Foods",
"Indian Foods",
"Kosher Foods",
"More International Foods",
"Coffee",
"Refrigerated",
"Tea",
"Juice & Nectars",
"Energy & Sports Drinks",
"Soft Drinks",
"Water, Seltzer & Sparkling Water",
"Cocoa & Drink Mixes",
"Cereal",
"Hot Cereal & Pancake Mixes",
"Granola",
"Breakfast Bars & Pastries",
"Candy & Chocolate",
"Chips & Pretzels",
"Cookies & Cakes",
"Crackers",
"Energy & Granola Bars",
"Ice Cream Toppings",
"Nuts, Seeds & Dried Fruit",
"Popcorn & Jerky",
"Trail Mix & Snack Mix",
"Mint & Gum",
"Fruit & Vegetable Snacks",
"Frozen Breakfast",
"Frozen Appetizers & Sides",
"Frozen Meals",
"Frozen Meat & Seafood",
"Frozen Pizza",
"Frozen Breads & Doughs",
"Frozen Produce",
"Frozen Vegan & Vegetarian",
"Frozen Juice",
"Frozen Dessert",
"Ice Cream & Ice",
"Digestion",
"Vitamins & Supplements",
"Protein & Meal Replacements",
"Baby Food & Formula",
]

files = [f for f in os.listdir('.') if re.match(r'wf-.*\.json', f)]
insta_names = []
calorie_missing_count = 0
insta_item_count = 0
for file in files:
    with open(file) as data_file:
        data_str = data_file.readlines()[0]
        data_str = unicode(data_str, errors='ignore')
        data_str = data_str.strip()
        data = json.loads(data_str)
        insta_items = data['data']['items']
        for item in insta_items:
            insta_item_count += 1
            if item['fat_calories']:
                calorie_missing_count += 1
            item_name = str(item['name'])
            brand_name = str(item['brand_name'])
            #remove_brand = item_name[item_name.index(brand_name):]
            #remove_brand = remove_brand.replace(brand_name,"").strip()
            prefix_flag = False
            for prefix in department_prefixes:
                if item['brand_name']:
                    prefix_string = prefix + " " + item['brand_name']
                else:
                    prefix_string = prefix
                if item['name'].startswith(prefix_string):
                    prefix_flag = True
                    insta_names += [str(item['name']).replace(prefix_string,"").strip()]
            if not prefix_flag:
                pdb.set_trace()

print "Ratio: "
print calorie_missing_count
print float(calorie_missing_count/insta_item_count)

mfp_names = []
with open('mfpWholeFoods061515.json') as data_file:
    data_str = data_file.readlines()[0]
    data_str = unicode(data_str, errors='ignore')
    data_str = data_str.strip()
    data = json.loads(data_str)
    mfp_items = data['results']['collection1']
    for item in mfp_items:
        mfp_names += [item['name']['text']]


print mfp_names[0:100]

insta_super = 0
mfp_super = 0
no_matches = []
has_matches = []
pdb.set_trace()
## for insta_name in insta_names[0:10]:
##     #foo = difflib.get_close_matches(insta_name, mfp_names)
##     #mfp_matches = process.extract(insta_name, mfp_names, limit=10)
##     for name in mfp_names:
##         pass
##     pdb.set_trace()
##     if not mfp_matches:
##         no_matches += [insta_name]
##     if mfp_matches and mfp_matches[0] == insta_name:
##         has_matches += [mfp_matches[0]]
##     ## for mfp_name in mfp_names:
##     ##     if mfp_name in insta_name:
##     ##         mfp_super += 1
##     ##     if insta_name in mfp_name:
##     ##         insta_super += 1

pdb.set_trace()
print insta_super
print mfp_super

#with open('wf-82-516.json') as data_file:
#    data = data_file.readlines()[0]
#    print data[183180:183190]
