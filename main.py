import numpy as np
import random as rand
import matplotlib
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

class Mass:
  def __init__(self, mass, pos, id):
    self.id = id
    self.mass = mass
    self.pos = np.array(pos)
    self.vel = np.array([0,0])
  
  def calculate_new_vel(self, objects, dt):

    G = 6.67E-11
    vec_part = np.array([0,0])
    for obj in objects:
      if obj.id == self.id:
        continue
      pos_diff = np.subtract(obj.pos, self.pos)
      norm_diff = np.linalg.norm(pos_diff)
      scalar_part = G*obj.mass/norm_diff**3
      vec = np.multiply(scalar_part, pos_diff)
      vec_part = np.add(vec_part, vec)

    new_vel = np.multiply(dt, vec_part)
    new_vel = np.add(new_vel, self.vel)
    self.vel = new_vel
  
  def calculate_new_position(self, dt):
    dt_v = np.multiply(dt, self.vel)
    new_pos = np.add(self.pos, dt_v)
    self.pos = new_pos

  
class Universe:
  def __init__(self, num_objects, universe_size):
    self.num_objects = num_objects
    self.universe_size = universe_size
    self.xs = []
    self.ys = []
    self.positions = []
    self.objects = []
  
  def insert_manual_mass(self, mass, pos):
      object = Mass(mass, pos, len(self.objects))
      self.xs.append(pos[0])
      self.ys.append(pos[1])
      self.objects.append(object)

  def initialise_objects(self, min_mass, max_mass):
    for i in range(len(self.objects), self.num_objects + len(self.objects)):
      mass = np.random.uniform(min_mass, max_mass)
      pos_x = self.universe_size*np.random.uniform(-1,1)
      pos_y = self.universe_size*np.random.uniform(-1,1)
      pos = [pos_x, pos_y]
      object = Mass(mass, pos, i)
      self.xs.append(pos_x)
      self.ys.append(pos_y)
      self.objects.append(object)
    print("Objects initialised!")
  
  def evolution_step(self, dt):
    self.xs = []
    self.ys = []
    self.positions = []
    for obj in self.objects:
      obj.calculate_new_vel(self.objects, dt)
      obj.calculate_new_position(dt)
      self.xs.append(obj.pos[0])
      self.ys.append(obj.pos[1])
      self.positions.append(obj.pos)


size = 500
num_objects = 100
Universe = Universe(num_objects, size)
Universe.initialise_objects(1E10, 1E18)

fig = plt.figure(figsize=(7,7))
ax = plt.axes(xlim=(-size-50,size+50),ylim=(-size-50,size+50))
scatter=ax.scatter(x=Universe.xs, y=Universe.ys, s=4)

def update(frame_number):
  Universe.evolution_step(0.00005)
  positions = Universe.positions
  scatter.set_offsets(positions)
  return scatter,

anim = FuncAnimation(fig, update, interval=1, frames=10000)
writergif = matplotlib.animation.PillowWriter(fps=30) 
# anim.save('anim.gif', writer=writergif)
plt.show()


