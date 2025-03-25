# Wesign SDK

<div align="center">

<img src="https://wesign.odisoft.in/assets/images/logo.png" alt="Wesign logo" width="500" role="img">
</div>



<!-- [![PyPI - Version](https://img.shields.io/pypi/v/hatchling.svg?logo=pypi&label=PyPI&logoColor=gold)](https://pypi.org/project/hatchling/) [![PyPI - Downloads](https://img.shields.io/pypi/dm/hatchling.svg?color=blue&label=Downloads&logo=pypi&logoColor=gold)](https://pypi.org/project/hatchling/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hatchling.svg?logo=python&label=Python&logoColor=gold)](https://pypi.org/project/hatchling/) 

 -->

---

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [License](#license)

## Installation

```console
pip install wesign-sdk
```

## Configuration
The Wesign API uses API keys for authentication.

Wesign uses API keys for authentication. You can generate a Wesign API key in the [API keys](https://wesign.com) section of your Wesign account settings.

The wesign-sdk requires the configuration of a domain, which should be set to https://api.wesign.com.


```console
from wesign_sdk.sdk import WesignSDK

wesign_app = WesignSDK('https://api.wesign.com','<API KEY>')

```

### <span style="color:red;">&#x2022;</span> Exceptions :
- ***InvalidHostError*** : Exception raised on invalid host.
- ***InvalidAPIKeyError*** : Exception raised on invalid API key.


## Usage
Use listed api in order to get document signed. 

1. [Upload Documents](#upload-documents)
2. [Add Recipients](#add-recipients)
3. [Send Envelope for signing](#send-envelope-for-signing)
4. [Get Sign URL](#get-sign-url)
5. [Download Documents](#download-documents)
##
### <img src="./static/document.png" height=30 width=30>    Upload Documents 
Upload document to the wesign server. \
Allowed file types : .docx, .pdf, .png, .jpg, .ppt, .csv, .xlsx, .html, .txt

```console
from wesign_sdk.sdk import WesignSDK

wesign_app = WesignSDK('https://api.wesign.com','<API KEY>')

document_information = wesign_app.upload_documents('<absolute document path>')

```

#### <span style="color:red;">&#x2022;</span> Exceptions :
- Exception : raised by server.
- FileUploadingError : Exception raised during uploading file
- InvalidPathError : Invalid document path.


#### Returned response :

```console
{
    "document_id" : unique generated id for the document,
    "document_name" : document name,
    "created_on" : document uploaded timestamp,
    "converted" : true/false (usefull for other than pdf files, as all files will be converted to pdf.) 
    "uploaded_by" : Account holder user ID.
}

```


##

### <img src="./static/recipient.png" height=30 width=30>  Add Recipients
Include recipient details to send the envelope to the signer for document signing.

Wesign offers various types of fields that can be included in a document, as listed below.


- signature
- stamp
- initial
- checkbox
- radio
- text
- drawing
- date_signed
- full_name
- email
- company
- title
- plain_text
- comment_text
- dropdown
- attachment

**Note :** Each fields has different structure and attribute requirements.

The Recipient object must follow the proper structure and include the required attributes listed below:

- **recipient_name** (required) - Signer/Recipient Name.
- **recipient_email** (required) - Signer/Recipient Email ID. [Either the recipient's email or phone number is required.]
- **recipient_phone** (required) - Signer/Recipient Phone Number. [Either the recipient's email or phone number is required.]
- **action** (required) - Action to be taken by the recipient; it must be either `needs_to_sign` or `receive_copy`.
- **meta_data** (required) - Contains the field information that needs to be completed by the recipient or signer.
    -**page_no** (required) - Specify the page number of the document where this field should appear.
    - **left** (required) - Specify the X-axis position where the field should appear.
    - **top** (required) - Specify the Y-axis position where the field should appear.
    - **width** (required) - Specify the width of the field box.
    - **height** (required) - Specify the height of the field box.
    - **document_order** (required) - Specify the document order number corresponding to the sequence in which the documents were uploaded in the previous API call.
    - **field_name** (required) - Specify the field name, which must be selected from the predefined list of available field names.
    - **font_color** - Specify the font color in RGB format (e.g. `rgb(0,0,0)`).
    - **font_size** - Font size of the text.
    - **signature_with_border** - Indicate whether the signature should have a border and provide the generated unique signature ID.
    - **initial_with_border** - Indicate whether the initial should have a border and provide the generated unique initial ID.
    - **group** (required for field radio) - Specify the group name for **radio** buttons (e.g., `gender`).
    - **is_checked** - Mark `true` if the **checkbox** should be pre-checked.
    - **field_data** - Must not be null in case of **plain_text**, **dropdown**, **radio** fields.

```console
from wesign_sdk.sdk import WesignSDK

wesign_app = WesignSDK('https://api.wesign.com','<API KEY>')

document_information = wesign_app.upload_documents('<absolute document path>')

data = {
        "recipient_name": "Mayur P.",
        "recipient_email": "mayur@wesign.com", [OR] "recipient_phone": "country_code-phonenumber" //+1-1234567890
        "action": "needs_to_sign",
        "meta_data": [
            {
                "page_no": 1,
                "left": 1,
                "top": 1,
                "width": 100,
                "height": 100,
                "document_order":1,
                "field_name": "signature",
                "include_date_name": True,
                "signature_with_border": True
            },{
                "page_no": 1,
                "left": 120,
                "top": 1,
                "width": 100,
                "height": 100,
                "document_order":1,
                "field_name": "initial",
                "include_date_name": None,
                "initial_with_border": False
            },{
                "page_no": 1,
                "left": 240,
                "top": 1,
                "width": 100,
                "height": 20,
                "document_order":1,
                "field_name": "email",
                "font_color" : "rgb(0,0,0)"
            },{
                "page_no": 1,
                "left": 1,
                "top": 150,
                "width": 100,
                "height": 20,
                "document_order":1,
                "field_name": "comment_text",
                "font_color" : "rgb(0,0,0)"
            },{
                "page_no": 1,
                "left": 120,
                "top": 150,
                "width": 100,
                "height": 20,
                "document_order":1,
                "field_name": "plain_text",
                "font_color" : "rgb(0,0,0)",
                "field_data" : "Field Data"
            },{
                "page_no": 1,
                "left": 240,
                "top": 150,
                "width": 100,
                "height": 100,
                "document_order":1,
                "field_name": "drawing",
            },{
                "page_no": 1,
                "left": 1,
                "top": 270,
                "width": 20,
                "height": 20,
                "document_order":1,
                "field_name": "attachment",
                "required_field_checkbox": True
            },{
                "page_no": 2,
                "left": 1,
                "top": 1,
                "width": 100,
                "height": 100,
                "document_order":1,
                "field_name": "signature",
                "include_date_name": True,
                "signature_with_border": True
            },{
                "page_no": 2,
                "left": 120,
                "top": 1,
                "width": 100,
                "height": 100,
                "document_order":1,
                "field_name": "initial",
                "include_date_name": None,
                "initial_with_border": False
            },{
                "page_no": 2,
                "left": 240,
                "top": 1,
                "width": 100,
                "height": 20,
                "document_order":1,
                "field_name": "email",
                "font_color" : "rgb(0,0,0)"
            },{
                "page_no": 2,
                "left": 1,
                "top": 150,
                "width": 100,
                "height": 20,
                "document_order":1,
                "field_name": "comment_text",
                "font_color" : "rgb(0,0,0)"
            },{
                "page_no": 2,
                "left": 120,
                "top": 150,
                "width": 100,
                "height": 20,
                "document_order":1,
                "field_name": "plain_text",
                "font_color" : "rgb(0,0,0)",
                "field_data" : "Field Data"
            },{
                "page_no": 2,
                "left": 240,
                "top": 150,
                "width": 100,
                "height": 100,
                "document_order":1,
                "field_name": "drawing",
            },{
                "page_no": 3,
                "left": 1,
                "top": 150,
                "width": 20,
                "height": 20,
                "field_name": "checkbox",
                "document_order":2,
                "is_checked": False
            }, {
                "page_no": 3,
                "left": 120,
                "top": 150,
                "width": 100,
                "height": 20,
                "field_name": "dropdown",
                "field_data": "Gender,Female,Male,dont want to answer",
                "document_order":2,
                "font_size": 10
            }, {
                "page_no": 3,
                "left": 240,
                "top": 150,
                "width": 10,
                "height": 10,
                "field_name": "radio",
                "field_data": "Male",
                "document_order":2,
                "group": "gender"
                
            }, {
                "page_no": 3,
                "left": 240,
                "top": 170,
                "width": 10,
                "height": 10,
                "field_name": "radio",
                "field_data": "Female",
                "document_order":2,
                "group": "gender"
            }, {
                "page_no": 1,
                "left": 1,
                "top": 270,
                "width": 20,
                "height": 20,
                "document_order":2,
                "field_name": "attachment",
                "required_field_checkbox": True
            },
        ],
        
    }

recipient_1 = wesign_app.add_recipient(data)

```



#### <span style="color:red;">&#x2022;</span> Exceptions :
- ***InvalidRecipientStructureError*** : Exception raised during validating recipient meta_data structure
- ***InvalidFontFamilyError*** : Exception raised during validating font-family
- ***Exception*** : General exception.
- ***InvalidDropDownOptions*** : Exception raised during validating dropdown structure.

##

### <img src="./static/paper_plane.png" height=30 width=30>  Send Envelope for signing

After uploading the document(s) and adding recipient(s), the user can send the envelope for signing.

When sending the envelope, Wesign requires certain keyword arguments, which are listed below.

- **subject** *(str)* : The subject line to address the envelope.

- **expiry_date** *(str - YYYY-MM-DD)* : The date when the envelope expires (format: YYYY-MM-DD).

- **follow_signing_order** *(bool)* : Expiry date for signing the envelope; after this date, recipients cannot sign the envelope.

- **enable_writing_id** *(bool)* : Disabling this will prevent writing the envelope ID on the top-left of each page of documents (default: true).

- **auto_reminder** *(int)* : Allows reminders to be sent to the recipient to sign the envelope. To enable this feature, specify the number of days between reminder intervals (default: 0).

- **number_of_reminders** *(int)* : Specifies the number of reminders to be sent to the recipient.

- **send_email_recipient** *(bool)* : Send email to recipient.

- **follow_envelope_order** *(int)* : Provide the previous Envelope ID to initiate a follow-up signature request. (default : null)


```console
from wesign_sdk.sdk import WesignSDK

wesign_app = WesignSDK('https://api.wesign.com','<API KEY>')

document_information = wesign_app.upload_documents('<absolute document path>')

data = {
        "recipient_name": "Mayur P.",
        "recipient_email": "mayur@wesign.com", [OR] "recipient_phone": "country_code-phonenumber" //+1-1234567890
        "action": "needs_to_sign",
        "meta_data": [
            {
                "page_no": 1,
                "left": 1,
                "top": 1,
                "width": 100,
                "height": 100,
                "document_order":1,
                "field_name": "signature",
                "include_date_name": True,
                "signature_with_border": True
            },
            ...
        ],
        
    }

recipient_1 = wesign_app.add_recipient(data)

envelope = wesign_sdk.send_envelope(
    subject='subject', 
    expiry_date="2030-12-31", # DATE FORMAT - YYYY-MM-DD
    follow_signing_order=True, # default False
    enable_writing_id=True, # Default true
    auto_reminder=0, # default 0
    number_of_reminders=2 # default 0
    )

print(envelope)

```


#### <span style="color:red;">&#x2022;</span> Exceptions :
- ***ValueError*** : Excpection raised if any value is invalid.
- ***TypeError*** : Exception raised if any type is invalid.
- ***EnvelopeSendingError*** : Exception raised if server return with error.

#### <span style="color:green;">&#x2022;</span> Returned response :
In response, Wesign provides a detailed envelope with signing URLs. Developers should use these URLs to sign the documents.

```console
{
  "message": "Envelope Created.",
  "status": true,
  "status_code": 200,
  "envelope": {
    "id": 1,
    "envelope_documents": [
      {
        "id": 1,
        "document_key": "document_key",
        "priority": "document_order",
        "document_name": "document_name",
        "created_on": "created timestamp",
        "updated_on": "updated timestamp",
        "deleted": true/false,
        "document_id": "unique generated id",
        "is_attachment": true/false, // true in case of document is attachment during signing process
        "converted": true/false, // indicates document is converted to pdf or no
        "envelope": "envelope id"
      }
    ],
    "envelope_recepients": [
      {
        "id": "recipient id",
        "token": "unique token generated for recipient",
        "recepient_name": "recipient name",
        "recepient_email": "recipient email id",
        "recipient_phone": "recipient phone number"
        "signed_status": "signed status", // signed, unsinged, declined
        "signed_date": "signed timestamp",
        "action": "recipient actions", // needs_to_sign or recieve_copy
        "last_changed": "last changed timestamp",
        "last_viewed": "last viewed document timestamp",
        "meta_data": [
          {
            "page_no": "page number passed to sign on",
            "left": "X-axis coordinate",
            "top": "Y-axis coorfinate",
            "width": "element box width",
            "height": "element box height",
            "document_order": "document order",
            "field_name": "field_name",
            "element_id": "auto-generated element id",
            "color_code": "color-code assigned",
            "border_color": "border color-code assigned",
            "document_key": "auto assigned document key",
            "type": "element accept type", // image, text
          },
         ....
    ],
    "envelope_content": {
      "subject": "subject of the envelope",
      "content": "content to be send during emailing to the recipient",
      "envelope": "envelope id"
    },
    "subject": "subject of the envelope",
    "envelope_id": "auto-generated unique id of envelope",
    "location": "wesign",
    "sent": "envelope email status",
    "sent_on": "envelope email sent timestamp",
    "signed_status": "envelope signed status", // pending, completed, declined
    "last_changed": "last changed timestamp",
    "last_viewed": "last viewed document timestamp",
    "created_on": "created timestamp",
    "updated_on": "updated timestamp",
    "document_status": "envelope email status",,
    "im_signer": true/false, // true in case of acccount holder is signer
    "expiry_date": "envelope expiry date - YYYY-MM-DD",
    "enable_comments": true/false,
    "void": false/false,
    "voided_on": "voided timestamp",
    "deleted": true/false,
    "deleted_on": "deleted timestamp",
    "completed": true/false,
    "auto_reminder": "auto reminder days",
    "number_of_reminders": "number of auto reminder",
    "follow_signing_order": true/false, // indicates that envelope follows signing order
    "enable_writing_id": true/false, // indicates writing id on top-left of the pages.
    "api_v1": true,
    "holder": "account holder user id"
  },
  "signings_url": [
    {
      "recipient": "recipient email id" [OR] "recipient phone number",
      "signing_url": "signing url to be redirected"
    }
  ]
}

```



##

### <img src="./static/link.png" height=30 width=30> Get Sign URL

After successfully creation of envelope. Developer can access signing URL by recipient Email-ID [OR] Phone number.

```console
from wesign_sdk.sdk import WesignSDK

wesign_app = WesignSDK('https://api.wesign.com','<API KEY>')

document_information = wesign_app.upload_documents('<absolute document path>')

data = {
        "recipient_name": "Mayur P.",
        "recipient_email": "mayur@wesign.com", [OR] "recipient_phone": "+1-1234567890"
        "action": "needs_to_sign",
        "meta_data": [
            {
                "page_no": 1,
                "left": 1,
                "top": 1,
                "width": 100,
                "height": 100,
                "document_order":1,
                "field_name": "signature",
                "include_date_name": True,
                "signature_with_border": True
            },
            ...
        ],
        
    }

recipient_1 = wesign_app.add_recipient(data)

envelope = wesign_sdk.send_envelope(
    subject='subject', 
    expiry_date="2030-12-31", # DATE FORMAT - YYYY-MM-DD
    follow_signing_order=True, # default False
    enable_writing_id=True, # Default true
    auto_reminder=0, # default 0
    number_of_reminders=2 # default 0
    )

sign_url = wesign_sdk.get_sign_url('mayur@wesign.com')

```

#### <span style="color:green;">&#x2022;</span> Returned response :
Wesign returns a secure HTTP URL for signing the documents.
##


## <img src="./static/download_doc.png" height=30 width=30> Download Documents


After the envelope is created, the developer can retrieve a detailed response of the envelope and use the document_key to download the signed documents.

```console
from wesign_sdk.sdk import WesignSDK, DocumentExtractor

document_extractor = DocumentExtractor('https://api.wesign.com','<API KEY>', 'ID OF ENVELOPE')

print(document_extractor.envelope)
document_list = document_extractor.list_documents() 

<!-- returns the list of documents
[{
   'document_name' : "Name of the document",
   'is_attachment' : True/False, # Indicates whether its attached document or uploaded by creator.
    'document_key' : "unique key generated for document stored in secured File storage"
}] -->


document_extractor.download_documents('ABSOLUTE PATH TO FOLDER TO STORE FILES')
```


## License

`wesign-sdk` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
