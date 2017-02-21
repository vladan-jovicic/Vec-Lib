// http://blog.ivank.net/fastest-gaussian-blur.html
#include <libgimp/gimp.h>
#include "contdet.h" 
#include <math.h>

int gaussian_blur(GimpDrawable* drawable, int r)
{
	//gint channels = gimp_drawable_bpp(drawable);
	//gint w = gimp_drawable_width();
	//gint h = gimp_drawable_height();
	
	//gimpImage* img = gimp_image_init(drawable, w, h, channels);
	
	//double boxes[3];
    //boxesForGauss(r, 3, boxes);
    
    //boxBlur_4(img, w, h, (boxes[0] - 1) / 2);
    //boxBlur_4(img, w, h, (boxes[1] - 1) / 2);
    //boxBlur_4(img, w, h, (boxes[2] - 1) / 2);
	
	//gimp_image_free(img);
	
	gint         channels;
	gint         x1, y1, x2, y2, w, h;
	GimpPixelRgn rgn_in, rgn_out;

	/* Gets upper left and lower right coordinates,
	 * and layers number in the image */
	gimp_drawable_mask_bounds (drawable -> drawable_id,
							   &x1, &y1,
							   &x2, &y2);
	channels = gimp_drawable_bpp (drawable -> drawable_id);

	/* Initialises two PixelRgns, one to read original data,
	 * and the other to write output data. That second one will
	 * be merged at the end by the call to
	 * gimp_drawable_merge_shadow() */
	gimp_pixel_rgn_init (&rgn_in,
						 drawable,
						 x1, y1,
						 x2 - x1, y2 - y1, 
						 FALSE, FALSE);
	gimp_pixel_rgn_init (&rgn_out,
						 drawable,
						 x1, y1,
						 x2 - x1, y2 - y1, 
						 TRUE, TRUE);
						 
	w = x2 - x1;
	h = y2 - y1;
						 
	double bxs[3];
	boxes(r, 3, bxs);
	
	boxBlur(&rgn_in, &rgn_out, w, h, (bxs[0] - 1) / 2);
	boxBlur(&rgn_in, &rgn_out, w, h, (bxs[0] - 1) / 2);
	boxBlur(&rgn_in, &rgn_out, w, h, (bxs[0] - 1) / 2);
	
	gimp_drawable_flush (drawable);
	gimp_drawable_merge_shadow (drawable -> drawable_id, TRUE);
	gimp_drawable_update (drawable -> drawable_id,
						  x1, y1,
						  x2 - x1, y2 - y1);
						  
						  
	return 0;

}


void boxes(double sigma, unsigned int n, double* sizes)
{
	double ideal_weight = sqrt((12 * sigma * sigma / n) + 1);
	int wl = floor(ideal_weight);
	if(wl % 2 == 0) wl--;
	int wu = wl + 2;
	
	double mIdeal = (12 * sigma * sigma - n * wl * wl - 4 * n * wl - 3 * n) / (-4.0 * wl - 4);
	double m = round(mIdeal);
	
	for(unsigned int i = 0; i < n; i++) sizes[i] = i < m ? wl : wu;
	
	
}

void boxBlur(GimpPixelRgn* in, GimpPixelRgn* out, gint w, gint h, double r)
{
    //for(int i = 0; i < scl.length; i++) tcl[i] = scl[i];
    boxBlurH(in, out, w, h, r);
    boxBlurT(in, out, w, h, r);
    
}

void boxBlurH(GimpPixelRgn* in, GimpPixelRgn* out, gint w, gint h, double r)
{
    double iarr = 1 / (r + r + 1);
    for(int i = 0; i < h; i++) {
        int ti = 0;
        
        guchar buf_in[w];
        guchar buf_out[w];
        gimp_pixel_rgn_get_row(in, buf_in, 0, i, w);
        
        for(int j = 0; j < w; j++) buf_out[j] = buf_in[j];
        
        int li = ti;
        int ri = ti + r;
        
        int fv = buf_in[ti];
        int lv = buf_in[ti + w - 1];
        int val = (r + 1) * fv;
        
        for(int j = 0; j < r; j++) val += buf_in[ti + j];
        for(int j = 0; j <= r; j++) {
			val += buf_in[ri++] - fv;
			buf_out[ti++] = round(val * iarr);
		}
        for(int j = r + 1; j < w - r; j++) {
			val += buf_in[ri++] - buf_in[li++];
			buf_out[ti++] = round(val * iarr);
		}
        for(int j = w - r; j < w; j++) {
			val += lv - buf_in[li++];
			buf_out[ti++] = round(val * iarr);
		}
		
		gimp_pixel_rgn_set_row(out, buf_out, 0, i, w);
		
    }
}

void boxBlurT(GimpPixelRgn* in, GimpPixelRgn* out, gint w, gint h, double r) {
    double iarr = 1 / (r + r + 1);
    
    for(int i = 0; i < w; i++) {
        int ti = i;
        int li = ti;
        int ri = ti + r * w;
        
        guchar buf_in[h];
        guchar buf_out[h];
        gimp_pixel_rgn_get_col(in, buf_in, i, 0, h);
        
        int fv = buf_in[ti];
        int lv = buf_in[ti + w * (h - 1)];
        int val = (r + 1) * fv;
        
        for(int j = 0; j < r; j++) val += buf_in[ti + j * w];
        for(int j = 0; j <= r; j++) {
			val += buf_in[ri] - fv;
			buf_out[ti] = round(val * iarr);
			ri += w; 
			ti += w;
		}
        for(int j = r + 1; j < h - r; j++) {
			val += buf_in[ri] - buf_in[li];
			buf_out[ti] = round(val * iarr);
			li += w;
			ri += w;
			ti += w;
		}
        for(int j = h - r; j < h; j++) {
			val += lv - buf_in[li];
			buf_out[ti] = round(val * iarr);
			li += w;
			ti += w;
		}
		
		gimp_pixel_rgn_set_col(out, buf_out, i, 0, h);
    }
}
