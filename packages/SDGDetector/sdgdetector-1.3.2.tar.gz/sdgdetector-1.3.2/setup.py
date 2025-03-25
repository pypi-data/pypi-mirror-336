from setuptools import find_packages, setup

setup(name='SDGDetector',
      version='1.3',
      description='A python library for classifying text with the 17 SDGs.',
      long_description= 'A library for classifying texts to the 17 SDGs using a pretrained fine-tuned RoBERTa or XLNet model or the keywords extraction \
      method, which computes the similarity scores between the extracted keywords of texts with the keywords of the SDGs.The combination of the two methods \
      is also available.',
      url='https://gitlab.com/netmode/SDGDetector',
      author='Ioanna Mandilara',
      author_email='ioanna_mandilara@yahoo.gr',
      packages=find_packages(include=['SDGDetector']),
      install_requires=[
          # 'torch>=2.6.0',  
          'numpy>=1.26.4',  #2.2.3
          'nltk>=3.9.1',  
          # 'transformers>=4.30.2',  
          'sentence-transformers>=3.4.1', # install transformers, scikit-learn
          'sentencepiece>=0.2.0', # needed for XLNet Tokenizer
          # 'scikit-learn>=1.6.1', 
          'keras_preprocessing>=1.1.2' 
      ],
      classifiers=[
        'Programming Language :: Python :: 3',
        'License ::  CC BY-NC 4.0 License',  # License type
        'Operating System :: OS Independent',
      ],
      python_requires=">=3.11",
      include_package_data=True,
      zip_safe=False
      )
