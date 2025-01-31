from tkinter import *
import sqlite3
from datetime import date
from tkinter import messagebox
from datetime import *
import re

def clearFrame():
    # destroy all widgets from frame
    for widget in root.winfo_children():
       widget.destroy()

#Insert on SQL table
def SubmitEval(iden,rating_options,comments):

    resid = iden.get()
    rate = rating_options.get()
    comment = comments.get("1.0",END)
    
    conn = sqlite3.connect('car-rental-python-database.db')
    c= conn.cursor()

    #fetch reservation id
    qry = """SELECT reservation_id 
         FROM reservation 
         WHERE reservation_id = ?;"""
    x=c.execute(qry,(resid,))
    q=x.fetchall()
    conn.commit()

    #Prompr user to enter valid reservation id
    if len(q)==0:
        messagebox.showinfo(title='Invalid credentials', message='Enter valid reservation id')
        Evaluation()
        
    else:
        #Inser to table 'evaluation'
        insert = """INSERT 
        INTO evaluation (r_id,rating,comments)
        VALUES(?,?,?);"""
                                                               
        c.execute(insert,(resid,rate,comment))

        conn.commit()
        conn.close()

        messagebox.showinfo(title='Evaluation submitted', message='Thanks for helping us improve!')
        mainmenu()
        
#Rate us and leave a comment functionality
def Evaluation():
    clearFrame()  
    #set window color & appearance    
    root.configure(bg = "#384d66")
    root.title('Car Rental App-Please rate us!')

    #reservation id
    reservationlabel=Label(root,text='Reservation Id:',font=("Arial",10,"bold"),fg="white",bg="#384d66").place(relx=0.3,rely=0.25,anchor=CENTER)
    iden=Entry(root,width=50)
    iden.place(relx=0.5,rely=0.25,anchor=CENTER)

    ratinglabel=Label(root, text='Choose rating:',font=("Arial",10,"bold"),fg="white",bg="#384d66").place(relx=0.3,rely=0.35,anchor=CENTER)

    #rating drop down menu
    rating_options = StringVar(root)
    rating_options.set("1")    
    w = OptionMenu(root, rating_options, "1", "2", "3","4","5")
    w.place(relx=0.38,rely=0.35,anchor=CENTER)

    #Comments form
    commentslabel=Label(root, text='Comments:',font=("Arial",10,"bold"),fg="white",bg="#384d66").place(relx=0.3,rely=0.45,anchor=CENTER)
    comments = Text(root,width=70,height=10,font=('Arial',10))
    comments.place(relx=0.58,rely=0.55,anchor=CENTER)

    proceed=Button(root,text="Submit",font=('Arial',10,"bold"),padx=50,pady=10,fg="white",bg="#848f9e",activebackground="#575917",command=lambda: SubmitEval(iden,rating_options,comments))
    proceed.place(relx=0.99,rely=0.95,anchor=SE)

    back1=Button(root,text="Back",font=('Arial',10,"bold"),padx=50,pady=10,fg="white",bg="#848f9e",activebackground="#575917",command=mainmenu)
    back1.place(relx=0.01,rely=0.95,anchor=SW)

#Update SQL tables accordingly
def Return_Car(resid):

    #check for late days
    conn = sqlite3.connect('car-rental-python-database.db')
    c= conn.cursor()
    
    days_late = """ SELECT julianday('now')-julianday(return_date)
                        FROM reservation
                        WHERE reservation_id = ?;"""

    x=c.execute(days_late,(resid,))
    q=x.fetchall()

    #total cost is number of reserved days + days late (if any) * cost of category

    planned_cost = """SELECT total_cost,cost_per_day
                      FROM reservation JOIN category ON category.category_id=reservation.cat_id
                      WHERE reservation_id=?"""

    l=c.execute(planned_cost,(resid,))
    w=l.fetchall()

    standard_cost=int(w[0][0])
    cat_cost=int(w[0][1])
    days_late=int(q[0][0])

    if days_late>0:
        total_cost = standard_cost + cat_cost * days_late
    else:
        total_cost = standard_cost
    

    #update resevation cost on reservation
    update_cost = """UPDATE reservation
                SET total_cost=?
                WHERE reservation_id=?;"""
                                                            
    c.execute(update_cost,(total_cost,resid))
    conn.commit()

    #update return date on reservation
    update_return = """UPDATE reservation
                SET returned_date=date('now')
                WHERE reservation_id=?;"""
    c.execute(update_return,(resid,))

    #Update car location based on drop ff locationon 
    update_car_location="""UPDATE car
                           SET l_id=(select dol_id from reservation where reservation_id=?)
                           WHERE car_id=(select c_id from reservation where reservation_id=?)"""
    
    c.execute(update_car_location,(resid,resid))
    conn.commit()
    
    conn.close()
    print(q[0][0])
    if(q[0][0]>0):
        messagebox.showinfo(title='Reservation cancelled', message='Car returned {days} days late\nTotal cost (without damages) is: {cost}'.format(days=days_late,cost=total_cost))
        mainmenu()
    else:
        messagebox.showinfo(title='Reservation cancelled', message='Car returned without delay\nTotal cost (without damages) is: {cost}'.format(cost=total_cost))
        mainmenu()

#Show user's info and prompr correct message when they press "return car"
def Proceed_Return():

    mail = str(em.get())
    resid = res_id.get()

    conn = sqlite3.connect('car-rental-python-database.db')
    c= conn.cursor()
    
    qry = """SELECT reservation_id,email,returned_date,cancellation_date,julianday(date('now'))-julianday(pickup_date)
         FROM reservation join client on reservation.client_id = client.afm
         WHERE reservation_id = ? and email = ?;"""
    x=c.execute(qry,(resid,mail))
    q=x.fetchall()
    conn.commit()
    
    #Check for valid credentials
    if len(q)==0:
        messagebox.showinfo(title='Invalid credentials', message='Enter valid credentials')
    elif q[0][2]!=None:
        messagebox.showinfo(title='Invalid credentials', message='Car alrready returned')
    elif q[0][3]!=None:
        messagebox.showinfo(title='Invalid credentials', message='Reservation has been cancelled')
    elif int(q[0][4])<0:
        messagebox.showinfo(title='Invalid credentials', message='Car has not been picked up yet')    
    else:
        clearFrame()  
        #set window color & appearance    
        root.configure(bg = "#384d66")
        root.title('Car Rental App-Return car')

        #get reservation details and show them
        qry = """SELECT pickup_date,return_date,julianday(date('now'))-julianday(return_date)
        FROM reservation
        WHERE reservation_id = ?;"""
        x=c.execute(qry,(resid,))
        q=x.fetchall()
        
        pick_up_date = Label(root,text='Pick up date: {}'.format(q[0][0]),font=("Arial",15,"bold"),fg="white",bg="#384d66")
        supposed_return_date = Label(root,text='Drop off date: {}'.format(q[0][1]),font=("Arial",15,"bold"),fg="white",bg="#384d66")
        #Late return
        if int(q[0][2])>0:
            actual_return_date = Label(root,text='Days late: {}'.format(int(q[0][2])),font=("Arial",15,"bold"),fg="white",bg="#384d66")
        #On time return
        elif int(q[0][2])==0:
            actual_return_date = Label(root,text='Return on time',font=("Arial",15,"bold"),fg="white",bg="#384d66")
        #Early return
        if int(q[0][2])<0:
            actual_return_date = Label(root,text='Days early: {}'.format(int(-q[0][2])),font=("Arial",15,"bold"),fg="white",bg="#384d66")
        pick_up_date.place(relx=0.3,rely=0.3)
        supposed_return_date.place(relx=0.3,rely=0.35)
        actual_return_date.place(relx=0.3,rely=0.4)
        
        conn.commit()
        conn.close()
        proceed=Button(root,text="Return car",font=('Arial',10,"bold"),padx=50,pady=10,fg="white",bg="#848f9e",activebackground="#575917",command=lambda: Return_Car(resid))
        proceed.place(relx=0.99,rely=0.95,anchor=SE)
        
        back=Button(root,text="Back",font=('Arial',10,"bold"),padx=50,pady=10,fg="white",bg="#848f9e",activebackground="#575917",command=Cancelation)
        back.place(relx=0.01,rely=0.95,anchor=SW)
        
#Return car
def Return():
    global em
    global res_id
    
    clearFrame()  
    #set window color & appearance    
    root.configure(bg = "#384d66")
    root.title('Car Rental App-Return car')
    
    #enter email 
    maillabel=Label(root,text="Email:",font=("Arial",10,"bold"),fg="white",bg="#384d66")
    #maillabel.grid(row=0,column=0)
    em=Entry(root,width=50)
    #email.grid(row=0,column=1)
    em.place(relx=0.5,rely=0.3,anchor=CENTER)
    maillabel.place(relx=0.3,rely=0.3,anchor=CENTER)
    #enter reservation id
    idlabel=Label(root,text="Reservation ID:",font=("Arial",10,"bold"),fg="white",bg="#384d66")
    #idlabel.grid(row=1,column=0)
    idlabel.place(relx=0.3,rely=0.35,anchor=CENTER)
    res_id=Entry(root,width=50)
    res_id.place(relx=0.5,rely=0.35,anchor=CENTER)
    #back button
    back1=Button(root,text="Back",font=('Arial',10,"bold"),padx=50,pady=10,fg="white",bg="#848f9e",activebackground="#575917",command=mainmenu)
    back1.place(relx=0.01,rely=0.95,anchor=SW)
    #proceed button
    proceed=Button(root,text="Proceed",font=('Arial',10,"bold"),padx=50,pady=10,fg="white",bg="#848f9e",activebackground="#575917",command=Proceed_Return)
    proceed.place(relx=0.99,rely=0.95,anchor=SE)

#Cancel reservation and update SQL tables accordingly
def Cancel_Res(resid):

    #check for free cancelation period
    conn = sqlite3.connect('car-rental-python-database.db')
    c= conn.cursor()
    
    free_cancelation = """ SELECT julianday(free_can_period)-julianday("now")
                        FROM reservation
                        WHERE reservation_id = ?;"""

    x=c.execute(free_cancelation,(resid,))
    q=x.fetchall()

    #update cancelation date on reservation
    delete = """UPDATE reservation
                SET cancellation_date=date('now')
                WHERE reservation_id=?;"""
                                                            
    c.execute(delete,(resid,))

    conn.commit()
    
    #If cancelation take place during free cancelation period 100% of his money is returned.Else only 50%
    if(q[0][0]>0):
        messagebox.showinfo(title='Reservation cancelled', message='Successful cancellation (100% returned)')
        update_cost = """UPDATE reservation
                        SET total_cost=0
                        WHERE reservation_id=?;"""
                                                            
        c.execute(update_cost,(resid,))
        conn.commit()
    else:
        messagebox.showinfo(title='Reservation cancelled', message='Successful cancellation (50% returned)')
        update_cost = """UPDATE reservation
                        SET total_cost=0.5*total_cost
                        WHERE reservation_id=?;"""
                                                            
        c.execute(update_cost,(resid,))
        conn.commit()
        
    conn.close()
    
    mainmenu()
    
#proceed button function
def Proceed_Cancelation():
    mail = str(email.get())
    resid = iden.get()

    conn = sqlite3.connect('car-rental-python-database.db')
    c= conn.cursor()
    try:
        qry = """SELECT reservation_id,email,cancellation_date,returned_date,julianday(date('now'))-julianday(pickup_date)
             FROM reservation join client on reservation.client_id = client.afm
             WHERE reservation_id = ? and email = ?;"""
        x=c.execute(qry,(resid,mail))
        q=x.fetchall()
        conn.commit()
        print(q)
        
        
        if len(q)==0:
            messagebox.showinfo(title='Invalid credentials', message='Enter valid credentials')
        elif q[0][2]!=None:
            messagebox.showinfo(title='Invalid credentials', message='Reservation already canceled')
        elif q[0][3]!=None or int(q[0][4])>0:
            messagebox.showinfo(title='Invalid credentials', message='Too late to cancel this reservation')    
        else:
            clearFrame()  
            #set window color & appearance    
            root.configure(bg = "#384d66")
            root.title('Car Rental App-Cancel Your Reservation')

            #get reservation details and show them
            qry = """SELECT pickup_date,return_date,free_can_period 
            FROM reservation
            WHERE reservation_id = ?;"""
            x=c.execute(qry,(resid,))
            q=x.fetchall()
            
            pick_up_date = Label(root,text='Pick up date: {}'.format(q[0][0]),font=("Arial",15,"bold"),fg="white",bg="#384d66")
            return_date = Label(root,text='Return date: {}'.format(q[0][1]),font=("Arial",15,"bold"),fg="white",bg="#384d66")
            free_can_date = Label(root,text='Free cancelation date: {}'.format(q[0][2]),font=("Arial",15,"bold"),fg="white",bg="#384d66")
            pick_up_date.place(relx=0.3,rely=0.3)
            return_date.place(relx=0.3,rely=0.35)
            free_can_date.place(relx=0.3,rely=0.4)
            
            conn.commit()
            conn.close()
            proceed=Button(root,text="Cancel reservation",font=('Arial',10,"bold"),padx=50,pady=10,fg="white",bg="#848f9e",activebackground="#575917",command=lambda: Cancel_Res(resid))
            proceed.place(relx=0.99,rely=0.95,anchor=SE)
            
            back=Button(root,text="Back",font=('Arial',10,"bold"),padx=50,pady=10,fg="white",bg="#848f9e",activebackground="#575917",command=Cancelation)
            back.place(relx=0.01,rely=0.95,anchor=SW)
    except:
            messagebox.showinfo(title='No reservations found', message='You need to make a reservation to cancel one')
            mainmenu()
        
    return
    
#cancelation page
def Cancelation():
    global email
    global iden
    
    clearFrame()  
    #set window color & appearance    
    root.configure(bg = "#384d66")
    root.title('Car Rental App-Cancel Your Reservation')
    
    #enter email 
    maillabel=Label(root,text="Email:",font=("Arial",10,"bold"),fg="white",bg="#384d66")
    #maillabel.grid(row=0,column=0)
    email=Entry(root,width=50)
    #email.grid(row=0,column=1)
    email.place(relx=0.5,rely=0.3,anchor=CENTER)
    maillabel.place(relx=0.3,rely=0.3,anchor=CENTER)
    #enter reservation id
    idlabel=Label(root,text="Reservation ID:",font=("Arial",10,"bold"),fg="white",bg="#384d66")
    #idlabel.grid(row=1,column=0)
    idlabel.place(relx=0.3,rely=0.35,anchor=CENTER)
    iden=Entry(root,width=50)
    iden.place(relx=0.5,rely=0.35,anchor=CENTER)
    #back button
    back1=Button(root,text="Back",font=('Arial',10,"bold"),padx=50,pady=10,fg="white",bg="#848f9e",activebackground="#575917",command=mainmenu)
    back1.place(relx=0.01,rely=0.95,anchor=SW)
    #proceed button
    proceed=Button(root,text="Proceed",font=('Arial',10,"bold"),padx=50,pady=10,fg="white",bg="#848f9e",activebackground="#575917",command=Proceed_Cancelation)
    proceed.place(relx=0.99,rely=0.95,anchor=SE)

#Insert and Update all necessary tables in SQL database
def Confirm():
    cardno=int(cardnume.get())
    exp=expde.get()
    cvv=int(cvve.get())
    
    #connect to database
    conn = sqlite3.connect('car-rental-python-database.db')
    c= conn.cursor()
    #add client info into database
    c.execute("INSERT OR IGNORE INTO client VALUES(?,?,?,?,?,?,?,?)",
    (afm,fname,lname,dr,mail,phone,addr,addrn) )
    conn.commit()
    conn.close()
    #add reservation info into database
    
    #find and save pick up location id
    conn = sqlite3.connect('car-rental-python-database.db')
    c= conn.cursor()
    c.execute("SELECT location_id FROM location where lname=?", (pulclicked.get(),))
    l1=c.fetchone()
    pickup=l1[0]    
    #find and save drop off location id
    c.execute("SELECT location_id FROM location where lname=?", (dolclicked.get(),))
    l2=c.fetchone()
    dropoff=l2[0]
    #find and save car key and category key
    c.execute("SELECT car_id,cat_id FROM car where model=?", (caropt.get(),))
    l1=c.fetchone()
    car=l1[0]
    cat=l1[1]
    #save insurance key
    c.execute("SELECT insurance_id FROM insurance where iname=?", (inopt.get(),))
    l1=c.fetchone()
    ins_id=l1[0]
    #get today's date
    today = date.today()
    day= today.strftime("%Y-%m-%d")

    c.execute("INSERT OR IGNORE INTO reservation (client_id,reservation_date,pickup_date,return_date,total_cost,ins_id,cat_id,c_id,pul_id,dol_id) VALUES(?,?,?,?,?,?,?,?,?,?)",
    (afm,day,pick_date,drop_date,total,ins_id,cat,car,pickup,dropoff) )
    
    conn.commit()
    conn.close()
    
    #fetch reservation_id
    conn = sqlite3.connect('car-rental-python-database.db')
    c= conn.cursor()
    c.execute("SELECT reservation_id FROM reservation where client_id=?", (afm,))
    l=c.fetchall()
    rid=[]
    for i in range(0,len(l)):
        rid.append(l[i][0])
    rid=rid[-1]
    
    conn.commit()
    conn.close()
    
    #query for free_can_period
    #update reservation and make sure that free cancelation period ends 10 days before pickup date
    conn = sqlite3.connect('car-rental-python-database.db')
    c= conn.cursor()
    c.execute("UPDATE reservation SET free_can_period=(date((pickup_date),'-10 days'))WHERE reservation_id=?", (rid,))

    conn.commit()
    
    conn.close()
    
    #add payment info into database
    conn = sqlite3.connect('car-rental-python-database.db')
    c= conn.cursor()
    c.execute("INSERT INTO payment(r_id,card_number,card_exp_date,card_cvv) VALUES(?,?,?,?)",
    (rid,cardno,exp,cvv) )


    #contains keys
    ser_id=[]
    ser_id.append(sopt1.get())
    ser_id.append(sopt2.get())
    ser_id.append(sopt3.get())
    ser_id.append(sopt4.get())
    for i in range(0,len(ser_id)):
        if ser_id[i]!=0:
            c.execute("INSERT OR IGNORE INTO contains VALUES(?,?)",
                      (rid,ser_id[i]))

    
    
    conn.commit()
    conn.close()

    messagebox.showinfo(title='Reservation was succesful', message='Thank you for your reservation! \n Your reservation id is : {}'.format(rid))
    mainmenu()
    
#Check that payment info is valid
def Pay_Check():
    
    card=cardnume.get()
    exp=expde.get()
    cvv=cvve.get()

    form="%Y-%m"
    advance=1

    #Prompt user to enter correct formats
    if len(card)==0:
        messagebox.showinfo(title='Invalid entries', message='Enter your card number')
        advance=0
    elif len(card)!=16 or card.isnumeric()==False:
        messagebox.showinfo(title='Invalid entries', message='Card number must be 16 digits')
        advance=0
    elif len(exp)==0:
        messagebox.showinfo(title='Invalid entries', message='Enter the expiration date of your card')
        advance=0
    elif len(cvv)==0:
        messagebox.showinfo(title='Invalid entries', message='Enter the CVV of your card')
        advance=0
    elif len(cvv)!=3 or cvv.isnumeric()==False:
        messagebox.showinfo(title='Invalid entries', message='CVV must be 3 digits')
        advance=0
    else:
        try:
            datetime.strptime(exp,form)
        except ValueError:
            messagebox.showinfo(title='Invalid entries', message='Date format should be YYYY-MM')
            advance=0
            
    if advance==1:
        Confirm()
        
#Payment info
def Pay():
    global cardnume
    global expde
    global cvve
    
    clearFrame()
    #set window color & appearance    
    root.configure(bg = "#384d66")
    root.title('Car Rental App-Complete Payment')
    root.geometry('1024x683')

    #enter card number
    cardnum=Label(root,text="Enter Card Number: ",font=("Arial",10,"bold"),fg="white",bg="#384d66")    
    cardnume=Entry(root,width=50)                                                                     
    cardnum.place(relx=0.3,rely=0.25,anchor=CENTER)                                                 
    cardnume.place(relx=0.55,rely=0.25,anchor=CENTER)    
    #enter card exp date
    expd=Label(root,text="Card Expiration Date:",font=("Arial",10,"bold"),fg="white",bg="#384d66")    
    expde=Entry(root,width=50)                                                                    
    expd.place(relx=0.3,rely=0.3,anchor=CENTER)
    expde.place(relx=0.55,rely=0.3,anchor=CENTER)    
    #enter cvv
    cvv=Label(root,text="CVV:",font=("Arial",10,"bold"),fg="white",bg="#384d66")   
    cvve=Entry(root,width=50)                                                                    
    cvv.place(relx=0.3,rely=0.35,anchor=CENTER)
    cvve.place(relx=0.55,rely=0.35,anchor=CENTER)        
    
    #back button
    back1=Button(root,text="Back",font=('Arial',10,"bold"),padx=50,pady=10,fg="white",bg="#848f9e",activebackground="#575917",command=Book)
    back1.place(relx=0.01,rely=0.95,anchor=SW)
    #proceed button
    confirm=Button(root,text="Confirm",font=('Arial',10,"bold"),padx=50,pady=10,fg="white",bg="#848f9e",activebackground="#575917",command=Pay_Check)
    confirm.place(relx=0.99,rely=0.95,anchor=SE)

#Check that email format is correct 
def check(email):
    
    #Format checked using regular expressions
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

#Check that user's cedentials are valid 
def Book_Check():
    global afm
    global fname
    global lname
    global dr
    global mail
    global phone
    global addr
    global addrn
    
    afm=afme.get()
    fname=fnamee.get()
    lname=lnamee.get()
    dr=dre.get()
    mail=maile.get()
    phone=phonee.get()
    addr=addre.get()
    addrn=addrne.get()

    #Prompt user to enter proper credentials
    if len(fname)==0:
        messagebox.showinfo(title='Invalid entries', message='Enter your first name')
    elif len(lname)==0:
        messagebox.showinfo(title='Invalid entries', message='Enter your last name')
    elif len(addr)==0:
        messagebox.showinfo(title='Invalid entries', message='Enter your address street')
    elif len(addrn)==0 or addrn.isnumeric()==False:
        messagebox.showinfo(title='Invalid entries', message='Enter your address number')
    elif len(afm)==0:
        messagebox.showinfo(title='Invalid entries', message='Enter your AFM')
    elif len(afm)!=9 or afm.isnumeric()==False:
        messagebox.showinfo(title='Invalid entries', message='AFM must be 9 digits')
    elif len(dr)!=9 or dr.isnumeric()==False:
        messagebox.showinfo(title='Invalid entries', message='Driving license must be 9 digits')
    elif len(mail)==0 or check(mail)==False:
        messagebox.showinfo(title='Invalid entries', message='Invalid Email')
    elif len(phone)!=10 or phone.isnumeric()==False:
        messagebox.showinfo(title='Invalid entries', message='Phone number must be 10 digits')
    else:
        afm=int(afm)
        dr=int(dr)
        phone=int(phone)
        addrn=int(addrn)
        Pay()

#Client's personal info        
def Book():
    global afme
    global fnamee
    global lnamee
    global dre
    global maile
    global phonee
    global addre
    global addrne
 
    clearFrame()
    #set window color & appearance    
    root.configure(bg = "#384d66")
    root.title('Car Rental App-Client Information')
    root.geometry('1024x683')

    #enter name
    fname=Label(root,text="Enter Full Name: ",font=("Arial",10,"bold"),fg="white",bg="#384d66")    
    fnamee=Entry(root,width=25)
    lnamee=Entry(root,width=25)
    fname.place(relx=0.3,rely=0.25,anchor=CENTER)                                                 
    fnamee.place(relx=0.475,rely=0.25,anchor=CENTER)
    lnamee.place(relx=0.63,rely=0.25,anchor=CENTER)
    #enter client afm
    afm=Label(root,text="AFM:",font=("Arial",10,"bold"),fg="white",bg="#384d66")    
    afme=Entry(root,width=50)                                                                    
    afm.place(relx=0.3,rely=0.3,anchor=CENTER)
    afme.place(relx=0.55,rely=0.3,anchor=CENTER)    
    #enter driv license
    dr=Label(root,text="Driver License :",font=("Arial",10,"bold"),fg="white",bg="#384d66")   
    dre=Entry(root,width=50)                                                                    
    dr.place(relx=0.3,rely=0.35,anchor=CENTER)
    dre.place(relx=0.55,rely=0.35,anchor=CENTER)
    #enter email
    mail=Label(root,text="E-mail:",font=("Arial",10,"bold"),fg="white",bg="#384d66")    
    maile=Entry(root,width=50)
    mail.place(relx=0.3,rely=0.4,anchor=CENTER)
    maile.place(relx=0.55,rely=0.4,anchor=CENTER)       
    
    #enter phone number
    phone=Label(root,text="Phone Number:",font=("Arial",10,"bold"),fg="white",bg="#384d66")    
    phonee=Entry(root,width=50)
    phone.place(relx=0.3,rely=0.45,anchor=CENTER)
    phonee.place(relx=0.55,rely=0.45,anchor=CENTER)       
    #insert address
    addr=Label(root,text="Address:",font=("Arial",10,"bold"),fg="white",bg="#384d66")    
    addr.place(relx=0.3,rely=0.5,anchor=CENTER)
    addre=Entry(root,width=25)
    addrne=Entry(root,width=10)
    addre.place(relx=0.475,rely=0.5,anchor=CENTER)                                                 
    addrne.place(relx=0.6,rely=0.5,anchor=CENTER)
    
    
    #back button
    back1=Button(root,text="Back",font=('Arial',10,"bold"),padx=50,pady=10,fg="white",bg="#848f9e",activebackground="#575917",command=Search)
    back1.place(relx=0.01,rely=0.95,anchor=SW)
    #proceed button
    pay=Button(root,text="Pay",font=('Arial',10,"bold"),padx=50,pady=10,fg="white",bg="#848f9e",activebackground="#575917",command=Book_Check)
    pay.place(relx=0.99,rely=0.95,anchor=SE)

#Add services and insurance to total cost
def Calculate_Cost(total_cost):
    global total
    x=0
    y=0

    ins=inopt.get()
    
    ser1=sopt1.get()
    ser2=sopt2.get()
    ser3=sopt3.get()
    ser4=sopt4.get()
    ser=[ser1, ser2, ser3, ser4]
    ser_cost=[]
    
    conn = sqlite3.connect('car-rental-python-database.db')
    c= conn.cursor()

    c.execute("SELECT cost FROM insurance WHERE iname=?", (ins,))
    ins_cost = c.fetchall()
    for i in range(0,len(ser)):        
        c.execute("SELECT cost FROM services WHERE services_id=?", (ser[i],))
        l=c.fetchall()
        if len(l)==1:
            ser_cost.append(int(l[0][0]))
            
    if len(ins_cost)!=0:
        x=ins_cost[0][0]
    if len(ser_cost)!=0:
        y=sum(ser_cost)

    #Calculate total cost including insurance and extra services
    total = total_cost + x + y
    cost_lab_txt.delete('1.0', END)
    cost_lab_txt.insert(INSERT,str(total) + "€")
    conn.commit()

    
    #close database
    conn.close()

#Check car and insurance entries are not empty
def Search_Check():

    #If no car or insurance package has been selected prompt the user to make a selection
    car=caropt.get()
    insurance=inopt.get()
    
    if len(car)==0:
        messagebox.showinfo(title='Invalid entries', message='Select a car')
        advance=0
    elif len(insurance)==0:
        messagebox.showinfo(title='Invalid entries', message='Select an insurance package')
        advance=0
    else:
        Book()
        
#Search page where the user selects car, insurance and extra perks
def Search():
    global caropt
    global inopt
    global sopt1 
    global sopt2
    global sopt3
    global sopt4
    global cost_lab_txt
    global pick_date
    global drop_date
    
    clearFrame()
    #set window color & appearance    
    root.configure(bg = "#384d66")
    root.title('Car Rental App-Make Your Reservation')
    root.geometry('1024x683')
    soptions=[]
    ioptions=[]
    coptions=[]
    sid=[]
    
    #connect to database
    conn = sqlite3.connect('car-rental-python-database.db')
    c= conn.cursor()
    
    #find all available services
    c.execute("SELECT sname FROM services")  #null option?
    
    #store results in list
    li=c.fetchall()
    for i in range(0,len(li)):
        soptions.append(li[i][0])

    c.execute("SELECT services_id FROM services")  
    #store results in list
    li=c.fetchall()
    for i in range(0,len(li)):
        sid.append(li[i][0])
        
    #find insurance options
    c.execute("SELECT iname FROM insurance")
    li=c.fetchall()
    for i in range(0,len(li)):
        ioptions.append(li[i][0])
    
    #find available cars
    c.execute("SELECT category_id FROM category WHERE size=?",(catopt.get(),))
    category = c.fetchall()[0][0]
        
    c.execute("SELECT cost_per_day FROM category WHERE category_id=?",(category,))
    cost_per_day = c.fetchall()[0][0]

    qry = """SELECT DISTINCT car_id,car.cat_id,model
            FROM car LEFT JOIN reservation ON c_id = car_id 
            WHERE (pickup_date IS NULL AND car.cat_id=?)
            OR (car.cat_id=? AND car_id NOT IN (SELECT c_id FROM reservation 
                                                WHERE cat_id=? 
                                                AND((pickup_date <= ? AND return_date >= ?)
                                                OR (pickup_date < ? AND return_date >= ?)
                                                OR (pickup_date >= ? AND return_date <= ?))))"""

    c.execute(qry,(category,category,category,pick,pick,drop,drop,pick,drop))
                                                                
    li=c.fetchall()
    
    for i in range(0,len(li)):
        #coptions.append(li[i])
        coptions.append(li[i][2])
    conn.commit()
    
    #close database
    conn.close()
    
    #choose an available car
    av_car=Label(root,text="Choose an available car: ",font=("Arial",10,"bold"),fg="white",bg="#384d66")    
                                                                                                    
    av_car.place(relx=0.3,rely=0.25,anchor=CENTER)                                                    
    #teste.place(relx=0.55,rely=0.25,anchor=CENTER)                                                 
    caropt=StringVar()
    av_car_dropdown=OptionMenu(root,caropt,*coptions)
    av_car_dropdown.config(width=35)
    av_car_dropdown.place(relx=0.525,rely=0.25,anchor=CENTER) 
                                                                                                    
    #choose an insurance package
    ins_pack=Label(root,text="Choose an insurance package:",font=("Arial",10,"bold"),fg="white",bg="#384d66")    
    ins_pack.place(relx=0.3,rely=0.3,anchor=CENTER)
    inopt=StringVar()
    ins_pack_dropdown=OptionMenu(root,inopt,*ioptions)
    ins_pack_dropdown.config(width=35)
    ins_pack_dropdown.place(relx=0.525,rely=0.3,anchor=CENTER)
    
    #choose extra services
    servs=Label(root,text="Choose extra services:",font=("Arial",10,"bold"),fg="white",bg="#384d66")   
    servs.place(relx=0.3,rely=0.35,anchor=CENTER)

    sopt1=IntVar()
    check1=Checkbutton(root,text=soptions[0],variable=sopt1,onvalue=sid[0],offvalue=0) 
    check1.place(relx=0.445,rely=0.35,anchor=CENTER)
    
    sopt2=IntVar()
    check2=Checkbutton(root,text=soptions[1],variable=sopt2,onvalue=sid[1],offvalue=0) 
    check2.place(relx=0.425,rely=0.4,anchor=CENTER)
    
    sopt3=IntVar()
    check3=Checkbutton(root,text=soptions[2],variable=sopt3,onvalue=sid[2],offvalue=0) 
    check3.place(relx=0.53,rely=0.35,anchor=CENTER)

    sopt4=IntVar()
    check4=Checkbutton(root,text=soptions[3],variable=sopt4,onvalue=sid[3],offvalue=0) 
    check4.place(relx=0.54,rely=0.4,anchor=CENTER)
    
    #calculate cost based on car categpry and reservation length
    pick_up = pick.split("-")
    if len(pick_up[1])==1:
        pick_up[1]=pick_up[1].zfill(2)
    day1 = date(int(pick_up[0]),int(pick_up[1]),int(pick_up[2]))
               
    drop_off = drop.split("-")
    if len(drop_off[1])==1:
        drop_off[1]=drop_off[1].zfill(2)
    day2 = date(int(drop_off[0]),int(drop_off[1]),int(drop_off[2]))
    
    
    total_cost = cost_per_day * ((day2-day1).days + 1)
    
    cost_lab=Label(root,text="Total Cost:",font=("Arial",10,"bold"),fg="white",bg="#384d66")    
    cost_lab_txt=Text(root,width=25,height=1)
    cost_lab.place(relx=0.3,rely=0.5,anchor=CENTER)
    cost_lab_txt.place(relx=0.5,rely=0.5,anchor=CENTER)

    calc = Button(root,text="Calculate",font=('Arial',10,"bold"),fg="white",bg="#848f9e",activebackground="#575917",command=lambda: Calculate_Cost(total_cost))
    calc.place(relx=0.61,rely=0.48)

    pick_date=day1
    drop_date=day2
    
    #back button
    back1=Button(root,text="Back",font=('Arial',10,"bold"),padx=50,pady=10,fg="white",bg="#848f9e",activebackground="#575917",command=Reservation)
    back1.place(relx=0.01,rely=0.95,anchor=SW)
    #proceed button
    book=Button(root,text="Book",font=('Arial',10,"bold"),padx=50,pady=10,fg="white",bg="#848f9e",activebackground="#575917",command=Search_Check)
    book.place(relx=0.99,rely=0.95,anchor=SE)

#Check reservation entries and proceed
def Reservation_Check():
    global pick
    global drop
    
    pick=pude.get()
    drop=doden.get()
    pick_loc=pulclicked.get()
    drop_loc=dolclicked.get()
    cat=catopt.get()

    advance=1
    form="%Y-%m-%d"
    drop_date=0
    pick_date=0
    
    if len(pick_loc)==0:
        messagebox.showinfo(title='Invalid entries', message='Enter pick up location')
        advance=0
    elif len(drop_loc)==0:
        messagebox.showinfo(title='Invalid entries', message='Enter drop off location')
        advance=0
    elif len(cat)==0:
        messagebox.showinfo(title='Invalid entries', message='Enter car category')
        advance=0
    else:
        try:
            #Making sure that the date formats are valid
            datetime.strptime(pick,form)
            datetime.strptime(drop,form)
            
            pick_l=pick.split('-')
            pick_date=date(int(pick_l[0]),int(pick_l[1]),int(pick_l[2]))
    
            drop_l=drop.split('-')
            drop_date=date(int(drop_l[0]),int(drop_l[1]),int(drop_l[2]))
            
        except ValueError:
            #If not show appropriate message
            messagebox.showinfo(title='Invalid entries', message='Date format should be YYYY-MM-DD')
            advance=0

    #Making sure that pick up date is before or same as drop off date
    if advance==1 and drop_date<pick_date:
        messagebox.showinfo(title='Invalid entries', message='Drop off date can not be before pick up date')
        advance=0
        
    if advance==1:
        Search()
        
#reservation page
def Reservation():
    global pulclicked
    global dolclicked
    global pude
    global doden
    global catopt
    
    clearFrame()
    #set window color & appearance    
    root.configure(bg = "#384d66")
    root.title('Car Rental App-Make Your Reservation')
    root.geometry('1024x683')
    #create empty list to store location query
    options=[]
    #connect to database
    conn = sqlite3.connect('car-rental-python-database.db')
    c= conn.cursor()
    #find all available location names
    c.execute("SELECT lname FROM location")
    #store results in list
    li=c.fetchall()
    for i in range(0,len(li)):
        options.append(li[i][0])
    #print(options)

    conn.commit()
    #close database
    conn.close()

    #choose pick up and drop off location
    pul=Label(root,text="Pick up Location: ",font=("Arial",10,"bold"),fg="white",bg="#384d66")    
    pul.place(relx=0.3,rely=0.25,anchor=CENTER)
    pulclicked=StringVar(root)
    puld=OptionMenu(root,pulclicked,*options)
    puld.config(width=10)
    puld.place(relx=0.41,rely=0.25,anchor=CENTER)  
    
    dol=Label(root,text="Drop off Location:",font=("Arial",10,"bold"),fg="white",bg="#384d66")
    #create dropdown menu with available locations
    dol.place(relx=0.3,rely=0.3,anchor=CENTER)
    dolclicked=StringVar()
    dold=OptionMenu(root,dolclicked,*options)
    dold.config(width=10)
    dold.place(relx=0.41,rely=0.3,anchor=CENTER)  

    #choose dates
    pud=Label(root,text="Pick up Date:",font=("Arial",10,"bold"),fg="white",bg="#384d66")   
    pude=Entry(root,width=50)                                                                     #-> calendar?
    pud.place(relx=0.3,rely=0.35,anchor=CENTER)
    pude.place(relx=0.51,rely=0.35,anchor=CENTER)   

    dod=Label(root,text="Drop off Date:",font=("Arial",10,"bold"),fg="white",bg="#384d66")    
    doden=Entry(root,width=50)
    dod.place(relx=0.3,rely=0.4,anchor=CENTER)
    doden.place(relx=0.51,rely=0.4,anchor=CENTER)    

    #choose car category
    cat_car=Label(root,text="Choose a car category: ",font=("Arial",10,"bold"),fg="white",bg="#384d66")
    cat_car.place(relx=0.275,rely=0.45,anchor=CENTER)
    
    catopt=StringVar()
    catd=OptionMenu(root,catopt,'City','SUV','Jeep')
    catd.config(width=35)
    catd.place(relx=0.485,rely=0.45,anchor=CENTER)
    
    #back button
    back1=Button(root,text="Back",font=('Arial',10,"bold"),padx=50,pady=10,fg="white",bg="#848f9e",activebackground="#575917",command=mainmenu)
    back1.place(relx=0.01,rely=0.95,anchor=SW)
    #proceed button
    search=Button(root,text="Search",font=('Arial',10,"bold"),padx=50,pady=10,fg="white",bg="#848f9e",activebackground="#575917",command=Reservation_Check)
    search.place(relx=0.99,rely=0.95,anchor=SE)

#main page
def mainmenu():
    global bg
    clearFrame()
    #set window color & appearance
    root.title('Car Rental App')
    root.geometry('1024x683')

    #disable window resizing 
    root.resizable(False, False)
    #change app icon
    root.iconbitmap("caricon.ico")

    #add image of car to background
    bg = PhotoImage(file = "car3.png") # ->needs to be in png format
      
    # Show image using label widget
    label1 = Label( root, image = bg)
    label1.place(x=0,y=0) 

     #button widgets for reservation options
    op1=Button(root,text="Make a\nReservation",font=('Arial',20,"bold"),width=15,height=5,fg="white",bg="#1a2537",activebackground="#373c0e",command=Reservation)
    op2=Button(root,text="Cancel a\nReservation",font=('Arial',20,"bold"),width=15,height=5,fg="white",bg="#1a2537",activebackground="#373c0e",command=Cancelation)
    op3=Button(root,text="Return car",font=('Arial',20,"bold"),width=15,height=5,fg="white",bg="#1a2537",activebackground="#373c0e",command=Return)
    op4=Button(root,text="Rate us!",font=('Arial',20,"bold"),width=15,height=5,fg="white",bg="#1a2537",activebackground="#373c0e",command=Evaluation)
    

    #put buttons on app window
    
    op1.grid(row=0,column=0)
    op2.grid(row=0,column=1)
    op3.grid(row=0,column=2)
    op4.grid(row=0,column=3)
    
#open tkinter window
root= Tk()
#create mainmenu widgets
mainmenu()
#run the mainloop
root.mainloop()
