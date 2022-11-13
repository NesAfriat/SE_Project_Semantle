# SE_Project_Semantle
Final academic project focus on AI using machine learning and word embedding using the Word2Vec models.
The project is based on the 'semantle' game and it's porpuse is to 'solve' the game with minimal number of guesses. The game will be played and solved automatically by the player. 

## Moduls
The project make use in several libraries:
- Word2Vec
- gensim
- nltk

## External tools
For the words model creation, there is a need for a large file database. For that project, we use the [wikipedia database](https://meta.wikimedia.org/wiki/Data_dump_torrents#English_Wikipedia) and used the [wp2txt](https://github.com/yohasebe/wp2txt) tool to parse them. 

### parsing
To use the wp2txt tool there is need to install the libraries:
- lbzip2
- gem
After that, install via gem the wp2txt tool. 
after parsing, make sure the files are in a folder named 'Trains' inside the current working directory. So that the model will be trained using those files.
For specific preperation instructions use the [link](https://github.com/yohasebe/wp2txt#preparation)

## Training
To train the model, there is a need for large database of files. As said before, we used the wikipedia database. Before training, make sure the current project directory must include a folder named 'Model' for saving the created the model after training, and for loading an existing model. 
 
## useful links
[Presentation](https://www.canva.com/design/DAFRYJAmbNg/_d_bKCAGRgMu5d2TtldRHQ/edit?utm_source=shareButton&utm_medium=email&utm_campaign=designshare#)
[UML](https://app.diagrams.net/#G1-d7tI8ivWkuQoYyhlRgrr8loEUvlj2Z_)
[ARD](https://docs.google.com/document/d/1drYsqAkdsnR_eQdjR0mnUvczxVibufzVPYcYIjzX1-4/edit#)
