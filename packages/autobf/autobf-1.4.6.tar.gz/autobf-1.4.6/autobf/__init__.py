import numpy as np
import pyautogui
import pydirectinput
import time
# import keyboard
import cv2
import pygetwindow as gw
Xc=int(1920/2)
Yc=int(1080/2)
import threading
timeUp = False
def _timer(hours, minutes=0, seconds=0):
    global timeUp
    total_seconds = hours * 3600 + minutes * 60 + seconds
    while total_seconds:
        hrs, remainder = divmod(total_seconds, 3600)
        mins, secs = divmod(remainder, 60)
        print(f"{hrs:02d}:{mins:02d}:{secs:02d}", end="\r")
        time.sleep(1)
        total_seconds -= 1
    print("時間到！")
    timeUp = True
    
def timerStart(hours, minutes=0, seconds=0):
    global timeUp
    timeUp = False
    timeThread=threading.Thread(target=_timer,args=(hours,minutes,seconds,))
    timeThread.start()
 
def get_window_size(title='Roblox'):
    '''
    獲取所有符合標題的視窗
    '''
    windows = gw.getWindowsWithTitle(title)
    if not windows:
        print(f"找不到標題為 '{title}' 的視窗。")
        return
    for window in windows:
        if window.title == title:
            width, height = window.width, window.height
            print(f"視窗 '{window.title}' 的大小為: {width}x{height}")
            return width, height

def setCenterXY(x=639,y=530):#預設值為螢幕左大右小
    Xc=x;Yc=y
    
def row(x,y,dx=0,dy=0,button='right',delay=0.2):
    '''
    在 (x,y) 處，按下滑鼠 button 鍵後拖曳 dx,dy
    '''
    pydirectinput.mouseDown(x,y,button=button);time.sleep(delay)
    pydirectinput.moveTo(x+dx,y+dy);    time.sleep(delay)
    pydirectinput.mouseUp(button=button)

def zoom(scroll=-200,repeat=1):
    '''
    使用滑鼠滾輪縮放
    scroll:捲動方向 正值為往前捲，負值為往後捲
    repeat:重覆捲動次數
    '''
    for i in range(repeat):    pyautogui.scroll(scroll)
    
def zoom2max(scroll=-500,repeat=10,dy=100):
    '''
    拉最遠並把視角放到頭頂
    '''
    global Xc,Yc
    for i in range(repeat):    pyautogui.scroll(scroll)
    row(Xc,Yc,dy=dy)
#     row(Xc,Yc,dy=50)
def checkAndClick(x,y,color,tolorance=30,double=False):
    pydirectinput.moveTo(x,y)
    while True:
        a=np.array(pyautogui.pixel(x,y))
        dist = np.linalg.norm(a-np.array(color), axis=-1)
        if dist<=tolorance:
            print(f"於({x},{y})執行點擊，dist={dist}")
            break
    if double: pydirectinput.doubleClick()
    else:      pydirectinput.click()
    
def click(x=None,y=None,repeat=1,delay=0):
    '''
    點擊 x,y 重複 repeat 次，每次延遲 delay 秒
    '''
    try:
        if x==None:
            for i in range(repeat):pydirectinput.click();time.sleep(delay)
        else:
            for i in range(repeat):pydirectinput.click(x,y);pydirectinput.click(x+1,y+1);time.sleep(delay)
    except:print("except while click()...")
    
def slide(key='down',repeat=1):
    '''
    按q滑行，由 key 指定方向， 重複repeat次
    '''
    for i in range(repeat):
        pydirectinput.keyDown(key)
        pydirectinput.press('q')
        pydirectinput.keyUp(key)
        
def jumpSlide(key,j_repeat,s_repeat):
    '''
    跳躍滑行
    '''
    press('space',j_repeat)
    slide(key,s_repeat)
    
def keyDown(key,duration=2):
    '''
    按下 key , 等待 duration 秒後放開
    '''
    pydirectinput.keyDown(key);time.sleep(duration);pydirectinput.keyUp(key)
    
def press(key,repeat=1,delay=0):
    '''
    按 key ，重覆repeat次，每次等的delay秒
    '''
    for i in range(repeat):pydirectinput.press(key);time.sleep(delay)
    
def reset(delay=8):
    '''
    重設色角色 esc + r + enter
    '''
    pydirectinput.press('esc');time.sleep(1)
    pydirectinput.press('r');time.sleep(1)
    pydirectinput.press('enter')
    time.sleep(delay)
    
def findColorsYX(color,tolorance=0,image=[]):
    '''
    給定 image ，在上面找到和 color 相近顏色的座標
    並回傳座標陣列[(y1,x1),(y2,x2)...]，tolorance 為容忍範圍
    '''
    if len(image)==0:image = pyautogui.screenshot()
    image=np.array(image)
    a=np.array(image)
    b=np.array(color)
    dist = np.linalg.norm(a-b, axis=-1)
    return np.argwhere(dist <= tolorance)

def checkColorByXY(x,y,color=(241,234,41),
                   color_tolorance=25,
                   XY_tolorance=8,image=[]):
    '''
    找出螢幕上所有顏色類似 color 的像素所在位置，看是否有接近 (x,y) 的
    若有則回傳真
    '''
    if len(image)==0:image = pyautogui.screenshot()
    image=np.array(image)
    a=findColorsYX(color,color_tolorance,image)
#     print(a)
    if len(a)>0:
        dist = np.linalg.norm(a-np.array([y,x]), axis=-1)
#         print("===============")
#         print(dist)
        ps = np.argwhere(dist <= XY_tolorance)
#         print("===============")
#         print(a[ps])
        if len(ps)>0:return True
        else :return False
    return False
    
def findColorsInSizeYX(color,tolorance=0,size=300,image=[]):
    '''
    給定 image ，在上面找到和 color 相近顏色的座標
    [(y1,x1),(y2,x2)...]
    並回傳座標陣列，tolorance 為容忍範圍
    size為上下左右搜與範圍
    '''
    global Xc,Yc
    if len(image)==0:image = pyautogui.screenshot()
    image=np.array(image)
    a=image[Yc-size:Yc+size,Xc-size:Xc+size]
    b=np.array(color)
    dist = np.linalg.norm(a-b, axis=-1)
    base = np.array([Yc-size,Xc-size])
    ret = np.argwhere(dist <= tolorance) + base
    return ret



def findNearestColor(color,tolorance=0,LOW=0):
    '''
    找到離角色(螢幕中心)最近的指定顏色 color
    LOW:距離下限
    '''
    global Xc,Yc
    a = findColorsYX(color,tolorance=tolorance)
    if len(a)>0:
        b = np.array([Yc,Xc])
        dist=np.linalg.norm(a-b,axis=-1)
        a=a[np.argwhere(dist>LOW)]
        if len(a)>0:
            i = np.argmin(np.linalg.norm(a-b,axis=-1))
            y,x=a[i][0]
            return x,y
    return -1,-1

def instinctOn(p1=(932,902),p2=(985,910)):
    '''
    檢查是否開啟見聞色，落未開啟啟見聞色就按下e開啟它
    '''
    img = np.array(pyautogui.screenshot())
    L,T=p1
    R,B=p2
    ps=findColorsYX((124, 216, 239),30,img[T:B,L:R])
    if len(ps)<10:press('e')
    
def switchOn(switch='1'):
    '''
    檢查若技能未開啟則開啟它
    1: (x,y)=(861,962),pixel=(129, 226, 247)
    2: (x,y)=(929,962),pixel=(129, 225, 246)
    3: (x,y)=(991,962),pixel=(130, 226, 248)
    4: (x,y)=(1055,962),pixel=(130, 226, 248)
    j: (x,y)=(903,907),pixel=(133, 232, 254)
    e: (x,y)=(960,906),pixel=(127, 222, 243)
    r: (x,y)=(1014,906),pixel=(127, 222, 243)
    '''
    XYs={'1':(861,962),'2':(929,962),
         '3':(991,962),'4':(1055,962),
         'j':(903,907),'e':(960,906),'r':(1014,906)}
    x,y=XYs[switch]
    check=checkColorByXY(x,y,color=(130, 227, 249),
                         color_tolorance=30,XY_tolorance=2)
    if not check:press(switch) ;return True
    return False
   
def getMission(mission=1,baseX=1400,baseY=510,dy=50):
    '''
    取得任務
    mission=1,2,3...
    baseX,basY :任務1所在座標
    dy：往下一個任務的y位移值
    '''
    global Xc,Yc
    click(Xc,Yc,delay=2)
    click(baseX,baseY+dy*(mission-1));time.sleep(2)
#     click(1448,562);time.sleep(2)
    row(Xc,Yc)
    click(baseX,baseY);time.sleep(2)
    click(baseX,baseY);time.sleep(2)
    
def aimEnemy(LOW=0):
    '''
    在見聞色下找到最近的敵人(紅色)瞄準一下
    LOW：可以瞄準的最短距離，此值越大可以瞄準越遠的敵人
    '''
    x,y = findNearestColor((255,0,0),LOW=LOW)
    if x>0:
        print(f'瞄準：{x},{y}',)
        row(x,y,dy=-1,delay=0)
        row(x,y,dy=1,delay=0)
#         click(x,y);
        return True
    return False

def shotEnemy(a='4',b='',c='1'):
    '''
    在見聞色下找到最近的敵人
    開 a 欄位做射擊,a='1'or'2'or'3'or'4'
    使用 b 招,     b='z'or'x'or'c'or'v'
    切換回 c 欄位   c='1'or'2'or'3'or'4'
    '''
    x,y = findNearestColor((255,0,0))
    if x>0:
        print(f'射擊：{x},{y}',)
        if a!='':press(a);
        row(x,y,dy=1,delay=0)
        click(x,y);
        if b!='':press(b)
        if c!='':press(c)
        return True
    return False

def isComplete(targetImgPath='goal.png',p1=(740,596)):
    '''
    檢查螢幕中是否有 goal.png 來判斷任務是否完成
    若任務已完成就開啟邏盤，p1為縮小對話框的座標
    '''
    try:
        x,y=pyautogui.locateCenterOnScreen(targetImgPath,confidence=0.92)
        click(x,y,delay=1)
        click(p1[0],p1[1])
        print('mission complete!')
        return True
    except:return False
    
def close2Color(color=(241, 234, 41),size=300,tolorance=25,
                distTH=13,
                offsetX=0,offsetY=45):
    '''
    以角色為中心搜與方圓 size內的指定顏色(color)
    並接近指定顏色所在位置
    tolorance：顏色容忍值
    distTH：距離容忍值
    offsetX:X方向偏移值
    offsetY:Y方向偏移值
    '''
    global Xc,Yc
    while True:
        ps=findColorsInSizeYX(color,tolorance=tolorance,size=size)
        if(len(ps)>0):
            y,x=ps[0]
            y+=offsetY
            x+=offsetX
            print(f'接近目標顏色{color} 位置：({x},{y})')
            if x>Xc+distTH:press('d')
            elif x<Xc-distTH:press('a')
            elif y>Yc+distTH:press('s')
            elif y<Yc-distTH:press('w')
            else:break
        else:print(f'找不到指定顏定{color}');break
        
def getXYDist(x,y,color):#1590,918
    '''
    於(x,y)處的顏色和目標顏色的差異
    '''
    pix = np.array(pyautogui.pixel(x,y))
    dist = np.linalg.norm(pix-np.array(color),axis=-1)
    print(f"於({x},{y})處 pix={pix}和目標顏色{color}距離={dist}")
    return dist

def buyRandomFruit():
    '''
    買隨機水果，定位點可能需要調整
    '''
    click(Xc,Yc)
    print(Xc,Yc)
    time.sleep(1)
    check=checkColorByXY(1150,505,color=(255, 255, 255))
    if check:
        print('OK')
        row(1150,505)
        click(1150,505)
        time.sleep(1.5)
        click(1150,505)
        time.sleep(1.5)
        click(1150,505)
        time.sleep(1)
        check=checkColorByXY(573,579,color=(255, 255, 255))
        if check:
            print('時間未到')
            return False
        click(1150,505)
        return True
    return False

def putDownFruit():
    '''
    放下水果，，定位點可能需要調整
    '''
    press('5')
    time.sleep(1)
    click(Xc,Yc)
    time.sleep(1)
    row(1176,565)
    time.sleep(1)
    click(1176,565)
    time.sleep(1)
    click(1176,565)
#1176,565,color=(255, 255, 255)

def storeFruit():
    '''
    儲存水果，定位點可能需要調整
    '''
    press('5')
    time.sleep(1)
    click(Xc,Yc)
    time.sleep(1)
    row(1157,633)
    click(1157,633)
    time.sleep(1)
    click(Xc,Yc)
    #check if fruit repeat
    check=checkColorByXY(1173,683,color=(255, 255, 255))
    if check:
        row(1173,683);
        click()
        putDownFruit()        
def quitJob():
    '''
    放棄目前任務，定位點可能需要調整
    '''
#     237,496,color=(255, 255, 255)
    click(237,496)
    time.sleep(1)
    click(455,587)
    time.sleep(1)
    click(455,587)
    
def homePoint(x=83,y=458,delay=8):
    '''
    按下home point (x,y) 並等待 delay 秒
    '''
    check = checkColorByXY(x,y,(255,255,255))
    if not check: print("can't find home point. Is (x,y) correct?")
    else:
        click(x,y)
        for i in range(delay):
            print('wait for ',delay-i, 'sec')
            time.sleep(1)
        return True
    return False
# checkAndClick(1819,921,color=(222, 66, 45))
#=============================================        
# def goEnemy():
#     global isGetMission
#     zoom2max()
#     if checkColorByXY(x=553,y=656):
#         #背對問號
#         keyDown('left',0.5)
#         slide('w',2);slide('a',2)
#         close2Color(color=(241, 234, 41))
#         if isGetMission:getMission(p1=(1400,510))
#         isGetMission = False
#         slide('d',5)
#         slide('s',12)
#     else:
#         #面向問號
#         slide('w',4);slide('d',1)
#         if checkColorByXY(x=1124,y=93):
#             slide('w',3);slide('d',1)
#             close2Color(color=(241, 234, 41))
#             getMission(p1=(1400,510))
#             print('1')
#             slide('a',5);slide('s',3);slide('a',9)
#         elif checkColorByXY(x=1132,y=96):
#             slide('w',3);slide('d',1)
#             close2Color(color=(241, 234, 41))
#             getMission(p1=(1400,510))
#             print('2')
#             slide('a',5);slide('s',2);slide('a',8)
#         else:
#             close2Color(color=(241, 234, 41))
#             getMission(p1=(1400,510))
#             slide('a',12)
#             slide('w',2)
#             print('3')
# 
# 
# def fight():
#     for i in range(33):
#         print('fight:',i)
#         instinctOn()
#         time.sleep(0.6)
#         shotEnemy(a='', b='v', c='')
#         if aimEnemy():
#             if getXYDist(1590,918,(180,180,180))>50:
#                 press('v')
#             else:press('4');click();press('2')
#         press('e')
#         for j in range(150):click()
#         if isComplete(targetImgPath='goal.png', p1=(740,596)):
#             return True
#     return False
#     
# isGetMission = False
# def work():
#     global isGetMission
#     while True:
#         reset()
#         if getXYDist(925,962,(131, 226, 247))>30:press('2')
#         goEnemy()
#         isGetMission = fight()
        
        
# if __name__ == '__main__':
#     
#     click(Xc,Yc)
#     work()

