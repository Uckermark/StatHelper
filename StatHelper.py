import ac
import acsys
from sim_info_lib.sim_info import info
import configparser

class app:
    def __init__(self, interval, perf_mode): # TODO: dynamic window size scaling
        
        # initialize config
        ac.log("Inititalized with:\nInterval: " + str(interval) + "\nPerformance mode: " + str(perf_mode))
        self.refresh_interval = interval

        # performance counter are marked with p_<var>
        # labels with l_<var>
        self.path = "apps/python/StatHelper/"
        self.texture = self.path + "texture/"

        # performance
        self.p_update1 = 0
        self.p_ers = 0
        self.prev_ot = False
        self.prev_drs = False
        self.prev_flag = 0

        # get initial data
        self.car_checked = False
        self.has_drs = False
        self.has_ers = False
        self.refresh_data()

        # create app window
        self.app_window = ac.newApp("StatHelper")
        ac.setSize(self.app_window, 300, 100)
        ac.setIconPosition(self.app_window, 0, -10000)
        ac.drawBorder(self.app_window, 0)
        ac.setBackgroundTexture(self.app_window, self.texture + "background.png")
        ac.initFont(0, "Formula1 Display", 1, 1)

        # create labels
        ac.setTitle(self.app_window, "")
        self.l_drs = ac.addLabel(self.app_window, "")
        self.l_gear = ac.addLabel(self.app_window, "")
        self.l_ers = ac.addLabel(self.app_window, "")
        self.l_lapers = ac.addLabel(self.app_window, "")
        self.l_speed = ac.addLabel(self.app_window, "")
        self.l_rpm = ac.addLabel(self.app_window, "")
        self.l_flag = ac.addLabel(self.app_window, "")
        self.l_ot = ac.addLabel(self.app_window, "")
        self.l_pos = ac.addLabel(self.app_window, "")
        self.l_lap = ac.addLabel(self.app_window, "")
        self.l_fuel = ac.addLabel(self.app_window, "")

        # set the label position
        ac.setPosition(self.l_gear, 195, 5)
        ac.setPosition(self.l_ers, 280, 0)
        ac.setPosition(self.l_lapers, 261, 0)
        ac.setPosition(self.l_drs, 70, 50)
        ac.setPosition(self.l_speed, 80, 9)
        ac.setPosition(self.l_rpm, 170, 70)
        ac.setPosition(self.l_ot, 140, 50)
        ac.setPosition(self.l_pos, 3, 50)
        ac.setPosition(self.l_lap, 3, 70)
        ac.setPosition(self.l_fuel, 242, 0)
        ac.setSize(self.l_ers, 20, 100)
        ac.setSize(self.l_lapers, 20, 100)
        ac.setSize(self.l_ot, 40, 30)
        ac.setSize(self.l_drs, 60, 30)
        ac.setSize(self.l_fuel, 20, 100)
        labels = [self.l_drs, self.l_ers, self.l_lapers, self.l_speed, self.l_rpm, self.l_gear, self.l_pos, self.l_lap, self.l_fuel]
        for label in labels:
            ac.setFontSize(label, 18)
            ac.setCustomFont(label, "Formula1 Display", 0, 1)
        ac.setFontSize(self.l_gear, 25)


    # loads data from ac
    def refresh_data(self):
        self.rpm = int(ac.getCarState(0, acsys.CS.RPM))
        self.pos = ac.getCarRealTimeLeaderboardPosition(0) + 1
        self.speed = ac.getCarState(0, acsys.CS.SpeedKMH)
        if info.static.maxFuel != 0:
            self.fuel = int(100 * info.physics.fuel / info.static.maxFuel)
        self.flag = int(info.graphics.flag)
        self.gear = ac.getCarState(0, acsys.CS.Gear) - 1
        if self.has_drs:
            self.drs = True if int(ac.getCarState(0, acsys.CS.DrsEnabled)) == 1 else False
        if self.has_ers:
            self.ers = 100 * ac.getCarState(0, acsys.CS.KersCharge)
            self.lap_ers = int(100 - (ac.getCarState(0, acsys.CS.ERSCurrentKJ) / (ac.getCarState(0, acsys.CS.ERSMaxJ) * 0.00001)))
            self.ot = True if int(ac.getCarState(0, acsys.CS.KersInput)) == 1 else False
        laps = []
        cars = ac.getCarsCount()
        for i in range(cars):
            laps.append(ac.getCarState(i, acsys.CS.LapCount))
        self.lap = max(laps) + 1


    # updates ers related labels
    def update_ers(self):
        self.p_ers += 1
        if self.p_ers >= 2:
            # update ers label
            int_ers = int(self.ers)
            if int_ers > 75:
                ac.setBackgroundTexture(self.l_ers, self.texture + "ers/100.png")
            elif int_ers > 50:
                ac.setBackgroundTexture(self.l_ers, self.texture + "ers/75.png")
            elif int_ers > 25:
                ac.setBackgroundTexture(self.l_ers, self.texture + "ers/50.png")
            elif int_ers > 0:
                ac.setBackgroundTexture(self.l_ers, self.texture + "ers/25.png")
            else:
                ac.setBackgroundTexture(self.l_ers, self.texture + "ers/0.png")
            # update per-lap-ers label
            if 100 >= self.lap_ers >= 0:
                ac.setBackgroundTexture(self.l_lapers, self.texture + "lap_ers/" + str(self.lap_ers) + ".png")
            else:
                ac.log("process \"lap_ers\" failed")
            # update overtake label
            if not self.prev_ot and self.ot:
               ac.setBackgroundTexture(self.l_ot, self.texture + "ot/overtake_on.png")
               self.prev_ot = True
            elif self.prev_ot and not self.ot:
               ac.setBackgroundTexture(self.l_ot, self.texture + "ot/overtake_off.png")
               self.prev_ot = False
            self.p_ers = 0
            


    # updates fuel label
    def update_fuel(self):
        if 100 >= self.fuel >= 0:
            ac.setBackgroundTexture(self.l_fuel, self.texture + "fuel/" + str(self.fuel) + ".png")
        else:
            ac.log("process \"fuel\" failed")
    
    
    # update displayed flag
    def update_flag(self):
        if self.flag != self.prev_flag:
            self.prev_flag = self.flag
            if self.flag == 0:
                print("no flag")
            elif self.flag == 1:
                print("blue flag")
            elif self.flag == 2:
                print("yellow flag")
            elif self.flag == 3:
                print("black flag")
            elif self.flag == 4:
                print("white flag")
            elif self.flag == 5:
                print("checkered flag")
            elif self.flag == 6:
                print("penalty flag")
            else:
                ac.log("flag error")


    # updates all labels
    def update(self):
        self.p_update1 += 1
        if self.p_update1 == 1:
            if not self.car_checked:
                self.has_drs = True if info.static.hasDRS == 1 else False
                self.has_ers = True if info.static.hasERS == 1 else False
                self.car_checked = True
            self.refresh_data()
            ac.setText(self.l_speed, "{} km/h".format(int(self.speed)))
            ac.setText(self.l_rpm, str(self.rpm))
            ac.setText(self.l_pos, "P" + str(self.pos))
            ac.setText(self.l_lap, "L" + str(self.lap))
        elif self.p_update1 == 2:
            if self.has_drs:
                if not self.prev_drs and self.drs:
                    ac.setBackgroundTexture(self.l_drs, self.texture + "drs/on.png")
                    self.prev_drs = True
                elif self.prev_drs and not self.drs:
                    ac.setBackgroundTexture(self.l_drs, self.texture + "drs/off.png")
                    self.prev_drs = False
        elif self.p_update1 == 3:
            if self.has_ers:
                self.update_ers()
            if self.gear == -1:
                ac.setText(self.l_gear, "R")
            elif self.gear == 0:
                ac.setText(self.l_gear, "N")
            else:
                ac.setText(self.l_gear, str(self.gear))
        elif self.p_update1 >= 4:
            self.update_fuel()
            self.update_flag()
            self.p_update1 = 0
            
        

# triggered on ac start
def acMain(ac_version):
    global app
    try:
        config = configparser.ConfigParser()
        config.read('apps/python/StatHelper/config.ini')
        perf_mode = config['PERF']['PERFORMANCE_MODE']
        interval = int(config['PERF']['INTERVAL'])
    except:
        perf_mode = False
        interval = 1
        ac.log("Could not parse config.ini, using defaults")
    app = app(interval, perf_mode)
    return "StatHelper"


# triggered every frame
def acUpdate(deltaT):
    global app
    app.update()
