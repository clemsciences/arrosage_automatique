
#include <VirtualWire.h> // On inclut la librairie VirtualWire

// Connect Vin to 3-5VDC
// Connect GND to ground
// Connect SCL to I2C clock pin (A5 on UNO)
// Connect SDA to I2C data pin (A4 on UNO)

const uint8_t tranceiverPin = 4;
const uint8_t receiverPin = 6;
const uint8_t pompePin = 2;
const int hygrometreSolPin = 3;

const uint32_t TRHSTEP   = 10000UL; // période de mesure

int hygrometrie_sol;


const char ordre_donner_humidite_sol[] = "donner_humidite_sol";
const char ordre_allumer_pompe[] = "allumer_pompe";
const char ordre_eteindre_pompe[] = "eteindre_pompe";

char string_allumage_pompe[] = "PA_";
char string_extinction_pompe[] = "PE_";
String prefix_hygrometrie_sol = "HS_";

const char string_verification_connexion[] = "connexion_bet";
const char string_message_recu[] = "message_recu";
const char string_succes_connexion[] = "connexion_bet_ok";
int octet_lu = 0;

void setup() {

  pinMode(pompePin, OUTPUT);
  Serial.begin(9600);
  vw_setup(1000);
  vw_set_tx_pin(tranceiverPin);
  vw_set_rx_pin(receiverPin);
  vw_rx_start();
  
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
       if (strcmp(msg_received, ordre_allumer_pompe) == 0)
       {
          digitalWrite(pompePin, HIGH);
          Serial.println(string_allumage_pompe);
          vw_send((uint8_t *)string_allumage_pompe,strlen(string_allumage_pompe)); // On envoie le message 
          vw_wait_tx();
         }
        else if(strcmp(msg_received,ordre_eteindre_pompe) == 0)
        {
          digitalWrite(pompePin, LOW);
          Serial.print(string_extinction_pompe);
          vw_send((uint8_t *)string_extinction_pompe, strlen(string_extinction_pompe));
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


