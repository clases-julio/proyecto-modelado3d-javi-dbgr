import bpy
import math

'''*********************************************************************'''
'''Funciones comunes útiles para selección/activación/borrado de objetos'''
'''*********************************************************************'''
def seleccionarObjeto(nombreObjeto): # Seleccionar un objeto por su nombre
    bpy.ops.object.select_all(action='DESELECT') # deseleccionamos todos...
    bpy.data.objects[nombreObjeto].select = True # ...excepto el buscado

def activarObjeto(nombreObjeto): # Activar un objeto por su nombre
    bpy.context.scene.objects.active = bpy.data.objects[nombreObjeto]

def borrarObjeto(nombreObjeto): # Borrar un objeto por su nombre
    seleccionarObjeto(nombreObjeto)
    bpy.ops.object.delete(use_global=False)

def borrarObjetos(): # Borrar todos los objetos
    if(len(bpy.data.objects) != 0):
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)

def seleccionar_coleccion(nombre):
    for object in bpy.data.collections[nombre].all_objects:
        object.select_set(True)

'''****************************************************************'''
'''Clase para realizar transformaciones sobre objetos seleccionados'''
'''****************************************************************'''
class Seleccionado:
    def mover(v):
        bpy.ops.transform.translate(
            value=v, constraint_axis=(True, True, True))

    def escalar(v):
        bpy.ops.transform.resize(value=v, constraint_axis=(True, True, True))
    
    def duplicar(v):
        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'})


    def rotarX(v):
        bpy.ops.transform.rotate(value=v, orient_axis='X')

    def rotarY(v):
        bpy.ops.transform.rotate(value=v, orient_axis='Y')

    def rotarZ(v):
        bpy.ops.transform.rotate(value=v, orient_axis='Z')

'''**********************************************************'''
'''Clase para realizar transformaciones sobre objetos activos'''
'''**********************************************************'''
class Activo:
    def posicionar(v):
        bpy.context.object.location = v

    def escalar(v):
        bpy.context.object.scale = v

    def rotar(v):
        bpy.context.object.rotation_euler = v

    def renombrar(nombreObjeto):
        bpy.context.object.name = nombreObjeto

'''**************************************************************'''
'''Clase para realizar transformaciones sobre objetos específicos'''
'''**************************************************************'''
class Especifico:
    def escalar(nombreObjeto, v):
        bpy.data.objects[nombreObjeto].scale = v

    def posicionar(nombreObjeto, v):
        bpy.data.objects[nombreObjeto].location = v

    def rotar(nombreObjeto, v):
        bpy.data.objects[nombreObjeto].rotation_euler = v

'''************************'''
'''Clase para crear objetos'''
'''************************'''
class Objeto:
    def crearCubo(objName):
        bpy.ops.mesh.primitive_cube_add(size=0.5, location=(0, 0, 0))
        Activo.renombrar(objName)

    def crearEsfera(objName):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(0, 0, 0))
        Activo.renombrar(objName)

    def crearCono(objName):
        bpy.ops.mesh.primitive_cone_add(radius1=0.5, location=(0, 0, 0))
        Activo.renombrar(objName)
    
    def crearCilindro(objName, r, d):
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d, location=(0, 0, 0))
        Activo.renombrar(objName)


def create_body(collection_name):
    collection = bpy.data.collections.new(name=collection_name)
    bpy.context.scene.collection.children.link(collection)

    Objeto.crearCubo("main_body")
    Seleccionado.escalar((6, 12, 1))
    object = bpy.context.active_object
    bpy.data.collections[collection_name].objects.link(object)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=0.3, location=(1.65, 2, 0))
    Activo.rotar((0, math.pi / 2, 0))
    object = bpy.context.active_object
    bpy.data.collections[collection_name].objects.link(object)


    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=0.3, location=(-1.65, 2, 0))
    Activo.rotar((0, math.pi / 2, 0))
    object = bpy.context.active_object
    bpy.data.collections[collection_name].objects.link(object)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=0.3, location=(-1.65, -2, 0))
    Activo.rotar((0, math.pi / 2, 0))
    object = bpy.context.active_object
    bpy.data.collections[collection_name].objects.link(object)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=0.3, location=(1.65, -2, 0))
    Activo.rotar((0, math.pi / 2, 0))
    object = bpy.context.active_object
    bpy.data.collections[collection_name].objects.link(object)

    seleccionar_coleccion(collection_name)
    bpy.ops.object.join()



def create_wheel(collection_name):
    collection = bpy.data.collections.new(name=collection_name)
    bpy.context.scene.collection.children.link(collection)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.8, depth=0.4, location=(0, 0, 0))
    Activo.rotar((0, math.pi / 2, 0))
    object = bpy.context.active_object
    bpy.data.collections[collection_name].objects.link(object)

    bpy.ops.mesh.primitive_torus_add(align='WORLD', location=(0, 0, 0), rotation=(0, 0, 0), major_radius=0.8, minor_radius=0.25, abso_major_rad=1.25, abso_minor_rad=0.75)
    Activo.rotar((0, math.pi / 2, 0))
    object = bpy.context.active_object
    bpy.data.collections[collection_name].objects.link(object)
  

def create_container(collection_name):
    collection = bpy.data.collections.new(name=collection_name)
    bpy.context.scene.collection.children.link(collection)

    Objeto.crearCubo("wall_1")
    Seleccionado.escalar((5, 0.4, 2.5))
    object = bpy.context.active_object
    bpy.data.collections[collection_name].objects.link(object)

    Objeto.crearCubo("wall_2")
    Seleccionado.escalar((5, 0.4, 2.5))
    Seleccionado.mover((0, 2.7, 0))
    object = bpy.context.active_object
    bpy.data.collections[collection_name].objects.link(object)

    Objeto.crearCubo("wall_3")
    Seleccionado.escalar((0.4, 5, 2.5))
    Seleccionado.mover((1.15, 1.35, 0))
    object = bpy.context.active_object
    bpy.data.collections[collection_name].objects.link(object)

    Objeto.crearCubo("wall_4")
    Seleccionado.escalar((0.4, 5, 2.5))
    Seleccionado.mover((-1.15, 1.35, 0))
    object = bpy.context.active_object
    bpy.data.collections[collection_name].objects.link(object)



def main():
    borrarObjetos()
    for collection in bpy.data.collections:
        bpy.data.collections.remove(collection)
    

    create_body("body")
    collection = bpy.data.collections["body"]
    

    create_wheel("wheel_1")
    seleccionar_coleccion("wheel_1")
    Seleccionado.mover((1.9, 2, 0))
    collection = bpy.data.collections["wheel_1"]

    create_container("container")
    seleccionar_coleccion("container")
    Seleccionado.mover((0, 0, 0))
    collection = bpy.data.collections["container"]





if __name__ == "__main__":
    main()
