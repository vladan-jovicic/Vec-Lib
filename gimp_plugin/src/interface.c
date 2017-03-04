/* GIMP Plug-in Template
 * Copyright (C) 2000-2004  Michael Natterer <mitch@gimp.org> (the "Author").
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

#include "config.h"

#include <libgimp/gimp.h>
#include <libgimp/gimpui.h>

#include "main.h"
#include "interface.h"
#include "render.h"

#include "plugin-intl.h"


/*  Constants  */

#define SCALE_WIDTH        180
#define SPIN_BUTTON_WIDTH   75
#define RANDOM_SEED_WIDTH  100


/*  Local function prototypes  */

static gboolean   dialog_image_constraint_func (gint32    image_id,
                                                gpointer  data);


/*  Local variables  */

static PlugInUIVals *ui_state = NULL;


/*  Public functions  */

gboolean
dialog (gint32              image_ID,
	GimpDrawable       *drawable,
	arg* data)
{
  GtkWidget *dlg;
  GtkWidget *main_vbox;
  GtkWidget *preview;
  GtkWidget *frame;
  GtkWidget *table;
  GtkWidget *hbox;
  GtkWidget *hbox2;
  GtkWidget *coordinates;
  GtkWidget *combo;
  GtkObject *adj;
  gint       row;
  gboolean   run = FALSE;
  GimpUnit   unit;
  gdouble    xres, yres;

  ui_state = data -> ui_vals;

  gimp_ui_init (PLUGIN_NAME, FALSE);

  dlg = gimp_dialog_new (_("Vectrabool"), PLUGIN_NAME,
                         NULL, 0,
			 gimp_standard_help_func, "vectrabool",

			 GTK_STOCK_CANCEL, GTK_RESPONSE_CANCEL,
			 GTK_STOCK_OK,     GTK_RESPONSE_OK,

			 NULL);

  main_vbox = gtk_vbox_new (FALSE, 12);
  gtk_container_set_border_width (GTK_CONTAINER (main_vbox), 12);
  gtk_container_add (GTK_CONTAINER (GTK_DIALOG (dlg)->vbox), main_vbox);
  gtk_widget_show(main_vbox);
  
  preview = gimp_drawable_preview_new (drawable, &data -> vals -> preview);
  gtk_box_pack_start (GTK_BOX (main_vbox), preview, TRUE, TRUE, 0);
  gtk_widget_show (preview);

  /*  gimp_scale_entry_new() examples  */

  frame = gimp_frame_new (_("contour detection parameters"));
  gtk_widget_show (frame);  
  gtk_box_pack_start (GTK_BOX (main_vbox), frame, TRUE, TRUE, 0);

  table = gtk_table_new (3, 3, FALSE);
  gtk_table_set_col_spacings (GTK_TABLE (table), 6);
  gtk_table_set_row_spacings (GTK_TABLE (table), 2);
  gtk_container_add (GTK_CONTAINER (frame), table);
  gtk_widget_show (table);

  row = 0;

  adj = gimp_scale_entry_new (GTK_TABLE (table), 0, row++,
			      _("low threshold :"), SCALE_WIDTH, SPIN_BUTTON_WIDTH,
			      data -> vals->low_threshold, 0, 255, 1, 10, 0,
			      TRUE, 0, 0,
			      _("low threshold"), NULL);
			      
  gtk_box_pack_start (GTK_BOX (main_vbox), adj, FALSE, FALSE, 0);
  gtk_widget_show (adj);

  /*  gimp_random_seed_new() example  

  frame = gimp_frame_new (_("A Random Seed Entry"));
  gtk_box_pack_start (GTK_BOX (main_vbox), frame, FALSE, FALSE, 0);
  gtk_widget_show (frame);
  hbox = gtk_hbox_new (FALSE, 6);
  gtk_container_add (GTK_CONTAINER (frame), hbox);
  gtk_widget_show (hbox);

  hbox2 = gimp_random_seed_new (&vals->seed, &vals->random_seed);
  gtk_widget_set_size_request (GTK_WIDGET (GIMP_RANDOM_SEED_SPINBUTTON (hbox2)),
                               RANDOM_SEED_WIDTH, -1);
  gtk_box_pack_start (GTK_BOX (hbox), hbox2, FALSE, FALSE, 0);
  gtk_widget_show (hbox2);

  /*  Image and drawable menus  

  frame = gimp_frame_new (_("Image and Drawable Menu Examples"));
  gtk_box_pack_start (GTK_BOX (main_vbox), frame, FALSE, FALSE, 0);
  gtk_widget_show (frame);

  table = gtk_table_new (3, 2, FALSE);
  gtk_container_set_border_width (GTK_CONTAINER (table), 4);
  gtk_table_set_col_spacings (GTK_TABLE (table), 4);
  gtk_table_set_row_spacings (GTK_TABLE (table), 2);
  gtk_container_add (GTK_CONTAINER (frame), table);
  gtk_widget_show (table);

  row = 0;

  combo = gimp_layer_combo_box_new (NULL, NULL);
  gimp_int_combo_box_connect (GIMP_INT_COMBO_BOX (combo), drawable->drawable_id,
                              G_CALLBACK (gimp_int_combo_box_get_active),
                              &drawable_vals->drawable_id);

  gimp_table_attach_aligned (GTK_TABLE (table), 0, row++,
			     _("Layers:"), 0.0, 0.5, combo, 1, FALSE);

  combo = gimp_image_combo_box_new (dialog_image_constraint_func, NULL);
  gimp_int_combo_box_connect (GIMP_INT_COMBO_BOX (combo), image_ID,
                              G_CALLBACK (gimp_int_combo_box_get_active),
                              &image_vals->image_id);

  gimp_table_attach_aligned (GTK_TABLE (table), 0, row++,
			     _("RGB Images:"), 0.0, 0.5, combo, 1, FALSE); */

  /*  Show the main containers  */
  

  g_signal_connect (preview, "invalidated",
                            G_CALLBACK (handle_invalidate),
                            data);
                            
  g_signal_connect_swapped (adj, "value_changed",
                            G_CALLBACK (gimp_preview_invalidate),
                            preview);
                            
  g_signal_connect (adj, "value_changed",
                    G_CALLBACK (gimp_int_adjustment_update),
                    &(data -> vals -> low_threshold));
                            
  //render(data);
    

  //gtk_widget_show (main_vbox);
  gtk_widget_show (dlg);

  run = (gimp_dialog_run (GIMP_DIALOG (dlg)) == GTK_RESPONSE_OK);
  
  data -> preview = NULL;
 

  if (run)
    {
      /*  Save ui values  */
      ui_state->chain_active =
        gimp_chain_button_get_active (GIMP_COORDINATES_CHAINBUTTON (coordinates));
    }

  gtk_widget_destroy (dlg);

  return run;
}

void handle_invalidate(GtkWidget* preview, arg* data)
{
	data -> preview = GIMP_PREVIEW(preview);
	render(data);
}


/*  Private functions  */

static gboolean
dialog_image_constraint_func (gint32    image_id,
                              gpointer  data)
{
  return (gimp_image_base_type (image_id) == GIMP_RGB);
}
