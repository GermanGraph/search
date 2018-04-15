import requests
import lxml.html as html
import PIL
import io

from cairosvg import svg2png


brand = 'gazprom'.lower()

url = f'https://worldvectorlogo.com/search/{brand}'

page = requests.get(url)
root = html.fromstring(page.content.decode())
imgs = root.xpath('//img[@class="logo__img"]')

for no, img in enumerate(imgs):
    print(no, end=' ')
    pic_url = img.get('src')
    pic_desc = img.get('alt')

    if brand in pic_desc.lower():
        svg = requests.get(pic_url).content
        try:
            png = svg2png(bytestring=svg)
        except Exception:
            print('!err')
            continue
        png = PIL.Image.open(io.BytesIO(png))

        try:
            background = PIL.Image.new("RGB", png.size, (255, 255, 255))
            background.paste(png, mask=png.split()[3])

            pil_jpg = png.convert('RGB')
            background.save(f'./logos/{brand}-{no}.jpg', 'JPEG', quality=80)
        except IndexError:
            pil_jpg = png.convert('RGB')
            pil_jpg.save(f'./logos/{brand}-{no}.jpg', 'JPEG', quality=80)

        print('+')
    else:
        print('-')
