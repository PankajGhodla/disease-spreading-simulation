# COMPSCI 130, Semester 012019
# Project Two - Virus
# Name - Pankaj Ghodla

import turtle
import random
import math


# used to infect
class Virus:
    """ Class used to represent a virus and infect a person with it. 
    Note: "black" colour is reserved to represent a healthy person. 
    """

    def __init__(self, colour, duration):
        """ Initialises the Virus class by assigning it a colour and duration. """
        self.colour = colour
        self.duration = duration


# This class represents a person
class Person:
    """ Class used to represent a person. 
    In this class black colour is reserved for a healthy person.
     """

    def __init__(self, world_size):
        """ Initialises the Person class by assigning it a world_size, radius,
        location, destination, infected_hours and virus_duration. 
        """
        self.world_size = world_size
        self.radius = 7
        self.location = (0, 0)
        self.destination = self._get_random_location()
        self.colour = "black"
        self.infected_hours = 0
        self.virus_duration = 0

    # random locations are used to assign a destination for the person
    # the possible locations should not be closer than 1 radius to the edge of the world
    def _get_random_location(self):
        """ This is a protected method. It returns a random location within the frame 
        (box) of the world. This random location is never closer than 1 radius to the 
        edge of the world frame.  
        """
        location_des = []
        location_des.append(
            random.randint(-(self.world_size[0]/2 - self.radius),
                           self.world_size[0]/2 - self.radius))
        location_des.append(
            random.randint(-(self.world_size[1]/2 - self.radius),
                           self.world_size[1]/2 - self.radius))
        return tuple(location_des)

    # returns true if within 1 radius
    def reached_destination(self):
        """ If the location of the person is closer than 1 radius to the destination, 
        return True.
        """
        x = abs(self.destination[0] - self.location[0])
        y = abs(self.destination[1] - self.location[1])
        if self.radius**2 > x**2 + y**2:
            return True
        else:
            return False

    # PART C returns true if the distance between self and other is less than the diameter
    def collides(self, other):
        """ If the distance between self (person) and other (another person) is closer 
        less than the diameter, return True. 

        Keyword argument:
        other -- a object of another person 
        """
        diff_x = self.location[0] - other.location[0]
        diff_y = self.location[1] - other.location[1]
        if diff_x**2 + diff_y**2 < (self.radius * 2) ** 2:
            return True
        else:
            return False

    # PART C given a list of people, return a list containing only
    # those people who are in contact with self
    def collision_list(self, list_of_people):
        """ Returns a list of people (object), who are in contact with self (object) i.e. 
        the distance between the location of self and location of others (people in the list,
        other than self itself) is less than the diameter. 

        Keyword argument:
        list_of_people -- the list of people in the world.
        """
        collision_with = []
        for i in list_of_people:
            if self.collides(i) == True and i != self:
                collision_with.append(i)
        return collision_with

    # infect a person with the given virus
    def infect(self, virus):
        """ Infect a person with the given virus.

        Keyword argument:
        virus -- a object of the virus class.
        """
        self.virus_duration = virus.duration
        self.colour = virus.colour

    # cures the person if infection
    def cured(self):
        """ Cures the person (if infected), by changing the colour and infected_hours. """
        self.colour = "black"
        self.infected_hours = 0

    # increase hours of sickness, check if duration of virus is reached.  If the
    # duration is reached then the person is cured
    def progress_illness(self):
        """ Increases infected_hours by one, then checks if the infected_hours has reached the
        virus_duration. If the duration is reached, it cures the person. 
        """
        self.infected_hours += 1
        if self.infected_hours >= self.virus_duration:
            self.cured()

    # draw a person using a dot.  Use colour if implementing Viruses
    def draw(self):
        """ Draws the person as a dot at current location and uses colours other than black to 
        indicate infection i.e. infected by a virus. 
        """
        turtle.goto(self.location[0], self.location[1])
        turtle.dot(self.radius * 2, self.colour)

    # moves person towards the destination
    def move(self):
        """ Moves the person (dot) half a radius towards the destination. """
        angle = math.atan2(- self.location[1] + self.destination[1], -
                           self.location[0] + self.destination[0])
        self.location = (self.location[0] + math.cos(angle)*self.radius/2,
                         self.location[1] + math.sin(angle)*self.radius/2)

    # Updates the person each hour.
    # - moves each person by calling the move method
    # - if the destination is reached then set a new destination
    # - progress any illness
    def update(self):
        """ Moves the person (dot) each hour. If the person (dot) has reached its destination 
        then choses a random destination (by calling '_get_random_location' method). It also 
        process any illness by calling 'progress_illness' method.
        """
        self.move()
        if self.reached_destination() == True:
            self.destination = self._get_random_location()
        if self.colour != "black":
            self.progress_illness()


class World:
    """ Class used to represent the world, in which all the people moves around."""

    def __init__(self, width, height, n):
        """ Initialises the World class by assigning it a size, hours(time passed),
        list of people and virus list. 
        """
        self.size = (width, height)
        self.hours = 0
        self.people = []
        self.virus_list = [Virus("red", 100), Virus("blue", 150)]  # list of viruses
        for i in range(n):
            self.add_person()

    # add a person to the list
    def add_person(self):
        """ Adds a person in the list of people in the world. """
        person = Person(self.size)
        self.people.append(person)

    # choose a random person to infect and infect with a Virus
    def infect_person(self):
        """ Choses a random healthy person (not infected my any virus) to infect 
        it with a virus (virus randomly chosen if there are more than one virus). 
        If all the people in the world are already infected than nothing happens. 
        """
        people_not_infected = []
        for i in self.people:
            if i.colour == "black":
                people_not_infected.append(i)
        if len(people_not_infected) >= 1:
            random_number = random.randint(0, len(people_not_infected) - 1)
            random_person = people_not_infected[random_number]
            virus = random.choice(self.virus_list)  #randomly choosing virus from the list
            random_person.infect(virus)

    # remove all infections from all people
    def cure_all(self):
        """ Cures all the people in the world by calling 'cured' method in 
        'Person' class for each person in the world. 
        """
        for i in self.people:
            i.cured()

    # Part C check for collisions and pass infection to other people
    def update_infections_slow(self):
        """ Checks if a infected person is in contact with a healthy person, if there are 
        in contact, infected person infects that healthy person with the virus it has. 
        """
        for i in self.people:
            if i.colour != "black":
                people_in_contact = i.collision_list(self.people)
                for j in self.virus_list:
                    if j.colour == i.colour:
                        break
                for k in people_in_contact:  # only infects the people who are not
                    if k.colour == "black":  # alerady infected with a virus.
                        k.infect(j)

    # simulate one hour in the world.
    # - increase hours passed.
    # - update all people
    # - update all infection transmissions
    def simulate(self):
        """ Increases the hours by 1. Calls the 'update' method of the 'Person' class for each
        person in the world and calls 'update_infections_slow'.
        """
        self.hours += 1
        for i in self.people:
            i.update()
        self.update_infections_slow()

    # Count the number of infected people
    def count_infected(self):
        """ Returns the counts the number of poeple infected by a virus in the world"""
        infected = 0
        for i in self.people:
            if i.colour != "black":
                infected += 1
        return infected

    # Draw the world.  Perform the following tasks:
    #   - clear the current screen
    #   - draw all the people
    #   - draw the box that frames the world
    #   - write the number of hours and number of people infected at the top of the frame
    def draw(self):
        """ Draws every person in the world. Draws the frame (box). Write the hours and infected
        people in the world at the top left and top centre of the frame, respectively. 
        """
        turtle.clear()
        turtle.penup()
        for i in self.people:
            i.draw()
        turtle.goto(- self.size[0]/2, self.size[1]/2)
        turtle.right(90)
        turtle.pendown()

        for i in range(2):  # draws the frame
            turtle.forward(self.size[0])
            turtle.right(90)
            turtle.forward(self.size[1])
            turtle.right(90)
        turtle.right(-90)
        turtle.penup()

        turtle.goto(- self.size[0]/2, self.size[1]/2)
        turtle.write(f"Hours: {self.hours}", False)
        turtle.goto(0, self.size[1]/2)
        infected = self.count_infected()
        turtle.write(f"Infected = {infected}", False, align="center")


# ---------------------------------------------------------
# Should not need to alter any of the code below this line
# ---------------------------------------------------------
class GraphicalWorld:
    """ Handles the user interface for the simulation

    space - starts and stops the simulation
    'z' - resets the application to the initial state
    'x' - infects a random person
    'c' - cures all the people
    """

    def __init__(self):
        self.WIDTH = 800
        self.HEIGHT = 600
        self.TITLE = 'COMPSCI 130 Project One'
        self.MARGIN = 50  # gap around each side
        self.PEOPLE = 200  # number of people in the simulation
        self.framework = AnimationFramework(self.WIDTH, self.HEIGHT, self.TITLE)

        self.framework.add_key_action(self.setup, 'z')
        self.framework.add_key_action(self.infect, 'x')
        self.framework.add_key_action(self.cure, 'c')
        self.framework.add_key_action(self.toggle_simulation, ' ')
        self.framework.add_tick_action(self.next_turn)

        self.world = None

    def setup(self):
        """ Reset the simulation to the initial state """
        print('resetting the world')
        self.framework.stop_simulation()
        self.world = World(self.WIDTH - self.MARGIN * 2,
                           self.HEIGHT - self.MARGIN * 2, self.PEOPLE)
        self.world.draw()

    def infect(self):
        """ Infect a person, and update the drawing """
        print('infecting a person')
        self.world.infect_person()
        self.world.draw()

    def cure(self):
        """ Remove infections from all the people """
        print('cured all people')
        self.world.cure_all()
        self.world.draw()

    def toggle_simulation(self):
        """ Starts and stops the simulation """
        if self.framework.simulation_is_running():
            self.framework.stop_simulation()
        else:
            self.framework.start_simulation()

    def next_turn(self):
        """ Perform the tasks needed for the next animation cycle """
        self.world.simulate()
        self.world.draw()


# This is the animation framework
# Do not edit this framework
class AnimationFramework:
    """This framework is used to provide support for animation of
       interactive applications using the turtle library.  There is
       no need to edit any of the code in this framework.
    """

    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.title = title
        self.simulation_running = False
        self.tick = None  # function to call for each animation cycle
        self.delay = 1  # smallest delay is 1 millisecond
        turtle.title(title)  # title for the window
        turtle.setup(width, height)  # set window display
        turtle.hideturtle()  # prevent turtle appearance
        turtle.tracer(0, 0)  # prevent turtle animation
        turtle.listen()  # set window focus to the turtle window
        turtle.mode('logo')  # set 0 direction as straight up
        turtle.penup()  # don't draw anything
        turtle.setundobuffer(None)
        self.__animation_loop()

    def start_simulation(self):
        self.simulation_running = True

    def stop_simulation(self):
        self.simulation_running = False

    def simulation_is_running(self):
        return self.simulation_running

    def add_key_action(self, func, key):
        turtle.onkeypress(func, key)

    def add_tick_action(self, func):
        self.tick = func

    def __animation_loop(self):
        try:
            if self.simulation_running:
                self.tick()
            turtle.ontimer(self.__animation_loop, self.delay)
        except turtle.Terminator:
            pass


gw = GraphicalWorld()
gw.setup()
turtle.mainloop()  # Need this at the end to ensure events handled properly
