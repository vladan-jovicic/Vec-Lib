## Process this file with automake to produce Makefile.in

bin_PROGRAMS = vectrabool

bindir = $(GIMP_LIBDIR)/plug-ins

vectrabool_SOURCES = \
	plugin-intl.h	\
	interface.c	\
	interface.h	\
	main.c		\
	main.h		\
	render.c	\
	render.h	\
	contdet.c	\
	contdet.h

AM_CPPFLAGS = \
	-DLOCALEDIR=\""$(LOCALEDIR)"\"		\
	-DDATADIR=\""$(DATADIR)"\"

INCLUDES =\
	-I$(top_srcdir)		\
	@GIMP_CFLAGS@		\
	-I$(includedir)

LDADD = $(GIMP_LIBS) -lm

