# Kashmir workshop code
# challenge-set
## Source code

### Normalizer

````
python3 normalizer.py input.txt > output.txt
````
### Sentence split using NTLK

````
python3 sentence_nltk.py input.txt > output.txt
````


## MT code

### Bing

#### Format input directory > eng-hin > file.txt

````
python3 bing_translator.py --input=input_dir --src=eng --tgt=hin
````

### SSMT

```
python3 recursive_dir_run_ssmt_api.py --input=input_dir --src=eng --tgt=hin
```

### AI4 Bharath

```
python3 ai4_bharata_inference.py --input=input_dir --src=eng --tgt=hin
````