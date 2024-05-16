import numpy as np

from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.core.window import Window

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.uix.slider import Slider
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, BooleanProperty
from kivy.vector import Vector
from kivy.clock import Clock


'''  QKD functions and variables '''

# Convention that Bob and Alice agree on in the preparation phase
MINUS_PI_8_BASIS = -1
ZERO_BASIS = 0
PI_8_BASIS = 1
PI_4_BASIS = 2

PROB_EQUAL = np.cos(np.pi/8) * np.cos(np.pi/8)
PROB_DIFFERENT = 1 - PROB_EQUAL

# Probability dictionaries
dico_0  = {
    (MINUS_PI_8_BASIS, ZERO_BASIS): [PROB_EQUAL, PROB_DIFFERENT],
    (MINUS_PI_8_BASIS, PI_8_BASIS): [0.5, 0.5],
    (MINUS_PI_8_BASIS, PI_4_BASIS): [PROB_DIFFERENT, PROB_EQUAL],
    (ZERO_BASIS, MINUS_PI_8_BASIS): [PROB_EQUAL, PROB_DIFFERENT],
    (ZERO_BASIS, PI_8_BASIS): [PROB_EQUAL, PROB_DIFFERENT],
    (ZERO_BASIS, PI_4_BASIS): [0.5, 0.5],
    (PI_8_BASIS, MINUS_PI_8_BASIS): [0.5, 0.5],
    (PI_8_BASIS, ZERO_BASIS): [PROB_EQUAL, PROB_DIFFERENT],
    (PI_8_BASIS, PI_4_BASIS): [PROB_EQUAL, PROB_DIFFERENT],
    (PI_4_BASIS, MINUS_PI_8_BASIS): [PROB_DIFFERENT, PROB_EQUAL],
    (PI_4_BASIS, ZERO_BASIS): [0.5, 0.5],
    (PI_4_BASIS, PI_8_BASIS): [PROB_EQUAL, PROB_DIFFERENT]
}

dico_1  = {
    (MINUS_PI_8_BASIS, ZERO_BASIS): [PROB_DIFFERENT, PROB_EQUAL],
    (MINUS_PI_8_BASIS, PI_8_BASIS): [0.5, 0.5],
    (MINUS_PI_8_BASIS, PI_4_BASIS): [PROB_EQUAL, PROB_DIFFERENT],
    (ZERO_BASIS, MINUS_PI_8_BASIS): [PROB_DIFFERENT, PROB_EQUAL],
    (ZERO_BASIS, PI_8_BASIS): [PROB_DIFFERENT, PROB_EQUAL],
    (ZERO_BASIS, PI_4_BASIS): [0.5, 0.5],
    (PI_8_BASIS, MINUS_PI_8_BASIS): [0.5, 0.5],
    (PI_8_BASIS, ZERO_BASIS): [PROB_DIFFERENT, PROB_EQUAL],
    (PI_8_BASIS, PI_4_BASIS): [PROB_DIFFERENT, PROB_EQUAL],
    (PI_4_BASIS, MINUS_PI_8_BASIS): [PROB_EQUAL, PROB_DIFFERENT],
    (PI_4_BASIS, ZERO_BASIS): [0.5, 0.5],
    (PI_4_BASIS, PI_8_BASIS): [PROB_DIFFERENT, PROB_EQUAL]
}

def measure_polarization(basis_a, basis_b):

    alice_bit = np.random.choice([0, 1], p=[0.5, 0.5])
    
    if basis_a == basis_b:
        bob_bit = alice_bit
    elif alice_bit == 0:
        bob_bit = np.random.choice([0, 1], p=dico_0[(basis_a, basis_b)])
    else:
        bob_bit = np.random.choice([0, 1], p=dico_1[(basis_a, basis_b)])

    return int(alice_bit), int(bob_bit)

def measure_polarization_eavesdropping(basis_a, basis_b, basis_e_a, basis_e_b):

    eve_alice_bit = np.random.choice([0, 1], p=[0.5, 0.5])
    
    if basis_e_a == basis_e_b:
        eve_bob_bit = eve_alice_bit
    elif eve_alice_bit == 0:
        eve_bob_bit = np.random.choice([0, 1], p=dico_0[(basis_e_a, basis_e_b)])
    else:
        eve_bob_bit = np.random.choice([0, 1], p=dico_1[(basis_e_a, basis_e_b)])

    if basis_e_a == basis_a:
        alice_bit = eve_alice_bit
    elif eve_alice_bit == 0:
        alice_bit = np.random.choice([0, 1], p=dico_0[(basis_a, basis_e_a)])
    else:
        alice_bit = np.random.choice([0, 1], p=dico_1[(basis_a, basis_e_a)])

    if basis_e_b == basis_b:
        bob_bit = eve_bob_bit
    elif eve_bob_bit == 0:
        bob_bit = np.random.choice([0, 1], p=dico_0[(basis_b, basis_e_b)])
    else:
        bob_bit = np.random.choice([0, 1], p=dico_1[(basis_b, basis_e_b)])

    return int(alice_bit), int(bob_bit), int(eve_alice_bit), int(eve_bob_bit)

def measure_polarization_eavesdropping_left(basis_a, basis_b, basis_e_a):

    eve_alice_bit = np.random.choice([0, 1], p=[0.5, 0.5])

    if basis_e_a == basis_a:
        alice_bit = eve_alice_bit
    elif eve_alice_bit == 0:
        alice_bit = np.random.choice([0, 1], p=dico_0[(basis_a, basis_e_a)])
    else:
        alice_bit = np.random.choice([0, 1], p=dico_1[(basis_a, basis_e_a)])

    if basis_e_a == basis_b:
        bob_bit = eve_alice_bit
    elif eve_alice_bit == 0:
        bob_bit = np.random.choice([0, 1], p=dico_0[(basis_b, basis_e_a)])
    else:
        bob_bit = np.random.choice([0, 1], p=dico_1[(basis_b, basis_e_a)])

    return int(alice_bit), int(bob_bit), int(eve_alice_bit)

def measure_polarization_eavesdropping_right(basis_a, basis_b, basis_e_b):

    eve_bob_bit = np.random.choice([0, 1], p=[0.5, 0.5])
    
    if basis_a == basis_e_b:
        alice_bit = eve_bob_bit
    elif eve_bob_bit == 0:
        alice_bit = np.random.choice([0, 1], p=dico_0[(basis_a, basis_e_b)])
    else:
        alice_bit = np.random.choice([0, 1], p=dico_1[(basis_a, basis_e_b)])

    if basis_b == basis_e_b:
        bob_bit = eve_bob_bit
    elif eve_bob_bit == 0:
        bob_bit = np.random.choice([0, 1], p=dico_0[(basis_e_b, basis_b)])
    else:
        bob_bit = np.random.choice([0, 1], p=dico_1[(basis_e_b, basis_b)])

    return int(alice_bit), int(bob_bit), int(eve_bob_bit)



''' Kivy widgets and animations '''


# offset photon - filter center when measuring
OFFSET = 12

class Source(Button):

    photon_alice = ObjectProperty(None)
    photon_bob = ObjectProperty(None)

    def on_touch_down(self, touch):
        dist = np.sqrt( pow(touch.pos[0] - self.center[0], 2) + pow(touch.pos[1] - self.center[1], 2) )
        if dist <= 38:  # radius of the circle
            return super(Source, self).on_touch_down(touch)
        else:
            return False
        
class Slider(Slider):
    pass

class Photon(Widget):

    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class Filter(Widget):
    pass

class Slit(Widget):
    angle = NumericProperty(0)

class Button(Button):

    def on_touch_down(self, touch):
        dist = np.sqrt( pow(touch.pos[0] - self.center[0], 2) + pow(touch.pos[1] - self.center[1], 2) )
        if dist <= 38:  # radius of the circle
            return super(Button, self).on_touch_down(touch)
        else:
            return False
        
class Button_Switch(Button):

    active = BooleanProperty(False)

    def change_mode(self, active):
        
        if active == True:  
            active = False
        elif active == False:
            active = True

    def get_mode(self, active):
        if active:
            return True
        else:
            return False

class Angle(Label):
    pass

class Switch(Switch):
    pass
        

def angle_to_basis(x):

    match x:
        case -22.5:
            return -1
        case 0:
            return 0
        case 22.5:
            return 1
        case 45:
            return 2
        

class E91Simulation(Widget):

    photon_alice = ObjectProperty(None)
    photon_bob = ObjectProperty(None)

    alice_filter = ObjectProperty(None)
    bob_filter = ObjectProperty(None)
    eve_left_filter = ObjectProperty(None)
    eve_right_filter = ObjectProperty(None)

    alice_slit = ObjectProperty(None)
    bob_slit = ObjectProperty(None)
    eve_left_slit = ObjectProperty(None)
    eve_right_slit = ObjectProperty(None)

    a_bit_old = NumericProperty(0)
    b_bit_old = NumericProperty(0)
    e_left_bit_old = NumericProperty(0)
    e_right_bit_old = NumericProperty(0)

    a_bit = NumericProperty(0)
    b_bit = NumericProperty(0)
    e_left_bit = NumericProperty(0)
    e_right_bit = NumericProperty(0)

    switch_eve = ObjectProperty(None)
    switch_eve_left = ObjectProperty(None)
    switch_eve_right = ObjectProperty(None)
    switch_expert_mode = ObjectProperty(None)

    slider = ObjectProperty(None)

    # Counters
    counts_a1b1 = np.zeros((2,2))
    counts_a1b3 = np.zeros((2,2))
    counts_a3b1 = np.zeros((2,2))
    counts_a3b3 = np.zeros((2,2))

    # Probabilities
    prob_a1b1 = np.zeros((2,2))
    prob_a1b3 = np.zeros((2,2))
    prob_a3b1 = np.zeros((2,2))
    prob_a3b3 = np.zeros((2,2))

    # Correlation Coefficients
    E_a1b1 = NumericProperty(0.0)
    E_a1b3 = NumericProperty(0.0)
    E_a3b1 = NumericProperty(0.0)
    E_a3b3 = NumericProperty(0.0)

    S = NumericProperty(0.0)

    def change_mode_switch_eve(self):
        
        if self.switch_eve.active == True:  
            self.switch_eve.active = False
        else:
            self.switch_eve.active = True

    def change_mode_switch_eve_left(self):
        
        if self.switch_eve_left.active == True:  
            self.switch_eve_left.active = False
        else:
            self.switch_eve_left.active = True

    def change_mode_switch_eve_right(self):
        
        if self.switch_eve_right.active == True:  
            self.switch_eve_right.active = False
        else:
            self.switch_eve_right.active = True

    def change_mode_switch_expert(self):
        
        if self.switch_expert_mode.active == True:  
            self.switch_expert_mode.active = False
        else:
            self.switch_expert_mode.active = True

    def change_alice_angle(self):

        match self.alice_slit.angle:
            case 0:
                self.alice_slit.angle = 22.5
            case 22.5:
                self.alice_slit.angle = 45
            case 45:
                self.alice_slit.angle = 0

        
    def change_bob_angle(self):

        match self.bob_slit.angle:
            case -22.5:
                self.bob_slit.angle = 0
            case 0:
                self.bob_slit.angle = 22.5
            case 22.5:
                self.bob_slit.angle = -22.5
        

    def change_e_left_angle(self):

        match self.eve_left_slit.angle:
            case 0:
                self.eve_left_slit.angle = 22.5
            case 22.5:
                self.eve_left_slit.angle = 45
            case 45:
                self.eve_left_slit.angle = 0

    
    def change_e_right_angle(self):

        match self.eve_right_slit.angle:
            case -22.5:
                self.eve_right_slit.angle = 0
            case 0:
                self.eve_right_slit.angle = 22.5
            case 22.5:
                self.eve_right_slit.angle = -22.5


    def emission(self):

        self.photon_alice.center = self.center
        self.photon_bob.center = self.center

        velocity_x = (self.center_x - self.alice_filter.center_x)/60
        velocity_y = 10

        self.photon_alice.velocity = Vector(-velocity_x, velocity_y)
        self.photon_bob.velocity   = Vector(velocity_x, velocity_y)

        basis_a   = angle_to_basis(self.alice_slit.angle)
        basis_b   = angle_to_basis(self.bob_slit.angle)
        basis_e_a = angle_to_basis(self.eve_left_slit.angle)
        basis_e_b = angle_to_basis(self.eve_right_slit.angle)

        for _ in range(0, self.slider.value):

            if self.switch_eve.active == False:
                self.a_bit_old, self.b_bit_old = measure_polarization(basis_a, basis_b)
            elif self.switch_eve_left.active and self.switch_eve_right.active:
                self.a_bit_old, self.b_bit_old, self.e_left_bit_old, self.e_right_bit_old = measure_polarization_eavesdropping(basis_a, basis_b, basis_e_a, basis_e_b)
            elif self.switch_eve_left.active:
                self.a_bit_old, self.b_bit_old, self.e_left_bit_old = measure_polarization_eavesdropping_left(basis_a, basis_b, basis_e_a)
            elif self.switch_eve_right.active:
                self.a_bit_old, self.b_bit_old, self.e_right_bit_old = measure_polarization_eavesdropping_right(basis_a, basis_b, basis_e_b)
        
            if (basis_a, basis_b) == (ZERO_BASIS, MINUS_PI_8_BASIS):
                self.counts_a1b1[self.a_bit_old, self.b_bit_old] += 1
                self.prob_a1b1 = self.counts_a1b1 / np.sum(self.counts_a1b1)
                self.E_a1b1 = round(float(self.prob_a1b1[0,0] + self.prob_a1b1[1,1] - self.prob_a1b1[1,0] - self.prob_a1b1[0,1]), 4)
            elif (basis_a, basis_b) == (ZERO_BASIS, PI_8_BASIS):
                self.counts_a1b3[self.a_bit_old, self.b_bit_old] += 1
                self.prob_a1b3 = self.counts_a1b3 / np.sum(self.counts_a1b3)
                self.E_a1b3 = round(float(self.prob_a1b3[0,0] + self.prob_a1b3[1,1] - self.prob_a1b3[1,0] - self.prob_a1b3[0,1]), 4)
            elif (basis_a, basis_b) == (PI_4_BASIS, MINUS_PI_8_BASIS):
                self.counts_a3b1[self.a_bit_old, self.b_bit_old] += 1
                self.prob_a3b1 = self.counts_a3b1 / np.sum(self.counts_a3b1)
                self.E_a3b1 = round(float(self.prob_a3b1[0,0] + self.prob_a3b1[1,1] - self.prob_a3b1[1,0] - self.prob_a3b1[0,1]), 4)
            elif (basis_a, basis_b) == (PI_4_BASIS, PI_8_BASIS):
                self.counts_a3b3[self.a_bit_old, self.b_bit_old] += 1
                self.prob_a3b3 = self.counts_a3b3 / np.sum(self.counts_a3b3)
                self.E_a3b3 = round(float(self.prob_a3b3[0,0] + self.prob_a3b3[1,1] - self.prob_a3b3[1,0] - self.prob_a3b3[0,1]), 4)

        self.S = round(self.E_a1b1 + self.E_a1b3 - self.E_a3b1 + self.E_a3b3, 4)

    

    def update(self, dt):
        
        self.photon_alice.move()
        self.photon_bob.move()

        # For each frame, vertical velocity is inverted 
        if self.photon_alice.velocity_x != 0:
            self.photon_alice.velocity_y = - self.photon_alice.velocity_y
            self.photon_bob.velocity_y = - self.photon_bob.velocity_y

        if self.photon_alice.x < self.eve_left_filter.center_x - OFFSET:

            if self.switch_eve_left.active:
                self.photon_alice.opacity = 0

            if self.switch_eve_right.active:
                self.photon_bob.opacity = 0

            self.e_left_bit = self.e_left_bit_old
            self.e_right_bit = self.e_right_bit_old

        if self.photon_alice.x < self.eve_left_filter.center_x - 10 * OFFSET:
            self.photon_alice.opacity = 1
            self.photon_bob.opacity = 1

        if self.photon_alice.x < self.alice_filter.center_x - OFFSET:
            self.photon_alice.center = self.center
            self.photon_bob.center = self.center
            self.photon_alice.velocity = Vector(0, 0)
            self.photon_bob.velocity = Vector(0, 0)
            self.a_bit = self.a_bit_old
            self.b_bit = self.b_bit_old


class E91App(App):

    def build(self):

        sim = E91Simulation()
        Clock.schedule_interval(sim.update, 1.0/60.0)
        return sim


if __name__ == '__main__':
    E91App().run()
