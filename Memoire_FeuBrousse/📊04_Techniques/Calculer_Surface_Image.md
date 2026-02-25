# FireProject - Techniques
#ML #DL #Python 
[[Glossaire_Tags]]

Nom de la technique: ndimage.sum
Type: ML / DL / Python 
Description: En compte les pixel d'un type d'image, avec spicy (ndimage) 
Usage dans le projet: Calcul de surface brulée
exemples:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

image = plt.imread('bacteria.png')

image = image[:,:,0]
plt.imshow(image, cmap='gray')

image_2 = np.copy(image)
plt.hist(image_2.ravel(), bins=255)
plt.show()

image  = image < 0.6
plt.imshow(image)

open_x = ndimage.binary_opening(image)
plt.imshow(open_x)


from scipy import ndimage

label_image, n_labels = ndimage.label(open_x)
print(n_labels)

### Voici la technique
sizes = ndimage.sum(open_x, label_image, range(n_labels))

plt.scatter(range(n_labels), sizes)
```