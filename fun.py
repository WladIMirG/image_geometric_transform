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

def escala(img, sx=1, sy=1):
    # This function scales an image around the center of the image.
    salida = np.zeros(img.shape, dtype=np.uint8)
    y, x = salida.shape[:2]
    
    midy, midx = y//2, x//2
    
    # sx sy = sx, sy
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
            
            p = np.dot(i_s, p)
            p[0] += midx
            p[1] += midy
            if p[0]>=0 and p[0]<x-1 and p[1]>=0 and p[1]<y-1:
                salida[i,j] = inter_bilinear(img, p)
                # salida[i,j] = inter_VMP(img, p)
    
    cv2.imshow("Escalada", salida)
    cv2.waitKey(0)

def rot(img, angulo, iter = 1):
    # This function rotates an image around the center of the image.
    salida = np.zeros(img.shape, dtype=np.uint8)
    y, x = salida.shape[:2]
    
    midy, midx = y//2, x//2
    # for a in range(0, angulo+1, angulo//iter):
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
            p = np.dot(ir, p)
            p[0] += midx
            p[1] += midy
            if p[0]>=0 and p[0]<x-1 and p[1]>=0 and p[1]<y-1:
                # salida[i,j] = inter_bilinear(img, p)#
                salida[i,j] = inter_VMP(img, p)
            
    
    cv2.imshow("Rotacionada", salida)
    # if cv2.waitKey(25) & 0xFF == ord('q'):
    #     break
    cv2.imshow("Rotacionada", salida)
    cv2.waitKey(0)
    cv2.imwrite("results/rot"+str(angulo)+".png", salida)
    
    
def perspectiva(img):
    pts1 = np.float32([[37,51],[342,42],[485,467],[73,380]])
    pts2 = np.float32([[0,0],[511,0],[511,511],[0,511]])
    
    M = cv2.getPerspectiveTransform(pts1,pts2)
    mode = cv2.warpPerspective(img, M, (511,511))
    
    img[51,27:47] = [255,0,0]
    img[41:61,37] = [255,0,0]
    
    img[42,332:352] = [0,255,0]
    img[32:52,342] = [0,255,0]
    
    img[467,475:495] = [0,0,255]
    img[457:477,485] = [0,0,255]
    
    img[380,63:83] = [255,255,255]
    img[370:390,73] = [255,255,255]
    
    cv2.imshow("Orginal", img)
    cv2.imshow("Modificada", mode)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
if __name__ == '__main__':
    # perspectiva()
    if os.path.isfile("img/baboon.png"):
        print("Existe")
        img = cv2.imread(os.getcwd()+"/img/baboon.png")
        # rot(img, 45, 1)
        escala(img, 0.5)
    cv2.destroyAllWindows()