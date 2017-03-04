/* GIMP Engine Plug-in Template
 * Copyright (C) 2000  Michael Natterer <mitch@gimp.org> (the "Author").
 * Copyright 2016 Lloyd Konneker
 * All Rights Reserved.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the "Software"),
 * to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included
 * in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
 * OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
 * THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
 * IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 *
 * Except as contained in this notice, the name of the Author of the
 * Software shall not be used in advertising or otherwise to promote the
 * sale, use or other dealings in this Software without prior written
 * authorization from the Author.
 */

#include <libgimp/gimp.h>
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "adaptOpenCV.hpp"
#include "contourDetection.hpp"



void renderUsingOpenCV (
    GimpDrawable *drawable,
    GimpPreview  *preview,
    gint32 low_threshold,
    gint32 dilate)
{
    gint         channels;
    gint         left, upper;
    gint         width, height;

    cv::Mat	src, dst;

    src = drawableToMat(drawable, preview);

    dst = innerRender(src, low_threshold, dilate); // image processing function(OpenCV Mat)
        
    setMatToDrawable(dst, drawable, preview);
    
    //g_message("preview : %d thr : %d\n", preview == NULL, low_threshold);
                
	return;
}


//https://github.com/renatoGarcia/gimp-opencv-plugin/blob/master/src/utility/interface.cpp
cv::Mat drawableToMat(GimpDrawable* drawable, GimpPreview* preview)
{
    gint x1, y1, x2, y2, width, height;
    
    if(preview == NULL) {
		gimp_drawable_mask_bounds(drawable->drawable_id,
								  &x1, &y1,
								  &x2, &y2);
								  
		width = x2 - x1;
		height = y2 - y1;
		
	} else {
		gimp_preview_get_position (preview, &x1, &y1);
		gimp_preview_get_size (preview, &width, &height);
		x2 = x1 + width;
		y2 = y1 + height;
    }

    GimpPixelRgn rgnIn;
    gimp_pixel_rgn_init(&rgnIn,
                        drawable,
                        x1, y1,
                        width, height,
                        FALSE, FALSE);

    cv::Mat mat(height, width, CV_MAKETYPE(CV_8U, drawable->bpp));
    gimp_pixel_rgn_get_rect(&rgnIn,
                            mat.data,
                            x1, y1,
                            width, height);

    return mat;
}

void setMatToDrawable(cv::Mat& mat, GimpDrawable* drawable, GimpPreview* preview)
{	
   /* if (mat.depth() != CV_8U) {
        //throw IncompatibleMat("cv::Mat depth is not CV_8U");
        g_message("cv::Mat depth is not CV_8U\n");
        //return;
	}*/

    if (mat.channels() < 0 || (guint)mat.channels() != drawable->bpp) {
        //throw IncompatibleMat("The number of channels in the cv::Mat and in GimpDrawable are diferent.");
        g_message("The number of channels in the cv::Mat and in GimpDrawable are diferent.\n");
        return;
	}

    gint x1, y1, x2, y2, width, height;
    
    if(preview == NULL) {
		gimp_drawable_mask_bounds(drawable->drawable_id,
								  &x1, &y1,
								  &x2, &y2);
								  
		width = x2 - x1;
		height = y2 - y2;
		
	} else {
		gimp_preview_get_position (preview, &x1, &y1);
		gimp_preview_get_size (preview, &width, &height);
		x2 = x1 + width;
		y2 = y1 + height;
	}
	
    GimpPixelRgn rgn;
    gimp_pixel_rgn_init(&rgn,
                        drawable,
                        x1, y1,
                        width, height,
                        preview == NULL, TRUE);

    gimp_pixel_rgn_set_rect(&rgn,
                            mat.data,
                            x1, y1,
                            width, height);

	if(preview == NULL) {
	    gimp_drawable_flush(drawable);
	    gimp_drawable_merge_shadow(drawable->drawable_id, TRUE);
	    gimp_drawable_update(drawable->drawable_id,
	                         x1, y1,
	                         width, height);
	} else {
		gimp_drawable_preview_draw_region (GIMP_DRAWABLE_PREVIEW (preview),
                                         &rgn);
	}
}
	
