import numpy as np
import matplotlib.pyplot as plt
import PIL.Image as Image
from matplotlib import cm
from random import randint


def droite(imax, jmax):
    """
    Renvoie une matrice de taille (imax, jmax) où une droite bruitée 
    a été tracée pour faire des tests.
    """
    M = np.zeros((imax, jmax), dtype=np.uint8)
    for j in range(jmax):
        i = int(0.5*j + 10) + randint(-1, 1)
        if 0 <= i < imax:
            M[i, j] = 100
    return M

def niveaux_gris(M):
    n, m, k = M.shape
    A = np.zeros((n,m), dtype = np.uint8)
    for i in range(n):
        for j in range(m):
            R,V,B = M[i,j] 
            A[i,j] = R//3 + V//3 + B//3 #moyenne pour saisir les points A[i,j] de la matrice M
    return A

def dyn(M):
    """
    Augmente au maximum la dynamique d'une image en niveaux de gris.
    """
    M2 = np.array(M, dtype=np.float64)
    mini = np.min(M)
    maxi = np.max(M)
    return np.array((M2 - mini)*255/(maxi - mini), dtype=np.uint8)
    

def contours(M):
    n, m = M.shape
    Mc = np.array(M, dtype=np.int32)
    M1 = np.zeros((n,m), dtype=np.int32)
    M2 = np.zeros((n,m), dtype=np.int32)
    M1[1:-1, :] = Mc[2:,:] - Mc[:-2,:] #derivation = filtrage passe-haut
    M2[:, 1:-1] = Mc[:,2:] - Mc[:,:-2]
    M3 = np.abs(M1) + np.abs(M2)    #norme du grad de l'intensite lumineuse
    M4 = np.array(M3, dtype=np.uint8)
    return M4

def seuil(M, s):
    """
    Applique un seuillage sur l'image M.
    """
    M[M > s] = 255
    M[M <= s] = 0
    return M

def acc(M):
    """
    Renvoie la matrice d'accumulation de Hough.
    """
    imax, jmax = M.shape
    rhomax = int(np.sqrt(imax**2 + jmax**2)) + 1
    #accumulation
    Acc = np.zeros((rhomax, 360), dtype=np.uint32)    
    for i in range(imax):
        for j in range(jmax):
            if M[i, j] != 0:     
                for theta in range(360):
                    t = theta*np.pi/180
                    rho = int(np.cos(t)*j + np.sin(t)*i)
                    if  0 <= rho < rhomax:
                        Acc[rho, theta] += 1
            
    return Acc


def detect_droites(Macc, seuil=255):
    """
    Renvoie la liste des couples (rho, theta) détectés comme droites
    dans la matrice d'accumulation
    """
    rhomax, thetamax = Macc.shape
    li = []
    for rho in range(rhomax):
        for theta in range(thetamax):
            if Macc[rho, theta] >= seuil:
                li.append((rho, theta))
    return li
    
def trace(Macc, M, seuil=255):
    """
    Trace les droites correspondant aux couples (rho, theta) détectés
    sur la mtrice d'accumulation.
    """
    M2 = np.zeros(M.shape, dtype=np.uint8)
    lid = detect_droites(Macc, seuil)
    print('droites détectées :',lid)
    imax, jmax = M.shape
    for (rho, theta) in lid:
        t = theta*np.pi/180
        for i in range(imax):
            j = int((rho - i*np.sin(t)) / (np.cos(t)))
            if 0 <= j < jmax:
                M2[i, j] = 255
                
        for j in range(jmax):
            i = int((rho - j*np.cos(t)) / (np.sin(t)))
            if 0 <= i < imax:
                M2[i, j] = 255
            
    return M2

def test_base():
    """
    On teste d'abord avec une unique droite bruitée pour voir.
    """
    M = droite(30, 50)
    Md = dyn(M)
    Macc = acc(Md)
    Maccd = dyn(Macc)
    M2 = trace(Maccd, M)
    
    fig, ax = plt.subplots(1, 3)
    ax[0].imshow(M, cmap=cm.gray, vmin=0, vmax=255)
    ax[1].imshow(Md, cmap=cm.gray, vmin=0, vmax=255)
    ax[2].imshow(M2, cmap=cm.gray, vmin=0, vmax=255)
    
    fig, ax = plt.subplots()
    ax.imshow(seuil(Maccd, 240), cmap=cm.gray, vmin=0, vmax=255)

def test_image():
    """
    Test avec une image de panneau routier.
    """
    im = Image.open('route-prioritaire.jpg')
    M = np.asarray(im)
    Mng = niveaux_gris(M)
    Mc = dyn(contours(Mng))
    Ms = seuil(Mc, 100)
    Macc = acc(dyn(Ms))
    M2 = trace(Macc, Mng, 200)
    
    fig, ax =plt.subplots(1, 3)
    ax[0].imshow(M, cmap=cm.gray, vmin=0, vmax=255)
    ax[1].imshow(Mc, cmap=cm.gray, vmin=0, vmax=255)
    ax[2].imshow(Ms, cmap=cm.gray, vmin=0, vmax=255)
    
    fig, ax = plt.subplots()
    ax.imshow(M2, cmap=cm.gray)
    
#test_base()
test_image()
