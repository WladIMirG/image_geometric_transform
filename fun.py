from operator import inv
from matplotlib.pyplot import hist, step
from imports import *
from config import *

def inter_VMP(img, p):
    # print(p[0])
    p = p.astype(int)
    return img[p[1],p[0]]

def inter_bilinear(img, p):
    dx = p[0] - p[0].astype(int)
    dy = p[1] - p[1].astype(int)
    p = p.astype(int)
    t1 = (1-dx)*(1-dy)*img[p[1],p[0]]
    t2 = dx*(1-dy)*img[p[1],p[0]+1]
    t3 = dx*dy*img[p[1]+1,p[0]+1]
    t4 = (1-dx)*dy*img[p[1]+1,p[0]]
    intensidade = t1+t2+t3+t4
    return intensidade

def imagem_upload(args):
    # This function loads an image from a path.
    if os.path.isfile("img/"+args["img_i"]):
        return cv2.imread(os.getcwd()+"/"+"img/"+args["img_i"])
    else:
        d = {"escala": "baboon.png",
             "rotate": "baboon.png",
             "perspectiva": "baboon_perspectiva.png"}
        print("A imagem tem que ficar na pasta img")
        print("Vai se carregar a imagem: "+d[args["mode"]])
        return cv2.imread(os.getcwd()+"/"+"img/"+d[args["mode"]])

def show_save_img(img, img_s, args):
    cv2.imshow("Original", img)
    cv2.imshow("Tranformada", img_s)
    if args["img_o"] != None:
        cv2.imwrite(os.getcwd()+"/"+"results/"+args["img_o"], img_s)
    else:
        if args["mode"] == "perspectiva":
            cv2.imwrite(os.getcwd()+"/"+"results/"+args["mode"]+".png", img_s)
        if args["mode"] == "rotate":
            cv2.imwrite(os.getcwd()+"/"+"results/"+args["mode"]+"_"+str(args["angulo"])+".png", img_s)
        if args["mode"] == "escala":
            cv2.imwrite(os.getcwd()+"/"+"results/"+args["mode"]+"_"+str(args["x_scale"]) \
                +"_"+str(args["y_scale"])+".png", img_s)
    cv2.waitKey(0)

def interpolador(args):
    inter = {
        "inter_VMP": inter_VMP,
        "inter_bilinear": inter_bilinear,
        }
    return inter[args["interp"]]

def escala(img, args):
    # This function scales an image around the center of the image.
    # Create out image whit the same size of the original image.
    # Calculing midle of the image.
    # Calculing a scale matrix.
    # Calculing inverse scale matrix.
    # Scale the image process.
    
    sx = args["x_scale"]
    sy = args["y_scale"]
    
    img_s = np.zeros(img.shape, dtype=np.uint8)
    y, x = img_s.shape[:2]
    midy, midx = y//2, x//2
    
    s = np.array([[sx, 0, 0],
                  [0, sy, 0],
                  [0, 0, 1]])
    
    i_s = np.linalg.inv(s)
    for i in range(y-1):
        for j in range(x-1):
            xnew = j - midx
            ynew = i - midy
            p = np.array([[xnew],
                          [ynew],
                          [1]])
            # Scale the point
            p = np.dot(i_s, p)
            # Add the midle of the image
            p[0] += midx
            p[1] += midy
            # If the point is inside the image
            if p[0]>=0 and p[0]<x-1 and p[1]>=0 and p[1]<y-1:
                # img_s[i,j] = inter_bilinear(img, p) or inter_VMP(img, p)
                img_s[i,j] = interpolador(args)(img, p)
    return img_s

def rotate(img, args):
    # This function rotates an image around the center of the image.
    # Create out image whit the same size of the original image.
    # Calculing midle of the image.
    # Calculing a rotation matrix.
    # Calculing inverse rotation matrix.
    # Rotate the image process.
    angulo = args["angulo"]
    salida = np.zeros(img.shape, dtype=np.uint8)
    y, x = salida.shape[:2]
    midy, midx = y//2, x//2
    cos = np.cos(np.deg2rad(angulo))
    sen = np.sin(np.deg2rad(angulo))
    r = np.array([[cos, -sen, 0], 
                [sen,  cos, 0],
                [  0,    0, 1]])
    ir = np.linalg.inv(r)

    for i in range(y-1):
        for j in range(x-1):
            xnew = j - midx
            ynew = i - midy
            p = np.array([[xnew],
                          [ynew],
                          [1]])
            # Rotate the point
            p = np.dot(ir, p)
            # Add the midle of the image
            p[0] += midx
            p[1] += midy
            # If the point is inside the image
            if p[0]>=0 and p[0]<x-1 and p[1]>=0 and p[1]<y-1:
                # salida[i,j] = inter_bilinear(img, p) or inter_VMP(img, p)
                salida[i,j] = interpolador(args)(img, p)
    return salida
    
def perspectiva(img, args):
    # This function applies a perspective transformation to an image.
    # Init points
    pts1 = np.float32([[37,51],[342,42],[485,467],[73,380]])
    # End points
    pts2 = np.float32([[0,0],[511,0],[511,511],[0,511]])
    
    # Calculate the perspective transform matrix
    M = cv2.getPerspectiveTransform(pts1,pts2)
    # Apply the perspective transform to the image
    img_s = cv2.warpPerspective(img, M, (511,511))
    
    img[51,27:47] = [255,0,0]
    img[41:61,37] = [255,0,0]
    
    img[42,332:352] = [0,255,0]
    img[32:52,342] = [0,255,0]
    
    img[467,475:495] = [0,0,255]
    img[457:477,485] = [0,0,255]
    
    img[380,63:83] = [255,255,255]
    img[370:390,73] = [255,255,255]
    
    return img_s

modo = {
    "perspectiva": perspectiva,
    "rotate": rotate,
    "escala": escala,
}



def main(args):
    img = imagem_upload(args)
    img_s = modo[args["mode"]](img, args)
    show_save_img(img, img_s, args)
    
if __name__ == '__main__':
    # perspectiva()
    if os.path.isfile("img/baboon.png"):
        print("Existe")
        img = cv2.imread(os.getcwd()+"/img/baboon_perspectiva.png")
        # rotate(img, 45, 1)
        # escala(img, args)
        perspectiva(img, args)
    cv2.destroyAllWindows()