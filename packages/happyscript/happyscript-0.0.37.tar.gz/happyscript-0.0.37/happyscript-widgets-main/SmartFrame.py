import wx
import wx.xrc
from SmartInput import SmartInput


class SmartFrame(wx.Frame):
    """
    Public methods
    """

    def __init__(self, parent=None, size=(500, 500), size_y=500):
        """GUI builder for widgets to be used with happyscript

        Keyword Arguments:
            parent -- The window parent. This may be, and often is, None. (default: {None})
            size -- tuple (x,y) containing the window size (default: {500})
        """
        wx.Frame.__init__(self, parent, size=wx.Size(size[0], size[1]))
        self.Bind(wx.EVT_CLOSE, self.__on_close)
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.__mainbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.__mainbox)
        self.Layout()
        self.Centre(wx.BOTH)
        self.__timers=[]

    def add_box(self, title):
        """adds a box with a title to be used to contain the widgets

        Arguments:
            title -- label for the box
        """
        self.__current_top_box = wx.StaticBoxSizer(wx.StaticBox(self, label=title), wx.VERTICAL)
        self.__mainbox.Add(self.__current_top_box, 0, wx.EXPAND, 5)

    def add_buttons(self, button_labels, button_event, label=None):
        """adds a horizontal row of buttons, which trigger the button_event(button_label) callback)

        Arguments:
            button_labels -- list of labels (one for each button)
            button_event -- callback triggered on button presses. function takes a button label as its argument

        Keyword Arguments:
            label -- optional label to be placed left of the buttons (default: {None})
        """
        self.__current_sub_box = self.__create_boxsizer(wx.HORIZONTAL, 0)
        if label is not None:
            self.__insert_label(label, 1)
        for button_label in button_labels:
            event_wrapper = lambda *args, x=button_label: button_event(x)
            proportion = 1 if (label is None) else 0
            self.__insert_button(button_label, event_wrapper, proportion)

    def add_slider(self, label, initial, min, max, set_event=None):
        """adds a slider for the user to set a value, which can trigger the set_event(value) callback
        the value can be accessed in the .value field of the object returned by this method

        Arguments:
            label -- label to be placed left of the slider
            initial -- slider initial value
            min -- slider minimum value
            max -- slider maximum value

        Keyword Arguments:
            set_event -- optional callback triggered when set button is pressed. function takes the new value as its argument (default: {None})

        Returns:
            object to access the slider value via the .value field (object type is SmartInput)
        """
        self.__current_sub_box= self.__create_boxsizer(wx.HORIZONTAL, 0)
        self.__insert_label(label, 0)
        slider_obj = self.__insert_slider(initial, min, max, 1)
        label_obj = self.__insert_label(str(initial), 0)
        smart_input = SmartInput(slider_obj, set_event)
        self.__insert_button("Set", lambda *args: smart_input.set(), 0)
        slider_obj.Bind(wx.EVT_SCROLL, lambda *args: label_obj.SetLabel(str(slider_obj.GetValue())))
        return smart_input

    def add_combo_box(self, label, option_list, set_event=None):
        """adds a combo box for the user to set a value, which can trigger the set_event(value) callback
        the value can be accessed in the .value field of the object returned by this method

        Arguments:
            label -- label to be placed left of the combo box
            option_list -- list of options to be presented in the combo box

        Keyword Arguments:
            set_event -- optional callback triggered when set button is pressed. function takes the new value as its argument (default: {None})

        Returns:
            object to access the combo box value via the .value field (object type is SmartInput)
        """
        self.__current_sub_box = self.__create_boxsizer(wx.HORIZONTAL, 0)
        self.__insert_label(label, 0)
        combo_obj = self.__insert_combo_box(option_list, 1)
        smart_input = SmartInput(combo_obj, set_event)
        self.__insert_button("Set", lambda *args: smart_input.set(), 0)
        return smart_input

    def add_spin_control(self, label, initial, min, max, set_event=None):
        """adds a spin control for the user to set a value, which can trigger the set_event(value) callback
        the value can be accessed in the .value field of the object returned by this method

        Arguments:
            label -- label to be placed left of the spin control
            initial -- spin control initial value
            min -- spin control minimum value
            max -- spin control maximum value

        Keyword Arguments:
            set_event -- optional callback triggered when set button is pressed. function takes the new value as its argument (default: {None})

        Returns:
            object to access the spin control value via the .value field (object type is SmartInput)
        """
        self.__current_sub_box = self.__create_boxsizer(wx.HORIZONTAL, 0)
        self.__insert_label(label, 0)
        spin_obj = self.__insert_spin_control(initial, min, max, 1)
        smart_input = SmartInput(spin_obj, set_event)
        self.__insert_button("Set", lambda *args: smart_input.set(), 0)
        return smart_input

    def add_timer_control(self, default, interval_callback, *args, **kwargs):
        """allows the user to periodically trigger a callback
        the timer interval is set with a spin control
        pressing start or stop will (re)start or stop the interval timer
        Timer info: https://www.blog.pythonlibrary.org/2009/08/25/wxpython-using-wx-timers/

        Arguments:
            default -- inverval default value
            interval_callback -- callback to be triggered each interval. any number of arguments can be passed via *args and **kwargs (interval_callback(*args, **kwargs))
        """
        self.__current_sub_box = self.__create_boxsizer(wx.HORIZONTAL, 0)
        self.__insert_label("Interval (s)", 0)
        spin_obj = self.__insert_spin_control(default, 1, 86400, 1)

        new_timer = wx.Timer(spin_obj)
        spin_obj.Bind(wx.EVT_TIMER, lambda ev: interval_callback(*args, **kwargs), new_timer)
        self.__timers.append(new_timer)
        self.__insert_button("Start", lambda *args: new_timer.Start(1000 * spin_obj.GetValue()), 0)
        self.__insert_button("Stop", lambda *args: new_timer.Stop(), 0)

    """
    private methods
    """

    def __create_boxsizer(self, orientation, proportion):
        """setup for a BoxSizer
        """
        box = wx.BoxSizer(orientation)
        self.__current_top_box.Add(box, proportion, wx.EXPAND, 5)
        return box

    def __insert_label(self, label_text, proportion):
        """setup for a label
        """
        label = wx.StaticText(self.__current_top_box.GetStaticBox(), label=label_text)
        label.Wrap(-1)
        self.__current_sub_box.Add(label, proportion, wx.ALL, 5)
        return label

    def __insert_button(self, button_label, button_event, proportion):
        """setup for a button
        """
        button = wx.Button(self.__current_top_box.GetStaticBox(), label=button_label)
        button.Bind(wx.EVT_BUTTON, button_event)
        self.__current_sub_box.Add(button, proportion, wx.ALL, 5)
        return button

    def __insert_slider(self, initial, min, max, proportion):
        """setup for a slider
        """
        slider = wx.Slider(self.__current_top_box.GetStaticBox(), value=initial, minValue=min, maxValue=max)
        self.__current_sub_box.Add(slider, proportion, wx.ALL | wx.EXPAND, 5)
        return slider

    def __insert_combo_box(self, option_list, proportion):
        """setup for a combo box
        """
        combo = wx.ComboBox(self.__current_top_box.GetStaticBox(), value=option_list[0], choices=option_list)
        self.__current_sub_box.Add(combo, proportion, wx.ALL, 5)
        return combo

    def __insert_spin_control(self, initial, min, max, proportion):
        """setup for a spin control
        """
        spin = wx.SpinCtrl(self.__current_top_box.GetStaticBox(), initial=initial, min=min, max=max)
        self.__current_sub_box.Add(spin, proportion, wx.ALL, 5)
        return spin
    
    def __on_close(self, wxEvent):
        """cancels the running timer threads
        """
        for timer in self.__timers:
            timer.Stop()
        self.Destroy()