try:
    import android
    from jnius import autoclass
    activity = autoclass("org.renpy.android.PythonActivity")
except ImportError:
    android = None

class Event(object):
    def __init__(self, type, key, player):
        self.type = type
        self.key = key
        self.player = player

    def change(self):
        if self.type != activity.getBUTTON(self.player, self.key):
            self.type = not self.type
            return True
        else:
            return False

    def is_event(self):
        return self.change()

class OuyaController(object):
    BUTTON_MENU         = 0x0000
    BUTTON_O            = 0x0001
    BUTTON_U            = 0x0002
    BUTTON_Y            = 0x0004
    BUTTON_A            = 0x0008
    BUTTON_DPAD_UP      = 0x0010
    BUTTON_DPAD_DOWN    = 0x0020
    BUTTON_DPAD_LEFT    = 0x0040
    BUTTON_DPAD_RIGHT   = 0x0080
    BUTTON_L1           = 0x0100
    BUTTON_L2           = 0x0200
    BUTTON_L3           = 0x0400
    BUTTON_R1           = 0x1000
    BUTTON_R2           = 0x2000
    BUTTON_R3           = 0x4000
    
    AXIS_LS_X = 0x0001
    AXIS_LS_Y = 0x0002
    AXIS_RS_X = 0x0004
    AXIS_RS_Y = 0x0008
    
    def __init__(self, MAX_CONTROLLERS=4):
        self.events = {}
        self.DOWN = 1
        self.MOTION = 2
        self.UP = 3
        self.KEYDOWN = True
        self.KEYUP = False
        self.MAX_CONTROLLERS = MAX_CONTROLLERS        
        self.players = []
        for x in range(0, MAX_CONTROLLERS):
            y = []
            y.append(Event(False, self.BUTTON_MENU, x))
            y.append(Event(False, self.BUTTON_O, x))
            y.append(Event(False, self.BUTTON_U, x))
            y.append(Event(False, self.BUTTON_Y, x))
            y.append(Event(False, self.BUTTON_A, x))
            y.append(Event(False, self.BUTTON_DPAD_UP, x))
            y.append(Event(False, self.BUTTON_DPAD_DOWN, x))
            y.append(Event(False, self.BUTTON_DPAD_LEFT, x))
            y.append(Event(False, self.BUTTON_DPAD_RIGHT, x))
            y.append(Event(False, self.BUTTON_L1, x))
            y.append(Event(False, self.BUTTON_L2, x))
            y.append(Event(False, self.BUTTON_L3, x))
            y.append(Event(False, self.BUTTON_R1, x))
            y.append(Event(False, self.BUTTON_R2, x))
            y.append(Event(False, self.BUTTON_R3, x))
            self.players.append(y)

    def get_events(self):
        if android:
            for p in range(0, self.MAX_CONTROLLERS):
                activity.setDPAD(p)
                activity.setAXIS(p)
                for event in self.players[p]:
                    if event.is_event():
                        if event.type == self.KEYDOWN:
                            self.events.update({"%s%s"%(event.key, p): [event.type, self.DOWN]})
                        elif event.type == self.KEYUP:
                            self.events.update({"%s%s"%(event.key, p): [event.type, self.UP]})
    

    def get_left_stick(self, player=0):
        if android:
            return (activity.getAXIS(player, self.AXIS_LS_X),
                    activity.getAXIS(player, self.AXIS_LS_Y))

    def get_right_stick(self, player=0):
        if android:
            return (activity.getAXIS(player, self.AXIS_RS_X),
                    activity.getAXIS(player, self.AXIS_RS_Y))
        
        return (0.0, 0.0)
        
    def update(self):
        flag = []
        for event in self.events:
            if self.events[event][0] == self.KEYUP:
                flag.append(event)
            else:
                self.events[event][1] = self.MOTION

        for i in flag:
            del self.events[i]

    def _get(self, name):
        try:event = self.events[name]
        except KeyError:event = None
        return event
    
    def _stat(self, name):
        event = self._get(name)
        if event != None:status = event[1]
        else:status = None
        return status
    
    def isset(self, name):
        try:self.events[name];event = True
        except KeyError:event = False

        return event

    def down(self, name, player=0):
        stat = self._stat("%s%s"%(name, player))
        if stat == self.DOWN:return True
        else:return False

    def motion(self, name, player=0):
        stat = self._stat("%s%s"%(name, player))
        if stat == self.MOTION:return True
        else:return False

    def up(self, name, player=0):
        stat = self._stat("%s%s"%(name, player))
        if stat == self.UP:return True
        else:return False
