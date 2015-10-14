//emetteur_recepteur_pompe
#include <VirtualWire.h> 


const uint8_t tranceiverPin = 6;
const uint8_t receiverPin = 4;
const uint8_t pompePin = 8;


const char ordre_allumer_pompe[] = "allumer_pompe";
const char ordre_eteindre_pompe[] = "eteindre_pompe";
const uint32_t ENTRE_ARROSAGE = 3600000UL;
const uint32_t DUREE_MAXIMALE_ARROSAGE = 1200000UL;
int debut_arrosage = 0;
int pompe_allumee = 0;

void setup() {
    //Initialisation de la série pour le debug
    Serial.begin(9600); // Initialisation du port série pour avoir un retour sur le serial monitor
    
    //Initialisation de la communication radio
    vw_setup(1000);  // Initialisation de la librairie VirtualWire à 1000 bauds  (pas plus car ça réduit trop la portée sinon)
    vw_set_rx_pin(receiverPin);   // On indique que l'on veut utiliser la broche receiverPin pour recevoir
    vw_set_tx_pin(tranceiverPin);     // On indique que l'on veut utiliser la pin transceiverPin de l'Arduino pour émettre
    vw_rx_start();      // Activation de la partie réception de la librairie VirtualWire

    //Initialisation du relai sans accrochage

    pinMode(pompePin, OUTPUT);
    
}

void loop() { 
     
    unsigned long curMillis = millis();
    
    //partie réception
    uint8_t buf[VW_MAX_MESSAGE_LEN]; // Tableau qui va contenir le message recu (de taille maximum VW_MAX_MESSAGE_LEN)
    uint8_t buflen = VW_MAX_MESSAGE_LEN; // Taille maximum du buffer
    
    //message par defaut
    char msg_received[] = "rien";
    
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
          msg_received[buflen] = '\0';
        }
    }
    
    
    //partie emission
    if (strcmp(msg_received, ordre_allumer_pompe)== 0 && curMillis - debut_arrosage > ENTRE_ARROSAGE )
          {
              //On allume effectivement la pompe
              digitalWrite(pompePin, HIGH);
              //On informe que l'on a allume la pompe
              char string_allumage_pompe[] = "pompe_allumee";              
              Serial.println(string_allumage_pompe);
              vw_send((uint8_t *)string_allumage_pompe,strlen(string_allumage_pompe)); // On envoie le message 
              vw_wait_tx();
              debut_arrosage = millis();
              //msg_received = '\0';
              pompe_allumee = 1;
          }
     else if(strcmp(msg_received, ordre_eteindre_pompe) == 0 || curMillis - debut_arrosage > DUREE_MAXIMALE_ARROSAGE)
          {
              //On eteint effectivement la pompe
              digitalWrite(pompePin, LOW);
              //On informe que l'on a eteint la pompe
              char string_extinction_pompe[] = "pompe_eteinte";
              Serial.println(string_extinction_pompe);
              vw_send((uint8_t *)string_extinction_pompe,strlen(string_extinction_pompe)); // On envoie le message 
              vw_wait_tx();
              //msg_received = '\0';
              pompe_allumee = 0;
          }
 }
 
