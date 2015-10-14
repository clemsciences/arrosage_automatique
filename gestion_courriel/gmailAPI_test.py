import argparse
from oauth2client.tools import argparser
from Gmail import Gmail

if __name__ == '__main__':
    parser = argparse.ArgumentParser(parents=[argparser])
    flags = parser.parse_args()

    gmail = Gmail(flags, oauth_scopes = 'https://www.googleapis.com/auth/gmail.modify')
    messages = gmail.getMessagesList()

    if messages['messages']:
        for msg in messages['messages']:
            print 'Msg id = {}'.format(msg['id'])
            m = gmail.getMessageDetailq(msg['id'])
            print 'From : {}'.format(m.getFrom())
            print 'To : {}'.format(m.getTo())
            print 'Subject : {}'.format(m.getSubject())

    print 'Mails lus : {}'.format(len(messages['messages']))