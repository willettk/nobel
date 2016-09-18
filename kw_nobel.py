# kw_nobel

from collections import Counter
from astropy.io import ascii
from datetime import date

nobelpath = '/Users/willettk/Documents/Nobel/nobel/'

def died_in_different_country(api, verbose=False):

    dlist = []

    for l in api.laureates.all():
        try:
            dc_code = l.died_country.code
        except AttributeError:
            dc_code = None
        try:
            bc_code = l.born_country.code
        except AttributeError:
            bc_code = None
        try:
            surname = l.surname
        except AttributeError:
            surname = None

        if None not in (bc_code,dc_code) and bc_code != dc_code and surname != None:
            if verbose:
                print '%30s -- Born in %45s, died in %45s' % (l.surname,l.born_country,l.died_country)
            dlist.append(l)

    return dlist

def died_in_same_country(api, verbose=False):

    dlist = []

    for l in api.laureates.all():
        try:
            dc_code = l.died_country.code
        except AttributeError:
            dc_code = None
        try:
            bc_code = l.born_country.code
        except AttributeError:
            bc_code = None
        try:
            surname = l.surname
        except AttributeError:
            surname = None

        if None not in (bc_code,dc_code) and bc_code == dc_code and surname != None:
            if verbose:
                print '%30s -- Born in %45s, died in %45s' % (l.surname,l.born_country,l.died_country)
            dlist.append(l)

    return dlist

def not_dead(api, verbose=False):

    dlist = []

    for l in api.laureates.all():
        try:
            bc_code = l.born_country.code
        except AttributeError:
            bc_code = None
        try:
            died = l.died
        except AttributeError:
            died = None
        try:
            surname = l.surname
        except AttributeError:
            surname = None

        if (bc_code != None) and (died == None) and (surname != None):
            if verbose:
                print '%15s -- Born in %30s; not dead as of %s' % (l.surname,l.born_country,date.today().strftime('%B %d, %Y'))
            dlist.append(l)

    return dlist

def most_common_emigration(dlist,n=10,showall=False):

    cnt = Counter()
    for d in dlist:
        country_string = '%s_%s' % (d.born_country.code,d.died_country.code)
        cnt[country_string] += 1

    if showall:
        n = len(cnt)
    mcp = cnt.most_common(n)

    return mcp

def aggregate_countries(llist,n=10,showall=False):

    cnt = Counter()
    for l in llist:
        cnt[l.born_country.code] += 1

    if showall:
        n = len(cnt)
    mcp = cnt.most_common(n)

    return mcp

def geocode_paths(api,paths):

    # read in avg. lat/lon coordinates of countries
    data = ascii.read('%s%s' % (nobelpath,'country_coo.csv'),names=('code','lat','lon'))
    code,lat,lon = data['code'],data['lat'],data['lon']

    # open file
    f = open('%s%s' % (nobelpath,'emigrations_R.csv'),'wb')
    f.write('c1 c2 lon1 lat1 lon2 lat2 cnt \n')
    # loop over paths
    for em in paths:
        c1,c2 = em[0].split('_')
        # check if country code is in list
        if c1 in code and c2 in code:
            lat1 = lat[code == c1]
            lon1 = lon[code == c1]
            lat2 = lat[code == c2]
            lon2 = lon[code == c2]
            coo_string = '%2s %2s %7.3f %7.3f %7.3f %7.3f %3i \n' % (c1,c2,lon1.data[0],lat1.data[0],lon2.data[0],lat2.data[0],em[1])
            f.write(coo_string)
        else:
            print c1,c2

    f.close()

    return None

def geocode_points(api,points):

    # read in avg. lat/lon coordinates of countries
    data = ascii.read('%s%s' % (nobelpath,'country_coo.csv'),names=('code','lat','lon'))
    code,lat,lon = data['code'],data['lat'],data['lon']

    # open file
    f = open('%s%s' % (nobelpath,'points_R.csv'),'wb')
    f.write('c1 lon1 lat1 cnt \n')
    # loop over points
    for em in points:
        c1 = em[0]
        # check if country code is in list
        if c1 in code:
            lat1 = lat[code == c1]
            lon1 = lon[code == c1]
            coo_string = '%2s %7.3f %7.3f %3i \n' % (c1,lon1.data[0],lat1.data[0],em[1])
            f.write(coo_string)
        else:
            print c1

    f.close()

    return None

def continents_born(api,cont_string):

    asia = ('Afghanistan', 'Bahrain', 'Bangladesh', 'Bhutan', 'Brunei', 'Cambodia', 'China', 'East Timor', 'India', 'Indonesia', 'Iran', 'Iraq', 'Israel', 'Japan', 'Jordan', 'Kazakhstan', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Lebanon', 'Malaysia', 'Maldives', 'Mongolia', 'Myanmar', 'Nepal', 'North Korea', 'Oman', 'Pakistan', 'Palestine', 'Philippines', 'Qatar', 'Russia', 'Saudi Arabia', 'Singapore', 'South Korea', 'Sri Lanka', 'Syria', 'Taiwan', 'Tajikistan', 'Thailand', 'Turkey', 'Turkmenistan', 'United Arab Emirates', 'Uzbekistan', 'Vietnam', 'Yemen')
    southamerica = ('Argentina','Bolivia','Chile','Paraguay','Uruguay','Bolivia','Peru','Ecuador','Venezuela','Colombia','Guyana','Suriname')
    northamerica = ('Antigua and Barbuda', 'Bahamas', 'Barbados', 'Belize', 'Canada', 'Costa Rica', 'Cuba', 'Dominica', 'Dominican Republic', 'El Salvador', 'Grenada', 'Guatemala', 'Haiti', 'Honduras', 'Jamaica', 'Mexico', 'Nicaragua', 'Panama', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Trinidad and Tobago', 'USA')
    europe = ('Albania', 'Andorra', 'Armenia', 'Austria', 'Azerbaijan', 'Belarus', 'Belgium', 'Bosnia and Herzegovina', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'Estonia', 'Finland', 'France', 'Georgia', 'Germany', 'Greece', 'Hungary', 'Iceland', 'Ireland', 'Italy', 'Kosovo', 'Latvia', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macedonia', 'Malta', 'Moldova', 'Monaco', 'Montenegro', 'The Netherlands', 'Norway', 'Poland', 'Portugal', 'Romania', 'Russia', 'San Marino', 'Serbia', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Turkey', 'Ukraine', 'United Kingdom', 'Vatican City')
    oceania=('Australia', 'Fiji', 'Kiribati', 'Marshall Islands', 'Micronesia', 'Nauru', 'New Zealand', 'Palau', 'Papua New Guinea', 'Samoa', 'Solomon Islands', 'Tonga', 'Tuvalu', 'Vanuatu')
    africa=('Algeria', 'Angola', 'Benin', 'Botswana', 'Burkina Faso', 'Burundi', 'Cameroon', 'Cape Verde', 'Central African Republic', 'Chad', 'Comoros', "Cote d'Ivoire", 'Democratic Republic of the Congo', 'Djibouti', 'Egypt', 'Equatorial Guinea', 'Eritrea', 'Ethiopia', 'Gabon', 'Gambia', 'Ghana', 'Guinea', 'Guinea-Bissau', 'Kenya', 'Lesotho', 'Liberia', 'Libya', 'Madagascar', 'Malawi', 'Mali', 'Mauritania', 'Mauritius', 'Morocco', 'Mozambique', 'Namibia', 'Niger', 'Nigeria', 'Republic of the Congo', 'Rwanda', 'Sao Tome and Principe', 'Senegal', 'Seychelles', 'Sierra Leone', 'Somalia', 'South Africa', 'South Sudan', 'Sudan', 'Swaziland', 'Tanzania', 'Togo', 'Tunisia', 'Uganda', 'Zambia', 'Zimbabwe') 

    cont_dict = {'africa':africa,'asia':asia,'northamerica':northamerica,'southamerica':southamerica,'europe':europe,'oceania':oceania}

    for country in cont_dict[cont_string]:
        print country
        for l in api.laureates.filter(born_country = country):
            print '   %s' % l

    return None
