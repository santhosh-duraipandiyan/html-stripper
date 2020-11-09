# 
# web scraping tool created by using python
# 
# created by odd introvert
# 

#importing nessesary modules

import pycurl

import time

import warnings

from shutil import copyfile

from io import BytesIO

from html.parser import HTMLParser

metacount = 0

class MyHTMLParser(HTMLParser):

	# getting all comments
	def handle_comment(self, data):

		pos = self.getpos()

		# print("\t At line : ", pos[0], "position ", pos[1])

		f = open("comments_temp.txt", "a") 

		f.write("\n\n At line :\t\t" + str(pos[0]) + "\n\n position :\t\t" + str(pos[1]) + "\n\n comment :\t\t" + data + "\n\n")

		f.close()


	# getting all starting tags
	def handle_starttag(self, tag, attrs):

		global metacount

		pos = self.getpos()

		if (tag == "meta"):

			metacount += 1

			f = open("meta_temp.txt", "a") 

			f.write("\n\n At line :\t\t" + str(pos[0]) + "\n\n position :\t\t" + str(pos[1]) + "\n\n tag :\t\t" + str(attrs) + "\n\n")

			f.close()

		if (tag == "link" or tag == "a"):
			
			f = open("links_temp.txt", "a") 

			f.write("\n\n At line :\t\t" + str(pos[0]) + "\n\n position :\t\t" + str(pos[1]) + "\n\n tag :\t\t" + str(attrs) + "\n\n")

			f.close()


	def handle_data(self, data):

		pos = self.getpos()
		
		if data.isspace():

			return

		if self.lasttag == "script" and data.strip():

			f = open("scripts_temp.txt", "a") 

			f.write("\n\n At line :\t\t" + str(pos[0]) + "\n\n position :\t\t" + str(pos[1]) + "\n\n data :\t\t" + data + "\n\n")

			f.close()

		f = open("data_temp.txt", "a") 

		f.write("\n\n At line :\t\t" + str(pos[0]) + "\n\n position :\t\t" + str(pos[1]) + "\n\n data :\t\t" + data + "\n\n")

		f.close()

def copying():

	print("75% Copying files to /data...\n")

	time.sleep(1)

	copyfile('comments_temp.txt', 'data/comments.txt') 

	copyfile('data_temp.txt', 'data/data.txt')

	copyfile('meta_temp.txt', 'data/meta.txt')

	copyfile('links_temp.txt', 'data/links.txt')

	copyfile('scripts_temp.txt', 'data/scripts.txt')

def deleting():

	print("90% Deleting the temproary files...\n")

	time.sleep(1)

	f = open('comments_temp.txt', 'r+')

	f.truncate(0)

	f.close()

	f = open('data_temp.txt', 'r+')

	f.truncate(0)

	f.close()

	f = open('meta_temp.txt', 'r+')

	f.truncate(0)

	f.close()

	f = open('links_temp.txt', 'r+')

	f.truncate(0)

	f.close()

	f = open('scripts_temp.txt', 'r+')

	f.truncate(0)

	f.close()


def main():

	warnings.simplefilter("ignore", category=DeprecationWarning)

	parser = MyHTMLParser()
	
	b_obj = BytesIO() 

	crl = pycurl.Curl() 

	url = input("\nEnter the url: ")

	# Set URL value
	crl.setopt(crl.URL, url)

	# Write bytes that are utf-8 encoded
	crl.setopt(crl.WRITEDATA, b_obj)

	# Perform a file transfer 
	crl.perform() 

	# End curl session
	crl.close()

	# Get the content stored in the BytesIO object (in byte characters) 
	data = b_obj.getvalue()

	print("\n25% Getting data from url...\n")

	time.sleep(1)

	f = open("content.html", "w+") 

	f.write(data.decode("utf-8"))

	f.close()

	f = open("content.html")

	if f.mode == 'r':

		contents = f.read()

		print("50% Prasing the data from url...\n")

		time.sleep(1)

		parser.feed(contents)

		# print("metatags found: ", metacount)

	copying()

	deleting()

	print("100% Completed...")

main()