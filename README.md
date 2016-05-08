Software project WiSe 2015/16  
Institute of Computational Linguistics  
Heidelberg University, Germany  

The Great Dictation
===================

*Final README / DOCUMENTATION*  
Authors: Dominik Both, Tobias Göbel, Svenja Lohse, Tonio Weidler  
Advisor: Magdalena Wolska  

Distribution of Tasks
----
We divided the accrued tasks according to the special skills each of us brings in.

**Main Responsibilities**:  
*Dominik*: Backend development, database management

*Tobias*: Analysing algorithms, kinds of mistakes  

*Svenja*: Didatic background of dictation/listening comprehension and feedback/result (research)  

*Tonio*: Frontend development, database management, project management

Although everybody participates in each section for minor tasks.

Contacts  
----

S.Lohse (--at--) stud.uni-heidelberg.de

tobygoebel (--at--) web.de

uni (--at--) dboth.de

uni (--at--) tonioweidler.de

Link
----
http://dictator.cl.uni-heidelberg.de/  

Requirements
----
- Server
- PHP >= 5.3
- Python 2 or 3
- Apache user (normally www-data) able to execute Python scripts in code/analysis
- MySQL database


About the Task
------
Our **goal** is an online dictation system for non-native speakers to support and exercise their listening and writing skills in an acquired second language (in our case German).
It will be important to motivate the learners and keep them in this state over the whole learning process.
Analysing their mistakes, giving them constructive feedback and using the analysed data for improvement of our system - these are the desirable steps to make our dictation platform, aka *The Great Dictation* awesome.

**Why dictation and listening comprehension?**  
Orthography or Spelling has to be exercised to enhance it.
Using auditive dictation and therefore listening comprehension plays a key role in facilitating language learning by coordinating the discrimination between sounds, understanding of vocabulary and grammatical structures, as well as interpretation of stress and intonation for punctuation.  
Furthermore the students have greater motivation to continue learning because they can develop their listening skills and concentrate on internalising grammar rules instead of additional pressure of producing own text intonations while handling all the before mentioned processes in their heads *(Vandergrift,1999)*.  
With dictation they do not only learn vocabulary, they also learn grammar while memorising meaning and relationship of words *(Alkire,2002)* and get some useful standard phrases. Afterwards they can review a list of their mistakes, get some advice for grammar rule repetition and keep track of their progress. *(Kazazoglu, 2012)*

To that end we have to *filter, sort, group and analyse* the mistakes, consistently *refine our algorithm* with given data, find a way to give positive and *motivating result feedback*, on the one hand build the whole platform on a *solid, extensible database* and on the other hand make it *interesting and user friendly* in design and use.  

Data
----
It is in the nature of our task that there is *no data* available upfront. Therefore we need to collect the data ourselves. To that end our system is designed to *collect data* while it *expands its features*.  
To provide an incentive, the **version zero** already contains a small analysis that expands by using the data it collects.  

System architecture and modules
----
With the former in mind the composition of said system has to be constructed to fullfil the needed requirements.

In web development an application is usually parted in two modules: The server sided *backend* and the client sided *frontend*.  
The **backend** serves as the *main controller* of the application and functions as a *connector* between the database and the application. The **frontend** represents the *viewpoint of the user* and officiates as the *interface between human and computer*.

This general model can be utilised for our application as well. However, we decided to bisect the backend to separate the **standard backend** - comprising *page generation* and *user administration system* - from the **analysis backend**, containing the *computational lingustic analysis* itself. Thus we can dispose of different programming languages for each section of the backend, allowing us to combine the time efficience of PHP in building web application backends and the effectivity of Python in linguistic analysis.

In conclusion there are three components:  
* Management backend
* Analysis backend
* Frontend

**Management Backend**   
Blablabla....   

**Analysis Backend**  
The analysis is used to find the best alignment between target and input text. it contains several sub-algorithms listed below. In principle it consists of the alignment itself,
an implementation of the ukkonen algorithm to find the longest common substrings which are used to accellerate the algorithm and a post processing part which creates the final word alignment.

| Name                      | Location          | Description
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| * Aligner                 | analysis/Aligner.py               | Core of the Analysis. This is based on the Needleman-Wunsch Algorithm. It gets input and target string and returns the optimal alignment                                              |
| submodules:               |                                   |                                                                                                                                                                                       |
| FaultPenalizer            | analysis/FaultPenalizer.py        | Class to change path probability weights (probability to choose a path with this process) to fault weights (penalty for the fault the user made) after the optimal path is found.     |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| * SuffixTree              | analysis/SuffixTree               | This is an implementation of the ukkonen algorithm to find suffix trees. The implementation is slightly different and thus are the denotations.                                      |
| submodules:               |                                   |                                                                                                                                                                                       |
| - TreeGhost               | analysis/TreeGhost                | These refer to the active points in the ukkonen algorithm                                                                                                                             |
| - TreeNode                | analysis/TreeNode                 | These are the nodes of the suffix tree                                                                                                                                                |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| * AlignmentPostProcessor  | analysis/AlignmentPostProcessor   | This takes the path from the aligner which only consists of processes and turns it into a word to word alignment which contains all relevant information for the frontend.            |
| submodules:               |                                   |                                                                                                                                                                                       |
| None                                                                                                                                                                                                                                                  |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

**Frontend**  
The frontend determines, which informations it needs to receive from the backend to show the user what he wants to see. It also asks the user for information to send to the backend.
To define, what the user sees in his browser, *HTML* and *CSS* (SASS as a preprocessor) are used to structure and style the content. Several Javascript scripts handle page events like actions by the user and process the data received from the backend to show it to the user in an appropriate and appealing way.
*The Great Dictation* is usable on multiple plattforms including mobile devices and therefore fully responsible. This means it design dynamically adapts to the users screensize. We implemented this responsiveness via **Bootstrap**, a framework that consists of HTML, CSS and JS Components, providing a useful Grid Structure and several other functionalities. This framework was customized, such that it fits the project. With **jQuery** we included a common framework that simplifies many processes in JS. Charts are created with the help of **ChartJS**, one of the most famous libraries in this area. It not only displays the charts but also provides the user interactivity (tooltips).
Pages are build by reusable components that get plugged into page layouts which themselves are loaded into the main template. This way we can reuse the same template for all pages and reuse components like the result in different pages. One of the main concerns of this projects frontend is how to display the results of the dictations. Apart from that it consists of scripts that manage the error messages that the user receives, register, login, feedback and evaluation forms and different pages that dynamically adjust to the users actions and data (e.g. the profile page, statistics page, etc.).

The HTML/PHP pages generating the views are organized in a wrapper directory containing the templates in which pages can be plugged in, a subdirectory containing all pages (*frontend/pages/*) and one containing components that themselves get plugged into pages (*frontend/components/*). Those Components are reusable in different Pages.

The JS Files are organized in a wrapper js/ folder that contains the following subdirectories:  

| Name                 | Location              | Description                                                                                       |
|----------------------|-----------------------|---------------------------------------------------------------------------------------------------|
| Asynchronous Calls   | js/async_calls/       | Collection of Asynchronous Calls (via AJAX) to receive or save data without reloading the page.   |
| Libraries            | js/libs/              | Directory for all JS-libraries used in the project.                                               |
| Page Events          | js/page_events/       | JS Handler for specific pages handling events (e.g. buttons)                                      |
| Result Generation    | js/result_generation/ | All Files concerning the processing of the analysis data and generation of the Result Page        |
| Dictation List       | js/show_dictations/   | Files concerned with again showing past dictations and listing them                               |
| Statistic Generation | js/statistics/        | All Files concerning the displaying and calculation of Statistics about an users past performance |

The most important JS Modules are listed in the following table:

| Name              | Location                                 | Description                                                                                                                                                                                                                                                                                                                                       |
|-------------------|------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Result Class      | js/result_generation/Result.js           | Class, that takes the analysis data as an argument and contains several methods to display informations about the Dictation. Those methods are used to fill the result page.                                                                                                                                                                      |
| Result Displaying | js/result_generation/display_analysis.js | Handles the Submit Button in the dictation page. Once clicked, it asynchronously sends the dictation text and additional informations to the analysis backend and receives back the analysed data. It then calls the function createAnalysis(...) which builds up the Result Page by using the methods provided in the Result Class (see above).  |
| Error Handler     | js/error_handler.js                      | Contains two methods that allow to show the user information about an error by first identifying the error via an AJAX call to the Error Handler in the Backend and then processing and displaying this information to the user.                                                                                                                  |
| General Functions | js/functions.js                          | A file containing functions used all over the project, sort of a mini library.                                                                                                                                                                                                                                                                    |
|                   |                                          |                                                                                                                                                                                                                                                                                                                                                   |


Obstacles
---
,bdjskvv  

Result
----
The data calculated by the backends analysis components is processed by the frontend to show the user informations and statistics about his errors and performance.  
In the **What you've entered** Section the user gets presented the whole text as how he typed it in. Where he made mistakes the word is highlighted in a color representing the weight of the error.  
The **Error Distribution** shows how the users characterwise mistakes are distributed over the different mistake groups. Those are created by categorizing the *Aligners* error types as follows: *correct, waste, missing, wrong, switched, capitalization, punctuation, similar punctuation* and *word switch*. This distribution can be either displayed as a radar chart or as a bar chart. The current dictation is compared to the users average values.   
The **Rating** consists of the ratio of correct and total words in this dictation and a score for the dictation. The score is calculated as a value between 0 and 100 representing the *correctness* of the users input. It considers the weight of errors and the word lengths.  
A **Detailed character by character error info** shows the words with mistakes again by exactly revealing where the mistakes were made and how to correct them.  
The line chart under the section **Performance over time** shows how the errorweight of the levenshtein path develops over the text (word-wise).  
All past dictations can be reviewed under *Your Dictations*, where the same informations will be showed again. Average values and statistics about all dictations can be looked up under *Statistics*.  


Literature
----
dbldsbhljblh...  
