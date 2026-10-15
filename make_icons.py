from PIL import Image, ImageDraw
import random, os

random.seed(7)
os.makedirs("assistant/static/assistant/icons", exist_ok=True)

def make(size):
    n = 16
    cell = size // n
    img = Image.new("RGB", (size, size))
    d = ImageDraw.Draw(img)
    for y in range(n):
        for x in range(n):
            if y < 2:
                base = (244, 166, 192) if random.random() < 0.5 else (232, 138, 171)
            elif y < 5:
                base = (93, 155, 58)
            else:
                base = (107, 74, 47)
            j = random.randint(-12, 12)
            color = tuple(max(0, min(255, c + j)) for c in base)
            d.rectangle([x*cell, y*cell, (x+1)*cell - 1, (y+1)*cell - 1], fill=color)
    img.save(f"assistant/static/assistant/icons/icon-{size}.png")

make(192)
make(512)
print("done")