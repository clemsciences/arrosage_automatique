package besnier.jardinosage;

import android.app.Activity;
import android.content.Context;
import android.graphics.Bitmap;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Bundle;
import android.util.Log;
import android.view.Gravity;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TableLayout;
import android.widget.TableRow;
import android.widget.TextView;


import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class MainActivity extends Activity {

    private static final String TAG = MainActivity.class.getSimpleName();
    final String[] lig1 = {"Heure", "Température", "Hygrométrie", "Pression"};
    final String[] col1 = {"00h", "01h", "02h", "03h", "04h", "05h", "06h", "07h", "08h", "09h",
            "10h", "11h", "12h", "13h", "14h", "15h", "16h", "17h", "18h", "19h", "20h", "21h", "22h",
            "23h"};

    TableLayout table;// on prend le tableau défini dans le layout
    TableRow row; // création d'un élément : ligne
    TextView tv1, tv2; // création des cellules

    @Override
    protected void onCreate(final Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

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

        //istNetzwerkVerfuegbar();
        new Thread(new Runnable() {
            public void run() {
                try {
                    Log.d(TAG, "on récupère les données");

                    final ArrayList<DataMeteorologicae> donnee_aujourdhui = ConnexionAPI.getDataToday();
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


    public void update_table(ArrayList<DataMeteorologicae> donnee_aujourdhui) {

        table.removeAllViewsInLayout();
        TableRow row1; // création d'un élément : ligne
        TextView tv1, tv2; // création des cellules

        // pour chaque ligne
        for (int i = 0; i < col1.length + 1; i++) {
            row1 = new TableRow(this); // création d'une nouvelle ligne
            Log.d(TAG, "ligne" + i);
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
                    DataMeteorologicae dm = donnee_aujourdhui.get(i-1);
                    TextView cellule = new TextView(this);
                    if (j == 1) {
                        Log.d(TAG, dm.temperature);
                        cellule.setText(dm.temperature);
                    } else if (j == 2) {
                        Log.d(TAG, dm.hygrometrie);
                        cellule.setText(dm.hygrometrie);
                    } else if (j == 3) {
                        Log.d(TAG, dm.pression);
                        cellule.setText(dm.pression);
                    }
                    cellule.setLayoutParams(new TableRow.LayoutParams(0, android.view.ViewGroup.LayoutParams.WRAP_CONTENT, 1));
                    row1.addView(cellule);
                }
                }
            table.addView(row1);
            }

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

