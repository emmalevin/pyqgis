import qgis.core as qc
import qgis.utils as qu


WORKING_DIR = "/Users/emmalevin/desktop/“


def load_county_layer():
    # Load counties from shapefile and add as vector layer
    county_path =  WORKING_DIR  + "cb_2015_us_county_5m/cb_2015_us_county_5m.shp"
    county_layer = qu.iface.addVectorLayer(county_path, "county_layer", "ogr")
    return county_layer


def load_data_layer():
    # Load data from text file and add as vector layer
    data_path = WORKING_DIR + "data.txt"
    uri = 'file:///%s?crs=%s&delimiter=%s&xField=%s&yField=%s&decimal=%s' % (data_path, 'EPSG:4326', ',', 'Longitude', 'Latitude',     '.')
    data_layer = qu.iface.addVectorLayer(uri, "data_layer", "delimitedtext")
    return data_layer


def main():
    # Load county layer
    county_layer = load_county_layer()


    # Load data layer
    data_layer = load_data_layer()


    # Extract fields 34Distance, 50Distance, and 64Distance from data layer
    fields = data_layer.pendingFields()

    field_34Distance = fields[4].name()
    field_50Distance = fields[5].name()
    field_64Distance = fields[6].name()


    # Create buffers
    buffer_34Distance = processing.runalg('qgis:variabledistancebuffer',  data_layer, field_34Distance,  20, "false", None, progress=None)
    buffer_50Distance = processing.runalg('qgis:variabledistancebuffer',  data_layer, field_50Distance,  20, "false", None, progress=None)
    buffer_64Distance = processing.runalg('qgis:variabledistancebuffer',  data_layer, field_64Distance,  20, "false", None, progress=None)


    # Taking differences
    diff_buffer_50_34 = processing.runalg('qgis:difference', buffer_50Distance['OUTPUT'], buffer_34Distance['OUTPUT'], True, None, progress=None)
    diff_buffer_64_50 = processing.runalg('qgis:difference', buffer_64Distance['OUTPUT'], buffer_50Distance['OUTPUT'], True, None, progress=None)


    # Compute clip
    clip_vector = processing.runalg('qgis:clip', county_layer, buffer_34Distance['OUTPUT'], None, progress=None)


    # Add clip vector layer
    clip_layer = qc.QgsVectorLayer(clip_vector['OUTPUT'], "clip_layer",  "ogr")
    qc.QgsMapLayerRegistry.instance().addMapLayer(clip_layer)


    # Save clip attribute table as .csv
    outpath = WORKING_DIR + "test.csv"
    qc.QgsVectorFileWriter.writeAsVectorFormat(clip_layer, outpath, "CP1250", None, "CSV")


main()