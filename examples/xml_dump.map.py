import sys,os;sys.path.insert(0, os.path.abspath(os.getcwd()))
from mw import xml_dump

files = ["examples/dump.xml", "examples/dump2.xml"]

def page_info(dump, path):
	for page in dump:
		
		yield page.id, page.namespace, page.title
		

for page_id, page_namespace, page_title in xml_dump.map(files, page_info):
	print("\t".join([str(page_id), str(page_namespace), page_title]))

