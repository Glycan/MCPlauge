#Note
from org.bukkit.plugin.python import PythonPlugin

from org.bukkit.event.entity import EntityListener
from org.bukkit.event.entity import EntityDamageByEntityEvent

from org.bukkit.entity import PigZombie, Pig, Player

from org.bukkit.event.Event import Type, Priority

from org.bukkit.scheduler import BukkitScheduler


from org.bukkit.util import Vector

class Plauge(PythonPlugin):
    def onEnable(self):
        li = PigmanListener(self)
        pm = self.getServer().getPluginManager()
        pm.registerEvent(Type.CREATURE_SPAWN, li, Priority.Normal, self)
        pm.registerEvent(Type.ENTITY_TARGET, li, Priority.Normal, self)
        pm.registerEvent(Type.ENTITY_DEATH, li, Priority.Normal, self)
        print "Plauge enabled"

    def onDisable(self):
        print "Plauge disabled"
        
    def onCommand(self, sender, command, label, args):
        if len(args) == 0:
            print "This plugin written in python. It's called plauge."
        else:
            if args[0] == "disable":
                self.setEnabled(0)
            elif args[0] == "inter":
                print "Accepting."
                while 1:
                    exec raw_input(">>>")
            else:
                print "You issued the following command: " + args[0]
        return 1;

class PigmanListener(EntityListener):
    def __init__(self, plugin):
        self.plugin = plugin
        
    def onCreatureSpawn(self, event):
        entity = event.getEntity()
        if type(entity) ==  PigZombie:
            self.search(entity)
            print "ZP spawned in world", entity.getWorld().getName()
            
        
    def onEntityTarget(self, event):
        if event.getTarget() == None:
            entity = event.getEntity()
            if type(entity) ==  PigZombie: self.search(entity)
            print "ZP targeted null"

    def search(self, entity):
        print "ZP search started"
        task = PigTarget(entity)
        task.ID = BukkitScheduler.scheduleSyncRepeatingTask(self.plugin, task, 5, 1)
        print "ZP target task scedualed"

    def onEntityDeath(self, event):
        deathloc = event.getEntity().getLocation()
        deathev = event.getEntity().getLastDamageCause()
        if type(deathev) == EntityDamageByEntityEvent:
            killer = deathev.getDamager()
            if type(killer) == PigZombie:
                print "Pig killed by PZ"
                killer.getWorld().spawnCreature(deathloc, CreatureType.PIG_ZOMBIE)
                print "Pig Zombie spawned at death loc"
        
        
class PigTarget:
    def __init__(self, pig):
        self.pig = pig

    def run(self, sced):
        print "Zombie finding pigs/people"
        pig = self.pig
        near = pig.getNearbyEntities(32, 32, 32)
        nearest = (None, 17)
        pigloc = pig.getLocation()
        for entity in near:
            if type(entity) in (Player, Pig):
                distance = pigloc.distance(entity.getLocation())
                if distance < nearest[1]:
                    nearest = entity, distance
        if not nearest[1]:
            pig.setTarget(entity)
            print "Zombie has found people"
            sced.cancelTask(self.ID)
            
