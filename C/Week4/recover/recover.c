/* 
 * Recover JPEGs from a memory card/ forensic file
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main (int argc, char *argv[])
{
	/*
	 * Ensure proper usage
	 */
	if (argc != 2)
	{
		fprintf(stderr, "Usage: ./recover raw\n");
		return 1;
	}
	
    char *rawfile = argv[1];
	
    FILE *inptr = fopen(rawfile, "r");							// open raw file to read
	
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", rawfile);
        return 2;
    }
	
	/*
	 * Allocate space for recovering
	 */
	uint8_t buffer[512];								// buffer array of size 512 bytes
	char imgname[8];								// for file names
	FILE *outptr = NULL;
	unsigned int n = 0; 								// JPEG file counter
	
	/*
	 * Read forensic file and write jpegs until EOF
	 */
	while(fread(buffer, 512, 1, inptr ) == 1)
	{
		if(buffer[0] == 0xff && buffer[1] == 0xd8 &&
			buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0) 		// start of a new jpeg
			{
				if(outptr != NULL) 					// if already writing a jpeg
				{
					fclose(outptr);
					sprintf(imgname, "%03i.jpg", n);		// name, open and write a new jpeg
					outptr = fopen(imgname, "w");
					fwrite(buffer, 512, 1, outptr);
					n++;
				}
				else							// if first jpeg encountered
				{
					sprintf(imgname, "%03i.jpg", n);
					outptr = fopen(imgname, "w");
					fwrite(buffer, 512, 1, outptr);
					n++;
				}
			}
		
		else if(outptr != NULL)							// already writing a jpeg, but no header found
		{
			fwrite(&buffer, 512, 1, outptr);
		}
		else
		{
			continue;							// discard those bytes
		}
	}
	
	fclose(outptr);
	fclose(inptr);
	return 0;
}
