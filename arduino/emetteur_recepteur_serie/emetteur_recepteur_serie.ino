/*
 * Ce code permet la réception de signaux se baladant sur une onde-électromégnétique de longueur d'onde 434MHz.
 */
#include <VirtualWire.h> // On inclut la librairie VirtualWire
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP085_U.h>


const char ordre_allumer_pompe[] = "allumer_pompe";
const char ordre_eteindre_pompe[] = "eteindre_pompe";

const char ordre_donner_temperature[] = "donner_temperature";
const char ordre_donner_humidite[] = "donner_humidite";

const char verification_connexion[] = "connexion_bet";
const char resultat_connexion[] = "connexion_bet_ok";

const uint8_t tranceiverPin = 6;
const uint8_t receiverPin = 4;
long euh = millis();

int octet_lu = 0;

Adafruit_BMP085_Unified bmp = Adafruit_BMP085_Unified(10085);

void setup()
{
    Serial.begin(9600); // Initialisation du port série pour avoir un retour sur le serial monitor
    //Pour l'émission et la réception
    vw_setup(1000);  // Initialisation de la librairie VirtualWire à 2400 bauds  (maximum de mon module)
    vw_set_rx_pin(receiverPin);   // On indique que l'on veut utiliser la broche 2 pour recevoir
    vw_set_tx_pin(tranceiverPin);     // On indique que l'on veut utiliser la pin 10 de l'Arduino pour émettre
    vw_rx_start();      // Activation de la partie réception de la librairie VirtualWire
    /* Initialise the sensor */
    if(!bmp.begin())
    {
      /* There was a problem detecting the BMP085 ... check your connections */
      Serial.print("Ooops, no BMP085 detected ... Check your wiring or I2C ADDR!");
    }
    Serial.println("ca commence");

}

void loop()
{
    //Pour l'envoi périodique de demande
    unsigned long curMillis = millis();
    
    //partie réception radio et émission série
    uint8_t buf[VW_MAX_MESSAGE_LEN]; // Tableau qui va contenir le message recu (de taille maximum VW_MAX_MESSAGE_LEN)
    uint8_t buflen = VW_MAX_MESSAGE_LEN; // Taille maximum du buffer
    if (vw_have_message()) // Si on a un message dans le buffer
    {
        if (vw_get_message(buf, &buflen)) // Alors on récupère ce message qu'il soit entier ou pas
        {
          char msg_received[buflen];
          int i;
          Serial.print("RX : ");
          
          for (i = 0; i < buflen; i++) // On affiche tout ce que l'on a
          {
              Serial.print(char(buf[i]));
              msg_received[i] = char(buf[i]);
              
          }
          Serial.println("");
        }
    }
    //Partie réception série et émission radio
    if(Serial.available() > 0)
    {
      octet_lu = Serial.read();
      //Serial.println(octet_lu);
      if(octet_lu == 116 ) //116 <=> t
      {
        //demander température
        vw_send((uint8_t *)ordre_donner_temperature,strlen(ordre_donner_temperature)); // On envoie le message 
        vw_wait_tx();
      }
      else if(octet_lu == 104) //104 <=> h
      {
        //demander humidité
        vw_send((uint8_t *)ordre_donner_humidite,strlen(ordre_donner_humidite)); // On envoie le message 
        vw_wait_tx();
      }
      else if(octet_lu == 97 ) // 97 <=> a
      {
        //allumer pompe
        vw_send((uint8_t *)ordre_allumer_pompe,strlen(ordre_allumer_pompe)); // On envoie le message 
        vw_wait_tx();
      }
      else if(octet_lu == 101) //101 <=> e
      {
        //eteindre pompe
        vw_send((uint8_t *)ordre_eteindre_pompe,strlen(ordre_eteindre_pompe)); // On envoie le message 
        vw_wait_tx();
      }
      else if(octet_lu == 111) //111 <=> o
      {
        //vrification de la connexion
        vw_send((uint8_t *)verification_connexion,strlen(verification_connexion)); // On envoie le message 
        vw_wait_tx();
        Serial.println("demande de connexion...");
      }
      else if(octet_lu == 105) //105 <=> i
      {
        float temperature;
        bmp.getTemperature(&temperature);
        Serial.print("temperature_interieure: ");
        Serial.print(temperature);
        Serial.println(" C");
      }
      else if(octet_lu == 112) //112 <=> p
      {
          //demande de la pression
          sensors_event_t event;
          bmp.getEvent(&event);
          if (event.pressure)
          {
            /* Display atmospheric pressue in hPa */
            Serial.print("pression:");
            Serial.print(event.pressure+7.23); //calibration
            Serial.println(" hPa");            
          }
          
          else
          {
            Serial.println("Probleme avec le barometre");
          }
        }
      }   
}
