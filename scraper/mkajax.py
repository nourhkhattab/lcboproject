import json
import re
import cgi
import time

json_data = open('items.json')
data=json.load(json_data)

master = {}
i=0
j=0
for c in data:
 
    d = list(c.values())

    
    if d[0] == []:
        j+= 1
        continue
    s = d[0][0]
    i+=1

    s = s.replace('\r','').replace('\n','').replace('\t','')

    while "  " in s:
        s = s.replace('  ',' ')

    s = re.sub('<[^<]+>','', s).strip()
    
    if re.search('PRODUCT DISCONTINUED', s) != None or re.search('Accessories and Non-Alcohol Items', s) != None:
        continue

    m = re.search('^.*(?= \w* \d*[|])', s)
    name = cgi.escape(m.group(0))
    
    m = re.search('\d*(?=[|])', s)
    number = cgi.escape(m.group(0))
    
    m = re.search('((\d*x\d*)|(\d*))(?= mL)', s)
    volumeR = cgi.escape(m.group(0))
    if "x" in volumeR:
        volumeR = int(volumeR.split("x")[0]) * int (volumeR.split("x")[1])

    m = re.search('[\d\.]*(?=[%])', s)
    percentage = cgi.escape(m.group(0))
    if percentage + '%' in name:
        percentage = re.findall('[\d\.]*(?=[%])', s)[2]

    m = re.search('(?<=\$ )[\d\.]*', s)
    price = cgi.escape(m.group(0))

    m = re.search('(Wine|Spirits|Beer|Coolers and Cocktails|Cider)', s)
    cat1 = cgi.escape(m.group(0))

    m = re.search('(?<=, )(Ale|Bags \& Boxes|Bar Accessories|Brandy|Champagne|Cider|Cognac \/ Armagnac|Coolers|Dessert Wine|Eau\-de\-Vie|Fortified Wines|Gift and Sampler Packs|Gin|Hybrid|Icewine|Lager|Liqueur\/Liquor|One Pour Cocktails|Product Knowledge Videos|Red Wine|Ros[é] Wine|Rum|Shochu \/ Soju|Sparkling Wine|Specialty|Specialty Wines|Tequila|Vessels|Vodka|Whisky\/Whiskey|White Wine)', s)
    if m:
        cat2 = cgi.escape(m.group(0))
    else:
        cat2 = 'N/A'

    m = re.search('(?<=, )(Altbier|Amber|Aniseed|Belgian Ale|Berry|Bitter|Bitters \/ Herbs|Blanco|Bock|Bourbon \/ American Whiskey|Cachaca|Canadian Whisky|Chocolate|Citrus|Classic|Coffee|Cream|Cream Ale|Creamy|Dark|Dark Lager|Dark\/Brown Ale|Dessert|European Fortified|Flavoured|Flavoured Ale|Flavoured Cider|Flavoured Vodka|Flavoured Wine|Floral|Fruit Flavoured|Fruit Spirit|Fruit Wine|Fruity|Gluten Free Beer|Grappa / Grape Spirit|India Pale Ale [(]IPA[)]|International Whiskey|Irish Whiskey|Kolsch|Madeira \/ Marsala|Mead|Mezcal|Mint|Mixed|Mixto|New World Fortified|Nut|Pale Ale|Pale Lager|Party Packs|Port|Porter|Red|Reposado|Ros[é] / Red|Ros[é]|Sake \/ Rice Wine|Scotch Single Malts|Scotch Whisky Blends|Sherry|Sotal|Sour|Sparkling|Spice|Spiced|Spicy|Steam Beer|Stout|Strong Ale|Sweet Flavours|Traditional Cider|Tropical|Unique Selections|VS|VSOP|Vermouth\/ Aperitif|Wheat|White|XO)', s)
    if m:
        cat3 = cgi.escape(m.group(0))
    else:
        cat3 = 'N/A'

    apml = (float(percentage) * int(volumeR))/100
    apd = apml/float(price)
    master[number] = [str(name), str(int(volumeR)).rjust(4), str("{0:.2f}".format(float(price))).rjust(7), str("{0:.2f}".format(float(percentage))).rjust(5), str("{0:.2f}".format(apml)).rjust(7), str("{0:.4f}".format(apd)).rjust(7), cat1, cat2, cat3]
    
print(len(master))
print(i)
print(j)

html = '[\n\t'
for key, value in master.items():
    html += '\t\t\t["' +'<a href=\'http://www.lcbo.com/lcbo-ear/lcbo/product/searchResults.do?ITEM_NUMBER=' + str(key).replace('\'','\\\'') + '\'>' + str(key).zfill(6) + '</a>"'
    for v in value:
        html += ', "' + v.replace('"','\\"') + '"'
    html += '],\n'

html = html[:-2]
html += '];'

f = open('../ajax.txt', 'w')
f.write(html)
f.close()

f = open('../_includes/date.txt', 'w')
f.write(time.strftime("%c"))
f.close()
