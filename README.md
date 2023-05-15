# SE_Project_Semantle
Final academic project focus on AI using machine learning and word embedding using the Word2Vec models.
The project is based on the 'semantle' game and it's porpuse is to 'solve' the game with minimal number of guesses. The game will be played and solved automatically by the player. 

## Moduls
The project make use in several libraries:
- Word2Vec
- gensim
- nltk


This project aims for research purposes. Because of that, its usage is made by command prompt. The main idea of the project is to check the ability to solve the Semantle challenge with different algorithms in a minimal number of guesses until the secret word is guessed. It is also possible to run the tests offline and returns specific data for each test. Because the system's main purpose is scientific and needs minimal human intervention, the main tool for running the system is the configuration file. Which is a .txt file that contains all configurations needed for running several experiments/games. The configuration file can contain several game configurations , each inside curly bracelets.
Besides, the system contains one menu when the system is loaded to separate the different steps of a game.
The configuration file
The configuration file is a .txt file configured in JSON format(key-value pairs).
As seen below, the values are: 
•	Agent – The game variation. Representing the relationship between the host and the player’s models( Same or different).
•	Host – The host identity. If the game is online against the Semantle game. Or against an offline version.
•	Distance method – The formula name which with it the distance will be calculated.
•	Error – The error ratio. In case of need to create artificial difference between the host and player models.
•	Calc_Error – The two method that are being used to calculate the weights of each word when picking the next guessed word.
This configuration is a combination of two parts, the error vector calculation method. Which can be one of the options below:
-	SUM
-	Sum_Relative
The second part is the method to calculate each word weight in the priority queue that will set the next guessed word, and how to word will be picked from that queue. The options are:
-	 Norm1
-	Norm2
-	Relative_Probability
-	VOI
This two part, will be represented in one string under Calc_Error configuration, in the format part1$part2. 
•	Agent_Model/ Host_Model – The names of the models being used for the host and the player. The options are : 
-	'fasttext_wiki' 
-	'glove_wiki' 
-	 'word2vec_google' 
-	 'local_word2vec' 
•	Algorithm – The name of the algorithm that are being used to calculate the next word. The options are :
-	‘multi-lateration’
-	 ‘n-lateration’ 
-	’ multi-lateration-agent-2’
-	 ‘naive’ 
•	Algorithms_list – A list of algorithms from the list above, that are being used in several tests suck as algorithms compare.
•	Runs – The number of games(Each game represent a secret word need to be guessed by the player).
•	Game_Type – The test being run. In case of None value, the system will play regular game(without saving the results to a file).

The Menu  
The menu contains 4 steps representing one game configuration.
The menu contains the following options that needed to be pressed by order, each one in each turn and after the previous one was completed. The steps are :
-	Build game from file – Reads the configuration file and initialize the games objects and data.
-	Run games – Run the games loaded in the previous step serially one after the other.
-	Clear games – Erase the data loaded after the games run. The clear memory.



Testing
Testing strategy- General
To test the entire system, we spliced the tests into types. At first, we  tested the basic functionality functions using unit tests . such as distance calculations, guessing algorithms etc. Next, we will check components functionality using integration tests, to check the combination of the agents’ actions (Guessing a word, getting feedback, and calculating next guess etc.
And after integration testing, we would test the entire system according to the use cases using various scenarios(test menu), and of course we will run some regression tests along the way. 
All these steps are covering the system functional requirements, to cover Non-Functional requirements as well, we would add more black box testing such as performance tests, to make sure our software can handle different system conditions, communication disturbance and more.
