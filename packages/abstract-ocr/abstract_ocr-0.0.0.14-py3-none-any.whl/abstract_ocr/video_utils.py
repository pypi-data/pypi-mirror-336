import cv2,pytesseract,os,shutil,logging,spacy,json,re
logging.basicConfig(level=logging.INFO)  # Set level to INFO or higher
from .ocr_utils import *
from moviepy import VideoFileClip
import numpy as np
from abstract_utilities import eatAll,safe_read_from_json
from collections import Counter
# Load spaCy model (run `python -m spacy download en_core_web_sm` first if not installed)
nlp = spacy.load("en_core_web_sm")
def analyze_video_text(video_path,output_dir=None):
    dirname = os.path.dirname(video_path)
    output_dir = output_dir or os.path.join(dirname,'./frames')
    os.makedirs(output_dir, exist_ok=True)

    # Load the video
    video = VideoFileClip(video_path)
    duration = video.duration

    # Extract frames every 1 second
    frame_interval = 1  # Adjust as needed
    for t in range(0, int(duration), frame_interval):
        frame = video.get_frame(t)
        frame_path = f"{output_dir}/frame_{t}.jpg"
        cv2.imwrite(frame_path, cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR))

    # Function to extract text from an image
    def extract_text_from_image(image_path):
        img = cv2.imread(image_path)
        # Preprocess: Convert to grayscale and apply thresholding
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # Apply OCR
        text = pytesseract.image_to_string(thresh)
        return text.strip()

    # Process all extracted frames
    extracted_text = []
    for frame_file in os.listdir(output_dir):
        if frame_file.endswith(".jpg"):
            image_dir = f"{output_dir}/{frame_file}"
            text = extract_text_from_image(image_dir)
            if text:  # Only append non-empty text
                extracted_text.append({"frame": frame_file, "text": text})
                
    # Clean up (optional)
    return extracted_text
def get_file(filename,directory):
    file=None
    for item in os.listdir(directory):
        basename = os.path.splitext(item)[0]
        if basename and str(filename) == str(basename):
            file = item
            break
    return file
def get_thumbnail_texts(directory):
    texts = []
    if not directory.endswith('thumbnails'):
        thumbnails_dir = os.path.join(directory,'thumbnails')
    if os.path.isdir(thumbnails_dir):
        for thumbnail in os.listdir(thumbnails_dir):
            thumbnail_path = os.path.join(thumbnails_dir,thumbnail)
            text= convert_image_to_text(thumbnail_path)
            if text:
                texts.append(text)
    return texts
def get_constants(text,constants=[]):
    if constants == []:
        for line in text.split('\n'):
            line = eatAll(line,[' ','','\n','\t','\n'])
            constants.append(line)
        return constants
    constants = {const:False for const in constants}
    for line in text.split('\n'):
        line = eatAll(line,[' ','','\n','\t','\n'])
        for key,value in constants.items():
            if line in key and value == False:
                constants[key] = True
    constants_output=[]
    for key,value in constants.items():
        if value == True:
            constants_output.append(key)
    return constants_output
def get_text_constants(video_text):
    constants={}
    video_text_length = len(video_text)
    for j,frame in enumerate(video_text):
        print(frame)
        text = frame.get('text')
        text_spl = text.split('\n')
        text_spl_len = len(text_spl)
        for i,line in enumerate(text_spl):
            line = eatAll(line,[' ','','\n','\t','\n'])
            if line not in constants:
                constants[line]={"count":0,"positions":[]}
            constants[line]["count"]+=1
            constants[line]["positions"].append({"count":i+1,"of":text_spl_len,"frame":j+1})
    return constants
def derive_video_info(data,keywords=[],description='',title=''):

    # Step 1: Preprocess the data
    def preprocess_text(text):
        # Remove special characters, normalize case, and fix common OCR errors
        text = re.sub(r'[^\w\s@]', '', text).strip().lower()
        return text

    # Extract phrase frequencies
    phrase_counts = {preprocess_text(phrase): info["count"] for phrase, info in data.items()}
    def extract_keywords_nlp(data, top_n=5):
        # Combine all phrases into a single text, weighted by count
        combined_text = " ".join([preprocess_text(phrase) * info["count"] for phrase, info in data.items()])
        
        # Process with spaCy
        doc = nlp(combined_text)
        
        # Extract nouns, proper nouns, and entities
        word_counts = Counter()
        for token in doc:
            if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop and len(token.text) > 2:
                word_counts[token.text] += 1
        
        # Extract multi-word entities (e.g., "Elon Musk")
        entity_counts = Counter(ent.text.lower() for ent in doc.ents if len(ent.text.split()) > 1)
        
        # Combine and rank
        combined_counts = word_counts + entity_counts
        top_keywords = [word for word, count in combined_counts.most_common(top_n)]
        
        return top_keywords
    keywords_nlp = extract_keywords_nlp(data)
    keywords +=keywords_nlp
    # Step 2: Extract Title
    def get_title(phrase_counts, min_count=10):
        # Filter out noise and low-frequency phrases
        valid_phrases = {phrase: count for phrase, count in phrase_counts.items() 
                         if count > min_count and phrase and not phrase.startswith("~~~") and len(phrase.split()) > 1}
        try:
            # Sort by frequency and pick the top phrase
            top_phrase = max(valid_phrases.items(), key=lambda x: x[1])[0]
        except:
            top_phrase=''

        return top_phrase.capitalize()

    title+= ' '+ get_title(phrase_counts)

    # Step 3: Generate Description
    def get_description(phrase_counts, top_n=5):
        # Define keywords related to common video themes
        
        # Get top N frequent phrases
        top_phrases = sorted(phrase_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
        
        # Filter phrases with keywords
        relevant_phrases = [phrase for phrase, count in top_phrases 
                            if any(kw in phrase for kw in keywords) or count > 20]
        
        # Simple template-based description
        desc = description
        
        
        themes = [phrase for phrase in relevant_phrases if len(phrase.split()) > 1]
        desc += ", ".join(themes[:3])
        return desc

    description = get_description(phrase_counts)

    # Step 4: Determine Uploader
    def get_uploader(phrase_counts):
        # Look for phrases that look like handles or names
        candidates = [phrase for phrase in phrase_counts.keys() 
                      if phrase.startswith("@") or phrase.isupper()]
        
        if not candidates:
            return "Unknown"
        
        # Pick the most frequent candidate
        uploader = max(candidates, key=lambda x: phrase_counts[x])
        return uploader

    uploader = get_uploader(phrase_counts)

    return {"description":description,"uploader":uploader,"title":title,'keywords':keywords}
def derive_all_video_meta(video_path,output_dir=None,video_text_path=None,keywords=None,description=None,title=None):
    video_dir = os.path.dirname(video_path)
    info_path = os.path.join(video_dir,'info.json')
    if os.path.isfile(info_path):
        info_data = safe_read_from_json(info_path)
        keywords = keywords or info_data.get('context',{}).get('keywords',[])
        description = description or info_data.get('context',{}).get('description','')
        title = title or info_data.get('context',{}).get('title','')
    if video_text_path == None:
        text_dir = os.path.join(video_dir,'video_text')
        os.makedirs(text_dir, exist_ok=True)
        video_text_path = os.path.join(text_dir,'video_text.json')
    video_text = analyze_video_text(video_path,output_dir=output_dir)
    text_constants = get_text_contants(video_text)
    thumbnail_texts = get_thumbnail_texts(video_dir)
    video_info = derive_video_info(text_constants,keywords,description,title)
    video_json = {"video_file_path":video_path,'thumbnail_texts':thumbnail_texts,"video_info":video_info,"video_text":video_text,"text_contants":text_constants}
    safe_dump_to_file(data=video_json,file_path=video_text_path)
    return video_json
