SDMtoolbox Version 2.4
Date: 2/18/2018
Changes made in this version:

NEW Options: 
Added multi-cpu capabilities to the MaxEnt 'Spatial Jackknife' tool!  Less time waiting for modeling tuning!

NEW TOOLS: 
None

BUG FIXES:
None

SDMtoolbox Version 2.3
Date: 12/16/2018
Changes made in this version:

NEW TOOLS:  1 new tool!
SDM-> MaxEnt Tools->Trouble Shooting: Scrub ASCII Headers

BUG FIXES:
Added an option to the Extract by Mask tool to scrub ASCII headers for Maxent


SDMtoolbox Version 2.2D
Date: 9/16/2018
Changes made in this version:
BUG FIXES:
-Fixed another bug in Spatial Jackknife tool associated with replicates when spatial jackniffing - this was a result of a fix in 2.2c.

SDMtoolbox Version 2.2C
Date: 4/29/2018
Changes made in this version:
NEW TOOLS:  2 new tools!
Basic-> Raster Tools ->
-11f. Raster Calculator: Standardize 0-1 (Folder)
Landscape Connectivity Tools-> Genetic -> 
-Split SDM by input clade relationship- Inverse Distance Weighting

BUG FIXES:
-Fixed another bug in Spatial Jackknife tool associated with selecting models with 1 OER and 0.5 AUC (created as a bug)
-Fixed another bug in Spatial Jackknife tool associated with replicates when spatial jackniffing.
-Updated menu for Spatial Jacknife tool
-Added model paramterization criteron - sum of prediction rate and AUC values for Spatial Jacknife tool

SDMtoolbox Version 2.2
Date: 12/23/2017
Changes made in this version:
NEW TOOLS:  9 new tools!
Basic-> Raster Tools ->
-11b. Raster Calculator: Plus (Folder)
-11c. Raster Calculator: Subtract (Folder)
-11d. Raster Calculator: Times (Folder)
-11e. Raster Calculator: Times (Folder)
-2f. Multiband NetCDF to Separate Rasters
-2g. Multiband NetCDF to Separate Rasters (Folder)
-4c. Advance Downscale Grids (Folder)
SDM Tools-> 1.Universal Tools-> Microclim Tools ->
-Create Microclim Bioclim variable – single factor
-Create Microclim Bioclim variable – two factors
BUG FIXES:
-Fixed another bug in Spatial Jackknife tool associated with thresholds values
-Fixed a bug in ‘Sample by Buffered Local Adaptive Convex-Hull’ where it wouldn’t process more than a single species input.


SDMtoolbox Version: 2.1.0
Date: 12/21/2017
Changes: MAJOR RELEASE-IMPORTANT UPDATES SEE CORRESPONDING PAPER FOR CURRENT CHANGES.
NEW TOOLS:

Basic-> Raster Tools ->
-11b. Raster Calculator: Plus (Folder)
-11c. Raster Calculator: Subtract (Folder)
-11d. Raster Calculator: Times (Folder)
-11e. Raster Calculator: Times (Folder)
-2f. Multiband NetCDF to Separate Rasters
-2g. Multiband NetCDF to Separate Rasters (Folder)
-4c. Advance Downscale Grids (Folder)
SDM Tools-> 1.Universal Tools-> Microclim Tools -> 
-Create Microclim Bioclim variable - single factor
-Create Microclim Bioclim variable - two factors

BUG FIXES:
Fixed another bug in Spatial Jacknife tool assocated with thresholds values
Fixed a bug in 'Sample by Buffered Local Adaptive Convex-Hull' where it wouldnt process more than a single species input.

SDMtoolbox Version: 2.1.0
Date: 11/13/2017
Changes: MAJOR RELEASE-IMPORTANT UPDATES SEE CORRESPONDING PAPER FOR CURRENT CHANGES.
NEW TOOLS:
None
BUG FIXES:
Fixed a bug in Spatial Jacknife tool- do not use Version 2.0.0
Add a script to all tools to automatically check if spatial analysts in on.

SDMtoolbox Version: 2.0.0
Date: 9/3/2017
Changes: MAJOR RELEASE.  SEE CORRESPONDING PAPER FOR CURRENT CHANGES
Note python code contained in SDMtoolbox2.0 is open source. To access python code use password "dendrobates".  
If you have problems accessing code email: sdmtoolbox.help@gmail.com 

SDMtoolbox Version: 1.1c
Date: 3/13/2015
Changes:
NEW TOOLS:
None
BUG FIXES:
-Fixed a bug in the Universal SDM tools-> 1. Distribution Changes Between Binary SDMs that caused incorrect calcuations  
-Fixed several minor issues
OTHER:

SDMtoolbox Version: 1.1b
Date: 11/4/2014
Changes:
NEW TOOLS:
 - NetCDF to Raster tool
BUG FIXES:
 - Run Maxent: spatial jackknife tool. Fixed another error that arose when running a single replicate of spatial jackknifed models and more than 1 replicate for species with too few points to be spatial jackknifed. The error would cause the latter to not properly run.
 - Also added minimum number of occurrences needed model to tool menu
OTHER:


SDMtoolbox Version: 1.1a
Date: 10/14/2014
Changes:
NEW TOOLS:
 - Landscape Connectivity: Pairwise All Sites: Create Pairwise Distant Matrix
 - Basic Tools: Raster Files: 4b Upscale Grids (Folder)
BUG FIXES:
 - Run Maxent: spatial jackknife tool. Fixed an error that arose when running a single replicate of spatial jackknifed models and more than 1 replicate for species with too few points to be spatial jackknifed. The error would cause the latter to not properly run.
OTHER:

SDMtoolbox Version: 1.1
Date: 8/19/2014
Changes:
BUG FIXES:
 - Fixed a major error in the ranking of models in the Run Maxent: spatial jackknife tool.  Note this bug only manifested itself in a few circumstances, regardless I recommend rerunning all results obtained from SDMtoolbox 1.0-1.0b2. 
- Provided a solution to a menu issue associated with the Run Maxent: spatial jackknife tool.
OTHER:

SDMtoolbox Version: 1.0b2
Date: 6/26/2014
Changes:
BUG FIXES:
 - Fixed a menu item in the Spatial Jackknife tool that cause models to be extrapolated when clicked 'do not extrapolate'
-changed text: 'location of maxent jar file' to 'maxent jar file'

SDMtoolbox Version: 1.0b1
Date: 5/4/2014
Changes:
NEW TOOL:
 - Basic Tools: Raster Files: Define Projection (folder)
BUG FIXES:
 - Fixed an error to all tools using equal area-projection that caused errors in Europe and North America equal-area projections
 - Fixed an projection display error in Friction layer tool
 - Updates to 'Run Maxent tool' menu
 - Updated menus to all Maxent Background Selection tools, clarifying that all template rasters MUST be projected
 - Updated and added new distant search feature to the Gaussian Kernel Density of Sampling Localities 
 - Fixed an error associated with using polygon shapefiles as a mask in the extract by mask tool
OTHER:
  
SDMtoolbox Version: 1.0a
Date: 4/25/2014
Changes:
NEW TOOL:
    MaxEnt Tools: Background Selection via Bias Files scripts: Sample by Buffered Local Adaptive Convex-Hull
BUG FIXES:
  Fixed Bug in 'Run Maxent tool' that causes spaces to be introduced to regularization multiplier value folders
  Fixed two bugs associated with the two dispersal change tools that resulted in errors when file names had "." periods
OTHER:
  Cleaned up python scripts in all MaxEnt Tools: Background Selection via Bias Files scripts

  
SDMtoolbox Version: 1.0
Date: 4/11/2014
Changes: First Release


