import wx
from SmartFrame import SmartFrame


class MyFrame(SmartFrame):
    def __init__(self):
        super().__init__()

        self.add_box("Buttons")
        self.add_buttons(["Button 3", "Button 2", "Button 1"], self.on_buttons)

        self.add_box("Slider")
        self.slider1 = self.add_slider("Speed", 50, 0, 100, self.on_slider1_set)

        self.add_box("Slider and buttons")
        self.slider2 = self.add_slider("Speed", 50, 0, 100, self.on_slider2_set)
        self.add_buttons(["Reverse", "Stop", "Forward"], self.on_buttons)

        self.add_box("More examples")
        self.add_buttons(["Automatic", "Normal", "Single"], self.on_buttons, label="Trigger mode")
        self.add_buttons(["AC", "DC"], self.on_buttons, label="Coupling")
        self.combo = self.add_combo_box("Bandwidth", ["Full", "100 MHz", "20 MHz"], self.on_combo_set)
        self.spin = self.add_spin_control("Trigger level (V)", 5, 0, 10, self.on_spin_set)
        self.add_timer_control(60, self.on_timer_done)

    def on_buttons(self, label):
        print(label, "pressed")

    def on_slider1_set(self, value):
        print("Slider set to", value)

    def on_slider2_set(self, value):
        print("Slider set to", value)
        print(f"Slider1= {self.slider1.value}")

    def on_combo_set(self, value):
        print("Combo box set to", value)

    def on_spin_set(self, value):
        print("Spin Control set to", value)

    def on_timer_done(self):
        print("Timer done")

    def print_inputs(self):
        print("slider 1:", self.slider1.value)
        print("slider 2:", self.slider2.value)
        print("combo box:", self.combo.value)
        print("spin control:", self.spin.value)


if __name__ == "__main__":
    app = wx.App(False)
    my_frame = MyFrame()
    my_frame.Show()
    app.MainLoop()
