#include <libgimp/gimp.h>
#include "contdet.h"

typedef struct
{
	gint radius;
} GaussBlurValues;


/* Set up default values for options */
static GaussBlurValues bvals =
{
	3  /* radius */
};


/* Declare local functions.
 */
static void      query  (void);
static void      run    (const gchar*       name,
                         gint         		nparams,
                         const GimpParam*   param,
                         gint*        		nreturn_vals,
                         GimpParam**  		return_vals);

static void      stripes_demo         (GimpDrawable *drawable);

GimpPlugInInfo PLUG_IN_INFO =
{
  NULL,  /* init_proc  */
  NULL,  /* quit_proc  */
  query, /* query_proc */
  run,   /* run_proc   */
};


MAIN ()

static void
      query (void)
        {
          static GimpParamDef args[] = {
            {
              GIMP_PDB_INT32,
              "run-mode",
              "Run mode"
            },
            {
              GIMP_PDB_IMAGE,
              "image",
              "Input image"
            },
            {
              GIMP_PDB_DRAWABLE,
              "drawable",
              "Input drawable"
            }
          };

          gimp_install_procedure (
            "Vectrabool-plugin",
            "Image vectorization plug-in",
            "Translates an image to .svg format",
            "Vectrabool team - https://vladan-jovicic.github.io/Vec-Lib/",
            "",
            "2017",
            "<Image>/Image/Transform/Vectorize",
            "RGB*, GRAY*",
            GIMP_PLUGIN,
            G_N_ELEMENTS (args), 0,
            args, NULL);

            //gimp_plugin_menu_register ("Vectrabool-plugin",
            //                           "/Image/Transorm"); 
        }

static void
     run (const gchar*      name,
          gint              nparams,
          const GimpParam*  param,
          gint*             nreturn_vals,
          GimpParam**       return_vals)
{
	static GimpParam  values[1];
	GimpPDBStatusType status = GIMP_PDB_SUCCESS;
	GimpRunMode       run_mode;

   /* Setting mandatory output values */
	*nreturn_vals = 1;
	*return_vals  = values;

	values[0].type = GIMP_PDB_STATUS;
	values[0].data.d_status = status;

   /* Getting run_mode - we won't display a dialog if 
	* we are in NONINTERACTIVE mode */
	run_mode = param[0].data.d_int32;

   /*  Get the specified drawable  */
	GimpDrawable* drawable = gimp_drawable_get(param[2].data.d_drawable);

	double r = 3;
	
	gaussian_blur(drawable, r);
	
	g_message("end of blur\n");

	gimp_displays_flush();
	gimp_drawable_detach (drawable);
}
