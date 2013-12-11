import argparse

from mw import dump

def page_info(dump):
	for page in dump:
		yield page.id, page.namespace, page.title

parser = argparse.ArgumentParser(
	description = ("Prints the page_id, page_namespace and page_title of " + 
                   "every page in a set of XML database dump files as tab " + 
                   "separated values using one thread per CPU core.")
)
parser.add_argument(
	'files',
	help="The path to dump files to process",
	narg="+",
	type=dump.file # Checks that each path actually exists and has a valid file
	               # extension (.xml, .gz, .bz2, .7z or .lzma)
)
args = parser.parse_args()


for page_id, page_namespace, page_title in dump.map(args.files, page_info)
	print("\t".join(str(page_id), str(page_namespace), page_title))
