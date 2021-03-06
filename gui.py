import kivy
import random

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

from kivy.core.window import Window

from kivy.uix.textinput import TextInput

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.behaviors import CompoundSelectionBehavior

from kivy.properties import StringProperty, ObjectProperty

from itemlist import ItemList


red = [1, 0, 0, 1]
green = [0, 1, 0, 1]
green_high = [0.8, 1, 0, 1]

blue = [0, 0, 1, 1]
purple = [1, 0, 1, 1]
gray = [0.5,0.5,0.5, 1]

def color_for_state(state):
    if state == 'out':
        return purple
    if state == 'in':
        return green

# from https://kivy.org/docs/api-kivy.uix.screenmanager.html
# Declare both screens
class MainScreen(Screen):
    pass

class AddItemScreen(Screen):

    def add_item(self):
        if self.ids.item_name.text == "":
            self.ids.status.text = "missing name"
            return

        if self.ids.price.text == "":
            self.ids.status.text = "missing price"
            return

        if self.ids.description.text == "":
            self.ids.status.text = "missing description"
            return

        self.items.add_item(self.ids.item_name.text, self.ids.description.text, self.ids.price.text)
        self.ids.status.text = "item "+self.ids.item_name.text + " added"

        self.ids.item_name.text = ""
        self.ids.description.text = ""
        self.ids.price.text = ""

Builder.load_string("""
<AddItemScreen>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: "Item Name:"
        TextInput:
            id: item_name
            text: ""
        Label:
            text: "Description:"
        TextInput:
            id: description
            text: ""
        Label:
            text: "Price Per Day:"
        TextInput:
            id: price
            text: ""
        Button:
            text: 'Save Item'
            on_press:
                root.add_item()
        Button:
            text: 'Cancel'
            on_press:
                root.manager.transition.direction = 'right'
                root.manager.current = 'main'
        Label:
            id: status
""")


# from http://nullege.com/codes/show/src%40k%40i%40kivy-HEAD%40examples%40widgets%40compound_selection.py/3/kivy.uix.behaviors.CompoundSelectionBehavior/python
class SelectableGrid(CompoundSelectionBehavior, GridLayout):

    def __init__(self, **kwargs):
        super(SelectableGrid, self).__init__(**kwargs)
        keyboard = Window.request_keyboard(None, self)
        keyboard.bind(on_key_down=self.select_with_key_down,
                      on_key_up=self.select_with_key_up)

    def select_node(self, node):
        node.background_color = green_high
        return super(SelectableGrid, self).select_node(node)

    def deselect_node(self, node):

        record = self.items.items[node.storage_idx]
        state = record.status
        node.background_color = color_for_state(state)
        super(SelectableGrid, self).deselect_node(node)

    def do_touch(self, instance, touch):
        if ('button' in touch.profile and touch.button in
            ('scrollup', 'scrolldown', 'scrollleft', 'scrollright')) or \
                instance.collide_point(*touch.pos):
            self.select_with_touch(instance, touch)
        else:
            return False
        return True


class MainWindow(App):

    label_text = StringProperty()
    selection = []

    on_selection = None

    def set_selection(self, grid, *args):
        description = []
        total_price = 0
        self.selection = []
        self.selection_with_idx = {}

        for node in grid.selected_nodes:
           record = self.items.items[node.storage_idx]
           self.selection.append(record)
           self.selection_with_idx[node.storage_idx] = record

        for record in self.selection:
           price = record.price
           name = record.name

           total_price += float(price)
           description.append(name)

        self.main_label.text = ",".join(description) + ":"+ str(total_price)

    def on_button_pressed(self, button):
        print(button.state)

    def list_items(self,*args):
        self.main_label.text = "Choose action from the left menu, then choose items on the right "

    def hire_items(self, *args):
        inst = args[0]
        ## This will hire items for the current selection
        for record in self.selection:
            if record.status == 'out':
                self.main_label.text = "You are trying to hire an already hired equipment. Please return it first!"
                self.selection_with_idx = {}
                return True

        self.main_label.text = "Please click Confirm to hire!"
        return True

    def return_items(self,*args):
        for record in self.selection:
            if record.status == 'in':
                self.main_label.text = "You are trying to return a non-hired equipment. Please check your selections!"
                self.selection_with_idx = {}
                return False

        self.main_label.text = "Please click to Confirm to return!"
        return True

    def confirm(self,*args):
        ## Check if selected_functions is selected
        products = []
        if len(self.selection_with_idx) == 0:
            self.main_label.text = "Confirm won't work! Fix your choices"
            return False

        ## If hire is being selected - then we set hired to all items in the file
        for key, record in self.selection_with_idx.items():
            #print key, record
            if self.items.items[key].status=='in':
                self.items.items[key].status = 'out'
                products.append(self.items.items[key].name)
                out_message = ' Items Hired'

            else:
                self.items.items[key].status = 'in'
                products.append(self.items.items[key].name)
                out_message = ' Items Returned'


        self.items.save()
        self.main_label.text = ','.join(products) + out_message
        return True

    def add_new_item(self,*args):
        self.sm.transition.direction = 'left'
        self.sm.current = "add_item"

    def build_main(self):
        main_layout = BoxLayout(padding=5, orientation='vertical')
        group_layout = BoxLayout(padding=5)
        actions = {
            'List items':self.list_items,
            'Hire items':self.hire_items,
            "Return Items":self.return_items,
            "Confirm":self.confirm,
            "Add New Item":self.add_new_item
        }

        items = self.items.load()

        colors = [red, green, blue, purple]

        h_layout = BoxLayout(padding=5, orientation='vertical', size_hint_x=None, width=150,)
        for action_name in sorted(actions.keys()):
            callback = actions[action_name]
            btn = ToggleButton(text=action_name,background_color=gray, group="actions")
            btn.bind(on_press=callback)
            h_layout.add_widget(btn)
        group_layout.add_widget(h_layout)

        items = list(items.values())

        layout = SelectableGrid(cols=2, up_count=5, multiselect=True, scroll_count=1)
        for idx, item in self.items.items.items():
            #print(idx)
         #   category, name, cost, state = item
            btn = Button(text=item.name,
                         background_color=color_for_state(item.status))
            btn.bind(on_touch_down=layout.do_touch)
            btn.storage_idx = idx

            layout.add_widget(btn)
        layout.bind(selected_nodes=self.set_selection)
        layout.items = self.items

        group_layout.add_widget(layout)

        main_layout.add_widget(group_layout)

        self.main_label = Label(text="loading...", size_hint_y=None, height=50)
        self.selected_functions = []
        main_layout.add_widget(self.main_label)

        return main_layout

    def build(self):
        self.items = ItemList('items.csv')
        self.items.load()

        self.main = MainScreen(name='main')

        self.main.add_widget(self.build_main())

        sm.add_widget(self.main)

        self.add_item_screen = AddItemScreen(name='add_item')
        self.add_item_screen.items = self.items

        sm.add_widget(self.add_item_screen)

        self.sm = sm
        sm.current = "main"
        return sm

# Create the screen manager
sm = ScreenManager()

if __name__ == "__main__":
    app = MainWindow()
    app.run()
