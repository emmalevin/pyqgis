#Upload data
from qgis.core import *
from PyQt4.QtCore import *
import os

InFlnm = "Test.txt"
InDrPth = "/Users/emmalevin/Desktop/"
InFlPth =  "file:///" + InDrPth+ InFlnm

uri = InFlPth + "?delimiter=%s&xField=%s&yField=%s" % (",","Longitude","Latitude")

#COUNTY
county = QgsVectorLayer("/Users/emmalevin/Desktop/cb_2015_us_county_5m.shp", "county", "ogr")
county.isValid()

bh = QgsVectorLayer(uri,  InFlnm, "delimitedtext")
bh.isValid()
#bh.setCrs(QgsCoordinateReferenceSystem(31467, QgsCoordinateReferenceSystem.EpsgCrsId))
QgsMapLayerRegistry.instance().addMapLayer(bh)

#COUNTY
QgsMapLayerRegistry.instance().addMapLayer(county)

#Buffers
buffer1_layer = "/Users/emmalevin/Desktop/temp_r64kt.shp"
buffer2_layer = "/Users/emmalevin/Desktop/temp_r50kt.shp"
buffer3_layer = "/Users/emmalevin/Desktop/temp_r34kt.shp"


buffer1 = processing.runalg('qgis:variabledistancebuffer', bh, "64Distance", 20, "false", buffer1_layer)
buffer2 = processing.runalg('qgis:variabledistancebuffer', bh, "50Distance", 20, "false", buffer2_layer)
buffer3 = processing.runalg('qgis:variabledistancebuffer', bh, "34Distance", 20, "false", buffer3_layer)

buffer2_layer2 = "/Users/emmalevin/Desktop/temp_r50kt-r64kt.shp"
buffer3_layer2 = "/Users/emmalevin/Desktop/temp_r34kt-r50kt.shp"

#Differences
tmp1 = buffer1
tmp2 = processing.runalg('qgis:difference', buffer1_layer, buffer2_layer, True, buffer2_layer2)
tmp3 = processing.runalg('qgis:difference', buffer2_layer, buffer3_layer, True, buffer3_layer2)

#Clipping 
clip1_layer = "/Users/emmalevin/Desktop/temp_clip1.shp"
clip2_layer = "/Users/emmalevin/Desktop/temp_clip2.shp"
clip3_layer = "/Users/emmalevin/Desktop/temp_clip3.shp"


tmp4 = processing.runalg('qgis:clip', county, buffer1_layer, clip1_layer)
tmp5 = processing.runalg('qgis:clip', county, buffer2_layer2, clip2_layer)
tmp6 = processing.runalg('qgis:clip', county, buffer3_layer2, clip3_layer)

