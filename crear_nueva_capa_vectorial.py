
mem_layer = QgsVectorLayer("Polygon", "Polygon", "memory") # Nombre, Tipo, ubicación
mem_layer.startEditing()

obtener_campos = attribute_dialog.feature().fields().toList() # Lista de campos de una capa como objetos tipo QgsField

# Agregar a la capa mem_layer los campos antes obtenidos y almacenados en obtener_campos
for i in obtener_campos:
    mem_layer.addAttribute(i)

mem_layer.commitChanges()

nuevo_campo = QgsField('fid', QVariant.Int) # parametros ("nombre del campo", tipo -> QVariant)
mem_layer.addAttribute(nuevo_campo)

# Definir el valor por defecto que debe tomar el campo id que está en la variable idx
layer.setDefaultValueDefinition(idx, QgsDefaultValue('maximum("id")+1'))
# Obtener los campos que tiene la capa layer
fields = layer.fields()
# Obtener el índice que tiene el campo id
field_idx = fields.indexOf('id')
# Iniciar edición del Formulario de la capa layer
config = layer.editFormConfig()
# Establecer el campo field_idx como sólo lectura
config.setReadOnly(field_idx , True) # parametros (índice del campo, True o False) True para determinar que es de solo lectura
# Insertar a la capa layer la configuración de su formulario
layer.setEditFormConfig(config)

config = layer.editFormConfig()
if config.readOnly(field_idx):
    config.setReadOnly(field_idx, True)
    layer.setEditFormConfig(config)

QgsVectorFileWriter.writeAsVectorFormat(layer, '/home/gop/Proyectos/jumundi25k/05_04_21/vl.shp',
                                        'utf-8', QgsCoordinateReferenceSystem('EPSG: 4326'),
                                        driverName="ESRI Shapefile")