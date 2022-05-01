# Interface Specification

[toc]

## Server calls Algorithm 

**On the embedded platform**, the server module calls the algorithm module to predict the user's motion. On the both platform, use process calls directly for more flexibility.

```
python3 predict.py <model_file>
```

The sensor data should flow into the `stdin`, one line of comma-separated values for each sample. The predicted result should flow out to `stdout`, one motion name for each line.

The `model_file` is an absolute path of the model file used.

Additionally, the algorithm module should provide a `motions.json` file giving information about calibration motions required. For the schema of the JSON document, refer to the response of `GET /calibration/pending` API on embedded platform.

**On the cloud platform**, the server module calls the algorithm module to train various models.

```
python3 train.py <data_dir> <new_model> <base_model>
```

The `data_dir` is an absolute path of a directory, with some `.csv` motion data files named with the motion recorded.

The `new_model` is an absolute path of a writable file, which should contain the training outcome when finished.

The `base_model` is an absolute path of the model file used as the base of this training.

## Server calls Database

**On the embedded platform**, the database module provides sensor data sampling to the server module, then to the algorithm module. Use process calls directly for more flexibility.

```
python3 collect.py
```

The data collected should be written directly to the `stdout`, one line of comma-separated values for each sample.

**On the cloud platform**, the server module calls the database module to manage admin accounts, device models, device calibrations, device contact email etc. Use a Python package interface for interoperability and simplicity.

The database module provides a package named `db`, with 3 modules `admin`, `device` and `model` in it.

### `db.admin`

```
db.admin.add(username: str, password: str)-> bool
```

Add an administrator account with the specified username and password.

The strings must be non-empty and less than 40 characters. The username must contain only `[A-Za-z0-9_]`, and the password must contain only character greater than `0x1f` and less than `0x7f`. `ValueError` should be raised when the sanity check failed.

Returns `True` if succeed, `False` if the username existed.

```
db.admin.check(username: str, password: str)-> bool
```

Check if the given credential is a valid administrator account.

Returns `True` if the credential is valid, `False` otherwise.

```
db.admin.remove(username: str)-> None
```

Removes the administrator with the specified username.

Returns `None` always.

### `db.device`

```
db.device.get(uuid: str|uuid.UUID, create: bool=True)-> db.device.Device
```

Get the `db.device.Device` object of the device with a specified UUID. The UUID must be a valid UUIDv4.

If the `create` is set to `True`, the device entry is created and returned if not found.

Returns a `db.device.Device` instance if the device is found or created, `None` otherwise.

```
db.device.remove(uuid: str|uuid.UUID)-> None
```

Delete everything about the device with the specified UUID.

Returns `None` always.

### `db.device.Device`

```
db.device.Device.id: uuid.UUID
```

The UUID of the device.

Read only property.

```
db.device.Device.banned: bool
```

Indicate if the device is banned from the cloud services.

Defaults to `False`.

```
db.device.Device.email: str
```

The device's contact email, if exists. Support at least 254 characters, `ValueError` should be raised if exceeded.

Defaults to `None`.

```
db.device.Device.model: str
```

The path of the device's model file, if exists. Must be an absolute path.

On assignment, it's expected to copy the file specified into the database, rather than just changing the path. When `None` is assigned, delete the model.

Defaults to `None`.

```

db.device.Device.calibration: str
```

The path of the device's calibration data directory, if exists, with some `.csv` motion data files named with the motion recorded. Must be an absolute path.

On assignment, it's expected to copy the files in the directory specified into the database, rather than just changing the path. When `None` is assigned, delete the data.

Defaults to `None`.

### `db.model`

```
db.model.getBase(): str
```

Get the path of the base model.

Returns an absolute path if set, `None` otherwise.

```
db.model.setBase(path: str): None
```

Set the path of the base model. Must be an absolute path.

Returns `None` always.

## Interaction calls Server

**On the cloud platform**, the server module provides API in RESTful flavour to the interaction module. The API is provided via HTTPS. 

### Authentication

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

Please note the signed timestamp is valid for only 1 hour. Device ticket with a timestamp issued more than 1 hour ago will be rejected.

The administrator authentication procedure is described in a later section.

### Device Management

All device management APIs are based at `/device/<uuid>`, the `uuid` is the one in `GET /` of the device API. If the UUID is not a valid UUIDv4, These APIs return 404.

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

The email must be of the right form and a maximum of 254 characters.

Returns 400 if email is invalid, 200 otherwise.

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
```

Checks whether calibration data is available on the server.

Returns 200 if data is found, 404 otherwise.

```
PUT /device/<uuid>/calibration
```

Upload new calibration data to the cloud platform.

The request must have a valid `Signature` header passed from the device.

The request should be of type `multipart/form-data` with a file field `calibration`, the file must be of type `application/x-tar+gzip`.

Returns 200 if succeeds, or 400 if the signature is not valid.

```
DELETE /device/<uuid>/calibration
```

Clears calibration data from the cloud.

Returns 200 always.

```
HEAD /device/<uuid>/model
```

Checks the version of the device model on the server.

The response contains a `Last-Modified` header of the device model. If the device model does not exist, no such header is sent, but the base version is still available to download.

The response contains a `Content-Length` header to indicate the size of model.

Returns 200 always.

```
GET /device/<uuid>/model
```

Acquire the current version of the device model, signed with the platform key.

If the device model does not exist, the base version is provided.

The response is of type `application/octet-stream`.

The response will have a `Signature` header to be passed to the device.

Returns 200 always.

```
DELETE /device/<uuid>/model
```

Clears device model from the cloud.

Returns 200 always.

### Administration

#### Restricted Device Management

First, several device management APIs are available to administrators only. Please note that the API above are also available to administrators without a device ticket or signature.

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

#### Authentication

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

A new session should be set if logged in successfully, do nothing otherwise.

Returns 200 if succeed, 403 otherwise.

To log out, use

```
DELETE /session
```

Returns 200 always.

Access administrator APIs with device ticket will get a 403. 

#### Base Model Management

```
PUT /model/base
```

Upload a model to the cloud, and set it to be the default model for users without calibration.

The request should be of type `multipart/form-data` with a file field `model`.

Returns 200 always.

### Device API

**On the embedded platform**, the server module provides the necessary API in RESTful flavour to the interaction module. The API is provided via HTTP, nested in Bluetooth. As the end-user controls the pairing procedure, the access to API itself is sufficient as client authentication.

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
GET /calibration/pending
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
