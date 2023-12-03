
from num2words import num2words
import argparse

def read_args ():
  parser = argparse.ArgumentParser ()
  pad = parser.add_argument
  pad ("lang",nargs='*')
  args = parser.parse_args ()
  return args

args = read_args()

for lang in args.lang:
  lenny = 0
  tuhat = num2words (1000,lang=lang)
  f = open (f"{tuhat.replace (' ','-')}-{lang}.txt","w")
  for i in range (1,1_001):
    num = num2words (i,lang=lang)
    text = f"{num}, \n"
    if i % 100 == 0:
      text = text.replace (",",".")
    if i % 100 == 1:
      text = text.capitalize ()
    f.write (text)
    lenny = lenny + len (text) - 1
  f.close()
  print (lang, lenny,"characters.")


