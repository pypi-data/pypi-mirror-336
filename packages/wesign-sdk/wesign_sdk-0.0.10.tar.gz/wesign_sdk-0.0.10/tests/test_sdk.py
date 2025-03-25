from src.wesign_sdk.sdk import WesignSDK, DocumentExtractor

import responses
from responses import matchers

api_key = "KDk8FTJBSsg5WrfPpyqIBelk8LzaGgnW8rM38npUWFrX3QOQC0s7zXQ7YdzuQtPuvOvIKah1zpXCAo73QB1NJHEIKucrGwPeS5R0IFyHbpfuQ24zolpmpeI4FSZzxEhfl70XvixyR5O343kO4PbquqVjUNs2GWOeBU5qpaxsxF92ohe4VNxhoNOTjgPARF0v4Iyz5lBR6HLrVb9xtrtpxDbOJgWXJd0QD1vPprdEL8Vr3tvc"
api_domain = 'https://dev.wesign.com'



# @responses.activate
def test_sdk_validating_api():
    # responses.add(
    #     responses.POST,
    #     api_domain + "/auth/validate/api_key",
    #     json=[
    #         {"id": 1, "name": "Lidl", "products": 10},
    #         {"id": 2, "name": "Walmart", "products": 15},
    #     ],
    #     status=200,
    #     match=[matchers.header_matcher({"X-API-KEY": api_key})],
    # )

    sdk = WesignSDK(api_domain, api_key)
    validate_api_key = sdk.validate_api_key()

    assert validate_api_key == 774
    
def test_sdk_document_uploading():
    
    path = '/home/mayur/Downloads/claims.pdf'
    sdk = WesignSDK(api_domain, api_key)
    uploaded_doc = sdk.upload_documents(path)
    
    assert uploaded_doc['status'] == True
    assert uploaded_doc['status_code'] == 200
    assert uploaded_doc['result']['document_name'] == path.split('/')[-1]
    
def test_sdk_adding_recipient():
    path = '/home/mayur/Downloads/claims.pdf'
    data = {
        "recipient_name": "mayur",
        "recipient_email": "mayurbppatil@gmail.com",
        "action": "needs_to_sign",
        "meta_data": [
            {
                "imageId": "page_1",
                "page_no": 1,
                "x": 355.3333333333333,
                "y": 683,
                "left": 355.3333333333333,
                "top": 683,
                "width": 111.66666666666667,
                "height": 33.333333333333336,
                "page_width": 595,
                "page_height": 841,
                "image_width": 595,
                "image_height": 841,
                "document_key": "774/57082392024112043_claimsagreement.pdf",
                "document_order":1,
                "field_name": "signature",
                "include_date_name": True,
                "signature_with_border": True
            },
            
            {
                "imageId": "page_1",
                "page_no": 1,
                "x": 355.3333333333333,
                "y": 683,
                "left": 355.3333333333333,
                "top": 683,
                "width": 111.66666666666667,
                "height": 33.333333333333336,
                "page_width": 595,
                "page_height": 841,
                "image_width": 595,
                "image_height": 841,
                "document_key": "774/57082392024112043_claimsagreement.pdf",
                "document_order":1,
                "field_name": "initial",
                "include_date_name": None,
                "initial_with_border": False
            },
            
            {
                "imageId": "page_1",
                "page_no": 1,
                "x": 355.3333333333333,
                "y": 683,
                "left": 355.3333333333333,
                "top": 683,
                "width": 111.66666666666667,
                "height": 33.333333333333336,
                "page_width": 595,
                "page_height": 841,
                "image_width": 595,
                "image_height": 841,
                "document_order":1,
                "field_name": "email",
                "font_color" : "rgb(0,0,0)"
            },
        ],
        
    }
    
    
    sdk = WesignSDK(api_domain, api_key)
    uploaded_doc = sdk.upload_documents(path)
    verified = sdk.add_recipient(data)
    
    assert verified['recipient_name'] == data['recipient_name']
    assert verified['recipient_email'] == data['recipient_email']
    assert verified['action'] == data['action']
    assert verified['meta_data'][0]['field_name'] == data['meta_data'][0]['field_name']
    
    
def test_sdk_send_envelope():
    path = '/home/mayur/Downloads/claims.pdf'
    data = {
        "recipient_name": "mayur",
        "recipient_email": "mayurbppatil@gmail.com",
        "action": "needs_to_sign",
        "meta_data": [
            {
                "imageId": "page_1",
                "page_no": 1,
                "x": 355.3333333333333,
                "y": 683,
                "left": 355.3333333333333,
                "top": 683,
                "width": 111.66666666666667,
                "height": 33.333333333333336,
                "page_width": 595,
                "page_height": 841,
                "image_width": 595,
                "image_height": 841,
                "document_key": "774/57082392024112043_claimsagreement.pdf",
                "document_order":1,
                "field_name": "signature",
                "include_date_name": True,
                "signature_with_border": True
            },
            
            {
                "imageId": "page_1",
                "page_no": 1,
                "x": 355.3333333333333,
                "y": 683,
                "left": 355.3333333333333,
                "top": 683,
                "width": 111.66666666666667,
                "height": 33.333333333333336,
                "page_width": 595,
                "page_height": 841,
                "image_width": 595,
                "image_height": 841,
                "document_key": "774/57082392024112043_claimsagreement.pdf",
                "document_order":1,
                "field_name": "initial",
                "include_date_name": None,
                "initial_with_border": False
            },
            
            {
                "imageId": "page_1",
                "page_no": 1,
                "x": 355.3333333333333,
                "y": 683,
                "left": 355.3333333333333,
                "top": 683,
                "width": 111.66666666666667,
                "height": 33.333333333333336,
                "page_width": 595,
                "page_height": 841,
                "image_width": 595,
                "image_height": 841,
                "document_order":1,
                "field_name": "email",
                "font_color" : "rgb(0,0,0)"
            },
        ],
        
    }
    
    
    sdk = WesignSDK(api_domain, api_key)
    uploaded_doc = sdk.upload_documents(path)
    verified = sdk.add_recipient(data)
    envelope = sdk.send_envelope(subject='subject', expiry_date="2024-10-07", enable_comments = True, follow_signing_order=True, enable_writing_id=True, auto_reminder=0, number_of_reminders=2)
    
    wesign_doc = DocumentExtractor(api_domain, api_key, envelope['envelope']['id'])
    print(wesign_doc.list_documents())

    wesign_doc.download_documents('/home/mayur/Documents/sdk_download')

    
    assert verified['recipient_name'] == data['recipient_name']
    assert verified['recipient_email'] == data['recipient_email']
    assert verified['action'] == data['action']
    assert verified['meta_data'][0]['field_name'] == data['meta_data'][0]['field_name']
    assert envelope['status_code'] == 200
    
    
    
