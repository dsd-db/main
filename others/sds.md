


# Software Design Specification (SDS)

Revision History: 



| Date      | Author | Description |
| ----      | ------ | ----------- |
| Apr 7     | XU xiaoquan | Converted the template |
| Apr 11    | ZHOU wenhui, ZHU wenxuan, HUA cong | Provide the SDS of Sever Module2 |
| Apr 10-16 | CHENG weibin, TANG haotian | Provide the SDS of Interface Module2 |
| Apr 16    | DENG xiangping, BAI xiaoyang |Provide the SDS of Database Module1  |
| Apr 11,16 | DONG jin, WEN xueru | Provide the SDS of Algorithm Module2 |
| Apr 12    | GUO siqi | Provide the SDS of Algorithm Module1 |
| Apr 12    | DONG chunlai, TAN zhikang | Provide the SDS of Interface Module1 |
| Apr 14    | LIU yuxuan | Provide the SDS of Database Module2 |
| Apr 14    | ZHAO yiyuan | Provide the SDS of Server Module1 |
| Apr 16-19 | ZHAO yiyuan, DENG xiangping, CHENG yiruo | Integrate the documentation |


[toc]

## Introduction
### Intended Audience and Purpose
&emsp;&emsp;The document is intended to show the system design content to the customers and provide design information for developers and testers.


### How to use the document

&emsp;&emsp;The document is organized as follows:

- show the system design of every module in this project，and each module will be shown in detail 
- show the module interface design of every model
- show detailed design through sequence diagram 
  
  

## System Design
### Server
#### Context

- The server module is divided in two part. One part is the device server to play a role of controller on device and is responsible of connecting to the web server and upload both motion data and model data. The other part is web server on remote real server. It serve as the controller to coordinate database module and algorithm module and respond to the requests from interface module.

- The server module is planned to develop with java and connect to other module
- The module is planned to develop and test on IDEA.
- the module is planned to use the framework of spring boot to develop back-end part.

#### Design Pattern
- The whole system is designed as a Browser/Server structure, the interface is provided on web browser and the business is solved on web server.

- The system is planned to have a design pattern of MVC, which has the part of model, controller and view. The server module paly a role of controller and is served to connect other modules.

#### Architecture
##### Component Diagram
- version 1.0

![](https://doc.ciel.pro/uploads/330b3aef93b0cd2a1c8ba5463.png)


- version 2.0

 ![](https://doc.ciel.pro/uploads/330b3aef93b0cd2a1c8ba5464.png)


  





##### Deploy Diagram

![](https://doc.ciel.pro/uploads/330b3aef93b0cd2a1c8ba5465.png)

### Interaction
#### Context
&emsp;&emsp;The system is to be based on the **Browser/Server** architecture, with a web app as the front-end and a server as the backend. Thus, our software is **cross-platform** and **operating-system-irrelevant**.
&emsp;&emsp;**HTML**, **CSS** and **JavaScript** are the main languages used to construct the **interaction** module of the system. Furthermore, for the convenience of the developing process, we take advantage of JavaScript framework **JQuery** (may also with Vue), together with python web app framework **Flask** to render html templates.


#### Design Pattern
This system is based on B/S architecture.
#### Architecture
##### Component Diagram
![](https://doc.ciel.pro/uploads/330b3aef93b0cd2a1c8ba5479.png)
![](https://doc.ciel.pro/uploads/330b3aef93b0cd2a1c8ba547a.png)



### Database
#### Component diagram
![](https://doc.ciel.pro/uploads/330b3aef93b0cd2a1c8ba547e.png)

### Algorithm
#### Architecture
##### Component Diagram
![](https://doc.ciel.pro/uploads/330b3aef93b0cd2a1c8ba5472.png)

##### Deploy Diagram
![](https://doc.ciel.pro/uploads/330b3aef93b0cd2a1c8ba5471.png)







## Module Interface Design
### Server
#### Cloud Side
On the cloud platform, the server module provides API in RESTful flavor to the interaction module. The API is provided via HTTPS. 

##### Authentication

All device-related API requires device ticket authentication or administrator authentication. If the authentication is not valid, all APIs may return a 401.

The device ticket authentication is performed by a cloud-signed time stamp, then signed with the device key, which is signed by the cloud key. To request a cloud-signed time stamp, use

```
GET /timestamp
```

will generate a signed timestamp consists a Unix timestamp, a colon, and a server signature. For example:

```
1650375337:6bce5953a9506d6c14f2522fd6228afbee394da3
```

Send this timestamp to the device's `/ticket?ts=` API to get the device ticket, and send this ticket as an `Authorization` header in every request.

The administrator authentication procedure is described in a later section.


##### Device Management
All device management API are base at `/device/<uuid>`, the `uuid` is the one in `GET /` of device API. If the UUID is not a valid UUIDv4, These API return 400.

```
POST /device/<uuid>/email
```

Sets the contact email.

The request must be of type `application/json`. Example request:

```
{
	"email": "t@t.tt"
}
```

The email The email must be of right form and at maximum 254 characters.

Returns 200 always.

```
GET /device/<uuid>/email
```

Gets the contact email.

The response is of type `application/json`. Example response:

```
{
	"email": "t@t.tt"
}
```

Returns 404 if not set, 200 otherwise.

```
DELETE /device/<uuid>/email
```

Clears the contact email setting.

Returns 200 always.

```
HEAD /device/<uuid>/calibration
Check if calibration available
req: none
auth: device ticket
resp: 200 / 403 / 404
```

Checks whether calibration data available on server.

Returns 200 if data found, 404 otherwise.

```
PUT /device/<uuid>/calibration
Upload calibration
req: zip_file
auth: device sign header
resp: 200 / 403 / 400
```

Upload new calibration data to the cloud platform.

The request must have a valid `Signature` header passed from the device.

The response should be of type `multipart/form-data` with a file field `calibration`, the file must be of type `application`.

Returns 200 if succeed, 400 if the signature is not valid.

```
HEAD /device/<uuid>/model
req: none
auth: device ticket
resp: 200
header: Last-Modified if calibrated
```
```
GET /device/<uuid>/model
req: none
auth: device ticket
resp: file
auth: ca sign header
```
##### Administration

###### Restricted Device Management

First, several device management APIs are available to administrators only. Please note that the API above are also available to administrators without a device ticket.

```
GET /device/<uuid>/calibration
```

Download the calibration data from the cloud.

The response is of type `application/x-tar+gzip`.

Returns 404 if there's currently no data collected, 200 otherwise.

```
PUT /device/<uuid>/model
```

Upload a new model to the cloud. Please note the model is not deployed to the device until the user chooses to.

The request should be of type `multipart/form-data` with a file field `model`.

Returns 200 always.

```
DELETE /device/<uuid>
```

Deletes everything of the specified device from the cloud, and selectively prohibits its future use of the cloud platform.

The request must be of type `application/json`. Example request:

```
{
    "ban": true // disable cloud functionalities for this device
}
```

Returns 200 always.

###### Authentication

To log in to the current session, use

```
POST /session
```

The request must be of type `application/json`. Example request:

```
{
    "username": "UserName",
    "password": "PaSSw0Rd!"
}
```

Returns 200 if logged in successfully.

To log out, use

```
DELETE /session
```

Returns 200 always.

###### Base Model Management

```
PUT /model/base
```

Upload a model to the cloud, and set it to be the default model for users without calibration.

The request should be of type `multipart/form-data` with a file field `model`.

Returns 200 always.
##### Device Side
On the embedded platform, the server module provides the necessary API in RESTful flavour to the interaction module. The API is provided via HTTP, nested in Bluetooth. As the end-user controls the pairing procedure, the access to API itself is sufficient as client authentication.

```
HEAD /
```

Do nothing but return `200 OK` to confirm the link is established.

```
GET /
```

Provides the client with status information of the device.

The response is of type `application/json`.

Example response with comments:

```
{
    "id": "00000000-0000-0000-0000-000000000000", // string, the device UUID
    "battery": 90, // int, percentage of battery
    "charging": true, // bool, true if power connected
    "prediction": "walk", // string, the current detected motion
}
```

Returns 200 always.

```
GET /ticket?ts=<server_timestamp>
```

Obtain a signed device ticket.

The `server_timestamp` is from the `/timestamp` API of the cloud platform.

If the timestamp is of the right shape, the device signs it with the device key to creating and returns a device ticket. 

Returns 400 if the timestamp is missing or malformed, 200 otherwise.

```
GET /model
```

Download the current model from the device. This API is for debugging only.

The response is of type `application/octet-stream`.

Returns 404 if there's currently no model, 200 otherwise.

```
PUT /model
```

Upload a new model to the device.

The request must have a valid `Signature` header passed from the server.

The request should be of type `multipart/form-data` with a file field `model`.

Returns 200 if succeeds, or 400 if the signature is not valid.

```
HEAD /calibration/pending
```

Get metadata of pending calibrations.

The response is of type `application/json`.

Example response with comments:

```
[
    {
        "name": "walk", // the motion name, [a-z]+
        "duration": 20, // the duration of recording requested
        "display": "walk", // the displayed name of motion
        "desc": "Please walk on a firm and level ground" // the displayed description of motion
    },
    // .....
]
```

If all calibrations are finished, returns `[]`.

Returns 200 always.

```
POST /calibration/<motion>
```

Initialize a new calibration data recording.

The `motion` should be from the request above. 

Returns 409 if the previous calibration is not finished, 400 if the motion name is invalid, 200 otherwise and the data recording is started instantly.

```
GET /calibration
```

Acquire a pack of all current calibration data, signed with the device key.

The response is of type `application/x-tar+gzip`.

The response will have a `Signature` header to be passed to the cloud platform.

Returns 404 if no data is collected, 200 otherwise.

```
DELETE /calibration
```

Clears local calibration data.

Returns 200 always.


### Interaction
| interface name | function 
| ------------- | -------- | 
| Data accessCloudServer(string type)|  Get data from cloud server|
| int accessCloundServer(string type,Data data)|Upload Data to cloud server        | 
| Data accessLocalServer(string type)|  Get data from local server| 
| int accessLocalServer(string type,Data data)| Upload Data to local server| 
|displayData(string type,Data &data)|Display data on the web interface|
:::	success
Type in these interfaces means that if you want to implement specific function,then you make the type specific value.Detailed introduction is in the detailed design.

:::

### Database
#### cloud slide
The cloud side of the database module provides a package named `db`, with 3 module `admin`, `device` and `model` in it.

##### `db.admin`

```
db.admin.add(username: string, password: string): bool
```

Add an administrator account with the specified username and password. The strings must be non-empty, the username must contains only `[A-Za-z0-9_]`.

Returns `True` if succeed, `False` if the username existed.

```
db.admin.check(username: string, password: string): bool
```

Check if the given credential is an valid administrator account.

Returns `True` if the credential is valid, `False` otherwise.

```
db.admin.remove(username: string): None
```

Removes the administrator with the specified username.

Returns `None` always.

##### `db.device`

```
db.device.get(uuid: string, create: bool=False): db.device.Device
```

Get the `db.device.Device` object of the device with specified UUID. The UUID must be a valid UUIDv4.

If the `create` is set to `True`, the device entry is created and returned if not found.

Returns a `db.device.Device` instance if the device is found or created, `None` otherwise.

```
db.device.remove(uuid: string): None
```

Delete everything about the device with specified UUID.

Returns `None` always.

##### `db.device.Device`

```
db.device.Device.banned: bool
```

Indicate if the device is banned from the cloud services.

Defaults to `False`.

```
db.device.Device.email: string
```

The device's contact email, if exists. Support at least 254 characters, `ValueError` should be raised if exceeded.

Defaults to `None`.

```
db.device.Device.model: string
```

The path of the device's model file, if exists. Must be an absolute path.

On assignment, it's expected to copy the file specified into the database, rather than just changing the path. When `None` is assigned, delete the model.

Defaults to `None`.

```

db.device.Device.calibration: string
```

The path of the device's calibration data directory, if exists, with some `.csv` motion data files named with the motion it recorded. Must be an absolute path.

On assignment, it's expected to copy the files in the directory specified into the database, rather than just changing the path. When `None` is assigned, delete the data.

Defaults to `None`.

##### `db.model`

```
db.model.getBase(): string
```

Get the path of the base model.

Returns an absolute path if set, `None` otherwise.

```
db.model.setBase(path: string): None
```

Set the path of the base model. Must be an absolute path.

Returns `None` always.

On the embedded platform, the database module provides sensor data sampling to the server module, then to the algorithm module. Use process call directly for more flexibility.



### Algorithm
#### Services Provided



| Service                                                      | Provided  By | Tested  By |
| ------------------------------------------------------------ | ------------ | ---------- |
| 1.Algorithm can train the general model                         | train        | T1         |
| 2.Algorithm can train the personalized model for specific users | train        | T2         |
| 3.Algorithm can predict the next motion state                   | predict      | T3         |



 

#### Access Method 

| **Access   Method**          | **Parameter   name**                     | **Parameter   type** | **Description**                                              | **Exceptions** | **Map to services** |
| ---------------------------- | ---------------------------------------- | -------------------- | ------------------------------------------------------------ | -------------- | ------------------- |
| get_model_instance_for_train | haper_params,[params]                    | Dict,[Dict]          | haper_params can control some data in the training process by changing values such as learning rate. |                | 1,2                 |
| get_data                     | path_data                                | String               | path_data provides the location of data and this method can get original data. |                | 1,2                 |
| get_real_time_data           | socket                                   | Socket               | socket continually provide real-time data                    |                | 3                   |
| process_data                 | original_data                            | Dataframe            | when training, data is [n,1800], n is uncertain; when predicting, data is [1,n], containg real-time data for 5 seconds. |                | 1,2,3               |
| get_model_params             | path_params                              | String               | path_params provide the location for one model's params.     |                | 2,3                 |
| save_model_params            | trained_model_params, path_to_save_model | Dict, String         | after the model has been trained, the params will be saved   |                | 1,2                 |
| save_predict_result          | next_motion_state                        | Integer              | next_motion_state will be one of 0,1,2,3,4,5                 |                | 3                   |

 

#### Access Method Effects

| **Access   Method**          | **Description**                                              |
| ---------------------------- | ------------------------------------------------------------ |
| get_model_instance_for_train | when training or predicting, one model will be created.      |
| get_data                     | before training, original data will be achieved by file.     |
| get_real_time_data           | before predicting, original data will be achieved by socket. |
| process_data                 | after get original data, this method will prepocessing the data and then generate data for training or predicting, the type of data is tensor. |
| get_model_params             | before geting the instance of model, params may be needed.   |
| save_model_params            | after training process, the params need to be saved.         |
| save_predict_result          | after predicting process, the result need to be saved.       |


## Detailed Design
### Server
sequence diagram

- device connection and user login

![](https://doc.ciel.pro/uploads/330b3aef93b0cd2a1c8ba5466.png)


  

- record data and update model

![](https://doc.ciel.pro/uploads/330b3aef93b0cd2a1c8ba5467.png)


  

  

- predict and display results

![](https://doc.ciel.pro/uploads/330b3aef93b0cd2a1c8ba5468.png)

### Interaction
#### Sequence diagram
![](https://doc.ciel.pro/uploads/330b3aef93b0cd2a1c8ba547b.png)




### Database
#### E-R diagram
![](https://doc.ciel.pro/uploads/330b3aef93b0cd2a1c8ba547c.png)
#### MySql Table
![](https://doc.ciel.pro/uploads/330b3aef93b0cd2a1c8ba547d.png)

### Algorithm
![](https://doc.ciel.pro/uploads/330b3aef93b0cd2a1c8ba546a.png)






## Appendices

### Definitions and acronyms

#### Definitions

| Keyword | Definitions |
| ------- | ----------- |
|         |             |
|         |             |
|         |             |

#### Acronyms and abbreviations
| Acronym or Abbreviation | Definitions |
| ----------------------- | ----------- |
|                         |             |
|                         |             |
|                         |             |

### References
