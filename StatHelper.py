import ac
import acsys
from sim_info_lib.sim_info import info


class acs:
    def __init__(self):
        self.path = "apps/python/StatHelper/"
        self.texture = self.path + "texture/"
        # label
        self.l_drs = 0
        self.l_gear = 0
        self.l_ers = 0
        self.l_lapers = 0
        self.l_speed = 0
        self.l_rpm = 0
        self.l_flags = 0
        self.l_ot = 0
        self.l_pos = 0
        self.l_lap = 0
        self.l_fuel = 0
        # app
        self.app_window = 0
        # data
        self.speed = 0
        self.drs = 0
        self.ot = ""
        self.gear = 0
        self.ers = 0
        self.lap_ers = 0
        self.ers_mode = 0
        self.rpm = 0
        self.pos = 0
        self.lap = 0
        self.fuel = 0
        self.flag = 0
        # perfcounter
        self.x = 0
        self.y = 0
        self.ot_flag = False
        self.drs_flag = False
        self.prev_flag = 0
        
        
    def refresh_data():
        self.speed = ac.getCarState(0, acsys.CS.SpeedKMH)
        self.drs = True if int(ac.getCarState(0, acsys.CS.DrsEnabled)) == 1 else False
        self.ot = True if int(ac.getCarState(0, acsys.CS.KersInput)) == 1 else False
        self.gear = ac.getCarState(0, acsys.CS.Gear) - 1
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
        
    def init_labels():
        ac.setTitle(app_window, "")
        self.l_drs = ac.addLabel(app_window, "")
        self.l_gear = ac.addLabel(app_window, "")
        self.l_ers = ac.addLabel(app_window, "")
        self.l_lapers = ac.addLabel(app_window, "")
        self.l_speed = ac.addLabel(app_window, "")
        self.l_rpm = ac.addLabel(app_window, "")
        self.l_flag = ac.addLabel(app_window, "")
        self.l_ot = ac.addLabel(app_window, "")
        self.l_pos = ac.addLabel(app_window, "")
        self.l_lap = ac.addLabel(app_window, "")
        self.l_fuel = ac.addLabel(app_window, "")
        ac.setPosition(self.l_gear, 195, 5)
        ac.setPosition(self.l_ers, 280, 0)
        ac.setPosition(self.l_lapers, 261, 0)
        ac.setPosition(self.l_drs, 70, 50)
        ac.setPosition(self.l_speed, 80, 9)
        ac.setPosition(self.l_rpm, 170, 70)
        ac.setPosition(self.l_ersm, 3, 9)
        ac.setPosition(self.l_ot, 140, 50)
        ac.setPosition(self.l_pos, 3, 50)
        ac.setPosition(self.l_lap, 3, 70)
        ac.setPosition(self.l_fuel, 242, 0)
        ac.setSize(self.l_ers, 20, 100)
        ac.setSize(self.l_lapers, 20, 100)
        ac.setSize(self.l_ot, 40, 30)
        ac.setSize(self.l_drs, 60, 30)
        ac.setSize(self.l_fuel, 20, 100)
        labels = [self.l_drs, self.l_ers, self.l_lapers, self.l_speed, self.l_rpm, self.l_ersm, self.l_gear, self.l_pos, self.l_lap, self.l_fuel]
        for label in labels:
            # ac.setFontColor(label, 0, 0, 0, 1)
            ac.setFontSize(label, 18)
            ac.setCustomFont(label, "Formula1 Display", 0, 1)
        ac.setFontSize(self.l_gear, 25)


def update_ers():
    global l_ers, ers, y
    y += 1
    if y == 2:
        int_ers = int(ers)
        if int_ers > 75:
            ac.setBackgroundTexture(l_ers, texture + "ers/100.png")
        elif int_ers > 50:
            ac.setBackgroundTexture(l_ers, texture + "ers/75.png")
        elif int_ers > 25:
            ac.setBackgroundTexture(l_ers, texture + "ers/50.png")
        elif int_ers > 0:
            ac.setBackgroundTexture(l_ers, texture + "ers/25.png")
        else:
            ac.setBackgroundTexture(l_ers, texture + "ers/0.png")
        y = 0


def update_fuel():
    global l_fuel, fuel, y
    if 100 >= fuel >= 0:
        ac.setBackgroundTexture(l_fuel, texture + "fuel/" + str(fuel) + ".png")
    else:
        ac.log("process \"fuel\" failed")


def update_lap_ers():
    global l_lapers, lap_ers
    if 100 >= lap_ers >= 0:
        ac.setBackgroundTexture(l_lapers, texture + "lap_ers/" + str(lap_ers) + ".png")
    else:
        ac.log("process \"lap_ers\" failed")


def acMain(ac_version):
    global app_window
    app_window = ac.newApp("StatHelper")
    ac.setSize(app_window, 300, 100)
    ac.setIconPosition(app_window, 0, -10000)
    ac.drawBorder(app_window, 0)
    ac.setBackgroundTexture(app_window, texture + "background_tp.png")
    ac.initFont(0, "Formula1 Display", 1, 1)
    init_labels()
    return "StatHelper"


def acUpdate(deltaT):
    global x
    x += 1
    if x >= 3:
        global l_drs, l_gear, l_lapers, l_speed, l_rpm, l_ersm, l_ot, l_pos, l_lap, l_fuel, app_window
        global speed, drs, ot, gear, lap_ers, ers_mode, rpm, ot_flag, drs_flag, lap, fuel, flag, is_bg
        refresh_data()
        ac.setText(l_speed, "{} km/h".format(int(speed)))
        if ot_flag and ot:
            ac.setBackgroundTexture(l_ot, texture + "ot/overtake_on.png")
            ot_flag = False
        elif not ot_flag and not ot:
            ac.setBackgroundTexture(l_ot, texture + "ot/overtake_off.png")
            ot_flag = True
        if drs_flag and drs:
            ac.setBackgroundTexture(l_drs, texture + "drs/drs_on.png")
            drs_flag = False
        elif not drs_flag and not drs:
            ac.setBackgroundTexture(l_drs, texture + "drs/drs_off.png")
            drs_flag = True
        update_lap_ers()
        update_fuel()
        update_ers()
        if gear == -1:
            ac.setText(l_gear, "R")
        elif gear == 0:
            ac.setText(l_gear, "N")
        else:
            ac.setText(l_gear, str(gear))
        ac.setText(l_rpm, str(rpm))
        ac.setText(l_ersm, str(ers_mode))
        ac.setText(l_pos, "P" + str(pos))
        ac.setText(l_lap, "L" + str(lap))
        if flag != prev_flag:
            if flag == 1:
                print("blue flag")
            elif flag == 2:
                print("yellow flag")
            else:
                ac.log("flag error")
        x = 0
