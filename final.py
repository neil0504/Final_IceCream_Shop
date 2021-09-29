import os
import sqlite3
import tkinter
from tkinter import messagebox

cat_list = []
db_list = []
cat_dict = {}
command_variables = {}
r = 1
value2 = None
index_bufferListBox = None

buf_total = 0
buf_total_cash = 0
buf_total_online = 0

total = 0
total_cash = 0
total_online = 0

name_category_db = "Category_List"
conn_category = sqlite3.connect(f"{name_category_db}.sqlite")
cur_category = conn_category.cursor()

name_BufferList = "BufferList"
# id, name, total, quantity, price, mode, class_name
conn_BufferList = sqlite3.connect(f"{name_BufferList}.sqlite")
cur_BufferList = conn_BufferList.cursor()

name_SoldList = "SoldList"
# id, name, total, quantity, price, mode, discount
conn_SoldList = sqlite3.connect(f"{name_SoldList}.sqlite")
cur_SoldList = conn_SoldList.cursor()

name_WarningList = "WarningList"
# id, name
conn_WarningList = sqlite3.connect(f"{name_WarningList}.sqlite")
cur_WarningList = conn_WarningList.cursor()


def on_select1(event):
    global index_bufferListBox, value2
    box = event.widget
    index_bufferListBox = int(BufferListBox.curselection()[0])
    value2 = box.get(index_bufferListBox),


class Box(tkinter.Listbox):

    def __init__(self, window, **kwargs):
        super().__init__(window, **kwargs)
        self.scrollbar = tkinter.Scrollbar(window, orient=tkinter.VERTICAL, command=self.yview)

    def grid(self, row, column, sticky='nse', rowspan=1, columnspan=1, **kwargs):
        super().grid(row=row, column=column, sticky=sticky, rowspan=rowspan, columnspan=columnspan, **kwargs)
        self.scrollbar.grid(row=row, column=column, sticky='nse', rowspan=rowspan, **kwargs)
        self['yscrollcommand'] = self.scrollbar.set


class CreateButtonFunction:

    def __init__(self, name, db, artificially_created):
        self.name = name
        if os.path.exists(f"{db}.sqlite"):
            self.db_name = db
            # id, name, quantity, price
            self.conn = sqlite3.connect(f"{db}.sqlite")
            self.cur = self.conn.cursor()
            self.value = None

            if not artificially_created:
                cur_category.execute(f"INSERT INTO {name_category_db} (name, cat_name) VALUES(?, ?)", (db, name))
                c = cur_category.connection
                c.commit()

        else:
            print("Not Present")
            add_category()

    def onSelect(self, event):
        box = event.widget
        index_listBox = int(self.list_box.curselection()[0])
        temporary = box.get(index_listBox),
        # t = box.get(index_1),
        self.value = temporary[0].split(" ", 1)[1],

    def b(self):

        def common(mode):
            global buf_total, buf_total_cash, buf_total_online
            if self.value is not None:
                if self.value[0] not in BufferListBox.get(0, tkinter.END):
                    if self.quantity != "":
                        try:
                            q = int(self.quantity.get())
                            price = self.cur.execute("SELECT price from {} where name=?".format(self.name),
                                                     (self.value[0],)).fetchall()[0][0]
                            t = q * price
                            buf_total += t
                            if mode == "Cash":
                                buf_total_cash += t
                                textBufCash.set(buf_total_cash)
                            elif mode == "Online":
                                buf_total_online += t
                                textBufOnline.set(buf_total_online)
                            cur_BufferList.execute(
                                "INSERT INTO {} (name, total, quantity, price, mode, class_name) VALUES(?, ?, "
                                "?, ?, ?, ?)".format(name_BufferList), (self.value[0], t, q, price,
                                                                        mode, "{}_Button_Command".format(self.name)))
                            conn_BufferList.commit()
                            # id_ = cur_BufferList.execute("SELECT id from {} where name=?".format(name_BufferList),
                            #                              (self.value[0],)).fetchall()[0][0]
                            id_ = len(cur_BufferList.execute("SELECT * FROM {}".format(name_BufferList)).fetchall())
                            BufferListBox.insert(tkinter.END, "{}. {}".format(id_, self.value[0]))
                            textBufTotal.set(buf_total)
                            self.quantity.set("")
                            self.value = None

                        except ValueError:
                            pass

        def onlinePay_():
            common("Online")

        def cash():
            common("Cash")

        self.window = tkinter.Tk()
        self.quantity = tkinter.StringVar(self.window)
        self.list_box = Box(self.window)
        self.window.geometry("500x768")
        self.window.title(self.name)
        self.window.columnconfigure(0, weight=2)
        self.window.rowconfigure(1, weight=2)
        tkinter.Label(self.window, text="Items List", font=("Comic Sans MS", 14, "bold"), bg="#b7d477") \
            .grid(row=0, column=0, sticky='nsew', padx=(30, 0))
        self.list_box.grid(row=1, column=0, sticky='nsew', padx=(30, 0), pady=(0, 30))
        self.list_box.bind('<<ListboxSelect>>', self.onSelect)
        self.cur.execute("SELECT * FROM {}".format(self.name))
        items = self.cur.fetchall()
        count = 1
        for item in items:
            self.list_box.insert(tkinter.END, "{}. {}".format(count, item[1]))
            count += 1
        self.ef = tkinter.Frame(self.window)
        self.ef.grid(row=2, column=0)
        tkinter.Label(self.ef, text="Quantity: ", font=("Comic Sans MS", 12, 'italic'), bg="#84c2e7", width=7
                      , anchor="w"). \
            grid(row=0, column=0, sticky='nsw', padx=(30, 0))
        quantity_entry = tkinter.Entry(self.ef, textvariable=self.quantity)
        quantity_entry.grid(row=0, column=1, sticky='nsw', padx=(3, 0))
        self.buttonFrame = tkinter.Frame(self.window)
        self.buttonFrame.grid(row=3, column=0, sticky='nsew')
        tkinter.Button(self.buttonFrame, text="Online Payment", command=onlinePay_,
                       font=("Comic Sans MS", 12, 'italic'),
                       bg="#e5acf1").grid(row=0, column=0, sticky='nsew', padx=(30, 0), pady=(15, 10))
        tkinter.Button(self.buttonFrame, text="Cash Payment", command=cash, font=("Comic Sans MS", 12, 'italic'),
                       bg="#e5acf1") \
            .grid(row=0, column=1, sticky='nsew', padx=(20, 0), pady=(15, 10))
        self.window.mainloop()


def refill_BufferListBox():
    BufferListBox.delete(0, tkinter.END)
    items = cur_BufferList.execute("SELECT * FROM {}".format(name_BufferList)).fetchall()
    print("ALL ITEMS: ", items)
    for item in items:
        index = items.index(item)
        print(index, item[1])
        name = item[1]
        BufferListBox.insert(tkinter.END, "{}. {}".format(index + 1, name))


def create_common_fun():
    def template(name, db, artificially_created):
        global r
        value = f"{name}_Button_Command"
        command_variables[value] = CreateButtonFunction(name, db, artificially_created)
        tkinter.Button(bframe, text=name, command=command_variables[value].b).grid(row=r, column=0)
        r += 1

    return template


def add_category(artificially_create=False, artificial_name=None, artificial_db=None):
    def add_cat(n=None, db=None):
        if not artificially_create:
            if cat_name.get() != "" and cat_database.get() != "":
                n = cat_name.get()
                db = cat_database.get()
                hey(n, db, artificially_create)
                cat_name.set("")
                cat_database.set("")
                window.destroy()
        elif n is not None and db is not None:
            hey(n, db, artificially_create)

    def hey(name, db, artificially_created):
        if name not in cat_list and db not in db_list:
            cat_list.append(name)
            db_list.append(db)
            cat_dict[name] = create_common_fun()
            print(cat_dict[name](name, db, artificially_created))
            messagebox.showinfo(title="Category Added", message="Category has been add Successfully")
        else:
            messagebox.showinfo(title="Category NOT Added", message="Category already EXISTS")
            print("Already in the List")

    if not artificially_create:
        window = tkinter.Tk()
        window.title("add_category")
        cat_name = tkinter.StringVar(window)
        cat_database = tkinter.StringVar(window)
        tkinter.Label(window, text="Category Name: ").grid(row=0, column=0)
        tkinter.Entry(window, textvariable=cat_name).grid(row=0, column=1)
        tkinter.Label(window, text="Database: ").grid(row=1, column=0)
        tkinter.Entry(window, textvariable=cat_database).grid(row=1, column=1)
        tkinter.Button(window, text="OK", command=add_cat).grid(row=2, column=0, sticky='nse')
        window.mainloop()
    else:
        add_cat(artificial_name, artificial_db)


def remove_category():
    def remove():
        if cat_name.get() != "":
            cur_category.execute("SELECT cat_name FROM {}".format(name_category_db))
            all_items = cur_category.fetchall()
            name = cat_name.get()
            # print(all_items)
            # Getting a tuple because all item has the list with all names as  tuple eg: [('IceCream',), ('Ballons',)]
            t = name,
            if t in all_items:
                cur_category.execute("DELETE  FROM {} WHERE cat_name=?".format(name_category_db), (t[0],))
                c = cur_category.connection
                c.commit()
                messagebox.showinfo(title="Remove Category", message="Category has been Removed Successfully")
                response = messagebox.showinfo(title="RESTART", message="RESTART TO CONTINUE")
                # if response == "ok":
                #     os.execl(sys.executable, sys.executable, *sys.argv)
            else:
                messagebox.showinfo(title="Remove Category FAILED", message="Category has not been Removed")

    window = tkinter.Tk()
    window.title("Remove Category")
    cat_name = tkinter.StringVar(window)
    tkinter.Label(window, text="Category Name: ").grid(row=0, column=0)
    tkinter.Entry(window, textvariable=cat_name).grid(row=0, column=1)
    tkinter.Button(window, text="OK", command=remove).grid(row=2, column=0, sticky='nse')


def undo():
    global buf_total, buf_total_cash, buf_total_online
    if BufferListBox.curselection() != ():
        index = BufferListBox.curselection()[0]
        temporary = BufferListBox.get(index),
        value = temporary[0].split(" ", 1)[1],
        # print("Value = ", value[0])
        item_details = \
        cur_BufferList.execute("SELECT * FROM {} WHERE name=?".format(name_BufferList), (value[0],)).fetchall()[0]
        item_total, mode = item_details[2], item_details[5]
        # print(item_total, mode)
        cur_BufferList.execute("DELETE FROM {} WHERE name=?".format(name_BufferList), (value[0],))
        conn_BufferList.commit()
        # print(cur_BufferList.execute("SELECT * FROM {} WHERE name=?".format(name_BufferList), (value[0], )).fetchall())
        buf_total -= item_total
        textBufTotal.set(buf_total)
        if mode == "Cash":
            buf_total_cash -= item_total
            textBufCash.set(buf_total_cash)
        elif mode == "Online":
            buf_total_online -= item_total
            textBufOnline.set(buf_total_online)
        BufferListBox.delete(index)
        refill_BufferListBox()


def add():
    global total, total_cash, total_online, buf_total, buf_total_cash, buf_total_online
    price = None
    if discount.get() != "":
        if discount.get().isnumeric():
            price = int(discount.get())
            percentage = (price * 100) / buf_total
            details.set("{:.2f} % or ₹ {:.2f}".format(percentage, price))
        else:
            numS = ""
            wrong = False

            for i in discount.get():
                if i.isnumeric():
                    numS += i
                elif i == "%":
                    break
                else:
                    wrong = True
                    break

            if not wrong:
                if numS != "":
                    d = int(numS)
                    price = (d * buf_total) / 100
                    details.set(f"{d} % or ₹ {price}")

    else:
        details.set("0 % or ₹ 0")
        price = 0
    print(price)
    if price is not None:
        item_list = cur_BufferList.execute("SELECT * FROM {}".format(name_BufferList)).fetchall()
        length = len(item_list)
        soldListBox_length = len(SoldListBox.get(0, tkinter.END))
        for item in item_list:

            cur_SoldList.execute(
                "INSERT INTO {} (name, total, quantity, price, mode, discount) VALUES(?, ?, ?, ?, ?, ?)".format(
                    name_SoldList), (item[1], item[2], item[3], item[4], item[5], price / length))
            conn_SoldList.commit()
            total += (item[2] - (price / length))
            textTotal.set(total)
            if item[5] == 'Cash':
                total_cash += (item[2] - (price / length))
                textTotalCash.set(total_cash)
            elif item[5] == "Online":
                total_online += (item[2] - (price / length))
                textTotalOnline.set(total_online)
            db_name = command_variables[item[6]].db_name
            print(db_name)
            quan = command_variables[item[6]].cur.execute("SELECT quantity from {} where name=?".format(db_name), (item[1], )).fetchall()[0][0]
            # print(quan)
            print(quan)

            SoldListBox.insert(tkinter.END, "{}. {}".format(soldListBox_length + 1, item[1]))
            soldListBox_length += 1

        cur_BufferList.execute("DELETE FROM {}".format(name_BufferList))
        conn_BufferList.commit()
        buf_total = 0
        buf_total_cash = 0
        buf_total_online = 0
        textBufTotal.set(buf_total)
        textBufCash.set(buf_total_cash)
        textBufOnline.set(buf_total_online)
        BufferListBox.delete(0, tkinter.END)
    l1.grid_forget()
    l2.grid_forget()


def check():
    print(discount.get())
    l1.grid(row=3, column=0, pady=(15, 0))
    l2.grid(row=3, column=1, pady=(15, 0), sticky='w')
    if discount.get() != "":
        if discount.get().isnumeric():
            d = int(discount.get())
            percentage = (d * 100) / buf_total
            details.set("{:.2f} % or ₹ {:.2f}".format(percentage, d))
        else:
            numS = ""
            wrong = False
            for i in discount.get():
                if i.isnumeric():
                    numS += i
                elif i == "%":
                    break
                else:
                    wrong = True
                    break

            if not wrong:
                print(numS)
                if numS != "":
                    d = int(numS)
                    price = (d * buf_total) / 100
                    details.set(f"{d} % or ₹ {price}")

    else:
        details.set("0 % or ₹ 0")

    # details.set("HEY")
    print(details.get())


mainWindow = tkinter.Tk()
mainWindow.title("Sale")
mainWindow.geometry("1366x768")
mainWindow.columnconfigure(0, weight=2)
mainWindow.columnconfigure(1, weight=2)
mainWindow.columnconfigure(2, weight=2)

mainWindow.rowconfigure(2, weight=2)
mainWindow.rowconfigure(3, weight=1)

tkinter.Label(mainWindow, text="SALES", font=("Comic Sans MS", 20, "bold"), bg="#ade1ef") \
    .grid(row=0, column=0, columnspan=5, sticky='nsew', padx=30)
tkinter.Label(mainWindow, text="Category List", font=("Comic Sans MS", 14, "bold"), bg="#b7d477") \
    .grid(row=1, column=0, sticky='nsew', padx=(30, 0))
tkinter.Label(mainWindow, text="Buffer List", font=("Comic Sans MS", 14, "bold"), bg="#b7d477") \
    .grid(row=1, column=1, sticky='nsew', padx=(30, 0))
tkinter.Label(mainWindow, text="Sold List", font=("Comic Sans MS", 14, "bold"), bg="#b7d477") \
    .grid(row=1, column=2, sticky='nsew', padx=(30, 0))
tkinter.Label(mainWindow, text="", font=("Comic Sans MS", 14, "bold")) \
    .grid(row=1, column=3, sticky='nsew', padx=(30, 0))
warningLabel = tkinter.Label(mainWindow, text="Warning List", font=("Comic Sans MS", 14, "bold"), bg="#b7d477") \
    .grid(row=1, column=4, sticky='nsew', padx=30)

bframe = tkinter.Frame(mainWindow)
bframe.grid(row=2, column=0)
# tkinter.Button(bframe, text="HI").grid(row=0, column=0)
tkinter.Button(mainWindow, text="Add Category", command=add_category).grid(row=3, column=0, sticky='nsew')
tkinter.Button(mainWindow, text="Remove Category", command=remove_category).grid(row=4, column=0, sticky='nsew')

BufferListBox = Box(mainWindow)
BufferListBox.grid(row=2, column=1, sticky='nsew', padx=(30, 0), pady=(0, 30))
BufferListBox.config(border=2, relief='sunken')
BufferListBox.bind('<<ListboxSelect>>', on_select1)

SoldListBox = Box(mainWindow)
SoldListBox.grid(row=2, column=2, sticky='nsew', padx=(30, 0), pady=(0, 30))
SoldListBox.config(border=2, relief='sunken')

WarningBox = Box(mainWindow)
WarningBox.grid(row=2, column=4, sticky='nsew', pady=(0, 30), padx=30)
WarningBox.config(border=2, relief='sunken')

bufferButtonFrame = tkinter.Frame(mainWindow)
bufferButtonFrame.grid(row=3, column=1, rowspan=2)

discount = tkinter.StringVar()  # To Read the discount Value
details = tkinter.StringVar()  # To display Discount Details

tkinter.Button(bufferButtonFrame, text="Undo", command=undo, width=15, font=("Comic Sans MS", 12, 'italic', 'bold'),
               bg="#e5acf1").grid(row=0, column=0, sticky='nsew', columnspan=2)

tkinter.Label(bufferButtonFrame, text="Discount: ", font=("Comic Sans MS", 12, 'italic'), bg="#84c2e7", width=7
              , anchor="w").grid(row=1, column=0, pady=(15, 0))
tkinter.Entry(bufferButtonFrame, textvariable=discount).grid(row=1, column=1, sticky='nsew', pady=(15, 0))

tkinter.Button(bufferButtonFrame, text="CHECK", command=check, width=10, font=("Comic Sans MS", 8, 'italic', 'bold'),
               bg="#e5acf1").grid(row=2, column=0, sticky='nse', columnspan=2, pady=(15, 0))

l1 = tkinter.Label(bufferButtonFrame, text="Discount Details: ", font=("Comic Sans MS", 8, 'italic'), bg="#84c2e7",
                   width=12
                   , anchor="w")
l2 = tkinter.Label(bufferButtonFrame, textvariable=details, font=("Comic Sans MS", 8, 'italic'), anchor='w', width=12)
tkinter.Button(bufferButtonFrame, text="Add", command=add, font=("Comic Sans MS", 12, 'italic', 'bold'), bg="#e5acf1") \
    .grid(row=4, column=0, sticky='nsew', pady=(15, 10), columnspan=2)
discount.set(0)

displayFrame = tkinter.Frame(mainWindow)
displayFrame.grid(row=1, column=3, rowspan=2, sticky='nsew', padx=(30, 0), pady=(0, 10))

tkinter.Label(displayFrame, text="Temp Total", font=("Comic Sans MS", 10, 'italic'), bg="#fbbbb2", width=12) \
    .grid(row=0, column=0, pady=(5, 0))
lf1 = tkinter.Frame(displayFrame)
lf1.grid(row=3, column=0)
tkinter.Label(lf1, text="Temp Cash", font=("Comic Sans MS", 10, 'italic'), bg="#fbbbb2", width=12) \
    .grid(row=0, column=0, pady=(5, 0))
tkinter.Label(lf1, text="Temp Online", font=("Comic Sans MS", 10, 'italic'), bg="#fbbbb2", width=12) \
    .grid(row=0, column=1, pady=(5, 0), padx=(3, 0))
tkinter.Label(displayFrame, text="Total", font=("Comic Sans MS", 10, 'italic'), width=12, bg="#9ffc39") \
    .grid(row=4, column=0, pady=(20, 0))
lf2 = tkinter.Frame(displayFrame)
lf2.grid(row=6, column=0)
tkinter.Label(lf2, text="Total Cash", font=("Comic Sans MS", 10, 'italic'), width=12, bg="#9ffc39") \
    .grid(row=0, column=0, pady=(5, 0))
tkinter.Label(lf2, text="Total Online", font=("Comic Sans MS", 10, 'italic'), width=12, bg="#9ffc39") \
    .grid(row=0, column=1, pady=(5, 0), padx=(3, 0))
tkinter.Label(displayFrame, text="Total for added Quantity", font=("Comic Sans MS", 10, 'italic'), width=19,
              bg="#fe814b").grid(row=12, column=0, pady=(20, 0))
lf = tkinter.Frame(displayFrame)
lf.grid(row=14, column=0)
tkinter.Label(lf, text="Added - Cash", font=("Comic Sans MS", 10, 'italic'), width=12, bg="#fe814b") \
    .grid(row=0, column=0, pady=(5, 0))
tkinter.Label(lf, text="Added - Online", font=("Comic Sans MS", 10, 'italic'), width=12, bg="#fe814b") \
    .grid(row=0, column=1, padx=(3, 0), pady=(5, 0))

textBufTotal = tkinter.StringVar()
textBufCash = tkinter.StringVar()
textBufOnline = tkinter.StringVar()
textTotal = tkinter.StringVar()
textTotalCash = tkinter.StringVar()
textTotalOnline = tkinter.StringVar()
textTotalAddedQuantity = tkinter.StringVar()
textTotalAddedQuantity_cash = tkinter.StringVar()
textTotalAddedQuantity_online = tkinter.StringVar()

tkinter.Label(displayFrame, textvariable=textBufTotal, borderwidth=3, relief="raised", width=15).grid(row=1, column=0)
tkinter.Label(lf1, textvariable=textBufCash, borderwidth=3, relief="raised", width=8).grid(row=1, column=0)
tkinter.Label(lf1, textvariable=textBufOnline, borderwidth=3, relief="raised", width=8).grid(row=1, column=1,
                                                                                             padx=(3, 0))
tkinter.Label(displayFrame, textvariable=textTotal, borderwidth=3, relief="raised", width=15).grid(row=5, column=0)
tkinter.Label(lf2, textvariable=textTotalCash, borderwidth=3, relief="raised", width=8).grid(row=1, column=0)
tkinter.Label(lf2, textvariable=textTotalOnline, borderwidth=3, relief="raised", width=8) \
    .grid(row=1, column=1, padx=(3, 0))
tkinter.Label(displayFrame, textvariable=textTotalAddedQuantity, borderwidth=3, relief="raised", width=15) \
    .grid(row=13, column=0)
tkinter.Label(lf, textvariable=textTotalAddedQuantity_cash, borderwidth=3, relief="raised", width=8) \
    .grid(row=1, column=0)
tkinter.Label(lf, textvariable=textTotalAddedQuantity_online, borderwidth=3, relief="raised", width=8) \
    .grid(row=1, column=1, padx=(3, 0))

textBufTotal.set(0.0)
textBufCash.set(0.0)
textBufOnline.set(0.0)
textTotal.set(0.0)
textTotalCash.set(0.0)
textTotalOnline.set(0.0)
textTotalAddedQuantity.set(0.0)
textTotalAddedQuantity_cash.set(0.0)
textTotalAddedQuantity_online.set(0.0)

cur_category.execute("SELECT * FROM {}".format(name_category_db))
temp = cur_category.fetchall()
if temp:
    for item in temp:
        add_category(True, item[1], item[2])

temp = cur_SoldList.execute("SELECT * FROM {}".format(name_SoldList)).fetchall()
if temp:
    for item in temp:
        SoldListBox.insert(tkinter.END, "{}. {}".format(temp.index(item) + 1, item[1]))
        total += (item[2] - item[6])
        if item[5] == "Cash":
            total_cash += (item[2] - item[6])
        elif item[5] == "Online":
            total_online += (item[2] - item[6])

    textTotal.set(total)
    textTotalCash.set(total_cash)
    textTotalOnline.set(total_online)

temp = cur_BufferList.execute("SELECT * FROM {}".format(name_BufferList)).fetchall()
if temp:
    for item in temp:
        BufferListBox.insert(tkinter.END, "{}. {}".format(temp.index(item) + 1, item[1]))
        buf_total += (item[2])
        if item[5] == "Cash":
            buf_total_cash += (item[2])
        elif item[5] == "Online":
            buf_total_online += (item[2])

    textBufTotal.set(buf_total)
    textBufCash.set(buf_total_cash)
    textBufOnline.set(buf_total_online)

temp = cur_WarningList.execute("SELECT * FROM {}".format(name_WarningList)).fetchall()
if temp:
    for item in temp:
        WarningBox.insert(tkinter.END, "{}. {}".format(temp.index(item) + 1, item[1]))

mainWindow.mainloop()