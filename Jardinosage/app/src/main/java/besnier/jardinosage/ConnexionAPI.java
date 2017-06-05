package besnier.jardinosage;

/**
 * Created by Clément on 04/06/2017.
 */

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.util.Log;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.text.MessageFormat;
import java.util.ArrayList;

public class ConnexionAPI {

    private static final String URL = "http://arrobes.hopto.org/data/aujourdhui";
    private static final String URL_date = "http://arrobes.hopto.org/data/{0}/{1}/{2}";

    static private ArrayList<DataMeteorologicae> data;
    private static final String TAG = MainActivity.class.getSimpleName();


    public static ArrayList<DataMeteorologicae> getDataDay(String year, String month, String day) throws JSONException,
            IOException /* MalformedURLException */ {

        JSONObject jsonObject = new JSONObject(getFromServer(MessageFormat.format(URL_date, year, month, day)));
        data = new ArrayList<>();

        for(int i=0; i<24; i++)
        {
            if(jsonObject.has(Integer.toString(i)))
            {
                JSONObject mesure = jsonObject.getJSONObject(Integer.toString(i));
                data.add(new DataMeteorologicae(i, mesure.getString("humidite"), mesure.getString("temperature"),
                        mesure.getString("pression")));
            }
            else
            {
                data.add(new DataMeteorologicae(i, "", "", ""));
            }
        }
        return data;
    }


    public static ArrayList<DataMeteorologicae> getDataToday() throws JSONException,
            IOException /* MalformedURLException */ {
        String a = getFromServer(URL);
        String TAG = MainActivity.class.getSimpleName();

        Log.d(TAG, a);
        JSONObject jsonObject = new JSONObject(a);
        data = new ArrayList<>();

        for (int i = 0; i < 24; i++) {
            if (jsonObject.has(Integer.toString(i))) {
                JSONObject mesure = jsonObject.getJSONObject(Integer.toString(i));
                Log.d(TAG, mesure.getString("humidite")+""+ mesure.getString("temperature")+""+mesure.getString("pression"));
                data.add(new DataMeteorologicae(i, mesure.getString("humidite"), mesure.getString("temperature"),
                        mesure.getString("pression")));
            } else {
                data.add(new DataMeteorologicae(i, "", "", ""));
            }
        }
        Log.d(TAG, Integer.toString(data.size()));
        return data;
    }

    public static String getFromServer(String url)
            throws IOException /* MalformedURLException */ {
        StringBuilder sb = new StringBuilder();
        Log.d(TAG, url);
        URL _url = new URL(url);
        HttpURLConnection httpURLConnection = (HttpURLConnection) _url
                .openConnection();
        //Log.d(TAG, httpURLConnection.getErrorStream().toString());
        Log.d(TAG, "on va voir la connxion");
        final int responseCode = httpURLConnection.getResponseCode();
        if (responseCode == HttpURLConnection.HTTP_OK) {
            Log.d(TAG, "La connxion st bonn");
            InputStreamReader inputStreamReader = new InputStreamReader(
                    httpURLConnection.getInputStream());
            BufferedReader bufferedReader = new BufferedReader(
                    inputStreamReader);
            String line;
            while ((line = bufferedReader.readLine()) != null) {
                sb.append(line);
            }
            try {
                bufferedReader.close();
            } catch (IOException e) {
                // ein Fehler beim Schließen wird bewusst ignoriert
            }
        }
        httpURLConnection.disconnect();
        return sb.toString();
    }

    /*public static Bitmap getImage(WeatherData w) throws IOException  {
        URL req = new URL("http://openweathermap.org/img/w/" + w.icon + ".png");
        HttpURLConnection c = (HttpURLConnection) req.openConnection();
        Bitmap bmp = BitmapFactory.decodeStream(c
                .getInputStream());
        c.disconnect();
        return bmp;
    }*/






}
