

def brainstrip(inim):
    import numpy as np
    import skimage
    from skimage.filters  import threshold_otsu
    from skimage import measure
    import mahotas
    from skimage.morphology import disk
    import skimage.morphology as morph
    import matplotlib.pyplot as plt

    if len(inim.shape) > 2:
        inim = inim[:,:,0]

    dimn = inim.shape
    th = threshold_otsu(inim)
    binim1 = inim > th
    print(th)

    eroded_image = morph.erosion(binim1, disk(3))
    plt.imshow(eroded_image)

    contours = measure.find_contours(eroded_image, 0.5)
    maxind = 0
    max = 0

    for i, contour in enumerate(contours):
        if contour.size > max:
                max = contour.size
                maxind = i


    n_dil = 10
    if len(contours) != 0:
        mask = np.where(measure.grid_points_in_poly(dimn, contours[maxind][:,:]), 1, 0)
        for i in range(0, n_dil):
            mask = skimage.morphology.binary_dilation(mask)
    else:
        mask = np.zeros(eroded_image.shape)
        
    closed_mask = mahotas.close_holes(mask)
    
    return np.where(closed_mask == 1, inim, 0)
    