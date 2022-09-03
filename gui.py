import tkinter
from tkinter import messagebox

from illustrator import Illustrator

# メインフレーム
class App(tkinter.Frame):
    def __init__(self, master):
        super().__init__(master)

        # リストボックス
        self.listbox = IllustratorListbox(self)
        self.listbox.grid(column=0, row=0)

        # コントロールフレーム
        controlFrame = tkinter.Frame(self)

        createButton = tkinter.Button(controlFrame, text='新規', command=self.listbox.createButtonPressed)
        editButton = tkinter.Button(controlFrame, text='編集', command=self.listbox.editButtonPressed)
        deleteButton = tkinter.Button(controlFrame, text='削除', command=self.listbox.deleteButtonPressed)
        createButton.pack()
        editButton.pack()
        deleteButton.pack()

        controlFrame.grid(column=1, row=0)
        

# イラストレータ一覧のリストボックス
class IllustratorListbox(tkinter.Listbox):
    def __init__(self, master):
        super().__init__(master)

        self['height'] = 30
        self['width'] = 50
        self['selectmode'] = 'extended'
        self.bind('<Double-Button-1>', self.doubleClicked)

        self.reload()

    # 項目を再読込する
    def reload(self):
        self.delete(0, tkinter.END)
        self.records = []
        for illustrator in Illustrator.getAll():
            self.insert(tkinter.END, illustrator.name)
            self.records.append(illustrator)

    # ダブルクリック
    def doubleClicked(self, event):
        self.editButtonPressed()

    # 新規作成ボタン押下
    def createButtonPressed(self):
        self.editRecord(Illustrator.new())

    # 編集ボタン押下
    def editButtonPressed(self):
        if len(self.curselection()) > 0:
            self.editRecord(self.records[self.curselection()[0]])
    
    # 削除ボタン押下
    def deleteButtonPressed(self):
        if len(self.curselection()) > 0:
            for illustrator in [self.records[i] for i in self.curselection()]:
                if messagebox.askyesno('確認', f'{illustrator.name} を本当に削除しますか？'):
                    illustrator.remove()
        self.reload()

    def editRecord(self, illustrator: Illustrator):
        Editor(self, illustrator, updateEvent=self.reload)

class Editor(tkinter.Toplevel):
    def __init__(self, master, illustrator: Illustrator, updateEvent=None):
        super().__init__(master)

        self.illustrator = illustrator
        self.updateEvent = updateEvent

        # IDフレーム
        idFrame = tkinter.Frame(self)
        tkinter.Label(idFrame, text='ID', width=10).grid(column=0, row=0)
        idEntry = tkinter.Entry(idFrame, state='normal')
        if illustrator.id:
            idEntry.insert('0', illustrator.id)
        idEntry['state'] = 'readonly'
        idEntry.grid(column=1, row=0)
        
        # 名前フレーム
        nameFrame = tkinter.Frame(self)
        tkinter.Label(nameFrame, text='名前', width=10).grid(column=0, row=0)
        self.nameEntry = tkinter.Entry(nameFrame)
        self.nameEntry.insert('0', illustrator.name)
        self.nameEntry.grid(column=1, row=0)

        # ランクフレーム
        rankFrame = tkinter.Frame(self)
        tkinter.Label(rankFrame, text='ランク', width=10).grid(column=0, row=0)
        self.rankEntry = tkinter.Entry(rankFrame)
        self.rankEntry.insert('0', illustrator.rank)
        self.rankEntry.grid(column=1, row=0)

        # 操作フレーム
        controlFrame = tkinter.Frame(self)
        tkinter.Button(controlFrame, text='キャンセル', command=self.destroy).grid(column=0, row=0)
        tkinter.Button(controlFrame, text='削除', command=self.remove).grid(column=1, row=0)
        tkinter.Button(controlFrame, text='決定', command=self.updateRecord).grid(column=2, row=0)

        idFrame.pack()
        nameFrame.pack()
        rankFrame.pack()
        controlFrame.pack()

    # データを削除する
    def remove(self):
        if messagebox.askyesno('確認', f'{self.illustrator.name} を本当に削除しますか？'):
            if self.illustrator.isSaved():
                self.illustrator.remove()
                self.updateEvent()
            self.destroy()
            
    def updateRecord(self):
        self.illustrator.name = self.nameEntry.get()
        self.illustrator.rank = int(self.rankEntry.get())
        self.illustrator.save()
        if self.updateEvent:
            self.updateEvent()
        self.destroy()

if __name__ == '__main__':
    window = tkinter.Tk()
    app = App(window)
    app.pack()

    window.mainloop()