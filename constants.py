SSIZE = SWIDTH, SHEIGHT = 1080, 720
DEF_BG_COLOR = (20, 10, 30)

FUTURE = 100

PSPEED = 10
PSIZE = (12, 12)
DEFPHP = 100
DEF_PCOLOR = (240, 200, 200)
DEF_PCLHP = (120, 100, 100)
HPCOEFF = (PSIZE[0] // 2 + PSIZE[1] // 2) / DEFPHP
print(HPCOEFF)

GMOV_TIME = min(FUTURE, 100)
DEF_GMOV_COLOR = DEF_BG_COLOR
