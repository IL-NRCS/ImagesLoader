###############################################
## A Simmons-Steffen                         ##
##                                           ##
##                                           ##
## USDA-NRCS                                 ##
## Date created: Oct 10, 2022                ##
## Date modified:                            ##
###############################################


## This script creates a csv file template
## for creating metadata.

import os
from os.path import isfile, isdir
from os import listdir
import arcpy
# import a groupby() method
#metadata lib
from arcpy import metadata as md

import sys
import csv

from datetime import datetime


liste_fichiers=[]

image_folder = arcpy.GetParameterAsText(0)
# Set local variables
out_folder_path = arcpy.GetParameterAsText(1)




def listerFichier(path):

            listefichiers = listdir(path)

            if listefichiers != None:

                for f in listefichiers :
                    if(isfile(path+"/"+f)):
                        liste_fichiers.append(path+"/"+f)
                    elif(isdir(path+"/"+f)):
                        temp = listerFichier(path+"/"+f)

            return liste_fichiers


def replace_txt(stringg):

    stringg=stringg.replace('<DIV STYLE="text-align:Left;"><DIV><P><SPAN>','').replace('<DIV STYLE="text-align:Left;"><DIV><DIV><P><SPAN>','').replace('</SPAN></P></DIV></DIV>','').replace('</DIV>','')
    return stringg
    
def returnImages(path):

        liste_fichiers.clear()
        liste_images=[]

        #head of log file
        head=['index','source file location','title','tags','summary','description','credits','Use limitations']
        liste_images.append(head)
        
        files_list = listerFichier(path)
        listFormats=['jpg','tif','png','jp2','img','bmp','gif','crf','bip']
        index=1
        
        for f in files_list:
            
            if f[-3:] in listFormats or  f[-4:] in listFormats or  f[-6:] in listFormats:

                try :
                    
                        arcpy.AddMessage(f)
                        
                        raster = arcpy.Raster(f)
                        item_md = md.Metadata(raster)

                        title=item_md.title
                        tags=item_md.tags
                        summary=item_md.summary
                        description=item_md.description
                        credits_=item_md.credits
                        accessConstraints=item_md.accessConstraints
                        
                        if str(title)=='None' or str(tags)=='None' or str(summary)=='None' or str(description)=='None' or str(credits_)=='None' or str(accessConstraints)=='None' or str(title)=='' or str(tags)=='' or str(summary)=='' or str(description)=='' or str(credits_)=='' or str(accessConstraints)=='':
                             
                            arcpy.AddMessage(str(liste_images))
                            tg=''
                            smmry=''
                            desc=''
                            crdts=''
                            accConst=''
                            ttle=''
                            
                            if str(title)!='None': 
                                ttle=replace_txt(str(title))
                                
                            if str(tags)!='None': 
                                tg=replace_txt(str(tags))
                                
                            if str(summary)!='None' :
                                smmry=replace_txt(str(summary))
                                
                            if str(description)!='None' :      
                                desc=replace_txt(str(description))
                                
                            if str(credits_)!='None':
                                crdts=replace_txt(str(credits_))
                                
                            if str(accessConstraints)!='None':
                                 accConst=replace_txt(str(accessConstraints))
                                
                            liste_images.append([index,f,ttle,tg,smmry,desc,crdts,accConst])
                            index=index+1
                    
                        
                except Exception:

                    e = sys.exc_info()[1]
                    arcpy.AddError(e.args[0])
                    continue

        return liste_images


liste_images=returnImages(image_folder)
 
# datetime object containing current date and time
now = datetime.now()
dt_string = now.strftime("%d%m%Y_%Hh%Mmin%S")

with open(out_folder_path+"/NoMetadataImages_"+dt_string+".csv","w", newline="") as f:
    writer = csv.writer(f,delimiter = ";")
    writer.writerows(liste_images)    
