# Testing Report (Happy Family)

Revision History:

<style>#rev +table td:nth-child(1) { white-space: nowrap }</style>
<div id="rev"></div>

| Date   | Author | Description |
| ------ | ------ | ----------- |
|  |  |  |
| Apr 20 | Ciel ZHAO | converted the template |
| Apr 21 | Elaina BAI | completed |
|  |  |  |
|  |  |  |
|  |  |  |

[toc]
 
## Introduction

### Intended Audience and Purpose

<!--
This document provides the testing method and results, corresponding to the requirement from the customer. It consists of 3 parts, the testing cases, the test plan, and the testing results.
-->

### How to use the document

<!--
You may refer to the content section for the structure of the document, in which Sec. Testing Cases collect the unit and module test information from each team; Sec. Testing Plan shows the steps and expected results of the integration test; Sec. Results describes the real world data out of the test, and the correspondence to the requirements.
-->

## Testing Cases

<!--
In this section, each team propose their testing cases on unit and module testing.
-->

### Server

### Client

### Map

### Wi-Fi Fingerprint

### Database

### Algorithm

## Testing Plan

<!--
Here comes the complete testing plan for integration, referring to the workflows in the system design document.
-->

### Register

### Upload Map

### …

## Testing Results

<!--
The results of the integration are listed here and you may find the correspondence to the requirements in the requirement analysist document.
-->

| Test Case No. | Module | Result | Corresponding Requirement |
| ------------- | ------ | ------ | ------------------------- |
| 1 | db.admin | OK | get() |
| 2 | db.admin | OK | check() |
| 3 | db.admin | OK | remove() |
| 4 | db.device | OK | get() |
| 5 | db.device | OK | remove() |
| 6 | db.device | OK | Device.banned |
| 7 | db.device | OK | Device.email |
| 8 | db.device | OK | Device.model |
| 9 | db.device | OK | Device.calibration |
| 10 | db.model | OK | getBase() |
| 11 | db.model | OK | setBase() |
| 12 | db.admin | OK | * |
| 13 | db.device | OK | * |
| 14 | db.model | OK | * |
