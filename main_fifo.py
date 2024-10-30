import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import TclError
from tkcalendar import DateEntry
from tktooltip import ToolTip
import fifo
import os
import sys



def resource_path(relative_path):
	try:
		base_path = sys._MEIPASS2
	except Exception:
		base_path = os.path.abspath(".")

	return os.path.join(base_path, relative_path)


def main():
	app = Application()
	app.mainloop()


class Application(tk.Tk):
	purchase_list = []
	sales_list = []
	do_not_run_azure = False

	def __init__(self):
		super().__init__()
		self.title("FIFO Inventory Calculator")
		self.resizable(False, False)
		try:
			self.tk.call("source", resource_path(r"assets/Azure-ttk-theme-2.1.0/azure.tcl"))
			self.tk.call("set_theme", "light")
		except TclError:
			Application.do_not_run_azure = True
		frame = InputForm(self, "Purchases", "Purchases", "Unit Cost ($)")
		frame.grid(row=0, column=0, padx=5, pady=5)
		frame2 = InputForm(self, "Sales", "Sales", "Unit Price ($)")
		frame2.grid(row=1, column=0, padx=5, pady=5)
		frame3 = InventoryForm(self)
		frame3.grid(row=2, column=0, padx=5, pady=5)
		cogs = ResultForm(self, "Cost of Goods Sold ($)")
		cogs.grid(row=0, column=1, padx=5)
		revenue = ResultForm2(
			self, "Sales Revenue ($)", "Gross Profit ($)", "Gross Margin (%)"
		)
		revenue.grid(row=1, column=1, padx=5)
		try:
			img = tk.PhotoImage("photo", file=resource_path("assets/box.png"))
			self.tk.call("wm", "iconphoto", self._w, img)
		except TclError:
			pass
		

		def calculation():
			cogs.result_list.delete(0, "end")
			revenue.result_list.delete(0, "end")
			revenue.result_list2.delete(0, "end")
			revenue.result_list3.delete(0, "end")
			frame3.batch_no.delete(0, tk.END)
			frame3.date_list.delete(0, tk.END)
			frame3.quantity_list.delete(0, tk.END)
			frame3.price_list.delete(0, tk.END)
			frame.get_data()
			frame2.get_data()
			calc_result = fifo.Inventory(self.purchase_list, self.sales_list)
			try:
				cogs_text = calc_result.cogs()
			except fifo.SalesMoreThanInventoryError:
				messagebox.showerror(
					"Calculation Error",
					"You cannot sell more than you have in your inventory!",
				)
			else:
				cogs.result_list.insert(tk.END, f"{cogs_text:.2f}")
				revenue_text = calc_result.sales_revenue()
				revenue.result_list.delete(0, "end")
				revenue.result_list.insert(tk.END, f"{revenue_text:.2f}")
				leftover_inventory = calc_result.leftover_inventory()
				gross_profit = revenue_text - cogs_text
				revenue.result_list2.delete(0, "end")
				revenue.result_list2.insert(tk.END, f"{gross_profit:.2f}")
				if cogs_text == 0:
					gross_margin = 0
				else:
					gross_margin = (revenue_text - cogs_text) * 100 / revenue_text
				revenue.result_list3.delete(0, "end")
				revenue.result_list3.insert(tk.END, f"{gross_margin:.2f}%")

				if leftover_inventory:
					for i in leftover_inventory:
						leftover_purchases, leftover_quantity, leftover_price = (
							i.date_iso,
							i.quantity,
							i.unit_price,
						)
						frame3.batch_no.insert(tk.END, i.index)
						frame3.date_list.insert(tk.END, leftover_purchases)
						frame3.quantity_list.insert(tk.END, leftover_quantity)
						frame3.price_list.insert(tk.END, f"{leftover_price:.2f}")

		calculate_button = ttk.Button(self, text="Calculate", command=calculation)
		calculate_button.grid(row=2, column=1, rowspan=2, ipadx=10, ipady=10)


enterkey = "<Enter>"
leavekey = "<Leave>"
returnkey = "<Return>"
mousewheel = "<MouseWheel>"
scrollkey = "scroll"
date_order_msg = "Advice: Dates should be relative, purchases are added first.\nUse different dates for purchases and sales on the same day."


class InputForm(ttk.Frame):
	def __init__(self, parent, name: str, button_label: str, price_label: str):
		super().__init__(parent)
		box_height = 4
		padx_no = 5
		list_width = 17
		self.name = name
		self.button_label = button_label
		self.price_label = price_label

		self.label = ttk.Label(self, text=name, font={"size": 13})
		self.label.grid(row=0, column=0, padx=padx_no, columnspan=2, sticky="w")

		self.batch_label = ttk.Label(self, text="No.")
		self.batch_label.grid(row=2, column=0, padx=padx_no)

		self.date_label = ttk.Label(self, text="Date")
		self.date_label.grid(row=1, column=1, padx=padx_no)
		self.date_label_tooltip = ToolTip(self.date_label, msg=date_order_msg)

		self.date = DateEntry(self, date_pattern="yyyy-MM-dd", width=list_width - 3)
		self.date.grid(row=2, column=1)
		self.date_tooltip = ToolTip(self.date, msg=date_order_msg)

		self.quantity_label = ttk.Label(self, text="Quantity")
		self.quantity_label.grid(row=1, column=2, padx=padx_no)

		quantity_choices = (1, 2, 3, 4, 5, 10, 20, 30, 50, 100)
		self.quantity = ttk.Combobox(
			self, values=quantity_choices, width=list_width - 3
		)
		self.quantity.grid(row=2, column=2)

		self.price_label = ttk.Label(self, text=price_label)
		self.price_label.grid(row=1, column=3, padx=padx_no)

		self.price_entry = ttk.Entry(self, width=list_width)
		self.price_entry.grid(row=2, column=3)

		self.price_entry.bind(returnkey, self.get_data)
		self.quantity.bind(returnkey, self.get_data)

		self.button = ttk.Button(self, text=button_label, command=self.get_data)
		self.button.grid(row=0, column=3)

		self.text_scroll = ttk.Scrollbar(self)
		self.text_scroll.grid(row=3, column=4)

		self.batch_no = tk.Listbox(
			self, height=box_height, width=4, yscrollcommand=self.text_scroll.set
		)
		self.batch_no.grid(row=3, column=0, sticky="w")
		self.batch_no.bind(mousewheel, self.on_mouse_wheel)

		self.date_list = tk.Listbox(
			self,
			height=box_height,
			width=list_width,
			yscrollcommand=self.text_scroll.set,
		)
		self.date_list.grid(row=3, column=1, padx=padx_no)
		self.date_list.bind(mousewheel, self.on_mouse_wheel)
		self.date_list_tooltip = ToolTip(self.date_list, msg=date_order_msg)

		self.quantity_list = tk.Listbox(
			self,
			height=box_height,
			width=list_width,
			yscrollcommand=self.text_scroll.set,
		)
		self.quantity_list.grid(row=3, column=2, padx=padx_no)
		self.quantity_list.bind(mousewheel, self.on_mouse_wheel)

		self.price_list = tk.Listbox(
			self,
			height=box_height,
			width=list_width,
			yscrollcommand=self.text_scroll.set,
		)
		self.price_list.grid(row=3, column=3, padx=padx_no)
		self.price_list.bind(mousewheel, self.on_mouse_wheel)

		self.text_scroll.config(command=self.multiple_yview)

		self.clear_button = ttk.Button(self, text="Clear", command=self.clear_data)
		self.clear_button.grid(row=0, column=2)

	def multiple_yview(self, *args):
		self.batch_no.yview(*args)
		self.date_list.yview(*args)
		self.quantity_list.yview(*args)
		self.price_list.yview(*args)

	def on_mouse_wheel(self, event):
		self.batch_no.yview(scrollkey, event.delta, "units")
		self.date_list.yview(scrollkey, event.delta, "units")
		self.quantity_list.yview(scrollkey, event.delta, "units")
		self.price_list.yview(scrollkey, event.delta, "units")
		# this prevents default bindings from firing, which
		# would end up scrolling the widget twice
		return "break"

	def get_data(self, event=None):
		date_entry = self.date.get_date()
		quantity = self.quantity.get()
		price = self.price_entry.get()

		if (quantity != "") and (price != ""):
			valueerror = "Value Error"
			try:
				int(quantity)
				float(price)
			except ValueError:
				messagebox.showerror(valueerror, "Please enter a valid number")
			else:
				if int(quantity) < 0:
					messagebox.showerror(valueerror, "Quantity cannot be negative!")
				elif float(price) < 0:
					messagebox.showerror(valueerror, "Price cannot be negative!")
				else:
					if self.name == "Purchases":
						item = fifo.Purchases(date_entry, int(quantity), float(price))
						Application.purchase_list.append(item)
					if self.name == "Sales":
						item = fifo.Sales(date_entry, int(quantity), float(price))
						Application.sales_list.append(item)
					self.batch_no.insert(tk.END, item.index)
					self.date_list.insert(tk.END, date_entry)
					self.quantity_list.insert(tk.END, quantity)

					self.quantity.delete(0, tk.END)
					self.price_list.insert(tk.END, price)
					self.price_entry.delete(0, tk.END)

	def clear_data(self, event=None):
		if (self.name == "Purchases") and (Application.purchase_list):
			Application.purchase_list = []
		if self.name == "Sales" and (Application.sales_list):
			Application.sales_list = []
		self.batch_no.delete(0, tk.END)
		self.date_list.delete(0, tk.END)
		self.quantity_list.delete(0, tk.END)
		self.price_list.delete(0, tk.END)


class InventoryForm(ttk.Frame):
	def __init__(self, parent):
		super().__init__(parent)

		padx_no = 5
		box_height = 4
		list_width = 17

		self.text_scroll = ttk.Scrollbar(self)
		self.text_scroll.grid(row=2, column=4)

		self.label = tk.Label(self, text="Leftover Inventory", font={"size": 13})
		self.label.grid(row=0, column=0, padx=padx_no, columnspan=2, sticky="w")

		self.batch_label = tk.Label(self, text="No.")
		self.batch_label.grid(row=1, column=0, padx=padx_no)

		self.date_label = tk.Label(self, text="Date")
		self.date_label.grid(row=1, column=1, padx=padx_no)

		self.quantity_label = tk.Label(self, text="Quantity")
		self.quantity_label.grid(row=1, column=2, padx=padx_no)

		self.price_label = tk.Label(self, text="Unit Price ($)")
		self.price_label.grid(row=1, column=3, padx=padx_no)

		self.batch_no = tk.Listbox(self, height=box_height, width=4)
		self.batch_no.grid(row=2, column=0, sticky="w")
		self.batch_no.bind(mousewheel, self.on_mouse_wheel)

		self.date_list = tk.Listbox(self, height=box_height, width=list_width)
		self.date_list.grid(row=2, column=1, padx=padx_no)
		self.date_list.bind(mousewheel, self.on_mouse_wheel)

		self.quantity_list = tk.Listbox(self, height=box_height, width=list_width)
		self.quantity_list.grid(row=2, column=2, padx=padx_no)
		self.quantity_list.bind(mousewheel, self.on_mouse_wheel)

		self.price_list = tk.Listbox(self, height=box_height, width=list_width)
		self.price_list.grid(row=2, column=3, padx=padx_no)
		self.price_list.bind(mousewheel, self.on_mouse_wheel)

		self.text_scroll.config(command=self.multiple_yview)

	def multiple_yview(self, *args):
		self.batch_no.yview(*args)
		self.date_list.yview(*args)
		self.quantity_list.yview(*args)
		self.price_list.yview(*args)

	def on_mouse_wheel(self, event):
		self.batch_no.yview("scroll", event.delta, "units")
		self.date_list.yview("scroll", event.delta, "units")
		self.quantity_list.yview("scroll", event.delta, "units")
		self.price_list.yview("scroll", event.delta, "units")
		# this prevents default bindings from firing, which
		# would end up scrolling the widget twice
		return "break"


class ResultForm(tk.Frame):
	def __init__(self, parent, label_text: str):
		super().__init__()
		self.label_text = label_text
		self.label = tk.Label(self, text=self.label_text)
		self.label.grid(row=1, column=0)
		box_height = 1
		self.result_list = tk.Listbox(self, height=box_height)
		self.result_list.grid(row=2, column=0)
		if Application.do_not_run_azure is False:
			self.dark_mode_button = ttk.Checkbutton(
				self,
				text="Light/Dark",
				style="Switch.TCheckbutton",
				command=self.change_theme,
			)
			self.dark_mode_button.grid(row=0, column=0, pady=15, sticky="n")

	def change_theme(self):
		# NOTE: The theme's real name is azure-<mode>
		if self.tk.call("ttk::style", "theme", "use") == "azure-dark":
			# Set light theme
			self.tk.call("set_theme", "light")
		else:
			# Set dark theme
			self.tk.call("set_theme", "dark")


class ResultForm2(tk.Frame):
	def __init__(self, parent, label_text: str, label_text2: str, label_text3: str):
		super().__init__(parent)
		box_height = 1
		self.label_text = label_text
		self.label = tk.Label(self, text=self.label_text)
		self.label.grid(row=0, column=0)
		self.result_list = tk.Listbox(self, height=box_height)
		self.result_list.grid(row=1, column=0)
		self.label_text2 = label_text2
		self.label2 = tk.Label(self, text=self.label_text2)
		self.label2.grid(row=2, column=0)
		self.result_list2 = tk.Listbox(self, height=box_height)
		self.result_list2.grid(row=3, column=0)

		self.label_text3 = label_text3
		self.label3 = tk.Label(self, text=self.label_text3)
		self.label3.grid(row=4, column=0)
		self.result_list3 = tk.Listbox(self, height=box_height)
		self.result_list3.grid(row=5, column=0)


if __name__ == "__main__":
	main()
