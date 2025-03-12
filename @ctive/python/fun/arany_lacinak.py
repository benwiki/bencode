from animals import Human
from objects import Gate, Story, Size
import places
import postures
import expressions
import activities

def main():
    laci = Human(name="László")
    if laci.is_deaf:
        return
    counter = 0
    while laci.position != places.HERE:
        if counter >= 2:
            laci.set_position(places.HERE)
            expressions.destroy_demolish.say()
            break
        laci.call_to(places.HERE)
        counter += 1
    laci.set_posture(postures.SITTING)
    laci.set_position(places.LAP)
    if laci.is_fidgeting:
        while laci.pain_level < 0.2:
            laci.pinch()
        laci.sound_volume = 0
    laci.ear = Gate()
    laci.ear.open()
    laci.ear.send(Story(alias="tarka lepke", size=Size.SMALL))

    story(laci)

def story(laci: Human):
    ember = Human()
    ember.mustache.set_size(Size.LARGE)
    match ember.activity:
        case activities.go_to(places.WELL):
            if objects.BUCKET.is_empty:
                ember.do(activities.fill(objects.BUCKET))
