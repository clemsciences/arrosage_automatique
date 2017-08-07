package besnier.jardinosage;

import java.io.Serializable;

/**
 * Created by Clément on 07/06/2017.
 */
public class DateObservation implements Serializable {
    int jour;
    int mois;
    int annee;
    String s_jour;
    String s_mois;
    String s_annee;

    public DateObservation(int jour, int mois, int annee)
    {
        this.jour = jour;
        this.mois = mois;
        this.annee = annee;
        update_string_values();
    }


    public DateObservation getPreviousDay()
    {
        DateObservation previous_day;
        if (jour == 1 && mois == 1)
        {
            previous_day = new DateObservation(31, 12, annee-1);
        }
        else if(jour == 1 && (mois == 5 || mois == 7 || mois == 8 || mois == 10 || mois == 12)){
            previous_day = new DateObservation(30, mois-1, annee);
        }
        else if(jour == 1 && mois == 3 && annee % 4 == 0)
        {
            previous_day = new DateObservation(29, mois-1, annee);
        }
        else if(jour == 1 && mois == 3 && annee % 4 != 0)
        {
            previous_day = new DateObservation(28, mois-1, annee);
        }
        else if(jour == 1 && (mois == 4 || mois == 6 || mois == 9 || mois == 11)){
            previous_day = new DateObservation(31, mois-1, annee);
        }
        else{
            previous_day = new DateObservation(jour - 1, mois, annee);
        }
        return previous_day;
    }

    public DateObservation getNextDay()
    {
        DateObservation next_day;
        if (jour == 31 && mois == 12)
        {
            next_day = new DateObservation(1, 1, annee+1);
        }
        else if(jour == 31 && (mois == 1 || mois == 3 || mois == 5 || mois == 7 || mois == 8 || mois == 10 )){
            next_day = new DateObservation(1, mois+1, annee);
        }
        else if(jour == 28 && mois == 2 && annee % 4 == 0)
        {
            next_day = new DateObservation(29, mois, annee);
        }
        else if(jour == 28 && mois == 2 && annee % 4 != 0)
        {
            next_day = new DateObservation(1, mois+1, annee);
        }
        else if(jour == 29 && mois == 2 && annee % 4 == 0)
        {
            next_day = new DateObservation(1, mois+1, annee);
        }
        else if(jour == 30 && (mois == 4 || mois == 6 || mois == 9 || mois == 11)){
            next_day = new DateObservation(1, mois+1, annee);
        }
        else{
            next_day = new DateObservation(jour + 1, mois, annee);
        }
        return next_day;
    }
    public void update_string_values()
    {
        s_jour = Integer.toString(jour);
        s_mois = Integer.toString(mois);
        s_annee = Integer.toString(annee);
    }

    public String toString()
    {
        return s_jour + "/" + s_mois+ "/" + s_annee;
    }


}
