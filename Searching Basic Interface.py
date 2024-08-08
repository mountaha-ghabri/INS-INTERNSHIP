import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
import pandas as pd
import time
from fuzzywuzzy import fuzz

file_path = "C:\\Users\\ghabri\\Downloads\\TESTING.xlsx"
df = pd.read_excel(file_path)

def fuzzy_filter(value, column):
    return df[column].astype(str).apply(lambda x: fuzz.partial_ratio(x, value) >= 86)

def search_data():
    start_time = time.time()
    query = {col: entry_vars[col].get() for col in columns}
    filtered_df = df.copy()
    
    for col, value in query.items():
        if value:
            filtered_df = filtered_df[fuzzy_filter(value, col)]
    
    elapsed_time = time.time() - start_time
    time_left = max(0, 10 - elapsed_time)  
    time_left_str = f"Time Spent: {time_left:.2f} ms"

    if filtered_df.empty:
        result_text.set("No Available Data")
    else:
        result_text.set(f"Found {len(filtered_df)} records")
        display_results(filtered_df)
    
    time_label.config(text=time_left_str)

def display_results(filtered_df):
    result_window = tk.Toplevel(root)
    result_window.title("Search Results")

    tree = ttk.Treeview(result_window, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor=tk.CENTER)

    for index, row in filtered_df.iterrows():
        tree.insert("", tk.END, values=list(row))

    tree.pack(expand=True, fill='both')

root = tk.Tk()
root.title("Data Search App")
root.geometry("900x600")

background_img = PhotoImage(file="C:\\Users\\ghabri\\Downloads\\INS_Tunisie.png")
background_label = tk.Label(root, image=background_img)
background_label.place(relx=0.5, rely=0.5, anchor='center')

canvas = tk.Canvas(root, bg='light grey')
canvas.pack(side="left", fill="both", expand=True)

scroll_y = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scroll_y.pack(side="right", fill="y")

scroll_x = tk.Scrollbar(root, orient="horizontal", command=canvas.xview)
scroll_x.pack(side="bottom", fill="x")

canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

frame = tk.Frame(canvas, bg='lightgrey')
canvas.create_window((0, 0), window=frame, anchor="nw")

def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

frame.bind("<Configure>", on_frame_configure)

columns = df.columns.tolist()
entry_vars = {}

max_columns = 3  
padding = 5  

for i, col_name in enumerate(columns):
    row = i // max_columns
    col = i % max_columns
    tk.Label(frame, text=col_name, bg='lightgrey').grid(row=row, column=col*2, sticky='w', padx=padding, pady=padding)
    entry_var = tk.StringVar()
    tk.Entry(frame, textvariable=entry_var, width=25).grid(row=row, column=col*2 + 1, padx=padding, pady=padding, sticky='w')
    entry_vars[col_name] = entry_var

search_button = tk.Button(frame, text="Search", command=search_data, bg='lightgray')
search_button.grid(row=(len(columns) // max_columns) + 1, columnspan=max_columns*2, pady=padding)

result_text = tk.StringVar()
result_label = tk.Label(frame, textvariable=result_text, fg='red', bg='lightgrey')
result_label.grid(row=(len(columns) // max_columns) + 2, columnspan=max_columns*2)

time_label = tk.Label(frame, text="", fg='blue', bg='lightgrey')
time_label.grid(row=(len(columns) // max_columns) + 3, columnspan=max_columns*2)

root.mainloop()