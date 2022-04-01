import json

def cleanStr4SQL(s):
    return s.replace("'", "`").replace("\n", " ")

# def getNestedAttributes(attributes, key):
#     result = attributes.get(key, 'None')
#     if isinstance(result, dict):
#         return result
#     else:
#         return {}

def int2BoolStr (value):
    if value == 0:
        return 'False'
    else:
        return 'True'


def getNestedAttributes(attributes):
    L = []
    for (attribute, value) in list(attributes.items()):
        if isinstance(value, dict):
            L += getNestedAttributes(value)
        else:
            L.append((attribute,value))
    return L
    
    
def insert2BusinessTable():
    #reading the JSON file
    with open('./yelp_business.JSON','r') as f:    #TODO: update path for the input file
        #outfile =  open('./yelp_business_out.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()
        count_line = 0

        #connect to yelpdb database on postgres server using psycopg2
        try:
            #TODO: update the database name, username, and password
            conn = psycopg2.connect("dbname='tempyelp' user='postgres' host='localhost' password='passw'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            # Generate the INSERT statement for the current business
            # TODO: The below INSERT statement is based on a simple (and incomplete) businesstable schema. Update the statement based on your own table schema and
            # include values for all businessTable attributes
            
            try:
                cur.execute("INSERT INTO businessTable (business_id, name, address, state, city, zipcode, latitude, longitude, stars, numCheckins, numTips, is_open)"
                       + " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                         (data['business_id'],cleanStr4SQL(data["name"]), cleanStr4SQL(data["address"]), data["state"], data["city"], data["postal_code"], data["latitude"], data["longitude"], data["stars"], 0 , 0 , [False,True][data["is_open"]] ) )
            except Exception as e:
                print("Insert to businessTABLE failed!",e)
            conn.commit()
            # optionally you might write the INSERT statement to a file.
            # sql_str = ("INSERT INTO businessTable (business_id, name, address, state, city, zipcode, latitude, longitude, stars, numCheckins, numTips, is_open)"
            #           + " VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', {6}, {7}, {8}, {9}, {10}, {11})").format(data['business_id'],cleanStr4SQL(data["name"]), cleanStr4SQL(data["address"]), data["state"], data["city"], data["postal_code"], data["latitude"], data["longitude"], data["stars"], 0 , 0 , [False,True][data["is_open"]] )
            
            #write the INSERT statement to a file
            outfile.write(sql_str+'\n')

            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()

    print(count_line)
    #outfile.close()  #uncomment this line if you are writing the INSERT statements to an output file.
    f.close()
    
    
def parseBusinessData():
    # read the JSON file
    # We assume that the Yelp data files are available in the current directory. If not, you should specify the path when you "open" the function.
    with open('.//yelp_business.JSON', 'r') as f:
        outfile = open('.//business.txt', 'w')
        line = f.readline()
        count_line = 0
        # read each JSON abject and extract data
        while line:
            data = json.loads(line)
            outfile.write("{} - business info : '{}' ; '{}' ; '{}' ; '{}' ; '{}' ; '{}' ; {} ; {} ; {} ; {}\n".format(
                str(count_line),  # the line count
                cleanStr4SQL(data['business_id']),
                cleanStr4SQL(data["name"]),
                cleanStr4SQL(data["address"]),
                cleanStr4SQL(data["state"]),
                cleanStr4SQL(data["city"]),
                cleanStr4SQL(data["postal_code"]),
                str(data["latitude"]),
                str(data["longitude"]),
                str(data["stars"]),
                str(data["is_open"])))

            # process business categories
            categories = data["categories"].split(', ')
            outfile.write("      categories: {}\n".format(str(categories)))

            # TO-DO : write your own code to process attributes
            # make sure to **recursively** parse all attributes at all nesting levels. You should not assume a particular nesting level.

            # attributes = data['attributes']
            # outfile.write(attributes.get('GoodForKids', 'None') + '\t')  #good for kids
            # outfile.write(attributes.get('NoiseLevel', 'None') + '\t')  #noise level
            # outfile.write(attributes.get('RestaurantsDelivery', 'None') + '\t')  #restaurants delivery
            #
            # good_for_meal = getNestedAttributes(attributes, 'GoodForMeal')
            # outfile.write(good_for_meal.get('dessert', 'None')+'\t') #good for dessert
            # outfile.write(good_for_meal.get('latenight', 'None')+'\t') #good for latenight
            # outfile.write(good_for_meal.get('lunch', 'None')+'\t') #good for lunch
            # outfile.write(good_for_meal.get('dinner', 'None')+'\t') #good for dinner
            # outfile.write(good_for_meal.get('brunch', 'None')+'\t') #good for brunch
            # outfile.write(good_for_meal.get('breakfast', 'None')+'\t') #good for breakfast
            #
            # outfile.write(attributes.get('Alcohol', 'None')+'\t') #alcohol
            # outfile.write(attributes.get('Caters', 'None')+'\t') #caters
            # outfile.write(attributes.get('WiFi', 'None')+'\t') #wifi
            # outfile.write(attributes.get('RestaurantsTakeOut', 'None')+'\t') #restaurants take out
            # outfile.write(attributes.get('BusinessAcceptsCreditCards', 'None')+'\t') #business accepts credit cards
            #
            # dietary_restrictions = getNestedAttributes(attributes, 'DietaryRestrictions')
            # outfile.write(dietary_restrictions.get('dairy-free', 'None') + '\t') #no dairy
            # outfile.write(dietary_restrictions.get('gluten-free', 'None') + '\t') #no gluten
            # outfile.write(dietary_restrictions.get('vegan', 'None') + '\t') #vegan
            # outfile.write(dietary_restrictions.get('kosher', 'None') + '\t') #kosher
            # outfile.write(dietary_restrictions.get('halal', 'None') + '\t') #halal
            # outfile.write(dietary_restrictions.get('soy-free', 'None') + '\t') #no soy
            # outfile.write(dietary_restrictions.get('vegetarian', 'None') + '\t') #vegatarian
            #
            # outfile.write(attributes.get('Open24Hours', 'None') + '\t')
            # outfile.write(attributes.get('RestaurantsCounterService', 'None') + '\t')
            #
            # ambience = getNestedAttributes(attributes, 'Ambience')
            # outfile.write(ambience.get('romantic', 'None')+'\t') #ambience romantic
            # outfile.write(ambience.get('intimate', 'None')+'\t') #ambience intimate
            # outfile.write(ambience.get('touristy', 'None')+'\t') #ambience touristy
            # outfile.write(ambience.get('hipster', 'None')+'\t') #ambience hipster
            # outfile.write(ambience.get('divey', 'None')+'\t') #ambience divey
            # outfile.write(ambience.get('classy', 'None')+'\t') #ambience classy
            # outfile.write(ambience.get('trendy', 'None')+'\t') #ambience trendy
            # outfile.write(ambience.get('upscale', 'None')+'\t') #ambience upscale
            # outfile.write(ambience.get('casual', 'None')+'\t') #ambience casual
            #
            # business_parking = getNestedAttributes(attributes, 'BusinessParking')
            # outfile.write(business_parking.get('garage', 'None')+'\t') #business parking garage
            # outfile.write(business_parking.get('street', 'None')+'\t') #business parking street
            # outfile.write(business_parking.get('validated', 'None')+'\t') #business parking validated
            # outfile.write(business_parking.get('lot', 'None')+'\t') #business parking lot
            # outfile.write(business_parking.get('valet', 'None')+'\t') #business parking valet
            #
            # outfile.write(attributes.get('RestaurantsTableService', 'None')+'\t') #restaurants table service
            # outfile.write(attributes.get('RestaurantsGoodForGroups', 'None')+'\t') #restaurants good for groups
            # outfile.write(attributes.get('OutdoorSeating', 'None')+'\t') #outdoor seating
            # outfile.write(attributes.get('HasTV', 'None')+'\t') #has tv
            # outfile.write(attributes.get('BikeParking', 'None')+'\t') #bike parking
            # outfile.write(attributes.get('RestaurantsReservations', 'None')+'\t') #restaurants reservations
            # outfile.write(attributes.get('RestaurantsPriceRange2', 'None')+'\t') #restaurants price range2
            # outfile.write(attributes.get('RestaurantsAttire', 'None')+'\t') #restaurants attire
            #
            # outfile.write(attributes.get('ByAppointmentOnly', 'None')+'\t') #by appointment only
            # outfile.write(attributes.get('BYOBCorkage', 'None')+'\t') #BYOB corkage
            # outfile.write(attributes.get('CoatCheck', 'None')+'\t') #coat check
            # outfile.write(attributes.get('HappyHour', 'None')+'\t') #happy hour
            # outfile.write(attributes.get('Smoking', 'None')+'\t') #smoking
            #
            # music = getNestedAttributes(attributes, 'Music')
            # outfile.write(music.get('dj', 'None')+'\t') #music dj
            # outfile.write(music.get('background_music', 'None')+'\t') #music background
            # outfile.write(music.get('no_music', 'None')+'\t') #no music
            # outfile.write(music.get('jukebox', 'None')+'\t') #jukebox
            # outfile.write(music.get('live', 'None')+'\t') #live music
            # outfile.write(music.get('video', 'None')+'\t') #music video
            # outfile.write(music.get('karaoke', 'None')+'\t') #karaoke
            #
            # best_nights = getNestedAttributes(attributes, 'BestNights')
            # outfile.write(best_nights.get('monday', 'None')+'\t') #monday
            # outfile.write(best_nights.get('tuesday', 'None')+'\t') #tuesday
            # outfile.write(best_nights.get('wednesday', 'None')+'\t') #wednesday
            # outfile.write(best_nights.get('thursday', 'None')+'\t') #thursday
            # outfile.write(best_nights.get('friday', 'None')+'\t') #friday
            # outfile.write(best_nights.get('saturday', 'None')+'\t') #saturday
            # outfile.write(best_nights.get('sunday', 'None')+'\t') #sunday
            #
            # outfile.write(attributes.get('WheelchairAccessible', 'None')+'\t')
            # outfile.write(attributes.get('BusinessAcceptsBitcoin', 'None')+'\t')
            # outfile.write(attributes.get('GoodForDancing', 'None')+'\t')
            #
            # hair_specializes_in = getNestedAttributes(attributes, 'HairSpecializesIn')
            # outfile.write(hair_specializes_in.get('straightperms', 'None')+'\t')
            # outfile.write(hair_specializes_in.get('coloring', 'None')+'\t')
            # outfile.write(hair_specializes_in.get('extensions', 'None')+'\t')
            # outfile.write(hair_specializes_in.get('africanamerican', 'None')+'\t')
            # outfile.write(hair_specializes_in.get('curly', 'None')+'\t')
            # outfile.write(hair_specializes_in.get('kids', 'None')+'\t')
            # outfile.write(hair_specializes_in.get('perms', 'None')+'\t')
            # outfile.write(hair_specializes_in.get('asian', 'None')+'\t')
            #
            # outfile.write(attributes.get('AcceptsInsurance', 'None')+'\t')
            # outfile.write(attributes.get('Corkage', 'None')+'\t')
            # outfile.write(attributes.get('BYOB', 'None')+'\t')
            # outfile.write(attributes.get('DogsAllowed', 'None')+'\t')
            # outfile.write(attributes.get('DriveThru', 'None')+'\t')
            # outfile.write(attributes.get('AgesAllowed', 'None')+'\t')

            #process business attributes
            outfile.write("      attributes: [")
            for (attributes,value) in getNestedAttributes(data['attributes']):
                attr_str = "('" + str(attributes) + "','" + str(value) + "')"
                outfile.write(attr_str +'\t')
            outfile.write("]")

            # TO-DO : write your own code to process hours data

            #process business hours
            hours = data['hours']
            # outfile.write(hours.get('Monday', 'None') + '\t')
            # outfile.write(hours.get('Tuesday', 'None') + '\t')
            # outfile.write(hours.get('Wednesday', 'None') + '\t')
            # outfile.write(hours.get('Thursday', 'None') + '\t')
            # outfile.write(hours.get('Friday', 'None') + '\t')
            # outfile.write(hours.get('Saturday', 'None') + '\t')
            # outfile.write(hours.get('Sunday', 'None') + '\t')
            outfile.write("\n      hours: [{}]\n".format(str(hours)))
            outfile.write("")

            outfile.write('\n')

            line = f.readline()
            count_line += 1
    print(count_line)
    outfile.close()
    f.close()


def parseUserData():
    # TO-DO : write code to parse yelp_user.JSON
    with open('.//yelp_user.JSON','r') as f:
        outfile = open('.//user.txt', 'w')
        line = f.readline()
        count_line = 0
        #read each JSON abject and extract data
        while line:
            data = json.loads(line)
            outfile.write("{} - user data : '{}'; '{}' ; {} ; {} ; {} ; {} ; {} ; {} ; {} \n".format(

                cleanStr4SQL(data['user_id']),
                cleanStr4SQL(data["name"]),
                str(data["average_stars"]),
                str(data["cool"]),
                str(data["fans"]),
                str(data["friends"]),
                str(data["funny"]),
                str(data["tipcount"]),
                str(data["useful"]),
                str(data["yelping_since"])))

            # outfile.write(str(count_line) + "-user data: ")
            # outfile.write(cleanStr4SQL(data['user_id']) + "; ")
            # outfile.write(cleanStr4SQL(data['name']) + "; ")
            # outfile.write(str(data['yelping_since']) + "; ")
            # outfile.write(str(data['average_stars']) + "; ")
            # outfile.write(str(data['tipcount']) + "; ")
            # outfile.write("(" + str(data['cool']) + "," + str(data['funny']) + "," + str(data['useful']) + "); ")
            # outfile.write(str(data['fans']) + "; ")
            # outfile.write(str(data['tipcount']) + "; ")
            # outfile.write("friends: ")
            # friends = data['friends']
            # outfile.write(str([item for item in friends]))

            outfile.write('\n')

            line = f.readline()
            count_line +=1
    print(count_line)
    outfile.close()
    f.close()

    pass


def parseCheckinData():
    # TO-DO : write code to parse yelp_checkin.JSON
    with open('.//yelp_checkin.JSON','r') as f:
        outfile =  open('.//checkin.txt', 'w')
        line = f.readline()
        count_line = 0
        #read each JSON abject and extract data
        while line:
            data = json.loads(line)
            outfile.write(" {} - Check in data : '{}' \n".format(
                cleanStr4SQL(data['business_id']),
                str(data["date"])))

            outfile.write('\n')

            line = f.readline()
            count_line +=1
    print(count_line)
    outfile.close()
    f.close()
    pass


def parseTipData():
    # TO-DO : write code to parse yelp_tip.JSON
    with open('.//yelp_tip.JSON', 'r') as f:
        outfile = open('.//tip.txt', 'w')
        line = f.readline()
        count_line = 0
        # read each JSON abject and extract data
        while line:
            data = json.loads(line)
            outfile.write("{} - tip data : '{}'; '{}' ; '{}' ; {} \n".format(
                cleanStr4SQL(data['user_id']),
                cleanStr4SQL(data['business_id']),
                cleanStr4SQL(data['text']),
                str(data["date"]),
                str(data["likes"])))

            outfile.write('\n')

            line = f.readline()
            count_line += 1
    print(count_line)
    outfile.close()
    f.close()
    pass


#insert2BusinessTable()
#insert2HoursTable()
#insert2CategoriesTable()
#insert2UsersTable()
#insert2CheckinsTable()
#insert2FriendsTable()

if __name__ == "__main__":
    parseBusinessData()
    parseUserData()
    parseCheckinData()
    parseTipData()
