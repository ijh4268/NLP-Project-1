# CS 337 - Project 1 - Golden Globes Tweet Mining

Team Members: Andrew Huang, Chase Duvall, Patrick George, Isaac Henry

Use `pip3 install -r requirements.txt` to install all required python packages.

Use `python3 -m spacy download en_core_web_sm` to install the SpaCy module

We've included a spacy.zip file of the .spacy files containing the preprocessed data for the tweets for your convenience. If you want to run the preprocessor to generate those files yourself, you can set the `spacy` parameter to `True` in the `pre_ceremony()` function in gg_api.py (defaults to False). **Please note: this will take a while, about an hour and a half or so to process both gg json files**

If you want to use the .spacy files, unzip the folder and place the two files in the same directory as the rest of the code.


Please first run pre_ceremony() in gg_api.py for each year that is analyzed. For example, to test on 2013, run pre_ceremony(2013), with gg2013.json in the same directory as gg_api.py.

Please run main() with the appropriate year to get the human-readable output, along with the results for best and worst dressed of the event.

In gg_api.py, we run pre_ceremony() and main() for you with 2013 and 2015 as inputs.
