import tkinter as tk
import cv2
from PIL import Image, ImageTk
import os.path
import subprocess
import datetime
import util

class App:
    def __init__(self):
        self.main_window= tk.Tk()
        self.main_window.geometry('1200x520+300+100')

        self.login_button_main_window= util.get_button(self.main_window, 'Login', 'green', self.login)
        self.login_button_main_window.place(x= 750, y= 200)
                                                   
        self.register_new_button_main_window= util.get_button(self.main_window, 'Register New User', 'gray', self.register_new_user, fg= 'black')
        self.register_new_button_main_window.place(x= 750, y= 300)

        self.logout_new_button_main_window= util.get_button(self.main_window, 'Log Out', 'red', self.logout)
        self.logout_new_button_main_window.place(x= 750, y= 400)

        self.webcam_label= util.get_img_label(self.main_window)
        self.webcam_label.place(x= 10, y= 0, width= 700, height= 500)

        self.add_webcam(self.webcam_label)

        self.db_dir= './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path= './log.txt'

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap= cv2.VideoCapture(0)

        self.label= label
        self.process_webcam()
    
    def process_webcam(self):
        frame= self.cap.read()

        self.most_recent_capture_arr= frame

        img= cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)

        self.most_recent_capture_pil= Image.fromarray(img)
        
        imgtk= ImageTk.PhotoImage(image= self.most_recent_capture_pil)
        self.label.imgtk= imgtk
        self.label.configure(image= imgtk)

        self.label.after(20, self.process_webcam)

    def login(self):
        unknown_img_path = './.temp.jpg'

        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)

        output = subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path], text=True)
        name = output.split(',')[1].strip()

        os.remove(unknown_img_path)

        if name.lower() in ['no_persons_found', 'unknown', 'no_person_found']:  
            util.msg_box('Ups...', 'Unknown User. Please Register New User Or Try Again.')
        else:
            util.msg_box('Welcome!', f'Welcome {name}.')
            with open(self.log_path, 'a') as f:
                f.write(f'{name}, {datetime.datetime.now()}\n')

    def register_new_user(self):
        self.register_new_user_window= tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry('1200x520+320+120')
        
        self.accept_button_register_new_user_window= util.get_button(self.register_new_user_window, 'Accept', 'green', self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x= 750, y= 300)

        self.try_again_button_register_new_user_window= util.get_button(self.register_new_user_window, 'Try Again', 'red', self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x= 750, y= 400)

        self.capture_label= util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x= 10, y= 0, width= 700, height= 500)

        self.add_img_to_label(self.capture_label)

        self.entry_text_register_new_user= util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=750, y=150)

        self.text_label_register_new_user= util.get_text_label(self.register_new_user_window, 'Please, Enter user name:')
        self.text_label_register_new_user.place(x=750, y=70)

    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()

    def add_img_to_label(self, label):
        imgtk= ImageTk.PhotoImage(image= self.most_recent_capture_pil)
        label.imgtk= imgtk
        label.configure(image= imgtk)

        self.register_new_user_capture= self.most_recent_capture_arr.copy()

    def start(self):
        self.main_window.mainloop()
    
    def accept_register_new_user(self):
        name= self.entry_text_register_new_user.get(1.0, 'end-1c')

        cv2.imwrite(os.path.join(self.db_dir, '{}.jpg'.format(name)), self.register_new_user_capture)

        util.msg_box('Success!', 'Use was register successfully!')

        self.register_new_user_window.destroy()
        
    def logout(self):
        util.msg_box('Good Bye!', 'You Have Been Log Out Successfully.')
        self.main_window.destroy()

if __name__ == '__main__':
    