from gameobject import GameObject, Location, Prop, Actor

class Scenario(GameObject):
    def __init__(self, name: str, desc: dict) -> None:
        super().__init__(name, desc)

    def move(self, object: GameObject, source: GameObject, destination: GameObject):
        destination.append(source.remove(object))

    def use(self, object: Prop):
        if isinstance(object, Prop):
            object.Use()

def scenario_TheCabin(game):
    scenario = Scenario("The Cabin", {"desc":"You are lost on a cold night and find a cabin"})
    #scenario.update(pack(Actor("player", {"player": "Person"})))
    scenario.append(Location("outside", {"outside": "dark and cold"}))
    scenario.append(Location("house", {"room": "warm and cozy"}))
    
    scenario.getgo(['outside']).append(Prop("tree", {"leaves": "Green", "branches": "sturdy"}, lambda: game.ActionResponse(f"{game.player.name} climbs on Tree")))
    scenario.getgo(['outside']).append(Prop("house", {"inside": "Homely"}, lambda: None))
    scenario.getgo(['outside', "house"]).append(Prop("door", {"color": "Green"}, lambda: game.ActionMove(['outside', game.player.name], ['house'])))
    scenario.getgo(['outside', "house", "door"]).append(Prop("window", {"glass": "Green"}, None))

    scenario.getgo(['house']).append(Prop("chair", {"chair": "wooden"}, lambda: game.ActionResponse(f"{game.player.name} sits on Chair")))
    scenario.getgo(['house']).append(Prop("door", {"door": "Green", "outside": "Cold and Dark"}, lambda: game.ActionMove(['house', game.player.name], ['outside'])))

    return scenario