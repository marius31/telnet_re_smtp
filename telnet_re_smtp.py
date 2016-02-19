# Proiect telnet
# Aplica telnetlib, ntplib, re, smtplib, functii si clase
# Gheorghe Marius - 10/23/15

import telnetlib,re, ntplib,time,smtplib

ntp_server="2.ro.pool.ntp.org"
ntp_vers=2 
ntp_port=123
ntp_timeout=5

text_cautat='Known via "bgp \d{1,5}"'

host_telnet="route-views.routeviews.org"
debug_level_telnet=1
user_telnet="rviews"
pass_telnet="rviews"
comanda_telnet="show ip route 192.0.2.1"

server_email ='smtp.gmail.com:587'
user_logare_email='mail.through.python'
pass_logare_email="infoacad"
email_trimitere='mail.through.python@gmail.com'
email_receptie='popescu.catalin.ionut@gmail.com'


def sesiuneTelnet(host,debug_level_telnet,user,parola,comanda):
  """Creaza un obiect telnet si aplica o comanda"""
  obiect_telnet = telnetlib.Telnet(host)
  obiect_telnet.set_debuglevel(debug_level_telnet)
  obiect_telnet.read_until("login: " , 5)
  obiect_telnet.write(user + "\r\n")
  obiect_telnet.read_until("password: " ,5)
  obiect_telnet.write(parola + "\r\n")
  obiect_telnet.read_until(">",10)

  if (debug_level_telnet!=0):
    print obiect_telnet.read_until(">",10)

  obiect_telnet.write(comanda+ "\r\n")
  captura = obiect_telnet.read_until("###",10)

  if (debug_level_telnet!=0):
    print captura

  obiect_telnet.write("exit" + "\r\n")
  obiect_telnet.close()
  return captura


def timpIncident(serverNtp):
  """cream un obiect ntplib de tip client"""
  obj_ntp = ntplib.NTPClient()
  try:
    timp = obj_ntp.request(serverNtp, ntp_vers , ntp_port, ntp_timeout)
  except:
    timp="Eroare: timpul nu a putut fi extras cel mai probabil din cauza unei probleme de retea!"
  else:
    timp=time.ctime(timp.tx_time)
  return timp



def mesajEmail(vecin, timp_incident):
  """formateaza un mesaj pentru a fi transmis prin email"""
  mesaj = """From: Persona care Origineaza e-mail <mail.through.python@gmail.com>
To: marius <marius.gheorghe22@yahoo.com>
Subject: Routerul are o ruta catre 192.0.2.1 prin '"""+ vecin +"""'

Timpul la care incidentul a aparut este  """+ timp_incident +"""
Acest timp este extras dintr-un server ntp cu o intarziere maxima de 5 secunde"""
  return mesaj

def trimiteMesaj(snmp_server,username,parola,originator_email, destinatari, mesaj):
  """Trimite mesajul"""
  try:
     smtpObj = smtplib.SMTP(snmp_server)
     smtpObj.starttls()
     smtpObj.login(username,parola)
     smtpObj.sendmail(originator_email, destinatari, mesaj)         
     print "Mesajul electronic a fost trimis cu succes"
  except(),e:
     print 3
     print "Mesajul electronic nu a fost trimis cu succes"
     print e
  else:
      smtpObj.quit()

def Cauta(textCautat,Sir_in_care_Caut):
  test_cap=re.search(text_cautat ,output_telnet)
  if test_cap:
    return test_cap.group(0)
  else:
    return False

output_telnet=sesiuneTelnet(host_telnet,debug_level_telnet,
                            user_telnet,pass_telnet,comanda_telnet)


#print output_telnet

test_cap=Cauta(text_cautat,output_telnet)
if test_cap:
  timp=timpIncident(ntp_server)
  mesaj = mesajEmail(test_cap,timp)
  trimiteMesaj(server_email,user_logare_email,pass_logare_email,
               email_trimitere,[email_receptie],mesaj)
else:
  print "textul cautat: "+ text_cautat+" nu a fost gasit in sirul de caractere:\n"+output_telnet

raw_input("Apasa enter sa iesi")




