//typedef struct {
	//size_t w;
	//size_t h;
	//size_t channels;
	//GimpDrawable* drawable;
//} gimpImage;


//gimpImage* gimp_image_init(gimpDrawable* drawable, gint w, gint h, gint channels)
//{
	//gimpImage* img = malloc(sizeof(gimpImage));
	
	//img -> w = w;
	//img -> h = h;
	//img -> channels = channels;
	
	//img -> drawable = drawable;
	
	//return img;
//}

//void gimp_image_free(gimpImage* img)
//{
	//if(img != NULL) free(img);
//}

//guint8* gimp_image_get(gimpImage* img, gint x, gint y)
//{
	//return gimp_drawable_get_pixel(img -> drawable, x, y, &img -> channels)
//}

//gboolean gimp_image_set(gimpImage* img, gint x, gint y, const guint8* px)
//{
	//return gimp_drawable_set_pixel(img -> drawable, x, y, &img -> channels, px);
//}
