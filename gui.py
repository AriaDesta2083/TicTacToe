# https://github.com/AriaDesta2083/TicTacToe.git
from tkinter import *
from tictactoe import *
from pathlib import Path
from tkinter import messagebox
import pygame

#! Assets
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")
# print(__file__)
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

blueC = "#2A0944"
yellowC = "#FEC260"
redC = "#A10035"
greenC = "#3FA796"
mulai = False
mp = False
bermain =  False
music = True

#!Initial Tkinter
mygui = Tk()
screen_width = mygui.winfo_screenwidth()
screen_height = mygui.winfo_screenheight()
window_width = 960
window_height = 540
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
mygui.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
mygui.title(" Aria Desta Prabu ")
mygui.configure(background=blueC)

#! Background 
frameCnt = 15
fire = [PhotoImage(file=relative_to_assets('bg_fire.gif'),format = 'gif -index %i' %(i)) for i in range(frameCnt)]
canvas = Canvas(
    mygui, bg=blueC, height=window_height, width=window_width, bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)

def updateGIF(ind):
    frame = fire[ind]
    ind += 1
    if ind == frameCnt:
        ind = 0
    bg_fire.configure(image=frame,background=blueC,bg=blueC,relief='flat',border=0)
    bg_fire1.configure(image=frame,background=blueC,bg=blueC,relief='flat',border=0)
    bg_fire2.configure(image=frame,background=blueC,bg=blueC,relief='flat',border=0)
    bg_fire3.configure(image=frame,background=blueC,bg=blueC,relief='flat',border=0)
    mygui.after(100, updateGIF, ind)

bg_fire = Label(mygui)
bg_fire1 = Label(mygui)
bg_fire2 = Label(mygui)
bg_fire3 = Label(mygui)
bg_fire.place(x=0,y=540-110,height=140)
bg_fire1.place(x=280,y=540-110,height=140)
bg_fire2.place(x=560,y=540-110,height=140)
bg_fire3.place(x=840,y=540-110,height=140)
mygui.after(0, updateGIF, 0)
mygui.resizable(False,False)


#! Items Game

def BgBoard():
        return Label(
        mygui,
        bg=greenC,
        background=greenC,
        activebackground=greenC,
        foreground=greenC,
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
    ).place(x=45, y=70, width=400, height=400)


def Item(x, y, value, item, img="kosong.png",):
    img = value + ".png" if type(value) != int else img
    imgPath = PhotoImage(file=relative_to_assets(img))
    Button(
        mygui,
        bg=greenC,
        background=greenC,
        activebackground=greenC,
        foreground=greenC,
        image=imgPath,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: clickItem(item),
        relief="flat",
    ).place(x=x, y=y, width=100.0, height=100.0)
    return imgPath, item

def Board():
    list = []
    x = 65.0
    y = 90.0
    pad = 130
    for i in range(len(board)):
        if i % 3 == 0:
            if i != 0:  
                y += pad
                x = 65.0
        else:
            x += pad
        list.append(Item(x=x, y=y, value=board[i], item=i))
    return list

def CreateLabel(x,y,text="Create Label", fstyle="SegoeUI", fsize=33, fweight="", bg=blueC, fg="white",)-> Label :
    label = Label(
        mygui, text=text, font=("%s %s %s" % (fstyle, fsize, fweight)), bg=bg, fg=fg
    )
    label.place(x=(x), y=(y))
    return label

def BgMenu():
    return canvas.create_rectangle(522.0,220.0,898.0,417.0,
        outline= redC,width=8)


def BtnPlay():
    button_play = PhotoImage(
        file=relative_to_assets("play.png"))
    play = Button(
        bg = blueC,
        activebackground=blueC,
        image=button_play,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: clickPlay(),
        relief="flat"
    ).place(
        x=580.0,
        y=274.0,
        width=260.0,
        height=40.0
    )
    return button_play, play

def BtnMP():
    button_mp = PhotoImage(
    file=relative_to_assets("multiplayer.png"))
    multiplayer = Button(
        bg = blueC,
        activebackground=blueC,
        image=button_mp,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: clickMP(),
        relief="flat"
    ).place(
        x=580.0,
        y=335.0,
        width=260.0,
        height=40.0
    )
    return button_mp , multiplayer

def BtnAudio():
    global music
    img = PhotoImage(file=relative_to_assets('audio.png')if music is True else relative_to_assets('mute.png'))
    audio = Button(
        background=blueC,
        activebackground= greenC if music is True else redC,
        image=img,
        width=40,
        height=40,
        bd=0.5,
        command=lambda: clickAudio(),
        relief='solid',
    ).place(x=950 - 44,
        y=5,
        )
    return img,audio


#! Controller
def computer_move():
    global computer
    move=-1
    # Jika saya menang, yang lain tidak dihiraukan.
    for i in range(1,10):
        if make_move(board, computer, i, True)[1]:
            move=i
            break
    if move == -1:
       # Jika player menang, lakukan penghadangan.
        for i in range(1,10):
            if make_move(board, player, i, True)[1]:
                move=i
                break
    if move == -1:
        # Mencoba mengambil posisi yang di inginkan.
        for tup in moves:
            for mv in tup:
                if move == -1 and can_move(board, computer, mv):
                    move=mv
                    break
    return make_move(board, computer, move)
    
def space_exist():
    return board.count('X') + board.count('O') == 9

def clickAudio():
    global music
    global output_audio
    music = not music
    if music == False:
        output_audio = BtnAudio()
        pygame.mixer.music.pause()
    else:
        output_audio = BtnAudio()
        pygame.mixer.music.unpause()    

def clickPlay():
    global mulai , bermain , output_btn_play, player, computer
    mulai = not mulai
    if bermain is True:
        print('masih dalam permainan')
    elif bermain is False:
        player , computer = select_char()
        print(player,computer)
        output_btn_play = Char()

def clickMP():
    global mp , bermain , output_btn_mp , player , computer
    mp = not mp
    if bermain is True:
        print('masih dalam permainan')
    elif bermain is False:
        player ,computer = select_char()
        print(player,computer)
        output_btn_mp = Char()

def Char()->Label:
    if mulai is True:
        output_player = CreateLabel(text='\t[ %s ] Player\t\t\n' % (player),fsize=15,x=530.0,y=274.0)
        output_computer = CreateLabel(text='\t[ %s ] Computer\t\t\n' % (computer),fsize=15,x=530.0,y=335.0)
        return output_player,output_computer
    elif mp is True:
        output_player = CreateLabel(text='\t[ %s ] Player 1\t\t\n' % (player),fsize=15,x=530.0,y=274.0)
        output_player2 = CreateLabel(text='\t[ %s ] Player 2\t\t\n' % (computer),fsize=15,x=530.0,y=335.0)
        return output_player,output_player2

def clickItem(value):
    global mulai , bermain , mp
    global output_board
    if mulai is True or mp is True:
        bermain = True
        if mulai is True:
            move = value if value == 'X' or value == 'O' else value+1
            moved, won = make_move(board, player, move)
            if not moved:
                return print('INPUT TIDAK VALID')
            if won:
                output_board = Board()
                return msgPop('Selamat Anda memenangkannya !')
            elif space_exist():
                output_board = Board()
                return msgPop('Hasil seri !\nHebat coba lagi')
            elif computer_move()[1]:
                output_board = Board()
                return msgPop('Anda kalah! \nSilahkan mencoba lagi dan tetap semangat !')
            output_board = Board()
        elif mp is True:
            move = value if value == 'X' or value == 'O' else value+1
            if board.count(computer)<board.count(player):
                moved, won = make_move(board, computer, move)
                if not moved:
                    return print('INPUT TIDAK VALID')
                if won:
                    output_board = Board()
                    return msgPop('Selamat \nPlayer 2 menang !')
                elif space_exist():
                    output_board = Board()
                    return msgPop('Hasil Seri !\nHebat coba lagi')
            else:
                moved, won = make_move(board, player, move)
                if not moved:
                    return print('INPUT TIDAK VALID')
                if won:
                    output_board = Board()
                    return msgPop('Selamat \nPlayer 1 menang !')
                elif space_exist():
                    output_board = Board()
                    return msgPop('Hasil Seri !\nHebat coba lagi')
            output_board = Board()
    else:
        print('Tekan Play')
        return msgPop('Play untuk memulai permainan')
 
def msgPop(msg):
    respose = messagebox.showinfo(title='Tic Tac Toe',message=msg)
    if respose == 'ok':
        restart()

def restart():
    global output_btn_play , output_btn_mp, mulai , bermain ,mp , output_board , board
    board = [i for i in range(0,9)]
    if bermain is True:
        if mulai is True:
            output_btn_play[0].after(30,output_btn_play[0].destroy())
            output_btn_play[1].after(30,output_btn_play[1].destroy())
        elif mp is True:
            output_btn_mp[0].after(30,output_btn_mp[0].destroy())
            output_btn_mp[1].after(30,output_btn_mp[1].destroy())
    mulai = False
    bermain = False
    mp = False
    output_btn_play = BtnPlay()
    output_btn_mp = BtnMP()
    output_board = Board()

pygame.mixer.init()
pygame.mixer.music.load(relative_to_assets('a7xNM.mp3'))
pygame.mixer.music.play(loops=100)
output_bg_board = BgBoard()
output_board = Board()
output_title = CreateLabel(text='Tic Tac Toe',x=584, y=113)
output_menu = BgMenu()
output_btn_play = BtnPlay()
output_btn_mp = BtnMP()
output_audio = BtnAudio()

if __name__ == '__main__':
    mygui.mainloop()