#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 11:43:56 2022

@author: martingarcia
"""
 
import numpy as np 

#Load the input dataset titled: Training Dataset
TrainDB = np.loadtxt("input_dataset.csv", skiprows=1, delimiter= ",", dtype= float) 

#This step optimizes 'Heights_20m' and Canopy 'Heights_Mean' to eliminate no_data values in last column of the dataset 'TrainDB'. 
CanoFilt = np.array(np.where(TrainDB[:,5]==0, TrainDB[:,4],TrainDB[:,5]))
Train = np.column_stack((TrainDB, CanoFilt))
TrainFilt = np.delete(Train, np.s_[4:6], axis=1) 
np.savetxt("00_Optimized Dataset.csv",TrainFilt, delimiter=',', header="N, classCode, LCP_Band, LCP_Height, Ground_H, Slope, SolarRad, WetnessInd, Blue, NIR, SWIR_1, NDWI_I, NDVI, NDWI_II, NIR_SWIR_2, SWIR_1_SWIR_2, TassCapGn, TassCapWet, SAVI, BN, North, East, B1, B2, B3, B4, B5, B6, B7, B8, B8A, B11, B12, Canopy Heights", fmt="%f")

## Dont forget to add or subtract header titles if the Input Data Template has been altered.

                                       
                                     #Class 01: Dense Short Vegetation

TrainFilt_Copy = TrainFilt.copy()
a = np.split(TrainFilt_Copy, [36728], axis=0) 
#split Class 01 data from the 'Training Dataset': Set the Row Value for the first class above. 

#_1_Thematic_Agreement_Classifier.

#Class 01: Data Input
Class01 = np.array(a[0])
print ("Class 01: Dense Short Vegetation")

#CAUTION: If UTF-8-data is +/- 10 degress from equator, change metric ranges in yellow below [values in brackets]. 
    
#1.1_NDVI (Red-Nir/Red+NIR: metrics in yellow)
filtIndx = np.array(np.where((Class01[:,12]>0.090) & (Class01[:,12]<0.853), 1, 0))
b = np.column_stack((Class01,filtIndx))
print ("(1) NVDI is queud and added to the list:", b[:,-1])
                    
#1.2_(Wetness Index: metrics in yellow)
filtIndx2 = np.array(np.where((b[:,7]>-3.810)&(b[:,7]<8.410), 1, 0))
c = np.column_stack((b,filtIndx2))
print ("(2) Wetness index is queud and added to the list:", c[:,-1])

#1.3_(Solar Radiation:  metrics in yellow)
filtIndx3 = np.array(np.where((c[:,6]>4647.26)&(c[:,6]<7870.77), 1, 0))
d = np.column_stack((c,filtIndx3))
print ("(3) Solar Radiation is queud and added to the list:", d[:,-1])

#1.4_(NIR_SWIR2: metrics in yellow)
filtIndx4 = np.array(np.where((d[:,14]>-0.033)&(d[:,14]<0.756), 1, 0))
e = np.column_stack((d,filtIndx4))
print ("(4) NIR_SWIR2 is queud and added to the list:", e[:,-1])

#1.5_(Tasseled Cap Greenness: metrics in yellow)
filtIndx5 = np.array(np.where((e[:,16]>-0.064)&(e[:,16]<0.319), 1, 0))
f = np.column_stack((e,filtIndx5))
print ("(5) Tasseled Cap Greenness is queud and added to the list:", e[:,-1])

#1_Thematic Agreement. Additional columns change the column ranges and indexes.
Agreement01 = np.where((np.sum(f[:,34:39], axis=1) ==5), 1, 0)
A01 = np.column_stack((f, Agreement01))
indx01 = np.delete(A01, np.s_[34:39], axis=1) 
print("Thematic Agreement:", indx01[:,-1])

#_2_Class Vetting with Forest heights.

nonVeg = np.where((indx01[:,3]<=5), 1, 0)
A02 = np.column_stack((indx01, nonVeg))
print("Class Vetting:", A02[:,-1])

#_3_Correlation between ICESat-2 and Forest Height Product.

n = A02[:,3] #Forest Height column.
m = A02[:,33] #Optimized LiDAR Canopy Height Column.
o=np.where((n>=(m-6))&(n<=(m+6)), 1, 0)
A03 = np.column_stack((A02, o))
print ("LiDAR Agreement:", A03[:,-1])

#_4_Reliability Levels: Save calibrated Data to File. 

Sum_1 = A03[:,34:37].sum(axis=1)
print("Class 01: Reliability Levels", Sum_1)
a04_1 = np.column_stack((A03, Sum_1))
np.savetxt("01_Dense Short Vegetation.csv", a04_1, delimiter=',', header="N, classCode, LCP_Band, LCP_Height, Ground_H, Slope, SolarRad, WetnessInd, Blue, NIR, SWIR_1, NDWI_I, NDVI, NDWI_II, NIR_SWIR_2, SWIR_1_SWIR_2, TassCapGn, TassCapWet, SAVI, BN, North, East, B1, B2, B3, B4, B5, B6, B7, B8, B8A, B11, B12, Canopy Height, Thematic Agreement, Class Height, Lidar Vetting, Reliability Level", fmt="%f")

                                                   
                                             #Class 02: Open Tree Cover

a_2 = np.split(a[1], [36788], axis=0) 
#split Class data from the 'Training Dataset': Set the number of unit rows for the class above.

#_1_Thematic_Agreement_Classifier.

Class02 = np.array(a_2[0])
print ("*")
print ("Class 02: Open Tree Cover")

#1.1_NDVI: metrics in yellow.
filtIndx_2 = np.array(np.where((Class02[:,12]>0.143) & (Class02[:,12]<0.855), 1, 0))
b_2 = np.column_stack((Class02,filtIndx_2))
print ("(1) NDVI is queued and added to the list:", b_2[:,-1])
                    
#1.2_NDWI_I: metrics in yellow.
filtIndx2_2 = np.array(np.where((b_2[:,13]>-0.116)&(b_2[:,13]<0.502), 1, 0))
c_2 = np.column_stack((b_2,filtIndx2_2))
print ("(2) NDWI_I is queued and added to the list:", c_2[:,-1])

#1.3_Tasselled Cap Greenness: metrics in yellow.
filtIndx3_2 = np.array(np.where((c_2[:,16]>-0.052)&(c_2[:,16]<0.277), 1, 0))
d_2 = np.column_stack((c_2,filtIndx3_2))
print ("(3) Tasselled Cap Greenness is queued and added to the list:", d_2[:,-1])

#1.4_Solar Radiation: metrics in yellow.
filtIndx4_2 = np.array(np.where((d_2[:,6]>3818.58)&(d_2[:,6]<7583.79), 1, 0))
e_2 = np.column_stack((d_2,filtIndx4_2))
print ("(4) Solar Radiation is queued and added to the list:", e_2[:,-1])

#1.5_GNDVI: metrics in yellow.
filtIndx5_2 = np.array(np.where((e_2[:,11]>0.220)&(e_2[:,11]<0.743), 1, 0))
f_2 = np.column_stack((e_2,filtIndx5_2))
print ("(5) GNDVI is queued and added to the list:", f_2[:,-1])

#1.6_Ground Height: change range metrics in yellow.
filtIndx6_2 = np.array(np.where((f_2[:,4]>25.13)&(f_2[:,4]<975.16), 1, 0))
g_2 = np.column_stack((f_2,filtIndx6_2))
print ("(6) Ground Height is queued and added to the list:", g_2[:,-1])

#1.7_Slope: metrics in yellow.
filtIndx7_2 = np.array(np.where((g_2[:,5]>0.22)&(g_2[:,5]<32.86), 1, 0))
h_2 = np.column_stack((g_2,filtIndx7_2))
print ("(7) Slope is queued and added to the list:", h_2[:,-1])

#1.8_NIR_SWIR_2: metrics in yellow.
filtIndx8_2 = np.array(np.where((h_2[:,14]>0.086)&(h_2[:,14]<0.773), 1, 0))
i_2 = np.column_stack((h_2,filtIndx8_2))
print ("(8) NIR_SWIR_2 is queued and added to the list:", i_2[:,-1])

#1_Thematic Agreement.
Agreement02 = np.where((np.sum(i_2[:,34:42], axis=1) ==8), 1, 0)
A01_2 = np.column_stack((i_2, Agreement02))
indx02 = np.delete(A01_2, np.s_[34:42], axis=1) 
print("Thematic Agreement:", indx02[:,-1])

#_2_Class Vetting with forest heights.

Veg_1 = np.where((indx02[:,3]>5)&(indx02[:,3]<12), 1, 0)
A02_2 = np.column_stack((indx02, Veg_1))
print("Class Vetting:", A02_2[:,-1])

#_3_Correlation between ICESat-2 and Forest Height Product.

n2 = A02_2[:,3] #Forest Height Product column.
m2 = A02_2[:,33] #Optimized LiDAR Canopy Height Column.
o2=np.where((n2>=(m2-6))&(n2<=(m2+6)), 1, 0)
A03_2 = np.column_stack((A02_2, o2))
print ("LiDAR Agreement:", A03_2[:,-1])

#_4_Reliability Levels: Save Calibrated Data to File.
 
Sum_2 = A03_2[:,34:37].sum(axis=1)
print("Class 02: Reliability Levels", Sum_2)
a04_2 = np.column_stack((A03_2, Sum_2))
np.savetxt("02_Open Tree Cover.csv", a04_2, delimiter=',', header="N, classCode, LCP_Band, LCP_Height, Ground_H, Slope, SolarRad, WetnessInd, Blue, NIR, SWIR_1, NDWI_I, NDVI, NDWI_II, NIR_SWIR_2, SWIR_1_SWIR_2, TassCapGn, TassCapWet, SAVI, BN, North, East, B1, B2, B3, B4, B5, B6, B7, B8, B8A, B11, B12, Canopy Height, Thematic Agreement, Class Height, Lidar Vetting, Reliability Level", fmt="%f")

                                     
                                        #Class 03: Dense Tree Cover

a_3 = np.split(a_2[1], [28397], axis=0) 
#split Class data from the 'Training Dataset': Set the Row Value for the next class above.

#_1_Thematic_Agreement_Classifier.

Class03 = np.array(a_3[0])
print ("*")
print ("Class 03: Dense Tree Cover")

#1.1_NDVI: metrics in yellow.
filtIndx_3 = np.array(np.where((Class03[:,12]>0.143) & (Class03[:,12]<0.848), 1, 0))
b_3 = np.column_stack((Class03,filtIndx_3))
print ("(1) NDVI is queued and added to the list:", b_3[:,-1])
                    
#1.2_NIR_SWIR_2:  metrics in yellow.
filtIndx2_3 = np.array(np.where((b_3[:,14]>0.086)&(b_3[:,14]<0.778), 1, 0))
c_3 = np.column_stack((b_3,filtIndx2_3))
print ("(2) NIR_SWIR_2 is queued and added to the list:", c_3[:,-1])

#1.3_NDWI_1: metrics in yellow.
filtIndx3_3 = np.array(np.where((c_3[:,13]>-0.052)&(c_3[:,13]<0.494), 1, 0))
d_3 = np.column_stack((c_3,filtIndx3_3))
print ("(3) NDWI_I is queued and added to the list:", d_3[:,-1])

#1.4_Tasseled Cap Greenness: metrics in yellow.
filtIndx4_3 = np.array(np.where((d_3[:,16]>-0.052)&(d_3[:,16]<0.302), 1, 0))
e_3 = np.column_stack((d_3,filtIndx4_3))
print ("(4) Tasseled Cap Greenness is queued and added to the list:", e_3[:,-1])

#1.5_Tasseled Cap Wetness: metrics in yellow.
filtIndx5_3 = np.array(np.where((e_3[:,17]>-0.325)&(e_3[:,17]<-0.021), 1, 0))
f_3 = np.column_stack((e_3,filtIndx5_3))
print ("(5) Tasseled Cap Wetness is queued and added to the list:", f_3[:,-1])

#1.6_Ground Height:  metrics in yellow.
filtIndx6_3 = np.array(np.where((f_3[:,4]>32.79)&(f_3[:,4]<934.09), 1, 0))
g_3 = np.column_stack((f_3,filtIndx6_3))
print ("(6) Ground Height is queued and added to the list:", g_3[:,-1])

#1.7_Solar Radiation: metrics in yellow.
filtIndx7_3 = np.array(np.where((g_3[:,6]>4275.05)&(g_3[:,6]<7688.83), 1, 0))
H_3 = np.column_stack((g_3,filtIndx7_3))
print ("(7) Solar Radiation is queued and added to the list:", H_3[:,-1])

#1_Thematic Agreement.
Agreement03 = np.where((np.sum(H_3[:,34:41], axis=1) ==7), 1, 0)
A01_3 = np.column_stack((H_3, Agreement03))
indx03 = np.delete(A01_3, np.s_[34:41], axis=1) 
print("Thematic Agreement Output:", indx03[:,-1])

#_2_Class Vetting with forest heights.

Veg_3 = np.where((indx03[:,3]>12), 1, 0)
A02_3 = np.column_stack((indx03, Veg_3))
print("Class Vetting:", A02_3[:,-1])

#_3_Correlation between ICESat-2 and Forest Height Product.

n3 = A02_3[:,3] #Forest Height column.
m3 = A02_3[:,33] #Optimized LiDAR Canopy Height Column.
o3=np.where((n3>=(m3-6))&(n3<=(m3+6)), 1, 0)
A03_3 = np.column_stack((A02_3, o3))
print ("LiDAR Agreement:", A03_3[:,-1])

#_4_Reliability Levels: Save Calibrated Training Data to File. 

Sum_3 = A03_3[:,34:37].sum(axis=1)
print("Class 03: Reliability Levels", Sum_3)
a04_3 = np.column_stack((A03_3, Sum_3))
np.savetxt("03_Dense Tree Cover.csv", a04_3, delimiter=',', header="N, classCode, LCP_Band, LCP_Height, Ground_H, Slope, SolarRad, WetnessInd, Blue, NIR, SWIR_1, NDWI_I, NDVI, NDWI_II, NIR_SWIR_2, SWIR_1_SWIR_2, TassCapGn, TassCapWet, SAVI, BN, North, East, B1, B2, B3, B4, B5, B6, B7, B8, B8A, B11, B12, Canopy Height, Thematic Agreement, Class Height, Lidar Vetting, Reliability Level", fmt="%f")


                                            #Class 04: Wetland

a_4 = np.split(a_3[1], [1245], axis=0) 
#split Class data from the 'Training Dataset': Set the Row Value for the next class above.

#_1_Thematic_Agreement_Classifier.

Class04 = np.array(a_4[0])
print ("*")
print ("Class 04: Wetland")

#1.1_NDVI: metrics in yellow.
filtIndx_4 = np.array(np.where((Class04[:,12]>-0.092) & (Class04[:,12]<0.699), 1, 0))
b_4 = np.column_stack((Class04,filtIndx_4))
print ("(1) NDVI is queued and added to the list:", b_4[:,-1])

#1.2_SWIR_1_SWIR_2: change range metrics in yellow.
filtIndx3_4 = np.array(np.where((b_4[:,15]>0.172)&(b_4[:,15]<0.455), 1, 0))
d_4 = np.column_stack((b_4,filtIndx3_4))
print ("(2) SWIR_1_SWIR_2 is queued and added to the list:", d_4[:,-1])

#1.3_Tasseled Cap Greenness: metrics in yellow.
filtIndx4_4 = np.array(np.where((d_4[:,16]>-0.056)&(d_4[:,16]<0.169), 1, 0))
e_4 = np.column_stack((d_4,filtIndx4_4))
print ("(3) Tasseled Cap Greenness is queued and added to the list:", e_4[:,-1])

#1.4_Tasselled Cap Wetness: metrics in yellow.
filtIndx5_4 = np.array(np.where((e_4[:,17]>-0.218)&(e_4[:,17]<0.010), 1, 0))
f_4 = np.column_stack((e_4,filtIndx5_4))
print ("(4) Tasselled Cap Wetness is queued and added to the list:", f_4[:,-1])

#1.5_Wetness Index: metrics in yellow.
filtIndx6_4 = np.array(np.where((f_4[:,7]>-0.078)&(f_4[:,7]<7.332), 1, 0))
g_4 = np.column_stack((f_4,filtIndx6_4))
print ("(5) Wetness Index is queued and added to the list:", g_4[:,-1])

#1_Thematic Agreement.
Agreement04 = np.where((np.sum(g_4[:,34:39], axis=1) ==5), 1, 0)
A01_4 = np.column_stack((g_4, Agreement04))
indx04 = np.delete(A01_4, np.s_[34:39], axis=1) 
print("Thematic Agreement Output:", indx04[:,-1])

#_2_Class Vetting with ICESat-2 canopy heights.

Veg_4 = np.where((indx04[:,33]<12), 1, 0)
A02_4 = np.column_stack((indx04, Veg_4))
print("Class Vetting:", A02_4[:,-1])

#_3_Correlation between ICESat-2 and the Forest Height product.

n4 = A02_4[:,3] #Forest Height column.
m4 = A02_4[:,33] #Optimized Canopy Height Column.
o4=np.where((n4>=(m4-6))&(n4<=(m4+6)), 1, 0)
A03_4 = np.column_stack((A02_4, o4))
print ("LiDAR Agreement:", A03_4[:,-1])

#_4_Reliability Levels: Save Calibrated Training Data to File. 

Sum_4 = A03_4[:,34:37].sum(axis=1)
print("Class 04: Reliability Levels", Sum_4)
a04_4 = np.column_stack((A03_4, Sum_4))
np.savetxt("04_Wetland.csv", a04_4, delimiter=',', header="N, classCode, LCP_Band, LCP_Height, Ground_H, Slope, SolarRad, WetnessInd, Blue, NIR, SWIR_1, NDWI_I, NDVI, NDWI_II, NIR_SWIR_2, SWIR_1_SWIR_2, TassCapGn, TassCapWet, SAVI, BN, North, East, B1, B2, B3, B4, B5, B6, B7, B8, B8A, B11, B12, Canopy Height, Thematic Agreement, Class Height, Lidar Vetting, Reliability Level", fmt="%f")


                                    #Class 05: Built Up

a_5 = np.split(a_4[1], [24602], axis=0) 
#split Class data from the 'Training Dataset': Set the Row Value for the next class above.

#_1_Thematic_Agreement_Classifier.

Class05 = np.array(a_5[0])
print ("*")
print ("Class 05: Built up")

#1.1_Slope: metrics in yellow
filtIndx_5 = np.array(np.where((Class05[:,5]>0.105) & (Class05[:,5]<14.22), 1, 0))
b_5 = np.column_stack((Class05,filtIndx_5))
print ("(1) Slope is queued and added to the list:", b_5[:,-1])

#1.2_NDVI: metrics in yellow.
filtIndx2_5 = np.array(np.where((b_5[:,12]>0.042)&(b_5[:,12]<0.794), 1, 0))
c_5 = np.column_stack((b_5,filtIndx2_5))
print ("(2) NDVI is queued and added to the list:", c_5[:,-1])

#1.3_NIR_SWIR_2: metrics in yellow.
filtIndx3_5 = np.array(np.where((c_5[:,14]>-0.033)&(c_5[:,14]<0.722), 1, 0))
d_5 = np.column_stack((c_5,filtIndx3_5))
print ("(3) NIR_SWIR_2 is queued and added to the list:", d_5[:,-1])

#1.4_SWIR_1_SWIR_2: metrics in yellow.
filtIndx4_5 = np.array(np.where((d_5[:,15]>0.020)&(d_5[:,15]<0.445), 1, 0))
e_5 = np.column_stack((d_5,filtIndx4_5))
print ("(4) SWIR_1_SWIR_2 is queued and added to the list:", e_5[:,-1])

#1.5_Tasselled Cap Greenness: metrics in yellow)
filtIndx5_5 = np.array(np.where((e_5[:,16]>-0.167) & (e_5[:,16]<0.206), 1, 0))
f_5 = np.column_stack((e_5,filtIndx5_5))
print ("(5) Tasselled Cap Greenness is queued and added to the list:", f_5[:,-1])

#1.6_NDWI_I: metrics in yellow.
filtIndx6_5 = np.array(np.where((f_5[:,13]>-0.160) & (f_5[:,13]<0.420), 1, 0))
g_5 = np.column_stack((f_5,filtIndx6_5))
print ("(6) NDWI_I is queued and added to the list:", g_5[:,-1])

#1_Thematic Agreement
Agreement05 = np.where((np.sum(g_5[:,34:40], axis=1) ==6), 1, 0)
A01_5 = np.column_stack((g_5, Agreement05))
indx05 = np.delete(A01_5, np.s_[34:40], axis=1) 
print("Thematic Agreement:", indx05[:,-1])

#_2_Class Vetting with ICESat-2 canopy heights.

nonVeg_5 = np.where((indx05[:,33]<8), 1, 0)
A02_5 = np.column_stack((indx05, nonVeg_5))
print("Class Vetting:", A02_5[:,-1])

#_3_Correlation between ICESat-2 and Forest Height product.

n5 = A02_5[:,3] #Forest Height column.
m5 = A02_5[:,33] #Filtered LiDAR Canopy Height Column.
o5=np.where((n5>=(m5-6))&(n5<=(m5+6)), 1, 0)
A03_5 = np.column_stack((A02_5, o5))
print ("LiDAR Agreement:", A03_5[:,-1])

#_4_Reliability Levels: Save Calibrated Training Data to File. 

Sum_5 = A03_5[:,34:37].sum(axis=1)
print("Class 05: Reliability Levels", Sum_5)
a04_5 = np.column_stack((A03_5, Sum_5))
np.savetxt("05_Built-up.csv", a04_5, delimiter=',', header="N, classCode, LCP_Band, LCP_Height, Ground_H, Slope, SolarRefle, WetnessInd, Blue, NIR, SWIR_1, NDWI_I, NDVI, NDWI_II, NIR_SWIR_2, SWIR_1_SWIR_2, TassCapGn, TassCapWet, SAVI, BN, North, East, B1, B2, B3, B4, B5, B6, B7, B8, B8A, B11, B12, Canopy Height, Thematic Agreement, Class Height, Lidar Vetting, Reliability Level", fmt="%f")

                                                #Class 06: Water

a_6 = np.split(a_5[1],[1864], axis=0) 
#split Class data from the 'Training Dataset': Set the Row Value for the next class above.

#_1_Thematic_Agreement_Classifier.

Class06 = np.array(a_6[0])
print ("*")
print ("Class 06: Water")

#1.1_NDWI_I: metrics in yellow
filtIndx_6 = np.array(np.where((Class06[:,13]>0.005) & (Class06[:,13]<0.494), 1, 0))
b_6 = np.column_stack((Class06,filtIndx_6))
print ("(1) NDWI_I is queued and added to the list:", b_6[:,-1])

#1.2_Tasselled Cap Greenness: metrics in yellow.
filtIndx3_6 = np.array(np.where((b_6[:,16]>-0.043) & (b_6[:,16]<0.051), 1, 0))
c_6 = np.column_stack((b_6,filtIndx3_6))
print ("(2) Tasselled Cap Wetness is queued and added to the list:", c_6[:,-1])

#1.3_GNDVI: metrics in yellow.
filtIndx4_6 = np.array(np.where((c_6[:,13]>-0.277) & (c_6[:,13]<0.479), 1, 0))
d_6 = np.column_stack((c_6,filtIndx4_6))
print ("(3) GNDVI is queued and added to the list:", d_6[:,-1])

#1_Thematic Agreement.
Agreement06 = np.where((np.sum(d_6[:,34:37], axis=1) ==3), 1, 0)
A01_6 = np.column_stack((d_6, Agreement06))
indx06 = np.delete(A01_6, np.s_[34:37], axis=1) 
print("Thematic Agreement:", indx06[:,-1])

#_2_Class Vetting with ICESat-2 canopy heights.

nonVeg_6 = np.where((indx06[:,3]==0), 1, 0)
A02_6 = np.column_stack((indx06, nonVeg_6))
print("Class Vetting:", A02_6[:,-1])

#_3_Correlation between ICESat-2 and Forest Height Product.

n6 = A02_6[:,3] #Forest Height column.
m6 = A02_6[:,33] #Optimized LiDAR Canopy Height Column.
o6=np.where((n6>=(m6-6))&(n6<=(m6+6)), 1, 0)
A03_6 = np.column_stack((A02_6, o6))
print ("LiDAR Agreement:", A03_6[:,-1])

#_4_Reliability Levels: Save Calibrated Training Data to File. 

Sum_6 = A03_6[:,34:37].sum(axis=1)
print("Class 06: Reliability Levels", Sum_6)
a04_6 = np.column_stack((A03_6, Sum_6))
np.savetxt("06_Water.csv", a04_6, delimiter=',', header="N, classCode, LCP_Band, LCP_Height, Ground_H, Slope, SolarRad, WetnessInd, Blue, NIR, SWIR_1, NDWI_I, NDVI, NDWI_II, NIR_SWIR_2, SWIR_1_SWIR_2, TassCapGn, TassCapWet, SAVI, BN, North, East, B1, B2, B3, B4, B5, B6, B7, B8, B8A, B11, B12, Canopy Height, Thematic Agreement, Class Height, Lidar Vetting, Reliability Level", fmt="%f")


 #Class 07: Cropland

a_7 = np.split(a_6[1], [38181], axis=0) 

#split Class data from the 'Training Dataset': Set the Row Value for the next class above.

#_1_Thematic_Agreement_Classifier.

Class07 = np.array(a_7[0])
print ("*")
print ("Class 07: Cropland")

#1.1_NDVI: metrics in yellow.
filtIndx_7 = np.array(np.where((Class07[:,12]>-0.073) & (Class07[:,12]<0.828), 1, 0))
b_7 = np.column_stack((Class07,filtIndx_7))
print ("(1) NDVI is queued and added to the list:", b_7[:,-1])
        
#1.2_BN: metrics in yellow.
filtIndx2_7 = np.array(np.where((b_7[:,19]>-0.841) & (b_7[:,19]<0.017), 1, 0))
c_7 = np.column_stack((b_7,filtIndx2_7))
print ("(2) BN is queued and added to the list:", c_7[:,-1])
  
#1.3_Tasseled Cap Greenness: metrics in yellow)
filtIndx3_7 = np.array(np.where((c_7[:,16]>-0.066) & (c_7[:,16]<0.247), 1, 0))
d_7 = np.column_stack((c_7,filtIndx3_7))
print ("(3) Tasseled Cap Greenness is queued and added to the list:", d_7[:,-1])
 
#1.4_Tasseled Cap Wetness: metrics in yellow)
filtIndx4_7 = np.array(np.where((d_7[:,17]>-0.405) & (d_7[:,17]<0.031), 1, 0))
e_7 = np.column_stack((d_7,filtIndx4_7))
print ("(4) Tasseled Cap Wetness is queued and added to the list:", e_7[:,-1])
         
#1.5_Ground Height: metrics in yellow)
filtIndx5_7 = np.array(np.where((e_7[:,4]>10.38)&(e_7[:,4]<696.30), 1, 0))
f_7 = np.column_stack((e_7,filtIndx5_7))
print ("(5) Ground Height is queued and added to the list:", f_7[:,-1])

#1.6_Slope: metrics in yellow)
filtIndx6_7 = np.array(np.where((f_7[:,5]>0.18)&(f_7[:,5]<21.44), 1, 0))
g_7 = np.column_stack((f_7,filtIndx6_7))
print ("(6) Slope is queued and added to the list:", g_7[:,-1])


#1_Thematic Agreement. 
Agreement10 = np.where((np.sum(g_7[:,34:40], axis=1) ==6), 1, 0)
A04_7 = np.column_stack((g_7, Agreement10))
indx10 = np.delete(A04_7, np.s_[34:40], axis=1) 
print("Thematic Agreement:", indx10[:,-1])

#_2_Class Vetting with ICESat-2 canopy heights.

Veg_7 = np.where((indx10[:,33]<=5), 1, 0)
A05_7 = np.column_stack((indx10, Veg_7))
print("Class Vetting:", A05_7 [:,-1])

#_3_Correlation between ICESat-2 and Forest Height Product.

n7 = A05_7[:,3] #Forest Height column.
m7 = A05_7[:,33] #Optimized LiDAR Canopy Height Column.
o7=np.where((n7>=(m7-6)) & (n7<=(m7+6)), 1, 0)
a06_7 = np.column_stack((A05_7, o7))
print ("LiDAR Agreement:", a06_7[:,-1])

#_4_Reliability Levels: Save Calibrated Training Data to File. 

Sum_7 = a06_7[:,34:37].sum(axis=1)
print("Class 07: Reliability Levels", Sum_7)
a07_7 = np.column_stack((a06_7, Sum_7))


#1.7_Cultivation/Harvest Seasons: metrics in yellow.

#1.7.1_NDVI
filtIndx7_7 = np.array(np.where(a07_7[:,12]<0.321, 1, 0))
h_7 = np.column_stack((a07_7,filtIndx7_7))
print ("(7) NDVI (1) is queued and added to the list:", h_7[:,-1])
 
#1.7.2_NIR (b8).
filtIndx8_7 = np.array(np.where((h_7[:,9]>0.222)&(h_7[:,9]<0.240) | (h_7[:,12]<0.321), 1, 0))
i_7 = np.column_stack((h_7,filtIndx8_7))
print ("(8) NIR (1) is queued and added to the list:", i_7[:,-1])

#1.7.3_SWIR1 (b11).
filtIndx9_7 = np.array(np.where((i_7[:,10]>0.147)&(i_7[:,10]<0.178) | (i_7[:,12]<0.321), 1, 0))
j_7 = np.column_stack((i_7,filtIndx9_7))
print ("(9) SWIR1 (1) is queued and added to the list:", j_7[:,-1])

#1.7.4_Output.
Agreement07 = np.where((np.sum(j_7[:,38:41], axis=1) ==3), 1, 0)
A01_7 = np.column_stack((j_7, Agreement07))
indx07 = np.delete(A01_7, np.s_[38:41], axis=1)  
print("Cultivation/Harvest Agreement:", indx07[:,-1])

#1.8_Senescence: metrics in yellow.

#1.8.1_Blue (b2)
filtIndx10_7 = np.array(np.where((indx07[:,12]<0.563) & (indx07[:,12]>0.321), 1, 0))
k_7 = np.column_stack((indx07,filtIndx10_7))
print ("(10) Blue (2) is queued and added to the list:", k_7[:,-1])

#1.8.2_NIR (b8).
filtIndx11_7 = np.array(np.where((k_7[:,9]>0.240) & (k_7[:,9]<0.273) | (k_7[:,12]<0.563) & (k_7[:,12]>0.321), 1, 0))
l_7 = np.column_stack((k_7,filtIndx11_7))
print ("(11) NIR (2) is queued and added to the list:", l_7[:,-1])

#1.8.3_SWIR1 (b11).
filtIndx12_7 = np.array(np.where((l_7[:,10]>0.178) & (i_7[:,10]<0.252) | (l_7[:,12]<0.563) & (l_7[:,12]>0.321), 1, 0))
m_7 = np.column_stack((l_7,filtIndx12_7))
print ("(12) SWIR1 (2) is queued and added to the list:", m_7[:,-1])

#1.8.4_Output.
Agreement08 = np.where((np.sum(m_7[:,39:42], axis=1) ==3), 2, 0)
A02_7 = np.column_stack((m_7, Agreement08))
indx08 = np.delete(A02_7, np.s_[39:42], axis=1)  
print("Senescence Agreement:", indx08[:,-1])

#1.9_Growing Peak: metrics in yellow.

#1.9.1_NDVI
filtIndx13_7 = np.array(np.where(indx08[:,12]>0.563, 1, 0))
n_7 = np.column_stack((indx08,filtIndx13_7))
print ("(13) NDVI (3) is queued and added to the list:", n_7[:,-1])

#1.9.2_NIR (b8).
filtIndx14_7 = np.array(np.where((n_7[:,9]>0.273) & (n_7[:,9]<0.294) | (n_7[:,12]>0.563), 1, 0))
o_7 = np.column_stack((n_7,filtIndx14_7))
print ("(14) NIR (3) is queued and added to the list:", o_7[:,-1])

#1.9.3_SWIR1 (b11).
filtIndx15_7 = np.array(np.where((o_7[:,10]>0.252) & (o_7[:,10]<0.337) | (o_7[:,12]>0.563), 1, 0))
p_7 = np.column_stack((o_7,filtIndx15_7))
print ("(15) SWIR1 (3) is queued and added to the list:", p_7[:,-1])

#1.9.4_Output.
Agreement09 = np.where((np.sum(p_7[:,40:43], axis=1) ==3), 3, 0)
A03_7 = np.column_stack((p_7, Agreement09))
indx09 = np.delete(A03_7, np.s_[40:43], axis=1)  
print("growing peak Agreement:", indx09[:,-1])

np.savetxt("07_Cropland.csv", indx09, delimiter=',', header="N, classCode, LCP_Band, LCP_Height, Ground_H, Slope, SolarRad, WetnessInd, Blue, NIR, SWIR_1, NDWI_I, NDVI, NDWI_II, NIR_SWIR_2, SWIR_1_SWIR_2, TassCapGn, TassCapWet, SAVI, BN, North, East, B1, B2, B3, B4, B5, B6, B7, B8, B8A, B11, B12, Canopy Height, Thematic Agreement, Class Height, Lidar Vetting, Reliability Level, Cultivation/Harvest Agreement, Senescence Agreement, Growing Agreement", fmt="%f")

#*****

#Save output classification as a compact dataset.
empt_array = np.concatenate((a04_1, a04_2, a04_3, a04_4, a04_5, a04_6)).astype(float)

#Input zeros: dataset total rows - cropland rows (e.g., 168,102 - 35,534 = 132,568 zeros in 3 columns)
z = np.zeros((129624,3), dtype =float)
new_shape = np.append(empt_array,z,axis=1)
output = np.concatenate((new_shape,indx09))                           
np.savetxt("08_Output Dataset.csv", output, delimiter=',', header="N, classCode, LCP_Band, LCP_Height, Ground_H, Slope, SolarRad, WetnessInd, Blue, NIR, SWIR_1, NDWI_I, NDVI, NDWI_II, NIR_SWIR_2, SWIR_1_SWIR_2, TassCapGn, TassCapWet, SAVI, BN, North, East, B1, B2, B3, B4, B5, B6, B7, B8, B8A, B11, B12, Canopy Height, Thematic Agreement, Class Height, Lidar Vetting, Reliability Level, Cultivation/Harvest Agreement, Senescence Agreement, Growing Agreement", fmt="%f")

     
#End






            



                    
          
                    
            





