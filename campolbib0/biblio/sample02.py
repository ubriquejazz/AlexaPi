#!/usr/bin/python
# -*- coding: latin-1 -*-
"""
	>> from biblio.sample02 import *
	>> main()
"""
import yaml
import sys, pdb 

from biblio.models import Book, Categories, Borrowing, LibraryUser

def u(v):
	return v.encode('utf-8') if isinstance(v, str) else v

def print_dict(row_dict):
	for key, value in row_dict.items():
		print( "%-15s: %s" % ( key, u(value) ))

def main():
	with open('../Katalog_2019_10_20.yaml', 'r') as file_desc:
		yaml_data = yaml.load (file_desc, Loader=yaml.Loader)

	for yaml_book in yaml_data:
					
		ISBN 		= yaml_book['ISBN']
		status 		= yaml_book['Available']
		location 	= yaml_book['Location']
		quantity 	= yaml_book['Amount']
		category 	= yaml_book['Category'] # To validate	

		title 		= u(yaml_book['Title'])
		author 		= u(yaml_book['Name']) + u(yaml_book['Surname'])
		description = u(yaml_book['Description'])
		notes 		= u(yaml_book['Anotations'])
		
		publisher_name = u(yaml_book['Publisher'])
		publisher_city = u(yaml_book['City'])
		year_published = yaml_book['Year']

		book = Book (  ISBN=ISBN, status=status, 
			location=location, quantity=quantity,
			# category=category,
			title=title, 
			author=author,
			description=description, notes=notes,
			publisher_name=publisher_name, 
			publisher_city= publisher_city,
			year_published=year_published)

		input("\nPlease confirm book %s" % ISBN)
		print_dict(yaml_book)
		#pdb.set_trace()
		#book.save()


if __name__ == "__main__":
	sys.exit(main())