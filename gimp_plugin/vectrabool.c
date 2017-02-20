#include <libgimp/gimp.h>


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

       if (run_mode != GIMP_RUN_NONINTERACTIVE)
         g_message("Hello, world!\n");
     }


//static void
//stripes_demo (GimpDrawable *drawable)
//{
  //GimpPixelRgn src_rgn, dest_rgn;
  //guchar *src, *s;
  //guchar *dest, *d;
  //gint    progress, max_progress;
  //gint    has_alpha, red, green, blue, alpha;
  //gint    x1, y1, x2, y2;
  //gint    x, y;
  //gpointer pr;

  ///* Get selection area */
  //gimp_drawable_mask_bounds (drawable->id, &x1, &y1, &x2, &y2);
  //has_alpha = gimp_drawable_has_alpha (drawable->id);

  //red = 0; green = 1; blue = 2;

  //alpha = (has_alpha) ? drawable->bpp - 1 : drawable->bpp;

  ///* Initialize progress */
  //progress = 0;
  //max_progress = (x2 - x1) * (y2 - y1);

  ///* substitute pixel vales */
  //gimp_pixel_rgn_init (&src_rgn, drawable,
                       //x1, y1, (x2 - x1), (y2 - y1), FALSE, FALSE);
  //gimp_pixel_rgn_init (&dest_rgn, drawable,
                       //x1, y1, (x2 - x1), (y2 - y1), TRUE, TRUE);

  //for (pr = gimp_pixel_rgns_register (2, &src_rgn, &dest_rgn);
       //pr != NULL;
       //pr = gimp_pixel_rgns_process (pr))
    //{
      //src = src_rgn.data;
      //dest = dest_rgn.data;

      //for (y = 0; y < src_rgn.h; y++)
        //{
          //s = src;
          //d = dest;

          //for (x = 0; x < src_rgn.w; x++)
            //{
              //d[0] = (src_rgn.x + x + src_rgn.y + y) % 256;
              //d[1] = s[1];
              //d[2] = (- src_rgn.x - x + src_rgn.y + y) % 256;
              //if (has_alpha)
                //d[alpha] = s[alpha];

              //s += src_rgn.bpp;
              //d += dest_rgn.bpp;
            //}

          //src += src_rgn.rowstride;
          //dest += dest_rgn.rowstride;
        //}

      ///* Update progress */
      //progress += src_rgn.w * src_rgn.h;

      //gimp_progress_update ((double) progress / (double) max_progress);
    //}

  ///*  update the region  */
  //gimp_drawable_flush (drawable);
  //gimp_drawable_merge_shadow (drawable->id, TRUE);
  //gimp_drawable_update (drawable->id, x1, y1, (x2 - x1), (y2 - y1));
//}
