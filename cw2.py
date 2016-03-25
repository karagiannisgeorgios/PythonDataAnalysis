import collections
#import sys
import json      
import os.path
import operator
import re
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from user_agents import parse  #I am going to use it for the browser main name

#############################      GUI         #######################

class MyGui(tk.Frame):

	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		root.title("Karagiannis Georgios - Coursework 2")
		self.pack()
		self.widget()

	def widget(self):
		#the label at the start of the programm
		self.UpLabel = tk.Label(self)
		self.UpLabel["text"] = "Select question from bellow and do not forget to select file at the right"
		self.UpLabel.pack(side="top")
		#the menu with the question tasks
		self.question = ttk.Combobox(self, state="readonly", values=("Countries", "Continent", "Browser","BrowserName","AvidUsers","Also Like"))
		self.question.current(0)
		self.question.pack(side="top")
		#the label for the Document ID
		self.docLabel = tk.Label(self)
		self.docLabel["text"] = "Fill the document code (doc_id)"
		self.docLabel.pack(side="top")
		#the area for the Document ID
		self.docID = ttk.Entry(self, width=45)
		self.docID.insert(0,"100806162735-00000000115598650cb8b514246272b5")
		self.docID.pack(side="top")
		#the label for the User ID
		self.userLabel = tk.Label(self)
		self.userLabel["text"] = "Fill the user code (user_id)"
		self.userLabel.pack(side="top")
		#the area for the User ID
		self.userID = ttk.Entry(self, width=16)
		self.userID.insert(0,"4108dc09bfe11a0c")
		self.userID.pack(side="top")
		#the button for the file
		self.fileButton = tk.Button(self)
		self.fileButton["text"] = "Select file"
		self.fileButton["command"] = self.selectfile
		self.fileButton.pack(side="right")
		#the button to start running my app and to produce results
		self.OkButton = tk.Button(self)
		self.OkButton["text"] = "OK"
		self.OkButton["command"] = self.launch
		self.OkButton.pack(side="bottom")
		#the area with the results
		self.textArea = tk.Text(self)
		self.textArea.grid(sticky=(W, E, S))
		self.textArea.pack(side="bottom")
		self.textArea.insert(INSERT,"hello user! lets start..."+"\n\n")

	def launch(self):
		taskid = self.question.get() 
		docid = self.docID.get()
		userid = self.userID.get()
		try:
			launchProgramm(taskid, filename, userid, docid)
		except NameError as nameerror:
			printInTheArea ("You have to select a file first..."+"\n\n")

	#the methods which return the name and the path of the file I chose
	def selectfile(self):
		root.filename = filedialog.askopenfilename(initialdir = "$HOME",title = "Choose File",filetypes = (("json files","*.json"),("all files","*.*")))
		global filename
		filename = root.filename

	#the methods which prints at the text area
	def printInTheArea(self,result):
		self.textArea.insert(INSERT,"\n"+str(result))

###################################### GUI finish  ############################################


###################################### My basic methods  - Class ############################################

class MyMethods:
	
	# which country to which continet, I use this dictionary for the question 1-b
	cntry_to_cont = {
	  'AP' : 'AS',
	  'AF' : 'AS',
	  'AX' : 'EU',
	  'AL' : 'EU',
	  'DZ' : 'AF',
	  'AS' : 'OC',
	  'AD' : 'EU',
	  'AO' : 'AF',
	  'AI' : 'NA',
	  'AQ' : 'AN',
	  'AG' : 'NA',
	  'AR' : 'SA',
	  'AM' : 'AS',
	  'AW' : 'NA',
	  'AU' : 'OC',
	  'AT' : 'EU',
	  'AZ' : 'AS',
	  'BS' : 'NA',
	  'BH' : 'AS',
	  'BD' : 'AS',
	  'BB' : 'NA',
	  'BY' : 'EU',
	  'BE' : 'EU',
	  'BZ' : 'NA',
	  'BJ' : 'AF',
	  'BM' : 'NA',
	  'BT' : 'AS',
	  'BO' : 'SA',
	  'BQ' : 'NA',
	  'BA' : 'EU',
	  'BW' : 'AF',
	  'BV' : 'AN',
	  'BR' : 'SA',
	  'IO' : 'AS',
	  'VG' : 'NA',
	  'BN' : 'AS',
	  'BG' : 'EU',
	  'BF' : 'AF',
	  'BI' : 'AF',
	  'KH' : 'AS',
	  'CM' : 'AF',
	  'CA' : 'NA',
	  'CV' : 'AF',
	  'KY' : 'NA',
	  'CF' : 'AF',
	  'TD' : 'AF',
	  'CL' : 'SA',
	  'CN' : 'AS',
	  'CX' : 'AS',
	  'CC' : 'AS',
	  'CO' : 'SA',
	  'KM' : 'AF',
	  'CD' : 'AF',
	  'CG' : 'AF',
	  'CK' : 'OC',
	  'CR' : 'NA',
	  'CI' : 'AF',
	  'HR' : 'EU',
	  'CU' : 'NA',
	  'CW' : 'NA',
	  'CY' : 'AS',
	  'CZ' : 'EU',
	  'DK' : 'EU',
	  'DJ' : 'AF',
	  'DM' : 'NA',
	  'DO' : 'NA',
	  'EC' : 'SA',
	  'EG' : 'AF',
	  'SV' : 'NA',
	  'GQ' : 'AF',
	  'ER' : 'AF',
	  'EE' : 'EU',
	  'ET' : 'AF',
	  'FO' : 'EU',
	  'FK' : 'SA',
	  'FJ' : 'OC',
	  'FI' : 'EU',
	  'FR' : 'EU',
	  'GF' : 'SA',
	  'PF' : 'OC',
	  'TF' : 'AN',
	  'GA' : 'AF',
	  'GM' : 'AF',
	  'GE' : 'AS',
	  'DE' : 'EU',
	  'GH' : 'AF',
	  'GI' : 'EU',
	  'GR' : 'EU',
	  'GL' : 'NA',
	  'GD' : 'NA',
	  'GP' : 'NA',
	  'GU' : 'OC',
	  'GT' : 'NA',
	  'GG' : 'EU',
	  'GN' : 'AF',
	  'GW' : 'AF',
	  'GY' : 'SA',
	  'HT' : 'NA',
	  'HM' : 'AN',
	  'VA' : 'EU',
	  'HN' : 'NA',
	  'HK' : 'AS',
	  'HU' : 'EU',
	  'IS' : 'EU',
	  'IN' : 'AS',
	  'ID' : 'AS',
	  'IR' : 'AS',
	  'IQ' : 'AS',
	  'IE' : 'EU',
	  'IM' : 'EU',
	  'IL' : 'AS',
	  'IT' : 'EU',
	  'JM' : 'NA',
	  'JP' : 'AS',
	  'JE' : 'EU',
	  'JO' : 'AS',
	  'KZ' : 'AS',
	  'KE' : 'AF',
	  'KI' : 'OC',
	  'KP' : 'AS',
	  'KR' : 'AS',
	  'KW' : 'AS',
	  'KG' : 'AS',
	  'LA' : 'AS',
	  'LV' : 'EU',
	  'LB' : 'AS',
	  'LS' : 'AF',
	  'LR' : 'AF',
	  'LY' : 'AF',
	  'LI' : 'EU',
	  'LT' : 'EU',
	  'LU' : 'EU',
	  'MO' : 'AS',
	  'MK' : 'EU',
	  'MG' : 'AF',
	  'MW' : 'AF',
	  'MY' : 'AS',
	  'MV' : 'AS',
	  'ML' : 'AF',
	  'MT' : 'EU',
	  'MH' : 'OC',
	  'MQ' : 'NA',
	  'MR' : 'AF',
	  'MU' : 'AF',
	  'YT' : 'AF',
	  'MX' : 'NA',
	  'FM' : 'OC',
	  'MD' : 'EU',
	  'MC' : 'EU',
	  'MN' : 'AS',
	  'ME' : 'EU',
	  'MS' : 'NA',
	  'MA' : 'AF',
	  'MZ' : 'AF',
	  'MM' : 'AS',
	  'NA' : 'AF',
	  'NR' : 'OC',
	  'NP' : 'AS',
	  'NL' : 'EU',
	  'NC' : 'OC',
	  'NZ' : 'OC',
	  'NI' : 'NA',
	  'NE' : 'AF',
	  'NG' : 'AF',
	  'NU' : 'OC',
	  'NF' : 'OC',
	  'MP' : 'OC',
	  'NO' : 'EU',
	  'OM' : 'AS',
	  'PK' : 'AS',
	  'PW' : 'OC',
	  'PS' : 'AS',
	  'PA' : 'NA',
	  'PG' : 'OC',
	  'PY' : 'SA',
	  'PE' : 'SA',
	  'PH' : 'AS',
	  'PN' : 'OC',
	  'PL' : 'EU',
	  'PT' : 'EU',
	  'PR' : 'NA',
	  'QA' : 'AS',
	  'RE' : 'AF',
	  'RO' : 'EU',
	  'RU' : 'EU',
	  'RW' : 'AF',
	  'BL' : 'NA',
	  'SH' : 'AF',
	  'KN' : 'NA',
	  'LC' : 'NA',
	  'MF' : 'NA',
	  'PM' : 'NA',
	  'VC' : 'NA',
	  'WS' : 'OC',
	  'SM' : 'EU',
	  'ST' : 'AF',
	  'SA' : 'AS',
	  'SN' : 'AF',
	  'RS' : 'EU',
	  'SC' : 'AF',
	  'SL' : 'AF',
	  'SG' : 'AS',
	  'SX' : 'NA',
	  'SK' : 'EU',
	  'SI' : 'EU',
	  'SB' : 'OC',
	  'SO' : 'AF',
	  'ZA' : 'AF',
	  'GS' : 'AN',
	  'SS' : 'AF',
	  'ES' : 'EU',
	  'LK' : 'AS',
	  'SD' : 'AF',
	  'SR' : 'SA',
	  'SJ' : 'EU',
	  'SZ' : 'AF',
	  'SE' : 'EU',
	  'CH' : 'EU',
	  'SY' : 'AS',
	  'TW' : 'AS',
	  'TJ' : 'AS',
	  'TZ' : 'AF',
	  'TH' : 'AS',
	  'TL' : 'AS',
	  'TG' : 'AF',
	  'TK' : 'OC',
	  'TO' : 'OC',
	  'TT' : 'NA',
	  'TN' : 'AF',
	  'TR' : 'AS',
	  'TM' : 'AS',
	  'TC' : 'NA',
	  'TV' : 'OC',
	  'UG' : 'AF',
	  'UA' : 'EU',
	  'AE' : 'AS',
	  'GB' : 'EU',
	  'US' : 'NA',
	  'UM' : 'OC',
	  'VI' : 'NA',
	  'UY' : 'SA',
	  'UZ' : 'AS',
	  'VU' : 'OC',
	  'VE' : 'SA',
	  'VN' : 'AS',
	  'WF' : 'OC',
	  'EH' : 'AF',
	  'YE' : 'AS',
	  'ZM' : 'AF',
	  'ZW' : 'AF',
	  'ZZ' : 'Unknown',
	  'EU' : 'Unknown'
	}
					
	
	def countries(self, filename,docid):
		""" this method prints the countries of the visitors of one document  """
		countries = []
		ReaderByCountries = {}
		try:
			with open(filename) as json_file:
				for line in json_file:
					if (re.search('"subject_doc_id":"'+docid+'"', line)):
						parsed = json.loads(line)
						country = parsed['visitor_country']
						#i store each element, each country in a list
						countries.append(country)
			#I create a dictionary which has as key the name of the country and as value how many times each country is
			ReaderByCountries= collections.Counter(countries)
			for a in ReaderByCountries:
				print(a," ---> ",ReaderByCountries[a])	
			#Countries histogram
			n = len(ReaderByCountries)
			if n==0:
				printInTheArea ("Xmm.. seems there no histogram.. please check your inputs..")
			else:
				plt.barh(range(n), list(ReaderByCountries.values()), align='center', alpha=0.4)
				plt.yticks(range(n), list(ReaderByCountries.keys())) 
				plt.xlabel('counts')
				plt.title('Number of countries represented')
				plt.show()
		except:
			printInTheArea("Chose file")


	def continent(self, filename,docid):
		""" this method illustrates the continent of the visitors of one document  """
		countries = []
		ReaderByCountries = {}
		totalCountries = {}
		try:
			with open(filename) as json_file:
				for line in json_file:
					if (re.search('"subject_doc_id":"'+docid+'"', line)):
						parsed = json.loads(line)
						country = parsed['visitor_country']
						#i store each element, each country in a list
						countries.append(country)
			#I create a dictionary which has as key the name of the country and as value how many times each country is
			ReaderByCountries= collections.Counter(countries)

			# associate my countries in my previous dectionary with the continents using a fixed dictionary
			for country in ReaderByCountries:
				try:
					totalCountries[self.cntry_to_cont[country]] += ReaderByCountries[country]
				except KeyError as ke:
					totalCountries[self.cntry_to_cont[country]] = ReaderByCountries[country]
			for a in totalCountries:
				print(a," ---> ",totalCountries[a])
			#Countries histogram
			n = len(totalCountries)
			if n==0:
				printInTheArea ("Xmm.. seems there no histogram.. please check your inputs..")
			else:
				plt.barh(range(n), list(totalCountries.values()), align='center', alpha=0.4)
				plt.yticks(range(n), list(totalCountries.keys())) 
				plt.xlabel('counts')
				plt.title('Number of continent represented')
				plt.show()
		except:
			printInTheArea("Chose file")

	# for the question 3-a ----  works fine!
	def browsers(self,filename):
		"""this method finds and illustrates the list of the browsers"""
		browserslist = []
		browsers = {}
		try:
			with open(filename) as json_file:
				for line in json_file:
					try:
	# I used the user_agent library to identify the browser name, that library IS NOT installed at the LAB
	#it is easy to do that without that library but I chose to use it
						parsed = json.loads(line)
						temp=parsed["visitor_useragent"]
						user_agent = parse(temp)
						browserslist.append(user_agent.browser)   
						pass
					except KeyError as ke:
						pass
	#I made a list with the browsers and using the Counter I have a dictonary for the histogram
			browsers= collections.Counter(browserslist)
			for a in browsers:
				print(a," ---> ",browsers[a])
			n = len(browsers)
			if n==0:
				printInTheArea ("Xmm.. seems there no histogram.. please check your inputs..")
			else:
				plt.barh(range(n), list(browsers.values()), align='center', alpha=0.4)
				plt.yticks(range(n), list(browsers.keys())) 
				plt.xlabel('counts')
				plt.title('browsers')
				plt.show()
		except:
			printInTheArea("Chose file")

	def browsersName(self,filename):
		""" this method illustrates only the main name of the browser using the user_agent library  """
		browserslist = []
		browsers = {}
		try:
			with open(filename) as json_file:
				for line in json_file:
					try:
						parsed = json.loads(line)
						temp=parsed["visitor_useragent"]
						user_agent = parse(temp)
						browserslist.append(user_agent.browser.family)
						# I did not split the string, i used the user_agent library - DOES NOT WORKS AT THE LAB    
						#ua_string=temp.split('/').pop(0) --- with this I keep only the first word of the browsers 
						pass
					except KeyError as ke:
						pass
		
			browsers= collections.Counter(browserslist)
			for a in browsers:
				print(a," ---> ",browsers[a])
			# using form the collection the Counter I build a dictionary to illustrate at the histogram
			n = len(browsers)
			if n==0:
				printInTheArea ("Xmm.. seems there no histogram.. please check your inputs..")
			else:
				plt.barh(range(n), list(browsers.values()), align='center', alpha=0.4)
				plt.yticks(range(n), list(browsers.keys())) 
				plt.xlabel('counts')
				plt.title('browsers Name')
				plt.show()
		except:
			printInTheArea("Chose file")


	def avidUsers(self,filename):
		""" this method counts the top10 avid users """
# I use a dictionary in which as key are the userID and as as value each time I add (1) when I find the user
		users = {}
		try:
			with open(filename) as json_file:
				for line in json_file:
					parsed = json.loads(line)
					if 'visitor_uuid' in parsed:
						user = parsed['visitor_uuid']
						if 'event_readtime' in parsed:
							readtime = parsed['event_readtime']
							if user in users:
								users[user] += readtime
							else:
								users[user] = readtime;
			print("\n"+"The most avid readers are:"+"\n")
			# I sort the dictionary and I keep the first 10 of the users		
			top10 = sorted(users, key=users.get, reverse=True)[:10]
			for a in top10:
				print(a," ---> ",users[a])
			return users
		except:
			 printInTheArea("Chose file")

###################################### My basic methods  - Class  ---  finish    ############################################



#-----------------------------------------------question 5--------------------------------------------#

# read all the JSON file and increases the functionality of the project
def readfile(filename):
    data = []
    with open(filename) as json_file:
        for line in json_file:
            data.append(line)
            if line.find('}') >= 0:
                doc = json.loads(''.join(data))
                yield doc
                data = []

# 5 - a
def readersOfdocument(docid):
    """returns all visitor UUIDs of readers of that document uuid."""
    count = {}
    for obj in readfile(filename):
        try:
                c = obj['visitor_uuid']
                if (obj['subject_doc_id'] == docid) & (obj['event_type'] == 'read'):
                    count[c] = 1
                elif c in count:
                    count[c] += 1
        except:
            continue
    return count

# 5 - b
def documentsReaded(userid):
    """returns all visitor UUIDs of readers of that document uuid."""
    count = []
    for obj in readfile(filename):
        try:
                c = obj['subject_doc_id']
                if (obj['visitor_uuid'] == userid) & (c not in count):
                    count.append(c)
        except:
            continue
    return count

#5 - c - d - e
def alsoLike(userid, docid):
    """is the method for the question 5"""
    listofVisitors = []
    listofdocsvisited = []
    listofVisitors = readersOfdocument(docid)

    forPrint = ("Visitors --> "+str(listofVisitors)+"\n\n")
    printInTheArea (forPrint)
    
    if not listofVisitors:
        forPrint = str(("Only the user: ", userid, "read the document: ", docid))
        printInTheArea(forPrint)
        return

    for k in listofVisitors:
        c = documentsReaded(k)
        listofdocsvisited.append(c)

    # removing all elements which matches documents ID from listofdocsvisited
    temp = []
    for iter in listofdocsvisited:
        for it in iter:
            if docid in it:
                iter.remove(docid)
            else: 
                temp.append(iter)

    vistors_who_readother_docs = {}

#5d

    for k in temp[0]:
        count = 0
        c = readersOfdocument(k)

        for m, n in c.items():
            count += n
        vistors_who_readother_docs[k] = count

    top10 = sorted(vistors_who_readother_docs.items(), key=operator.itemgetter(1))[-11:]
    
    printInTheArea("\n\n"+"--------------Top Documents by count of readers ----------"+"\n\n")
    printInTheArea("Document ID	                             Number of Readers"+"\n\n")
    for k in reversed(top10):
        string = str((k[0], "-->", k[1]))
        printInTheArea (string)
    

    printInTheArea("\n\n"+"------Top Documents by page read time of readers ---------"+"\n\n")
    printInTheArea("Document ID	                                Total Reading time"+"\n\n")
    for k in reversed(avidUsers2(temp[0])):
        string = str((k[0], "-->", k[1]))
        printInTheArea (string)



def avidUsers2(docid=0):
    """ggrgeregf"""
    users = {}
    for obj in readfile(filename):
        try:
            if obj['event_type'] == "pagereadtime":
                userid = obj['visitor_uuid']
                time = obj['event_readtime']
                document_id = obj['subject_doc_id']
                # get all readers according to their pagereadtime
                if docid == 0:
                    if userid in users.keys():
                        users[userid] = time + users[userid]
                    else:
                        users[userid] = time
                # get total pagereadtime for a  document
                elif document_id in docid:
                    if (document_id in users.keys()):
                        users[document_id] = time + users[document_id]
                    else:
                        users[document_id] = time
        except:
            continue
    top10 = sorted(users.items(), key=operator.itemgetter(1))[-11:]
    return top10  # return largest 10 values, if you prefer (for testing)




##############################################


#----------------------------MAIN----------------------------------#

def launchProgramm(taskid, filename, userid, docid):
	""" I use this method in order to call each time the specific method based on the user choise  """
	method = MyMethods()

	if taskid == 'Countries':
		method.countries(filename,docid)		

	if taskid == 'Continent':
		method.continent(filename,docid)

	if taskid == 'Browser':
		method.browsers(filename)

	if taskid == 'BrowserName':
		method.browsersName(filename)
	
	if taskid == 'AvidUsers':
		users = method.avidUsers(filename)
		printInTheArea("\n""The most avid users are:"+"\n")
		top10 = sorted(users, key=users.get, reverse=True)[:10]
		# I print the users at the text area of the gui
		for a in top10:
			printInTheArea("The user: " +a+ " spend -> " + str(users[a]))
	
	if taskid == 'Also Like':
		also_likes = alsoLike(userid, docid)


# It is for the GUI
root = tk.Tk()
app = MyGui(master=root)
printInTheArea = app.printInTheArea
app.mainloop()

# I start my application using as inputs the GUI's inputs -
try:
	launchProgramm(taskid, filename, userid, docid)
except NameError as nameerror:
	print ("\n\n\n\n"+"              bye bye user! CU again"+"\n\n\n\n")  




