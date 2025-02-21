"""Run Bing Translator API using API keys."""
from argparse import ArgumentParser
import requests, uuid, json
from json import dump
from collections import OrderedDict
import os
from re import search
import logger as log

logger = log.setup_logger('bing.log')


three_lettered_to_two_lettered_dict = {'ban': 'bn', 'eng': 'en', 'hin': 'hi', 'doi': 'doi', 'guj': 'gu', 'kas': 'ks', 'mar': 'mr', 'odi': 'or', 'snd': 'sd', 'tam': 'ta', 'tel': 'te', 'urd': 'ur', 'pan': 'pa', 'kan': 'kn'}
# Add your key and endpoint
# Click here to view endpoints
key = "a87438c2baa64a1ebe2d857e95206811"
# 2nd key
# key = "cd119dde7e074cf187850f99c9ae6314"
endpoint = "https://api.cognitive.microsofttranslator.com"
# endpoint = "https://il-ilmt-iiith.cognitiveservices.azure.com"

# location, also known as region.
# required if you're using a multi-service or regional (not global) resource. It can be found in the Azure portal on the Keys and Endpoint page.
location = "centralindia"

path = '/translate'
constructed_url = endpoint + path

headers = {
	'Ocp-Apim-Subscription-Key': key,
	# location required if you're using a multi-service or regional (not global) resource.
	'Ocp-Apim-Subscription-Region': location,
	'Content-type': 'application/json',
	'X-ClientTraceId': str(uuid.uuid4())
}


def read_lines_from_file(file_path):
	"""Read lines from file."""
	with open(file_path, 'r', encoding='utf-8') as file_read:
		return [line.strip() for line in file_read.readlines() if line.strip()]

def write_to_file(data_object, output_file_path):
	"""Dump an object into a json file."""
	with open(output_file_path, 'w', encoding='utf-8') as file_dump:
		file_dump.write('\n'.join(data_object))
		  
def process_file1(input_file_path):
	"""Pass arguments and call functions here."""
	# You can pass more than one object in body.
	parser = ArgumentParser()
	parser.add_argument('--input', dest='inp', help='Enter the input folder path')
	parser.add_argument('--output', dest='out', help='Enter the output folder path')
	parser.add_argument('--src', dest='src', help='eng|hin|tel|kan|tam|guj|mar|odi|pan|urd|kas|snd|doi|ban')
	parser.add_argument('--tgt', dest='tgt', help='eng|hin|tel|kan|tam|guj|mar|odi|pan|urd|kas|snd|doi|ban')
	args = parser.parse_args()
	print(args.inp, args.out)
	print(args.src, args.tgt)
	logger.info("input|output:|%s|%s|" %(args.inp, args.out))
	logger.info("src|tgt:|%s|%s|" %(args.src, args.tgt))
	if not os.path.isdir(args.out):
		os.makedirs(args.out)
	root_path = os.path.abspath(args.inp)
	print(os.listdir(root_path))
	logger.info("root_path:|%s|" %(root_path))
	for folder_name in os.listdir(root_path):
		folder_path = os.path.join(root_path, folder_name)
		# print(folder_name)
		# print(folder_path)
		if os.path.isdir(folder_path):
			print(folder_name)
			logger.info("Currently running folder:|%s|" %(folder_name))
			# source_three_lettered, target_three_lettered = search('^(eng)\-(.*?)$', folder_name).groups()
			source = three_lettered_to_two_lettered_dict[args.src]
			target = three_lettered_to_two_lettered_dict[args.tgt]
			params = {'api-version': '3.0', 'from': source, 'to': target}
			# print(source, target)
			logger.info("source|target:|%s|%s|" %(source, target))
			output_folder_path = os.path.join(args.out, folder_name)
			if not os.path.isdir(output_folder_path):
				os.makedirs(output_folder_path)
			for file_name in os.listdir(folder_path):
				file_path = os.path.join(folder_path, file_name)
				print(file_name)
				logger.info("Currently running file:|%s|" %(file_name))
				lines = read_lines_from_file(file_path)
				responses = []
				for line in lines:
					body = [{'text': line}]
					request = requests.post(constructed_url, params=params, headers=headers, json=body)
					response = request.json()
					# print(response)
					mt_output = response[0]["translations"][0]["text"]
					# print(mt_output)
					responses.append(mt_output)
				print('Done for all lines')
				logger.info("Done for all lines %s", file_name)
				file_name_no_extension = file_name[: file_name.find('.')]
				out_file_name = file_name_no_extension + '_MS_Bing.txt'
				output_file_path = os.path.join(output_folder_path, out_file_name)
				write_to_file(responses, output_file_path)

def process_file(input_file_path, file_name, root_path):
	"""Process the file."""
	print(input_file_path)
	logger.info("Currently running file:|%s|" %(file_name))
	lines = read_lines_from_file(input_file_path)
	responses = []

	file_name_no_extension = file_name[: file_name.find('.')]
	out_file_name = file_name_no_extension + '_MS_Bing.txt'
	output_file_path = os.path.join(root_path, out_file_name)
	if os.path.exists(output_file_path):
			print(f"Output file already exists for {output_file_path}. Skipping...")
			logger.info(f"Output file already exists for {output_file_path}. Skipping...")
			return  # Skip processing and go to the next file

	for line in lines:
		body = [{'text': line}]
		request = requests.post(constructed_url, params=params, headers=headers, json=body)
		response = request.json()
		# print(response)
		mt_output = response[0]["translations"][0]["text"]
		# print(mt_output)
		responses.append(mt_output)
	print('Done for all lines')
	logger.info("Done for all lines %s", file_name)	
	logger.info("Writing to file %s", output_file_path)	
	write_to_file(responses, output_file_path)
												
def iterate_directory(directory, source_language, target_language):
	"""Iterate through the directory."""
	# Loop through all items in the directory
	print(directory)
	root_path = os.path.abspath(directory)

	logger.info("Current Directory:|%s|" %(directory))
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
	source = three_lettered_to_two_lettered_dict[args.src]
	target = three_lettered_to_two_lettered_dict[args.tgt]
	params = {'api-version': '3.0', 'from': source, 'to': target}
	iterate_directory(base_directory, source_language, target_language)
