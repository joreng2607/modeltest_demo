import pyglet
import os
import ratcave as rc
from pyglet.gl import gl
from pyglet.window import key

from modeltestSDK import SDKclient

client = SDKclient()
campaign_name = "STT"
test_name = "waveReg_1110"
sensor_name = "M206_COG"
dof = ["X", "Y", "Z", "Roll", "Pitch", "Yaw"]
sensors = []
for i in dof:
    sensors.append(sensor_name + " " + i)
campaign = client.campaign.get_by_name(campaign_name)
v2_test = campaign.get_tests(type='floater')[test_name]
all_timeseries = v2_test.get_timeseries()
curr_timeseries = [all_timeseries[sensor] for sensor in sensors]
for timeseries in curr_timeseries:
    timeseries.get_data_points()
times, X = curr_timeseries[0].to_arrays()
Y = curr_timeseries[1].to_arrays()[1]
Z = curr_timeseries[2].to_arrays()[1]
Roll = curr_timeseries[3].to_arrays()[1]
Pitch = curr_timeseries[4].to_arrays()[1]
Yaw = curr_timeseries[5].to_arrays()[1]


window = pyglet.window.Window(resizable=True)
keys = key.KeyStateHandler()
window.push_handlers(keys)

global f
f = 0

# get an object
model_file = rc.resources.obj_primitives
monkey = rc.WavefrontReader("M206v4.obj").get_mesh('Cube', scale= .1)
monkey.position.xyz = 0, 0, -3.5


monkey.uniforms['diffuse'] = [0.255,0.191,0.]  # RGB values

scene = rc.Scene(meshes=[monkey])


scene.camera.rotation.x = -15
scene.light.rotation.x = -15




def move_camera(dt):
    camera_speed = 3
    if keys[key.LEFT]:
        scene.camera.position.x -= camera_speed * dt
    if keys[key.RIGHT]:
        scene.camera.position.x += camera_speed * dt
    if keys[key.UP]:
        scene.camera.position.y -= camera_speed * dt
    if keys[key.DOWN]:
        scene.camera.position.y += camera_speed * dt
    if keys[key.PLUS]:
        scene.camera.position.z -= camera_speed * dt
    if keys[key.MINUS]:
        scene.camera.position.z += camera_speed * dt

    scene.light.position.x = scene.camera.position.x
    scene.light.position.y = scene.camera.position.y
    scene.light.position.z = scene.camera.position.z
pyglet.clock.schedule(move_camera)

global run
run = False



@window.event
def on_draw():
    with rc.default_shader:
        scene.draw()

t = 0


def update(dt):

    global run

    if keys[key.ENTER]:
        run = True


    global t
    if(run):
        if t>=len(X)-10:
            t=0
            print("DONE!")
            exit()
        else:
            t += 5
        global f
        f += 1
        filename = "img" + str(f).zfill(4) + ".png"
        kitten_stream = open(f'screenshots\{filename}', 'wb')
        pyglet.image.get_buffer_manager().get_color_buffer().save(filename , file=kitten_stream)
        kitten_stream.close()
    monkey.position.x = -0.005*X[t]
    monkey.position.z = 0.005*Y[t]
    monkey.position.y = 0.005*Z[t]
    monkey.rotation.x = Roll[t]
    monkey.rotation.y = Yaw[t]
    monkey.rotation.z = Pitch[t]



pyglet.clock.schedule_interval(update, 131/(len(X)/5))


pyglet.app.run()