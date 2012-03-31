import wikitools
import poster
import pyexiv2
import os
import shutil

#wiki_url = "MediaWiki API url here"

#wiki_url = 'http://localhost/mediawiki/api.php'
wiki_url =  'http://commons.wikimedia.org/w/api.php'

wiki_username = raw_input("Username:")
wiki_password = raw_input("Password:")

category = "English pronunciation"

try:
  wiki = wikitools.wiki.Wiki(wiki_url)
except:
	print "Can not connect with wiki. Check the URL"


try:
	wiki.login(username=wiki_username,password=wiki_password)

except:
	print "Invalid Username or Password"

path = './'

listing = os.listdir(path)

def filetype(file):
	return file.split(".")[-1]

def filename(file):
	return file.split(".")[-2]


def get_file_details(image):
	try:
		metadata = pyexiv2.ImageMetadata(image)
		metadata.read()
		file_name=metadata['Iptc.Application2.Headline'].raw_value[0].strip()
		caption=metadata['Iptc.Application2.Caption'].raw_value[0].strip()
		file_meta = {'name':file_name,'caption':caption}
		return file_meta
	except:
		print "No tag is set for the image " + image	
		exit	

	
def move_file(file):
	source = file
	destination = "./uploaded/"+file

	if os.path.isdir("uploaded"):
		shutil.move(source,destination)
	else:
		os.mkdir("uploaded")
		shutil.move(source,destination)		
	print "Moving the file " + file + " to the folder 'uploaded' "

def upload_file(file):
	

	file_name = filename(file)
	
	caption = "Audio pronunciation of the term '" + file_name + " 'in Indian English. "
		
	file_object=open(file,"r")
	picture=wikitools.wikifile.File(wiki=wiki, title=file_name)
       	picture.upload(fileobj=file_object,comment=caption, ignorewarnings=True)
	print "Uploaded the File " + file_name

	page_name = file_name.replace(" ","_")

	page_url = "File:" + page_name + filetype(file)

	page = wikitools.Page(wiki, page_url, followRedir=True)

#	wikidata = "=={{int:filedesc}}=={{Information|description={{en|1= " + caption + "}}{{TamilWiki Media Contest}}|source={{own}}|author=[[User:" + wiki_username + "|" + wiki_username + "]]}}=={{int:license-header}}=={{self|cc-by-sa-3.0}}[[Category:" + category + "]] [[Category:Uploaded with MediawikiUploader]]"


	wikidata = " {{Information |Description= " + caption + "|Source= Self |Author= [[User: " +  wiki_username + "|" + wiki_username + " ]] |Permission=Dual licensed per GFDL Version 1.2 or later / Creative Commons Attribution ShareAlike license versions 2.5, 2.0, and 1.0 as noted.}} == {{int:license}} == {{self|GFDL|Cc-by-sa-3.0-migrated|Cc-by-sa-2.5,2.0,1.0}} [[Category:English pronunciation|" +  file_name + "]] "


	page.edit(text=wikidata)

	move_file(file)
		
for photo in listing:
#	print photo
#`	print filetype(photo)
	if filetype(photo) in ['JPG','jpg','GIF','gif','png','PNG','ogg','OGG']:
		upload_file(photo)
				
sys.exit()
