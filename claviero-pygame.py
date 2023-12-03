
"""
python claviero-pygame.py --ordine /pmdrfwcuygj/tlsnvqeaoik/xbzhåöä,.-/ -i texts/morse-code-mnemonics-short.txt
"""

import pygame
from sys import exit
from itertools import accumulate
from collections import defaultdict
from datetime import datetime, timedelta
import argparse
import textwrap
import codecs
import time
import json

def read_args ():
  parser = argparse.ArgumentParser ()
  pad = parser.add_argument
  pad ("-i", "--infile", default="texts/tao-te-king.txt")
  pad ("-ln", "--line", type=int, default=-1)
  pad ("-font1", "--keycapfont", default="fonts/Arial_Bold.ttf")
  pad ("-font2", "--writesamplefont", default="fonts/DejaVuSansMono.ttf")
  pad ("-font3", "--resultlinefont", default="fonts/DejaVuSans-Bold.ttf")
  pad ("-font4", "--insectfont", default="fonts/Arial_Bold.ttf")
  pad ("-sz1", "--keycapfontsize", type=int, default=20)
  pad ("-sz2", "--writesamplefontsize", type=int, default=20)
  pad ("-sz3", "--resultlinefontsize", type=int, default=16)
  pad ("-sz4", "--insectfontsize", type=int, default=8)
  pad ("-sz5", "--resultfontsize", type=int, default=18)
  pad ("-sz6", "--hugefontsize", type=int, default=84)
  pad ("-sz7", "--infoscreenfontsize", type=int, default=14)
  pad ("-ww", "--wrapwidth", type=int, default=75)
  pad ("-wpm1", "--lowerwpm", type=float, default=12.5)
  pad ("-wpm2", "--upperwpm", type=float, default=80)
  pad ("--outlier", type=float, default=5.0)
  pad ("-order", "--ordine", default="")
  pad ("--info", action="store_true")
  pad ("--dontsave", action="store_true")
  pad ("--showmouse", action="store_true")
  pad ("--no_insects", action="store_true")
  pad ("--no_inumbers", action="store_true")
  pad ("--constspeed", action="store_true")
  pad ("-p", "--parolas", default="")
  args = parser.parse_args ()
  return (args)

args = read_args()

class S:
  def __init__(self):
    self.data = []

print ("-order", args.ordine)

openmojipalette = {
  'blue': '#92d3f5', 'blueshadow': '#61b2e4', 'red': '#ea5a47',
  'redshadow': '#d22f27', 'green': '#b1cc33', 'greenshadow': '#5c9e31',
  'yellow': '#fcea2b', 'yellowshadow': '#f1b31c', 'white': '#ffffff',
  'lightgrey': '#d0cfce', 'grey': '#9b9b9a', 'darkgrey': '#3f3f3f',
  'bggrey': '#333333', 'black': '#000000', 'orange': '#f4aa41',
  'orangeshadow': '#e27022', 'pink': '#ffa7c0', 'pinkshadow': '#e67a94',
  'purple': '#b399c8', 'purpleshadow': '#8967aa', 'brown': '#a57939',
  'brownshadow': '#6a462f', 'LightSkinTone': '#fadcbc',
  'MediumLightSkinTone': '#debb90', 'MediumSkinTone': '#c19a65',
  'MediumDarkSkinTone': '#a57939', 'DarkSkinTone': '#6a462f',
  'DarkSkinShadow': '#352318', 'NavyBlue': '#1e50a0',
  'Maroon': '#781e32', 'DarkGreen': '#186648'}

hardware_codes = [
  10,11,12,13,14,  15,16,17,18,19,
  24,25,26,27,28,  29,30,31,32,33,34,
  38,39,40,41,42,  43,44,45,46,47,48,
  52,53,54,55,56,  57,58,59,60,61, 
]

left,right,number,kgreen = "left","right","number","kgreen"

squares = [
  # number row: 85-25,85-25
  (10, number, 60, 0),
  (11, number, 120, 0),
  (12, number, 180, 0),
  (13, number, 240, 0),
  (14, number, 300, 0),
  (15, number, 360, 0),
  (16, number, 420, 0),
  (17, number, 480, 0),
  (18, number, 540, 0),
  (19, number, 600, 0),
  (20, number, 660, 0),
  # upper row: 115-25,85-25
  (24, left, 90, 60),
  (25, left, 150, 60),
  (26, left, 210, 60),
  (27, left, 270, 60),
  (28, left, 330, 60),
  (29, right, 390, 60),
  (30, right, 450, 60),
  (31, right, 510, 60),
  (32, right, 570, 60),
  (33, right, 630, 60),
  (34, right, 690, 60),
  # middle row:
  (38, left, 105, 120),
  (39, left, 165, 120),
  (40, left, 225, 120),
  (41, left, 285, 120),
  (42, left, 345, 120),
  (43, right, 405, 120),
  (44, right, 465, 120),
  (45, right, 525, 120),
  (46, right, 585, 120),
  (47, right, 645, 120),
  (48, right, 705, 120),
  # bottom row:
  (52, left, 135, 180),
  (53, left, 195, 180),
  (54, left, 255, 180),
  (55, left, 315, 180),
  (56, left, 375, 180),
  (57, right, 435, 180),
  (58, right, 495, 180),
  (59, right, 555, 180),
  (60, right, 615, 180),
  (61, right, 675, 180),
]

w,h = 60,60

def create_order (self):
  order = "/qwertyuiopå/asdfghjklöä/zxcvbnm,.-/"
  # if self.order:
  #   order = self.order
  if args.ordine:
    order = args.ordine
  ao = order.split(order[0])
  claves = (
    # number row:
    [(10+i,x) for i,x in enumerate ("1234567890+")] +
    # upper row:
    [(24+i,x.upper()) for i,x in enumerate (ao[1])] +
    # middle row:
    [(38+i,x.upper()) for i,x in enumerate (ao[2])] +
    # bottom row:
    [(52+i,x.upper()) for i,x in enumerate (ao[3])]
  )
  special = {
    ',': ';', '.': ':', '-': '−', '1': '!', '2': '"', 
    '3': '#', '5': '%', '7': '/', '8': '(', '9': ')',
  }
  sqs = {}
  labels = {}
  poss = {num: (side,x,y) for num,side,x,y in squares}
  keyst = {num:ch for num,ch in claves}
  shift = [(kgreen,0,180,75,60),(kgreen,736,180,165,60)]
  for num,ch in claves:
    side,x1,y1 = poss [num]
    sqs[ch.lower()] = [(side,x1,y1,60,60)]
    labels[ch.upper()] = (side,num,x1,y1,60,60)
    if ch.isalpha(): 
      sqs[ch.upper()] = [(side,x1,y1,60,60)] + [shift[0 if side == right else 1]]
  sqs[' '] = [(kgreen,240,240,360,60)]
  sqs['BackSpace'] = [(kgreen,781,0,120,60)]
  self.sqs = sqs
  self.shift = shift
  self.keyst = keyst
  self.special = special
  self.labels = labels

def wrap_text (teksto):
  wrapper = textwrap.TextWrapper (width=args.wrapwidth)
  teksto = wrapper.wrap (text=teksto)
  teksto = [s + ("" if s.endswith("-") else " ") for s in teksto]
  return teksto

def load_teksto ():
  f = codecs.open (args.infile, encoding='utf-8', errors='replace')
  teksto = f.read().strip()
  f.close ()
  rpl = ("\n"," "),("  "," "),("  "," "),
  for a,b in rpl:
    teksto = teksto.replace (a,b)
  return teksto

def hex_to_rgb (hex):
  h = hex.lstrip ('#')
  return tuple (int (h[i:i+2], 16) for i in (0, 2, 4))

def om (name,alpha=255):
  return hex_to_rgb (openmojipalette [name]) + (alpha,)

def label_color (side):
  d = {right:om ("blue"), left:om ("pink"), 
       number:om("grey"), kgreen: om ("green")}
  return d [side]

def img_source (self,side):
  d = {right:self.imgblue1, left:self.imgpink1, 
       number:self.imggrey1, kgreen:self.imggreen1}
  return d [side]

def save_resultlog (self):
  print ("save_resultlog")
  r = defaultdict (lambda: [])
  for k,v in self.presses.items():
    if len(k) == 2:
      a,b = k[0],k[1]
      if a != b and 'a' <= b <= 'z':
        r[b].append (v)
  q = []
  for k,v in r.items():
    c,d = v[0]
    for a,b in v:
      c,d = (c * d + a * b) / (d + b), d + b
    q.append ((k,c))
  q.sort (key=lambda x: x[1])
  f = open ("resultlog.txt","a")
  f.write (f"# {self.alltimekeys}\n")
  for a,b in q:
    f.write (f"{a} {b:.4f}\n")
  f.close()

def load (img):
  return pygame.image.load ("graphics/" + img).convert_alpha()

def draw_images (self):
  self.keygrid = pygame.image.load ("graphics/claviero-1.png")
  th = args.keycapfontsize
  for ch in self.labels:
    side,num,x1,y1,h1,w1 = self.labels[ch]
    img = self.keycapfont.render (ch,True,label_color (side))
    x,y = x1 + 25+9, y1 + 25+6
    rect = img.get_rect (topleft = (x,y))
    if side == number:
      x,y = x,y+48
      rect = img.get_rect (bottomleft = (x,y))
    self.keygrid.blit (img, rect)
  pygame.image.save (self.keygrid,"graphics/claviero-2.png")
  self.keygrid = load ("claviero-2.png")
  self.imgerror = load ("white-red-kb.png")
  self.imgblue1 = load ("blue-1.png")
  self.imgpink1 = load ("pink-1.png")
  self.imggreen1 = load ("green-1.png")
  self.imggrey1 = load ("grey-1.png")

insects = [om(name) for name in ['purple','green','orange','grey',
  'blue','red','pink','NavyBlue','Maroon' ]]

def paint_insects (self):
  if self.starttime and not args.no_insects:
    insectspace = self.w / len (insects)
    tme1 = time.time()
    tme2 = tme1 - self.insecttime
    self.insectnow = self.insectnow + self.charw * (cpm(self.insectspeed) * tme2 / 60) % self.w
    self.insecttime = tme1
    if args.no_inumbers:
      for i,color in enumerate (insects):
        xpt =  int ((self.insectnow + i*insectspace) % self.w)
        pygame.draw.rect (self.screen, color, [xpt, self.h + 78, 110, 7])
        if xpt + 110 > self.w:
          pygame.draw.rect (self.screen, color, [-(self.w - xpt), self.h + 78, 110, 7])
    else:
      for i,color in enumerate (insects):
        xpt =  int ((self.insectnow + i*insectspace) % self.w)
        pygame.draw.rect (self.screen, color, [xpt, self.h + 78, 30, 7])
        img = self.insectfont.render (f"{self.insectspeed:.1f}",True,color)
        rect = img.get_rect (bottomleft = (xpt+50, self.h + 85 + 1))
        self.screen.blit (img, rect)
        if xpt + 110 > self.w:
          pygame.draw.rect (self.screen, color, [-(self.w - xpt), self.h + 78, 30, 7])
          img = self.insectfont.render (f"{self.insectspeed:.1f}",True,color)
          rect = img.get_rect (bottomleft = (-(self.w - xpt)+50, self.h + 85 + 1))
          self.screen.blit (img, rect)

def draw_res (self):
  img = self.resultlinefont.render (self.resline,True,om ("white"))
  self.screen.blit (img, (920-img.get_width(),3))
  if args.info:
    for i,line in enumerate (self.hugelines):
      img = self.hugefont.render (line,True,om (["green","purple","lightgrey"][i]))
      self.screen.blit (img, (920-img.get_width(),int (22 + i*1.10*img.get_height())))

def draw_txt (self,x,y,sample,gotright,gotwrong,show_arrow=False):
  tsize = args.writesamplefontsize + 2
  if show_arrow:
    img = self.insectfont.render ("1",True,om ("pink"))
    self.screen.blit (img, (5,y+6+1*tsize))
    img = self.insectfont.render ("2",True,om ("pink"))
    self.screen.blit (img, (5,y+6+0*tsize))

  sams = same (self.current,sample[0])
  padded = sample[0] if sams == 0 else " " * sams + sample[0] [sams:]
  img = self.writesamplefont.render (padded,True,om ("white"))
  self.screen.blit (img, (x,y+tsize))

  img = self.writesamplefont.render (sample[1],True,om ("lightgrey"))
  self.screen.blit (img, (x,y))

  if gotright:
    img = self.writesamplefont.render (gotright,True,om ("white"))
    self.screen.blit (img, (x,y+2*tsize))
    x = x + img.get_width()

  lft = sample[0] [len(gotright):]
  nxt = lft [:1]

  img = self.writesamplefont.render (gotwrong,True,om ("pink"))
  self.screen.blit (img, (x,y+2*tsize))
  x = x + img.get_width()

  if len (gotwrong) != 0:
    pygame.draw.rect (self.screen, om ("pink"), [x,y+2*tsize,tsize//2,tsize])
  else:
    pygame.draw.rect (self.screen, om ("green"), [x,y+2*tsize,tsize//2,tsize])
  return nxt,len(gotwrong)

def draw_infolines (self):
  for i,s in enumerate (self.infolines):
    img = self.infolinefont.render (s,True,om ("lightgrey"))
    self.screen.blit (img, (20,int (25 + i*1.00*img.get_height())))

def draw_screen (self):
  self.screen.fill (om("bggrey"))
  if args.info:
    draw_infolines (self)
  else:
    self.screen.blit (self.keygrid, (0,0))
  gotright,gotwrong,lft = calc_cire (self.current,self.text[self.line % len (self.text)])
  this_and_some = [self.text [x % len(self.text)] 
    for x in range (self.line,self.line+5)]
  self.nxt,self.gotwronglen = draw_txt (
    self,
    20,self.h+2,
    this_and_some, gotright, gotwrong,
    show_arrow=(not self.starttime))
  draw_res (self)
  paint_insects (self)
  if self.gotwronglen != 0:
    self.screen.blit (self.imgerror, (0,0))
  if not args.info:
    bs = [] if self.gotwronglen == 0 else self.sqs ['BackSpace']
    if self.nxt and self.nxt in self.sqs:
      for side,x,y,w,h in self.sqs [self.nxt] + bs:
        source = img_source (self,side)
        cir = self.manysames % 3
        self.screen.blit (
           source, 
           (x+25+cir*5, y+25+cir*5),
           (x+25+cir*5, y+25+cir*5, w-cir*10, h-cir*10))

def init_vars (self):
  self.info = False
  self.resline, self.oldresline = "",""
  self.current, self.old = "",""
  self.nxt, self.last = '',''
  self.restlen, self.total = 0,0
  self.startkey = -1
  self.lastkept = 90
  self.oldtot, self.manysames = 0,0
  self.starttime, self.timeold, self.rank = None,None,None
  self.curline = {}
  self.lasterror = 0,0
  self.keys,self.ers = [],[]
  self.outliers = []
  self.infolines = []
  self.hugelines = []
  self.capture = []
  self.savecapture = 0
  self.cc = 0
  self.infolineslen = 16

def wpm (cpm):
  return cpm / 5.0

def cpm (wpm):
  return 5.0 * wpm

def cps (wpm):
  return 5.0 * wpm / 60

def infolines_append (self, infoline):
  self.infolines.append (infoline)
  self.infolines = self.infolines[-self.infolineslen:]

def infolines_hr (self):
  infolines_append (self, 56*"=")

def load_json_files (self):
  try:
    f = open ("scores.txt")
    s = f.read ()
    f.close ()
    t = [x.split("\t") for x in s.split("\n")]
    self.scores = [(float(a),b,float(c)) for a,b,c in t]
  except:
    self.scores = []
  for i in range(29,-1,-1):
    if len (self.scores) > i:
      x,t,ers = self.scores [i]
      infoline = f"{x:>5.1f} {cps(x):.1f} {t} {ers:.2f}% ({i+1})"
      infolines_append (self,infoline)
  self.insectspeed = args.lowerwpm
  try:
    self.presses = json.load (open ("presses.json","r"))
  except:
    self.presses = {}
  try:
    self.capture = json.load (open ("capture.json","r"))
  except:
    self.capture = []
  try:
    self.config = json.load (open ("config.json","r"))
  except:
    self.config = {'line': 0, 'usage': 0, 'alltimekeys': 0}
  self.line = self.config ['line']
  if (not args.parolas) and 'curline' in self.config:
    self.curline = self.config ['curline']
    if args.infile in self.curline:
      self.line = self.curline [args.infile]
    else:
      self.line = 0
  if 'order' in self.config:
    self.order = self.config ['order']
  else:
    self.order = ""
  self.usage = self.config ['usage']
  self.alltimekeys = self.config ['alltimekeys']
  infolines_hr (self)

def init (self):
  pygame.init ()
  pygame.mouse.set_visible (args.showmouse)
  init_vars (self)
  load_json_files (self)
  pygame.display.set_caption ("Claviero-pygame")
  create_order (self)
  self.w, self.h = 952,352
  screen_w, screen_h = self.w, self.h+85
  self.screen = pygame.display.set_mode ((screen_w, screen_h))
  self.clock = pygame.time.Clock ()
  self.keycapfont = pygame.font.Font (args.keycapfont,
    args.keycapfontsize)
  self.writesamplefont = pygame.font.Font (args.writesamplefont,
    args.writesamplefontsize)
  self.infolinefont = pygame.font.Font (args.writesamplefont,
    args.infoscreenfontsize)
  self.resultlinefont = pygame.font.Font (args.resultlinefont,
    args.resultlinefontsize)
  self.hugefont = pygame.font.Font (args.resultlinefont,
    args.hugefontsize)
  self.insectfont = pygame.font.Font (args.insectfont,
    args.insectfontsize)
  img = self.writesamplefont.render (100*"x",True,om ("white"))
  self.charw = img.get_width() // 100
  draw_images (self)
  if args.parolas:
    self.text = 50 * (args.parolas + " ")
  else:
    self.text = load_teksto ()
  self.text = wrap_text (self.text)
  self.wrappoints = list (accumulate([0]+[len (s) for s in self.text]))
  if self.line >= len (self.text):
    self.line = 0
  if args.line != -1:
    self.line % len (self.text)

def same (s1,s2):
  x = 0
  while len(s1) > x and len (s2) > x and s1 [x] == s2 [x]:
    x += 1
  return x

def save_score (self,wpm3,ers):
  inx = 0
  for x,t,er in self.scores:
    if wpm3 > x:
      break
    else:
      inx += 1
  if inx < 31 or self.savecapture > 1:
    print ("Capture added.")
    self.capture.append ([wpm3,self.keys,self.ers])
    if self.savecapture > 1:
      self.savecapture = 1
  self.scores.insert (inx,[wpm3,time.strftime("%Y-%m-%d %H:%M:%S"),ers])
  self.scores = self.scores [:15000]
  return inx + 1

def calc_speed (self,chars):
  if not (self.starttime):
    self.starttime = time.time()
    self.startkey = chars - 1
    self.insectnow = 0.0
    self.insecttime = self.starttime
    pygame.time.set_timer (pygame.USEREVENT, 195)
    print ("Started.")
  self.total = chars - self.startkey 

def calc_cire (current,sample0):
  sams = same (current,sample0)
  gotright = sample0 [:sams]
  gotwrong = current [len(gotright):]
  lft = sample0 [len(gotright):]
  return gotright, gotwrong, lft

def divmod_wrappoint (wrappoints, line):
  q,r = divmod (line, len(wrappoints)-1)
  result = q * wrappoints [-1] + wrappoints [r]
  return result

def got_error (self,gotright):
  newerror = self.line, len(gotright)
  if newerror != self.lasterror:
    now = time.time()
    self.ers.append (now)
    self.lasterror = newerror

def purge_errors (self):
  now = time.time ()
  for t in self.ers:
    t1 = now - t
    if t1 > 120:
      del (self.ers[0])
    else:
      break

def purge_keys (self):
  now = time.time ()
  for t,c in self.keys:
    t1 = now - t
    if t1 > 120:
      del (self.keys[0])
    else:
      break

def add_key (self):
  gotright,gotwrong,lft = calc_cire (
    self.current,
    self.text [self.line % len (self.text)])
  if gotwrong == "" and self.current != self.old:
    calc_speed (self,divmod_wrappoint (self.wrappoints,self.line) + len(gotright))
    now = time.time ()
    c = self.current [-1:]
    if c and self.oldtot < self.total:
      self.keys.append ([now,c])
      self.oldtot = self.total
    if self.gotwronglen == 0 and self.timeold:
      ad = (" " + self.current) [-2:]
      t1 = now - self.timeold
      if len (ad) == 2:
        if ad in self.presses:
          a,be = self.presses [ad] 
          if t1 / a < args.outlier:
            be += 1
            b = min (300,be)
            self.presses [ad] = [(1/b) * t1 + (1 - 1/b) * a, be]
          else:
            out = (ad,t1,t1/a)
            self.outliers.append (out)
        else:
          self.presses [ad] = [t1,1]
    self.timeold = now
    self.old = self.current
  else:
    if len (gotwrong) == 1 and self.starttime:
      got_error (self,gotright)
  if gotright and lft and gotright[-1] == lft[0]:
    self.manysames += 1
  else:
    self.manysames = 0

def letter_shift (letter,shift):
  if letter.isalpha():
    return letter.upper() if shift else letter.lower() 
  return letter

def infolines_add_help (self):
  m, s = divmod (self.usage, 60)
  h, m = divmod (m, 60)
  total = self.alltimekeys + self.total
  for s in [
    "Control-I: Toggle between info-screen and keymap image.",
    "Control-S: Save captured key-presses.",
    "Control-B: Show best scores.",
    "Control-N: Toggle insectstyle.",
    "Control-M: Toggle mouse visibility.",
    "Control-H: Help",
    "Control-X: Exit.", 
    f"Total usage: {h} hours {m} minutes.",
    f"Total keys: {total:_}".replace("_", " ")]:
   infolines_append (self,s)
  infolines_hr (self)

def infolines_add_scores (self):
  for i in range(29,-1,-1):
    if len (self.scores) > i:
      x,t,ers = self.scores [i]
      dt = datetime.strptime(t,"%Y-%m-%d %H:%M:%S")
      past1h = datetime.now() - timedelta(hours=1)
      past24 = datetime.now() - timedelta(days=1)
      past = ""
      if dt > past24: past = "+"
      if dt > past1h: past = "*"

      infoline = f"{x:>5.1f} {cps(x):.1f} {t} {ers:.2f}% ({i+1}) {past}"
      infolines_append (self,infoline)
  infolines_hr (self)

def handle_key_press (self, event):
  hw2 = event.scancode
  number = event.key
  keyname = chr (number)
  ctrl = event.mod & pygame.KMOD_CTRL
  shift = event.mod & pygame.KMOD_SHIFT
  accept = False
  if ctrl and keyname == "x":
    print ("Control-X pressed. Quitting.")
    do_quit (self)
  elif ctrl and keyname == "i":
    print (f"Control-I pressed.")
    args.info = not args.info
  elif ctrl and keyname == "b":
    print (f"Control-B pressed.")
    args.info = not args.info
    infolines_add_scores (self)
  elif ctrl and keyname == "n":
    print (f"Control-N pressed.")
    args.no_inumbers = not args.no_inumbers
  elif ctrl and keyname == "s":
    print ("Control-S pressed.")
    self.savecapture = 2
  elif ctrl and keyname == "m":
    print (f"Control-M pressed.")
    args.showmouse = not args.showmouse
    pygame.mouse.set_visible (args.showmouse)
  elif ctrl and keyname == "h":
    print (f"Control-H pressed.")
    args.info = True
    infolines_add_help (self)
  elif keyname == " ":
    accept = True
    self.current += " "
  elif number == pygame.K_BACKSPACE :
    accept = True
    self.current = self.current [:-1]
  elif hw2 in hardware_codes:
    letter = self.keyst [hw2]
    accept = letter != ''
    if letter in self.special and shift:
      letter = self.special [letter]
    letter = letter_shift (letter,shift)
    self.current += letter
  add_key (self)
  if self.current == self.text [self.line % len (self.text)]:
    self.line += 1
    self.current = ""

def take_timeout (self):
  now = time.time()
  wpm1 = wpm (len (self.keys) / 2)
  ers = 100 * len(self.ers) / max (1,len(self.keys))
  seconds = int (now - self.starttime)
  if seconds < 120:
    wpm1 = wpm (60 * len (self.keys) / max (seconds,1.0))
  if seconds >= self.lastkept + 30 and wpm1 > args.lowerwpm:
    self.rank = save_score (self,wpm1,ers)
    self.lastkept = seconds
    infoline = (f"{wpm1:>5.1f} {cps(wpm1):.1f} {time.strftime('%Y-%m-%d %H:%M:%S')}"
      f" {ers:.2f}% ({self.rank})" + (" *" if self.rank <= 30 else ""))
    infolines_append (self,infoline)
    print (infoline)
  tottime = [(str (int (seconds / 60)).zfill (2) 
      + ":" + str (int(seconds % 60)).zfill (2))]

  self.resline = " ".join (
    [str(self.total)] + 
    [f"{wpm1:.1f}"] +
    tottime +
    [f"{ers:.2f}%"] +
    [("(" + str(self.rank) + ")") if self.rank else ""])
  self.hugelines = tottime + [f"{wpm1:.1f}"] + [f"{ers:.2f}%"]
  if not args.constspeed:
    self.insectspeed = max (args.lowerwpm, (10.00 - ers)/10 * wpm1)
    self.insectspeed = min (args.upperwpm, self.insectspeed)
  purge_keys (self)
  purge_errors (self)

def do_quit (self):
  self.alltimekeys += self.total
  save_resultlog (self)
  if self.starttime:
    self.usage += round (time.time() - self.starttime)
  if not args.parolas:
    self.curline [args.infile] = self.line % len (self.text)
  self.config = {'line': self.line % len (self.text), 'usage': self.usage,
    'curline': self.curline, 'alltimekeys': self.alltimekeys, 
    'order': self.order }
  if not args.dontsave:
    self.capture.sort (reverse=True)
    self.capture = self.capture[:30+self.savecapture]
    json.dump (self.capture, open("capture.json","w"))
    json.dump (self.config, open("config.json","w"))
    json.dump (self.presses, open("presses.json","w"))
    t = []
    for score,day,errs in self.scores:
      t.append (F"{score:.1f}\t{day}\t{errs:.2f}")
    s = "\n".join (t)
    f = open ("scores.txt","w")
    f.write (s)
    f.close ()
  else:
    print ("Argument '--dontsave': Nothing has been saved.")
  print ("Outliers:")
  for out in self.outliers:
    print (f"'{out[0]}' {out[1]:.4f} s {out[2]:.2f}x")
  print ("Number of scores =",len(self.scores))
  print ("Best scores:")
  for i,(wpm,t,errs) in enumerate (self.scores[:30]):
    dt = datetime.strptime(t,"%Y-%m-%d %H:%M:%S")
    past1h = datetime.now() - timedelta(hours=1)
    past24 = datetime.now() - timedelta(days=1)
    past = ""
    if dt > past24: past = "+"
    if dt > past1h: past = "*"
    print (f"{wpm:>5.1f} wpm {t} {errs:.2f}% ({i+1}) {past}")
  print ("Quitting.")
  m, s = divmod (self.usage, 60)
  h, m = divmod (m, 60)
  print ("Total usage:", h, "hours", m, "minutes.")
  print (f"Total keys: {self.alltimekeys:_}".replace("_", " "))
  pygame.quit ()
  exit ()

self = S ()
init (self)
while True:
  for event in pygame.event.get ():
    if event.type == pygame.QUIT:
      do_quit (self)
    elif event.type == pygame.KEYDOWN:
      handle_key_press (self, event)
    elif event.type == pygame.USEREVENT:
      take_timeout (self)
  draw_screen (self)
  pygame.display.update ()
  self.clock.tick (20)

