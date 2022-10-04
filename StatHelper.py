import ac
import acsys
from sim_info_lib.sim_info import info

app = None

class acs:
    def __init__(self):
        self.path = "apps/python/StatHelper/"
        self.texture = self.path + "texture/"
        # label
        self.l_drs = None
        self.l_gear = None
        self.l_ers = None
        self.l_lapers = None
        self.l_speed = None
        self.l_rpm = None
        self.l_flags = None
        self.l_ot = None
        self.l_pos = None
        self.l_lap = None
        self.l_fuel = None
        # app
        self.app_window = None
        # perfcounter
        self.x = 0
        self.y = 0
        self.ot_flag = False
        self.drs_flag = False
        self.prev_flag = 0
        # data
        self.has_drs = True if info.static.hasDRS == 1 else False
        self.has_ers = True if info.static.hasDRS == 1 else False
        self.refresh_data()
        # init app window
        self.app_window = ac.newApp("StatHelper")
        ac.setSize(self.app_window, 300, 100)
        ac.setIconPosition(self.app_window, 0, -10000)
        ac.drawBorder(self.app_window, 0)
        ac.setBackgroundTexture(self.app_window, self.texture + "background_tp.png")
        ac.initFont(0, "Formula1 Display", 1, 1)
        self.init_labels()
        
        
    def refresh_data(self):
        self.speed = ac.getCarState(0, acsys.CS.SpeedKMH)
        if self.has_drs:
            self.drs = True if int(ac.getCarState(0, acsys.CS.DrsEnabled)) == 1 else False
        self.ot = True if int(ac.getCarState(0, acsys.CS.KersInput)) == 1 else False
        self.gear = ac.getCarState(0, acsys.CS.Gear) - 1
        if self.has_ers:
            self.ers = 100 * ac.getCarState(0, acsys.CS.KersCharge)
            self.lap_ers = int(100 - ((ac.getCarState(0, acsys.CS.ERSCurrentKJ)) / (ac.getCarState(0, acsys.CS.ERSMaxJ) * 0.001)) * 100)
            self.ers_mode = ac.getCarState(0, acsys.CS.ERSDelivery)
        self.rpm = int(ac.getCarState(0, acsys.CS.RPM))
        self.pos = ac.getCarRealTimeLeaderboardPosition(0) + 1
        laps = []
        cars = ac.getCarsCount()
        for i in range(cars):
            laps.append(ac.getCarState(i, acsys.CS.LapCount))
        self.lap = max((laps[i] for i in range(cars))) + 1
        self.fuel = int(info.physics.fuel / info.static.maxFuel * 100)
        self.flag = int(info.graphics.flag)
        
    def init_labels(self):
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
            # ac.setFontColor(label, 0, 0, 0, 1)
            ac.setFontSize(label, 18)
            ac.setCustomFont(label, "Formula1 Display", 0, 1)
        ac.setFontSize(self.l_gear, 25)
        
        
    def update_ers(self):
        self.y += 1
        if self.y == 2:
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
            self.y = 0
                
                
    def update_fuel(self):
        if 100 >= self.fuel >= 0:
            ac.setBackgroundTexture(self.l_fuel, self.texture + "fuel/" + str(self.fuel) + ".png")
        else:
            ac.log("process \"fuel\" failed")
        
        
    def update_lap_ers(self):
        if 100 >= self.lap_ers >= 0:
            ac.setBackgroundTexture(self.l_lapers, self.texture + "lap_ers/" + str(self.lap_ers) + ".png")
        else:
            ac.log("process \"lap_ers\" failed")
            
    def update(self):
        self.x += 1
        if self.x >= 3:
            self.refresh_data()
            ac.setText(self.l_speed, "{} km/h".format(int(self.speed)))
            if self.ot_flag and self.ot:
                ac.setBackgroundTexture(self.l_ot, self.texture + "ot/overtake_on.png")
                self.ot_flag = False
            elif not self.ot_flag and not self.ot:
                ac.setBackgroundTexture(self.l_ot, self.texture + "ot/overtake_off.png")
                self.ot_flag = True
            if self.has_drs:
                if self.drs_flag and self.drs:
                    ac.setBackgroundTexture(self.l_drs, self.texture + "drs/drs_on.png")
                    self.drs_flag = False
                elif not self.drs_flag and not self.drs:
                    ac.setBackgroundTexture(self.l_drs, self.texture + "drs/drs_off.png")
                    self.drs_flag = True
            if self.has_ers:
                self.update_lap_ers()
                self.update_ers()
            self.update_fuel()
            if self.gear == -1:
                ac.setText(self.l_gear, "R")
            elif self.gear == 0:
                ac.setText(self.l_gear, "N")
            else:
                ac.setText(self.l_gear, str(self.gear))
            ac.setText(self.l_rpm, str(self.rpm))
            ac.setText(self.l_pos, "P" + str(self.pos))
            ac.setText(self.l_lap, "L" + str(self.lap))
            if self.flag != self.prev_flag:
                if self.flag == 1:
                    print("blue flag")
                elif self.flag == 2:
                    print("yellow flag")
                else:
                    ac.log("flag error")
        


def acMain(ac_version):
    global app
    app = acs()
    return "StatHelper"


def acUpdate(deltaT):
    global app
    app.update()
