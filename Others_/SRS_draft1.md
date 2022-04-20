#### Requirement Analysis
##### Functional planning
The requirements of the user's training model and the management of the database's version are obviously improved, including the requirements of the user's training model and the management of the database's version and so on. Developers adopt the combination of structured analysis method and object-oriented analysis method in demand analysis. Firstly, the subsystems are divided according to the functions, and the functional modules and businesses of each subsystem are determined. Then, the data flow and processing process of the whole system are described by using the structured analysis method, and the interaction between users and the system is described by using the object-oriented method to show the task of the system. Finally, combined with the analysis results of the two methods, it not only manages the data flow and processing process of the system, but also highlights the interaction between users and the system.
##### Overview of specific requirements
In the database module, it not only provides the basic functions of user account login, exit and logout and password management for the interactive interface group. At the same time, it also saves the specific data collected from the sensor.
In addition, the database module also interacts with the server group to obtain the model and data from the algorithm group and save them in the database. The algorithm model and modification will be saved in the form of document, and the corresponding training set and corresponding results will be saved as relational data.
The corresponding requirements are as follows:
1. Input, modify, delete and search of user basic information;
2. Management of user login information;
3. Administrator's addition and password modification;
4. Preservation and management of algorithm model;
5. The addition, deletion, modification and search of data sets and results corresponding to the algorithm model;
6. Storage of sensor data and management of corresponding results;
7. The accuracy of algorithm model and the management of related performance indicators;
8. Backup and restore of database
