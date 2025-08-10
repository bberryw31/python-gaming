import pandas as pd

data = [
    ["Truffle Sailfish Tartare", 785, 1727, 195, 295, 2, 2, "3 Sailfish Meat, 3 Purple Sea Urchin, 1 Truffle", "Jango", None],
    ["Truffle Blue Lobster Tail Sushi", 780, 1716, 190, 282, 2, 2, "2 Blue Lobster, 1 Truffle", "Jango", None],
    ["Truffle Shark Sandwich", 775, 1705, 185, 273, 2, 2, "3 Frilled Shark Meat, 3 Megamouth Shark Meat, 1 Truffle", "Jango", None],
    ["Grilled Antarctic Octopus & Truffle", 770, 1694, 185, 253, 2, 2, "3 Antarctic Octopus, 3 Kajime, 1 Truffle", "Jango", None],
    ["Hyalonema Tuna Sashimi", 765, 1683, 185, 265, 1, 1, "3 Bluefin Tuna Ootoro, 3 Yellowfin Tuna Ootoro, 2 Hyalonema", None, 15],
    ["Boiled Asian Sheepshead Wrasse & Truffle", 755, 1661, 180, 280, 2, 2, "3 Sheepshead Meat, 3 Kelp, 1 Truffle", "Make Jango Warm!", None],
    ["Steamed Hyalonema Angler Fish", 750, 1650, 180, 248, 1, 1, "3 Atlantic Anglerfish, 2 Hyalonema, 1 Soy Sauce", None, 12],
    ["Lobster Platter", 435, 1609, 195, 375, 4, 6, "2 American Lobster, 2 Tropical Rock Lobster, 2 Tokummia Katalepsis", "Jango", None],
    ["Soy Sauce Marinated Crab", 435, 1609, 190, 505, 4, 6, "2 Golden King Crab, 2 Snow Crab, 2 Horsehair Crab, 1 Soy Sauce", "Jango", None],
    ["Boiled Sailfish and Seaweed", 425, 1572, 138, 300, 6, 9, "3 Sailfish Meat, 2 Southern Bull Kelp, 2 Kajime, 1 Soy Sauce", "Seasonal Event: Marlin Party", 5],
    ["Great Barracuda Canape", 425, 1572, 147, 372, 4, 6, "5 Great Barracuda, 1 Cherry Tomato, 1 Onion, 1 Mayonnaise", "Cooksta Diamond Rank", 12],
    ["Grilled Eel with Habanero", 425, 1572, 155, 335, 6, 9, "2 Snub-nosed Spiny Eel, 2 Habanero, 1 Kajime, 1 Soy Sauce", "Jango", None],
    ["Seasoned Waptia Fieldensis", 425, 1572, 150, 440, 5, 7, "3 Waptia Fieldensis, 2 Cucumber, 3 Black Coral, 1 Black Vinegar", "Seasonal Event: Cucumber Party", 15],
    ["Dumbo Takoyaki", 420, 1554, 156, 390, 6, 9, "3 Dumbo Octopus, 2 Wheat, 1 Mayonnaise", "Cooksta Diamond Rank", 15],
    ["Falcatus Soybean Paste Soup", 420, 1554, 130, 382, 5, 7, "3 Falcatus, 3 Seaweed, 3 Buckbean, 1 Miso", None, 15],
    ["Humboldt Ink Pasta", 420, 1554, 150, 375, 7, 10, "1 Humboldt Squid Meat, 3 White Shrimp, 3 Wheat, 3 Garlic", "Complete Let Us Begin the Contest", None],
    ["Pikaia Ramen", 420, 1554, 135, 360, 7, 10, "3 Pikaia, 1 Grade A Egg, 2 Wheat, 3 Southern Bull Kelp", None, 15],
    ["Pufferfish Dumpling Soup", 420, 1554, 150, 420, 6, 9, "3 Longspine Porcupinefish, 3 Starry Puffer, 1 Egg, 1 Bladderwrack", "Jango", None],
    ["Nasu Dengaku", 415, 1535, 155, 317, 3, 4, "1 Eggplant, 1 Garlic, 1 Olive Oil, 1 Miso", "Cooksta Diamond Rank", 12],
    ["Fried Habanero Fangtooth", 410, 1517, 150, 420, 5, 7, "2 Fangtooth, 2 Habanero, 1 Bladderwrack, 1 Olive Oil", "Jango", None],
    ["Peacock Squid Ripieni", 410, 1517, 135, 360, 5, 7, "3 Peacock Squid, 2 Egg, 2 Garlic, 1 Black Pepper", "Complete Let Us Begin the Contest", 7],
    ["Batfish Ricebowl", 400, 1480, 150, 447, 5, 7, "5 Longfin Batfish, 5 Orbicular Batfish, 2 Rice, 2 Egg", "Train Mitchell to Level 15", 15],
    ["Boiled Porbeagle Shark", 400, 1480, 143, 332, 5, 7, "3 Porbeagle Shark Meat, 1 Black Vinegar, 1 Black Pepper", "Train Raul to Level 15", 15],
    ["Crimson Fish Roll", 400, 1480, 168, 258, 6, 9, "3 Clown Frogfish, 3 Red Bream, 3 Rhinochimaeridae", "Train Billy to Level 15", 15],
    ["Deep-Fried Eggplant Shrimp Meatballs", 400, 1480, 145, 460, 5, 7, "3 Black Tiger Shrimp, 3 Whiteleg Shrimp, 3 Eggplant, 1 Olive Oil", "Train Yusuke to level 15", 15],
    ["Dried Stingray", 400, 1480, 180, 225, 8, 12, "3 Starry Skate, 3 Stingray Meat, 3 Marbled Electric Ray Meat, 1 Salt", "Train Carolina to Level 15", 15],
    ["Dusky Grouper Steak", 400, 1480, 148, 328, 5, 7, "5 Dusky Grouper, 3 Cherry Tomato, 1 Salt, 1 Olive Oil", "Train El Nino to level 15", 15],
    ["Fried Onion Cuttlefish", 400, 1480, 153, 360, 5, 7, "5 Cuttlefish, 3 Onion, 1 Olive Oil, 1 Salt", "Train Raptor to Level 15", 15],
    ["Great Spider Crab Curry", 400, 1480, 155, 290, 6, 9, "1 Spider Crab, 1 Grade A Egg, 1 Curry Block", "Train Charlie to Level 15", 15],
    ["Ice Fish Curry", 400, 1480, 155, 317, 6, 9, "3 Ice Fish, 2 Bean, 1 Curry Block", "Train Drae to Level 15", 15],
    ["Latok Omelet", 400, 1480, 170, 260, 6, 9, "1 Grade A Egg, 2 Rice, 2 Sea Grape, 1 Soy Sauce", "Train Masayoshi to Level 15", 15],
    ["Mackerel Scad Hotdog", 400, 1480, 160, 340, 4, 6, "5 Mackerel Scad, 2 Wheat, 1 Mayonnaise", "Train Cohh to Level 15", 15],
    ["Narwhal Miso Soup", 400, 1480, 150, 420, 8, 12, "3 Narwhal Meat, 2 Carrot, 2 Buckbean, 1 Miso", "Train Davina to Level 15", 15],
    ["Rice with White Shrimp Meat", 400, 1480, 148, 400, 6, 9, "3 White Shrimp, 2 Rice, 2 Egg, 1 Soy Sauce", "Train Kyoko to Level 15", 15],
    ["Roasted Tropical Fish and Garlic", 400, 1480, 173, 236, 6, 9, "5 Clownfish, 5 Pyramid Butterflyfish, 5 Blue Tang, 3 Garlic", "Train Tohoku to Level 15", 15],
    ["Seahorse Salad", 400, 1480, 160, 295, 4, 6, "3 Long-Snouted Seahorse, 2 Cherry Tomato, 2 Sea Grape, 1 Olive Oil", "Train Yone to Level 15", 15],
    ["Seasoned Jellyfish", 400, 1480, 163, 298, 4, 6, "5 Barrel Jellyfish, 5 Fried Egg Jellyfish, 2 Garlic, 2 Black Coral", "Train James to Level 15", 15],
    ["Seaweed Rolled Omelet", 400, 1480, 165, 300, 6, 9, "1 Grade A Egg, 3 Seaweed, 3 Kelp", "Train Pai to Level 15", 15],
    ["Shark Karaage", 400, 1480, 155, 380, 6, 9, "3 Blacktip Shark Meat, 3 Copper Shark Meat, 1 Wheat, 1 Olive Oil", "Train Itsuki to Level 15", 15],
    ["Three-Colored Squid Roast", 400, 1480, 155, 334, 8, 12, "3 Peacock Squid, 3 Vampire Squid, 3 Cuttlefish, 1 Salt", "Train Liu to Level 15", 15],
    ["Trevally Nanbanzuke", 400, 1480, 145, 343, 5, 7, "5 White Trevally, 3 Onion, 1 Soy Sauce, 1 Olive Oil", "Train Maki to Level 15", 15],
    ["Wrasse Curry", 400, 1480, 150, 330, 4, 6, "5 Rainbow Wrasse, 5 Ornate Wrasse, 1 Bean, 1 Curry Block", "Train Jandi to Level 15", 15],
    ["Deep Fish Tempura", 395, 1461, 140, 320, 5, 7, "1 Cookiecutter Shark, 1 Vampire Squid, 1 Barreleye, 3 Kelp", "Complete Whose Fried food is the Best?", None],
    ["Hot Pepper Tuna", 395, 1461, 170, 350, 5, 7, "3 Bluefin Tuna Chutoro, 2 Habanero, 2 Sea Grape, 1 Sesame Seed", "Spicy Pepper Seeds!", None],
    ["Comber Sandwich", 390, 1443, 150, 420, 4, 6, "5 Comber, 5 Painted Comber, 2 Egg, 2 Wheat", "Complete Whose Fried food is the Best?", 7],
    ["Deep-Fried Red Lionfish", 390, 1443, 132, 366, 3, 4, "5 Red Lionfish, 1 Wheat, 1 Olive Oil, 1 Black Pepper", "Train Cohh to Level 10", 12],
    ["Fried Tomato and Snailfish", 390, 1443, 110, 335, 8, 12, "3 Gelatinous Snailfish, 3 Salmon Snailfish, 2 Bean, 2 Cherry Tomato", "Complete Chinese Cuisine Contest!", 7],
    ["Narrow-barred Spanish Mackerel Arancini", 390, 1443, 130, 364, 5, 7, "5 Narrow-Barred Spanish Mackerel, 2 Egg, 2 Rice, 2 Garlic", "Complete Let Us Begin the Contest", 7],
    ["Roasted Capelin", 390, 1443, 138, 345, 5, 7, "5 Capelin, 1 Black Coral, 1 Turmeric", "Train Drae to Level 10", 12],
    ["Stir-fried Habanero Lobster", 390, 1443, 140, 320, 4, 6, "2 Norway Lobster, 2 Habanero, 1 Olive Oil", None, 7],
    ["Sweet and Sour Stargazer", 390, 1443, 125, 395, 4, 6, "1 Bluespotted Stargazer, 1 Wheat, 1 Egg, 1 Olive Oil", "Complete Chinese Cuisine Contest!", None],
    ["Smoked Atlantic Mackerel Scramble", 387, 1431, 145, 460, 4, 6, "5 Atlantic Mackerel, 2 Wheat, 2 Egg", "Complete Whose Fried food is the Best?", 7],
    ["Black Vinegar Braised Parrotfish", 385, 1424, 136, 406, 4, 6, "5 Mediterranean Parrotfish, 2 Carrot, 1 Black Vinegar", "Cooksta Platinum Rank", 9],
    ["Fried Rice with Sally Lightfoot Crab", 385, 1424, 125, 305, 7, 10, "2 Sally Lightfoot Crab, 2 Rice, 1 Grade A Egg, 1 Black Pepper", "Complete Chinese Cuisine Contest!", 7],
    ["Plotosid Pie", 385, 1424, 150, 420, 5, 7, "5 Striped Catfish, 2 Wheat, 2 Onion, 2 Bean", "Complete Whose Fried food is the Best?", 7],
    ["Rice with Purple Sea Urchin Sushi", 385, 1424, 140, 320, 3, 4, "2 Purple Sea Urchin, 2 Rice, 1 Sesame Seed", "Train Raptor to Level 10", 12],
    ["Atlantic Bonito Curry", 380, 1406, 137, 389, 5, 7, "5 Atlantic Bonito, 2 Carrot, 1 Curry Block", "Cooksta Platinum Rank", 12],
    ["Marlin and Soybean Paste Roast", 380, 1406, 137, 272, 6, 9, "3 Marlin Meat, 2 Garlic, 1 Miso", "Seasonal Event: Marlin Party", 5],
    ["Special Fried Shrimp Sushi", 380, 1406, 110, 317, 1, 1, "2 Black Tiger Shrimp, 2 Whiteleg Shrimp, 1 Rice, 1 Olive Oil", "Train Drae to Level 5", 8],
    ["Steamed Eastern Rock Lobster & Egg", 380, 1406, 140, 455, 5, 7, "2 Eastern Rock Lobster, 2 Egg, 2 Kelp", None, 9],
    ["Tomato Egg Soup", 380, 1406, 120, 309, 8, 12, "2 Grade A Egg, 2 Cherry Tomato, 1 Black Pepper", "Complete Chinese Cuisine Contest!", 7],
    ["Blobfish Spring Roll", 375, 1387, 115, 322, 7, 10, "3 Blobfish, 2 Wheat, 1 Mayonnaise, 1 Sesame Seed", "Complete Chinese Cuisine Contest!", 7],
    ["Humphead Parrotfish Curry", 375, 1387, 140, 347, 4, 6, "5 Green Humphead Parrotfish, 2 Onion, 1 Turmeric", "Cooksta Platinum Rank", 12],
    ["Mianbao Xia", 375, 1387, 125, 305, 7, 10, "5 Black Tiger Shrimp, 5 Whiteleg Shrimp, 2 Wheat, 1 Olive Oil", "Complete Chinese Cuisine Contest!", 7],
    ["Seahorse Udon", 375, 1387, 128, 353, 3, 4, "3 Long-Snouted Seahorse, 2 Wheat, 1 Miso", "Cooksta Platinum Rank", 9],
    ["Tropical Fish Sushi Set", 375, 1387, 130, 346, 6, 9, "3 Titan Triggerfish, 3 Harlequin Hind, 3 Coral Trout, 3 Rice", "Complete Michael Bang's Inspiration", None],
    ["Vegetable Sushi", 375, 1387, 120, 390, 1, 1, "1 Rice, 1 Carrot, 1 Eggplant", "Good Ol' Vegetable Sushi!", None],
    ["Pelican Eel Jelly", 373, 1380, 151, 439, 6, 9, "3 Pelican Eel, 1 Black Vinegar, 1 Agar", "Complete Whose Fried food is the Best?", 7],
    ["Crystal Lobster Roll", 370, 1369, 170, 305, 6, 9, "2 Crystal Lobster, 2 Rice, 2 Bladderwrack", None, 9],
    ["Godzilla vs. Ebirah Curry", 370, 1369, 140, 365, 6, 9, "2 European Lobster, 2 Moray Eel, 1 Turmeric, 1 Olive Oil", "Complete Go to Bancho Sushi", None],
]

Farm_Ingredients = ["Wheat", "Carrot", "Onion", "Cherry Toamto", "Bean", "Eggplant", "Garlic", "Rice", "Habanero", "Cucumber", "Egg", "Agar", "Kajime", "Seaweed", "Kelp", "Sea Grape", "Black Coral", "Southern Bull Kelp", "Buckbean", "Bladderwrack", "Hyalonema"]
Spices = ["Soy Sauce", "Black Vinegar", "Olive Oil", "Black Pepper", "Mayonnaise", "Curry Block", "Tumeric", "Salt", "Miso", "Sesame Seed", "Truffle"]

df = pd.DataFrame(data, columns=[
    'Name', 'BasePrice', 'MaxPrice', 'BaseTaste', 'MaxTaste',
    'BaseServing', 'MaxServing', 'Ingredients', 'AcquirementMethod', 'ArtisanFlameCost'
])

def calculate_efficiency_score(row):
    max_price_serving = row['MaxPrice'] * row['MaxServing']
    farm_ingredients_count = 1
    for ingredients in row['Ingredients'].split(', '):
        num = int(ingredients[0])
        if ingredients[2:] in Farm_Ingredients:
            farm_ingredients_count+=0.5*num
        elif ingredients[2:] in Spices:
            farm_ingredients_count+=0.3*num
        else:
            farm_ingredients_count+=0.05*num
    return max_price_serving / farm_ingredients_count

df['EfficiencyScore'] = df.apply(calculate_efficiency_score, axis=1)

df = df.sort_values(by='EfficiencyScore', ascending=False)

df[['Name', 'Ingredients', 'MaxPrice', 'MaxServing', 'EfficiencyScore']].to_csv('recipes_efficiency_scores.txt', index=False, sep='\t')

print("Efficiency scores exported to 'recipes_efficiency_scores.txt'")
