from flask import Flask, render_template, request, redirect, send_file
from flaskwebgui import FlaskUI
import os
from PIL import Image, ImageOps, ImageEnhance
import numpy as np
import random

randVar = random.randint(1,1e10)
IMAGE = 'static/operated/Image_ID_'+str(randVar)+'.jpg'

def setHirarchy(r,g,b):
    p=[r,g,b]
    p.sort()
    return p.index(r),p.index(g),p.index(b)
def setPriorityRGB(r,g,b):
    R,G,B=setHirarchy(r,g,b)  
    img = Image.open(IMAGE) 
    ImgArr=np.array(img, dtype=np.uint8)
    for x in range(len(ImgArr)):
        for y in range(len(ImgArr[0])):
            p=[ImgArr[x][y][0],ImgArr[x][y][1],ImgArr[x][y][2]]
            p.sort()
            # swapping the colours
            ImgArr[x][y][0]=p[R]
            ImgArr[x][y][1]=p[G]
            ImgArr[x][y][2]=p[B]
    img = Image.fromarray(ImgArr, 'RGB')
    img.save(IMAGE)
def ThemeSwapRGB(r,g,b):
    img = Image.open(IMAGE) 
    ImgArr=np.array(img)
    Arr=np.zeros([len(ImgArr), len(ImgArr[0]), 3], dtype=np.uint8)
    for x in range(len(ImgArr)):
        for y in range(len(ImgArr[0])):
            Arr[x][y][0]=ImgArr[x][y][r]
            Arr[x][y][1]=ImgArr[x][y][g]
            Arr[x][y][2]=ImgArr[x][y][b]
    img = Image.fromarray(Arr, 'RGB')
    img.save(IMAGE)
def MakeInRange(x):
    if x>255:
        return 255
    elif x<0:
        return 0
    else:
        return x
def ColorEnhanceRGB(r,g,b): 
    img = Image.open(IMAGE) 
    ImgArr=np.array(img, dtype=np.uint8)
    for x in range(len(ImgArr)):
        for y in range(len(ImgArr[0])):
            # enhancing the pixels and Making in range
            ImgArr[x][y][0]=MakeInRange(ImgArr[x][y][0]+r)
            ImgArr[x][y][1]=MakeInRange(ImgArr[x][y][1]+g)
            ImgArr[x][y][2]=MakeInRange(ImgArr[x][y][2]+b)
    img = Image.fromarray(ImgArr, 'RGB')
    img.save(IMAGE)
def ImproveBrightness(f):
    im = Image.open(IMAGE)
    enhancer = ImageEnhance.Brightness(im)
    im_output = enhancer.enhance(f)
    im_output.save(IMAGE)
def ImproveContrast(f):
    im = Image.open(IMAGE) 
    im2= ImageEnhance.Contrast(im) 
    im3= im2.enhance(f)
    im3.save(IMAGE)
def ImproveSharpness(f):
    im = Image.open(IMAGE) 
    im2= ImageEnhance.Sharpness(im) 
    im3= im2.enhance(f)
    im3.save(IMAGE)

app = Flask(__name__)
ui = FlaskUI(app)

# app.config["Image_UPLOADS"] = str(os.getcwd()+'/static/')

@app.after_request
def add_header(r):
    # this function is to simulate the Developer Option -> Network -> Disable Cache
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/')
def main():
	return render_template('home.html')

@app.route('/download')
def download_file():
	# p = app.config["Image_UPLOADS"]+IMAGE
	# return send_file(p, as_attachment=True)
	return send_file(IMAGE, as_attachment=True)

@app.route('/image-selected', methods=['POST'])
def image_selected():
	if(request.method == 'POST'):
		
		try:
			os.remove(IMAGE)
		except:
			pass

		try:
			mySrc=request.files['mySrc']
			# mySrc.save(app.config["Image_UPLOADS"]+IMAGE)
			mySrc.save(IMAGE)
		except:
			pass

		return render_template('image-selected.html', ImageSource=IMAGE[7:], theWidth=540, theHeight=360)
		# passing after removing the 'static/' part

@app.route('/image-operation', methods=['POST'])
def image_operation():
	# try:os.chdir(str(app.config["Image_UPLOADS"]))
	# except:pass

	if(request.method == 'POST'):
		try :
			priority = request.form['priority']		
			if(priority != 'none'):
				if(priority == 'rgb'):
					setPriorityRGB(2,1,0)
				if(priority == 'rbg'):
					setPriorityRGB(2,0,1)
				if(priority == 'brg'):
					setPriorityRGB(1,0,2)
				if(priority == 'bgr'):
					setPriorityRGB(0,1,2)
				if(priority == 'grb'):
					setPriorityRGB(1,2,0)
				if(priority == 'gbr'):
					setPriorityRGB(0,2,1)

			swap = request.form['swap']
			if(swap != 'none'):
				if(swap == 'rg'):
					ThemeSwapRGB(1,0,2)
				if(swap == 'gb'):
					ThemeSwapRGB(0,2,1)
				if(swap == 'br'):
					ThemeSwapRGB(2,1,0)

			cast = request.form['cast']
			if(cast != 'none'):
				if(cast == 'rtog'):
					ThemeSwapRGB(0,0,2)
				if(cast == 'rtob'):
					ThemeSwapRGB(0,1,0)
				if(cast == 'btor'):
					ThemeSwapRGB(2,1,2)
				if(cast == 'btog'):
					ThemeSwapRGB(0,2,2)
				if(cast == 'gtor'):
					ThemeSwapRGB(1,1,2)
				if(cast == 'gtob'):
					ThemeSwapRGB(0,1,1)

			EnhanceRed = int(request.form['EnhanceRed'])
			EnhanceGreen = int(request.form['EnhanceGreen'])
			EnhanceBlue = int(request.form['EnhanceBlue'])
			if(EnhanceRed!=0 or EnhanceGreen!=0 or EnhanceGreen!=0):
				ColorEnhanceRGB(EnhanceRed, EnhanceGreen, EnhanceBlue)

			Brt = int(request.form['Brightness'])/100.0
			ImproveBrightness(Brt)

			Cst = int(request.form['Contrast'])/100.0
			ImproveSharpness(Cst)

			Srp = int(request.form['Sharpness'])/100.0
			ImproveSharpness(Srp)

			myWidth=request.form.get('myWidth')
			myHeight=request.form.get('myHeight')

		except:
			pass
		
		return render_template('image-selected.html', ImageSource=IMAGE[7:], theWidth=myWidth, theHeight=myHeight)

if(__name__ == '__main__'):
	ui.run()
	#app.run(debug = True)
