#include <stdio.h>
#include "sparseWeights.h"
#include <string.h>

void MatrixVectorMult(double out[], double Val[], int RowPtr[], int Col[],
		      double in[], int m)
{
   int i, k;

   for (k = 0; k < m; k = k + 1) {
      out[k] = 0.0;
   }

   for (i = 0; i < m; i = i + 1) {
      for (k = RowPtr[i]; k < RowPtr[i+1]; k = k + 1) {
         // cout << "k = " << k << ", Col[k] = " << Col[k] 
         //		<< ", in[Col[k]] = " << in[Col[k]] << endl;
         // cout << Val[k] << " * " << in[Col[k]] << endl;

         out[i] = out[i] + Val[k]*in[Col[k]];
      }
   }
}

void fullMatrixMult(int layer, double vec[], double out[], int n, int m){
	int i,j;

	if (layer == 0)
		for (int i = 0; i < m; i++)
			for (int j = 0; j < n; j++)
				out[i] = out[i] + fweight0[i][j]*vec[j];
	else
		for (int i = 0; i < m; i++)
			for (int j = 0; j < n; j++)
				out[i] = out[i] + fweight1[i][j]*vec[j];



 }

int main(int argc, char ** argv)
{
   /*double Val[] = {11, 12, 14, 22, 23, 25, 31, 33, 34, 42, 45,
		46, 55, 65, 66, 67, 75, 77, 78, 87, 88};
   int RowPtr[] = {0, 3, 6, 9, 12, 13, 16, 19, 21};
   int Col[] = {0, 1, 3, 1, 2, 4, 0, 2, 3, 1, 4,
		5, 4, 4, 5, 6, 4, 6, 7, 6, 7};*/
   double output[VECSIZE], temp[WSIZE], fullout[VECSIZE];
   int i, j;

   //u[0] = 3; u[1] = 5; u[2] = 2; u[3] = 1;
   //u[4] = 0; u[5] = 1; u[6] = 2; u[7] = 4;


   MatrixVectorMult(temp, Val0, RowPtr0, Col0, vector, WSIZE);
   MatrixVectorMult(output, Val1, RowPtr1, Col1, temp, VECSIZE);

   for (i = 0; i < VECSIZE; i = i + 1) {
       printf("      %4.1lf\n", output[i]);
   }

   memset(output, 0.0, VECSIZE*sizeof(double));
   memset(temp, 0.0, WSIZE*sizeof(double));
   for (i = 0; i < VECSIZE; i = i + 1) {
       printf("      %4.1lf\n", output[i]);
   }

   fullMatrixMult(0, vector, temp, VECSIZE, WSIZE);
   fullMatrixMult(1, temp, output, WSIZE, VECSIZE);

   printf("\n full mult\n");
   for (i = 0; i < VECSIZE; i = i + 1) {
       printf("      %4.1lf\n", output[i]);
   }
}

