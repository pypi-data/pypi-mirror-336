#ifndef __DJVULIBRE_WRAPPER
#define __DJVULIBRE_WRAPPER

#include "Python.h"

#include "ddjvuapi.h"
#include "miniexp.h"

typedef struct {
   int width;
   int height;
   char* pixels;
} djvu_document;

int get_djvu_number_of_pages(char* path);
djvu_document get_djvu_page(int pagenumber, char* filepath);


#endif // __DJVULIBRE_WRAPPER 
