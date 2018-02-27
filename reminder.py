import Tkinter as tk
import AppKit
import time
import atexit
import ttk
import sys


#constants, i.e. change these to change what the program does and displays
REMINDER_LABEL = """Updates are available for your computer that require a restart. If you do nothing, 
your computer will restart automatically"""
UPDATE_LABEL = """Your computer will restart to install required updates"""

#Time until restart if user does nothing
DELAY_TIME = 600
#update every ___ ms
UPDATE_RATE = 1000


#NOT ACTUALLY USED
def get_delays_remaining(filenameWithPath):
	'''gets the number of 'snoozes' remaining from a file. the file should just contain a number'''
	file = open(filenameWithPath, "r")
	fileContents = file.read()
	return int(fileContents.strip())



def seconds_to_time(seconds):
	'''Converts seonds as an int to a string with minutes and seconds'''
	minutesLeft = seconds // 60
	secondsLeft = seconds % 60

	if (minutesLeft == 1):
		minutesText = " minute "
	else:
		minutesText = " minutes "

	if (secondsLeft == 1):
		secondsText = " second"
	else:
		secondsText = " seconds"

	if secondsLeft == 0:
		return str(minutesLeft) + minutesText
	if minutesLeft == 0:
		return str(secondsLeft) + secondsText
	return str(minutesLeft) + minutesText + "and " + str(secondsLeft) + secondsText


class ReminderWindow(tk.Frame):


	def __init__(self, master):
		tk.Frame.__init__(self, master)
		self.pack()
		self.master.title("")
		#hide title bar
		root.overrideredirect(1)
		#cannot resize on X or Y axis
		self.master.resizable(False,False)
	 	# '#ececec' is the standard gray background of El Capitain
		self.master.tk_setPalette(background='#ececec')
		#make closing the window the same as snooze
		self.master.protocol("WM_DELETE_WINDOW", self.click_snooze)
		#key bindings TODO when you know which will be default, make sure to add "event=None" to function
		#self.master.bind("<Return>", self.click_restart)
		#self.master.bind("<Escape>", self.click_snooze)
		#put the window roughly in the middle of the screen
		x = (self.master.winfo_screenwidth() - self.master.winfo_reqwidth()) / 3
		#no clue why these are indented but leave them that way
        	y = (self.master.winfo_screenheight() - self.master.winfo_reqheight()) / 3
        	self.master.geometry("+{}+{}".format(x, y))
		#get rid of menu bar
		self.master.config(menu=tk.Menu(self))
		
		#text with some padding
		dialog_frame = tk.Frame(self)
		dialog_frame.pack(padx=20, pady=15)
		tk.Label(dialog_frame, text=REMINDER_LABEL).pack()

		#text and progress barw ith  time remaining
		timer_frame = tk.Frame(self)
		timer_frame.pack(padx=20, pady=20)

		tk.Label(timer_frame, text = "Time remaining: ").pack()
		self.timerLabel = tk.Label(timer_frame, text = seconds_to_time(DELAY_TIME))
		self.timerLabel.pack()

		self.progress = ttk.Progressbar(timer_frame, orient='horizontal', length=500, mode='determinate')
		self.progress.pack()
		#get initial time for progress bar
		self.initial = DELAY_TIME

		#add buttons in a frame
		button_frame = tk.Frame(self)
		button_frame.pack(padx=15, pady=(0, 15), anchor="e")
		self.snoozeLabel = tk.Label(button_frame, text = "You can delay the update _ times			")
		self.snoozeLabel.pack(side = "left")
		tk.Button(button_frame, text = "Restart Now", default = "active", command=self.click_restart).pack(side="right")
		tk.Button(button_frame, text = "Snooze", command = self.click_snooze).pack(side="right")

	def click_restart(self):
		print "The user clicked restart"
		#Call the terminal command to restart and install updates

	def click_snooze(self):
		print "The user clicked snooze"
		self.master.destroy()

	def user_exits(self):
		'''Called either from click_snooze or by exiting the program. Must be separate from snooze to
		capture exits from right clicking the dock icon'''
		print "the user exited"

	def decrement_timer(self):
		global DELAY_TIME
		if DELAY_TIME == 0:
			self.click_restart()

		self.timerLabel.configure(text = seconds_to_time(DELAY_TIME))

		#handle progress bar
		percent = 100 - (100 * (float(DELAY_TIME) / float(self.initial)))
		#print DELAY_TIME, self.initial, percent
		self.progress['value'] = percent

		DELAY_TIME = DELAY_TIME -1
		reminder.after(UPDATE_RATE, reminder.decrement_timer)

	def display_snoozes_remaining(self, remaining):
		self.snoozeLabel.configure(text = "You can delay the update %d times			" %(remaining))



#This window is displayed when the user is out of chances and must restart
class UpdateWindow(tk.Frame):


	def __init__(self, master):
		tk.Frame.__init__(self, master)
		self.pack()
		self.master.title("")
		#hide title bar
		root.overrideredirect(1)
		#cannot resize on X or Y axis
		self.master.resizable(False,False)
	 	# '#ececec' is the standard gray background of El Capitain
		self.master.tk_setPalette(background='#ececec')
		#key bindings TODO when you know which will be default, make sure to add "event=None" to function
		#self.master.bind("<Return>", self.click_restart)
		#self.master.bind("<Escape>", self.click_snooze)
		#put the window roughly in the middle of the screen
		x = (self.master.winfo_screenwidth() - self.master.winfo_reqwidth()) / 3
		#no clue why these are indented but leave them that way
        	y = (self.master.winfo_screenheight() - self.master.winfo_reqheight()) / 3
        	self.master.geometry("+{}+{}".format(x, y))
		#get rid of menu bar
		self.master.config(menu=tk.Menu(self))
		
		#text with some padding
		dialog_frame = tk.Frame(self)
		dialog_frame.pack(padx=20, pady=15)
		tk.Label(dialog_frame, text=UPDATE_LABEL).pack()

		#text and progress barw ith  time remaining
		timer_frame = tk.Frame(self)
		timer_frame.pack(padx=20, pady=20)

		tk.Label(timer_frame, text = "Time remaining: ").pack()
		self.timerLabel = tk.Label(timer_frame, text = seconds_to_time(DELAY_TIME))
		self.timerLabel.pack()

		self.progress = ttk.Progressbar(timer_frame, orient='horizontal', length=500, mode='determinate')
		self.progress.pack()
		#get initial time for progress bar
		self.initial = DELAY_TIME

		#add buttons in a frame
		button_frame = tk.Frame(self)
		button_frame.pack(padx=15, pady=(0, 15), anchor="e")
		tk.Button(button_frame, text = "Restart Now", default = "active", command=self.click_restart).pack(side="right")

	def click_restart(self):
		print "The user clicked restart"
		#Call the terminal command to restart and install updates
		self.master.destroy()

	def user_exits(self):
		'''Called either from click_snooze or by exiting the program. Must be separate from snooze to
		capture exits from right clicking the dock icon'''
		print "the user exited"

	def decrement_timer(self):
		global DELAY_TIME
		if DELAY_TIME == 0:
			self.click_restart()

		self.timerLabel.configure(text = seconds_to_time(DELAY_TIME))

		#handle progress bar
		percent = 100 - (100 * (float(DELAY_TIME) / float(self.initial)))
		#print DELAY_TIME, self.initial, percent
		self.progress['value'] = percent

		DELAY_TIME = DELAY_TIME -1
		update.after(UPDATE_RATE, update.decrement_timer)



if __name__ == '__main__':
	#get argument: number of snoozes left
	if (len(sys.argv) > 1):
		remaining = int(sys.argv[1])
	else:
		remaining = 1

	if (remaining > 0):
		root = tk.Tk()
		reminder = ReminderWindow(root)
		AppKit.NSApplication.sharedApplication().activateIgnoringOtherApps_(True)
		#make exiting via the dock smooth
		atexit.register(reminder.user_exits)

		reminder.after(UPDATE_RATE, reminder.decrement_timer)
		reminder.after(UPDATE_RATE, reminder.display_snoozes_remaining(remaining))
		reminder.mainloop()
	else:
		root = tk.Tk()
		update = UpdateWindow(root)
		AppKit.NSApplication.sharedApplication().activateIgnoringOtherApps_(True)
		#make exiting via the dock smooth
		atexit.register(update.user_exits)
		update.after(UPDATE_RATE, update.decrement_timer)
		update.mainloop()


