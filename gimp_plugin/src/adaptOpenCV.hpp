#ifndef ADAPT_OPENCV_HPP
#define ADAPT_OPENCV_HPP

#include <libgimp/gimp.h>
#include <libgimp/gimpui.h>

#ifdef __cplusplus
// Public

// extern "C" so that this C++ function is callable from C
extern "C" {
#endif
void renderUsingOpenCV (
    GimpDrawable *drawable,
    GimpPreview  *preview,
    gint32,
    gint32
);
#ifdef __cplusplus
}
#endif

// Private

void
getUpperLeftWidthHeightOfDrawable (
    GimpDrawable *drawable,
    gint* leftX,
    gint* upperY,
    gint* width,
    gint* height
);

cv::Mat
adaptDrawableToOpenCV (
    GimpDrawable *drawable,
    guchar *rect,
    gint left,
    gint upper,
    gint width,
    gint height
);

void
adaptOpenCVToDrawable (
    GimpDrawable *drawable,
    guchar *rect,
    gint left,
    gint upper,
    gint width,
    gint height
);

void setMatToDrawable(cv::Mat&, GimpDrawable*, GimpPreview*);
cv::Mat drawableToMat(GimpDrawable*, GimpPreview*);

#endif
