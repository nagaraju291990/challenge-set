import os
import re
import json
import requests
import sys
import logger as log
from argparse import ArgumentParser

url = "https://ssmt.iiit.ac.in/onemt"

headers = {
	'Content-Type': 'application/json',
	'Accept': 'application/json'
}
logger = log.setup_logger('ssmt.log')

# Set the base directory path
base_directory = sys.argv[1]  # Replace with your actual directory path
target_language = sys.argv[2]
tlang = sys.argv[3]

logging = log.setup_logger('ssmt.log')

def call_mt(text, source_language, target_language):
	data = {'text': text, 'source_language':source_language, 'target_language':target_language}
	r = requests.post(url, headers=headers, json=data)
	output = json.loads(r.text)['data']
	return output

def process_file(input_file_path, file_name, root_path):
	# Open and read the file
	logger.info("Currently running:|%s|" %(input_file_path))
	print("Currently running %s" %(input_file_path))
	with open(input_file_path, 'r') as file:
		lines = file.read().split("\n")
	
	file_name_no_extension = file_name[: file_name.find('.')]
	out_file_name = file_name_no_extension + '_SSMT.txt'
	output_file_path = os.path.join(root_path, out_file_name)
	if os.path.exists(output_file_path):
		print(f"Output file already exists for {output_file_path}. Skipping...")
		logger.info(f"Output file already exists for {output_file_path}. Skipping...")
		return  # Skip processing and go to the next file
	# Do something with the file content
	# For example, we'll just convert it to uppercase (you can replace this with any other processing logic)
	out_array = []
	sentence_no = 1
	for line in lines:
		line = line.strip()
		if(line == ""):
			continue
		try:
			# arr = line.split("\t")
			# input_line = arr[1].strip()
			line = line.strip()
			out_line = call_mt(line, source_language, target_language)
			sentence_no = sentence_no + 1
			# seg_no = arr[0]
			# seg_no = re.sub(r'_Tel', r'_' + tlang, seg_no)
			# out_array.append(seg_no + "\t" + out_line)
			out_array.append(out_line)
			logger.info("Currently running:|%d|" %(sentence_no))
		except:
			continue
		# fp_out.write(arr[0] + "\t" + out_line + "\n")
	
	# Write the processed content to the output file
	with open(output_file_path, 'w') as output_file:
		output_file.write("\n".join(out_array))
	print(f"Processed and saved: {output_file_path}")
	logger.info("Processed and saved:|%s|" %(output_file_path))
		

def iterate_directory(directory, source_language, target_language):
	"""Iterate through the directory."""
	# Loop through all items in the directory
	print(directory)
	logger.info("Current Directory:|%s|" %(directory))
	root_path = os.path.abspath(directory)
	for item in os.listdir(directory):
		item_path = os.path.join(directory, item)
		
		# If it's a file, process it
		if os.path.isfile(item_path):
			process_file(item_path, item, root_path)
		
		# If it's a directory, call this function recursively
		elif os.path.isdir(item_path):
			iterate_directory(item_path, source_language, target_language)




if __name__ == '__main__':
	#  main()
	# Set the base directory path
	parser = ArgumentParser()
	parser.add_argument('--input', dest='inp', help='Enter the input folder path')
	# parser.add_argument('--output', dest='out', help='Enter the output folder path')
	parser.add_argument('--src', dest='src', help='eng|hin|tel|kan|tam|guj|mar|odi|pan|urd|kas|snd|doi|ban')
	parser.add_argument('--tgt', dest='tgt', help='eng|hin|tel|kan|tam|guj|mar|odi|pan|urd|kas|snd|doi|ban')
	args = parser.parse_args()
	print(args.inp)
	print(args.src, args.tgt)
	logger.info("input|%s|" %(args.inp))
	logger.info("src|tgt:|%s|%s|" %(args.src, args.tgt))
	base_directory = args.inp  # Replace with your actual directory path
	# output_directory = args.out
	source_language = args.src
	target_language = args.tgt
	iterate_directory(base_directory, source_language, target_language)

