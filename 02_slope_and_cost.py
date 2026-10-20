import numpy as np 
import matplotlib.pyplot as plt 

#Insert the clipped matrix 
input_path = '/kaggle/working/rwanda_dem_patch_1000x1000.npy'
patch = np.load(input_path)

#Slope computing 
grad_y, grad_x = np.gradient(patch, 10.0, 10.0)
slope_fraction = np.sqrt(grad_x**2 + grad_y**2)
slope_pct = slope_fraction * 100


#construct the physical cost matrix - if slope < 5% = low cost; above 5% cost increseas
cost_surface = 1.0 + (slope_pct / 5.0)**2

#Slope over 25% are impassable
cost_surface[slope_pct > 25.0] = 50.0 + (slope_pct[slope_pct > 25.0] - 25.0) * 10.0

#Saving
output_cost_path = "/kaggle/working/cost_surface_1000x1000.npy"
np.save(output_cost_path, cost_surface)


#Plot

plt.figure(figsize=(10, 8))
plt.imshow(slope_pct, cmap='inferno', vmin=0, vmax=35)
cbar = plt.colorbar()
cbar.set_label('Slope (%)')
plt.title("Slope Map Rwanda")
plt.xlabel("East (pixels - 10m)")
plt.ylabel("North (pixels - 10m)")
plt.savefig("/kaggle/working/Rwanda_Slope_Map.png", dpi=300, bbox_inches='tight')
plt.close()

