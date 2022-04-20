<!-- Happy Family (DB) ~ Interaction -->

### Case: Interaction wants to store user personal information in the database

- Version: 1
- Created: Mar. 30
- Authors: Yiruo Cheng
- Source: Server
- Actors: Interaction
- Goal: Store the registration information of user
- Summary: Add User ID, Add password, Add related e-mail
- Trigger: The end user selects the "Register" option
- Frequency: 
- Precondition: The application is open and running
- Postconditions: The user personal information is stored in the database

![](https://doc.ciel.pro/uploads/330b3aef93b0cd2a1c8ba5402.png)

#### Basic Flow

| Actor | System |
| ----- | ------ |
| From the Interaction menu, the end user selects the "Register" option | |
| | User ID, password and related e-mail are transported to the database by the server |
| | Database store the user ID, password and related e-mail |
| The end user registered successfully | |


#### Alternative Flow

| Actor | System |
| ----- | ------ |
| From the Interaction menu, the end user selects the "Register" option | |
| | User ID, password and related e-mail are transported to the database by the server |
| | This e-mail has been registered |
| The end user registered unsuccessfully | |


### Case: Interaction wants to use user personal information to login in the database

- Version: 1
- Created: Mar. 30
- Authors: Yiruo Cheng
- Source: Server
- Actors: Interaction
- Goal: Check the user personal information and verify
- Summary: Add User ID, Add password, Add related e-mail
- Trigger: The end user selects the "Login" option
- Frequency: 
- Precondition: The application is open and running and the user personal information has been stored in the database
- Postconditions: Interaction dispalys a feedback for successful login

#### Basic Flow

| Actor | System |
| ----- | ------ |
| Interaction wants to use user personal information to login | |
| | User ID, password and related e-mail are transported to the database by the server |
| | Find the User ID, and check  the corresponding password. |
| | Find the User ID and the password is correct. |
| Interaction dispalys a feedback for successful login | |


#### Alternative Flow

| Actor | System |
| ----- | ------ |
| Interaction wants to use user personal information to login | |
| | User ID, password and related e-mail are transported to the database by the server |
| | Find the User ID, and check  the corresponding password |
| | Find the User ID and the password is wrong |
| Interaction dispalys a feedback for unsuccessful login | |

### Case: Interaction wants to change user personal information in the database

- Version: 1
- Created: Mar. 30
- Authors: Yiruo Cheng
- Source: Server
- Actors: Interaction
- Goal: Change the user personal information 
- Summary: Change the password and the related e-mail
- Trigger: The end user selects the "Change" option
- Frequency: 
- Precondition: The application is open and running, and the user personal information has been stored in the database
- Postconditions: Interaction dispalys a feedback for successful change and the changed user information is stored in the database

![](https://doc.ciel.pro/uploads/330b3aef93b0cd2a1c8ba5406.png)

#### Basic Flow

| Actor | System |
| ----- | ------ |
| The end user selects the "Change" option | |
| The end user input the original password and the new word twice | |
| The end user clicks the "yes" button | |
| The interaction check whether the two new password is the same | |
| | User ID, original password and  new password are transported to the database by the server |
| | Find the User ID, and check  wheter the original password is correct |
| | Change the password in the database |
| Interaction dispalys a feedback for successful change | |


#### Alternative Flow

| Actor | System |
| ----- | ------ |
| The end user selects the "Change" option | |
| The end user input the original password and the new word twice | |
| The end user clicks the "yes" button | |
| The interaction check whether the two new password is the same | |
| | User ID, original password and  new password are transported to the database by the server |
| | Find the User ID, and check  wheter the original password is wrong |
| Interaction dispalys a feedback for unsuccessful change | |

<!-- Happy Family (DB) ~ Algorithm -->

### Case: Algorithm Wants to Save the Algorithm model in Binary form

- Version: 1
- Created: Mar. 30
- Authors: Xiangping Deng
- Source: Server
- Actors: Algorithm
- Goal: The algorithm wants to store their algorithm model in database in order to use it to predict the action of users
- Summary: 
- Trigger: 
- Frequency: 
- Precondition: Algorithm has trained their model
- Postconditions: The algorithm model has been stored in the database

#### Basic Flow

| Actor | System |
| ----- | ------ |
| Algorithm send the model in binary to the Server | |
| | Server sends the model to Database |
| | Database stores it |


#### Alternative Flow

| Actor | System |
| ----- | ------ |
| Algorithm send the model in binary to the Server | |
| | Server sends the model to Database |
| | Incomplete or incorrect information in the model file |
| | The database stores and specially labels it |


### Case: Algorithm Wants to Save Relevant Datasets

- Version: 1
- Created: Mar. 30
- Authors: Xiangping Deng
- Source: Server
- Actors: Algorithm
- Goal: The algorithm wants to store the datasets and results of the train in the database
- Summary: 
- Trigger: 
- Frequency: 
- Precondition: Algorithm has trained their model
- Postconditions: The database has stored the datasets and the results

#### Basic Flow

| Actor | System |
| ----- | ------ |
| Algorithm send the model in binary to the Server | |
| | Database stores the datasets and results in database |
| | Algorithm gets the relevant data from the database to train the model |
| | The model has runed |
| | Algorithm sends the results to Server |
| | Server sends the results to database |
| | Database stores it |


#### Alternative Flow

| Actor | System |
| ----- | ------ |
| Algorithm send the model in binary to the Server | |
| | Database stores the datasets and results in database |
| | Algorithm gets the relevant data from the database to train the model |
| | The model has runed |
| | Algorithm sends the results to Server |
| | Server sends the results to database |
| | Incomplete or incorrect information in the results |
| | Database stores and specially labels it |


### Case: Algorithm Wants to Save the Results of trained sensor data

- Version: 1
- Created: Mar. 30
- Authors: Xiangping Deng
- Source: Server
- Actors: Algorithm
- Goal: The algorithm wants to store the results of the sensor data from Sever in the database
- Summary: 
- Trigger: 
- Frequency: 
- Precondition: Database has stored the sensor data, and Algorithm has got the sensor data, trained their model, and run the sensor data in their model
- Postconditions: The database has stored the results

#### Basic Flow

| Actor | System |
| ----- | ------ |
| Algorithm | |
| | Algorithm sends the results to the database by the server |
| | Database stores it |


#### Alternative Flow

| Actor | System |
| ----- | ------ |
| Algorithm | |
| | Algorithm sends the results to the database by the server |
| | Incomplete or incorrect information in the results |
| | Database stores and specially labels it |


### Case: Algorithm Wants to Save the performance metrics of the Algorithm model

- Version: 1
- Created: Mar. 30
- Authors: Xiangping Deng
- Source: Server
- Actors: Algorithm
- Goal: The algorithm wants to store the performance metrics of the Algorithm model in database
- Summary: 
- Trigger: 
- Frequency: 
- Precondition: Algorithm has trained their model and run the sensor data in their model
- Postconditions: The database has stored the performance metrics of the Algorithm model

#### Basic Flow

| Actor | System |
| ----- | ------ |
| Algorithm | |
| | Algorithm has run the model |
| | Database stores it |
| | Algorithm sends the performance metrics to Server |
| | Server sends the performance metrics to database |
| | Database stores it |


#### Alternative Flow

| Actor | System |
| ----- | ------ |
| Algorithm | |
| | Algorithm has run the model |
| | Database stores it |
| | Algorithm sends the performance metrics to Server |
| | Server sends the performance metrics to database |
| | Incomplete or incorrect information in the results |
| | Database stores and specially labels it |
