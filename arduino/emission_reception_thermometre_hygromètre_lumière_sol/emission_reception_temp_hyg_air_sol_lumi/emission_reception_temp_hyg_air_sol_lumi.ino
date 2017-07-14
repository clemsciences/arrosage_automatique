
#include <Wire.h>
#include <VirtualWire.h> // On inclut la librairie VirtualWire
#include "Adafruit_HTU21DF.h"

// Connect Vin to 3-5VDC
// Connect GND to ground
// Connect SCL to I2C clock pin (A5 on UNO)
// Connect SDA to I2C data pin (A4 on UNO)
const int photometrePin = 0;
const int hygrometreSolPin = 2;

const uint8_t tranceiverPin = 8;
const uint8_t receiverPin = 6;

const uint32_t TRHSTEP   = 10000UL; // période de mesure



int luminosity;
int hygrometrie_sol;
float temperature;
float humidite_air;

String prefix_luminosity = "LU_";
String prefix_hygrometrie_sol = "HS_";
String prefix_temperature = "TE_";
String prefix_humidite_air = "HA_";
Adafruit_HTU21DF htu = Adafruit_HTU21DF();



//const char ordre_allumer_pompe[] = "allumer_pompe";
//const char ordre_eteindre_pompe[] = "eteindre_pompe";

//char string_allumage_pompe[] = "pompe_allumee";
//char string_extinction_pompe[] = "pompe_eteinte";

const char ordre_donner_temperature[] = "donner_temperature";
const char ordre_donner_humidite_air[] = "donner_humidite_air";
const char ordre_donner_humidite_sol[] = "donner_humidite_sol";
const char ordre_donner_luminosite[] = "donner_luminosite";

const char string_verification_connexion[] = "connexion_gimel";
const char string_message_recu[] = "message_recu";
const char string_succes_connexion[] = "connexion_gimel_ok";

int octet_lu = 0;
void setup() {
  Serial.begin(9600);
  vw_setup(1000);
  vw_set_tx_pin(tranceiverPin);
  vw_set_rx_pin(receiverPin);
  vw_rx_start();

  
  Serial.println("HTU21D-F test");
  if (!htu.begin()) {
    Serial.println("Couldn't find sensor!");
    while (1);
  }
  Serial.println("test fini");
}


void loop() {
  unsigned long curMillis = millis();          // Get current time
  //initialisation pour la réception
  
  uint8_t buf[VW_MAX_MESSAGE_LEN]; // Tableau qui va contenir le message recu (de taille maximum VW_MAX_MESSAGE_LEN)
  uint8_t buflen = VW_MAX_MESSAGE_LEN; // Taille maximum du buffer

  //message par defaut
  //char msg_received[];
  //Partie réception
  if(Serial.available() > 0)
    {
      octet_lu = Serial.read();
      if(octet_lu == 116 ) //116 <=> t
      {
        
        Serial.println(octet_lu);
        temperature = htu.readTemperature();
        Serial.println(temperature);
        humidite_air = htu.readHumidity();
        Serial.println(humidite_air);
  
        int luminosity = analogRead(photometrePin);
        Serial.println(luminosity);
  
        hygrometrie_sol = analogRead(hygrometreSolPin);
        Serial.print("hygrometrie du sol = " );    // impression du titre
        Serial.println(hygrometrie_sol);
      }
    }
  if (vw_have_message()) // Si on a un message dans le buffer
    {
        if (vw_get_message(buf, &buflen)) // Alors on récupère ce message qu'il soit entier ou pas
        {
          char msg_received[buflen];          
          //Serial.print("RX : ");
          
          for (int i = 0; i < buflen; i++) // On affiche tout ce que l'on a
              {
                Serial.print(char(buf[i]));
                msg_received[i] = char(buf[i]);
              }
          Serial.println("");
          msg_received[buflen] = '\0';
         
         Serial.println(msg_received);
   
   
   
        //Partie émission
       if (strcmp(msg_received, ordre_donner_temperature) == 0)
       {
          temperature = htu.readTemperature();

          
          char string_temperature[10];
          Serial.print(temperature);
          getFloatToCharArray(temperature, string_temperature, prefix_temperature);
          Serial.print(" Temperature here : ");
          Serial.println(string_temperature);
          //vw_send((uint8_t *)announce_temperature, strlen(announce_temperature)); // On envoie le message 
          //vw_wait_tx();
          vw_send((uint8_t *)string_temperature,strlen(string_temperature)); // On envoie le message 
          vw_wait_tx();
         }
        else if(strcmp(msg_received,ordre_donner_humidite_air) == 0)
        {
          humidite_air = htu.readHumidity();

          
          char string_air_humidity[10];
          Serial.println(humidite_air);
          getFloatToCharArray(humidite_air, string_air_humidity, prefix_humidite_air);
          //Serial.print(" Humidity here : ");
          //Serial.println(string_air_humidity);
          vw_send((uint8_t *)string_air_humidity, strlen(string_air_humidity));
          vw_wait_tx();
        }

        else if(strcmp(msg_received, ordre_donner_luminosite) == 0)
        {

          int luminosity = analogRead(photometrePin);
          Serial.println(luminosity);
          
          char string_luminosity[10];
          getFloatToCharArray(luminosity, string_luminosity, prefix_luminosity);
          Serial.print(" Luminosity here : ");
          Serial.println(string_luminosity);
          vw_send((uint8_t *)string_luminosity, strlen(string_luminosity));
          vw_wait_tx();
        }

        else if(strcmp(msg_received,ordre_donner_humidite_sol) == 0)
        {
          hygrometrie_sol = analogRead(hygrometreSolPin);
          Serial.print("hygrometrie du sol = " );    // impression du titre
          Serial.println(hygrometrie_sol);    // impression de la valeur mesurée

          
          char string_soil_humidity[10];
          getIntToCharArray(hygrometrie_sol, string_soil_humidity, prefix_hygrometrie_sol);
          //Serial.print(" Soil Humidity here : ");
          //Serial.println(string_soil_humidity);
          vw_send((uint8_t *)string_soil_humidity, strlen(string_soil_humidity));
          vw_wait_tx();
        }
        /*
        else if(strcmp(msg_received,ordre_allumer_pompe) == 0)
        {
          vw_send((uint8_t *)ordre_allumer_pompe, strlen(ordre_allumer_pompe));
          vw_wait_tx();
        }
    
        else if(strcmp(msg_received,ordre_eteindre_pompe) == 0)
        {
          vw_send((uint8_t *)ordre_eteindre_pompe, strlen(ordre_eteindre_pompe));
          vw_wait_tx();
        }
        else if(strcmp(msg_received,string_allumage_pompe) == 0)
        {
          vw_send((uint8_t *)string_allumage_pompe, strlen(string_allumage_pompe));
          vw_wait_tx();
        }
        else if(strcmp(msg_received,string_extinction_pompe) == 0)
        {
          vw_send((uint8_t *)string_extinction_pompe, strlen(string_extinction_pompe));
          vw_wait_tx();
        }
        */
        else if(strcmp(msg_received,string_verification_connexion) == 0)
        {
          Serial.println(string_message_recu);
          vw_send((uint8_t *)string_succes_connexion, strlen(string_succes_connexion));
          vw_wait_tx();
        }
      }
    }
}
void getIntToCharArray(int value, char* result, String prefix)
{
  getStringToCharArray(getIntToString(value, prefix), result);
}
void getFloatToCharArray(float value, char* result, String prefix)
{
  getStringToCharArray(getFloatToString(value, prefix), result);
}
void getStringToCharArray(String value, char * result)
{
  //char result[value.length()+1];
  value.toCharArray(result, value.length()+1);
}

String getFloatToString(float value, String prefix)
 {
  String result = "";
  result += prefix;
  result +=String(int(value))+"."+String(getDecimal(value));
  return result;
 }

 String getIntToString(int value, String prefix)
 {
  String result = "";
  result += prefix;
  result += String(int(value));
  return result;
 }
int getDecimal(float val)
{
  int intPart = int(val);
  int decPart = 1000*(val - intPart);
   if(decPart > 0) return decPart;
   else if (decPart < 0) return (-1)*decPart;
   else if (decPart = 0) return 00;
}

String addPrefix(String prefix, String measure)
{
  return prefix+measure;
}


