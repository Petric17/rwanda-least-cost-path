import rasterio
import matplotlib.pyplot as plt
import numpy as np 
from rasterio.windows import Window 
file_path = "/kaggle/input/datasets/irakozekelly/rwanda-digital-elevation-model-dem10m-resolution/DEM/dem_Rwanda_10m.tif"

with rasterio.open(file_path) as src:
    row_offset = src.height // 2
    col_offset = src.width // 2
    window = Window(col_off=col_offset, row_off=row_offset, width=1000, height=1000)
    patch = src.read(1, window=window).astype(np.float32)
    if src.nodata is not None:
        patch[patch == src.nodata] = np.nan


np.save("rwanda_dem_patch_1000x1000.npy", patch)

#Show

plt.figure(figsize=(10, 8))
plt.imshow(patch, cmap='terrain')
plt.colorbar(label="Altitude (m)")
plt.title("Clipped Terrain for Rwanda (10 km x 10 km @ 10m/px")
plt.xlabel("East (pixels - 10m)")
plt.ylabel("North (pixels - 10m)")
plt.savefig("Rwanda_Clipped_Terrain.png", dpi=300, bbox_inches='tight')
plt.show()
plt.close()
