from values import *

class storyTeller:
    def __init__(self, app, player_inventory):
        self.app = app
        self.player_inventory = player_inventory
        self.playerPerformanceTick = GameTick(15)
        self.playerPerformanceLowHealth = 0
        self.playerPerformanceHighHealth = 100
        self.playerPerformace = 1
        self.gunDropped = False
        self.drugMaxAmounts = {
            "Heroin" : 2,
            "Cocaine" : 3,
            "Diazepam" : 8,
        }

    def getGunDropRate(self):
        d = 0.01 * min([((4 - 3 * self.playerPerformace) ** 5), 100]) if not self.gunDropped else 0
        return d
    
    def checkGun(self, gun):
        for x in player_weapons:
            if gun == x.name:
                return False
        return True
    
    def getAmountInWorld(self, item):
        ammoAmountInWorld = self.player_inventory.get_amount_of_type(item.name)
        for x in interactables:
                if x.type == "item" and x.item.name == item.name:
                    ammoAmountInWorld += x.amount
        return ammoAmountInWorld
        

    def determineItemDropping(self, item, amount):
        if item.name in ["45 ACP", "9MM", "50 CAL", "12 GAUGE", "7.62x39MM", "5.56x45MM NATO", "Energy Cell", "HE Grenade", "Molotov"]:

            ammoAmountInWorld = self.getAmountInWorld(item)

            if item.name == "5.56x45MM NATO" and self.playerPerformace > 0.8:
                return False
            

            if ammoAmountInWorld + amount > item.max_stack:
                print("Skipping ammo drop:", item.name, amount, "Amount of ammo in world:", ammoAmountInWorld)
                return False
            
        elif item.name in ["Diazepam", "Cocaine", "Heroin"]:
            if random.uniform(0, self.app.player_actor_ref.sanity/100) < 1 - self.playerPerformace:
                if self.getAmountInWorld(item) + amount <= self.drugMaxAmounts[item.name]:
                    return True
            else:
                print("Not dropping drug")
                return False
            
        elif item.name in ["Sentry Turret", "Moving Turret"]:

            if item.name == "Sentry Turret":
                inWorld = len(turret_list)
            else:
                inWorld = len(turret_bro)

            if random.uniform(0.95, 1.02) > self.playerPerformace and self.getAmountInWorld(item) + inWorld + amount <= item.max_stack:
                return True
            else:
                return False
            
        else:
            if random.uniform(0.95, 1.02) > self.playerPerformace and self.getAmountInWorld(item) + amount <= item.max_stack:
                return True
            else:
                return False



        return True