package besnier.jardinosage;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.Gravity;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.TableLayout;
import android.widget.TableRow;
import android.widget.TextView;


import java.util.ArrayList;
import java.util.Calendar;

public class MainActivity extends Activity {

    private static final String TAG = MainActivity.class.getSimpleName();
    final String[] lig1 = {"Heure", "Température", "Hygrométrie", "Pression"};
    final String[] col1 = {"00h", "01h", "02h", "03h", "04h", "05h", "06h", "07h", "08h", "09h",
            "10h", "11h", "12h", "13h", "14h", "15h", "16h", "17h", "18h", "19h", "20h", "21h", "22h",
            "23h"};

    TableLayout table;// on prend le tableau défini dans le layout
    TableRow row; // création d'un élément : ligne
    TextView tv1, tv2; // création des cellules




    TextView text_date;
    Button button_precedent;
    Button button_suivant;
    Button button_voir_courbes;
    DateObservation date_selectionnee;
    DateObservation date_aujourdhui;



    @Override
    protected void onCreate(final Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);


        date_selectionnee = (DateObservation) getIntent().getSerializableExtra("date");
        if (date_selectionnee == null)
        {
            Calendar rightNow = Calendar.getInstance();
            int jour_selectionne = rightNow.get(Calendar.DAY_OF_MONTH);
            int mois_selectionne = rightNow.get(Calendar.MONTH) + 1;
            int annee_selectionne = rightNow.get(Calendar.YEAR);

            date_selectionnee = new DateObservation(jour_selectionne, mois_selectionne, annee_selectionne);
            date_aujourdhui = new DateObservation(jour_selectionne, mois_selectionne, annee_selectionne);

        }

        text_date = (TextView) findViewById(R.id.textDateView);
        text_date.setText(date_selectionnee.toString());

        button_precedent = (Button) findViewById(R.id.buttonPrecedent);
        button_suivant = (Button) findViewById(R.id.buttonSuivant);
        button_voir_courbes = (Button) findViewById(R.id.button_courbes);

        //Le tableau

        table = (TableLayout) findViewById(R.id.idTable); // on prend le tableau défini dans le layout

        // pour chaque ligne
        for (int i = 0; i < col1.length + 1; i++) {
            row = new TableRow(this); // création d'une nouvelle ligne
            Log.println(1, "ok", "on a la connxion à Intrnt" + i);
            for (int j = 0; j < lig1.length; j++) {
                if (i == 0) {
                    tv1 = new TextView(this); // création cellule
                    tv1.setText(lig1[j]); // ajout du texte
                    tv1.setGravity(Gravity.LEFT); // centrage dans la cellule
                    // adaptation de la largeur de colonne à l'écran :
                    tv1.setLayoutParams(new TableRow.LayoutParams(0, android.view.ViewGroup.LayoutParams.WRAP_CONTENT, 1));
                    row.addView(tv1);
                } else if (j == 0) {
                    tv2 = new TextView(this);
                    tv2.setText(col1[i - 1]);
                    tv2.setGravity(Gravity.TOP);
                    tv2.setLayoutParams(new TableRow.LayoutParams(0, android.view.ViewGroup.LayoutParams.WRAP_CONTENT, 1));
                    row.addView(tv2);
                } else {
                    TextView cellule = new TextView(this);
                    row.addView(cellule);
                }

            }
            table.addView(row);
        }
        button_precedent.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View v) {

                new Thread(new Runnable() {

                    @Override
                    public void run() {
                        try {
                            date_selectionnee = date_selectionnee.getPreviousDay();
                            Log.d(TAG, date_selectionnee.s_annee+ date_selectionnee.s_mois+
                                    date_selectionnee.s_jour);
                            final ArrayList<DataMeteorologicae> donnees =
                                    ConnexionAPI.getDataDay(date_selectionnee.s_annee, date_selectionnee.s_mois,
                                            date_selectionnee.s_jour);
                            runOnUiThread(new Runnable() {
                                @Override
                                public void run() {
                                    update_table(donnees);
                                    text_date.setText(date_selectionnee.toString());
                                }
                            });
                        } catch (Exception e) {
                            Log.e(TAG, "getWeather()", e);
                        }
                    }
                }).start();
            }
        });

        button_suivant.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View v) {
                new Thread(new Runnable() {
                    @Override
                    public void run() {
                        try {
                            date_selectionnee = date_selectionnee.getNextDay();
                            Log.d(TAG, date_selectionnee.s_annee+ date_selectionnee.s_mois+
                                    date_selectionnee.s_jour);
                            final ArrayList<DataMeteorologicae> donnees =
                                    ConnexionAPI.getDataDay(date_selectionnee.s_annee, date_selectionnee.s_mois,
                                            date_selectionnee.s_jour);
                            runOnUiThread(new Runnable() {
                                @Override
                                public void run() {
                                    update_table(donnees);
                                    text_date.setText(date_selectionnee.toString());
                                }
                            });
                        }catch (Exception e )
                        {
                            Log.e(TAG, "getWeather()", e);
                        }
                    }
                }).start();
            }
        });


        button_voir_courbes.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent i = new Intent(MainActivity.this, CourbesActivity.class);
                i.putExtra("date", date_selectionnee);
                startActivity(i);
            }
        });

        //istNetzwerkVerfuegbar();
        new Thread(new Runnable() {
            public void run() {
                try {
                    Log.d(TAG, "on récupère les données");

                    final ArrayList<DataMeteorologicae> donnee_aujourdhui = ConnexionAPI.getDataDay(date_selectionnee.s_annee, date_selectionnee.s_mois, date_selectionnee.s_jour);
                    runOnUiThread(new Runnable() {
                                      @Override
                                      public void run() {
                                          Log.d(TAG, "on va mettre à jour le tableau");
                                          update_table(donnee_aujourdhui);

                                      }
                                  }
                    );
                } catch (Exception e /* IOException, MalformedURLException, JSONException */) {
                    Log.e(TAG, "getWeather()", e);
                }
            }
        }).start();






    }


    public void update_table(ArrayList<DataMeteorologicae> data) {

        table.removeAllViewsInLayout();
        TableRow row1; // création d'un élément : ligne
        TextView tv1, tv2; // création des cellules

        // pour chaque ligne
        for (int i = 0; i < col1.length + 1; i++) {
            row1 = new TableRow(this); // création d'une nouvelle ligne
            //Log.d(TAG, "ligne" + i);
            for (int j = 0; j < lig1.length; j++) {

                if (i == 0) {
                    tv1 = new TextView(this); // création cellule
                    tv1.setText(lig1[j]); // ajout du texte
                    tv1.setGravity(Gravity.LEFT); // centrage dans la cellule
                    // adaptation de la largeur de colonne à l'écran :
                    tv1.setLayoutParams(new TableRow.LayoutParams(0, android.view.ViewGroup.LayoutParams.WRAP_CONTENT, 1));
                    row1.addView(tv1);
                } else if (j == 0) {
                    tv2 = new TextView(this);
                    tv2.setText(col1[i - 1]);
                    tv2.setGravity(Gravity.TOP);
                    tv2.setLayoutParams(new TableRow.LayoutParams(0, android.view.ViewGroup.LayoutParams.WRAP_CONTENT, 1));
                    row1.addView(tv2);
                } else if(i > 0) {
                    DataMeteorologicae dm = data.get(i-1);
                    TextView cellule = new TextView(this);
                    if (j == 1) {
                        //Log.d(TAG, dm.temperature);
                        cellule.setText(dm.temperature);
                    } else if (j == 2) {
                        //Log.d(TAG, dm.hygrometrie);
                        cellule.setText(dm.hygrometrie);
                    } else if (j == 3) {
                        //Log.d(TAG, dm.pression);
                        cellule.setText(dm.pression);
                    }
                    cellule.setLayoutParams(new TableRow.LayoutParams(0, android.view.ViewGroup.LayoutParams.WRAP_CONTENT, 1));
                    row1.addView(cellule);
                }
                }
            table.addView(row1);
            }

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


//        final Button button = (Button) findViewById(R.id.button);
//        button.setOnClickListener(new OnClickListener() {
//
//            @Override
//            public void onClick(View v) {
//                new Thread(new Runnable() {
//                    public void run() {
//                        try {
//                            final WeatherData weather = WeatherUtils
//                                    .getWeather(city.getText().toString());
//                            final Bitmap bitmapWeather = WeatherUtils.getImage(weather);
//                            runOnUiThread(new Runnable() {
//
//                                @Override
//                                public void run() {
//                                    image.setImageBitmap(bitmapWeather);
//                                    beschreibung.setText(weather.description);
//                                    city.setText(weather.name);
//                                    Double temp = weather.temp - 273.15;
//                                    temperatur.setText(getString(R.string.temp_template, temp.intValue()));
//                                }
//
//                            });
//                        } catch (Exception e ) {
//                            Log.e(TAG, "getWeather()", e);
//                        }
//                    }
//                }).start();
//            }
//        });


//    private boolean istNetzwerkVerfuegbar() {
//        ConnectivityManager mgr = (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);
//        NetworkInfo info = mgr.getActiveNetworkInfo();
//        if (info != null && info.isConnected()) {
//            return true;
//        } else {
//            return false;
//        }
//    }

