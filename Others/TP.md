# Testing Report

## Revision History

<style>#rev +table td:nth-child(1) { white-space: nowrap }</style>
<div id="rev"></div>

| Date   | Author | Description |
| ------ | ------ | ----------- |
| Apr 20 | Ciel ZHAO | Converted the template |
| May 02 | Xiaoquan Xu | Finished the unit test of Pigeonhole |
| May 03 | Haozhen Zhang, Xiaoquan Xu | Merged the unit test of Serendipity |
| May 04 | Xiaoquan Xu, Alex Xu, Zeqi Chen, Haozhen Zhang, Yu Bai| Edited for the problems encountered during integration|
| May 15 | Weibin Cheng | unit testing case of Spirits |
| May 20 | Xiaoquan Xu | Made integration testing plans |
| May 26 | Xiaoquan Xu | Update the unit test of Pigeonhole in version 2.0 |
| May 28 | Cong Hua, Wenxuan Zhu | Update the unit test of Joker in version 2.0 |

[toc]

## Introduction

### Intended Audience and Purpose

This document provides the testing method and results, corresponding to the requirement from the customer. It consists of 3 parts, the testing cases, the test plan, and the testing results.

### How to use the document

You may refer to the content section for the structure of the document, in which Sec. Testing Cases collect the unit and module test information from each team; Sec. Testing Plan shows the steps and expected results of the integration test; Sec. Results describes the real world data out of the test, and the correspondence to the requirements.

## Unit Testing Cases

<!--
In this section, each team propose their testing cases on unit and module testing.
-->

### Pigeonhole

#### Cloud Authentication

##### Test 1.Request a cloud-signed time stamp

- [x] Use `GET /api/timestamp` to generate a signed timestamp.

> Like `1650983735:6bce5953a9506d6c14f2522fd6228afbee394da3
`
- [x] Two requests at different time should return different values.

:::info
If two requests were sent within a second, it will return the same value.
:::

- [x] If two requests are sent to the same server, the part of their timestamp after the colon should be the same.
- [x] A signed timestamp should be successfully split by a colon.

> For example: `1650375337:6bce5953a9506d6c14f2522fd6228afbee394da3`

- [x] The signed timestamp should be valid for only 1 hour.
- [x] It should always return 200.

##### Test 14.Log in to the current session

- [x] Use `POST /api/session` to log in a session as an administrator.

> The request must be of type `application/json`. Example request:
> ```
> {
>     "username": "UserName",
>     "password": "PaSSw0Rd!"
> }
> ```

- [x] If the request is in invalid form, it should return 400.
- [x] If the username or the password is wrong，it should return 403 and do nothing.
- [x] If the username and the password match correctly, it should return 200 and set a new session.

##### Test 15.Log out

- [x] Use `DELETE /api/session` to log out.
- [x] If logging out without logging in, it should do nothing.
- [x] It should always return 200.

#### Cloud Device Management API

##### Test 2.Set the contact email

- [x] After sending `POST /api/device/<uuid>/email`, the contact email should be set.
- [x] If set email for a device which has already been set, the contact email should be updated.
- [ ] (NEW) The `UUID` SHOULD be of any version, except the Nil `UUID`. If the `UUID` is not valid, it should return 404.

> UUIDv4 such like `11bf5b37-e0b8-42e0-8dcf-dc8c4aefc000`

:::success
~~It returns 404~~
:::

> The request must be of type `application/json`. Example request:
> ```
> {
>     "email": "t@t.tt"
> }
> ```

> The email must be of the right form and a maximum of 254 characters.

- [x] If either the form of request or `email` is invalid, it should return 400.

> Although the domain name `c.dev` does not exist, `pigeonhoe@c.dev` is a valid email here. 

> `hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhole11111111111111@ciel.dev
` is not valid because the number of characters before `@` exceeds 64.

- [x] If both the forms of request and `email` is valid, it should return 200.

> `pigeonhole@ciel.dev` and `t@t.tt` are valid

##### Test 3.Get the contact email

- [x] After sending `GET /api/device/<uuid>/email`, the contact email should be get.
- [x] If the contact email was not set, it should return 404.
- [x] If the contact email was get, it should return 200.
- [x] The response should be of the same right form as the request in Test 2.

##### Test 4.Clear the contact email setting

- [x] After sending `DELETE /api/device/<uuid>/email`, the contact email setting should be cleared.
- [x] It should always return 200. Even if the contact email was not set.

##### Test 11.Download the calibration data from the cloud

- [x] After sending `GET /api/device/<uuid>/calibration`, the calibration data from the cloud should be downloaded.
- [x] If no data is collected, it should return 404.
- [x] If downloaded successfully, it should return 200.
- [x] The response should be of type `application/x-tar+gzip`.
- [x] If the request is sent by device but not manager, it should return 403.

##### Test 5.Check whether calibration data is available

- [x] Send `HEAD /api/device/<uuid>/calibration` to check.
- [x] If the data is not found, it should return 404.
- [x] (NEW) If the data is found available, it should return 200 for ADMIN but 403 for device user.

##### Test 6.Upload new calibration data to the cloud platform

- [x] After sending `PUT /api/device/<uuid>/calibration`, the new calibration data should be uploaded.

> The request should be of type `multipart/form-data` with a file field `caxibration`, the file must be of type `application/x-tar+gzip`.

- [x] If the request is not valid, it should return 400.
- [x] If the `Signature` is not valid, it should return 400.
- [x] If the data was uploaded successfully, it should return 200.

##### Test 7.Clear calibration data from the cloud

- [x] After sending `DELETE /api/device/<uuid>/calibration`, the calibration data from the cloud should be cleared.
- [x] It should always return 200.

##### (Abandoned) Test 8.Check the version of the device model on the server

:::warning
What if called?
:::

- [x] Send `HEAD /api/device/<uuid>/model` to check.
- [x] If the device model does exist, the response should contain a `Last-Modified` header of the device model.
- [x] If the device model does not exist, the response should not contain `Last-Modified`. But the base version is still available to download.
- [x] The response should contain a `Content-Length` header to indicate the size of model.
- [x] It should always return 200.

##### (Changed) Test 9.Acquire the device model of a specific algorithm

- [x] After sending `GET /api/device/<uuid>/model/<algo>`, the current version of the device model should be get, signed with the platform key.
- [x] If the device model does not exist, the base version should be provided.
- [x] The response should be of type `application/octet-stream`, with the following headers:

- `Signature` header to be passed to the device
- `Last-Modified` if and only if the device model exist
- `Content-Length` to indicate the size of model

- [x] It should always return 200.

##### (NEW) Test 26.Train the device model of a specific algorithm

- [x] Use `POST /api/device/<uuid>/model/<algo>` to train the device model of a specific algorithm with calibration data uploaded.
- [x] If the previous training is not finished yet, it will be terminated first before new training starts.
- [x] An email will be send to the device’s contact email (if set) when the training finishes. (Actually it will be a log on Server)
- [x] Returns 400 if the no calibration data available, 200 otherwise.

##### (Changed) Test 12.Upload the device model of a specific algorithm

- [x] After sending `PUT /api/device/<uuid>/model/<algo>`, a new model should be uploaded to the cloud.

> The request should be of type `multipart/form-data` with a file field `model`.

- [x] If the request is invalid, it should return 400.

:::warning
400 is not defined in Interface Specification 2.0
:::

- [x] If uploaded successfully, it should return 200.
- [x] If the request is sent by device but not manager, it should return 403.

##### (NEW) Test 27.Clear device model of a specific algorithm

- [x] Use `DELETE /api/device/<uuid>/model/<algo>` to clear the device model of a specific algorithm from the cloud.
- [x] Returns 200 always.

##### (Changed) Test 10.Clear device model of all algorithms

- [x] After sending `DELETE /api/device/<uuid>/model`, the device model of all algorithms from the cloud should be cleared.
- [x] It should always return 200.

##### (Changed) Test 13.Delete everything specified from the cloud

- [x] After sending `DELETE /api/device/<uuid>`, everything of the specified device from the cloud should be deleted.

> Changed in version 2.0: The ban parameter is deprecated.
> Changed in version 2.0: Now available to device user.

##### (Abandoned) Test 16.Set a default model to the cloud

- [x] After sending `PUT /model/base`, a model should be uploaded to the cloud to be set as the default model for users without calibration.
> The request should be of type `multipart/form-data` with a file field `model`.
- [x] If the request is invalid, it should return 400.
- [x] If uploaded successfully, it should return 200.

- [x] It should always return 200.

#### Cloud Model Management API

##### (NEW) Test 28.Get metadata of available algorithms

- [x] Use `GET /api/models` to get metadata of available algorithms.
- [x] The response SHOULD be of type `application/json`, and the same format of `algo.json` provided by the algorithm module.
- [x] Always return 200.

##### (NEW) Test 29.Acquire the base model of an algorithm

- [x] Use `GET /api/model/<algo>` to acquire the base model of an algorithm.
- [x] The response SHOULD be of type `application/octet-stream`.
- [x] Returns 200 always.

##### (NEW) Test 30.Update the base model of an algorithm

- [x] Admin can use `PUT /api/model/<algo>` to update the base model of an algorithm to be used as the default model for users without calibration.
- [x] If called by device users, it should return 401 or 403.
- [x] The request SHOULD be of type `multipart/form-data` with a file field `model`.
- [x] Returns 200 always.

#### Device API

##### Test 17.Confirm the link is established

:::info
return 404 NOT FOUND
:::

- [x] Use `HEAD /` to check authentication.
- [x] It should always return `200 OK` to confirm the link is established.

##### Test 18.Provide status information

- [x] Use `GET /` to provide the client with status information of the device.
- [x] The response should be of type `application/json`.

> Example response with comments:
> ```
> {
>     "id": "00000000-0000-0000-0000-000000000000", // string, the device UUID
>     "battery": 90, // int, percentage of battery
>     "charging": true, // bool, true if power connected
>     "prediction": "walk", // string, the current detected motion
> }
> ```

- [x] It should always return `200 OK` to confirm the link is established.

##### Test 19.Obtain a signed device ticket

- [x] After sending `GET /ticket?ts=<server_timestamp>`, if the timestamp is of the right shape, the device signs it with the device key to creating and returns a device ticket.

> The `server_timestamp` is from the `/timestamp` API of the cloud platform.

- [x] If the timestamp is missing or malformed, it should return 400.
- [x] If the timestamp is of the right shape, it should return 200.

##### Test 20.Download the current model from the device

- [x] After sending `GET /model`, the current model from the device should be downloaded.
- [x] This API is for debugging only，it should not be called by other procedures.
- [x] The response should be of type `application/octet-stream`.
- [x] If there’s currently no model, it should return 404.
- [x] If downloaded successfully, it should return 200.


##### Test 21.Upload a new model to the device

- [x] After sending `PUT /model`, a new model should be uploaded to the device.

>The request must have a valid `Signature` header passed from the server.
>The request should be of type `multipart/form-data` with a file field `model`.

- [x] If the signature is not valid, it should return 400.
- [x] If uploaded successfully, it should return 200.

##### Test 22.Get metadata of pending calibrations

- [x] Use `GET /calibration/pending` to get metadata of pending calibrations.
- [x] If all calibrations are finished, it should return `[]`.
- [x] The response should be of type `application/json`.

> Example response with comments:
> ```
> [
>     {
>         "name": "walk", // the motion name, [a-z]+
>         "duration": 20, // the duration of recording requested
>         "display": "walk", // the displayed name of motion
>         "desc": "Please walk on a firm and level ground" // the displayed description of motion
>     },
>     // .....
> ]
> ```

- [x] It should always return 200.

##### Test 23.Initialize a new calibration data recording

- [x] Use `POST /calibration/<motion>` to initialize a new calibration data recording.

> The `motion` should be from the request above.

- [x] If the motion name is invalid, it should return 400.
- [x] If the previous calibration is not finished, it should return 409.
- [x] If the data recording is able to be initialized, it should return 200 and start the process.

##### Test 24.Acquire all current calibration data

- [x] Use `GET /calibration` to acquire a pack of all current calibration data, signed with the device key.
- [x] The response should be of type `application/x-tar+gzip` and have a `Signature` header to be passed to the cloud platform.
- [x] If no data is collected, it should return 404.
- [x] If the request is satisfied, it should return 200.

##### Test 25.Clear local calibration data

- [x] After sending `DELETE /calibration`, the local calibration data should be cleared.
- [x] It should always return 200.


### Serendipity

1. **The end user gets started**
(1) Prerequisite
(2) Test Steps
a.Input the device ID
(3) Expected Result
a.Establishing a connection with the device successfully


2. **The end user gets started with wrong device ID**
(1) Prerequisite
(2) Test Steps
a.Input the wrong device ID
(3) Expected Result
a.The webpage prompts the device ID is wrong

3. **The end user set the correct contact e-mail**
(1) Prerequisite
a.The device is connected and the user enters the relevant webpage
(2) Test Steps
a.Input the correct e-mail and submit
b.Check if email is set up successfully
(3) Expected Result
a.The e-mail is set up normally
b.The webpage prompts the user e-mail has been successfully set up

4. **The end user set the wrong format e-mail**
(1) Prerequisite
a.The device is connected and the user enters the relevant webpage
(2) Test Steps
a.Input the wrong format e-mail and submit
b.Check if email is set up successfully
(3) Expected Result
a.The e-mail is NOT set up
b.The webpage prompts the user that the e-mail setting has failed and prompts a relevant error message

5. **The end user checks the contact e-mail**
(1) Prerequisite
a.The user enters the relevant webpage
(2) Test Steps
a.Enter the relevant webpage
b.Check if the e-mail is correct
(3) Expected Result
a.The webpage shows the correct e-mail normally

6. **The end user deletes the contact e-mail**
(1) Prerequisite
a.The user enters the relevant webpage
(2) Test Steps
a.Delete the contact e-mail
b.Check if the e-mail has been deleted
(3) Expected Result
a.The webpage prompts the contact e-mail is deleted successfully

5. **The end user deletes the contact e-mail before setting**
(1) Prerequisite
a.The user enters the relevant webpage
(2) Test Steps
a.Try to delete the contact e-mail
(3) Expected Result
a.The webpage prompts the contact e-mail has not been set up

6. **The end user checks the version of model on server**
(1) Prerequisite
a.The device is connected and the user enters the relevant webpage
(2) Test Steps
a.Check the model version
(3) Expected Result
a. The webpage shows the current model version according to server response

7. **The end user update the new model to device**
(1) Prerequisite
a.The device is connected and the user enters the relevant webpage
(2) Test Steps
a.Update(Upload) the model
(3) Expected Result
a.The webpage downloads and uploads the model successfully
b.The webpage prompts user update successfully

8. **The end user update the new model to device with exception**
(1) Prerequisite
a.The device is connected and the user enters the relevant webpage
(2) Test Steps
a.Update(Upload) the model
(3) Expected Result
a.The webpage prompts user update failed

8. **The end user delete the new model from cloud**
(1) Prerequisite
a.The device is connected and the user enters the relevant webpage
(2) Test Steps
a.Delete the model
(3) Expected Result
a.The server deletes the model from cloud
b.The webpage prompts user delete successfully

9. **The end user checks whether calibration data is available on the server**
(1) Prerequisite
a.The device is connected and the user enters the relevant webpage
(2) Test Steps
a.Enter the relevant webpage
(3) Expected Result
a.The webpage shows if the calibration data is available correctlly

10. **The end user upload the calibration data to the cloud**
(1) Prerequisite
a.The device is connected and the user enters the relevant webpage
(2) Test Steps
a.Upload the new calibration data
(3) Expected Result
a.The webpage prompts user upload successfully

11. **The end user upload the calibration data to the cloud  with exception**
(1) Prerequisite
a.The device is connected and the user enters the relevant webpage
(2) Test Steps
a.Upload the new calibration data
(3) Expected Result
a.The webpage prompts user upload failed and prompts the message

12. **The end user clears calibration data from the cloud**
(1) Prerequisite
a.The device is connected and the user enters the relevant webpage
(2) Test Steps
a.Clear all calibration data from the cloud
(3) Expected Result
a.The server clear the data successfully
b.The webpage prompts user clear successfully

13. **The end user collects and gets the calibration data**
(1) Prerequisite
a.The device is connected and the user enters the relevant webpage
(2) Test Steps
a.Enter the relevant webpage
b.Choose to start to collect data
(3) Expected Result
a.The webpage shows the guide during the calibration data collection
b.The webpage prompts users when collection finishes.

13. **The end user clears the local calibration data**
(1) Prerequisite
a.The device is connected and the user enters the relevant webpage
(2) Test Steps
a.Clear the local calibration data
(3) Expected Result
a.The webpage prompts user clear successfully

14. **The end user gets the device information from server**
(1) Prerequisite
a.The device is connected and the user enters the relevant webpage
(2) Test Steps
a.Enter the relevant webpage
(3) Expected Result
a.The webpage shows all information of device with real-time refresh

15. **The admin logs in**
(1) Prerequisite
(2) Test Steps
a.Input the login information and submit
(3) Expected Result
a.The webpage prompts the login information
b.The administrator function components are displayed

16. **The admin logs out**
(1) Prerequisite
a. The admin is logged in
(2) Test Steps
a.Input the login information and submit
(3) Expected Result
a.The administrator function components disappear
b.The webpage prompts logout successfully

17. **The admin clear or ban a device from cloud**
(1) Prerequisite
a. The admin is logged in and enters the relevant webpage
(2) Test Steps
a.Set whether ban the device
b.Clear the device
(3) Expected Result
a.The webpage prompts the user the response of server

18. **The admin upload the (Base) model to the cloud**
(1) Prerequisite
a. The admin is logged in and enters the relevant webpage
(2) Test Steps
a.Select the local model file
b.Upload the model
(3) Expected Result
a.Model is selected and uploaded to the cloud
b.The webpage prompts the response of server

19. **The admin download the calibration data from the cloud**
(1) Prerequisite
a. The admin is logged in and enters the relevant webpage
(2) Test Steps
a.Download the calibration data from the cloud
(3) Expected Result
a.The data is downloaded to the local successfully

### Jokers

#### Cloud  API

##### testcase1. Request a cloud-signed time stamp

- Use `GET /api/timestamp` to get a signed timestamp. The cloud-signed timestamp consist of colon-separated Unix timestamp and a server signature

>example: 1650375337:6bce5953a9506d6c14f2522fd6228afbee394da3

- Two requests at different time should return different values.

- If two requests are sent to the same server, the server signature should be the same.
- The signed timestamp is valid for only 1 hour.
- Always return 200.

##### testcase2. Log in to the current session

- Use `POST /api/session` to log in a session as an administrator
- The request should be of type `application/json`

```
{
	"username": jokers,
	"password": dsd_jokers
}
```

- If the username or the password is wrong, it should return 403 
- If the username and the password match correctly, it should return 200 and set a new session

##### testcase3. Log out

- Use `DELETE /api/session` to log out
- It should always return 200

##### testcase4. Set the contact email

- Send `POST /api/device/<uuid>/email` to set contact email.

- If the email has already been set, the request could update a new device's email .

- The email should be of the right form and a maximum of 254 characters

> Valid email : `1102106753@qq.com`

- The email should be the Any form of request or `email` is invalid will return 400.
- If both the forms of request and `email` is valid, It will return 200 always.

##### testcase5. Get the contact email

- Send `GET /api/device/<uuid>/email` to get contact email.

- The response should be of type `application/json`. For example:

  ```
  {
  	"email":"1102106753@qq.com"
  }
  ```

- If the contact email has not been set, it would return 404.

- If the contact email was got successfully,  it would return 200.

##### testcase6. Clear the contact email 

- Send `DELETE /api/device/<uuid>/email`to clear the contact email.

- Always return 200.

##### testcase7. Download the calibration data

- Send `GET /api/device/<uuid>/calibration` to download the calibration data.
- The response should be of type `application/x-tar+gzip` 
- If there is no data collected or the uuvid is not v4, it should return 404
- If the request is not sent by admins, it should return 401
- If downloaded successfully, it should return 200.

##### testcase8. Check whether calibration is available or not

- Send `HEAD /api/device/<uuid>/calibration` to check whether calibration is available.
- If the request is sent by the device user  without a valid `Signature`, it should return 401
- If there is no data collected or the uuid is not v4, it should return 404
- If calibration is available, it should return 200.

##### testcase9. Upload calibration data

- Send `PUT /api/device/<uuid>/calibration` to upload the new calibration data.

- The request should be of type `multipart/form-data`, the file must be of type `application/x-tar+gzip`.
- If the `Signature` or the form of request is not valid, it should return 400.

- Data upload successfully, return 200.

##### testcase10. Clear calibration data 

- Send `DELETE /api/device/<uuid>/calibration` to clear the calibration data.

- Always return 200.

##### testcase11. Download device model

- Sending `GET /api/device/<uuid>/model/<algo>` to get the current version of the device model.

- Acquire the device model of a specific algorithm, signed with the platform key. If the device model does not exist, the base version would be provided.

- If the request is sent by the device user without a valid `Signature`, it should return 401

- If the algorithm is not found or the base model is not provided or the uuid is not valid, it should return 404

- The response should be of type `application/octet-stream`. 

>`response.set_header('Content-Type', 'application/octet-stream')`
>`response.set_header('Signature', timestamp_solution.get_signature())`

- If downloaded successfully, it should return 200.

##### testcase12. Check device model's version

- Send `HEAD /api/device/<uuid>/model/<algo>` to check.

- If the request is sent by the device user  without a valid `Signature`, it should return 401

- If the algorithm is not found or the uuid is not valid, it should return 404

- The response contains a `Last-Modified` header and a `Content-Length` header.

- If checked successfully, it should return 200.  

##### testcase13. Upload  the device model of a specific algorithm

- Use `PUT /api/device/<uuid>/model/<algo>` to upload the device model for a specific algorithm. 
- If the request should be of type `multipart/form-data` with a file field `model`. 
- If the request is not sent by the admin, it should return 401.
- If the uuid is not valid or the algorithm is not found, it should return 404
- If the uploaded file does not exist, it should return 400.
- If the file was uploaded successfully, it should return 200.

##### testcase14. Train the device model of a specific algorithm

- Use `POST /api/device/<uuid>/model/<algo>` to train the device model of a specific algorithm with calibration data uploaded.
- If the request is sent by the device user without a valid `Signature`, it should return 401

- If the uuid is not valid or the algorithm is found, it should return 404.
- If no calibration data is available, it should return 400.
- If train the specific model successfully, return 200.

##### testcase15. Clear device model from the cloud

- Use `DELETE /api/device/<uuid>/model` to clear the device model of a all algorithm from the cloud.

- Always return 200.

##### testcase16. Clear everything of the specified device from the cloud

- Use ``DELETE /api/device/<uuid>`` to delete everything of the specified device from the cloud.
- Always return 200.

##### testcase17. Get metadata of available algorithms

- Use `GET /api/models` to get metadata of available algorithm
- The response should be of type `application/json`
- Always return 200

##### testcase18. Acquire the base model of an algorithm

- Use `GET /api/model/<algo>` to acquire the base model of an algorithm
- the response should be of type `application/octetstream`
- If the algorithm is not found, it should return 404.
- If the algorithm is got successfully, it should return 200.

##### testcase19. Update the base model of an algorithm 

- Use `PUT /api/model/<algo>` to update the base model of an algorithm to be used as the default model for users without calibration.
- The request should be of type `multipart/from-data` with a file field `model`
- If the request was not sent from admin, it should return 401
- If the algorithm was not found, it should return 404.
- If the uploaded file was None, it should return 400
- If the base model of an algorithm was uploaded successfully, it should return 200.

#### Device API

##### testcase20. Confirm the link is established

- Use `HEAD /` to check 
- Do nothing and return status code `200`  to confirm the link is established

##### testcase21. Provide status information

- Use `GET /` to provide the client with status information of the device
- The response is of type `application/json`.
- Returns 200 always to ensure that provide status information successfully

Example response with comments:

```cpp
status = {
        "id": "00000000-0000-0000-0000-000000000000",  # string, the device UUID
        "battery": 90,  # int, percentage of battery
        "charging": True,  # bool, true if power connected
        "algorithm":{
            "name": "lstm",
            "display": "LSTM",
			.....
        }
        "prediction": "walk",  # string, the current detected motion
    }
```

##### testcase22. Obtain a signed device ticket

- Use `GET /ticket?ts=<server_timestamp>` where the The `server_timestamp` is from the `Get /api/timestamp` API of the cloud platform.
- If the timestamp is of the right shape, the device SHOULD sign it with the device key to create and return a device ticket in plain text.
- Return 200 and a device ticket if the timestamp is of the right shape
- Returns 400 if the timestamp is missing or malformed

##### testcase23. Download the model from the device.

- Use `GET /model ` to download the current model from the device.
- The response is of type `application/octet-stream`.
- If there’s currently no model, return 404 
- If download the model successfully, return 200

##### testcase24. Upload a new model for a specific algorithm to the device.

- Use `PUT /model/<algo>` to upload a new model for a specific algorithm to the device
- The `<algo>` parameter should be the names in `GET /api/models` of  the cloud
- The request must have a valid `Signature` header passed from the server.
- The request should be of type `multipart/form-data` with a file field `model`.
- If the signature is not valid, return 400
- If upload the model to the device successfully, return 200

##### testcase25. Delete local model from device

- Use `DELETE /model` to delete local model from device
- Always return 200

##### testcase26. Get metadata of pending calibrations.

- Use `GET /calibration/pending` to get metadata of pending calibrations.
- The response is of type `application/json`.
- If all calibrations are finished, returns `[]`.
- If not finished, example response with comments

```cpp
[   
	{
        "name": "walk", // the motion name, [a-z]+
        "duration": 20, // the duration of recording requested
        "display": "walk", // the displayed name of motion
        "desc": "Please walk on a firm and level ground" // the displayed description of motion
    },
]
```

- Return 200 always

##### testcase27. Initialize a new calibration data recording

- Use `POST /calibration/<motion>` to initialize a new calibration data recording.
- The `motion` should be from the request above.
- If the previous calibration is not finished, returns 409
- If the motion name is invalid, return 400
- If the data recording is able to be initialized, return 200 and start the process

##### testcase28. Acquire all current calibration data

- Use `GET /calibration` to acquire a pack of current 

- The response is of type `application/x-tar+gzip`.
- The response will have a `Signature` header to be passed to the cloud platform.
- If no data is collected, return 404
- If data is collected successfully, return 200

##### testcase29. Clears local calibration data.

- Use `DELETE /calibration` to Clears local calibration data.
- Returns 200 always.


### Spirits
All test case below require a stable network connection in general
#### **GUI**
1. **Webpage Openability**
(1) Prerequisite
None
(2) Test Steps
a. Open (every) webpage [ckpt 1]
(3) Expected Result
a. The webpage can be opened in 1s[ckpt 1]
2. **Dimension Adaptability**
(1) Prerequisite
None
(2) Test Steps
a. Open (every) webpage [ckpt 1]
b. Resize the browser[ckpt 2]
(3) Expected Result 
a. The webpage is opened in 1s[ckpt 1]
b. The layout of the webpage adjust rationally to make the webpage looks normal under different dimension. [ckpt 2 ]
3. **Buttons&Hyperlinks Work as Expected**
(1) Prerequisite
None
(2) Test Steps
a. Open webpage [ckpt 1]
b. Click buttons&hyperlinks[ckpt 2]
(3) Expected Result
a. The webpage is opened in 1s[ckpt 1]
b. Buttons and hyperlinks work as expected, i.e. buttons work normally/link to correct subpages[ckpt 2]
#### **Admin Privileges**
3. **Admin log in---Normal**
(1) Prerequisite
None
(2) Test Steps
a. Open relavent webpage [ckpt 1]
b. Input login info [ckpt 2]
c. Login [ckpt 3]
(3) Expected Result
a. The webpage is opened in 1s normally [ckpt 1]
b. The login info can be input normally [ckpt 2]
c. The webpage redirect(200 succ.) or prompt wrong/mismatched usrname&passwd according to server response(403/Timeout: failed) [ckpt 3]
3. **Admin log in---Empty UserName**
(1) Prerequisite
None
(2) Test Steps
a. Open relavent webpage [ckpt 1]
b. Input password but leaves username to be empty[ckpt 2]
c. Try to log in
(3) Expected Result
a. The webpage is opened in 1s normally [ckpt 1]
b. The login info can be input normally [ckpt 2]
c. The login button is locked since empty username is not permitted, and prompt info is shown [ckpt 3]
8. **Admin log in---Empty Password**
(1) Prerequisite
None
(2) Test Steps
a. Open relavent webpage [ckpt 1]
b. Input username but leave password to be empty[ckpt 2]
c. Try to log in
(3) Expected Result
a. The webpage is opened in 1s normally [ckpt 1]
b. The login info can be input normally [ckpt 2]
c. The login button is locked since empty password is not permitted, and prompt info is shown [ckpt 3]
9. **Admin log out**
(1) Prerequisite
None
(2) Test Steps
a. Open relavent webpage [ckpt 1]
b. Logout [ckpt 2]
(3) Expected Result
a. The webpage is opened in 1s normally [ckpt 1]
b. The webpage redirect and prompt logout succeful(200 succ.) or do nothing(Timeout: failed) [ckpt 2]
1. **Admin downloads the calibration data from the cloud---Normal**
(1) Prerequisite
a. The admin is logged in
(2) Test Steps
a. Open relavent webpage [ckpt 1]
b. Input device uuid [ckpt 2]
c. Download calibration data [ckpt 3]
d. Check if the calibration data is downloaded successfully [ckpt 4]
(3) Expected Result
a. The webpage is opened in 1s normally [ckpt 1]
b. The uuid can be input normally, and uuid format is checked, if is invalid then download button is locked [ckpt 2]
c. The webpage prompts the user download starts [ckpt 3]
d. The calibration data is downloaded. [ckpt 4]
2. **Admin downloads the calibration data from the cloud---Exception(no calibration data(404), server respond timeout, network broke halfway, e.t.c.)**
(1) Prerequisite
a. The admin is logged in
(2) Test Steps
a. Open relavent webpage [ckpt 1]
b. Input device uuid [ckpt 2]
c. Download calibration data [ckpt 3]
(3) Expected Result
a. The webpage is opened in 1s normally [ckpt 1]
b. The uuid can be input normally, and uuid format is checked, if it's invalid then download button is locked [ckpt 2]
b. The webpage prompts user error according to server response[ckpt 3]
3. **Admin uploads a new model to the cloud---Normal**
(1) Prerequisite
a. The admin is logged in
(2) Test Steps
a. Open relavent webpage [ckpt 1]
b. Input device uuid [ckpt 2]
c. Upload calibration data [ckpt 3]
(3) Expected Result
a. The webpage is opened in 1s normally [ckpt 1]
b. The uuid can be input normally, and uuid format is checked, if it's invalid then upload button is locked [ckpt 2]
c. The webpage prompts the user upload starts [ckpt 3]
4. **Admin uploads a new model to the cloud---Exception(server respond timeout, network broke halfway, e.t.c.)**
(1) Prerequisite
a. The admin is logged in
(2) Test Steps
a. Open relavent webpage [ckpt 1]
b. Input device uuid [ckpt 2]
c. Upload calibration data [ckpt 3]
(3) Expected Result
a. The webpage is opened in 1s normally [ckpt 1]
b. The uuid can be input normally, and uuid format is checked, if it's invalid then upload button is locked [ckpt 2]
c. The webpage prompts the user error [ckpt 3]
5. **Admin clear/ban a device**
(1) Prerequisite
a. The admin is logged in
(2) Test Steps
a. Open relavent webpage [ckpt 1]
b. Input device uuid [ckpt 2]
c. Click ban/clear button [ckpt 3]
(3) Expected Result
a. The webpage is opened in 1s normally [ckpt 1]
b. The uuid can be input normally, and uuid format is checked, if it's invalid then upload button is locked [ckpt 2]
c. The webpage prompts the user operation status (200 succ, no resp. failed).[ckpt 3]
10. **Admin upload&set base model---Normal**
(1) Prerequisite
a. The admin is logged in
(2) Test Steps
a. Open relavent webpage [ckpt 1]
b. Selete and upload model [ckpt 2]
(3) Expected Result 
a. The webpage is opened in 1s normally [ckpt 1]
b. Model can be seletd and is uploaded to server. The webpage prompts successful operation(200:succ.) [ckpt 2]
11. **Admin upload&set base model---Exception(server respond timeout, network broke halfway, e.t.c.)**
(1) Prerequisite
a. The admin is logged in
(2) Test Steps
a. Open relavent webpage [ckpt 1]
b. Select and upload a model [ckpt 2]
(3) Expected Result 
a. The webpage is opened in 1s normally [ckpt 1]
b. Model can be seletd and is uploaded to server. The webpage prompts error. [ckpt 2]
#### **User Cloud Operation**
1. **User sets the contact email---Correct email**
(1) Prerequisite
a. The device is connected and activated already
(2) Test Steps
a. Open relavent webpage [ckpt 1]
b. Inputs email of correct format [ckpt 2]
c. Submit [ckpt 3]
d. Check if email is set successfully [ckpt 4]
(3) Expected Result
a. The webpage is opened in 1s normally [ckpt 1]
b. The email can be input normally [ckpt 2]
c. The submit button can be clicked normally [ckpt 3]
d. The webpage prompts the user success [ckpt 4]
(4) Sample Test Data
a. sample123@qq.com
b. sample55@163.com
c. sample@jlu.edu.cn
d. sample@sample.net
3. **User sets the contact email---Email of wrong format**
(1) Prerequisite
a. The device is connected and activated already
(1) Test Steps
a. Open relavent webpage [ckpt 1]
b. Inputs email of wrong format [ckpt 2]
(2) Expected Result
a. The webpage opens in 1s normaly [ckpt 1]
b. The email can be input normally, but the webpage prompts the user wrong email format and locks the submit button [ckpt 2]
(3) Sample Test Data
a. sdfsadf
b. -+23.-0512
c. www.baidu.com
d. @@@@@
5. **User sets the contact email---Too long email**
(1) Prerequisite
a. The device is connected and activated already
(1) Test Steps
a. Open relavent webpage [ckpt 1]
b. Inputs extremely long email(length>254) [ckpt 2]
(2) Expected Result
a. The webpage is opened in 1s normally [ckpt 1]
b. Only the first 254 characters can be inputed. [ckpt 2]
(3) Sample Test Data
a. c...c(c*255)
6. **User sets the contact email---Other exception(Server returns 400)**
(1) Prerequisite
a. The device is connected and activated already
(1) Test Steps
a. Open relavent webpage [ckpt 1]
b. Inputs email of correct format [ckpt 2]
c. Submit [ckpt 3]
d. Check set status [ckpt4]
(2) Expected Result
a. The webpage is opened in 1s normally [ckpt 1]
b. The email can be input normally [ckpt 2]
c. The submit button can be clicked normally[ckpt 3]
d. The webpage prompts the user setting failure. [ckpt4] 
(3) Sample Test Data
a. sample123@qq.com
b. sample55@163.com
c. sample@jlu.edu.cn
d. sample@sample.net
8. **User inspects the contact email---Email was set already**
(1) Prerequisite
a. The device is connected and activated already
(1) Test Steps
a. Open relavent webpage [ckpt 1]
(2) Expected Result
a. The webpage is opened in 1s normally and shows the set email [ckpt 1]
10. **User inspects the contact email---Email was not set yet**
(1) Prerequisite
a. The device is connected and activated already
(1) Test Steps
a. Open relavent webpage [ckpt 1]
(2) Expected Result
a. The webpage is opened in 1s normally but prompts user unset email [ckpt 1]
7. **User deletes email setting---Email was set already**
(1) Prerequisite
a. The device is connected and activated already
(1) Test Steps
a. Open relavent webpage [ckpt 1]
b. Deletes email setting [ckpt 2]
(2) Expected Result
a. The webpage is opened in 1s normally [ckpt 1]
b. The email setting is deleted successfully and the webpage prompts user successful operation. [ckpt 2]
9. **User deletes email setting---Email was not set yet**
(1) Prerequisite
a. The device is connected and activated already
(1) Test Steps
a. Open relavent webpage [ckpt 1]
(2) Expected Result
a. The webpage is opened in 1s normally but the 'delete' button is locked [ckpt 1]
9. **User checks calibration data availability on the server**
(1) Prerequisite
a. The device is connected and activated already
(2) Test Steps
a. Open relavent webpage [ckpt 1]
(3) Expected Result
a. The webpage is opened in 1s normally and shows if the calibration data is available on server currently according to server response(404 no, 200 yes) [ckpt 1]
10. **User uploads new calibration data to the cloud ---Normal**
(1) Prerequisite
a. The device is connected and activated already
(2) Test Steps
a. Open relavent webpage [ckpt 1]
b. Upload data [ckpt 2]
(3) Expected Result
a. The webpage is opened in 1s normally [ckpt 1]
b. The webpage prompts user successful operation[ckpt 2]
10. **User uploads new calibration data to the cloud---Exception(invalid signature, no calibration data, server respond timeout, network broke halfway, e.t.c.)**
(1) Prerequisite
a. The device is connected and activated already
(2) Test Steps
a. Open relavent webpage [ckpt 1]
b. Upload the data [ckpt 2]
(3) Expected Result
a. The webpage is opened in 1s normally [ckpt 1]
b. The webpage prompts the user error according to server response(400(cloud side): invalid signature, 404(device side):no calibration data, Timeout: upload failed)[ckpt 2]
12. **User clears calibration data from the cloud**
(1) Prerequisite
a. The device is connected and activated already
(1) Test Steps
a. Open relavent webpage [ckpt 1]
b. Clears the email setting [ckpt 2]
(2) Expected Result
a. The webpage is opened in 1s normally [ckpt 1]
b. The calibration data is deleted successfully and the webpage prompts user successful operation. [ckpt 2] 
13. **User checks the version of the device model on the server**
(1) Prerequisite
a. The device is connected and activated already
(2) Test Steps
a. Open relavent webpage and check the version [ckpt 1]
b. 
(3) Expected Result
a. The webpage is opened in 1s normally and shows the current model version according to server response.[ckpt 1] 
14. **User downloads the newest model from server---Normal**
(1) Prerequisite
a. The device is connected and activated already
(2) Test Steps
a. Open relavent webpage [ckpt 1]
b. Downloads the model [ckpt 2]
c. Check if the model is downloaded successfully [ckpt 3]
(3) Expected Result
a. The webpage is opened in 1s normally [ckpt 1]
b. The webpage prompts user download starts.[ckpt 2]
c. The model is downloaded successfully [ckpt 3]
14. **User downloads the newest model from server---Exception(server respond timeout, network broke halfway, e.t.c.)**
(1) Prerequisite
a. The device is connected and activated already
(2) Test Steps
a. Open relavent webpage [ckpt 1]
b. Downloads the model [ckpt 2]
(3) Expected Result
a. The webpage is opened in 1s normally [ckpt 1]
b. The webpage prompts the user error.[ckpt 2] 
15. **User resets model version---Normal**
(1) Prerequisite
a. The device is connected and activated already
(2) Test Steps
a. Open relavent webpage [ckpt 1]
b. Resets the model [ckpt 2]
(3) Expected Result
a. The webpage is opened in 1s normally [ckpt 1]
b. The webpage prompts user reset succeeded [ckpt 2] 
15. **User resets model version---Exception(server respond timeout, network broke halfway, e.t.c.)**
(1) Prerequisite
a. The device is connected and activated already
(2) Test Steps
a. Open relavent webpage [ckpt 1]
b. Resets the model [ckpt 2]
(3) Expected Result
a. The webpage is opened in 1s normally [ckpt 1]
b. The webpage prompts the user error.[ckpt 2]

#### **User Local Operation**
27. **User connects the device**
(1) Prerequisite
None
(2) Test Steps
a. Open relavent webpage [ckpt 1]
b. Selects and connects a device [ckpt 2]
(3) Expected Result
a. The webpage is opened in 1s normally [ckpt 1]
b. The webpage prompts user connecting result(200:succ, timeout:failed) [ckpt 2]
28. **User gets and inspects status information of the device**
(1) Prerequisite
a. The device is connected and activated
(2) Test Steps
a. Open relavent webpage [ckpt 1]
b. Gets status information [ckpt 2]
(3) Expected Result
a. The webpage is opened in 1s normally [ckpt 1]
b. The webpage shows the information gotten [ckpt 2]
29. **User download the model from the device---Normal**
(1) Prerequisite
a. The device is connected and activated
(2) Test Steps
a. Open relavent webpage [ckpt 1]
b. Downloads the model from the device [ckpt 2]
c. Check if the model is downloaded successfully [ckpt 3]
(3) Expected Result
a. The webpage is opened in 1s normally [ckpt 1]
b. The webpage shows download starts [ckpt 2]
c. The model is downloaded successfully [ckpt 3]
29. **User download the model from the device---Excetion(No model currently(404), server respond timeout, e.t.c.)**
(1) Prerequisite
a. The device is connected and activated
(2) Test Steps
a. Open relavent webpage [ckpt 1]
b. Downloads the model from the device [ckpt 2]
(3) Expected Result
a. The webpage is opened in 1s normally [ckpt 1]
b. The webpage prompts error(404:no model, Timeout:operation failed) [ckpt 2]
30. **User starts to calibrate**
(1) Prerequisite
a. The device is connected and activated
(2) Test Steps
a. Open relavent webpage [ckpt 1]
b. Starts to calibrate [ckpt 2]
c. Finish calibrate [ckpt 3]
(3) Expected result
a. The webpage is opened in 1s normally [ckpt 1]
b. The webpage shows calibration guide according to server response [ckpt 2]
c. The webpage prompts users calibrating finished [ckpt 3]
31. **User deletes local calibration data**
(1) Prerequisite
a. The device is connected and activated
(2) Test Steps
a. Open relavent webpage [ckpt 1]
b. Clears local calibration data. [ckpt 2]
(3) Expected result
a. The webpage is opened in 1s normally [ckpt 1]
b. The webpage prompt user operation status according to server response(200:succ, timeout:failed) [ckpt 2]

## Unexpected Problems During Integration

### Problem 1.The `stdin` in the pipe takes up a lot of CPU blocked.
|  Date  |            Progress                  |
| ------ | ------------------------------------ |
| May 03 | It is found that the CPU is occupied too much during runtime, so the test is forced to terminate. |
| May 07 | After some white box testing (by viewing the source code), the problem is located to `stdin`. |
| Until now | Looking for what caused `stdin` to be abnormal |

### Problem 2 (Solved).Disconnection condition

|  Date  |            Progress                  |
| ------ | ------------------------------------ |
| May 04 | The case of power failure or network disconnection in the middle of model training and transmission is presented. |
| May 06 | Automatically refiles to the old model.  |
| May 07 | Decided to add the model rewind function. |
| May 10 | Back up the model on the server at intervals. |

### Problem 3.The model saved by the algorithm group is not saved to the location where it should be.
|  Date  |            Progress                  |
| ------ | ------------------------------------ |
| May 04 | Found that the algorithm group sometimes reports an error that the model file cannot be found. |
| Until now | Locating the problem. |

### Problem 4 (Solved).The data format of algorithm group and server groups is different.
|  Date  |            Progress                  |
| ------ | ------------------------------------ |
| May 05 | The data format is different. |
| May 08 | Add data processing module to solve the problem of different formats. |

### Problem 5.Unexpected error from GPU

|  Date  |            Progress                  |
| ------ | ------------------------------------ |
| May 06 | Discovered unexpected error from GPU, even if we did not use GPU. |
| Until now | Trying to locate the problem. |

### Problem 6.The data format is different

|  Date  |            Progress                  |
| ------ | ------------------------------------ |
| May 09 | Successfully update the incremental training prediction model.|
| May 10 | Incremental training takes too long to update.  |
| Until now | Locating the problem  |

### Problem 7(Solved).The administrator cookie cannot be obtained

|  Date  |            Progress                  |
| ------ | ------------------------------------ |
| May 04 | The interface was unable to obtain the administrator cookie from the server|
| May 10 | Modified to automatically extract the cookie to solve this problem |


## Integration Testing Plan
<!--
Here comes the complete testing plan for integration, referring to the workflows in the system design document.
-->

### Overall Configuration

#### Test case 1.Conventions
- [x] `algo.json` SHOULD describe all algorithms provided by the algorithm module in `JSON` format.
- [x] `motions.json` SHOULD define all calibration motions required in `JSON` format.
- [x] `requirements.txt` SHOULD list all Python dependencies for algorithms.
- [x] For each algorithm, a valid base model specified in `algo.json` SHOULD be provided.

### Server calls Algorithm

#### Test case 2.Train Programs
- [x] The process SHOULD exit returning zero if the training was success, non-zero otherwise.
- [x] If the process returns zero, the new_model SHOULD exist and be a replacement of the base model.

#### Test case 3.Predict Program
- [x] The sensor data SHOULD flow in to the `stdin`, one line of 45 comma-separated values each sample from motion sensors.
- [x] The predicted result SHOULD flow out to `stdout`, one motion name each line.
- [x] The model file SHOULD be a training result, a administrator’s upload, or the base model provided in `algo.json`.
- [x] The program SHOULD flush its output buffer for server to receive results in time.

### Server calls Database

#### Test case 4.Sensor Interface
- [x] The data collected SHOULD be written directly to the `stdout`, one line of 45 comma-separated values for each sample from motion sensors.
- [x] One sample SHOULD contain 45 values now.
- [x] The program SHOULD flush its output buffer for server to receive samples in time.

#### Test case 5.`db Package`
- [x] The database module SHOULD provide a package named db, with 2 modules admin and device in it.
- [x] The database SHOULD be stored in the path where environment `DSD_DATABASE` points, or in the current working directory if the environment is not specified.
> *Changed in version 2.0*: The `db.model` module is now merged into the db.device module.

#### Test case 6.`db.admin.add`
- [x] Database SHOULD check the strings to be non-empty and less than 40 characters, the username to contain only `[A-Za-z0-9_]`, and the password to contain only character greater than `0x1f` and less than `0x7f`.
- [x] `ValueError` SHOULD be raised when the sanity check failed.
- [x] Returns True if succeed, False if the username existed.

#### Test case 7.`db.admin.check`
- [x] Check if the given credential is a valid administrator account.
- [x] Returns True if the credential is valid, False otherwise.

#### Test case 8.`db.device.exists`
- [x] Returns True if the device exists in the database, False otherwise.

#### Test case 9.`db.device`
- [x] The devid SHOULD always be a valid UUID.
- [x] The UUID SHOULD be of any version, including the Nil UUID.The Nil UUID (all zero) is now a special value that SHOULD never be assigned to a device. Its models SHOULD be considered the fallback base models, other fields SHOULD be preserved for future use.
- [x] The db.device.Device.banned is now deprecated.

### Interaction calls Server

#### Test case 13.Cloud Authentication
<!-- 
401：应认证未认证/签名无效
403：已认证成功，但权限不足
-->

- [x] If no valid authentication presents, all these API SHOULD return a 401 Unauthorized
- [x] The cloud API now base in `/api/` to ease the deployment with the interaction module.
- [x] Send `DELETE /api/session` to log out, returns 200 OK always.

#### Test case 14.Cloud Device Management API

- [x] The `<algo>` parameter in some interfaces SHOULD be the names in `GET /api/models`. If not, return 404.
- [x] Some interfaces are for administrator only, access them only with device ticket SHOULD get a `403 Forbidden`.
- [x] The UUID SHOULD be of any version, except the Nil UUID (should return 404).
- [x] In `POST /api/device/<uuid>/model/<algo>`, server should output a message when sending e-mail.
- [x] `DELETE /api/device/<uuid>` Now available to device user.
- [x] Device user will now get 403 in HEAD, if they get 200 previously, according to version 1.0.
- [x] `DELETE /api/device/<uuid>/model`is used to clear up all algorithms now.


#### Test case 15.Cloud Model Management API

- [x] Some interfaces are for administrator only, access them only with device ticket SHOULD get a `403 Forbidden`.
- [x] The `<algo>` parameter in some interfaces SHOULD be the names in `GET /api/models`.
- [x] In `GET /api/device/<uuid>/calibration`, if no data collected, it should return 404(no matter whether authorized)
- [x] Some interfaces are for administrator only, access them only with device ticket SHOULD get a `403 Forbidden`.

#### Test case 16.Device API

- [x] The `CORS` response headers sent by the device API SHOULD allow any Origin to use all methods below with credentials, and to access the Signature header.
- [x] The `server_timestamp` SHOULD be from the `GET /api/timestamp` of the cloud platform.
- [x] `DELETE /model` is new in version 2.0, it deletes local model from device and always returns 200.



<!--

## Testing Results


The results of the integration are listed here and you may find the correspondence to the requirements in the requirement analysist document.


| Test Case No. | Module | Result | Corresponding Requirement |
| ------------- | ------ | ------ | ------------------------- |

-->
