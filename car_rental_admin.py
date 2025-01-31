from tkinter import *
from tkinter import messagebox
import sqlite3
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
from tkinter import ttk
import numpy as np

#
def clearFrame():
    # destroy all widgets from frame
    for widget in root.winfo_children():
       widget.destroy()
       
#Model based search
def Model(model):
    m = model.get()
    if len(m)!=0:
        m='%'+ m +'%'

        conn = sqlite3.connect('car-rental-python-database.db')
        c= conn.cursor()
        
        #search models that contain letters that we got from the entry 
        mod = """SELECT car_id,model,size,lname
                FROM car JOIN location ON l_id=location_id JOIN category ON cat_id=category_id
                WHERE model like ?;"""
        x=c.execute(mod,(m,))
        q=x.fetchall()
        conn.commit()

        #Make treeview to exhibit data
        cols=('License Plate', 'Model', 'Size','Location','Availability')
        tree = ttk.Treeview(root, columns=cols, show='headings')

        for col in cols:
            tree.heading(col, text=col)            
        
        #check if car on reservation or free
        #If on reservation show with whom
        for j in range(0,len(q)):
            on_reservation=[]
            free="""SELECT pickup_date <= date('now') and return_date > date('now') and returned_date is NULL and cancellation_date is NULL,reservation_id
                    FROM car JOIN reservation on c_id=car_id
                    WHERE model like ?;"""

            x=c.execute(free,('%' + q[j][1] + '%',))
            w=x.fetchall()
            for k in range(0,len(w)):
                if w[k][0]==1:
                    on_reservation.append('On reservation with: {}'.format(w[k][1])) 
            conn.commit()
        
            if len(on_reservation)==0:
                on_reservation.append('Free')
            
            tree.insert("", "end", values=(q[j][0],q[j][1],q[j][2],q[j][3],on_reservation[0]))
                
            style=ttk.Style()
            style.theme_use("clam")
            style.configure("Treeview",
                            background="#839091",
                            foreground="red",
                            rowheight=35,
                            fieldbackground="#839091")
            style.map("Treeview",
                      background=[('selected','#0b316e')])
            
            tree.place(relx=0.01,rely=0.2)
        conn.close()
    else:
        messagebox.showinfo(title='Invalid entry', message='Enter a car model') 

#License based search    
def License(licensee):
    l=licensee.get()
    if len(l)!=0:
        conn = sqlite3.connect('car-rental-python-database.db')
        c= conn.cursor()

        #fetch info about car 
        lic = """SELECT car_id,model,size,lname
                FROM car JOIN location ON l_id=location_id JOIN category ON cat_id=category_id
                WHERE car_id=?;"""
        x=c.execute(lic,(l,))
        q=x.fetchall()
        conn.commit()
        
        #check if car on reservation or free
        #If on reservation show with whom
        on_reservation=[]
        
        for j in range(0,len(q)):
            free="""SELECT pickup_date <= date('now') and return_date > date('now') and returned_date is NULL and cancellation_date is NULL,reservation_id
                    FROM car JOIN reservation on c_id=car_id
                    WHERE car_id=?;"""

            x=c.execute(free,(q[j][0],))
            w=x.fetchall()
            
            for k in range(0,len(w)):
                if w[k][0]==1:
                    on_reservation.append('On reservation with: {}'.format(w[k][1])) 
            conn.commit()
        conn.close()
        if len(on_reservation)==0:
            on_reservation.append('Free')

        #Make treeview to exhibit data
        cols=('License Plate', 'Model', 'Size','Location','Availability')
        tree = ttk.Treeview(root, columns=cols, show='headings')

        for col in cols:
            tree.heading(col, text=col)
        for i in range(0,len(q)):
            tree.insert("", "end", values=(q[i][0],q[i][1],q[i][2],q[i][3],on_reservation[0]))
            
        style=ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#839091",
                        foreground="red",
                        rowheight=35,
                        fieldbackground="#839091")
        style.map("Treeview",
                  background=[('selected','#0b316e')])
        
        tree.place(relx=0.01,rely=0.2)
    else:
         messagebox.showinfo(title='Invalid entry', message='Enter a valid license plate')
         
#Location based search
def Location(location):
    loc = location.get()
    if len(loc)!=0:
        loc=loc +'%'

        conn = sqlite3.connect('car-rental-python-database.db')
        c= conn.cursor()

        #fetch info about car bsed on location
        loca = """SELECT car_id,model,size,lname
                FROM car JOIN location ON l_id=location_id JOIN category ON cat_id=category_id
                WHERE lname like ?;"""
        x=c.execute(loca,(loc,))
        q=x.fetchall()
        conn.commit()

        #Make a treeview to exhibit data
        cols=('License Plate', 'Model', 'Size','Location','Availability')
        tree = ttk.Treeview(root, columns=cols, show='headings')

        for col in cols:
            tree.heading(col, text=col)

        #check if car on reservation or free
        #If on reservation show with whom
        for j in range(0,len(q)):
            on_reservation=[]
            free="""SELECT pickup_date <= date('now') and return_date > date('now') and returned_date is NULL and cancellation_date is NULL,reservation_id
                    FROM car JOIN reservation on c_id=car_id
                    WHERE car_id = ?;"""

            x=c.execute(free,(q[j][0],))
            w=x.fetchall()
            for k in range(0,len(w)):
                if w[k][0]==1:
                    on_reservation.append('On reservation with: {}'.format(w[k][1]))
            conn.commit()
            if len(on_reservation)==0:
                on_reservation.append('Free')

            tree.insert("", "end", values=(q[j][0],q[j][1],q[j][2],q[j][3],on_reservation[0]))
                
            style=ttk.Style()
            style.theme_use("clam")
            style.configure("Treeview",
                            background="#839091",
                            foreground="red",
                            rowheight=35,
                            fieldbackground="#839091")
            style.map("Treeview",
                      background=[('selected','#0b316e')])
            
            tree.place(relx=0.01,rely=0.2)
        conn.close()
    else:
        messagebox.showinfo(title='Invalid entry', message='Enter a location') 

#Show Model based search
def Model_Search():
    
    #enter model
    model_label=Label(root,text="Model:",font=("Arial",10,"bold"),fg="white",bg="#1c1f08")
    
    model_label.place(relx=0.3,rely=0.06,anchor=CENTER)
    model=Entry(root,width=50)
    model.place(relx=0.48,rely=0.06,anchor=CENTER)

    #search model
    search = Button(root,text="Search",font=('Arial',10,"bold"),fg="white",bg="#848f9e",activebackground="#575917",command=lambda: Model(model))
    search.place(relx=0.64,rely=0.04)

#Show License based search
def License_Search():

    #enter license
    licensee_label=Label(root,text="Plate:",font=("Arial",11,"bold"),fg="white",bg="#1c1f08")
    
    licensee_label.place(relx=0.3,rely=0.06,anchor=CENTER)
    licensee=Entry(root,width=50)
    licensee.place(relx=0.48,rely=0.06,anchor=CENTER)

    #search model
    search = Button(root,text="Search",font=('Arial',10,"bold"),fg="white",bg="#848f9e",activebackground="#575917",command=lambda: License(licensee))
    search.place(relx=0.64,rely=0.04)
    
#Show Location based search
def Location_Search():
    #enter location
    location_label=Label(root,text="Where:",font=("Arial",10,"bold"),fg="white",bg="#1c1f08")
    
    location_label.place(relx=0.3,rely=0.06,anchor=CENTER)
    location=Entry(root,width=50)
    location.place(relx=0.48,rely=0.06,anchor=CENTER)

    #search model
    search = Button(root,text="Search",font=('Arial',10,"bold"),fg="white",bg="#848f9e",activebackground="#575917",command=lambda: Location(location))
    search.place(relx=0.64,rely=0.04)
    
#Search car based on location, license and model
def Search_Car():
    clearFrame()
    root.title('Car Rental Admin-Cars')

    var = IntVar()
    R1=Radiobutton(root,text="Search by model ",variable=var,fg="white",bg="#1c1f08",value=1,command=Model_Search)
    R2=Radiobutton(root,text="Search by license plate",variable=var,fg="white",bg="#1c1f08",value=2,command=License_Search)
    R3=Radiobutton(root,text="Search by location",variable=var,fg="white",bg="#1c1f08",value=3,command=Location_Search)

    R1.place(relx=0.05,rely=0.025)
    R2.place(relx=0.05,rely=0.075)
    R3.place(relx=0.05,rely=0.125)
     
    #back button
    back1=Button(root,text="Back",font=('Arial',10,"bold"),padx=50,pady=10,fg="white",bg="#848f9e",activebackground="#575917",command=mainmenu)
    back1.place(relx=0.01,rely=0.95,anchor=SW)

#Add damages to total cost
def Add_Damages(cost,resid):
    dmg=damages_txt.get('1.0',END)

    total = cost + int(dmg)

    #Update necessary table
    conn = sqlite3.connect('car-rental-python-database.db')
    c= conn.cursor()
    c.execute("UPDATE reservation SET total_cost=? WHERE reservation_id=?",(total,resid))
    conn.commit()
    c.execute("UPDATE reservation SET damages=? WHERE reservation_id=?",(int(dmg),resid))
    conn.commit()
    conn.close()
    if int(dmg)!=0:
        messagebox.showinfo(title='Damages added', message='Damages added to total cost succesfully')
        
#Show reservation info and add damgages if needed   
def Res_Info(resid):
    global text_res
    global damages_txt

    #delete pre-existing widgets if there are any
    try:
        for item in text_res:
            item.destroy()
    except:pass
    try:
        for item in text_car:
            item.destroy()
    except:pass
    try:
        for item in text_client:
            item.destroy()
    except:pass
    
    text_res=[]
    conn = sqlite3.connect('car-rental-python-database.db')
    c= conn.cursor()
    #fetch and show reservation details
    reservation = """SELECT pickup_date,return_date,returned_date,cancellation_date,total_cost
                  FROM reservation 
                  WHERE reservation_id=?"""
    
    x=c.execute(reservation,(resid,))
    res=x.fetchall()
    conn.commit()
    conn.close()

    pickup = Label(root,text='Pickup Date: ',font=("Arial",15,"bold"),fg="yellow",bg="#1c1f08")
    pickup_value = Label(root,text=res[0][0],font=("Arial",15,"bold"),fg="white",bg="#1c1f08")
    dropoff = Label(root,text='Scheduled return date: ',font=("Arial",15,"bold"),fg="yellow",bg="#1c1f08")
    dropoff_value = Label(root,text=res[0][1],font=("Arial",15,"bold"),fg="white",bg="#1c1f08")

    pickup.place(relx=0.3,rely=0.2)
    pickup_value.place(relx=0.42,rely=0.2) 
    dropoff.place(relx=0.3,rely=0.24)
    dropoff_value.place(relx=0.52,rely=0.24)
    
    text_res=[pickup,pickup_value,dropoff,dropoff_value]

    #if car returned the admin can add damages if needed
    if res[0][2]!=None:
        returned = Label(root,text='Return date: ',font=("Arial",15,"bold"),fg="yellow",bg="#1c1f08")
        returned_value = Label(root,text=res[0][2],font=("Arial",15,"bold"),fg="white",bg="#1c1f08")
        returned.place(relx=0.3,rely=0.32)
        returned_value.place(relx=0.42,rely=0.32)
        
        cost = Label(root,text='Cost (without damages): ',font=("Arial",15,"bold"),fg="yellow",bg="#1c1f08")
        cost_value = Label(root,text=str(res[0][4]) + ' €',font=("Arial",15,"bold"),fg="white",bg="#1c1f08")
        cost.place(relx=0.3,rely=0.36)
        cost_value.place(relx=0.53,rely=0.36)

        damages_lab=Label(root,text="Damages:",font=("Arial",15,"bold"),fg="white",bg="#1c1f08")
        damages_txt=Text(root,width=25,height=1)
        damages_lab.place(relx=0.3,rely=0.44)
        damages_txt.place(relx=0.4,rely=0.45)

        add = Button(root,text="Add",font=('Arial',10,"bold"),fg="white",bg="#848f9e",activebackground="#575917",command=lambda: Add_Damages(res[0][4],resid))
        add.place(relx=0.62,rely=0.445)
        
        text_res.append(returned)
        text_res.append(returned_value)
        text_res.append(cost)
        text_res.append(cost_value)
        text_res.append(damages_lab)
        text_res.append(damages_txt)
        text_res.append(add)

    #don't show cancelation details if cancelation date is NULL    
    if res[0][3]!=None:
        cancel = Label(root,text='Cancellation date: ',font=("Arial",15,"bold"),fg="yellow",bg="#1c1f08")
        cancel_value = Label(root,text=res[0][3],font=("Arial",15,"bold"),fg="white",bg="#1c1f08")
        cancel.place(relx=0.3,rely=0.32)
        cancel_value.place(relx=0.47,rely=0.32)

        text_res.append(cancel)
        text_res.append(cancel_value)
    
#Show client info        
def Client_Info(resid):
    global text_client

    #delete pre-existing widgets if there are any
    try:
        for item in text_client:
            item.destroy()
    except:pass
    try:
        for item in text_car:
            item.destroy()
    except:pass
    try:
        for item in text_res:
            item.destroy()
    except:pass
    
    text_client=[]
    conn = sqlite3.connect('car-rental-python-database.db')
    c= conn.cursor()

    #fetch and show client's info 
    qry = """SELECT afm,fname,lname,email,phone_number
         FROM reservation join client on reservation.client_id = client.afm
         WHERE reservation_id = ?;"""
    x=c.execute(qry,(resid,))
    q=x.fetchall()
    conn.commit()
    conn.close()
    
    afm = Label(root,text='AFM: ',font=("Arial",15,"bold"),fg="yellow",bg="#1c1f08")
    afm_value = Label(root,text=q[0][0],font=("Arial",15,"bold"),fg="white",bg="#1c1f08")
    fname = Label(root,text='First name: ',font=("Arial",15,"bold"),fg="yellow",bg="#1c1f08")
    fname_value = Label(root,text=q[0][1],font=("Arial",15,"bold"),fg="white",bg="#1c1f08")
    lname = Label(root,text='Last name: ',font=("Arial",15,"bold"),fg="yellow",bg="#1c1f08")
    lname_value = Label(root,text=q[0][2],font=("Arial",15,"bold"),fg="white",bg="#1c1f08")
    email = Label(root,text='Email: ',font=("Arial",15,"bold"),fg="yellow",bg="#1c1f08")
    email_value = Label(root,text=q[0][3],font=("Arial",15,"bold"),fg="white",bg="#1c1f08")
    phone = Label(root,text='Phone: ',font=("Arial",15,"bold"),fg="yellow",bg="#1c1f08")
    phone_value = Label(root,text=q[0][4],font=("Arial",15,"bold"),fg="white",bg="#1c1f08")

    afm.place(relx=0.3,rely=0.2)
    afm_value.place(relx=0.35,rely=0.2) 
    fname.place(relx=0.3,rely=0.24)
    fname_value.place(relx=0.41,rely=0.24)
    lname.place(relx=0.3,rely=0.28)
    lname_value.place(relx=0.41,rely=0.28)
    email.place(relx=0.3,rely=0.32)
    email_value.place(relx=0.36,rely=0.32)
    phone.place(relx=0.3,rely=0.36)
    phone_value.place(relx=0.37,rely=0.36)

    text_client=[afm,afm_value,fname,fname_value,lname,lname_value,email,email_value,phone,phone_value]
    return text_client

#Show car info
def Car_Info(resid):
    global text_car

    #delete pre-existing widgets if there are any
    try:
        for item in text_car:
            item.destroy()
    except:pass
    try:
        for item in text_client:
            item.destroy()
    except:pass
    try:
        for item in text_res:
            item.destroy()
    except:pass
        
    text_car=[]
    conn = sqlite3.connect('car-rental-python-database.db')
    c= conn.cursor()
    
    # fetch and show services, insurance package and mdoel
    services = """SELECT sname
                from reservation join contains on reservation_id=r_id join services on contains.s_id=services.services_id
                where reservation_id=?"""
    
    x=c.execute(services,(resid,))
    ser=x.fetchall()
    conn.commit()
    
    insurances = """SELECT iname
                    from reservation join insurance on ins_id=insurance_id
                    where reservation_id=?"""
    
    x=c.execute(insurances,(resid,))
    ins=x.fetchall()
    conn.commit()

    car = """SELECT model
                  FROM reservation JOIN car ON reservation.c_id=car.car_id
                  WHERE reservation_id=?"""
    
    x=c.execute(car,(resid,))
    c=x.fetchall()
    conn.commit()
    conn.close()

    #get all services in a single str variable to print them
    if len(ser)==0:
        all_services='None'
    else:
        all_services=ser[0][0]
        for i in range(1,len(ser)):
            all_services+=', '
            all_services+=ser[i][0]

    model = Label(root,text='Model: ',font=("Arial",15,"bold"),fg="yellow",bg="#1c1f08")
    model_value = Label(root,text=c[0][0],font=("Arial",15,"bold"),fg="white",bg="#1c1f08")
    sers = Label(root,text='Services: ',font=("Arial",15,"bold"),fg="yellow",bg="#1c1f08")
    sers_value = Label(root,text=all_services,font=("Arial",15,"bold"),fg="white",bg="#1c1f08")
    inss = Label(root,text='Insurance: ',font=("Arial",15,"bold"),fg="yellow",bg="#1c1f08")
    inss_value = Label(root,text=ins[0][0],font=("Arial",15,"bold"),fg="white",bg="#1c1f08")
    
    model.place(relx=0.3,rely=0.2)
    model_value.place(relx=0.37,rely=0.2)
    sers.place(relx=0.3,rely=0.24)
    sers_value.place(relx=0.39,rely=0.24)
    inss.place(relx=0.3,rely=0.28)
    inss_value.place(relx=0.4,rely=0.28)

    text_car=[model,model_value,sers,sers_value,inss,inss_value]

#Mkae sure that credentials are correct   
def Proceed_Res(res_id):
    
    resid=res_id.get()
    
    conn = sqlite3.connect('car-rental-python-database.db')
    c= conn.cursor()

    #fetch reservation id
    qry = """SELECT reservation_id
         FROM reservation
         WHERE reservation_id = ?;"""
    x=c.execute(qry,(resid,))
    q=x.fetchall()
    conn.commit()
    conn.close()

    if len(q)==0:
        messagebox.showinfo(title='Invalid credentials', message='Enter valid credentials') 
    else:
        #display client info
        var = IntVar()
        R1=Radiobutton(root,text="Client Info",variable=var,fg="white",bg="#1c1f08",value=1,command=lambda: Client_Info(resid))
        R2=Radiobutton(root,text="Car Info",variable=var,fg="white",bg="#1c1f08",value=2,command=lambda: Car_Info(resid))
        R3=Radiobutton(root,text="Reservation Info",variable=var,fg="white",bg="#1c1f08",value=3,command=lambda: Res_Info(resid))
        R1.place(relx=0.05,rely=0.15)
        R2.place(relx=0.05,rely=0.2)
        R3.place(relx=0.05,rely=0.25)
        
        
#Search Reservation functionality       
def Search_Reservation():
    
    clearFrame()
    root.title('Car Rental Admin-Reservations')
    
    #enter reservation id
    idlabel=Label(root,text="Reservation ID:",font=("Arial",10,"bold"),fg="white",bg="#1c1f08")
    idlabel.place(relx=0.1,rely=0.05,anchor=CENTER)
    res_id=Entry(root,width=50)
    res_id.place(relx=0.3,rely=0.05,anchor=CENTER)

    #search reservation
    search = Button(root,text="Search",font=('Arial',10,"bold"),fg="white",bg="#848f9e",activebackground="#575917",command=lambda: Proceed_Res(res_id))
    search.place(relx=0.46,rely=0.03)
     
    #back button
    back1=Button(root,text="Back",font=('Arial',10,"bold"),padx=50,pady=10,fg="white",bg="#848f9e",activebackground="#575917",command=mainmenu)
    back1.place(relx=0.01,rely=0.95,anchor=SW)

#reservations - category chart
def Reservations_Category():

    reservations=[0,0,0]
    
    conn = sqlite3.connect('car-rental-python-database.db')
    c= conn.cursor()    

    #query to get car categories and number of reservations for each category
    res = '''select cat_id,count(*)
             from reservation
             group by cat_id
          '''
    x=c.execute(res)
    q=c.fetchall()
    
    conn.commit()
    conn.close()

    fig = Figure(figsize = (7, 5),
                 dpi = 100)
    
    categories=["City","SUV","Jeep"]
    
    for i in range(0,len(q)):
        cat=int(q[i][0])
        num_res=int(q[i][1])
        
        reservations[cat-1]=num_res
        
    # adding the subplot
    plot1 = fig.add_subplot(111)
    # plotting the graph
    plot1.bar(categories,reservations)
    plot1.set_xlabel("Category")
    plot1.set_ylabel("Reservations")    
    plot1.set_title("Reservations - Category")
    plot1.set_yticks(np.arange(min(reservations),max(reservations)+1,1.0))
    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig,
                                master = root)  
    canvas.draw()
  
    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().place(relx=0.3,rely=0.2)

#reservations - month chart
def Reservations_Month():

    reservations=[0,0,0,0,0,0,0,0,0,0,0,0]
    
    conn = sqlite3.connect('car-rental-python-database.db')
    c= conn.cursor()


    #query to get pick up date's month and sum of number of reservations for that month
    res = '''select strftime('%m',pickup_date) as month,count(*)
             from reservation
             group by month
          '''
    x=c.execute(res)
    q=c.fetchall()
    
    conn.commit()
    conn.close()

    fig = Figure(figsize = (7, 5),
                 dpi = 100)
    
    months=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    
    for i in range(0,len(q)):
        month=int(q[i][0])
        num_res=int(q[i][1])
        
        reservations[month-1]=num_res
        
    # adding the subplot
    plot1 = fig.add_subplot(111)
  
    # plotting the graph
    plot1.bar(months,reservations)
    plot1.set_xlabel("Month")
    plot1.set_ylabel("Reservations")    
    plot1.set_title("Reservations - Month")
    plot1.set_yticks(np.arange(min(reservations),max(reservations)+1,1.0))
    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig,
                                master = root)  
    canvas.draw()
  
    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().place(relx=0.3,rely=0.2)

#revenue - month chart
def Revenue_Month():
    
    revenue=[0,0,0,0,0,0,0,0,0,0,0,0]
    
    conn = sqlite3.connect('car-rental-python-database.db')
    c= conn.cursor()

    #query to get pick up date's month and sum of total costs for that month
    rev = '''select strftime('%m',pickup_date) as month,sum(total_cost)
            from reservation
            where month is not NULL
            group by month
          '''
    x=c.execute(rev)
    q=c.fetchall()
    
    conn.commit()
    conn.close()

    fig = Figure(figsize = (7, 5),
                 dpi = 100)
    
    months=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

    
    for i in range(0,len(q)):
        month=int(q[i][0])
        month_revenue=int(q[i][1])
        
        revenue[month-1]=month_revenue
        
    # adding the subplot
    plot1 = fig.add_subplot(111)
  
    # plotting the graph
    plot1.bar(months,revenue)
    plot1.set_xlabel("Month")
    plot1.set_ylabel("Revenue")    
    plot1.set_title("Revenue - Month")
    plot1.set_yticks(np.arange(min(revenue),max(revenue)+1,100.0))
    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig,
                                master = root)  
    canvas.draw()
  
    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().place(relx=0.3,rely=0.2)

#Statistics
def Statistics():
    clearFrame()
    root.title('Car Rental Admin-Statistics')

    #Admin can see 3 statistics
    var = IntVar()
    R1=Radiobutton(root,text="See reservations - month chart",variable=var,fg="white",bg="#1c1f08",value=1,command=Reservations_Month)
    R2=Radiobutton(root,text="See revenue - month chart",variable=var,fg="white",bg="#1c1f08",value=2,command=Revenue_Month)
    R3=Radiobutton(root,text="See reservations - category chart",variable=var,fg="white",bg="#1c1f08",value=3,command=Reservations_Category)

    R1.place(relx=0.05,rely=0.2)
    R2.place(relx=0.05,rely=0.25)
    R3.place(relx=0.05,rely=0.3)
  
    #back button
    back1=Button(root,text="Back",font=('Arial',10,"bold"),padx=50,pady=10,fg="white",bg="#848f9e",activebackground="#575917",command=mainmenu)
    back1.place(relx=0.01,rely=0.95,anchor=SW)
    
#Ratings
def Ratings():
    
    clearFrame()
    root.title('Car Rental Admin-Ratings')

    conn = sqlite3.connect('car-rental-python-database.db')
    c= conn.cursor()

    #get average rating and display it
    avg = """SELECT avg(rating)
            from evaluation"""
    x=c.execute(avg)
    average_r=x.fetchall()[0][0]
    print(average_r)
    
    if average_r!=None:
        avg_rating = average_r
    else:
        avg_rating=0
    averageRating=Label(root, text='Average rating: '+str(avg_rating),font=("Arial",15,"bold"),fg="white",bg="#1c1f08").place(relx=0.55,rely=0.1,anchor=CENTER)

    #Show all comments 
    latest_com=Label(root, text='Comments: ',font=("Arial",10,"bold"),fg="white",bg="#1c1f08").place(relx=0.3,rely=0.3,anchor=CENTER)

    comments_txt = Text(root, height=18,width=55,spacing3=4)
    comments_txt.grid(row=0,column=0,rowspan=3,columnspan=2,padx=370,pady=190)
    scrollbar = Scrollbar(root,command=comments_txt.yview)
    scrollbar.grid(row=0,column=1,rowspan=3,padx=130,pady=190,sticky='ns')
    comments_txt['yscrollcommand']=scrollbar.set

    comm = """SELECT comments
                from evaluation"""
    x=c.execute(comm)
    comments=x.fetchall()
    for i in range(len(comments)):
        if len(comments[i][0])!=1:
            comments_txt.insert(INSERT,comments[i][0])
            comments_txt.insert(INSERT,"------------------------------------------------------\n")
    comments_txt.config(state=DISABLED)
    conn.commit()
    conn.close()
    #back button
    back1=Button(root,text="Back",font=('Arial',10,"bold"),padx=50,pady=10,fg="white",bg="#848f9e",activebackground="#575917",command=mainmenu)
    back1.place(relx=0.01,rely=0.95,anchor=SW)
    
#main page
def mainmenu():
    
    clearFrame()
    #set window color & appearance
    root.title('Car Rental Admin')
    root.geometry('1024x683')

    #disable window resizing 
    root.resizable(False, False)
    #change app icon
    root.iconbitmap("caricon.ico")
    
    #button widgets for reservation options
    op1=Button(root,text="Search car",font=('Arial',20,"bold"),padx=65,pady=40,width=5,height=2,fg="white",bg="#1a2537",activebackground="#373c0e", command=Search_Car)
    op2=Button(root,text="Search\nreservation",font=('Arial',20,"bold"),padx=70,pady=40,width=5,height=2,fg="white",bg="#1a2537",activebackground="#373c0e", command=Search_Reservation)
    op3=Button(root,text="Statistics",font=('Arial',20,"bold"),padx=65,pady=40,width=5,height=2,fg="white",bg="#1a2537",activebackground="#373c0e", command=Statistics)
    op4=Button(root,text="Ratings",font=('Arial',20,"bold"),padx=70,pady=40,width=5,height=2,fg="white",bg="#1a2537",activebackground="#373c0e", command=Ratings)

    #put label and buttons on app window
    #myLabel.grid(row=0,column=0)
    op1.place(relx=0.2,rely=0.2)
    op2.place(relx=0.5,rely=0.2)
    op3.place(relx=0.2,rely=0.5)
    op4.place(relx=0.5,rely=0.5)


#open tkinter window
root= Tk()
root.configure(bg="#1c1f08")
#create mainmenu widgets
mainmenu()
#run the mainloop
root.mainloop()



