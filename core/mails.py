import win32com.client as win32
from datetime import datetime
import pythoncom



def enviar_mail(lista_mails,asunto,mensaje):
    pythoncom.CoInitialize()
    Outlook = win32.Dispatch('Outlook.application')
    mail = Outlook.CreateItem(0)
    mailTo=";".join(lista_mails)
    mail.To = mailTo
    mail.Subject = asunto
    mail.Body = mensaje
    mail.Send()

def enviar_mail_notificacion(lista_mails,n_notif,tit_notif):
	hoy = datetime.today().strftime('%d-%m-%Y')
	asunto = f"Nueva notificación departamental (n° {n_notif} | {hoy})"
	mensaje = f"N° notif: {n_notif}\nTítulo:{tit_notif}\nPara ver la notificación completa visitar el sig. link: http://10.6.10.157:8000/notificaciones/update/{n_notif}/"
	enviar_mail(lista_mails,asunto,mensaje)