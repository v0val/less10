from xmlrpc.client import MAXINT
import telebot

TOKEN = ""

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])

#def send_welcome(message):
#	bot.reply_to(message, ".")

#def send_welcome(message):
#	bot.send_message(message.chat.id, "")

@bot.message_handler(content_types=['text'])
def summi_poly(message):
        stri = message.text
        poly1, poly2 = stri.split()
        def degree(poly):
            a = []
            for i in range(len(poly)):
                if poly[i] == 'x':
                    if i == len(poly) - 1 or poly[i + 1] != '^':
                        a.append(1)
                    else:
                        a.append(int(poly[i + 2]))
            return a
        def coefficient(poly):
            coeff = []
            n = poly.find('x')
            sign = 1
            if poly[0] == '-': sign = -1
            par = ''
            if n == 1: par = '1'
            if n != 0:
                coeff.append(int(poly[:n - 1]+par))
            else:
                coeff.append(1)
            if poly[0] == '-' and  poly[1] == 'x':
                coeff *= -1 
            
            N = len(poly)

            for i in range(N-1):
                if poly[i] == '+' or poly[i] == '-':
                    n = poly.find('x', i, N )
                    if i + 1 == n:
                        coeff.append(int(poly[i]+ '1'))
                    else:
                        if n != -1: coeff.append(int(poly[i:n - 1]))
            if poly[N - 1] != 'x':        
                t = max(poly.rfind('+'), poly.rfind('-'))
                coeff.append(int(poly[t:N]))
            return coeff

        maxi1 = degree(poly1)
        maxi2 = degree(poly2)
        max_degree = max(max(maxi1), max(maxi2))
        mas_coeff1= coefficient(poly1)
        mas_coeff2= coefficient(poly2)
        mas_degree1 = [0]*(max_degree + 1)
        mas_degree2 = [0]*(max_degree + 1)
        maxi1 = maxi1[::-1]
        maxi2 = maxi2[::-1]
        mas_coeff1 = mas_coeff1[::-1]
        mas_coeff2 = mas_coeff2[::-1]

        if len(maxi1) == len(mas_coeff1):
            nach1 = 0
        else:
            nach1 = 1
            mas_degree1[0] = mas_coeff1[0]

        if len(maxi2) == len(mas_coeff2):
            nach2 = 0
        else:
            nach2 = 1
            mas_degree2[0] = mas_coeff2[0]    

        k = 0
        for i in range(max_degree+1):
            if i == maxi1[k]:
                mas_degree1[i] = maxi1[k]
                if len(maxi1) - 1 != k:
                    k += 1

        t = 0
        for i in range(max_degree+1):
            if i == maxi2[t]:
                mas_degree2[i] = maxi2[t]
                if len(maxi2) - 1 != t:
                    t += 1


        k = nach1
        for i in range(nach1, len(mas_degree1)):
            if mas_degree1[i] > 0:
                mas_degree1[i] = mas_coeff1[k]
                k += 1
                
        t = nach2
        for i in range(nach2, len(mas_degree2)):
            if mas_degree2[i] > 0:
                mas_degree2[i] = mas_coeff2[t]
                t += 1

        mas_degree2 = [mas_degree1[i]+ mas_degree2[i] for i in range(max_degree + 1)]



        N = len(mas_degree2)
        for i in range(N):
            if mas_degree2[i] > 0:
                mas_degree2[i] = '+' + str(mas_degree2[i])
            else: mas_degree2[i] = str(mas_degree2[i])

        sum_poly = ''
        for i in range(max_degree,-1,-1): 
            if mas_degree2[i] != '0':
                if mas_degree2[i] != '1':            
                    if i == 1 and i != 0:
                        sum_poly = sum_poly  + mas_degree2[i] + 'x'
                    else:
                        if i == 0:
                            sum_poly = sum_poly + mas_degree2[i]
                        else:
                            sum_poly = sum_poly + mas_degree2[i] + '*x^' + str(i)
                else:
                    if i == 1 and i != 0:
                        sum_poly = sum_poly + '+x'
                    else:
                        if i == 0:
                            sum_poly = sum_poly + mas_degree2[i]
                        else:
                            sum_poly = sum_poly + '+x^' + str(i)

        if len(sum_poly) != 0:
            if sum_poly[0] == '+': sum_poly = sum_poly[1:]
            if sum_poly[0] == '1': sum_poly = sum_poly[2:]
            if sum_poly[0] == '-' and sum_poly[1] == '1': sum_poly = '-'+sum_poly[3:]
            bot.send_message(message.chat.id, 'cумма многочленов '+f'{sum_poly}' )
        else:
            bot.send_message(message.chat.id, 'cумма многочленов '+f'{len(sum_poly)}' )
    

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text + ', дружище')

bot.infinity_polling()
# 2*x^2+3=0 4*x^2-1=0
