from kivy.app import App
from kivy.uix import gridlayout, button, label, popup, textinput, image

class Grid_UI(gridlayout.GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 4

        self.add_widget(image.Image(
            source = 'passwordImage.png'
        ))

        self.add_widget(label.Label(
            text = "Enter your password:"
        ))

        self.textInp = textinput.TextInput(
            text = "",
            font_size = 14
        )
        self.add_widget(self.textInp)

        self.submitButton = button.Button(
            text = "Submit",
        )
        self.add_widget(self.submitButton)
        self.submitButton.bind(on_press = self.storePassword)

        self.pop_up = popup.Popup(
            title = "Password Storage",
            size = (40, 40),
            content = label.Label(
                text = ""
            )
        )
    
    def storePassword(self, element):
        if self.textInp.text:
            self.pop_up.content.text = "Password Stored successfully."
        self.pop_up.open()


class DemoApp(App):

    def build(self):
        return Grid_UI()


DemoApp().run()
