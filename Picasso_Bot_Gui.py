from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from threading import Thread
import cv2
import numpy as np  # used to flip array for properly mirrored output and picture taken
from time import sleep  # not needed, but could become necessary
import time
'''
GLOBALS
'''
pause = False  # pauses or unpauses the camera feed


# to access the array of the picture being taken, call variable final_picture, might need try/except
def take_picture(picture):  # takes a picture, in a thread later on
    global pause
    # picture = cv2.VideoCapture(0)
    result = True
    while result:
        ret, frame = picture.read()
        final_picture = np.fliplr(frame)
        # cv2.imwrite("/home/soft-dev/Documents/GantryGame3.0/picassopicture.png", final_picture)
        cv2.imwrite("picassopicture.png", final_picture)
        result = False
    # picture.release()
    pause = True


'''
END GLOBALS
'''


class CamApp(App):  # build for kivy display
    '''
    Colors and Shading
    '''
    button_shade = 1
    button_paused_shade = 0.5

    picture_button_text = 'Take Image'
    retake_button_text = 'Retake Image'
    print_button_text = 'Print'

    picture_button_color = (1, 0, 1, button_shade)
    retake_button_color = (0, 0, 1, button_paused_shade)
    print_button_color = (0, 1, 0, button_paused_shade)

    button_font_size = 88

    disable_all_buttons = False

    # extra
    x = Window.size[0]
    y = Window.size[1]
    '''
    End Colors and Shading
    '''

    def build(self):

        # start cv2stuff
        self.img1 = Image()
        layout = FloatLayout()
        layout.add_widget(self.img1)
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0 / 33.0)

        # end cv2stuff
        def add_button(button: Button):
            layout.add_widget(button)
        def remove_button(button: Button):
            layout.remove_widget(button)

        def disable_all_text():
            picture_button.text = ''
            retake_button.text = ''
            print_button.text = ''

        def enable_all_text():
            picture_button.text = 'Take Image'
            retake_button.text = 'Retake Image'
            print_button.text = 'Print'

        def enable_text(button: Button):
            if button == picture_button:
                picture_button.text = 'Take Image'
            elif button == retake_button:
                retake_button.text = 'Retake Image'
            elif button == print_button:
                print_button.text = 'Print'
            else:
                print(str(button), 'not found, in enable_text. try adding this buttons or callingn ir correctly')

        def disable(button):  # allows to disable or enable a single button
            button.disabled = True
            button.background_color[-1] = self.button_paused_shade

        def enable(button):  # allows to disable or enable a single button
            button.disabled = False
            button.background_color[-1] = self.button_shade

        def ready_to_print():
            global pause
            add_button(picture_button)
            enable_all_text()
            pause = False

        def disable_all_buttons():
            for button in button_array:
                remove_button(button)

        def take_picture_button(instance):  # changes ui, starts thread to take picture, as defined in GLOBALS
            remove_button(picture_button)
            add_button(retake_button)
            add_button(print_button)




            # cv2.destroyAllWindows()
            # self.capture.release()

            print('pic taken, see picassopicture.jpg')
            take_picture(self.capture)
            Thread(target=take_picture, args=(self.capture,)).start()
            # take_picture()

        def retake_picture_button(instance):  # changes ui accordingly, pauses the camera
            remove_button(retake_button)
            add_button(picture_button)
            remove_button(print_button)
            global pause
            pause = False


        def printing():
            print('start print here')
            sleep(5)
            ready_to_print()


        def thread_printing(instance): # disables all buttons upon print press
            disable_all_buttons()
            Thread(target=printing).start()


        picture_button = Button(size_hint_x=self.x/1600, size_hint_y=self.y/5900, text=self.picture_button_text,
                                font_size=self.button_font_size, on_press=take_picture_button,
                                background_color=self.picture_button_color, pos=(0, 0),
                                disabled=self.disable_all_buttons)

        print_button = Button(pos=(0, 960), size_hint_x=self.x/1600, size_hint_y=self.y/5900,
                              background_color=self.print_button_color,
                              on_press=thread_printing, font_size=self.button_font_size, text=self.print_button_text,
                              disabled=self.disable_all_buttons)

        retake_button = Button(size_hint_x=self.x/1600, size_hint_y=self.y/5900, text=self.retake_button_text,
                               font_size=self.button_font_size, on_press=retake_picture_button,
                               background_color=self.retake_button_color, pos=(0, 0),
                               disabled=self.disable_all_buttons)
        # ui may break upon entering the pi's screen size, will adjust to screen size later
        button_array = [picture_button, print_button, retake_button]



        temp_count = 1

        if temp_count  == 1:
            # layout.add_widget(retake_button)
            layout.add_widget(picture_button)
            # layout.add_widget(print_button)
            temp_count += 1

        return layout

    def update(self, dt):
        global final_picture
        ret, frame = self.capture.read()
        if not pause:
            buf1 = np.flipud(frame)
            buf2 = np.fliplr(buf1)
            buf = buf2.tobytes()
            texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')  # see https://kivy.org/doc/stable/api-kivy.graphics.texture.html
            texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.img1.texture = texture1
        if pause:
            try:
                buf = final_picture.tobytes()
                cv2.destroyAllWindows()
                texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                self.img1.texture = texture1
            except NameError:  # occurs because variable final_image is not created yet (instantaneously)
                # print("test")
                pass


if __name__ == '__main__':
    CamApp().run()
    cv2.destroyAllWindows()
'''
https://kivy.org/doc/stable/api-kivy.uix.floatlayout.html
https://stackoverflow.com/questions/26773932/global-variable-is-undefined-at-the-module-level
https://stackoverflow.com/questions/3323001/what-is-the-maximum-recursion-depth-in-python-and-how-to-increase-it 
https://stackshare.io/numpy/alternatives
useful color calculator for kivy colors: https://corecoding.com/utilities/rgb-or-hex-to-float.php
'''