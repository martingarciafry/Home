# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 17:45:03 2019

@author: Moya
"""
import numpy as np

import numpy as np

state = np.arange(7)

hhCode = np.arange(54) 
stateCode = np.arange(7) + 1
segmenCode = np.arange(8) + 1

state_hh   =  {1:[20,21,5,23,52,53,54,16] , 
               2:[20,21,6,23,52,53,54,16] ,  
               3:[20,21,5,23,52,53,54] ,  
               4:[53,20,21,5,6,23,52,54,16] ,  
               5:[53,20,6,21,23,52,54,16] ,  
               6:[20,21,5,23,52,53,54] ,  
               7:[6,21,52,53,54] }
   
             

#IMPORTANT A: Input DataBase "Here"
#dbAd = np.loadtxt("Adultos_DBFinal.csv", skiprows=1, delimiter= ",", dtype= np.int)

#IMPORTANT 1: Update Last Interation File Name: "testAd_G2" (G1, G2, G3, GN) Interation+Date 
dbAd = np.loadtxt("Copy_testAd_G05_20200318.csv", skiprows=1, delimiter= ",", dtype= np.int)

#IMPORTANT 2: Switch Off After First Iteration
#dbAd[:,2] -= 1

#IMPORTANT B: Input DataBase "Here"
#dbHh = np.loadtxt("Household_DBFinal.csv", skiprows=1, delimiter= ",", dtype= np.int)[:,1:]

#IMPORTANT 3: Update New Interation File Name "Here: FileName.csv" (Every Interation+1) 
dbHh = np.loadtxt("Copy_testHh_G05_20200318.csv", skiprows=1, delimiter= ",", dtype= np.int)[:,1:]

#IMPORTANT C: Dont Modify this Part
db_adultPerHh = np.loadtxt("AdultsPerHousehold_final.csv", skiprows=1, delimiter= ",")[:,1]



ThrSeg = {1: 18, # segmentation Progressist   ## Threshold value for segmentation
          2: 15, # segmentation modern
          3: 10, # segmentation austere
          4: 6, # segmentation formalist
          5: 1} # segmentation conservative

codeHhWith3Ad = np.where( db_adultPerHh == 3 )
codeHhWith2Ad = np.where( db_adultPerHh == 2 )
codeHhWith1Ad = np.where( db_adultPerHh == 1 )

#print(codeHhWith1Ad)

def createGroup(dbHh, dbAd, stateCode=1):
    hhCodes = np.array( state_hh[ stateCode ] )   # getting the type of households that can belong to stateCode
    indxHh = np.where( np.isin(dbHh, hhCodes)[:,0] )[0]
    indxAd = np.where( np.isin(dbAd, indxHh)[:,0] )[0]
    dbHhFilt = dbHh[indxHh,:]
    dbAdFilt = dbAd[indxAd,:]
    
    segThreshold = np.array([18,15,10,6,1])    # maximum values for each segementation class
    currentAmount = np.zeros_like(segThreshold)
    
    indxHhWith3Ad = np.where( np.isin(dbAdFilt[:,1] , codeHhWith3Ad ))[0]
    indxHhWith2Ad = np.where( np.isin(dbAdFilt[:,1] , codeHhWith2Ad ))[0]
    indxHhWith1Ad = np.where( np.isin(dbAdFilt[:,1] , codeHhWith1Ad ))[0]
    
    #### Selecting households composed by 3 adults
    maxIter = 5000
    counter = 0
    numFam3Ad = 0
    print("dbAdFilt:")
    print(dbAdFilt)
    while True:
#        segType = np.random.choice([1,2,3,4,5])
        segType = np.random.choice( np.unique(dbAdFilt[:,2]) )
        print("segType: ", segType)
        indxSeg = np.where( np.logical_and( dbAdFilt[:,2] == segType , dbAdFilt[:,3] == 0) )[0]
        if not len(indxSeg):
            print("there are not adults with segmentation %d available" % (segType))
            counter += 1
            if counter >= maxIter: 
            
                break
            continue
        indxSeg = indxSeg[ np.isin( indxSeg , indxHhWith3Ad ) ]
        if not len(indxSeg):
            print("there are no adults with segmentation %d that belong to a family of 3 adults" % (segType))
            counter += 1
            if counter >= maxIter:
                break
            continue
        indxSeg =  np.where( np.isin( dbAdFilt[:,0 ] , dbAdFilt[indxSeg , 0] ) )[0]


        indxSegChoiced = np.random.choice(indxSeg)
        aDSelected = dbAdFilt[indxSegChoiced]
        indxFamilySel = np.where( dbAdFilt[:,0] == aDSelected[0] )[0]
        famSelected = dbAdFilt[indxFamilySel , :]

        increment = np.copy(currentAmount)
        print(increment)
        print(famSelected[:,2])
        for n in famSelected[:,2]:
            increment[n] += 1
       
        counter += 1
        if np.sum( (increment - segThreshold) > 0 ):
            if counter >= maxIter:
                break
            continue
        currentAmount = increment
        numFam3Ad += 1
        if numFam3Ad == 8:
            dbAdFilt[indxFamilySel , 3] +=1
            break
        dbAdFilt[indxFamilySel , 3] +=1
    
    #### Insertando ahora las familias compuestas por 2 adultos
    maxIter = 1000
    counter = 0
    numFam2Ad = 0
    
    while True:
#        segType = np.random.choice(8)
        segType = np.random.choice( np.unique(dbAdFilt[:,2]) )
        indxSeg = np.where( np.logical_and( dbAdFilt[:,2] == segType , dbAdFilt[:,3] == 0) )[0]
        indxSeg = indxSeg[ np.isin( indxSeg , indxHhWith2Ad ) ]
        indxSeg =  np.where( np.isin( dbAdFilt[:,0 ] , dbAdFilt[indxSeg , 0] ) )[0]

        if len(indxSeg) == 0:
            counter += 1
            if counter > maxIter:
                break
            continue
        
        indxSegChoiced = np.random.choice(indxSeg)
        aDSelected = dbAdFilt[indxSegChoiced]
        indxFamilySel = np.where( dbAdFilt[:,0] == aDSelected[0] )[0]
        famSelected = dbAdFilt[indxFamilySel , :]
        
        increment = np.copy(currentAmount)
        for n in famSelected[:,2]:
            increment[n] += 1
        
        counter += 1
        
        if np.sum( (increment - segThreshold) > 0 ):
            if counter >= maxIter:
                break
            continue
        
        currentAmount = increment

        numFam2Ad += 1
        if numFam2Ad == 8:
            dbAdFilt[indxFamilySel , 3] +=1
            break
        dbAdFilt[indxFamilySel , 3] +=1
    
    #### Selecting households composed by 1 adults
    maxIter = 5000
    counter = 0
    numFam1Ad = 0
    
    while True:
#        segType = np.random.choice(8)
        segType = np.random.choice( np.unique(dbAdFilt[:,2]) )
        indxSeg = np.where( np.logical_and( dbAdFilt[:,2] == segType , dbAdFilt[:,3] == 0) )[0]
        indxSeg = indxSeg[ np.isin( indxSeg , indxHhWith1Ad ) ]
#        print(indxSeg)
        indxSeg =  np.where( np.isin( dbAdFilt[:,0 ] , dbAdFilt[indxSeg , 0] ) )[0]
#        print(indxSeg)
#        print(segType)
#        print( dbAdFilt[indxSeg , :] ) 
#        print(indxSeg)
#        print(numFam1Ad)
        if len(indxSeg) == 0:
            counter += 1
            if counter > maxIter:
                break
            continue
        
        indxSegChoiced = np.random.choice(indxSeg)
        aDSelected = dbAdFilt[indxSegChoiced]
        indxFamilySel = np.where( dbAdFilt[:,0] == aDSelected[0] )[0]
        famSelected = dbAdFilt[indxFamilySel , :]
        
        increment = np.copy(currentAmount)
        for n in famSelected[:,2]:
            increment[n] += 1
        
        counter += 1
        
        if np.sum( (increment - segThreshold) > 0 ):
            if counter >= maxIter:
                break
            continue
        
        currentAmount = increment

        numFam1Ad += 1
        if numFam1Ad == 10:
            dbAdFilt[indxFamilySel , 3] +=1
            break
        dbAdFilt[indxFamilySel , 3] +=1
    
    # Refining with remaining 1 adult HH
    print(currentAmount)
    for st in range(5):
        print(currentAmount[st], segThreshold[st] )
        dif = segThreshold[st] - currentAmount[st]
        if dif > 0:
            print("need to improve", dif)
            for n in range(dif):
                indxSeg = np.where( np.logical_and( dbAdFilt[:,2] == st , dbAdFilt[:,3] == 0) )[0]
                indxSeg = indxSeg[ np.isin( indxSeg , indxHhWith1Ad ) ]
                if len(indxSeg) == 0:
                    print("no additional adults of segementation %d" % st)
                    break
                else:
                    print("there are additional adults")
                    
                    
    
    print(currentAmount, np.sum(currentAmount))
    print(counter)
    print(numFam3Ad, numFam2Ad, numFam1Ad)    
    print()
#    for i in range(dbAdFilt.shape[0]):
#        print(dbAdFilt[i])
    dbAd_selected = np.copy(dbAd)
    dbAd_selected[indxAd,:] = dbAdFilt
    
    indxTmp =  np.unique( dbAd_selected[dbAd_selected[:,-1] == 1 , 0] )
    print(indxTmp)
    
    dbHh_selected = np.zeros((dbHh.shape[0],3))
    dbHh_selected[:,1:] = dbHh
    dbHh_selected[:,0] = np.arange(dbHh.shape[0])
#    indxTmp2 = np.isin(dbHh_selected[:,0] , indxTmp)
#    print(dbHh_selected[:,0])
#    print(indxTmp)
    dbHh_selected[indxTmp , 2] += 1 

#IMPORTANT 1: Update New Output File Number (G1, G2, G3, GN) Here: "testAd_G4" (Every Output Number+Date)        
    np.savetxt("testAd_G03_20200318.csv",dbAd_selected, delimiter=',', header="SurveyHHCode,HHCode,TypeOfSegmentation,FullZeros", fmt="%d")
    np.savetxt("testHh_G03_20200318.csv",dbHh_selected, delimiter=',', header="HH Num,HH_type,FullZeros", fmt="%d")
    return 

if __name__ == "__main__":
    createGroup(dbHh, dbAd, stateCode=1)
    
# IMPORTANT: Insert Piece of Code that asks "what trial number is it?", (Increment+1) Fullzeros every iteration.  
    
    