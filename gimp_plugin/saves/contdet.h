#ifndef CONTDET_H
#define CONTDET_H

int gaussian_blur(GimpDrawable* drawable, int r);

void boxes(double sigma, unsigned int n, double* sizes);

void boxBlur(GimpPixelRgn* in, GimpPixelRgn* out, gint w, gint h, double r);

void boxBlurH(GimpPixelRgn* in, GimpPixelRgn* out, gint w, gint h, double r);

void boxBlurT(GimpPixelRgn* in, GimpPixelRgn* out, gint w, gint h, double r);

#endif
