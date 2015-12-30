# -*-coding:utf-8-*-
import httplib2
from generer_xml import *
import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apiclient import discovery, errors
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow, argparser
import mimetypes, os, argparse

class Gmail:
    """
    Code pour se connecter à l'API Gmail
    """

    def __init__(self, flags, client_secret_file='client_secret.json', oauth_scope='https://www.googleapis.com/auth/gmail.send', storage_file='gmail.storage'):
        self.__client_secret_file = client_secret_file
        self.__oauth_scope = oauth_scope
        self.__storage = Storage(storage_file)
        self.__connect(flags)
        #self.gmail_service = None
    def __connect(self, flags):
        flow = flow_from_clientsecrets(self.__client_secret_file, scope=self.__oauth_scope)
        http = httplib2.Http()
        credentials = self.__storage.get()
        #print credentials
        if credentials is None or credentials.invalid:
            credentials = run_flow(flow, self.__storage, flags, http=http)
        http = credentials.authorize(http)
        self.gmail_service = discovery.build('gmail', 'v1', http=http)
    def getMessagesList(self, userId='me', query=None):
        return self.gmail_service.users().messages().list(userId=userId, q=query).execute()
    def getMessageDetails(self, msgId, userId='me'):
        return GmailMessage(self.gmail_service.users().messages().get(userId=userId, id=msgId).execute())
    def markAsRead(self, msgId, userId='me'):
        self.gmail_service.users().messages().modify(userId=userId, id=msgId, body={'removeLabelIds':['UNREAD'], 'addLabelIds':[]}).execute()


class GmailMessage:
    """
    Code pour extraire ce dont on a besoin dans un courriel
    """
    def __init__(self, data):
        self.__data = {k : v for k, v in zip(map(lambda m : m['name'], data['payload']['headers']), map(lambda m : m['value'], data['payload']['headers']))}
        self.__data['labels'] = data['labelIds']
        self.__data['snippet'] = data['snippet']
        self.data = self.__data
        if data['payload'].has_key('parts'):
            don = [ el for el in data['payload']['parts'] if el.has_key('name')]

            #print data['payload']['parts']
            self.d_attachment = {k : v for k, v in zip(map(lambda m : m['name'], don), map(lambda m : m['value'], don))}
            #print self.d_attachment
    def getSnippet(self):
        """
        Extraire le texte du courriel
        :return:
        """
        return self.__data['snippet'].encode('utf-8')
    def isUnread(self):
        """
        Voir si le courriel est non lu
        :return:
        """
        return 'UNREAD' in self.__data['labels']
    def getSubject(self):
        """
        voir l'objet du courriel
        :return:
        """
        if self.__data.has_key('Subject'):
            return self.__data['Subject'].encode('utf-8')
        elif self.__data.has_key('subject'):
            return self.__data['subject'].encode('utf-8')
        else:
            return None
    def getFrom(self):
        """
        Voir qui envoie le courriel
        :return:
        """
        if self.__data.has_key('From'):
            return self.__data['From'].encode('utf-8')
        elif self.__data.has_key('from'):
            return self.__data['from'].encode('utf-8')
        else:
            return None
    def getTo(self):
        """
        Voir à qui le courriel est destiné, normalement il n'y a que moi dans le projet d'arrosage !
        :return:
        """
        if self.__data.has_key('To'):
            return self.__data['To'].encode('utf-8')
        elif self.__data.has_key('to'):
            return self.__data['to'].encode('utf-8')
        else:
            return None
    def getText(self, service, user_id, msg_id):
        """
        Obtenir le texte d'un courriel en précisant le service gmail, l'adresse courriel de l'utilisateur et l'id
        du message
        :param service:
        :param user_id:
        :param msg_id:
        :return:
        """
        message = service.users().messages().get(userId=user_id, id = msg_id).execute()
        return message['snippet'].encode('utf-8')
    def getAttachment(self, service, user_id, msg_id):
        """
        Obtenir et enregistrer dans le repertoire courant la pièce-jointe
        :param service:
        :param user_id:
        :param msg_id:
        :return:
        """
        #TODO à voir ce qu'on peut en faire
        message = service.users().messages().get(userId=user_id, id = msg_id).execute()
        #print "raw", message['raw']
        print "snippet", message['snippet']
        for part in message['payload']['parts']:
            if part['filename']:
            #if self.d_attachment.has_key('filename'):
                print part['body']
                try:
                    file_data = base64.urlsafe_b64decode(part['body']['data'].encode('UTF-8'))
                except:
                    file_data = "rien"
                path = os.path.join(os.getcwd()+"tests", "test")
                f = open(path, 'w')
                f.write(file_data)
                f.close()
                return "fichier enregistré"
            """
            elif self.d_attachment.has_key('Filename'):
                file_data = base64.urlsafe_b64decode(self.d_attachment['body']['data'].encode('UTF-8'))
                path = ''.join([os.getcwd(), self.d_attachment['Filename']])
                f = open(path, 'w')
                f.write(file_data)
                f.close()
                print "fichier enregistré"
            else:
                return None
            """



class Message:
    def __init__(self, sender, to, subject, message_text, service):
        self.message = MIMEMultipart()
        self.message['to'] = to
        self.message['from'] = sender
        self.message['subject'] = subject
        self.message.attach(MIMEText(message_text))

    def sendMessage(self, service, user_id ):
        """Send an email message.
        Args:
            service: Authorized Gmail API service instance.
            user_id: User's email address. The special value "me"
            can be used to indicate the authenticated user.
            message: Message to be sent.

        Returns:
          Sent Message.
        """
        message = {'raw': base64.urlsafe_b64encode(self.message.as_string())}
        try:
            message = (service.users().messages().send(userId=user_id, body=message)
                     .execute())
            print 'Message Id: %s' % message['id']
            #return message
        except errors.HttpError, error:
            print 'An error occurred: %s' % error


class Message_Attachment(Message):
    def __init__(self, sender, to, subject, message_text, file_dir, filename, service):
        Message.__init__(self, sender, to, subject, message_text, service)
        path = os.path.join(file_dir, filename)
        content_type, encoding = mimetypes.guess_type(path)
        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)
        if main_type == 'text':
            fp = open(path, 'rb')
            msg = MIMEText(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'image':
            fp = open(path, 'rb')
            msg = MIMEImage(fp.read(), _subtype=sub_type)
            fp.close()
        else:
            fp = open(path, 'rb')
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(fp.read())
            fp.close()
        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        self.message.attach(msg)



if __name__ == "__main__":
    #script d'envoi d'un message
    parser = argparse.ArgumentParser(parents=[argparser])
    flags = parser.parse_args()
    json_file = "client_arrosage.json"
    sender = "arrosage.b@gmail.com"
    to = "clemsciences@gmail.com"
    message = "c'est un test"
    subject = "essai"
    filename = "message_test.txt"



    questions = generer_question(str(datetime.today()), "temperature")
    questions = generer_question(str(datetime.today()), "humidite", questions)
    questions = generer_question(str(datetime.today()), "parametres", questions)
    questions = generer_question(str(datetime.today()), "pression", questions)
    a = ElementTree.tostring(questions)


    gmail = Gmail(flags, client_secret_file=json_file, oauth_scope='https://www.googleapis.com/auth/gmail.send')
    #message = Message_Attachment(sender=sender,to=to,subject=subject,message_text= a, file_dir=os.getcwd(), filename= str(datetime.today()), service=gmail.gmail_service)
    message = Message(sender=sender, to=to, subject=subject, message_text=a, service=gmail.gmail_service)

    #obtenir tous les messages reçus
    messages = gmail.getMessagesList()
    message.sendMessage(gmail.gmail_service, sender)
