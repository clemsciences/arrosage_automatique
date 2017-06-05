package besnier.jardinosage;

/**
 * Created by Clément on 04/06/2017.
 */
public class DataMeteorologicae {
    int heure;
    String hygrometrie = "";
    String temperature = "";
    String pression = "";

    public DataMeteorologicae(int heure, String hygrometrie, String temperature, String pression)
    {
        this.heure = heure;
        this.hygrometrie = hygrometrie;
        this.temperature = temperature;
        this.pression = pression;
    }
}
