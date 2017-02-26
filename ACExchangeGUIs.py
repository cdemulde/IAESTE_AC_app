#(c) chaimdemulder, 2017

#Usage packages
import os
import pandas as pd
#import matplotlib.pyplot as plt
#import seaborn as sns

#GUI packages
import Tkinter as tk
from Tkconstants import *
import tkFileDialog
import tkMessageBox
from PIL import Image, ImageTk

class ReadData():
    def __init__(self,root):
        """
        Open an initial frame to read in the A-form data that can be used
        to compare an offer vs the demand for it.
        
        IMPORTANT!
        _out always means it concerns belgian students (for example country_out is the country of preference
        for a Belgian student)
        _in always means incoming, i.e. information about an exchanged internship, e.g. study_in contains 
        information on the field of an exchanged internship)
        """
        ###
        #create window to read in the data
        ###
        self.popup = tk.Frame(root,width=100,height=20)
        self.popup.grid(columns=2,rows=3)
        self.intro = tk.Label(self.popup, text='Enter the path to the A-form data file (usually csv)')
        self.intro.grid(column=1,row=0,columnspan=2)
        self.data_file = tk.StringVar()        
        self.docstring = tk.Entry(self.popup, textvariable=self.data_file)
        self.docstring.grid(column=1,row=2)
        self.docstring.config(width=75)
        
        #set default value for the data file
        self.data_file.set('./interests.csv')
        
        ###
        #browse button
        ###
        self.browse = tk.Button(self.popup, text='Browse', command = self.browse_files_in)
        self.browse.grid(column=2,row=2)
        
        ###
        #read button
        ###
        self.read = tk.Button(self.popup, text='OK', command = self.read_data)
        self.read.grid(column=1,row=3)
        
    def browse_files_in(self,*args):
        """
        Browse through files to choose the one containing the A-form data
        """
        path_to_data = tkFileDialog.askopenfilename()
        #show chosen value in textframe
        self.docstring.delete(0,tk.END)
        self.docstring.insert(0,path_to_data)
        #use chosen value as self.data_file
        self.data_file.set(path_to_data)
        
    def read_data(self,*args):
        """
        Read the data from the given file, i.e. from the file given by the entered
        path. This should be a csv (or alike) file, with columns separated by commas.
        """
        doc = str(self.data_file.get())
        try:
            self.data = pd.read_csv(doc,sep=',')
            self.popup.destroy()
            
        except:
            tkMessageBox.showwarning(title='File not found',
            message='The file you entered does not exist in this location')
            return None
        self.interest_frame = InterestFrame(self.data)
        self.add_offer_frame = AddOfferFrame()

class InterestFrame():
    def __init__(self,data):
        """
        Open new frame to check for interest in a certain internship
        """
        ###
        #Save/accept data from ReadData frame
        ###
        self.data = data
        
        ###
        #create tkinter window
        ###
        self.check_interest_frame = tk.Toplevel()
        self.check_interest_frame.title('Check interest')
        self.check_interest_frame.geometry('800x250')
        
        #set a background image
        self.canvas = tk.Canvas(self.check_interest_frame)
        self.canvas.grid(column=0,row=0,columnspan=2,rowspan=7,sticky=N+W+S+E)
        self.background_image = Image.open('/Users/chaimdemulder/Desktop/IAESTE/Exchange/background.png')
        self.background = ImageTk.PhotoImage(self.background_image)
        self.canvas.img = self.background
        self.canvas.create_image(0,0,anchor=NW,image=self.background)
        
        #self.background_label = tk.Canvas(self.check_interest_frame,image=self.background)
        #self.background_label.image = self.background
        #self.background_label.grid(column=0,row=0,columnspan=2,rowspan=7,sticky=N+W+S+E)
        #self.background_label.place(x=0,y=0,relwidth=1,relheight=1)
        
        ###
        #explain what this frame does
        ###
        self.explain = tk.Label(self.check_interest_frame,text='Enter the country and field of the internship you want to check interest for (case sensitive!)')
        self.explain.grid(column=1,row=1,columnspan=2)
        
        ###
        #create tkinter frame with widgets
        ###
        #self.interest = tk.Frame(self.check_interest_frame)
        #self.interest.grid(columns=3,rows=7)
        #self.intro = tk.Label(self.interest, 
        #                      text='Enter the study field and the country of the internship')
        #self.intro.grid(columnspan=2,row=1,stick=W)

        ###
        #Enter study field and country
        ###
        self.label_study_out = tk.Label(self.check_interest_frame, text='Study field')
        self.label_study_out.grid(column=1,row=2,sticky=W)
        self.study_out = tk.StringVar()
        self.entry_study_out = tk.Entry(self.check_interest_frame, textvariable=self.study_out)
        self.entry_study_out.grid(column=2,row=2)

        self.label_country_out = tk.Label(self.check_interest_frame, text='Country')
        self.label_country_out.grid(column=1,row=3,sticky=W)
        self.country_out = tk.StringVar()
        self.entry_country_out = tk.Entry(self.check_interest_frame, textvariable=self.country_out)
        self.entry_country_out.grid(column=2,row=3)

        ###
        #Check interest
        ###
        self.button_check = tk.Button(self.check_interest_frame,text='Check interest',command=self.check_interest)
        self.button_check.grid(column=2,row=4)

        ###
        #Show possibly interested people
        ###
        self.nr_interested = tk.Label(self.check_interest_frame, text='Number of interested students')
        self.nr_interested.grid(column=1,row=5,sticky=W)
        self.output_nr_interested = tk.Label(self.check_interest_frame,text='')
        self.output_nr_interested.grid(column=2,row=5)
        
        self.min_duration = tk.Label(self.check_interest_frame, text='Minimum duration')
        self.min_duration.grid(column=1,row=6,sticky=W)
        self.output_min_duration = tk.Label(self.check_interest_frame,text='')
        self.output_min_duration.grid(column=2,row=6)
        
        self.max_duration = tk.Label(self.check_interest_frame, text='Maximum duration')
        self.max_duration.grid(column=1,row=7,sticky=W)
        self.output_max_duration = tk.Label(self.check_interest_frame,text='')
        self.output_max_duration.grid(column=2,row=7)
        
        self.levels = tk.Label(self.check_interest_frame, text='Study levels')
        self.levels.grid(column=1,row=8,sticky=W)
        self.output_levels = tk.Label(self.check_interest_frame,text='')
        self.output_levels.grid(column=2,row=8)
            
    def check_interest(self):
        dataset = self.data
        country_ = self.entry_country_out.get()
        study_ = self.entry_study_out.get()
        if study_ == '' and country_ == '':
            data = dataset
    
        elif study_ == '':
            values_countries = {'Preferred country 1':[country_],
                                'Preferred country 2':[country_],
                                'Preferred country 3':[country_]}
            mask = dataset.isin(values_countries).any(1)
            data = dataset[mask]
            if data.empty:
                tkMessageBox.showwarning(title='No candidates',
                message='No students indicated an interest in these internship specifics')
                return None
                
        elif country_ == '':
            data = dataset[dataset['Study Field'].str.contains(study_)]
            if data.empty:
                tkMessageBox.showwarning(title='No candidates',
                message='No students indicated an interest in these internship specifics')
                return None
        else:
            values_countries = {'Preferred country 1':[country_],
                                'Preferred country 2':[country_],
                                'Preferred country 3':[country_]}
            mask = dataset.isin(values_countries).any(1)
            data = dataset[mask]
            data = data[data['Study Field'].str.contains(study_)]
            if data.empty:
                tkMessageBox.showwarning(title='No candidates',
                message='No students indicated an interest in these internship specifics')
                return None
                  
        nr_interested = len(data)
        percentage_interested = float(nr_interested)*100/len(dataset)
        min_duration = min(data['Minimum duration of your internship'])
        max_duration = max(data['Maximum duration of your internship'])
        levels = data['Year'].unique()
        
        self.output_nr_interested.config(text=str(nr_interested)+' ('+str(percentage_interested)+'%)')
        self.output_min_duration.config(text=str(min_duration))
        self.output_max_duration.config(text=str(max_duration))
        self.output_levels.config(text=', '.join([x for x in levels]))
        
class AddOfferFrame():
    def __init__(self):
        """
        Open new frame to add an exchange internship to the list of exchanged internships
        """
        ###
        #initialize self.exchanged to contain the exchange offer data
        ###
        self.exchanged = pd.DataFrame()
        
        ###
        #create tkinter window
        ###
        self.add_internship = tk.Toplevel()
        self.add_internship.title('Add internship')
        
        ###
        #explain what this frame does
        ###        
        self.explain = tk.Label(self.add_internship,text='Enter the data of the exchanged internship to add to the list of exchanged offers')
        self.explain.grid(column=1,row=0,columnspan=2)
        
        ###
        #Internship data
        ###
        self.label_domestic_code =  tk.Label(self.add_internship, text='Exchanged for offer (ref nr)')
        self.label_domestic_code.grid(column=1,row=1,sticky=W)
        self.domestic_code = tk.StringVar()
        self.entry_domestic_code = tk.Entry(self.add_internship, textvariable=self.domestic_code)
        self.entry_domestic_code.grid(column=2,row=1)
        
        self.label_code = tk.Label(self.add_internship, text='Reference number')
        self.label_code.grid(column=1,row=2,sticky=W)
        self.code = tk.StringVar()
        self.entry_code = tk.Entry(self.add_internship, textvariable=self.code)
        self.entry_code.grid(column=2,row=2)
        
        self.label_country_in = tk.Label(self.add_internship, text='Country')
        self.label_country_in.grid(column=1,row=3,sticky=W)
        self.country_in = tk.StringVar()
        self.entry_country_in = tk.Entry(self.add_internship, textvariable=self.country_in)
        self.entry_country_in.grid(column=2,row=3)
        
        self.label_study_in = tk.Label(self.add_internship, text='Field')
        self.label_study_in.grid(column=1,row=4,sticky=W)
        self.study_in = tk.StringVar()
        self.entry_study_in = tk.Entry(self.add_internship, textvariable=self.study_in)
        self.entry_study_in.grid(column=2,row=4)
        
        self.label_duration_min = tk.Label(self.add_internship, text='Min duration (weeks)')
        self.label_duration_min.grid(column=1,row=5,sticky=W)
        self.duration_min = tk.StringVar()
        self.entry_duration_min = tk.Entry(self.add_internship, textvariable=self.duration_min)
        self.entry_duration_min.grid(column=2,row=5)
        
        self.label_duration_max = tk.Label(self.add_internship, text='Max duration (weeks)')
        self.label_duration_max.grid(column=1,row=6,sticky=W)
        self.duration_max = tk.StringVar()
        self.entry_duration_max = tk.Entry(self.add_internship, textvariable=self.duration_max)
        self.entry_duration_max.grid(column=2,row=6)
        
        ###
        #File to save offers to
        ###
        self.exchanged_offers_filepath = tk.StringVar()        
        self.docstring_offers = tk.Entry(self.add_internship, textvariable=self.exchanged_offers_filepath)
        self.docstring_offers.grid(column=1,row=7)
        self.docstring_offers.config(width=30)
        
        #set default value for the data file
        self.exchanged_offers_filepath.set('./exchanged.csv')
        #self.docstring_offers.insert(0,'Exchanged_2017.csv')
        
        self.browse = tk.Button(self.add_internship, text='Browse', command = self.browse_files_out)
        self.browse.grid(column=2,row=7)
        
        ###
        #Add offer button
        ###
        self.add_offer_button = tk.Button(self.add_internship,text='Add offer',command=self.add_offer)
        self.add_offer_button.grid(column=2,row=8)
        
        ###
        #Plot buttons
        ###
        self.plot_countries_button = tk.Button(self.add_internship,text='Plot by country',command=self.plot_countries)
        self.plot_countries_button.grid(column=1,row=9,sticky=E)
        self.plot_studies_button = tk.Button(self.add_internship,text='Plot by field',command=self.plot_studies)
        self.plot_studies_button.grid(column=2,row=9)
    
    def add_offer(self,*args):
        """
        Adds offer to the list of exchanged offers
        """
        to_read = str(self.exchanged_offers_filepath.get())
        if not os.path.isfile(to_read):
            if tkMessageBox.askyesno(title="File doesn't exist yet",message="The filename or the location you entered does not exist yet. Do you want to create it?"):
                #could probably be improved
                empty = pd.DataFrame(columns=['domestic offer code','foreign offer code','country','field','min duration','max duration'])
                empty.to_csv(to_read)
            else:
                return None                                    
        
        self.exchanged = pd.read_csv(to_read,sep=',',usecols=['domestic offer code','foreign offer code','country','field','min duration','max duration'])
        ###
        #check if offer already exists, or if user is trying to add an offer without reference number
        ###
        if str(self.entry_code.get()) in self.exchanged['foreign offer code'].values:
            tkMessageBox.showwarning(title='Offer cannot be added',
            message='This offer is already in the list with exchanged offers and cannot be added twice!')
        elif str(self.entry_code.get()) == '':
            tkMessageBox.showwarning(title='Empty Reference number',
            message='You cannot add an offer without a reference number!')
        ###
        #add the offer
        ###
        else:
            self.exchanged = self.exchanged.append(pd.DataFrame([str(self.entry_domestic_code.get()),
                                                                 str(self.entry_code.get()),
                                                                 str(self.entry_country_in.get()),
                                                                 str(self.entry_study_in.get()),
                                                                 str(self.entry_duration_min.get()),
                                                                 str(self.entry_duration_min.get())],
                                                                 index=['domestic offer code','foreign offer code','country','field','min duration','max duration']).transpose())
            self.exchanged.to_csv(to_read)
            tkMessageBox.showinfo(title='Offer added',
            message='Offer successfully added!\n Click "Show offers" to have a look at the offers currently exchanged')
            
    def browse_files_out(self,*args):
        """
        Browse through files to pick one in which to save the exchanged offers
        """
        path_to_data = tkFileDialog.askopenfilename()
        #show chosen value in textframe
        self.docstring_offers.delete(0,tk.END)
        self.docstring_offers.insert(0,path_to_data)
        #use chosen value as self.exchanged_offers_filepa
        self.exchanged_offers_filepath.set(path_to_data)        
        
    def check_study(self,dataset,study):
        return dataset[dataset['field'].str.contains(study)]
        
    def check_country(self,dataset,country):
        return dataset[dataset['country'].str.contains(country)]
            
    def plot_studies(self):
        """
        Shows a popup figure with a bar graph showing the study fields of the 
        currently exchanged internships
        """
        import matplotlib.pyplot as plt
        import seaborn as sns
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        ###
        #check if internships are available in the given file
        ###
        to_read = str(self.exchanged_offers_filepath.get())
        if not os.path.isfile(to_read):
            tkMessageBox.showwarning(title="File doesn't exist",message="The filename or the location you entered does not exist!")
            return None
        else:
            self.exchanged = pd.read_csv(to_read,sep=',',usecols=['domestic offer code','foreign offer code','country','field','min duration','max duration'])
            
        if self.exchanged.empty:
            tkMessageBox.showwarning(title="No available data",
                                     message="No exchanged offers are available in the given file! Add some offers first and try again later")
            return None
        else:
            ###
            #define study fields to use for plotting
            ###
            studies=['Bio','Environment','Mechanic','Electric','Physic','Civil','Chemi','Material','Computer','Architecture']
        
            ###
            #use pandas functionalities for the plots
            ###  
            frequency = pd.DataFrame()
            for univ in studies:
                frequency[univ] = [len(self.check_study(self.exchanged,univ))]
            frequency = frequency.transpose()
            
            ###
            #make figure
            ###
            fig, ax = plt.subplots()
            frequency.sort_index().plot(ax=ax,kind='bar',figsize=(8,6))
            ax.tick_params(axis='both', labelsize=16)
            ax.set_xticklabels(ax.xaxis.get_ticklabels(),rotation=45)
            fig.tight_layout()

            ###
            #show figure in new tkinter window, and adjust window size to figure size
            ###
            figure_window_1 = tk.Toplevel()
            figure_window_1.title('Figure')
            #figure_window_1.geometry()
            #print()
        
            ###
            #create label to put figure in
            ###
            figure_canvas = FigureCanvasTkAgg(fig,master=figure_window_1)
            figure_canvas.get_tk_widget().grid(column=0,row=0)
            #pix_in_inch = figure_window_1.winfo_pixels('1i') #number of pixels in 1 inch
            #figure_canvas.get_tk_widget().geometry('{}x{}'.format(int(fig.get_figwidth()*pix_in_inch),
            #                                        int(fig.get_figheight()*pix_in_inch)))
            
    def plot_countries(self):
        """
        Shows a popup figure with a bar graph showing the study fields of the 
        currently exchanged internships
        """
        import matplotlib.pyplot as plt
        import seaborn as sns
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        ###
        #check if internships are available in the given file
        ###
        to_read = str(self.exchanged_offers_filepath.get())
        if not os.path.isfile(to_read):
            tkMessageBox.showwarning(title="File doesn't exist",message="The filename or the location you entered does not exist!")
            return None
        else:
            self.exchanged = pd.read_csv(to_read,sep=',',usecols=['domestic offer code','foreign offer code','country','field','min duration','max duration'])
            
        if self.exchanged.empty:
            tkMessageBox.showwarning(title="No available data",
                                     message="No exchanged offers are available in the given file! Add some offers first and try again later")
            return None
        else:
            ###
            #use pandas functionalities for the plots
            ###    
            frequency = pd.DataFrame()    
            for country in self.exchanged['country'].unique():
                frequency[country] = [len(self.check_country(self.exchanged,country))]
            frequency = frequency.transpose()
            frequency.columns=['values']
            
            ###
            #making figure
            ###
            fig, ax = plt.subplots(figsize=(4,14))
            frequency.sort_values(by='values').plot(ax=ax,kind='barh',figsize=(4,10))
            ax.tick_params(axis='both', labelsize=16)
            fig.tight_layout()

            ###
            #show figure in new tkinter window
            ###
            figure_window_2 = tk.Toplevel()
            figure_window_2.title('Figure')
        
            ###
            #create label to put figure in
            ###
            figure_canvas = FigureCanvasTkAgg(fig,master=figure_window_2)
            figure_canvas.get_tk_widget().grid(column=0,row=0)            
        
root = tk.Tk()
app = ReadData(root)
root.mainloop()

#root.bind('<Return>')
#root.mainloop()

#check_and_add.bind('<Return>', check_interest)
#check_and_add.mainloop()