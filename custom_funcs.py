import urllib2, json, sys, time
from print_pretty import pretty_print

#####################################
#         Functions Below           #
#####################################

# EDMUNDS API KEY
# Enter your own API key below or make make a text file
# with the name 'API_KEY' and just place the key in there.
API_KEY =open('API_KEY.txt', 'r').read()

def clear():
    print ('\n'*100)

def dots():
    print('.', time.sleep(.5),
          '.', time.sleep(.5),
          '.', time.sleep(.5),
          '.', time.sleep(.5),
          '.', time.sleep(1),)

def wait(req):
    print('Getting {} available'.format(req), dots())

def list_check(item, array):
    item = item
    while item not in array:
        item = raw_input ('Choice not in list above - try again...\nENTER CHOICE HERE -->  ').title()
    return item

def choose_car():

    clear()
    #wait('makes')

    # url to pull basic info for all years, makes and models available
    url = 'https://api.edmunds.com/api/vehicle/v2/'\
    'makes?fmt=json&api_key=' + API_KEY

    # get response data and append to 'resp' variable as JSON
    data = json.load(urllib2.urlopen(url))

    # set arrays to hold dynamic information
    makes = []
    models = []
    make_and_models = []
    years = []
    trim_packages = []
    car_id =''

    # loop through all available data and choose a car make
    for make in data['makes']:
        makes.append(make['name'])

    # get car make selection
    print('\nChoose a make from the following:\n')
    pretty_print(makes)
    make_choice = raw_input('\nENTER CHOICE HERE -->  ').title()
    make_choice = list_check(make_choice, makes)

    clear()
    #wait('models')

    # loop through and choose a model for the make
    for make in data['makes']:
        if make['name'] == make_choice:
            for model in make['models']:
                models.append(model['name'])

        for i in range(len(models)):
            make_and_models.append('{} {}'.format(make_choice, models[i]))

    # get model selection per the chosen make
    print('\nChoose a make from the following:\n')
    pretty_print(models)
    model_choice = raw_input('\nENTER CHOICE HERE -->  ').title()
    model_choice = list_check(model_choice, models)

    clear()
    #wait('years')

    # loop through and get the years available for that make and model
    for make in data['makes']:
        if make['name'] == make_choice:
            for model in make['models']:
                if model['name'] == model_choice:
                    for year in model['years']:
                        years.append(str(year['year']))

    # get the year selection for selected make and model
    print('\nThe following years are available for the {} {}:\n'.format(make_choice, model_choice))
    pretty_print(years)
    year_choice = raw_input('\nWhich year do you want information for?\nENTER THE YEAR HERE -->  ')
    year_choice = list_check(year_choice, years)

    clear()
    #wait('trim options')

    # get trim packaging avialable for that year-make-model
    styles_url = 'https://api.edmunds.com/api/vehicle/v2/'+make_choice+'/'+model_choice+'/'+year_choice+'/styles?fmt=json&api_key='+API_KEY
    # use new URL to pull trim data - append to 'styles_resp' as JSON
    styles_resp = json.load(urllib2.urlopen(styles_url))

    # append trim styles to trim_packaging array
    for style in styles_resp['styles']:
        trim_packages.append(style['trim'])

    print('\nThe following trim packaging are available for the {} {} {}:'.format(year_choice, make_choice,model_choice))

    # print out trim packages and associate them with numbers
    # this helps avoid capitalization errors and keeps things neet

    trim_selections = dict(zip(range(len(trim_packages)),trim_packages))

    for key in trim_selections:
        print('{} :   {}'.format(key+1, trim_selections[key]))

    # choose trim package by number selection
    run_number_check = True

    # get input and verify that it is a number and in range of the options list
    while run_number_check:

        # get input
        choice = raw_input('Enter the number of the trim package you would like to select\n-->  ')

        # try to turn it into an integer
        try:
            int(choice)

        # if that fails and provides a ValueError
        # then return the fact it isn't a number and
        # loop back through again
        except ValueError:
            print('That is not a number - try again...\n')

        # if we finally get something that is a digit
        # then we pass it to this if function to check
        # if it is within range
        else:

            # now that we know trying to turn it into an integer
            # won't fail, lets replace the choice variable with the
            # integer version of iteself
            choice = int(choice)

            # check if it is within range
            # if this fails, then we give an appropriate error message
            # and start the run_number_check all over again
            if choice > len(trim_packages):
                print('That number is not in the list - try again...\n')

            # and if alls well that ends well, we finally
            # get to end this piece of shit!
            else:
                run_number_check = False



    trim_choice = trim_packages[int(choice)-1]

    clear()
    #wait('unique style id')

    print('getting data for the {} {} {} {}\n'.format(year_choice,make_choice,model_choice,trim_choice))

    # get style number
    for style in styles_resp['styles']:
        if style['trim'] == trim_choice:
            car_id = style['id']
            print('Unique car style ID --> {}'.format(car_id))

    car_selection = {'year': year_choice, 'make': make_choice, 'model': model_choice, 'trim': trim_choice, 'styleID': car_id}
    return car_selection

def get_options(style_ID):
    # call url to get car options
    options_url = 'https://api.edmunds.com/api/vehicle/v2/styles/'+str(style_ID)+'/options?fmt=json&api_key='+API_KEY
    options = json.load(urllib2.urlopen(options_url))

    clear()
    #wait('special options')

    # list out options
    print('OPTIONS\n_______\n')
    count = 1
    for feature in options['options']:
        feature_attributes = []
        print('{}. {}'.format(str(count),feature['name']))
        print('Category - {}'.format(feature['category']))
        try:
            print('DESCRIPTION:\n{}'.format(feature['description']))
        except:
            print('DESCRIPTION:\nSorry, no description available')
        # append feature attributes to 'feature_attributes' array
        for attribute in feature['attributes']:
               feature_attributes.append(attribute['name'])
        if len(feature_attributes) > 0:
            print('features: {}\n\n'.format(', '.join(feature_attributes)))
        else:
            print('\n\n')
        count += 1

def get_colors(style_ID):
    colors = []
    color_url = 'https://api.edmunds.com/api/vehicle/v2/styles/'+str(style_ID)+'/colors?fmt=json&api_key='+API_KEY

    clear()
    #wait('color options')

    color_data = json.load(urllib2.urlopen(color_url))

    print(' _______________\n|EXTERIOR COLORS|\n _______________')
    for color in color_data['colors']:
        if color['category'] == 'Exterior':
            print('{}'.format(color['name']))
    print('\n')
    print(' _______________\n|INTERIOR COLORS|\n _______________')
    for color in color_data['colors']:
        if color['category'] == 'Interior':
            print('{}'.format(color['name']))
    print('\n')

    # print json.dumps(color_data, indent = 4)

def get_photos(style_ID):
    photos = []
    photo_url = 'https://api.edmunds.com/v1/api/vehiclephoto/service/'\
                'findphotosbystyleid?styleId='+str(style_ID)+'&fmt=json&api_key='+API_KEY
    photo_url_start = 'http://media.ed.edmunds-media.com'

    clear()

    photo_data = json.load(urllib2.urlopen(photo_url))

    '''
##############  Standard photo JSON response  #######################
---------------------------------------------------------------------

{
    "shotTypeAbbreviation": "EXM",
    "captionTranscript": "2012 Dodge Challenger SRT8 392 Coupe Exterior",
    "source": "OEM",
    "photoSrcs": [
        "/dodge/challenger/2012/oem/2012_dodge_challenger_coupe_srt8-392_exm_oem_1_717.jpg",
        "/dodge/challenger/2012/oem/2012_dodge_challenger_coupe_srt8-392_exm_oem_1_185.jpg",
        "/dodge/challenger/2012/oem/2012_dodge_challenger_coupe_srt8-392_exm_oem_1_98.jpg",
        "/dodge/challenger/2012/oem/2012_dodge_challenger_coupe_srt8-392_exm_oem_1_175.jpg",
        "/dodge/challenger/2012/oem/2012_dodge_challenger_coupe_srt8-392_exm_oem_1_815.jpg",
        "/dodge/challenger/2012/oem/2012_dodge_challenger_coupe_srt8-392_exm_oem_1_500.jpg",
        "/dodge/challenger/2012/oem/2012_dodge_challenger_coupe_srt8-392_exm_oem_1_423.jpg",
        "/dodge/challenger/2012/oem/2012_dodge_challenger_coupe_srt8-392_exm_oem_1_2048.jpg",
        "/dodge/challenger/2012/oem/2012_dodge_challenger_coupe_srt8-392_exm_oem_1_400.jpg",
        "/dodge/challenger/2012/oem/2012_dodge_challenger_coupe_srt8-392_exm_oem_1_276.jpg",
        "/dodge/challenger/2012/oem/2012_dodge_challenger_coupe_srt8-392_exm_oem_1_1600.jpg",
        "/dodge/challenger/2012/oem/2012_dodge_challenger_coupe_srt8-392_exm_oem_1_300.jpg",
        "/dodge/challenger/2012/oem/2012_dodge_challenger_coupe_srt8-392_exm_oem_1_196.jpg",
        "/dodge/challenger/2012/oem/2012_dodge_challenger_coupe_srt8-392_exm_oem_1_87.jpg",
        "/dodge/challenger/2012/oem/2012_dodge_challenger_coupe_srt8-392_exm_oem_1_600.jpg",
        "/dodge/challenger/2012/oem/2012_dodge_challenger_coupe_srt8-392_exm_oem_1_396.jpg",
        "/dodge/challenger/2012/oem/2012_dodge_challenger_coupe_srt8-392_exm_oem_1_131.jpg",
        "/dodge/challenger/2012/oem/2012_dodge_challenger_coupe_srt8-392_exm_oem_1_150.jpg"
    ],
    "site": "dam",
    "id": "dam/photo/dodge/challenger/2012/oem/2012_dodge_challenger_coupe_srt8-392_exm_oem_1",
    "authorNames": [
        "Chrysler LLC"
    ],
    "subType": "exterior",
    "vdpOrder": 1,
    "type": "PHOTOS",
    "children": []
}

---------------------------------------------------------------------
'''

    print(json.dumps(photo_data[0], indent=4))
    print('\n'*2 + '|  PHOTO URLS  |')
    print('-'*14 + '\n'*2)
    for photo in photo_data[0]['photoSrcs']:
        stub = photo

        print(photo_url_start + stub)
    print('\n'*2)


def directory(styleID):
    clear()
    #wait('directories')

    looking_at_info = True
    while looking_at_info:
        chose_option = {'1': ' - Get Options',
                        '2': ' - Get Colors',
                        '3': ' - Get Photos',
                        '#': ' - Choose Another Car',
                        '0': ' - Done'}

        print('\nChoose and option:')
        for key in chose_option:
            print key, chose_option[key]

        chosen_option = str(raw_input('\n-->  '))
        while chosen_option not in chose_option.keys():
            chosen_option = str(raw_input('Try again -->  '))

        if chosen_option == '1':
            get_options(styleID)
        elif chosen_option == '2':
            get_colors(styleID)
        elif chosen_option == '3':
            get_photos(styleID)
        elif chosen_option == '#':
            break
        else:
            sys.exit("Thanks!")
