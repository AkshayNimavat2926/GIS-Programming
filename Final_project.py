import os ## To import functions needed for the task
from qgis.core import (QgsVectorLayer)
from qgis.PyQt.QtCore import (QVariant)



# Location of the file to be retrived and use on the program
filepath = "C:/Users/axayn/GIS_Programming/Major_project/Shapefiles/"
inputShapefileA = "Geology.shp"
inputShapefileB = "20MDEM.tif"
inputShapefileC = "Bio_Regions.shp"
inputShapefileD = "Rainfall.shp"


# Assigned file to the raster and vector files to be used in the program.
DEMRasLayer = iface.addRasterLayer((filepath+inputShapefileB), inputShapefileB[:-4], "gdal")
GeoVecLayer = iface.addVectorLayer((filepath + inputShapefileA), inputShapefileA[:-4], "ogr")
BioVecLayer = iface.addVectorLayer((filepath + inputShapefileC), inputShapefileC[:-4], "ogr")
RfVecLayer = iface.addVectorLayer((filepath + inputShapefileD), inputShapefileD[:-4], "ogr")
add gpkg file
path_to_gpkg = "C:/Users/axayn/GIS_Programming/Major_project/Shapefiles/Study_area.gpkg"
gpkg_Study_area_layer = path_to_gpkg + "|layername=Study_area"
vlayer = QgsVectorLayer(gpkg_Study_area_layer, "Study_area", "ogr")
if not vlayer.isValid():
    print("Layer failed to load!")
else:
    QgsProject.instance().addMapLayer(vlayer)
    
Performed slope analysis from DEM to generate the watershed.
    
processing.runAndLoadResults("native:slope", { 'INPUT' : 'C:/Users/axayn/GIS_Programming/Major_project/Shapefiles/20MDEM.tif', 'OUTPUT' : 'C:/Users/axayn/GIS_Programming/Major_project/Shapefiles/Slope.tif', 'Z_FACTOR' : 1 })

Now we need to add one field called value for rainfall data as per research paper's described weight to individual factors.
Here it will be 0 for 50mm rain and 1 for 100 mm rain.
features = RfVecLayer.getFeatures()

caps = RfVecLayer.dataProvider().capabilities()
if caps & QgsVectorDataProvider.AddAttributes:
    res = RfVecLayer.dataProvider().addAttributes([QgsField('Value', QVariant.String)])
    RfVecLayer.updateFields()

Following code will show all the fields as well as newly added value field in python console.
for field in RfVecLayer.fields():
    print(field.name())

 The code below is commented out because at this stage it is not required but one can use this code to delete the additional fields which might get added to the attribute table.
if caps & QgsVectorDataProvider.DeleteAttributes:
    res = RfVecLayer.dataProvider().deleteAttributes([4])
    RfVecLayer.updateFields()

Rasterize rainfall layer based on given weight

processing.runAndLoadResults("gdal:rasterize", {'INPUT':'C:/Users/axayn/GIS_Programming/Major_project/Shapefiles/Rainfall.shp','FIELD':'Value','BURN':0,'UNITS':0,'WIDTH':100,'HEIGHT':100,'EXTENT':'2126679.353000000,2294236.972000000,2631118.887000000,2827183.369000000 [EPSG:3111]','NODATA':0,'OPTIONS':'','DATA_TYPE':5,'INIT':None,'INVERT':False,'EXTRA':'','OUTPUT':'C:/Users/axayn/GIS_Programming/Project2/RR1.tif'})
processing.runAndLoadResults("gdal:rasterize", {'INPUT':'C:/Users/axayn/GIS_Programming/Major_project/Shapefiles/Bio_Regions.shp','FIELD':'value','BURN':0,'UNITS':0,'WIDTH':100,'HEIGHT':100,'EXTENT':'140.962408733,142.743504991,-35.748582815,-33.981389858 [EPSG:4283]','NODATA':0,'OPTIONS':'','DATA_TYPE':5,'INIT':None,'INVERT':False,'EXTRA':'','OUTPUT':'C:/Users/axayn/GIS_Programming/Project2/Bio_ranked.tif'})