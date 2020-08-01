import os
import re
import sys
import json
import pickle
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import hypothesis_test

def deduplication_name(filename):
    name_list = []
    f = open(filename)
    line = f.readline()
    while line:
        if line not in name_list:
            name_list.append(line)
        line = f.readline()
    f = open('deduplication_name_list.txt', 'w')
    for i in range(len(name_list)):
        f.write(name_list[i])
        name_list[i] = name_list[i].replace('\n', '')
        name_list[i] = name_list[i].replace('/', '')
        if re.findall('[Uu]niversity', name_list[i]) != [] or \
                        re.findall('[Cc]ollege', name_list[i]) != [] or \
                            re.findall('[Ii]nstitute', name_list[i]) != []:
            name_list[i] = ''
    f.close()
    return name_list

def count_num(filename):
    male = 0
    female = 0

    white = 0
    hispano = 0
    asian = 0
    black = 0

    filename = filename.replace('\n', '')
    data = pd.read_csv('CSV_files_NLP/'+filename)
    for g in data['Gender']:
        if g == 'male':
            male += 1
        if g == 'female':
            female += 1
    for i in data['Race']:
        if i == 'W_NL':
            white += 1
        if i == 'HL':
            hispano += 1
        if i == 'A':
            asian += 1
        if i == 'B_NL':
            black += 1
    population = male + female

    return {'Population': population, 
    'male': male, 
    'female': female, 
    'white': white, 
    'hispano': hispano,
    'asian': asian,
    'black': black}

def arrange_files(filename):
    acl = {}
    emnlp = {}
    naacl = {}
    re_name = '[A-Za-z]{2,6}'
    re_year = '\d{4}'
    f = open(filename)
    line = f.readline()
    while line:
        conf_name = re.findall(re_name, line)[0]
        conf_year = re.findall(re_year, line)[0]
        if conf_name == 'acl':
            acl[conf_year] = count_num(line)
        if conf_name == 'emnlp':
            emnlp[conf_year] = count_num(line)
        if conf_name == 'naacl':
            naacl[conf_year] = count_num(line)
        line = f.readline()
    return acl, emnlp, naacl

def analysis_name(name_list, api_key):
    name_dict = {}
    name_dict = pickle.load(open('name_dict.pickle', "rb"))
    for name in name_list:
        if name not in name_dict and name.count(' ') > 0:
            info_dict = {}
            api_link_gender = 'http://v2.namsor.com/NamSorAPIv2/api2/json/genderFull/' + name
            parseName = 'https://v2.namsor.com/NamSorAPIv2/api2/json/parseName/' + name
            api_race = 'https://v2.namsor.com/NamSorAPIv2/api2/json/usRaceEthnicity/'

            gender = requests.get(api_link_gender, headers={'X-API-KEY': api_key})
            fs_name = requests.get(parseName, headers={'X-API-KEY': api_key})
            api_dict = json.loads(gender.text)
            info_dict['Gender'] = api_dict['likelyGender']
            fs_name = json.loads(fs_name.text)
            api_race += fs_name['firstLastName']['firstName'] + '/' + fs_name['firstLastName']['lastName']
            race = requests.get(api_race, headers={'X-API-KEY': api_key})
            race = json.loads(race.text)
            info_dict['Race'] = race['raceEthnicity']
            name_dict[name] = info_dict

            print(name_dict)
            print('\n')
            pickle.dump(name_dict, open('name_dict.pickle', "wb"))


    gender = pickle.load(open('name_dict.pickle', "rb"))
    print(gender)
    print("===================================")
    print('Finshed')
    print("===================================")
    return None

def set_grToCSV(file_list):
    name_dict = pickle.load(open('name_dict.pickle', "rb"))
    
    f = open(file_list)
    line = f.readline()
    while line:
        line = line.replace('\n', '')
        data = pd.read_csv(line)
        for i in range(len(data['Name'])):
            if data['Name'][i] in name_dict:
                gender = name_dict[data['Name'][i]]['Gender']
                race = name_dict[data['Name'][i]]['Race']
                data['Gender'][i] = gender
                data['Race'][i] = race
        data.to_csv(line, index=False, sep=',')

        line = f.readline()

def draw_bar(conf, year, arg1, arg2=None, arg3=None, arg4=None, proportion=None):
    x_sy = year
    x = np.arange(len(year)) #总共有几组，就设置成几，我们这里有三组，所以设置为3
    if arg3 == None:
        total_width, n = 0.8, 2  # 有多少个类型，只需更改n即可，比如这里我们对比了四个，那么就把n设成4
    else:
        total_width, n = 0.8, 4
    width = total_width / n
    x = x - (total_width - width) / 2
    if arg2 == None:
        plt.bar(range(len(arg1)), arg1, 0.4, color='b', alpha = 0.8,label='Population')
        # plt.title('Population for ' + conf)
        title = 'Population for ' + conf
    elif arg3 == None:
        plt.bar(x, arg1, color = "r",width=width,label='Female')
        plt.bar(x + width, arg2, color = "b",width=width,label='Male')
        if proportion != None:
            # plt.title('Gender Proportion for ' + conf)
            title = 'Gender Proportion for ' + conf
        else:
            # plt.title('Gender Population for ' + conf)
            title = 'Gender Population for ' + conf
    else:
        plt.bar(x, arg1, color = "r",width=width,label='White')
        plt.bar(x + width, arg2, color = "b",width=width,label='Hispano')
        plt.bar(x + 2 * width, arg3 , color = "c",width=width,label='Asian')
        plt.bar(x + 3 * width, arg4 , color = "g",width=width,label='Black')
        if proportion != None:
            # plt.title('Race Proportion for ' + conf)
            title = 'Race Proportion for ' + conf
        else:
            # plt.title('Race Population for ' + conf)
            title = 'Race Population for ' + conf
    plt.title(title)
    plt.xlabel("Year")
    if proportion != None:
        plt.ylabel("Percentage")
    else:
        plt.ylabel("Population")
    plt.legend(loc = "best")
    plt.xticks(range(0,len(year)), x_sy)
    if proportion != None:
        my_y_ticks = np.arange(0, 110, 10)
        plt.ylim((0, 110))
    else:
        my_y_ticks = np.arange(0, 6100, 500)
        plt.ylim((0, 6100))
    plt.yticks(my_y_ticks)
    if arg2 == None:
        for x,y in enumerate(arg1):
            plt.text(x, y+100,'%s' %y,ha='center')
    elif arg3 == None:
        for x,y in enumerate(arg1):
            plt.text(x, y+5,'%s' %y,ha='right')
        for x,y in enumerate(arg2):
            plt.text(x, y+5,'%s' %y,ha='left')
    else:
        for x,y in enumerate(arg1):
            plt.text(x-0.2, y+5,'%s' %y,ha='right')
        for x,y in enumerate(arg2):
            plt.text(x, y+5,'%s' %y,ha='right')
        for x,y in enumerate(arg3):
            plt.text(x, y+5,'%s' %y,ha='left')
        for x,y in enumerate(arg4):
            plt.text(x+0.2, y+5,'%s' %y,ha='left')
    # plt.savefig(title + '.png')
    plt.show()

def count_proportion(pop, arg):
    result = []
    for i in range(len(pop)):
        result.append(round((arg[i]/pop[i])*100, 2))
    return result

def draw_linear_regression(year, pop):
    sns.set(style="ticks")
    data = {'year':year, 'pop':pop}
    df = pd.DataFrame(data)
    sns.lmplot(x="year", y="pop", data=df, order=1)
    plt.show()

def create_diagram(conf_dict, conf, info):
    year = []
    pop = []
    female = []
    male = []
    white = []
    hispano = []
    asian = []
    black = []

    for key in conf_dict.keys():
        year.append(int(key))
        pop.append(conf_dict[key]['Population'])
        male.append(conf_dict[key]['male'])
        female.append(conf_dict[key]['female'])
        white.append(conf_dict[key]['white'])
        hispano.append(conf_dict[key]['hispano'])
        asian.append(conf_dict[key]['asian'])
        black.append(conf_dict[key]['black'])
        
    year.reverse()
    pop.reverse()
    female.reverse()
    male.reverse()
    white.reverse()
    hispano.reverse()
    asian.reverse()
    black.reverse()
    if info == 'population':
        draw_bar(conf, year, pop)
        draw_linear_regression(year, pop)
    if info == 'gender':
        draw_bar(conf, year, female, male)
        # draw_linear_regression(year, female)
        draw_bar(conf, year, count_proportion(pop, female), \
            count_proportion(pop, male), None, None, True)
    if info == 'race':
        draw_bar(conf, year, white, hispano, asian, black)
        draw_bar(conf, year, count_proportion(pop, white), \
            count_proportion(pop, hispano), count_proportion(pop, asian), \
                count_proportion(pop, black), True)
    return None

def run_hy_test(data_set, conf, year1, year2):
    print("Female proportion did not change in {} and {} in {}".format(year1, year2, conf))
    hypothesis_test.hyp_test(data_set[year1]['Population'], data_set[year1]['female'], data_set[year2]['Population'], data_set[year2]['female'])

    print("\nWhite participants proportion did not change in {} and {} in {}".format(year1, year2, conf))
    hypothesis_test.hyp_test(data_set[year1]['Population'], data_set[year1]['white'], data_set[year2]['Population'], data_set[year2]['white'])

    print("\nHispano participants proportion did not change in {} and {} in {}".format(year1, year2, conf))
    hypothesis_test.hyp_test(data_set[year1]['Population'], data_set[year1]['hispano'], data_set[year2]['Population'], data_set[year2]['hispano'])

    print("\nAsian participants proportion did not change in {} and {} in {}".format(year1, year2, conf))
    hypothesis_test.hyp_test(data_set[year1]['Population'], data_set[year1]['asian'], data_set[year2]['Population'], data_set[year2]['asian'])

    print("\nBlack participants proportion did not change in {} and {} in {}".format(year1, year2, conf))
    hypothesis_test.hyp_test(data_set[year1]['Population'], data_set[year1]['black'], data_set[year2]['Population'], data_set[year2]['black'])

    print('\n', '*'*70)

def test_two_conf(ds1, ds2, conf1, conf2, year):
    print("Female proportion does not change between {} and {} in {}".format(conf1, conf2, year))
    hypothesis_test.hyp_test(ds1[year]['Population'], ds1[year]['female'], ds2[year]['Population'], ds2[year]['female'])

    print("\nWhite participants proportion does not change between {} and {} in {}".format(conf1, conf2, year))
    hypothesis_test.hyp_test(ds1[year]['Population'], ds1[year]['white'], ds2[year]['Population'], ds2[year]['white'])

    print("\nHispano participants proportion does not change between {} and {} in {}".format(conf1, conf2, year))
    hypothesis_test.hyp_test(ds1[year]['Population'], ds1[year]['hispano'], ds2[year]['Population'], ds2[year]['hispano'])

    print("\nAsian participants proportion does not change between {} and {} in {}".format(conf1, conf2, year))
    hypothesis_test.hyp_test(ds1[year]['Population'], ds1[year]['asian'], ds2[year]['Population'], ds2[year]['asian'])

    print("\nBlack participants proportion does not change between {} and {} in {}".format(conf1, conf2, year))
    hypothesis_test.hyp_test(ds1[year]['Population'], ds1[year]['black'], ds2[year]['Population'], ds2[year]['black'])

    print('\n', '*'*70)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == 'analysis':
            api_key = '61f8c3dc68d36e701dd558f668eb4fb9' #prof's key
            name_list = deduplication_name('total_name_list.txt')
            pickle.dump(name_list, open('name_list.pickle', 'wb'))
            name_list = pickle.load(open('name_list.pickle', "rb"))
            analysis_name(name_list, api_key)

        if sys.argv[1] == 'setgr':
            set_grToCSV('csv_list.txt')

        if sys.argv[1] == 'diagram':
            acl, emnlp, naacl = arrange_files('csv_list.txt')

            create_diagram(acl, 'ACL', 'population')
            create_diagram(acl, 'ACL', 'gender')
            create_diagram(acl, 'ACL', 'race')

            create_diagram(emnlp, 'EMNLP', 'population')
            create_diagram(emnlp, 'EMNLP', 'gender')
            create_diagram(emnlp, 'EMNLP', 'race')

            create_diagram(naacl, 'NAACL', 'population')
            create_diagram(naacl, 'NAACL', 'gender')
            create_diagram(naacl, 'NAACL', 'race')

    else:
        deduplication_name('Support_file_NLP/total_name_list.txt')

        acl, emnlp, naacl = arrange_files('CSV_files_NLP/csv_list.txt')

        # print(acl)
        # print(emnlp)
        # print(naacl)

        # print('ACL')
        # for key in acl:
        #     print(key, acl[key])

        # print('EMNLP')
        # for key in emnlp:
        #     print(key, emnlp[key])

        # print("NAACL")
        # for key in naacl:
        #     print(key, naacl[key])
            
        run_hy_test(acl, 'ACL', '2010', '2019')
        run_hy_test(emnlp, 'EMNLP', '2010', '2019')
        run_hy_test(naacl, 'NAACL', '2010', '2019')
        
        test_two_conf(acl, emnlp, 'ACL', 'EMNLP', '2010')
        test_two_conf(acl, naacl, 'ACL', 'NAACL', '2010')
        test_two_conf(emnlp, naacl, 'EMNLP', 'NAACL', '2010')