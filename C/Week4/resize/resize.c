#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    /**
     * ensure proper usage
     */
    if (argc != 4)
    {
        fprintf(stderr, "Usage: ./resize n infile outfile\n");
        return 1;
    }

    int n = atoi( argv[1] );
    if ((n < 1) || (n > 100))
    {
        fprintf(stderr, "n must be a positive integer less than or equal to 100\n");
        return 2;
    }

    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file 
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 3;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 4;
    }
    
    /**
     * identify and edit between infile's and outfile's headers
     */

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 || 
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 5;
    }
	
	// retain infile's headers for reading
	LONG inWidth = bi.biWidth;
    LONG inHeight = bi.biHeight;
    int inPadding =  (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

	// write outfile's headers according to n
	bi.biWidth *= n;
    bi.biHeight *= n;
    int padding =  (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    bi.biSizeImage = (((sizeof(RGBTRIPLE) * bi.biWidth) + padding) * abs(bi.biHeight));
    bf.bfSize = bi.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);
	
    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);
    
    /**
     * iterate over infile's scanlines, writing to outfile's
     */
    for (int i = 0; i < abs(inHeight); i++)
    {
		// iterate scanline vertically n-1 times
		for (int v = 0; v < n; v++)
		{
			// iterate over pixels in scanline
			for (int j = 0; j < inWidth; j++)
			{
				// temporary storage
				RGBTRIPLE triple;

				// read RGB triple from infile
				fread(&triple, sizeof(RGBTRIPLE), 1, inptr);
				
				for (int h = 0; h < n; h++)
				{
					// write RGB triple to outfile
					fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
				}
			}
			
			// then add padding to outfile
			for (int k = 0; k < padding; k++)
			{
				fputc(0x00, outptr);
			}
			// skip infile's paddings, if any
	        fseek(inptr, inPadding, SEEK_CUR);
	        
	        // set pointer back to read the same scanline until last looping
	        if( v < n-1 )
	        {
	            fseek(inptr, -(sizeof(RGBTRIPLE) * inWidth + inPadding), SEEK_CUR);
	        }

		}

    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}