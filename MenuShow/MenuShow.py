"""
Menu Show
"""
__author__ = "Jiang Yu-Kuan, yukuan.jiang(at)gmail.com"
__date__ = "2009/01/29~2009/01/29"
__revision__ = "v1.0"


def loadMenus(fn):
    import yaml, copy
    y = list(yaml.load_all(file(fn)))
    menus = y[1:]
    for m in menus:
        attr = copy.deepcopy(y[0])
        for key in attr.keys():
            attr[key].update(m.get(key, {}))
        m.update(attr)
    return menus


def makeFont(style):
    import ImageFont
    fn, size = style
    return ImageFont.truetype(fn, size)


def calcCoords(m, font):
    titleW, titleH = font.getsize(m['title'])
    maxW = titleW
    for item in m['items']:
        w, h = font.getsize(item)
        maxW = max(maxW, w)

    totalH = len(m['items'])*h
    if titleW != 0:
        totalH += h

    x = (m['basemap']['dim'][0] - maxW) / 2
    y = (m['basemap']['dim'][1] - totalH) / 2
    return x, y, h, maxW, totalH


def makeBasemap(attr, textRect):
    import Image
    im1 = Image.new('RGB', attr['dim'], attr['color'])
    im2 = Image.open(attr['image']).resize(attr['dim'], Image.BICUBIC)
    if 'color' == attr['type']:
        im = im1
    elif 'image' == attr['type']:
        im = Image.blend(im1, im2, .5)

    x, y, w, h = textRect
    r1 = im.crop((x, y, x+w, y+h))
    r2 = Image.new('RGB', (w, h), '#000000')
    im.paste(Image.blend(r1, r2, .5), (x, y, x+w, y+h))
    return im


def showMenu(m):
    import Image, ImageDraw
    options = {'font':makeFont(m['style']['font'])}
    x, y, h, maxW, totalH = calcCoords(m, options['font'])

    colorHex = lambda c: m['colors'].get(c, c)
    m['basemap']['color'] = colorHex(m['basemap']['color'])
    im = makeBasemap(m['basemap'], (x, y, maxW, totalH))
    draw = ImageDraw.Draw(im)

    options['fill'] = colorHex(m['style']['title']['color'])
    if m['title'] != '':
        draw.text((x,y), m['title'], **options)
        y += h

    options['fill'] = colorHex(m['style']['items']['color'])
    for item in m['items']:
        draw.text((x,y), item, **options)
        y += h

    im.show()
    return im


def main():
    menus = loadMenus("menu.yaml")
    for i, m in enumerate(menus):
        im = showMenu(m)
        im.save('m'+str(i)+'.jpg')


if __name__ == "__main__":
    main()
