SSIZE = SWIDTH, SHEIGHT = 1080, 720
DEF_BG_COLOR = (20, 10, 30)

FUTURE = 100

PSPEED = 10
PSIZE = (80, 80)
DEFPHP = 100
HPCOEFF = DEFPHP / (PSIZE[0] // 2 + PSIZE[1] // 2)
print(HPCOEFF)

GMOV_TIME = min(FUTURE, 100)
DEF_GMOV_COLOR = DEF_BG_COLOR
