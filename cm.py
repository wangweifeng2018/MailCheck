#!user/bin python
#coding: utf-8
import imaplib,getpass,struct,datetime
import email,os,sys,re
from email.header import Header
reload(sys)
sys.setdefaultencoding('utf-8')

def Make_date_dir(work_path):
    """
    make a new dir，20170815
    if 20170815 is exist then,20170815_2
    """
    date_dir = "" 
    date = datetime.date.today()
    for i in str(date).split('-'):
        date_dir += i
    if not os.path.exists(work_path+date_dir):
        to_make_dir = work_path+date_dir
        os.mkdir(to_make_dir)
    else:
        num = 1
        for f in os.listdir(work_path):
            if f.startswith(date_dir):
                num = num +1
        to_make_dir = work_path+date_dir+"_"+str(num)
        os.mkdir(to_make_dir)
    return to_make_dir


def Main(host,port,user,passwd,work_path):
    
    ## Login on your email account,print login info and date time.
    m = imaplib.IMAP4_SSL(port=port,host=host)
    m.login(user,passwd)

    print (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print ("Login on successfully!")

    # select inbox unseen emails as the target emails
    m.select('INBOX',readonly=False)
    email_num,unseen_data = m.search(None,'UnSeen')
    unseen_list = unseen_data[0].decode("utf-8").split(' ')
    
    count = 0
    all_dir = []
    for num in unseen_list:
        count += 1
        try:
            # Trying to fetch the email. 
            typ,data = m.fetch(num, 'RFC822') 
        except:
            print ("No unseen emails!")
            print ("Login out  now.")
            m.close()
            m.logout()
            exit()
        print ("Unread email No. ",num)
        
        # Parsing using email lib.
        msg = email.message_from_string(data[0][1].decode()) 
        #m.store(num,'+FLAGS','\\Seen')# store this email as seen.
        
        #Get the subject.
        #subject = msg.get('subject') 
        sub_object = email.header.decode_header(msg['subject'])[0]
        charset,sub = sub_object[1],sub_object[0]

        if charset != None:
            print "Subject:",sub.decode(charset)
              
        # Get message body 
        attach = {}
        for part in msg.walk():
            if part.is_multipart():
                continue
            contentType = part.get_content_type()
            mycode = part.get_content_charset()

            if contentType == 'text/plain':
                content = part.get_payload(decode=True)
                print "Message:\n",content.decode(charset)    
            
            #Get attachment
            if part.get('Content-Disposition') != None:
                filename = part.get_filename()
                attach_name = email.Header.decode_header(filename)[0][0]
                attach_data = part.get_payload(decode=True)
                attach[attach_name] = attach_data
 
        #rewrite attachment
        date_dir = Make_date_dir(work_path+'/')
        for name,data in attach.items():
            att_file = os.path.join(date_dir+'/',name)
            if not os.path.isfile(att_file):
                with open(att_file,'wb') as fp:
                    fp.write(data)
            
                os.path.join(date_dir+'/',name)   
                if not os.path.isfile(att_file): 
                    with open(att_path,'wb') as fp:
                            fp.write(da) 
    m.logout()
    print ("Email count:",count)
    return 


if __name__ == '__main__':
    
    
    # server and host depend your email accounts type
    # yours may be different
    host = 'imap.exmail.qq.com'
    port = '993'
    user = input("Email:")
    passwd = getpass.getpass()
    work_path = input("Enter your work dir:")

    Main(host,port,user,passwd,work_path)
