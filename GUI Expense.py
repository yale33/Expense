# GUIBasic2-Expense.py
from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import *
import csv
import datetime

# ttk is theme of Tk

GUI = Tk()
GUI.title('โปรแกรมบันทึกค่าใช้จ่าย by Yale')
GUI.geometry('700x580+350+20')

############MENU###############
menubar = Menu(GUI)
GUI.config(menu=menubar)

# File menu
filemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='File',menu=filemenu)
filemenu.add_command(label='Import CSV')
filemenu.add_command(label='Export to Googlesheet')

# Help
def About():
    messagebox.showinfo('About','โปรแกรมบันทึกข้อมูลค่าใช้จ่ายจัดทำขึ้นเพื่อจัดระเบียบการเงิน\nติดต่อเจ้าของโปรแกรมได้ที่เมลล์ lm_jelly@hotmail.com')
helpmenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Help',menu=helpmenu)
helpmenu.add_command(label='About', command=About)
###########################

'''
style = ttk.Style()
style.theme_create( "MyStyle", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
        "TNotebook.Tab": {"configure": {"padding": [50, 20] },}})

style.theme_use("MyStyle")
'''

Tab = ttk.Notebook(GUI)

T1 = Frame(Tab)
T2 = Frame(Tab)
Tab.pack(fill=BOTH, expand=1)

expenseicon = PhotoImage(file='expense.png')
listicon = PhotoImage(file='list.png')


'''
# f'{"tab short": ^50s}
# f'{"tab longgggggggggg": ^50s}'

https://stackoverflow.com/questions/8450472/how-to-print-a-string-at-a-fixed-width
https://docs.python.org/3/whatsnew/3.6.html#whatsnew36-pep498
>>> f'{"HELLO": <{20}}'
'HELLO               '
>>> f'{"HELLO": >{20}}'
'               HELLO'
>>> f'{"HELLO": ^{20}}'
'       HELLO        '
'''

Tab.add(T1, text=f'{"Add Expense": ^50s}', image=expenseicon,compound='top')
Tab.add(T2, text=f'{"Expense List": ^50s}', image=listicon,compound='top')
#Tab.add(T2, text='Expense List', image=listicon,compound='top')

# B1 = Button(GUI,text='Hello')
# B1.pack(ipadx=50,ipady=20) #.pack() ติดปุ่มเข้ากับ GUI หลัก
 
F1 = Frame(T1)
#F1.place(x=140,y=10)
F1.pack()

today = datetime.date.today()

cal = Calendar(F1, selectmode='day',background='cadetblue',selectbackground ='slategrey',
                    foreground='white', cursor="plus",year=today.year, month=today.month, day=today.day)
cal.pack(padx=0,pady=15)

days = {'Mon':'จันทร์',
        'Tue':'อังคาร',
        'Wed':'พุธ',
        'Thu':'พฤหัสบดี',
        'Fri':'ศุกร์',
        'Sat':'เสาร์',
        'Sun':'อาทิตย์'}

def Save(event=None):
    date =  cal.selection_get()
    date = str(date)
    expense = v_expense.get()
    price = v_price.get()
    quantity = v_quantity.get()

    if expense == '': #or price == '' or quantity =='':
      messagebox.showwarning('Error','กรุณากรอกรายการค่าใช้จ่าย')
      #print('Not completed Info')
      #messagebox.showwarning('Error','กรุณากรอกข้อมูลให้ครบ')
      return
    elif price == '':
      messagebox.showwarning('Error','กรุณากรอกราคา')
      return
    elif quantity == '':
      quantity = 1
      #messagebox.showwarning('Error','กรุณากรอกจำนวน') 
      

    try:
        total = int(price) * int(quantity)
        # .get() คือดึงค่ามาจาก v_expense = StringVar()
        print('รายการ: {} ราคา: {}'.format(expense,price))
        print('จำนวน: {} รวมทั้งหมด: {} บาท'.format(quantity,total))
        text = 'รายการ: {} ราคา: {} บาท '.format(expense,price)        #\n เป็นการขึ้นบรรทัดใหม่
        text = date + '\n'+ text + 'จำนวน: {} รายการ  รวมทั้งหมด: {} บาท'.format(quantity,total)
        v_result.set(text)

        # clear ข้อมูลเก่า
        v_expense.set('')
        v_price.set('')
        v_quantity.set('')

        # บันทึกข้อมูลลง csv อย่าลืม import csv ด้วย
        from datetime import datetime

        today = datetime.now().strftime('%a') # days['Mon'] = 'จันทร์' #%a Abbreviated weekday name.   Sun, Mon, ...
        print(today)
        stamp = datetime.now()
        dt = stamp.strftime('%Y-%m-%d %H:%M')
        transactionid = stamp.strftime('%Y%m%d%H%M%f')      # %f หน่วยเป็น Microsecond เพื่อป้องกันการซ้ำกัน
        dt = days[today] + '-' + dt
        with open('savedata6.csv','a',encoding='utf-8',newline='') as f:
            # with คือสั่งเปิดไฟล์แล้วปิดอัตโนมัติ
            # 'a' การบันทึกเรื่อยๆ เพิ่มข้อมูลต่อจากข้อมูลเก่า
            # newline='' ทำให้ข้อมูลไม่มีบรรทัดว่าง
            fw = csv.writer(f) #สร้างฟังชั่นสำหรับเขียนข้อมูล
            data = [transactionid,date,expense,price,quantity,total,dt]
            fw.writerow(data)

        # ทำให้เคอเซอร์กลับไปตำแหน่งช่องกรอก E1
        E1.focus()
        update_table()
    except Exception as e: #(เป็น technique การดูว่า error ตรงไหน)
        #print(e)
        print("ERROR",e)
        messagebox.showwarning ('Error','ระบุแค่ตัวเลขเท่านั้น ไม่ต้องระบุหน่วย')
        #messagebox.showerror('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
        #messagebox.showinfo ('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
        v_expense.set('')
        v_price.set('')
        v_quantity.set('') 
        
        
# ทำให้สามารถกด enter ได้
GUI.bind('<Return>',Save) #ต้องเพิ่มใน def Save(event=None) ด้วย

FONT1 = ("TH SarabunPSK",14) # None เปลี่ยนเป็น 'Angsana New'
FONT2 = ("TH SarabunPSK",22)
FONT3 = ("TH SarabunPSK",18,'bold','underline')

centerimg = PhotoImage(file='wallet.png')
logo = ttk.Label(F1,image=centerimg)
logo.pack()


#------text1--------
L = ttk.Label(F1,text='รายการค่าใช้จ่าย',font=FONT1).pack()
v_expense = StringVar()
# StringVar() คือ ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E1 = ttk.Entry(F1,textvariable=v_expense,font=FONT1,width=40)
E1.pack()
#-------------------

#------text2--------
L = ttk.Label(F1,text='ราคา (บาท)',font=FONT1).pack()
v_price = StringVar()
# StringVar() คือ ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E2 = ttk.Entry(F1,textvariable=v_price,font=FONT1,width=30)
E2.pack()
#-------------------

#------text3--------
L = ttk.Label(F1,text='จำนวน (ชิ้น)',font=FONT1).pack()
v_quantity = StringVar()
# StringVar() คือ ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E3 = ttk.Entry(F1,textvariable=v_quantity,font=FONT1)
E3.pack()
#-------------------

saveicon = PhotoImage(file='save.png')


B2 = ttk.Button(F1,text=f'{"Save": >{6}}',command=Save,image=saveicon,compound='left')
B2.pack(ipadx=30,ipady=10,pady=15)



#F2 = Frame(T2)
#F1.place(x=140,y=10)
#F2.pack()
v_result = StringVar()
#v_result.set('     ผลลัพธ์      ')
result = ttk.Label(F1, textvariable=v_result, font=FONT1,foreground='darkslategrey')
# result = Label(F1, textvariable=v_result, font=FONT1,fg='teal')
result.pack(pady=5)


###########TAB2###########

def read_csv():
    with open('savedata6.csv',newline='',encoding='utf-8') as f:    
    # with open ช่วยให้เปิดและปิดได้เลย (ป้องกันการลืม close ถ้าลืมโปรแกรมจะ error) ไม่ต้องไปใส่ function open และ close ซึ่งต้องทำอีก 2 บรรทัด
        fr = csv.reader(f)      # fr stands for file reader
        data = list(fr)         # ถ้าไม่ใส่ list จะอ่านค่าไม่ออก
    return data                 # ต้องการค่าไปใช้งานต่อ ต้อง return
        # print(data)           # วิธี select แล้ว comment ลัดคือ กด ctrl+/
        # print('----')
        # print(data[0][0])
        # for d in data:
        #   print(d)
        # for a,b,c,d,e,f in data:
        #     print(b)

# def update_record():
#     getdata = read_csv()
#     v_allrecord.set('') 
#     text = ''
#     for d in getdata:
#         txt = '{}--{}--{}--{}--{}--{}\n'.format(d[0],d[1],d[2],d[3],d[4],d[5])
#         text = text+txt
#     v_allrecord.set(text)



# v_allrecord = StringVar()
# v_allrecord.set('----All Record----')
# Allrecord = ttk.Label(T2,textvariable=v_allrecord,font=FONT1,foreground='teal')
# Allrecord.pack()

# table

L = ttk.Label(T2,text='ตารางแสดงผลลัพธ์',font=FONT3, foreground='teal').pack(pady=20)
header = ['เลขที่รายการ','วันทำรายการ','รายการ','ค่าใช้จ่าย','จำนวน','รวม','วันที่บันทึกข้อมูล']
result_table = ttk.Treeview(T2, columns=header,show='headings',height=15)   # height เพิ่มความสูงของ table
result_table.pack()

# สร้าง ชื่อใน header ทำได้ 2 วิธี
# for i in range(len(header)):
#     result_table.heading(header[i],text=header[i])

for h in header:  
    result_table.heading(h,text=h)

headerwidth = [120,70,70,60,50,60,140]    #ตั้งค่าขนาดคอลัมภ์
for h,w in zip(header,headerwidth):
    result_table.column(h,width = w)

# result_table.insert('','end',value=['จันทร์','น้ำดื่ม',33,4,132]

alltransaction = {}  

def UpdateCSV():
    with open('savedata6.csv','w',newline='',encoding='utf-8') as f:    
        fw = csv.writer(f)      # fw = file writer
        # เตรียมข้อมูลจาก alltransaction ให้กลายเป็น list
        data = list(alltransaction.values())
        fw.writerows(data)       # multiple line from nested list [[],[],[]]
        print('Table was updated')
        

def DeleteRecord(event=None):
    check = messagebox.askyesno('Confirm?',"Are you sure to delete data?")
    #print('yes/no:',check)

    if check == True:
        select = result_table.selection()
        # print(select)
        data = result_table.item(select)
        data = data['values']
        transactionid = data[0]
        # print(transactionid)
        del alltransaction[str(transactionid)]
        UpdateCSV()
        update_table()
    else:
        print('cancel')

    
B_Delete = ttk.Button(T2,text=f'{"Delete": >{6}}',width=30, command=DeleteRecord)
B_Delete.place(x=250,y=450)

result_table.bind('<Delete>',DeleteRecord)

def update_table():
    result_table.delete(*result_table.get_children())   # ล้างค่าทุกครั้งก่อน อ่านค่าใหม่ *เทียบเท่า run for loop แบบไม่เอา ''
    # for c in result_table.get_children() :            # หรือใช้วิธี for loop ก็ได้
    #     result_table.delete(c)

    try:                                        # ใส่ try, except ให้ read csv แต่ถ้าไม่ได้ ก็ไม่เป็นไร (กรณีไม่มีข้อมูลตั้งแต่แรก) ไม่ error
        data = read_csv()
        for d in data:
            alltransaction[d[0]] = d    # d[0] = transactionID
            result_table.insert('',0,value=d)   # 0 หมายถึง ข้อมูลล่าสุดอยู่บนสุด 'end' หมายถึง ข้อมูลไล่ตามลำดับ
        print(alltransaction)

        # ตย result จาก print(alltransaction) {'202106072025833709': ['202106072025833709', '2021-06-07', 'ค่าเดินทาง', '30', '1', '30', 'จันทร์-2021-06-07 20:25'], ...
    except:
        print('No File') 

update_table()

GUI.bind('<Tab>',lambda x: E2.focus())   
GUI.mainloop()
