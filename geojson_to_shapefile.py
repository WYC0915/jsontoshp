import json
import gdal, ogr
#from osgeo import gdal, ogr 

def create_polygon(coords):
    ring = ogr.Geometry(ogr.wkbLinearRing)
    for coord in coords:
        for xy in coord:
            ring.AddPoint(xy[0],xy[1])
            poly = ogr.Geometry(ogr.wkbPolygon)
            poly.AddGeometry(ring)
    return poly.ExportToIsoWkt()

def create_shp_with_geojson(json,geo_type):
    #支持中文路徑
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
    #屬性表字段支持中文
    gdal.SetConfigOption("SHAPE_ENCODING", "UTF-8")
    #創建shp數據
    driver = ogr.GetDriverByName("ESRI Shapefile")
    properties_temp=list(json['features'][0]['properties'])
    
    if geo_type=='Polygon' or geo_type=='MultiPolygon':
        polygon_data_source = driver.CreateDataSource("testPolygon.shp")
        polygon_layer = polygon_data_source.CreateLayer("testPolygon", geom_type=ogr.wkbPolygon)
        for i in range(0,len(properties_temp)):
            field_testfield = ogr.FieldDefn("{}".format(str(properties_temp[i])), ogr.OFTString)
            field_testfield.SetWidth(254)
            polygon_layer.CreateField(field_testfield)
    elif geo_type=='Point': #建立shapefile的檔案名稱,屬性表格格式
        point_data_source = driver.CreateDataSource("testPoint.shp")
        point_layer = point_data_source.CreateLayer("testPoint", geom_type=ogr.wkbPoint) #layer 屬性
        for i in range(0,len(properties_temp)):
            field_testfield = ogr.FieldDefn("{}".format(str(properties_temp[i])), ogr.OFTString)
            field_testfield.SetWidth(254)
            point_layer.CreateField(field_testfield) #加入屬性
    elif geo_type == 'LineString':
        polyline_data_source = driver.CreateDataSource("testLine.shp")
        polyline_layer = polyline_data_source.CreateLayer("testLine", geom_type=ogr.wkbLineString)
        for i in range(0,len(properties_temp)):
            field_testfield = ogr.FieldDefn("{}".format(str(properties_temp[i])), ogr.OFTString)
            field_testfield.SetWidth(254)
            polyline_layer.CreateField(field_testfield)
            
    for record in json['features']:
        geo = record.get("geometry")
        geo_type = geo.get('type')
        temp=list(record['properties'])
        
        if geo_type == 'Polygon':
            
            polygonCOOR = geo.get('coordinates')
            poly = create_polygon(polygonCOOR)
            if poly:
                feature = ogr.Feature(polygon_layer.GetLayerDefn())
                for i in range(0,len(temp)):
                    if str(record['properties']["{}".format(str(temp[i]))])=="":
                        feature.SetField("{}".format(str(temp[i])), "NULL")
                    else:
                        data=str(record['properties']["{}".format(str(temp[i]))])
                        data1=data.encode('utf-8')
                        data2=data1.decode('utf-8')
                        feature.SetField("{}".format(str(temp[i])), data2)
                area = ogr.CreateGeometryFromWkt(poly)
                polygon_layer.CreateFeature(feature)
                feature = None
        elif geo_type == 'MultiPolygon':
            
            feature = ogr.Feature(polygon_layer.GetLayerDefn())
            for i in range(0,len(temp)):
                if str(record['properties']["{}".format(str(temp[i]))])=="":
                    feature.SetField("{}".format(str(temp[i])), "NULL")
                else:
                    data=str(record['properties']["{}".format(str(temp[i]))])
                    data1=data.encode('utf-8')
                    data2=data1.decode('utf-8')
                    feature.SetField("{}".format(str(temp[i])), data2)
            
            gjson = ogr.CreateGeometryFromJson(str(geo))
            if gjson:
                feature.SetGeometry(gjson)
                polygon_layer.CreateFeature(feature)
                feature = None
        elif geo_type == 'Point':
            
            feature = ogr.Feature(point_layer.GetLayerDefn())
            for i in range(0,len(temp)):
                if str(record['properties']["{}".format(str(temp[i]))])=="":
                    feature.SetField("{}".format(str(temp[i])), "NULL")
                else:
                    data=str(record['properties']["{}".format(str(temp[i]))])
                    data1=data.encode('utf-8')
                    data2=data1.decode('utf-8')
                    feature.SetField("{}".format(str(temp[i])), data2)
            
            point_geo = ogr.CreateGeometryFromJson(str(geo))
            if point_geo:
                feature.SetGeometry(point_geo)
                point_layer.CreateFeature(feature)
                feature = None
                
        elif geo_type == 'LineString':
            
            feature = ogr.Feature(polyline_layer.GetLayerDefn())
            for i in range(0,len(temp)):
                if str(record['properties']["{}".format(str(temp[i]))])=="":
                    feature.SetField("{}".format(str(temp[i])), "NULL")
                else:
                    data=str(record['properties']["{}".format(str(temp[i]))])
                    data1=data.encode('utf-8')
                    data2=data1.decode('utf-8')
                    feature.SetField("{}".format(str(temp[i])), data2)
            
            line_geo = ogr.CreateGeometryFromJson(str(geo))
            if point_geo:
                feature.SetGeometry(line_geo)
                polyline_layer.CreateFeature(feature)
                feature = None
        else:
            print('Could not discern geometry')
            
with open("D:/geojson_to_shapefile/地下水觀測井位置圖_彰化縣現存站.json", 'r', encoding="utf-8", newline='') as jsonfile:
    data = json.load(jsonfile)
    geo_type=str(data['features'][0]['geometry']['type'])
    #temp=list(data['features'][0]['properties'])
    print(geo_type)
    create_shp_with_geojson(data,geo_type)





