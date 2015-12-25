# -*-coding:utf-8-*-
import argparse
from oauth2client.tools import argparser
from Gmail import Gmail

if __name__ == '__main__':
    parser = argparse.ArgumentParser(parents=[argparser])
    flags = parser.parse_args()
    json_file =  "client_secret.json"
    sender =  "arrosage.b@gmail.com"
    to = "clemsciences@gmail.com"
    message = "c'est un test"
    subject =  "essai"
    filename = "message_test.txt"

    gmail = Gmail(flags, client_secret_file =json_file, oauth_scope = 'https://www.googleapis.com/auth/gmail.readonly')

    #gmail = Gmail(flags, oauth_scope = 'https://www.googleapis.com/auth/gmail.readonly')
    messages = gmail.getMessagesList()

    if messages['messages']:
        for msg in messages['messages']:
            #print msg
            print 'Msg id = {}'.format(msg['id'])
            m = gmail.getMessageDetails(msg['id'])
            #print m.data

            print 'From : {}'.format(m.getFrom())
            print 'To : {}'.format(m.getTo())
            print 'Subject : {}'.format(m.getSubject())
            #print 'Filename : {}'.format(m.getAttachment(gmail.gmail_service, to, msg['id']))
            print 'Text : {}'.format(m.getText(gmail.gmail_service, to, msg['id']))

    print 'Mails lus : {}'.format(len(messages['messages']))