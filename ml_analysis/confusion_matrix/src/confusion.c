#include <zephyr/kernel.h>
#include <math.h>
#include "confusion.h"
#include "adc.h"
#include "centroid_data.h"
#include <stdio.h>


/* 
  K-means algorithm should provide 6 center points with
  3 values x,y,z. Let's test measurement system with known
  center points. I.e. x,y,z are supposed to have only values
  1 = down and 2 = up
  
  CenterPoint matrix is thus the 6 center points got from K-means algoritm
  teaching process. This should actually come from include file like
  #include "KmeansCenterPoints.h"
  
  And measurements matrix is just fake matrix for testing purpose
  actual measurements are taken from ADC when accelerator is connected.
*/ 

// int CP[6][3]={
// 	                     {1,0,0},
// 						 {2,0,0},
// 						 {0,1,0},
// 						 {0,2,0},
// 						 {0,0,1},
// 						 {0,0,2}
// };

// int measurements[6][3]={
// 	                     {1,0,0},
// 						 {2,0,0},
// 						 {0,1,0},
// 						 {0,2,0},
// 						 {0,0,1},
// 						 {0,0,2}
// };

int CM[6][6]= {0}; // CM[rows][columns], joten CM[direction][winner]

// void test_function(void) {
//    // printing centroid points START 
//    // for (int i = 0; i < 6; i++) {
//    //      for (int j = 0; j < 3; j++) {
//    //          printf("%d ", centroid_coords[i][j]);
//    //      }
//    //      printf("\n");
//    // }
//    // printing centroid points END
//    printf("Now at test_function.\n");
//    printf("Calculated:",calculateDistanceToAllCentrePointsAndSelectWinner(1807, 1497, 1535));
// }

// Button 1 down, printing current Confusion Matrix
void printConfusionMatrix(void)
{
	printf("Confusion matrix = \n");
	printf("   cp1 cp2 cp3 cp4 cp5 cp6\n");
	for(int i = 0;i<6;i++)
	{
		printf("cp%d %d   %d   %d   %d   %d   %d\n",i+1,CM[i][0],CM[i][1],CM[i][2],CM[i][3],CM[i][4],CM[i][5]);
	}
}

// Button 3 down, making fake 100 meas or one real meas depending on DEBUG state // Pointless(maybe?!?)
void makeHundredFakeClassifications(void)
{
   /*
   Jos ja toivottavasti kun teet toteutuksen paloissa eli varmistat ensin,
   että etäisyyden laskenta 6 keskipisteeseen toimii ja osaat valita 6 etäisyydestä
   voittajaksi sen lyhyimmän etäisyyden, niin silloin voit käyttää tätä aliohjelmaa
   varmistaaksesi, että etäisuuden laskenta ja luokittelu toimii varmasti tunnetulla
   itse keksimälläsi sensoridatalla ja itse keksimilläsi keskipisteillä.*/
   // printk("Make your own implementation for this function if you need this\n");
}

// button 4 down, one meas and classification with current direction =0 // Pointless(maybe?!?)
void makeOneClassificationAndUpdateConfusionMatrix(int direction)
{
   /*
   Tee toteutus tälle ja voit tietysti muuttaa tämän aliohjelman sellaiseksi,
   että se tekee esim 100 kpl mittauksia tai sitten niin, että tätä funktiota
   kutsutaan 100 kertaa yhden mittauksen ja sen luokittelun tekemiseksi.*/

   // call for calculationfunction 100 times
   int i = 0;
   while (i<100) {
      struct Measurement m = readADCValue();
      int winner = calculateDistanceToAllCentrePointsAndSelectWinner(m.x,m.y,m.z);
      printf("x = %d,  y = %d,  z = %d\n",m.x,m.y,m.z);
      i++;
      CM[direction][winner] += 1;
   }
   
   // UNCOMMENT THESE TO MEASURE ONE TIME (+COMMENT UPPER WHILE-LOOP)
   // struct Measurement m = readADCValue();
   // int winner = calculateDistanceToAllCentrePointsAndSelectWinner(m.x,m.y,m.z);
   // CM[direction][winner] += 1;
}

int calculateDistanceToAllCentrePointsAndSelectWinner(int x,int y,int z)
{
   /*
   Tämän aliohjelma ottaa yhden kiihtyvyysanturin mittauksen x,y,z,
   laskee etäisyyden kaikkiin 6 K-means keskipisteisiin ja valitsee
   sen keskipisteen, jonka etäisyys mittaustulokseen on lyhyin.*/
   
   float distance_list[6] = {0}; // list for calculated distances. Order = high_x, low_x, high_y, low_y, high_z, low_z

   // käydään joka piste centroid_coords[row][col] keskipistelistasta läpi
   for (int row = 0; row < 6; row++) {

      float distance = sqrtf(
         (x - centroid_coords[row][0]) * (x - centroid_coords[row][0]) + 
         (y - centroid_coords[row][1]) * (y - centroid_coords[row][1]) + 
         (z - centroid_coords[row][2]) * (z - centroid_coords[row][2])
      );

      // lisätään laskettu arvo "distance_list" listaan indeksiin row
      distance_list[row] = distance;
   }
   // printf("distance_list: ");
   // for (int idx = 0; idx < 6; idx++) {
   //    printf("%f ",distance_list[idx]);
   // }
   // printf("\n");

   int length = sizeof(distance_list) / sizeof(distance_list[0]); // listan pituus
   float min_val = distance_list[0]; // oletetaan, että 1. arvo on pienin (päivitetään loopissa)
   int min_val_index = 0; // indeksi, missä pienin arvo on
   
   // selataan distance_list lista, tarkistetaan listan pienin arvo ja missä indeksissä se on
   for (int val = 0; val < length; val++) {
      if (distance_list[val] < min_val) {
         min_val = distance_list[val];
      }
   }
   
   // päivitetään listaindeksi pienimmän arvon mukaan
   for (int idx = 0; idx < length; idx++){
      if (distance_list[idx] == min_val){
         min_val_index = idx;
      }
   }

   //printf("Smallest value %f and index %d.\n",min_val, min_val_index);
   return min_val_index; // 0
}

// Button 2 down, resetting confusion matrix
void resetConfusionMatrix(void)
{
	for(int i = 0; i < 6; i++)
	{ 
		for(int j = 0;j<6;j++)
		{
			CM[i][j] = 0;
		}
	}
}

