import pygame
from projekt.levels import *  #Kui tekib probleem "unresolved reference või "no module named projekt", siis...
                      #...tuleb see ümber vahetada "from levels import *".
from pygame.locals import *
from time import *

"""
Veel on tegemist pooliku versiooniga.
TODO: Levelid lõpuni teha, teleport_rectid lõpetada
TODO: Mängu alguse ja lõpu pildid ära vahetada/paigutada
"""

def mäng(kiirus, tase):

    class Player(object):

        def __init__(self):
            self.rect = pygame.Rect(20, 20, 10, 10)  #Mängija asukoht ja suurus

        def mängija_liikumine(self, x, y):
            self.rect.x += x
            self.rect.y += y

            if tase == level1:
                if self.rect.x in range(80, 96) and self.rect.y in range(170, 192):
                    self.rect.x = 550
                    self.rect.y = 48
            if tase == level2:
                if self.rect.x in range(112, 136) and self.rect.y in range(448, 464):
                    self.rect.x = 384
                    self.rect.y = 512

            if tase == level4:
                if self.rect.x in range(328, 352) and self.rect.y in range(368, 384):
                    self.rect.x = 350
                    self.rect.y = 470

            for wall in seinad:
                if self.rect.colliderect(wall.rect):
                    if x > 0 or x < 0 or y > 0 or y < 0:  #Kui mängija läheb vastu seina, siis läheb ta tagasi algpositsioonile
                        self.rect.x = self.rect.y = 24    #Tegelikult minnakse algpositisoonile, kui minna "seina sisse"

        def liikumine(self, x, y):
            if x != 0:
                self.mängija_liikumine(x, 0)
            if y != 0:
                self.mängija_liikumine(0, y)

    class Wall(object):

        def __init__(self, pos):
            seinad.append(self)
            self.rect = pygame.Rect(pos[0], pos[1], 16, 16)

    pygame.init()
    pygame.display.set_caption("Labürindimäng")
    screen = pygame.display.set_mode((800, 592))
    clock = pygame.time.Clock()
    seinad = []
    player = Player()

    x = y = 0
    for rida in tase:
        for sein in rida:
            if sein  == "W":
                Wall((x, y))
            if sein == "E":
                end_rect = pygame.Rect(x, y, 16, 16)
            if sein == "A":
                teleport_rect = pygame.Rect(x, y, 16, 16)
            x += 16
        y += 16
        x = 0

    speed = kiirus
    aeg_k_algus = time()

    def kaart():
        screen.fill((255,255,255))
        for wall in seinad:
            pygame.draw.rect(screen, (0, 0, 0), wall.rect)
        pygame.draw.rect(screen, (255, 0, 0), end_rect)
        pygame.draw.rect(screen, (0, 0, 255), player.rect)
        pygame.draw.rect(screen, (0, 255, 0), teleport_rect)
        pygame.display.flip()

    while True:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type is pygame.QUIT:
                quit()
        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            quit()
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            player.liikumine(-speed, 0)
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            player.liikumine(speed, 0)
        if key[pygame.K_UP] or key[pygame.K_w]:
            player.liikumine(0, -speed)
        if key[pygame.K_DOWN] or key[pygame.K_s]:
            player.liikumine(0, speed)

        if tase == level1:
            if player.rect.colliderect(end_rect):
                aeg_k1 = time()
                m = round((aeg_k1 - aeg_k_algus),3)
                print("Tase kestis", m, "sekundit")
                with open("ajad.txt", 'a') as out:
                    out.write("\n")
                    out.write(str(m)+";")
                mäng(speed, level2)
            kaart()

        elif tase == level2:
            if player.rect.colliderect(end_rect):
                aeg_k2 = time()
                m = round((aeg_k2 - aeg_k_algus),3)
                print("Tase kestis", m, "sekundit")
                with open("ajad.txt", 'a') as out:
                    out.write(str(m)+";")
                mäng(speed, level3)
            kaart()

        elif tase == level3:
            if player.rect.colliderect(end_rect):
                aeg_k3 = time()
                m = round((aeg_k3 - aeg_k_algus),3)
                print("Tase kestis", m, "sekundit")
                with open("ajad.txt", 'a') as out:
                    out.write(str(m)+";")
                mäng(speed, level4)
            kaart()

        elif tase == level4:
            if player.rect.colliderect(end_rect):
                aeg_k3 = time()
                m = round((aeg_k3 - aeg_k_algus),3)
                print("Tase kestis", m, "sekundit")
                print("-----LÕPP-----")
                with open("ajad.txt", 'a') as out:
                    out.write(str(m) + '\n')
                lõpp()
            kaart()
        else:
            raise SystemExit

def ekraan(a, b, tekst, d, tekst2, e):
    pygame.init()

    ekraani_pind = pygame.display.set_mode((500, 320))
    pygame.display.set_caption(a)
    pilt = pygame.image.load(b)
    ekraani_pind.blit(pilt, (0,0))

    meie_font = pygame.font.SysFont("Arial", 24)
    teksti_pilt = meie_font.render(tekst, False, (255,255,255))
    ekraani_pind.blit(teksti_pilt, (d, 20))
    teksti_pilt2 = meie_font.render(tekst2, False, (255,255,255))
    ekraani_pind.blit(teksti_pilt2, (e, 50))
    pygame.display.flip()

def startup():
    ekraan("The Maze-Game", "jigsaw.jpg", "Alustamiseks vali sobiv kiirus: 1, 2, 3", 100, "Vajuta SPACE skooride jaoks", 130)

    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
    pygame.mixer.music.load("GoTtheme.mp3")
    pygame.mixer.music.play(loops = 100)
    pygame.mixer.music.set_volume(1.0)

    while True:
        for event in pygame.event.get():
            if event.type is QUIT:
                quit()
            if event.type is KEYDOWN and event.key is K_ESCAPE:
                quit()
            if event.type is KEYDOWN and event.key is K_1:
                mäng(1, level1)
            if event.type is KEYDOWN and event.key is K_2:
                mäng(2, level1)
            if event.type is KEYDOWN and event.key is K_3:
                mäng(3, level1)
            if event.type is KEYDOWN and event.key is K_SPACE:
                ajatabel()

def lõpp():
    ekraan("Victory!","victory.jpg","Jõudsid lõppu", 130, "Vajuta S restarti jaoks", 130)
    while True:
        for event in pygame.event.get():
            if event.type is QUIT:
                quit()
            if event.type is KEYDOWN and event.key is K_ESCAPE:
                quit()
            if event.type is KEYDOWN and event.key is K_s:
                pygame.quit()  #Lisasin "pygame.quit()", kuna see peaks vältima rekursiooni
                startup()

def arvuta(sõnena):
    x = sõnena.strip().split(";")
    num = [float(i) for i in x]
    tulemus = 0
    for i in num:
        tulemus += i
    return round(tulemus,3)

def ajatabel():
    fail = open("ajad.txt")
    x = fail.readlines()

    tabel = []
    for i in x:
        try:
            tabel.append(arvuta(i))
        except:
            pass
    skoorid = sorted(tabel)

    pygame.init()
    ekraani_pind = pygame.display.set_mode( (500, 320) )
    pygame.display.set_caption("SKOORID")

    ekraani_pind.fill((0, 0, 0))

    for i in range(5):
        try:
            tekst5 = "Click SPACE to return"
            meie_font1 = pygame.font.SysFont("Arial", 24)
            teksti_pilt5 = meie_font1.render(tekst5, False, (255, 255, 255))
            ekraani_pind.blit(teksti_pilt5, (150, 0))
            tekst = str(skoorid[i])
            meie_font = pygame.font.SysFont("Arial", 24)
            teksti_pilt = meie_font.render(str(i+1)+"."+" "+tekst, False, (255,255,255))
            ekraani_pind.blit(teksti_pilt, (200, 30+24*i))
        except:
            pass

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type is QUIT:
                quit()
            if event.type is KEYDOWN and event.key is K_ESCAPE:
                quit()
            if event.type is KEYDOWN and event.key is K_SPACE:
                startup()


startup()
pygame.quit()