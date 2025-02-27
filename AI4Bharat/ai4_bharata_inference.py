import torch
from transformers import (
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
)
from IndicTransToolkit import IndicProcessor
from re import search
import logger as log
from argparse import ArgumentParser
import os
lang_code_mapping = {
    'asm': 'asm_Beng',
    'ben': 'ben_Beng',
    'brx': 'brx_Deva',
    'doi': 'doi_Deva',
    'eng': 'eng_Latn',
    'gom': 'gom_Deva',
    'guj': 'guj_Gujr',
    'hin': 'hin_Deva',
    'kan': 'kan_Knda',
    'kas': 'kas_Arab',  # Kashmiri has two scripts; choose accordingly
    'kas_deva': 'kas_Deva',
    'mai': 'mai_Deva',
    'mal': 'mal_Mlym',
    'mar': 'mar_Deva',
    'mni': 'mni_Beng',  # Manipuri has two scripts; choose accordingly
    'mni_mtei': 'mni_Mtei',
    'npi': 'npi_Deva',
    'ory': 'ory_Orya',
    'pan': 'pan_Guru',
    'san': 'san_Deva',
    'sat': 'sat_Olck',
    'snd': 'snd_Arab',  # Sindhi has two scripts; choose accordingly
    'snd_deva': 'snd_Deva',
    'tam': 'tam_Taml',
    'tel': 'tel_Telu',
    'urd': 'urd_Arab'
}

logger = log.setup_logger('ai4bharat.log')

# model_name = "ai4bharat/indictrans2-indic-en-1B"
model_name = "ai4bharat/indictrans2-indic-indic-1B"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name, trust_remote_code=True)
ip = IndicProcessor(inference=True)


def read_lines_from_file(file_path):
	"""Read lines from file."""
	with open(file_path, 'r', encoding='utf-8') as file_read:
		return [line.strip() for line in file_read.readlines() if line.strip()]

def write_to_file(data_object, output_file_path):
	"""Dump an object into a json file."""
	with open(output_file_path, 'w', encoding='utf-8') as file_dump:
		file_dump.write('\n'.join(data_object))

# input_sentences = [
#     "जब मैं छोटा था, मैं हर रोज़ पार्क जाता था।",
#     "हमने पिछले सप्ताह एक नई फिल्म देखी जो कि बहुत प्रेरणादायक थी।",
#     "अगर तुम मुझे उस समय पास मिलते, तो हम बाहर खाना खाने चलते।",
#     "मेरे मित्र ने मुझे उसके जन्मदिन की पार्टी में बुलाया है, और मैं उसे एक तोहफा दूंगा।",
# ]

def process_file(input_file_path, file_name, root_path, source_language, target_language):
	"""Process the file."""
	print(input_file_path)
	src_lang, tgt_lang = lang_code_mapping[source_language], lang_code_mapping[target_language]
	logger.info("Currently running file:|%s|" %(file_name))
	input_sentences = read_lines_from_file(input_file_path)
	translations = []

	file_name_no_extension = file_name[: file_name.find('.')]
	out_file_name = file_name_no_extension + '_MS_Bing.txt'
	output_file_path = os.path.join(root_path, out_file_name)
	if os.path.exists(output_file_path):
			print(f"Output file already exists for {output_file_path}. Skipping...")
			logger.info(f"Output file already exists for {output_file_path}. Skipping...")
			return  # Skip processing and go to the next file


	batch = ip.preprocess_batch(
		input_sentences,
		src_lang=src_lang,
		tgt_lang=tgt_lang,
	)

	# Tokenize the sentences and generate input encodings
	inputs = tokenizer(
		batch,
		truncation=True,
		padding="longest",
		return_tensors="pt",
		return_attention_mask=True,
	).to(DEVICE)
	model.to(DEVICE)
	# Generate translations using the model
	with torch.no_grad():
		generated_tokens = model.generate(
			**inputs,
			use_cache=True,
			min_length=0,
			max_length=256,
			num_beams=5,
			num_return_sequences=1,
		)

	# Decode the generated tokens into text
	with tokenizer.as_target_tokenizer():
		generated_tokens = tokenizer.batch_decode(
			generated_tokens.detach().cpu().tolist(),
			skip_special_tokens=True,
			clean_up_tokenization_spaces=True,
		)

	# Postprocess the translations, including entity replacement
	translations = ip.postprocess_batch(generated_tokens, lang=tgt_lang)
	write_to_file(translations, output_file_path)
	# for input_sentence, translation in zip(input_sentences, translations):
	# 	# print(f"{src_lang}: {input_sentence}")
	# 	# print(f"{tgt_lang}: {translation}")
	# 	print(translation)

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
			process_file(item_path, item, root_path, source_language, target_language)
		
		# If it's a directory, call this function recursively
		elif os.path.isdir(item_path):
			iterate_directory(item_path, source_language, target_language)


if __name__ == '__main__':
	#  main()
	# Set the base directory path
	DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
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
	source = lang_code_mapping[args.src]
	target = lang_code_mapping[args.tgt]
	iterate_directory(base_directory, source_language, target_language)


