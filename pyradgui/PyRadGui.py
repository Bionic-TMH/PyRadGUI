# TMH radiomics extractor
# Author : Umesh Kumar Baburao Sherkhane
#!/usr/bin/env python
# coding: utf-8

# use --output-labelmap for non-overlapping

import logging
import distutils
from distutils.spawn import find_executable
import sys
#sys.modules[__name__].__dict__.clear()

from tkinter import filedialog
from tkinter import *

import os,subprocess,sys,time
from subprocess import run

def check_executable(executable):
    """
    Checks if an executable exists in $PATH.

    Returns:
        True or False
    """
    logger = logging.getLogger(__name__)
    logger.debug("Checking executable '%s'...", executable)
    executable_path = find_executable(executable)
    found = executable_path is not None
    if found:
        print("Plastimatch  found: '%s'", executable,
                     executable_path)
    else:
        print("Plastimatch not found, please install from http://plastimatch.org/", executable)
    return executable_path 
plasti=check_executable('plastimatch')
print(plasti,'$$$$$$$$')


def select():
    from tkinter import filedialog
    root = Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory()
    select.g=folder_selected
    pathlabel1.config(text=folder_selected)
    return(folder_selected)
    

def select1():
    from tkinter import filedialog
    root = Tk()
    root.withdraw()
    folder_selected1 = filedialog.askdirectory()
    pathlabel.config(text=folder_selected1)
    select1.g=folder_selected1
    return(folder_selected1)
#

def runradio():
    messagebox.showinfo(message= "running radiomics :) ")
    import os,pydicom,numpy,re,shutil
    import time
    import sys
    from datetime import datetime
    import tqdm
    from tkinter import filedialog
    start_time = datetime.now()
    print(start_time)
    #bar()
    #folder_selected = filedialog.askdirectory()
    #Mainpath="F:/share/integrate_dicom_nrrd_radiomics/dicom1/"
    u=select1.g ##@
    Mainpath=u+'/'
    s1=select.g #@
    #Mainpath=u+'/'
    


    os.listdir(Mainpath)

    for gb in tqdm.tqdm(os.listdir(Mainpath)):
        progress['value'] += 100/len(os.listdir(Mainpath))
        
        top.update() 
        time.sleep(0.1)
        print(gb,"----------")

        PathDicom=Mainpath+gb+"/"
        print(PathDicom)





        ###### getting the files and printing their modalities along with the number of images
        rtfiles=[]
        ctfiles=[]
        mrfiles=[]
        ptfiles=[]
        for dirName, subdirList, fileList in os.walk(PathDicom):
           # print(dirName)
            for filename in fileList:
                #print(filename)
                if ".dcm" in filename.lower(): 
                        print(filename)

                        ds = pydicom.filereader.dcmread(os.path.join(dirName, filename))
                        pid=re.sub('/','_',ds.PatientID)
                        if ds.Modality=='RTSTRUCT':
                            print(ds.Modality,'is a rt structure')
                            #pid=re.sub('/','_',ds.PatientID)
                            print(pid,'\n','****')
                            rt1=os.path.join(dirName, filename)
                            print(rt1)
                            rtfiles.append(rt1)
                        if ds.Modality=='CT':
                        #if ds.Modality=='PT':
                        #if ds.Modality=='MR':
                            print(filename,'-----------------')
                            print(ds.Modality)
                            ct=os.path.join(dirName, filename)
                            print(ct)
                            ctfiles.append(ct)
                        if ds.Modality=='MR':
                            print(filename,'-------MR----------')
                            print(ds.Modality)
                            mr=os.path.join(dirName, filename)
                            print(mr)
                            mrfiles.append(mr)
                        if ds.Modality=='PT':
                            print(filename,'-------PT----------')
                            print(ds.Modality)
                            pt=os.path.join(dirName, filename)
                            print(pt)
                            ptfiles.append(pt)
        print('NO of CT images =',len(ctfiles))
        print('NO of MR images =',len(mrfiles))
        print('NO of PT file =',len(ptfiles))
        print('NO of RT file =',len(rtfiles))


        #### select the file path except the dicom file
        if ptfiles:
            u=ptfiles[0].split('\\')
        elif ctfiles:
            u=ctfiles[0].split('\\')
        u1=u.pop()
        ct_ref="\\".join(u)
        print('the reference CT location == ',ct_ref)

        #import re
        #ct_ref1=re.sub(r'\\\d\..*dcm','',ctfiles[0])#
        #ct_ref1



        ########### nrrd conversion pyradiomics
        import os,subprocess,sys,time
        from subprocess import run

        start_time = datetime.now()
        print(start_time)
        ### convert to image nrrd
        command_line_im=[plasti,"convert", "--input",ct_ref,
                      "--output-img" ,'./Data/'+pid+"_image.nrrd"]
        #command_line_im=["./Data/Plastimatch/bin/plastimatch.exe","convert", "--input",ct_ref,
                      #"--output-img" ,pid+"_image.nrrd"]

        print("generating image nrrd_"+pid)
        myproc=run(command_line_im,stdout=subprocess.PIPE)#$
        #messagebox.showinfo("Result", myproc.stdout)#$
        text = tkinter.Text(top)
        text.pack()
        text.insert(END,myproc.stdout)

        #### convert to specific label.mha
        command_line_rt=[plasti,"convert", "--input",rt1,
                      "--output-ss-img" ,'./Data/'+pid+"label_all_delineation.nrrd", "--output-ss-list" ,"outfile.txt",
                     "--referenced-ct", ct_ref, "--output-prefix",'./Data/'+pid+"_mha"]


        print("generating label nrrd_"+pid)
        myproc=run(command_line_rt)#,stdout=subprocess.PIPE)#$$$$$$$
        #messagebox.showinfo("Result", myproc.stdout)#$
        #run(command_line_rt)#$

        end_time = datetime.now()
        print(datetime.now())
        dur=end_time - start_time
        print("took",dur.seconds,"seconds")


        ct_ref

        os.getcwd()


        # get the specific  mha files from current directory
        gtv=[]
        for dirName, subdirList, fileList in os.walk(os.getcwd()):
            if pid+"_mha" in dirName:
                for f in fileList:
                    p=re.findall('(G|g)(T|t)(V|v).*mha',f) or re.findall('(T|t).*mha',f)
                    #p=re.findall('(T|t).*mha',f)
                    if p:
                        print(f)
                        rs=os.path.join(dirName, f)
                        gtv.append(rs)
                    else:
                        print("removing unwanted file",f," for space preservation")
                        un=os.path.join(dirName, f)
                        os.remove(un) 
                        #print(rs)
            if pid+"_image.nrrd" in fileList:
                for f1 in fileList:
                    p1=re.findall(pid+"_image.nrrd",f1)
                    if p1:
                        print(f1)
                        rs1=os.path.join(dirName, f1)
                        #print(rs1)
        print(gtv) # list of all the gtv files

        rs1 # image nrrd

        gtv

        #run radiomics
        print('running radiomics')
        import radiomics
        from radiomics import featureextractor
        import six
        import sys
        import pydicom
        import logging
        import SimpleITK as sitk
        import numpy as np
        import os,re,time,csv
        log_file = './Data/'+pid+'_log_file_1.txt'
        handler = logging.FileHandler(filename=log_file, mode='w')  # overwrites log_files from previous runs. Change mode to 'a' to append.
        formatter = logging.Formatter("%(levelname)s:%(name)s: %(message)s")  # format string for log messages
        handler.setFormatter(formatter)
        radiomics.logger.addHandler(handler)
        # Control the amount of logging stored by setting the level of the logger. N.B. if the level is higher than the
        # Verbositiy level, the logger level will also determine the amount of information printed to the output
        radiomics.logger.setLevel(logging.DEBUG)
        params=ok.fname1

        #extractor = featureextractor.RadiomicsFeaturesExtractor(params)# for pyradiomics version 2
        extractor = featureextractor.RadiomicsFeatureExtractor(params) # for pyradiomics version 3

        ij=rs1
        print(ij)
        #print(gtv[1])
        if str('GTV-1') in gtv[0]:
            ms=gtv[0]
        #elif str()
        elif len(gtv)>1: #to comment 
            ms=gtv[-1] #to comment 
        else:#to comment 
            ms= gtv[0]#to comment 
        #ms=gtv[0]
        print(ms)
        im = sitk.ReadImage(ij)
        ma = sitk.ReadImage(ms)
        lsif = sitk.LabelShapeStatisticsImageFilter()
        lsif.Execute(ma)
        labels = lsif.GetLabels()
        print(labels,'=====')
        print(im.GetDirection(),'<======= directions of image')
        print(ma.GetDirection(),'<======= directions of mask')
        print(im.GetOrigin(),'<======= origin of image')
        print(ma.GetOrigin(),'<======= origin of mask')
        #ma.SetDirection(im.GetDirection())# for solving label ROI larger than image 
        #ma.SetOrigin(im.GetOrigin())      # for solving label ROI larger than image 
        print(type(ma))
        print(type(im))
        result = extractor.execute(im, ma)
        result
        gtv
        out1=["patient_id",pid] # insert pat id
        for key, val in six.iteritems(result):
            #print("    %s    %s" %(key, val))
            out1.append(key)
            out1.append(val)

            ## the following line prints pairs    
            size=2
            x=[out1[i:i+size] for i  in range(0, len(out1), size)]
            #print(x)    
        print(s1,'%%%%%%%%%%%%%%')
        myFile= open(s1+'/TMH_'+pid+'_orginal_&_wavelet_bin_'+str(bin_var.get())+'_sigma_'+str(sigma_var1.get())+'_'+str(sigma_var2.get())+'_'+str(sigma_var3.get())+'_'+'pixel_'+str(pixel_var1.get())+'_'+str(pixel_var2.get())+'_'+str(pixel_var3.get())+'.csv', 'w',newline='') #insert pat id
        with myFile:
         writer = csv.writer(myFile)
         writer.writerows([x][0])
        print('writing to file')
        print('^^^^^^^^^^^^^^^^________________________$$$$$$$$$$$$$$$$$$^^^^^^^^^^^^^^^^^^^^')
    messagebox.showinfo(message="Radiomics computation Done !!!!!!")


from tkinter import ttk
import tkinter
from tkinter import messagebox
from PIL import ImageTk, Image
from tkinter import *
from tkinter import filedialog #@

top =Tk()
# setting the title
top.title('TMH radiomics extractor') 

#set window color
#top.configure(bg='#856ff8')
#top.configure(bg='white')
#top= tkinter.Toplevel()
#w=Tk()
# setting the area of the canvas
#top.geometry('500x500')
top.geometry('1000x1000')
#top.resizable(100, 100)
# setting the back ground color of the canvas
C=Canvas(top, bg="navajo white", height=500, width=500) 

# adding the text into the canvas
C.create_text(250,10,fill="black",font="Times 15 bold",text="Radiomics Extraction Module")

C.pack(fill="both",expand=True)


#from PIL import ImageTk, Image
#img = ImageTk.PhotoImage(Image.open("D:/radiomics_script/radiomics.jpg"))  
#img2 = ImageTk.PhotoImage(Image.open("D:/radiomics_script/tmh_logo.png"))  
#img2 = ImageTk.PhotoImage(Image.open("D:/Capture.PNG"))  
#imag = ImageTk.PhotoImage(img2.resize((200, 200), Image.ANTIALIAS))     #  this line is for resizing the image to fit canvas size
#l1=Label(image=img2)
#l1.pack()
# l=Label(image=img)
# l.pack()
# def helloCallBack():
#     #messagebox.showinfo( "Hello Python", "Hello World")
#     #messagebox.showwarning(title="wait",message="work hard")
#     tkinter.messagebox.askyesno(title=None, message=None)

# setting the button for input folder
c = tkinter.Button(top, text ="SELECT INPUT FOLDER", command = select1,bg='#DFCCAF')
#c.pack(side=LEFT, padx=10, pady=1)
c.place(x=10,y=60)
pathlabel = Label(top)
pathlabel.place(x=300,y=60)
in1=Label(top, text="input location :",)
in1.place (x = 200, y = 60)



# setting the button for output folder
d = tkinter.Button(top, text ="SELECT OUTPUT FOLDER", command = select,bg='#DFCCAF')
d.pack()
d.place(x=10,y=100)
pathlabel1 = Label(top)
pathlabel1.place(x=200,y=100)





B = tkinter.Button(top, text ="RADIOMIC EXTRACTION", command = runradio, bg='#DFCCAF')#,image=img)
#pathlabel = Label(top)
B.place(x=10,y=600)

# entry box values for binwidth
l1=Label(top, text="BIn Width")
l1.place (x = 30, y = 300)
bin_var=tkinter.DoubleVar()
entry1 = Entry(top,textvariable = bin_var)
print("@@",bin_var.get())
entry1.place(x = 150, y = 300)

def ok():
 print("Bin width = ",bin_var.get())
 import yaml,re
 # change the file to your original param file
 #fname = "D://radiomics_script//gb_param_test12.yaml"
 fname = "./gb_param_test12.yaml"
 stream = open(fname, 'r')
 data = yaml.load(stream)
 
 
# bv=re.sub(r'\\'','',bin_var.get())
 print(bin_var.get())
 data['imageType']['Original']['binWidth'] = bin_var.get()
 data['setting']['resampledPixelSpacing'][0] = pixel_var1.get()
 data['setting']['resampledPixelSpacing'][1] = pixel_var2.get()
 data['setting']['resampledPixelSpacing'][2] = pixel_var3.get()
 
 data['imageType']['LoG']['sigma'][0] = sigma_var1.get()
 data['imageType']['LoG']['sigma'][1]  = sigma_var2.get()
 data['imageType']['LoG']['sigma'][2]  = sigma_var3.get()
 #ok.fname1='D://radiomics_script//gb_param_test2.yaml'
 ok.fname1='./gb_param_test2.yaml'
 with open(ok.fname1, 'w') as yaml_file:
  yaml_file.write( yaml.dump(data))
 print("Sigma values = ",sigma_var1.get(),' ',sigma_var2.get(),' ',sigma_var3.get())
 print("Pixel resampling = ",pixel_var1.get(),' ',pixel_var2.get(),' ',pixel_var3.get())
 return ok.fname1
 
def rest():
    bin_var.set("25")
    sigma_var1.set("1")
    sigma_var2.set("2")
    sigma_var3.set("3")
    pixel_var1.set("2")
    pixel_var2.set("2")
    pixel_var3.set("2")
    

def bar():
    import time 
    progress['value'] = 20
    top.update_idletasks() 
    time.sleep(0.1) 

cust= tkinter.Button(top, text ="OK",command=ok, bg='#DFCCAF')
#d.pack()
cust.place(x=10,y=500)

cust= tkinter.Button(top, text ="Reset",command=rest, bg='#DFCCAF')
#d.pack()
cust.place(x=50,y=500)    




l2=Label(top, text="Image Type")
l2.place (x = 30, y = 350)
#entry1 = Entry(top)
#entry1.place(x = 150, y = 350)

l3=Label(top, text="Sigma Value")
l3.place (x = 30, y = 400)
# create variables to store the textbox values
sigma_var1=tkinter.IntVar() 
sigma_var2=tkinter.IntVar()
sigma_var3=tkinter.IntVar()
entry1 = Entry(top,textvariable = sigma_var1)
entry1.place(x = 150, y = 400)
entry2 = Entry(top,textvariable = sigma_var2)
entry2.place(x = 250, y = 400)
entry3 = Entry(top,textvariable = sigma_var3)
entry3.place(x = 350, y = 400)

l4=Label(top, text="Pixel Resampling")
l4.place (x = 30, y = 450)
pixel_var1=tkinter.IntVar() 
pixel_var2=tkinter.IntVar()
pixel_var3=tkinter.IntVar()
entry1 = Entry(top,textvariable = pixel_var1)
entry1.place(x = 150, y = 450)
entry2 = Entry(top,textvariable = pixel_var2)
entry2.place(x = 250, y = 450)
entry3 = Entry(top,textvariable = pixel_var3)
entry3.place(x = 350, y = 450)


rad1 = Radiobutton(top,text='Original', value=1)

rad1.place(x = 150, y = 350)

rad2 = Radiobutton(top,text='LoG', value=2)

rad2.place(x = 250, y = 350)

rad3 = Radiobutton(top,text='Wavelet', value=3)

rad3.place(x = 300, y = 350)

rad3 = Radiobutton(top,text='All', value=3)

rad3.place(x = 350, y = 350)




from tkinter import * 
from tkinter.ttk import *
# Progress bar widget 
progress = Progressbar(top, orient = HORIZONTAL, style='text.Horizontal.TProgressbar',
              length = 100, mode = 'determinate')
    

progress.place(x=200,y=600) 


selected = IntVar()

rad1 = Radiobutton(top,text='Original', value='Original', variable=selected)
rad2 = Radiobutton(top,text='LoG', value='LoG', variable=selected)
rad3 = Radiobutton(top,text='Wavelet', value='Wavelet', variable=selected)
rad4 = Radiobutton(top,text='All', value='All', variable=selected)

def clicked():

   print(selected.get())

btn = Button(top, text="Click Me", command=clicked)

#rad1.grid(column=0, row=0)

#rad2.grid(column=1, row=0)

#rad3.grid(column=2, row=0)

#btn.grid(column=3, row=0)





"""

class Frames(object):
    def newFrame(self):
        newwin = Toplevel(top)
        newwin.title('Customization')
        #newwin.Button(self, text ="CUSTOMIZATION", bg='#DFCCAF')
        #newwin.place(x=10,y=140)
        #newwin.geometry("200x200") 
        #newwin.resizable(0, 0)
        display = Label(newwin, text="Hello, " + self.query.get()) #getting parameter via query var
        display.pack()
#B.pack()
    def mainFrame(self,root):
            self.query = IntVar() #passing parameter via query var
            
            root.title('Open Window!!!')
            #root.geometry("200x200") 
            #root.resizable(0, 0)
            button1 =Button(root, text ="Open and Send New Window", command =self.newFrame)
            button1.place(x = 15, y = 25, width=170, height=25)
     
            entry1 = Entry(root, textvariable=self.query)
            entry1.place(x = 50, y = 75, width=100, height=25)
app = Frames()
app.mainFrame(top)

#top.mainloop()

"""
top.mainloop()


