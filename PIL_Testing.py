from PIL import Image

bg = Image.open("1411091228372.png")
fg = Image.open("avenge.png")

bg.paste(fg, (0,0), fg)
bg.show()