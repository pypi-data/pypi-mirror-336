import torch
import numpy as np
import re
import os
import nltk
import random
import warnings

from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler, Dataset
from keras_preprocessing.sequence import pad_sequences
from transformers import RobertaForSequenceClassification, RobertaTokenizer, RobertaConfig
from transformers import XLNetTokenizer, XLNetModel, XLNetForSequenceClassification, XLNetConfig,\
set_seed, AutoTokenizer, AutoModelForSequenceClassification,get_linear_schedule_with_warmup

import torch
from torch.nn.utils.rnn import pad_sequence
import torch.nn.functional as F

nltk.download('stopwords') 
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from transformers import logging
logging.set_verbosity_error()

warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", category=DeprecationWarning) 


# Use GPU if available
if torch.cuda.is_available():       
    device = torch.device("cuda")
    print(f'There are {torch.cuda.device_count()} GPU(s) available.')
    print('Device name:', torch.cuda.get_device_name(0))
else:
    device = torch.device("cpu")
    print('No GPU available, using the CPU instead.')

# Dictionary to Map Goal Index to SDG Name
sdg_id2name = {
        1: 'GOAL 1: No Poverty',
        2: 'GOAL 2: Zero Hunger',
        3: 'GOAL 3: Good Health and Well-being',
        4: 'GOAL 4: Quality Education',
        5: 'GOAL 5: Gender Equality',
        6: 'GOAL 6: Clean Water and Sanitation',
        7: 'GOAL 7: Affordable and Clean Energy',
        8: 'GOAL 8: Decent Work and Economic Growth',
        9: 'GOAL 9: Industry, Innovation and Infrastructure',
        10: 'GOAL 10: Reduced Inequality',
        11: 'GOAL 11: Sustainable Cities and Communities',
        12: 'GOAL 12: Responsible Consumption and Production',
        13: 'GOAL 13: Climate Action',
        14: 'GOAL 14: Life Below Water',
        15: 'GOAL 15: Life on Land',
        16: 'GOAL 16: Peace and Justice Strong Institutions',
        17: 'GOAL 17: Partnerships to achieve the Goal'
    }

sdg_keywords={1:['poverty', 'income distribution', 'wealth distribution','socio economic', 'homeless', 'low income','affordab', 'disparity', 
                 'welfare', 'social safety', 'developing country', 'vulnerability', 'precarity','pro-poor'],
              2:['agricultur', 'nutrition', 'food security', 'food insecurity', 'food system', 'child hunger', 'food justice', 'food scarcity',
                 'food sovereignty', 'food culture', 'culinary', 'agro', 'permaculture', 'indigenous crops', 'regenerative agriculture', 
                 'urban agriculture', 'organic food', 'biodynamic', 'food literacy', 'food education', 'benefit sharing', 'access and benefit sharing (ABS)',
                 'malnutrition', 'end hunger', 'food price', 'zero hunger'],
              3:['well being','mental health', 'public health', 'global health', 'health care', 'health issues', 'mental wellness', 'disabilit',
                 'sexual education', 'mindfulness', 'holism', 'illness', 'health education', 'communicable disease', 'health determinants', 'vaccine', 
                 'substance abuse', 'maternal mortality', 'family planning', 'hazardous chemicals', 'pollution', 'health equity', 'neonatal mortality',
                 'infant mortality', 'child health', 'road traffic accidents', 'reproductive health', 'epidemics', 'universal health coverage'],
             4:['equitable', 'pedagogy', 'knowledge', 'worldview', 'learning', 'traditional knowledge', 'land-based knowledge', 'place-based knowledge',
                'decolonial', 'anticolonial', 'settler', 'equitable', 'equity', 'anti-racism', 'racism', 'anti-oppression', 'oppression', 'anti-discriminatory',
                'early childhood development', 'peace', 'citizen', 'sustainability teaching', 'sustainability education', 'universal literacy',
                'basic literacy', 'universal numeracy', 'environmental education', 'education for sustainable development', 'ecojustice education',
                'place-based education', 'humane education', 'land-based learning', 'nature-based education', 'climate change education',
                'vocational', 'technical learning', 'free education', 'accessible education', 'primary education', 'secondary education', 
                'tertiary education'],
             5:['gender', 'women', 'girl', 'queer', 'female', 'feminis', 'non binary', 'sexes', 'LGBTQ', 'patriarchy', 'transgender', 'two-spirit', 
                'gender equality', 'violence against women', 'trafficking', 'forced marriage'],
             6:['water', 'sanita', 'contamination', 'arid', 'drought', 'hygien', 'sewage','water scarcity', 'remediation', 'untreated wastewater',
                'water harvesting', 'desalination', 'water efficiency','groundwater depletion', 'desertification', 'water filtration', 'latrines',
                'open defecation', 'hydrological cycle', 'water and energy nexus', 'stormwater management', 'low impact development', 'green infrastructure',
                'living infrastructure', 'water education'],
             7:['energy', 'renewabl', 'wind', 'solar', 'geothermal','hydroelectric', 'fuel efficient', 'carbon capture', 'emission', 'greenhouse','biofuel',
                'energy sovereignty', 'energy security', 'energy education'],
             8:['employment', 'economic growth', 'sustainable development', 'labour', 'worker', 'wage', 'economic empowerment', 'entrepreneur', 
                'small- and medium-sized enterprises', 'SMEs', 'sustainable tourism', 'youth employment', 'green job', 'economic recovery',
                'green growth', 'sustainable growth'],
             9:['infrastructure', 'buildings', 'capital', 'invest', 'internet', 'globalis', 'Industrialization', 'value chain', 
                'affordable credit', 'industrial diversification'],
             10:['trade', 'inequality', 'financial market', 'taxation', 'equit', 'equalit', 'humanitarian', 'minorit', 'refugee', 'BIPOC',
                 'of colour','indigenous', 'reconciliation', 'truth and reconciliation', 'underserved', 'privileged', 'affordab', 'equal access',
                 'marginalised', 'impoverished', 'vulnerable population', 'social safety', 'social security', 'government program', 'disparity',
                 'income', 'Gini', 'anti-oppressive', 'anti-racist', 'anti-discriminatory', 'decolonization'],
             11:['cities', 'urban', 'resilien', 'rural', 'sustainable development', 'public transport', 'metro', 'housing green infrastructure',
                 'low impact development', 'climate change adaptation', 'climate change mitigation', 'green buildings', 'affordable housing', 'walkab',
                 'transit', 'civic spaces', 'open spaces', 'accessib', 'indigenous placemaking', 'indigenous placekeeping'],
             12:['consum', 'production', 'waste', 'natural resource','recycl', 'industrial ecology', 'sustainable design',
                 'supply chain', 'outsourc', 'offshor', 'reuse','decarbonis', 'carbon tax', 'carbon pricing', 'food waste', 'public procurement',
                 'fossil fuel subsidies'],
             13:['climate', 'greenhouse gas', 'global warming', 'weather', 'environmental', 'planet', 'vegan', 'vegetarian', 'anthropogenic', 'fossil fuel', 
                 'emissions', 'carbon dioxide', 'CO2', 'carbon neutral', 'net zero', 'methane', 'sea level', 'climate change mitigation',
                 'climate change adaptation', 'climate impacts', 'climate scenarios', 'climate solutions', 'climate justice', 'global climate models',
                 'carbon capture', 'carbon sequestration', 'low carbon', 'resilience', 'anthropocene', 'climate positive', 'offsets', 'carbon trading', 
                 'carbon markets', 'UNFCCC', 'climate finance', 'loss and damage', 'Paris'],
             14:['ocean', 'marine', 'pollut', 'conserv', 'fish', 'natural habitat', 'species', 'animal', 'biodivers', 'coral', 'maritime', 
                 'ocean literacy ecosystem', 'overfish', 'fish stocks', 'ocean', 'sustainable use', 'traditional use'],
             15:['forest', 'biodivers', 'ecolog', 'pollut', 'conserv', 'land use', 'natural habitat', 'species', 'animal', 'regeneration', 'resilience', 
                 'sustainable and traditional use', 'land ecological restoration', 'forest conservation', 'carbon sequestration', 'carbon capture', 'soil',
                 'erosion', 'habitat loss', 'endangered species ecosystem', 'deforestation', 'reforestation', 'wildlife', 'flora and fauna', 
                 'benefit sharing'],
             16:['institut', 'governance', 'peace', 'social justice', 'injustice', 'criminal justice', 'human rights', 'democratic rights', 'voter rights', 
                 'legal system', 'social change', 'corrupt', 'nationalism', 'democra', 'authoritarian', 'indigenous', 'judic', 'ecojustice', 
                 'indigenous rights', 'self-determination sovereignty violence', 'exploitation', 'trafficking', 'torture', 'rule of law', 'illicit', 
                 'organized crime', 'bribe', 'terroris', 'prior and informed consent', 'access and benefit sharing', 
                 'UNDRIP (United Nations Declaration on Rights of Indigenous Peoples)', 'indigenous rights'],
             17:['Capacity building','Civil society partnerships','Communication technologies','Debt sustainability','Development assistance',
                 'Disaggregated data','Doha Development Agenda','Entrepreneurship','Environmentally sound technologies','Foreign direct investments',
                 'Fostering innovation','Free trade','Fundamental principles of official statistics','Global partnership','Global stability',
                 'International aid','International cooperation','International support','Knowledge sharing','Multi-stakeholder partnerships',
                 'Poverty eradication','Public-private partnerships','Science cooperation agreements','Technology cooperation agreements',
                 'Technology transfer','Weighted tariff average','Women entrepreneurs','World Trade Organization']}

class SDG_classifier_using_model:

    # SDG Classifier Constructor. Load pretrained model fine-tuned on OSDG-CD
    def __init__(self, model_name, model_path):
        
        # if model_path == None and model_name == None:
        #     print("No model was loaded. Please give a valid fined-tuned model.")

        if model_name == 'RoBERTa' and model_path != None:
            print("Loading RoBERTa model fine-tuned on OSDG-CD...")

            self.model = RobertaForSequenceClassification.from_pretrained('roberta-base', num_labels=16, output_attentions = False,output_hidden_states = False)
            self.model.to(device)
            self.model.load_state_dict(torch.load(model_path, map_location=torch.device(device)),strict=False)

        elif model_name == 'XLNet' and model_path != None:
            print("Loading XLNET model fine-tuned on OSDG-CD...")

            self.model_config = XLNetConfig.from_pretrained('xlnet-base-cased',num_labels=16,low_cpu_mem_usage=True,
                                              problem_type="multi_label_classification",output_attentions = False,output_hidden_states = False)
            self.model = XLNetForSequenceClassification.from_pretrained('xlnet-base-cased',config=self.model_config)
            self.model.to(device)

            self.model.load_state_dict(torch.load(model_path, map_location=torch.device(device)))

        self.model_name = model_name
        self.model_path = model_path

    @property
    def model_name(self):
        return self._model_name
    
    @property
    def model_path(self):
        return self._model_path

    @model_name.setter
    def model_name(self, value):
        if value not in ['RoBERTa','XLNet']:
            raise Exception("Model name must be RoBERTa or XLNet model")
        self._model_name = value

    @model_path.setter
    def model_path(self, value):
        if value is None:
            raise Exception("model_path cannot be None")
        self._model_path = value

    
    def __pad_sentences(self,input_ids, maxlen):
    # Pad sequences manually using PyTorch
        padded_input_ids = pad_sequence([torch.tensor(x) for x in input_ids], 
                                        batch_first=True, padding_value=0)
        
        # Truncate sequences if they are longer than `maxlen`
        if padded_input_ids.size(1) > maxlen:
            padded_input_ids = padded_input_ids[:, :maxlen]
        
        # Pad sequences to `maxlen` length (at the end)
        if padded_input_ids.size(1) < maxlen:
            padding = torch.zeros((padded_input_ids.size(0), maxlen - padded_input_ids.size(1)), dtype=torch.long)
            padded_input_ids = torch.cat([padded_input_ids, padding], dim=1)
        
        return padded_input_ids

    # Function to prepare sentences as inputs 
    def sentence_preprocess(self, sentences, MAX_LEN = 512):
        
        if self.model_name == 'RoBERTa':

            # Use RoBERTa tokenizer to tokenize the sentence
            tokenizer = RobertaTokenizer.from_pretrained('roberta-base', do_lower_case=True,add_prefix_space=True)

            tokenized_texts = [tokenizer.tokenize(sent) for sent in sentences]

            # Clean text and add special tokens at the beginning and end of each sentence for RoBERTa to work properly
            tokenized_sentences = [["[CLS]"] + sentence + ["[SEP]"] for sentence in tokenized_texts]

            # Use the RoBERTa tokenizer to convert the tokens to their index numbers in the RoBERTa vocabulary
            input_ids = [tokenizer.convert_tokens_to_ids(x) for x in tokenized_sentences]

            # Pad our input tokens - no truncation will take place
            # old version
            # input_ids = pad_sequences(input_ids, maxlen=MAX_LEN, dtype="long", truncating="post", padding="post")
            # new version
            input_ids = self.__pad_sentences(input_ids, MAX_LEN)

            # Create attention masks
            attention_masks = []

            # Create a mask of 1s for each token followed by 0s for padding
            for seq in input_ids:
                seq_mask = [float(i>0) for i in seq]
                attention_masks.append(seq_mask)

            # Convert all of our data into torch tensors, the required datatype for our model
            inputs = torch.tensor(input_ids)
            masks = torch.tensor(attention_masks)
        
        if self.model_name == 'XLNet':
            tokenizer = XLNetTokenizer.from_pretrained(pretrained_model_name_or_path='xlnet-base-cased')
            token = tokenizer(text=sentences, return_tensors="pt", padding=True, truncation=True,  max_length=MAX_LEN)

            inputs = token['input_ids']
            masks = token['attention_mask']

        class CustomTextDataset(Dataset):
            def __init__(self, ids, attention, code):
                self.input_ids = ids
                self.attention_masks = attention
                self.code = code

            def __len__(self):
                return len(self.input_ids)

            def __getitem__(self, idx):
                input_id = self.input_ids[idx]
                attention_mask = self.attention_masks[idx]
                inputs_codes = self.code[idx]
                sample = {"id": input_id, "mask": attention_mask,'code':inputs_codes}
                return sample

        length_of_texts= len(sentences)
        input_codes = list(range(1, length_of_texts+1))

        if length_of_texts >= 32:
            BATCH_SIZE = 32    
        else:
            BATCH_SIZE = length_of_texts
        data = CustomTextDataset(inputs, masks,input_codes)
        dataloader = DataLoader(data,batch_size=BATCH_SIZE,shuffle=True)

        return dataloader

    # Main Function that maps Text to SDG
    def predict(self, sentence, return_probs=False):

        # preprocess input sentence
        dataloader = self.sentence_preprocess(sentences=sentence,MAX_LEN = 512)

        # Inference Time
        self.model.eval()

        probs_dict,sdg_dict= {},{}

        for (idx, batch) in enumerate(dataloader):

            b_input_ids = batch['id'].to(device)
            b_input_mask = batch['mask'].to(device)

            print('The association of batch {} of {} texts with the SDGs by using the model was calculated'.format(idx+1,len(b_input_ids)))

            with torch.no_grad():        

                output = self.model(b_input_ids, 
                            token_type_ids=None, 
                            attention_mask=b_input_mask)

                #loss = output.loss
                logits = output.logits

                sigmoid = torch.nn.Sigmoid()
                probs = sigmoid(logits)

            probs = probs.detach().cpu().numpy()
            probs = np.round(probs*100,2)
            probs = probs.tolist()

            logits = logits.detach().cpu().numpy()
            sdg = np.argmax(logits, axis=1).flatten()

            # Dictionaries
            probs_dict_batch = {batch['code'][i]: probs[i] for i in range(len(batch['code']))}
            probs_dict.update(probs_dict_batch)

            sdg_dict_batch = {batch['code'][i]: sdg[i] + 1 for i in range(len(batch['code']))}
            sdg_dict.update(sdg_dict_batch)

        probsKeys = list(probs_dict.keys())
        probsKeys.sort()
        sorted_probs_dict = {i: probs_dict[i] for i in probsKeys}

        sgdsKeys = list(sdg_dict.keys())
        sgdsKeys.sort()
        sorted_sdg_dict = {i: sdg_dict[i] for i in sgdsKeys}

        sdg_names = [sdg_id2name[x] for x in list(sorted_sdg_dict.values())]

        # return probability belonging to each SDG
        if return_probs:
            return list(sorted_sdg_dict.values()),sdg_names, list(sorted_probs_dict.values())

        return list(sorted_sdg_dict.values()),sdg_names

class SDG_classifier_using_keywords_extraction:

    def __init__(self, top_keywords = 5, diversity = 0.3, n_gram_range = (1,2) , model_name = None):

        if model_name in ['all-mpnet-base-v2','distilbert-base-nli-mean-tokens','all-MiniLM-L6-v2']:
            print('Loading Sentence Transformer model: {}..'.format(model_name))
            self.model = SentenceTransformer(model_name,device=device)
            self.model.max_seq_length = 512

        self.model_name = model_name
        self.top_keywords = top_keywords
        self.diversity = diversity
        self.nrangex,self.nrangey = n_gram_range

    @property
    def model_name(self):
        return self._model_name

    @model_name.setter
    def model_name(self, value):
        if value not in ['all-mpnet-base-v2','distilbert-base-nli-mean-tokens','all-MiniLM-L6-v2']:
            raise Exception("model_name must be either 'all-mpnet-base-v2' or 'distilbert-base-nli-mean-tokens' or 'all-MiniLM-L6-v2'")
        self._model_name = value
    
    def find_top_keywords(self, texts):

        full_keywords= []

        for txt in texts:
            # Delete digits in text 
            doc = re.sub(r'\d+', '', txt)

            # Select the size of the resulting candidates and the stop words provided by the package nltk
            n_gram_range = (self.nrangex,self.nrangey)
            stop_words = stopwords.words('english')

            # Extract candidate words/phrases
            # Convert a collection of text documents to a matrix of token counts
            count = CountVectorizer(ngram_range=n_gram_range, stop_words=stop_words).fit([doc])
            # Get output feature names for transformation.
            candidates = count.get_feature_names_out()

            # We convert both the document as well as the candidate keywords/keyphrases to numerical data.
            doc_embedding = self.model.encode([doc],show_progress_bar = False)
            candidate_embeddings = self.model.encode(candidates,show_progress_bar = False)

            # MMR
            # Extract similarity within words, and between words and the document
            word_doc_similarity = cosine_similarity(candidate_embeddings, doc_embedding)
            word_similarity = cosine_similarity(candidate_embeddings)

            # Initialize candidates and already choose best keyword/keyphras
            keywords_idx = [np.argmax(word_doc_similarity)]
            candidates_idx = [i for i in range(len(candidates)) if i != keywords_idx[0]]

            for _ in range(self.top_keywords - 1):
                # Extract similarities within candidates and
                # between candidates and selected keywords/phrases
                candidate_similarities = word_doc_similarity[candidates_idx, :]
                target_similarities = np.max(word_similarity[candidates_idx][:, keywords_idx], axis=1)

                # Calculate MMR
                mmr = (1-self.diversity) * candidate_similarities - self.diversity * target_similarities.reshape(-1, 1)
                mmr_idx = candidates_idx[np.argmax(mmr)]

                # Update keywords & candidates
                keywords_idx.append(mmr_idx)
                candidates_idx.remove(mmr_idx)

            # Append the list of top10 keywords using mmr
            full_keywords.append([candidates[idx] for idx in keywords_idx])
        
        return full_keywords

    def predict(self,text,return_cs_matrix_and_avg_cs=False):

        # find top keywords
        text_keywords = self.find_top_keywords(texts = text)
        #embeddings of texts keywords
        sdg_embeddings = {sdg: self.model.encode(sdg_keywords[sdg], show_progress_bar=False) for sdg in sdg_keywords.keys()}
        #embeddings of sdg keywords
        text_embedding = {i: self.model.encode(keywords_per_txt, show_progress_bar=False) for i,keywords_per_txt in enumerate(text_keywords)}

        cosine_per_text, cosine_matrix_per_text,sdg_per_text=[],[],[]
        for i in range(len(text_keywords)):
            cosine,cosine_matrix=[],[]
            for sdg_key in sdg_embeddings.keys():
                cosine_matrix_ = cosine_similarity(text_embedding[i], sdg_embeddings[sdg_key])
                avg_cosine_sim = np.average(cosine_matrix_)
                cosine.append(avg_cosine_sim)
                cosine_matrix.append(cosine_matrix_)
            
            print('The cosine similarity score between text {} and the SDGs was calculated'.format(i+1))

            sdg = cosine.index(max(cosine)) + 1

            cosine_per_text.append(cosine)
            cosine_matrix_per_text.append(cosine_matrix)
            sdg_per_text.append(sdg)  

        # for i in range(len(text)):
        #     cosine,cosine_matrix=[],[]
        #     for sdg,sdg_keyword in sdg_keywords.items():                

        #         # embeddings of keywords and sdgs keywords
        #         sdg_embedding = self.model.encode(sdg_keyword,show_progress_bar=False)
        #         candidate_embeddings = self.model.encode(text_keywords[i],show_progress_bar=False)

        #         # compute cosine similarity matrix & avg cosine similarity
        #         cosine_matrix_ = cosine_similarity(sdg_embedding, candidate_embeddings)
        #         avg_cosine_sim = np.average(cosine_matrix_)

        #         cosine.append(avg_cosine_sim)
        #         cosine_matrix.append(cosine_matrix_)

        #     sdg = cosine.index(max(cosine)) + 1

        #     cosine_per_text.append(cosine)
        #     cosine_matrix_per_text.append(cosine_matrix)
        #     sdg_per_text.append(sdg)

        sdg_names = [sdg_id2name[x] for x in sdg_per_text]

        if return_cs_matrix_and_avg_cs:
            return sdg_per_text,sdg_names,cosine_per_text,cosine_matrix_per_text
        return sdg_per_text,sdg_names

class SDG_classifier:
    def __init__(self,pretrained_model_path = None,pretrained_model_name = None,top_keywords = 5, diversity = 0.3, n_gram_range = (1,2) , sentence_model_name = None):
        self.sdg_model  = SDG_classifier_using_model(pretrained_model_name, pretrained_model_path)
#         self.sdg_model.to(device)
        self.sdg_keywords = SDG_classifier_using_keywords_extraction(top_keywords, diversity, n_gram_range, sentence_model_name)

    def predict(self,text,return_association = False):

        sdg_pretrained_model,sdg_name_pretrained_model, probs_pretrained_model = self.sdg_model.predict(text, return_probs=True)
        sdg_cosine_similarity,sdg_name_cosine_similarity, avg_cosine_similarity,cosine_similarity_matrix = self.sdg_keywords.predict(text, return_cs_matrix_and_avg_cs=True)

        list_of_ass,list_of_sdgs = [],[]
        for no_txt in range(len(text)):
            # Compute formula
            sdg_dict = {}

            for i in range(0,16,1):
                association = 0.7*(probs_pretrained_model[no_txt][i]/100) + 0.3*avg_cosine_similarity[no_txt][i]
                sdg_dict[i+1] = association
            sdg_dict[17] = 0.5*avg_cosine_similarity[no_txt][-1]

            sdg = max(sdg_dict, key=sdg_dict.get)

            list_of_ass.append(list(sdg_dict.values()))
            list_of_sdgs.append(sdg)

        sdg_names = [sdg_id2name[x] for x in list_of_sdgs]

        if return_association:
            return list_of_sdgs,sdg_names,list_of_ass

        return list_of_sdgs,sdg_names