'''
Fuel Parameter Plotting and Curve Fitting.
Need to set standard deviation value to cut the upper and lower unchanging values.
Tested value on given dataset is around 50
'''

import pandas as pd 
import numpy as np 
import sys
import matplotlib.pyplot as plt 
from os import listdir
from os.path import isfile, join
import re
import math
import json

regx = re.compile('(?<![\d.])'       '(?![1-9]\d*(?![\d.])|\d*\.\d*\.)'
                  '0*(?!(?<=0)\.)'
                  '([\d.]+?)'      # the only group , which is kept
                  '\.?0*'
                  '(?![\d.])')

def predictValue(coefficientFileName, valueToPredict):
    # with open(coefficientFileName,'r') as f:
    #     a = f.read()

    # b = a.splitlines()
    # s = []

    # for i in b:
    #     s.append(float(i))
    df = pd.read_json(coefficientFileName,orient='records')
    cf = np.array([])
    for i in range(15,-1,-1):
        cf = np.append(cf, df['a'+str(i)])

    p = np.poly1d(cf)
    pred = p(valueToPredict)

    return pred

def return_coefficient(fileName, degree, analog,std=None):
    df = pd.read_csv(fileName, header=None, error_bad_lines=False)

    y = df[0]
    x1 = df[analog]

    for i in range(50,len(x1),50):
        if np.std(x1[-i:]) > int(std):
            tail = i
            break
    for i in range(50,len(x1),50):
        if np.std(x1[:i]) > int(std):
            head = i
            break

    z1 = np.polyfit(x1, y, int(degree), rcond=0)
    p1 = np.poly1d(z1)

    # print(tail)
    minVoltage = x1[len(x1)-tail]
    maxVoltage = x1[head]

    if minVoltage > maxVoltage:
        temp = minVoltage
        minVoltage = maxVoltage
        maxVoltage = temp

    capacity = math.ceil(p1(x1[len(x1)-tail]))
    reserve = math.floor(p1(x1[head]))

    # print(reseved_lower)
    # print(reseved_upper)

    plt.plot(x1[head:-tail], y[head:-tail], '-')

    plt.plot(x1[head:-tail] ,p1(x1[head:-tail]), '-')

    plt.legend(['Raw Curve', 'Fitted Curve'], loc='upper center')
    plt.show()

    return z1, reserve, capacity, maxVoltage, minVoltage

def plotRaw(folderName, analog):
    #Take all the files under this folder
    files = [f for f in listdir(folderName) if isfile(join(folderName, f))]
    files = [f for f in files if 'csv' in files]

    for ifile in files:
        # print(ifile)
        df = pd.read_csv(join(folderName, ifile), header=None, error_bad_lines=False)

        y = df[0]
        x1 = df[analog]
        # x2 = df[2]
        # for i in range(100,len(x1),100):
        #     if np.std(x1[-i:]) > int(std_dev_limit):
        #         tail = i
        #         break
        # for i in range(100,len(x1),100):
        #     if np.std(x1[:i]) > int(std_dev_limit):
        #         head = i
        #         break

        # plt.plot(x1[head:-tail], y[head:-tail], '-')
        plt.plot(x1, y, '-')

    plt.legend([f for f in files], loc='upper center')
    plt.show()


if len(sys.argv) == 2 and sys.argv[1]=='help':
    print('Supported Usage: ')
    print('1. For Plotting the Curves: python script.py plot FolderContainingCSVFilesPath VoltageLevel')
    print()
    print('2. For Generating Coefficient of fitted Curve: python script.py fit CSVFilePath polyfitDegree voltageLevel StdDeviationThreshold SaveCoefficentFileName')
    print()
    print('3. For Predicting Value: python script.py predict CoefficentFile.json TestValue')
elif len(sys.argv) == 4 and sys.argv[1]=='plot':
    folderName = sys.argv[2]
    volt = sys.argv[3]

    if volt == '5':
        analog = 1
    elif volt == '12':
        analog = 2

    plotRaw(folderName, analog)

elif len(sys.argv) == 4 and sys.argv[1]=='predict':
    coefficientFileName = sys.argv[2]
    inValue = sys.argv[3]

    inValue = int(inValue)
    pred = predictValue(coefficientFileName, inValue)
    print(pred)

elif len(sys.argv) == 6 and sys.argv[1]=='fit':
    fileName = sys.argv[2]
    degree = sys.argv[3]
    volt = sys.argv[4]
    std_dev_limit = sys.argv[5]
    saveFileName = fileName.split('/')[1]  # For windows machine use backslash 
    saveFileName = 'Recharge/Coefficient/'+ saveFileName.split('.')[0] + '.json'

    if volt == '5':
        analog = 1
    elif volt == '12':
        analog = 2

    coefficients, reserve, capacity, maxVoltage, minVoltage = return_coefficient(fileName, degree, analog, std_dev_limit)
    coefficients = ['{:.80f}'.format(i) for i in coefficients]
    coef = []
    for q in coefficients:
        coef.append(regx.sub('\\1', q))
    
    dic = {}
    dic['hcf'] = '1'
    for i,z in enumerate(coef):
        dic['a'+str(int(degree)-i)] = z
    
    dic['capacity'] = str(capacity)
    dic['reserve'] = str(reserve)
    dic['maxVoltage'] = str(maxVoltage)
    dic['minVoltage'] = str(minVoltage)

    diclist = [dic]
    # jsonData = json.dumps(dic)

    # print(jsonData)
    with open(saveFileName, 'w') as f:
        json.dump(diclist, f)


elif len(sys.argv) > 7:
    print('Too many Argument to Unpack. To Check the usage run - python script.py')

elif len(sys.argv) < 4:
    print('Not Enough Argument to Unpack. To Check the usage run - python script.py')