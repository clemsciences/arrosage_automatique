package besnier.jardinosage;

import android.app.Activity;

import android.content.Intent;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.util.Log;
import android.view.Gravity;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.ImageView;


import java.util.ArrayList;
import java.util.Calendar;

/**
 * Created by Clément on 07/06/2017.
 */
public class CourbesActivity extends Activity{

    private static final String TAG = MainActivity.class.getSimpleName();

//    Calendar rightNow = Calendar.getInstance();
//    int jour_selectionnee;  // = rightNow.get(Calendar.DAY_OF_MONTH);
//    int mois_selectionnee;  // = rightNow.get(Calendar.MONTH)+1;
//    int annee_selectionnee;  // = rightNow.get(Calendar.YEAR);

//    DateObservation date_aujourdhui = new DateObservation(jour_selectionnee, mois_selectionnee, annee_selectionnee);
    DateObservation date_selectionnee;

    TextView text_date;
    ImageView image_press_vue;
    ImageView image_temp_vue;
    ImageView image_humi_vue;

    Button bouton_precedent_courbes;
    Button bouton_suivant_courbes;
    Button bouton_vers_tableau;



    @Override
    protected void onCreate(final Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.courbes_layout);

        text_date = (TextView) findViewById(R.id.textDateView);

//        jour_selectionnee = intent.getIntExtra("jour",0); //24
//        mois_selectionnee = intent.getIntExtra("mois",0); //24
//        annee_selectionnee = intent.getIntExtra("annee",0); //24

        // On récupère la date sélectionnées par l'activité principale
        date_selectionnee = (DateObservation) getIntent().getSerializableExtra("date");

        text_date.setText(date_selectionnee.toString());

        image_press_vue = (ImageView) findViewById(R.id.imagePressionView);
        image_temp_vue = (ImageView) findViewById(R.id.imageTempeView);
        image_humi_vue = (ImageView) findViewById(R.id.imageHumiView);

        bouton_precedent_courbes = (Button) findViewById(R.id.button_precedent_courbe);
        bouton_suivant_courbes = (Button) findViewById(R.id.button_suivant_courbe);
        bouton_vers_tableau = (Button) findViewById(R.id.button_tableau);

        bouton_precedent_courbes.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                date_selectionnee = date_selectionnee.getPreviousDay();
                new Thread(new Runnable() {
                    public void run() {
                        try {
                            Log.d(TAG, "on récupère les données");

                            final Bitmap im_tempe = ConnexionAPI.getTemperatureImageDay(date_selectionnee.s_annee, date_selectionnee.s_mois, date_selectionnee.s_jour);
                            final Bitmap im_humi = ConnexionAPI.getHumiditeImageDay(date_selectionnee.s_annee, date_selectionnee.s_mois, date_selectionnee.s_jour);
                            final Bitmap im_press = ConnexionAPI.getPressionImageDay(date_selectionnee.s_annee, date_selectionnee.s_mois, date_selectionnee.s_jour);

                            runOnUiThread(new Runnable() {
                                              @Override
                                              public void run() {
                                                  Log.d(TAG, "on va mettre à jour les courbes");
                                                  image_press_vue.setImageBitmap(im_press);
                                                  image_temp_vue.setImageBitmap(im_tempe);
                                                  image_humi_vue.setImageBitmap(im_humi);
                                                  text_date.setText(date_selectionnee.toString());
                                              }
                                          }

                            );
                        } catch (Exception e /* IOException, MalformedURLException, JSONException */) {
                            Log.e(TAG, "getWeather()", e);
                        }
                    }
                }).start();

            }
        });

        bouton_suivant_courbes.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                date_selectionnee = date_selectionnee.getNextDay();
                new Thread(new Runnable() {
                    public void run() {
                        try {
                            Log.d(TAG, "on récupère les données");

                            final Bitmap im_tempe = ConnexionAPI.getTemperatureImageDay(date_selectionnee.s_annee, date_selectionnee.s_mois, date_selectionnee.s_jour);
                            final Bitmap im_humi = ConnexionAPI.getHumiditeImageDay(date_selectionnee.s_annee, date_selectionnee.s_mois, date_selectionnee.s_jour);
                            final Bitmap im_press = ConnexionAPI.getPressionImageDay(date_selectionnee.s_annee, date_selectionnee.s_mois, date_selectionnee.s_jour);

                            runOnUiThread(new Runnable() {
                                              @Override
                                              public void run() {
                                                  Log.d(TAG, "on va mettre à jour les courbes");
                                                  image_press_vue.setImageBitmap(im_press);
                                                  image_temp_vue.setImageBitmap(im_tempe);
                                                  image_humi_vue.setImageBitmap(im_humi);
                                                  text_date.setText(date_selectionnee.toString());

                                              }
                                          }

                            );
                        } catch (Exception e /* IOException, MalformedURLException, JSONException */) {
                            Log.e(TAG, "getWeather()", e);
                        }
                    }
                }).start();


            }
        });

        bouton_vers_tableau.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent i = new Intent(CourbesActivity.this, MainActivity.class);
                i.putExtra("date", date_selectionnee);
                startActivity(i);
            }
        });



        //istNetzwerkVerfuegbar();
        new Thread(new Runnable() {
            public void run() {
                try {
                    Log.d(TAG, "on récupère les données");

                    final Bitmap im_tempe = ConnexionAPI.getTemperatureImageDay(date_selectionnee.s_annee, date_selectionnee.s_mois, date_selectionnee.s_jour);
                    final Bitmap im_humi = ConnexionAPI.getHumiditeImageDay(date_selectionnee.s_annee, date_selectionnee.s_mois, date_selectionnee.s_jour);
                    final Bitmap im_press = ConnexionAPI.getPressionImageDay(date_selectionnee.s_annee, date_selectionnee.s_mois, date_selectionnee.s_jour);


                    runOnUiThread(new Runnable() {
                                      @Override
                                      public void run() {
                                          Log.d(TAG, "on va mettre à jour les courbes");
                                          image_press_vue.setImageBitmap(im_press);
                                          image_temp_vue.setImageBitmap(im_tempe);
                                          image_humi_vue.setImageBitmap(im_humi);
                                          text_date.setText(date_selectionnee.toString());
                                      }
                                  }

                    );
                } catch (Exception e /* IOException, MalformedURLException, JSONException */) {
                    Log.e(TAG, "getWeather()", e);
                }
            }
        }).start();


    }
    @Override
    protected void onStart()
    {
        super.onStart();

    }

    @Override
    protected void onRestart()
    {
        super.onRestart();
        date_selectionnee = (DateObservation) getIntent().getSerializableExtra("date");

    }

    @Override
    protected void onResume()
    {
        super.onResume();

    }
    @Override
    protected void onPause()
    {
        super.onPause();
    }

    @Override
    protected void onDestroy()
    {
        super.onDestroy();
    }

}

