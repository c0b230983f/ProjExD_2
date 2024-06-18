import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1400, 800
sum_mv = [0, 0]
DELTA = {
    pg.K_UP: (0,-5),
    pg.K_DOWN: (0,+5),
    pg.K_LEFT: (-5,0),
    pg.K_RIGHT: (+5,0),
}

HOUGAKU = {

}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct:pg.Rect) -> tuple[bool,bool]:
    """
    引数：こうかとんRect爆弾Rect
    戻り値：タプル（横方向判定結果、縦方向判定結果）
    画面内ならTrue、画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  #横方向判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  #縦方向判定
        tate = False
    return yoko, tate


def main():
    global sum_mv
    muki = 0
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)  #こうかとん
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bb_img = pg.Surface((20,20))  #爆弾 #1辺が20の空のsurfaceを作る
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0,WIDTH),random.randint(0,HEIGHT)
    vx, vy = +5, +5
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)
    bb_img.set_colorkey((0,0,0))
    clock = pg.time.Clock()
    tmr = 0
    #accs = [a for a in range(1,11)]
    #avx = vx*bb_accs[min(tmr//500,9)]
    #bb_img = bb_img[min(tmr//500,9)]


    while True:
        kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):  #衝突判定
            return #ゲームオーバー
        """
        for r in range(1,11):
            bb_img = pg.surface((20*r,20*r))
            pg.draw.circle(bb_img,(255,0,0),(10*r,10*r),10*r)
        """
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        #sum_mv = [0, 0]
        for k,v in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        if sum_mv[0] == -5 and sum_mv[1] == -5:
            muki = -1
        elif sum_mv[0] == 0 and sum_mv[1] == -5:
            kk_img = pg.transform.flip(kk_img, True, False)
            muki = 2
        elif sum_mv[0] == +5 and sum_mv[1] == -5:
            kk_img = pg.transform.flip(kk_img, True, False)
            muki = 1
        elif sum_mv[0] == +5 and sum_mv[1] == 0:
            kk_img = pg.transform.flip(kk_img, True, False)
            muki = 0
        elif sum_mv[0] == +5 and sum_mv[1] == +5:
            kk_img = pg.transform.flip(kk_img, True, False)
            muki = -1
        elif sum_mv[0] == 0 and sum_mv[1] == +5:
            kk_img = pg.transform.flip(kk_img, True, False)
            muki = -2
        elif sum_mv[0] == -5 and sum_mv[1] == +5:
            muki = 2
        elif sum_mv[0] == -5 and sum_mv[1] == 0:
            muki = 0
        elif sum_mv[0] == 0 and sum_mv[1] == 0:
            muki = 0

                

        kk_img = pg.transform.rotozoom(kk_img, muki*45, 1.0)
        screen.blit(kk_img, kk_rct)
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])


        bb_rct.move_ip(vx,vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
