Software project WiSe 2015/16  
Institute of Computational Linguistics  
Heidelberg University, Germany  

The Great Dictation
===================

*Project plan*  
Authors: Dominik Both, Tobias Göbel, Svenja Lohse, Tonio Weidler  
Advisor: Magdalena Wolska  

About the Task
------
Our **goal** is an online dictation system for non-native speakers to support and exercise their listening and writing skills in an acquired second language (in our case German).
It will be important to motivate the learners and keep them in this state over the whole learning process.
Analysing their mistakes, giving them constructive feedback and using the analysed data for improvement of our system - these are the desirable steps to make our dictation platform, aka *The Great Dictation* awesome.

**Why dictation and listening comprehension?**  
Orthography or Spelling has to be exercised to enhance it.
Using auditive dictation and therefore listening comprehension plays a key role in facilitating language learning by coordinating the discrimination between sounds, understanding of vocabulary and grammatical structures, as well as interpretation of stress and intonation for punctuation.
Furthermore the students have greater motivation to continue learning because they can develop their listening skills and concentrate on internalising grammar rules instead of additional pressure of producing own text intonations while handling all the before mentioned processes in their heads. *(Vandergrift,1999)*
With dictation they do not only learn vocabulary, they also learn grammar while memorising meaning and relationship of words *(Alkire,2002)* and get some useful standard phrases. Afterwards they can review a list of their mistakes, get some advice for grammar rule repetition and keep track of their progress. *(Kazazoglu, 2012)*

To that end we have to *filter, sort, group and analyse* the mistakes, consistently *refine our algorithm* with given data, find a way to give positive and *motivating result feedback*, on the one hand build the whole platform on a *solid, extensible database* and on the other hand make it *interesting and user friendly* in design and use.

Data Representations/Formats and System Components/Modules
----
With the former in mind the composition of said system has to be constructed to fullfil the needed requirements. In web development an application is normally parted in two modules, the server side back end and the client side front end. The back end, serving the main controller of the application and functioning as a connector between database and the application, and the frontend, officiating as the viewpoint of the user and the interface between human and computer. This general model can be utilised for our application as well. However, we decided to bisect the back end to separate the standard backend comprising page generation and user administration system from the analysis back end containing the computational lingustic analysis itself. Thus we can dispose of different programming languages for each section of the back end. Availing ourself of this possibility allows us to combine the time efficience of PHP in building web application backends and the effectivity of Python in linguistic analysis. 

Schedule and concrete Distribution of Tasks
----
tbc...  

**Main Responsibilities**:  
*Dominik*: Backend-Development, Database Management
*Tobias*: Analysing-Algorithms, kind of mistakes  
*Svenja*: Didatic background of dictation/listening comprehension and feedback/result (research)  
*Tonio*: Frontend-Development, Database Management, Project Management
Although everybody participates in each section for minor tasks.


**schedule**:  
-> *roadmap*  
01.12.15 v0 and project plan finished  
08.12.15 start of data collection  
...analysis features, result feedback, platform design, fancy stuff  
02.02.16  version with features finished, final presentation  
ca. 12.03. final submission of code and documentation  

Specifikation of System architecture and Data format(s)
----
von Folie übernommen...tbc  
