# Interface Specification 2.0

**This document is currently under review by teams.**

Revision History:

| Date | Description |
| ---- | ----------- |
| May 17 | I->S / CMM API: `GET /api/model*` are now available to device users. |
| May 17 | I->S / Device API: Add `DELETE /model` deleting model from device |
| May 17 | I->S / CDM API: `DELETE /api/deivce/<uuid>` is now available to device users. |
| May 16 | Finished Drafting |

[toc]

## Introduction

The document reflects the consensus of teams on the modular division, defines how modules communicates with each other, providing a crucial basis of module design for developers and testers across teams.

The specifications in each section under the *New in version x.y* is added since this version. Lines starts with *Changed in version x.y* states how the specifications above this line changed in this version.

## Server calls Algorithm

The following files SHOULD be provided.

### `algo.json`

*New in version 2.0*

This file SHOULD describe all algorithms provided by the algorithm module in JSON format.

For example:

```
{
	"lstm": { # internal name, [a-z0-9]+(-[a-z0-9]+)*
		"name": "lstm", # same internal name
		"display": "LSTM", # displayed name
		"desc": "An algorithm that...", # displayed introduction
		"base": "$ALGO/lstm/base.h5", # default base model if not found in database
		"entrypoint": {
			# train program
			"train": ["/usr/bin/env", "python3", "$ALGO/lstm/train.py"],
			# predict program
			"predict": ["/usr/bin/env", "python3", "$ALGO/lstm/predict.py"]
		}
	},
	# ... more algorithms
}
```

`$ALGO` MAY be used as a variable containing the path pointing where the algorithm module is installed, without trailing slash.

Be noticed the comments above are for illustration only, may not be supported in production, so SHOULD be stripped.

### `motions.json`

This file SHOULD define all calibration motions required in JSON format.

For example:

```
[
    {
        "name": "walk", # internal name, [a-z]+
        "display": "Walk", # displayed name
        "desc": "Please walk on ...", # displayed introduction
        "duration": 20 # duration of recording requested
    },
    # ... more motions
]
```

*New in version 2.0*

Be noticed the comments above are for illustration only, may not be supported in production, so SHOULD be stripped.

### `requirements.txt`

*New in version 2.0*

This file SHOULD list all Python dependencies for algorithms.

### Base Model File

*New in version 2.0*

For each algorithm, a valid base model specified in `algo.json` SHOULD be provided.

### Train Programs

On the cloud platform, the server module SHOULD call a `train` entry point from `algo.json`, appending the following command-line arguments in order, to train various models.

- `data_dir`: Absolute path of a directory, with some `.csv` motion data files named with the motion recorded.
- `new_model`: Absolute path of a writable file containing the training outcome when finished.
- `base_model`: Absolute path of the model file used as the base of this training.

*Changed in version 2.0*: The program entry point is now provided in `algo.json`.

*Changed in version 2.0*: The CSV files SHOULD contain lines of samples from motion sensors. Each sample is one line of 45 comma-separated values.

*New in version 2.0*

The process SHOULD exit returning zero if the training was success, non-zero otherwise. If the process returns zero, the `new_model` SHOULD exist and be a replacement of the base model.

### Predict Program

On the embedded platform, the server module SHOULD call a `predict` entry point from `algo.json`, appending the following command-line arguments in order, to predict the user's motion.


- `model_file`: Absolute path of the model used for predicting

The sensor data SHOULD flow in to the `stdin`, one line of 45 comma-separated values each sample from motion sensors. The predicted result SHOULD flow out to `stdout`, one motion name each line.

*Changed in version 2.0*: One sample contains 45 values now.

*New in version 2.0*

The model file SHOULD be a training result, a administrator's upload, or the base model provided in `algo.json`.

The program SHOULD flush its output buffer for server to receive results in time.

## Server calls Database

### Sensor Interface

On the embedded platform, the database module provides sensor data sampling to the server module, then to the algorithm module.

The program `collect.py` SHOULD be called with no arguments. The data collected SHOULD be written directly to the `stdout`, one line of 45 comma-separated values for each sample from motion sensors.

*Changed in version 2.0*: One sample SHOULD contain 45 values now.

*New in version 2.0*

The program SHOULD flush its output buffer for server to receive samples in time.

### `db` Package

On the cloud platform, the server module calls the database modules to manage admin accounts, device models, device calibrations, device contact email etc. The database module SHOULD provide a package named `db`, with 2 modules `admin` and `device` in it.

*Changed in version 2.0*: The `db.model` module is now merged into the `db.device` module.

*New in version 2.0*

The database SHOULD be stored in the path where environment `DSD_DATABASE` points, or in the current working directory if the environment is not specified.

### `db.admin`

#### `db.admin.add(username: str, password: str) -> bool`

Add an administrator account with the specified username and password.

Database SHOULD check the strings to be non-empty and less than 40 characters, the username to contain only `[A-Za-z0-9_]`, and the password to contain only character greater than `0x1f` and less than `0x7f`. `ValueError` SHOULD be raised when the sanity check failed.

Returns `True` if succeed, `False` if the username existed.

#### `db.admin.check(username: str, password: str) -> bool`

Check if the given credential is a valid administrator account.

Returns `True` if the credential is valid, `False` otherwise.

#### `db.admin.remove(username: str) -> None`

Removes the administrator with the specified username.

Returns `None` always.

### `db.device`

The `devid` SHOULD always be a valid UUID.

*Changed in version 2.0*: The UUID SHOULD be of any version, **including** the Nil UUID.

*New in version 2.0*

The Nil UUID (all zero) is now a special value that SHOULD never be assigned to a device. Its models SHOULD be considered the fallback base models, other fields SHOULD be preserved for future use.

#### `db.device.exists(devid: Union[str, uuid.UUID]) -> bool`

*New in version 2.0*

Returns `True` if the device exists in the database, `False` otherwise.

#### `db.device.get(devid: Union[str, uuid.UUID]) -> db.device.Device`

Returns the `db.device.Device` object of the device with a specified device ID. The device entry SHOULD be created if not found.

#### `db.device.remove(devid: Union[str, uuid.UUID]) -> None`

Delete everything about the device with a specified device ID.

Returns `None` always.

### `db.device.Device`

*Changed in version 2.0*: The `db.device.Device.banned` is now deprecated.

#### `db.device.Device.id: uuid.UUID`

The ID of the device.

Read only property.

#### `db.device.Device.email: Optional[str]`

The device's contact email, if exists. Support at least 254 characters, `ValueError` MAY be raised if exceeded.

Defaults to `None`.

#### `db.device.Device.model[algo: str]: Optional[str]`

The path of the device's model file, if exists. SHOULD be an absolute path.

On assignment, SHOULD copy the file specified into the database. When `None` is assigned, SHOULD delete the corresponding model in the database.

Defaults to `None`.

*New in version 2.0*

The `algo` SHOULD be the an internal name of an algorithm, matching `[a-z0-9]+(-[a-z0-9]+)*`. Each device may have one model per algorithm.

#### `db.device.Device.calibration: Optional[str]`

The path of the device's calibration data directory, if exists, with some `.csv` motion data files named with the motion recorded. SHOULD be an absolute path.

On assignment, SHOULD copy the files in the directory specified into the database. When `None` is assigned, SHOULD delete the data.

Defaults to `None`.

### `db.model`

*Changed in version 2.0*: This module is deprecated. The base model SHOULD now be accessed by `db.device.get(uuid.UUID(int=0)).model[algo]`.

## Interaction calls Server

The server module provides API in RESTful style to the interaction module. The cloud and device API SHOULD be provided via HTTPS from two different Origin.

*Changed in version 2.0*: The cloud API now base in `/api/` to ease the deployment with the interaction module.

### Cloud Authentication

All cloud interfaces, excluding the authentication ones, requires a device ticket or an administrator session. If no valid authentication presents, all these API SHOULD return a `401 Unauthorized`.

#### Device Ticket Authentication

The device ticket SHOULD be created by signing a cloud-signed timestamp with the device key, which is signed by the cloud key at the factory. 

Send `GET /api/timestamp` to request a cloud-signed timestamp, consisting colon-separated Unix timestamp and a server signature. For example,

```
1650375337:6bce5953a9506d6c14f2522fd6228afbee394da3
```

Send the timestamp to device's `GET /ticket?ts=` to request the device ticket, consisting colon-separated cloud-signed timestamp, device signature for the timestamp, and device certificate from factory. For example,

```
1650375337:6bce5953a9506d6c14f2522fd6228afbee394da3:e2a29754a9c9d894748edaa3fa1175e126b4b7f58afa541fe7b58def3b298f2d800670c67300aea3bdcdd06db90d8a8830e0cee47e70f04a71e3edfda67ccb8c:c4bc95299b8ff4226399fb33d8b33608ecb31db281b579898292703a9509690b:038d03270d6cdb4b339758923654349e23eb8af21ccd0558690458bcdfae08655ec6e8a32728e4dbb7cffa3a623c54fc41d7d2eb8b0dccd41a79334d9d572d03
```

The interaction module SHOULD send the ticket in the `Authorization` header for cloud API to authenticate devices.

Please note the signed timestamp is valid for only 1 hour. Device ticket with a timestamp issued more than 1 hour ago SHOULD be considered invalid.

#### Administrator Authentication

Send `POST /api/session` to log in a session as an administrator. The request SHOULD be of type `application/json`. For example,

```
{
    "username": "UserName",
    "password": "PaSSw0Rd!"
}
```

A new session will be set, and `200 OK` is returned if logged in successfully, `403 Forbidden` otherwise.

Send `DELETE /api/session` to log out, returns `200 OK` always.

### Cloud Device Management API

These interfaces are for the end user and administrators to manage the cloud resources of a device. All device management interfaces are based in `/api/device/<uuid>`, the `<uuid>` SHOULD be the one in `GET /` of the device API，which is a non-zero UUID. The `<algo>` parameter in some interfaces SHOULD be the names in `GET /api/models`, which is defined in the next section. 

Some interfaces are for administrator only, access them only with device ticket SHOULD get a `403 Forbidden`. Administrators can use all interfaces below specifying any `<uuid>`, even without a device ticket or file `Signature`.

*Changed in version 2.0*: The UUID SHOULD be of any version, **except** the Nil UUID.

#### `GET /api/device/<uuid>/email`

Get the contact email.

The response SHOULD be of type `application/json`. For example,

```
{
    "email": "t@t.tt"
}
```

Returns 404 if not set, 200 otherwise.

#### `POST /api/device/<uuid>/email`

Set the contact email.

The request SHOULD be of type `application/json`, and the same format for `GET`.

The email SHOULD be of the right form and a maximum of 254 characters.

Returns 400 if email is invalid, 200 otherwise.

#### `DELETE /api/device/<uuid>/email`

Clear the contact email.

Returns 200 always.

#### `GET /api/device/<uuid>/calibration`

ADMIN ONLY. **However**, 404 should be always returned if no data collected.

Download the calibration data from the cloud.

The response SHOULD be of type `application/x-tar+gzip`.

Returns 404 if there's no data collected, 200 otherwise.

*Changed in version 2.0*: The `HEAD` method is combined here according to RFC 7231 section 4.3.2. Device user will now get 403 in `HEAD`, if they get 200 previously, accordingto version 1.0.

#### `PUT /api/device/<uuid>/calibration`

Upload new calibration data to the cloud platform.

The request SHOULD be of type `multipart/form-data` with a file field `calibration`, the file SHOULD be of type `application/x-tar+gzip`.

The request SHOULD have a valid `Signature` header passed from the device.

Returns 200 if succeeds, or 400 if the signature is not valid.

*Changed in version 2.0*: Though not specified previously, this should no longer automatically trigger a training task.

#### `DELETE /api/device/<uuid>/calibration`

Clears calibration data from the cloud.

Returns 200 always.

#### `GET /api/device/<uuid>/model/<algo>`

Acquire the device model of a specific algorithm, signed with the platform key. If the device model does not exist, the base version SHOULD be provided. 

The response SHOULD be of type `application/octet-stream`.

The response SHOULD have the following headers:

- `Signature` header to be passed to the device
- `Last-Modified` if and only if the device model exist
- `Content-Length` to indicate the size of model

Returns 200 always.

*Changed in version 2.0*: The `HEAD` method is combined here according to RFC 7231 section 4.3.2.

*Changed in version 2.0*: Add the `<algo>` parameter.

#### `POST /api/device/<uuid>/model/<algo>`

*New in version 2.0*

Train the device model of a specific algorithm with calibration data uploaded. If the previous training is not finished yet, it will be terminated first before new training starts. An email will be send to the device's contact email (if set) when the training finishes.

Returns 400 if the no calibration data available, 200 otherwise.

#### `PUT /api/device/<uuid>/model/<algo>`

ADMIN ONLY.

Upload the device model of a specific algorithm. Please note the model is not deployed to the device until the user chooses to.

The request SHOULD be of type `multipart/form-data` with a file field `model`.

Returns 200 always.

*Changed in version 2.0*: Add the `<algo>` parameter.

#### `DELETE /api/device/<uuid>/model/<algo>`

Clears device model of a specific algorithm from the cloud.

Returns 200 always.

*Changed in version 2.0*: Add the `<algo>` parameter, and the old interface is kept below.

#### `DELETE /api/device/<uuid>/model`

Clears device model of a all algorithms from the cloud.

Returns 200 always.

*Changed in version 2.0*: Delete all device models now.

#### `DELETE /api/device/<uuid>`

Deletes everything of the specified device from the cloud.

Returns 200 always.

*Changed in version 2.0*: The `ban` parameter is deprecated.

*Changed in version 2.0*: Now available to device user.

### Cloud Model Management API

*New in version 2.0*

These interfaces are for the administrators to manage the base models of algorithms. The `<algo>` parameter in some interfaces SHOULD be the names in `GET /api/models`. 

Some interfaces are for administrator only, access them only with device ticket SHOULD get a `403 Forbidden`.

#### `GET /api/models`

Get metadata of available algorithms. The response SHOULD be of type `application/json`, and the same format of `algo.json` provided by the algorithm module.

Returns 200 always.

#### `GET /api/model/<algo>`

Acquire the base model of an algorithm. The response SHOULD be of type `application/octet-stream`.

Returns 200 always.

#### `PUT /api/model/<algo>`

ADMIN ONLY.

Update the base model of an algorithm to be used as the default model for users without calibration. The request SHOULD be of type `multipart/form-data` with a file field `model`.

Returns 200 always.

### Device API

As the end-user controls the pairing procedure, the access to API itself is sufficient as client authentication.

*New in version 2.0*

The CORS response headers sent by the device API SHOULD allow any `Origin` to use all methods below with credentials, and to access the `Signature` header.

#### `GET /`

Provides the client with status information of the device.

The response SHOULD be of type `application/json`. For example,

```
{
    "id": "00000000-0000-0000-0000-000000000000", # string, the device UUID
    "battery": 90, # percentage of battery
    "charging": true, # true if power connected
    "algorithm": { # current algorithm in algo.json format
        "name": "lstm",
        "display": "LSTM",
        # ... other fileds
    },
    "prediction": "walk", # the current detected motion
}
```

Returns 200 always.

*Changed in version 2.0*: The `HEAD` method is combined here according to RFC 7231 section 4.3.2.

*Changed in version 2.0*: Add algorithm information.

*New in version 2.0*

Be noticed the comments above are for illustration only, may not be supported in production, so SHOULD be stripped.

#### `GET /ticket?ts=<server_timestamp>`

Obtain a signed device ticket.

The `server_timestamp` SHOULD be from the `GET /api/timestamp` of the cloud platform.

If the timestamp is of the right shape, the device SHOULD sign it with the device key to create and return a device ticket in plain text. 

Returns 400 if the timestamp is missing or malformed, 200 otherwise.

#### `GET /model`

Download the current model of the current algorithm from the device. This API is for debugging only.

The response SHOULD be of type `application/octet-stream`.

Returns 404 if there's currently no model, 200 otherwise.

#### `PUT /model/<algo>`

Upload a new model for a specific algorithm to the device, and start to use that algorithm.

The `<algo>` parameter SHOULD be the names in `GET /api/models` of the cloud.

The request SHOULD be of type `multipart/form-data` with a file field `model`.

The request SHOULD have a valid `Signature` header passed from the server.

Returns 200 if succeeds, or 400 if the algorithm name or signature is not valid.

*Changed in version 2.0*: Add the `<algo>` parameter.

#### `DELETE /model`

*New in version 2.0*

Delete local model from device.

Returns 200 always.

#### `GET /calibration/pending`

Get metadata of pending calibrations.

The response SHOULD be of type `application/json`. and the same format of `motions.json` provided by the algorithm module.

If all calibrations are finished, SHOULD return `[]`.

Returns 200 always.

#### `POST /calibration/<motion>`

Initialize a new calibration data recording.

The `motion` SHOULD be from the request above. 

Returns 409 if the previous calibration is not finished, 400 if the motion name is invalid, 200 otherwise and the data recording SHOULD be started after a beep.

#### `GET /calibration`

Acquire a pack of all current calibration data, signed with the device key.

The response SHOULD be of type `application/x-tar+gzip`.

The response SHOULD have a `Signature` header to be passed to the cloud platform.

Returns 404 if no data is collected, 200 otherwise.

#### `DELETE /calibration`

Clear local calibration data.

Returns 200 always.
