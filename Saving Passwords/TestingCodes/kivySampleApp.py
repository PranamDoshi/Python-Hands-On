from kivy.app import App

from kivy.uix.label import Label
from kivy.uix.button import Button

from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.pagelayout import PageLayout

class HelloWorldApp(App):

    def build(self):
        return Label(
            text = "Hello World!"
        )


class SampleApp_anchroLayout(App):
    """Sample class using Anchor layout."""

    def build(self):
        # anchor_x and anchor_y can be used to position the button appropriately.
        layout = AnchorLayout(
            anchor_x='left', anchor_y='center'
        )
        sampleButton = Button(
            text = "This is a button.",
            size_hint = (.15, .1),
            background_color = (0.0, 25.86, 1.0),
            color = (0, 0, 0, 1),
        )

        sampleButton2 = Button(
            text = "This is not a button.",
            size_hint = (.15, .1),
            background_color = (0.0, 25.86, 1.0),
            color = (0, 0, 0, 1),
        )
        layout.add_widget(sampleButton)
        layout.add_widget(sampleButton2)

        return layout


class GridLayouTemplate(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows, self.cols = 2, 1

        self.add_widget(
            Label(
                text = "Please click the button."
            )
        )
        
        self.add_widget(
            Button(
                text = "Click Me",
                background_color = (0.0, 25.86, 1.0, 1),
                color = (0, 0, 0, 1),
            )
        )


class SampleApp_gridLayout(App):

    def build(self):
        return GridLayouTemplate()


class FloatLayoutTemplate(FloatLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_widget(
            Button(
                text = "This is the large button.",
                size_hint = (0.3, 0.2),
                pos_hint = {
                    "x": 0.2,
                    "y": 0.2
                },
            )
        )

        self.add_widget(
            Button(
                text = "This is the small button.",
                size_hint = (0.2, 0.1),
                pos_hint = {
                    "x": 0.8,
                    "y": 0.7
                },
            )
        )


class SampleApp_floatLayout(App):

    def build(self):
        return FloatLayoutTemplate()


class PageLayoutTemplate(PageLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_widget(
            Button(
                text = "Button in first page."
            )
        )

        self.add_widget(
            Button(
                text = "Button in second page."
            )
        )

        self.add_widget(
            Button(
                text = "Button in third page."
            )
        )


class SampleApp_pageLayout(App):

    def build(self):
        return PageLayoutTemplate()


# HelloWorldApp().run()
# SampleApp_anchroLayout().run()
# SampleApp_gridLayout().run()
# SampleApp_floatLayout().run()
# SampleApp_pageLayout().run()
