import json
import mimetypes
import os
import sys
import datetime
import random
import string

import requests

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from custom_exceptions.custom_exceptions import (
    FileUploadingError, InvalidAPIKeyError, InvalidPathError,
    InvalidRecipientStructureError, InvalidHostError,EnvelopeSendingError,
    InvalidFontFamilyError,InvalidDropDownOptions, InvalidEnvelopeError)

from models import Config
from recipient_meta_info import meta_info

HTTP_TIMEOUT_SECONDS = 10



FIELD_NAMES = [
    "signature",
    "stamp",
    "initial",
    "checkbox",
    "radio",
    "text",
    "drawing",
    "date_signed",
    "full_name",
    "email",
    "company",
    "title",
    "plain_text",
    "comment_text",
    "dropdown",
    "attachment"
]

FONT_FAMILY = [
    "calibri",
    "couriernew",
    "garamond",
    "georgia",
    "helvetica1",
    "verdana",
    "tahoma",
    "timesnewroman",
    "trebuchet"
]

font_famil_conc = ','.join(FONT_FAMILY)

field_name_conc = ','.join(FIELD_NAMES)

def sdkFunction():
    return 1

class WesignSDK:
    def __init__(self, api_uri, api_key):
        """
        Initiate Document Signing Process.
        
        :param str api_key: the api_key provided by Wesign.com through webapp.
        """
        if api_uri in ['https://dev.wesign.com', 'https://api.wesign.com']:
            self.api_domain = api_uri
        else:
            raise InvalidHostError()
        
        self.api_domain = api_uri
        
        if api_key:
            self.api_key = api_key
        else:
            raise ValueError(f"Invalid API key: {api_key}")
            
        self.documents = []
        self.recipients = []
        self.envelope_id = None
        self.user_id = self.validate_api_key()
        self.signing_url = {}
        
    def validate_api_key(self):
        """
        Validate API key provided by Wesign.
        
        """
        url = self.api_domain+"/auth/validate/api_key"

        payload = json.dumps({
        "api_key": self.api_key
        })
        headers = {
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 200:
            res = response.json()
            self.user_id = res['result']['user']  
            return res['result']['user']
        else:
            raise InvalidAPIKeyError()

        return None
    
    def upload_documents(self, document_path):
        """
        Upload the document to be signed on wesign cloud.
        
        :param str document_path: Specify the absolute path of the document to be uploaded.
        """
        if document_path:
            url = self.api_domain+"/api/v1/upload/file"
            
            file_name = document_path.split('/')[-1]

            payload={'user': self.user_id}
            
            content_type, _ = mimetypes.guess_type(document_path)
            
            
            files=[
                ('file',(file_name,open(document_path,'rb'),content_type))
            ]
            headers = {
                'api-key': self.api_key
            }

            response = requests.request("POST", url, headers=headers, data=payload, files=files)
            if response.status_code == 200:
                res = response.json()
                if res['status_code'] == 200:
                    # print('Document Uploaded')
                    self.documents.append(res['result'])
                    return res
                else:
                    raise Exception(res['message'])
                
            elif response.status_code == 400:
                res = response.json()
                raise Exception(res['message'])
            else:
                raise FileUploadingError()
        else:
            raise InvalidPathError(f"Invalid document path: {document_path}")
        
    def validate_color(self, color):
        if color:
                                            
            if color.startswith('rgb('):
                try:
                    color_codes = [True if isinstance(int(i), int) else False for i in color.replace('rgb(', '').replace(')', '').split(',')]
                except(Exception)as e:
                    raise InvalidRecipientStructureError(f"Invalid font color: Exception "
                            "Font color must be in rgb format eg. rgb(0,0,0).")
                
                if len(color_codes)==3:
                    if False in color_codes:
                        raise InvalidRecipientStructureError(f"Invalid font color: Exception "
                            "Font color must be in rgb format eg. rgb(0,0,0).")
                    else:
                        return color
                else:
                    raise InvalidRecipientStructureError(f"Invalid font color: Exception "
                            "Font color must be in rgb format eg. rgb(0,0,0).")
            else:
                raise InvalidRecipientStructureError(f"Invalid font color: Exception "
                        "Font color must be in rgb format eg. rgb(0,0,0).")
        else:
            return "rgb(0, 0, 0)"
        
    def verify_recipient(self, recipient):
        prepared_meta = []
        meta_field_count = 1
        try:
            meta_info_selected = meta_info[len(self.recipients)]
        except(Exception)as e:
            meta_info_selected = random.choice(meta_info)
            
        if recipient:
            if recipient.get('recipient_name') and (recipient.get('recipient_email') or recipient.get('recipient_phone')):
                if recipient.get('action'):
                    if recipient.get('action') == 'needs_to_sign' or recipient.get('action') == 'receive_copy':
                        recipient['recepient_name'] = recipient['recipient_name']
                        recipient['recepient_email'] = recipient['recipient_email']
                        recipient['recepient_phone'] = recipient['recipient_phone']
                        
                        if recipient.get('action') == 'needs_to_sign':
                            if not recipient.get('meta_data'):
                                raise InvalidRecipientStructureError(f"Invalid Recipient Data : Invalid "
                                    "recipient meta_data structure, For more information please read the documentation.")
                        
                        for meta in recipient.get('meta_data'):
                            if meta.get('field_name') in FIELD_NAMES:
                                
                                meta['element_id'] = meta.get('field_name') +'-'+ ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
                                meta['container_type'] = meta.get('field_name')
                                meta['zoom_value'] =  "Fit To Width"
                                
                                meta['color_code'] = meta_info_selected['recepient_color']
                                meta['border_color'] = meta_info_selected['recepient_border_color']
                                    
                                
                                if meta.get('field_name') == 'attachment':
                                    if meta.get('page_no') and meta.get('width') and meta.get('height') and \
                                        meta.get('document_order') and meta.get('top') and meta.get('left'): 
                                        meta['x'] = meta['left']
                                        meta['y'] = meta['top']
                                        meta['document_key'] = self.documents[meta.get('document_order')-1]['document_key']
                                        meta['type'] = 'image'
                                        meta['field_class_name'] = meta.get('field_name') + str(meta_field_count)
                                        meta_field_count += 1
                                        prepared_meta.append(meta)
                                    else:
                                        raise InvalidRecipientStructureError(f"Invalid Recipient Field: Exception "
                                            "raised due to missing required values. Ensure that top, left, document_order,"
                                            "width, and height are provided.")
                                
                                
                                if meta.get('field_name') == 'signature':
                                    if meta.get('page_no') and meta.get('width') and meta.get('height') and \
                                        meta.get('document_order') and meta.get('top') and meta.get('left'): 
                                        meta['x'] = meta['left']
                                        meta['y'] = meta['top']
                                        meta['document_key'] = self.documents[meta.get('document_order')-1]['document_key']
                                        meta['type'] = 'image'
                                        meta['signature_with_border'] = True if meta.get('signature_with_border') else False
                                        if meta['signature_with_border']:
                                            recipient['signature_with_border'] = True
                                        
                                        meta['include_date_name'] = True if meta.get('include_date_name') else False
                                        
                                        meta['field_class_name'] = meta.get('field_name') + str(meta_field_count)
                                        meta_field_count += 1
                                        prepared_meta.append(meta)
                                    else:
                                        raise InvalidRecipientStructureError(f"Invalid Recipient Field: Exception "
                                            "raised due to missing required values. Ensure that top, left, document_order,"
                                            "width, and height are provided.")
                                        
                                if meta.get('field_name') == 'stamp':
                                    if meta.get('page_no') and meta.get('width') and meta.get('height') and \
                                        meta.get('document_order') and meta.get('top') and meta.get('left'): 
                                        meta['x'] = meta['left']
                                        meta['y'] = meta['top']
                                        meta['document_key'] = self.documents[meta.get('document_order')-1]['document_key']
                                        meta['type'] = 'image'
                                        
                                        meta['field_class_name'] = meta.get('field_name') + str(meta_field_count)
                                        meta_field_count += 1
                                        prepared_meta.append(meta)
                                    else:
                                        raise InvalidRecipientStructureError(f"Invalid Recipient Field: Exception "
                                            "raised due to missing required values. Ensure that top, left, document_order,"
                                            "width, and height are provided.")
                                        
                                if meta.get('field_name') == 'initial':
                                    if meta.get('page_no') and meta.get('width') and meta.get('height') and \
                                        meta.get('document_order') and meta.get('top') and meta.get('left'): 
                                        meta['x'] = meta['left']
                                        meta['y'] = meta['top']
                                        meta['document_key'] = self.documents[meta.get('document_order')-1]['document_key']
                                        meta['type'] = 'image'
                                        meta['initial_with_border'] = True if meta.get('initial_with_border') else False
                                        meta['field_class_name'] = meta.get('field_name') + str(meta_field_count)
                                        meta_field_count += 1
                                        prepared_meta.append(meta)
                                    else:
                                        raise InvalidRecipientStructureError(f"Invalid Recipient Field: Exception "
                                            "raised due to missing required values. Ensure that top, left, document_order,"
                                            "width, and height are provided.")
                            
                                if meta.get('field_name') == 'full_name':
                                    if meta.get('page_no') and meta.get('width') and meta.get('height') and \
                                        meta.get('document_order') and meta.get('top') and meta.get('left'): 
                                        
                                        meta['container_type'] = 'div'
                                        meta['x'] = meta['left']
                                        meta['y'] = meta['top']
                                        meta['document_key'] = self.documents[meta.get('document_order')-1]['document_key']
                                        meta['type'] = 'text'
                                        
                                        meta['field_class_name'] = 'div' + str(meta_field_count)
                                        meta_field_count += 1
                                        
                                        if meta.get('font_size'):
                                            meta['font_size'] = int(meta.get('font_size'))
                                        else:
                                            meta['font_size'] = 8
                                            
                                        if meta.get('font_color'):
                                            meta['font_color'] = self.validate_color(meta.get('font_color'))    
                                        else:
                                            meta['font_color'] = "rgb(0, 0, 0)"
                                            
                                        if meta.get('font_family'):
                                            if meta.get('font_family') in FONT_FAMILY:
                                                pass
                                            else:
                                                raise InvalidFontFamilyError(f"Invalid Font Family: Exception "
                                                    "raised due to Invalid fonts.") 
                                        else:
                                            meta['font_family'] = "helvetica"
                                            
                                        
                                        if meta.get('font_weight'):
                                            if meta.get('font_weight') == 'bold':
                                                pass
                                            else:
                                                raise Exception(f"Invalid Font Weight: Exception "
                                                    "raised due to Invalid font weight.") 
                                        else:
                                            meta['font_weight'] = "normal"
                                            
                                        if meta.get('font_style'):
                                            if meta.get('font_style') == 'italic':
                                                pass
                                            else:
                                                raise Exception(f"Invalid Font style: Exception "
                                                    "raised due to Invalid font style.") 
                                        else:
                                            meta['font_style'] = "normal"
                                        
                                        if meta.get('text_decoration'):
                                            if meta.get('text_decoration') == 'underline':
                                                pass
                                            else:
                                                raise Exception(f"Invalid Text decoration: Exception "
                                                    "raised due to Invalid text decoration.") 
                                        else:
                                            meta['text_decoration'] = None
                                            
                                        meta['field_data'] = recipient.get('recipient_name')
                                            
                                        prepared_meta.append(meta)
                                    else:
                                        raise InvalidRecipientStructureError(f"Invalid Recipient Field: Exception "
                                            "raised due to missing required values. Ensure that top, left, document_order,"
                                            "width, and height are provided.")
                            
                                if meta.get('field_name') == 'date_signed':
                                    if meta.get('page_no') and meta.get('width') and meta.get('height') and \
                                        meta.get('document_order') and meta.get('top') and meta.get('left'): 
                                        
                                        meta['container_type'] = 'div'
                                        meta['x'] = meta['left']
                                        meta['y'] = meta['top']
                                        meta['document_key'] = self.documents[meta.get('document_order')-1]['document_key']
                                        meta['type'] = 'text'
                                        meta['date_format'] = 'MM/DD/YYYY'
                                        
                                        meta['field_class_name'] = 'div' + str(meta_field_count)
                                        meta_field_count += 1
                                        
                                        if meta.get('font_size'):
                                            meta['font_size'] = int(meta.get('font_size'))
                                        else:
                                            meta['font_size'] = 8
                                            
                                        if meta.get('font_color'):
                                            meta['font_color'] = self.validate_color(meta.get('font_color'))    
                                        else:
                                            meta['font_color'] = "rgb(0, 0, 0)"
                                            
                                        meta['field_data'] = "Date Signed"
                                            
                                        prepared_meta.append(meta)
                                    else:
                                        raise InvalidRecipientStructureError(f"Invalid Recipient Field: Exception "
                                            "raised due to missing required values. Ensure that top, left, document_order,"
                                            "width, and height are provided.")
                                
                                
                                if meta.get('field_name') == 'email':
                                    if meta.get('page_no') and meta.get('width') and meta.get('height') and \
                                        meta.get('document_order') and meta.get('top') and meta.get('left'): 
                                        
                                        meta['container_type'] = 'div'
                                        meta['x'] = meta['left']
                                        meta['y'] = meta['top']
                                        meta['document_key'] = self.documents[meta.get('document_order')-1]['document_key']
                                        meta['type'] = 'text'
                                        
                                        meta['field_class_name'] = 'div' + str(meta_field_count)
                                        meta_field_count += 1
                                        
                                        if meta.get('font_size'):
                                            meta['font_size'] = int(meta.get('font_size'))
                                        else:
                                            meta['font_size'] = 8
                                            
                                        if meta.get('font_color'):
                                            meta['font_color'] = self.validate_color(meta.get('font_color'))    
                                        else:
                                            meta['font_color'] = "rgb(0, 0, 0)"
                                            
                                        meta['field_data'] = recipient.get('recipient_email')
                                        
                                        if meta.get('font_family'):
                                            if meta.get('font_family') in FONT_FAMILY:
                                                pass
                                            else:
                                                raise InvalidFontFamilyError(f"Invalid Font Family: Exception "
                                                    "raised due to Invalid fonts.") 
                                        else:
                                            meta['font_family'] = "helvetica"
                                            
                                        
                                        if meta.get('font_weight'):
                                            if meta.get('font_weight') == 'bold':
                                                pass
                                            else:
                                                raise Exception(f"Invalid Font Weight: Exception "
                                                    "raised due to Invalid font weight.") 
                                        else:
                                            meta['font_weight'] = "normal"
                                            
                                        if meta.get('font_style'):
                                            if meta.get('font_style') == 'italic':
                                                pass
                                            else:
                                                raise Exception(f"Invalid Font style: Exception "
                                                    "raised due to Invalid font style.") 
                                        else:
                                            meta['font_style'] = "normal"
                                        
                                        if meta.get('text_decoration'):
                                            if meta.get('text_decoration') == 'underline':
                                                pass
                                            else:
                                                raise Exception(f"Invalid Text decoration: Exception "
                                                    "raised due to Invalid text decoration.") 
                                        else:
                                            meta['text_decoration'] = None
                                        
                                        # print(meta)
                                        prepared_meta.append(meta)
                                    else:
                                        raise InvalidRecipientStructureError(f"Invalid Recipient Field: Exception "
                                            "raised due to missing required values. Ensure that top, left, document_order,"
                                            "width, and height are provided.")
                                        
                                
                                if meta.get('field_name') == 'company':
                                    if meta.get('page_no') and meta.get('width') and meta.get('height') and \
                                        meta.get('document_order') and meta.get('top') and meta.get('left'): 
                                        
                                        meta['container_type'] = 'text_field'
                                        meta['x'] = meta['left']
                                        meta['y'] = meta['top']
                                        meta['document_key'] = self.documents[meta.get('document_order')-1]['document_key']
                                        meta['type'] = 'text'
                                        
                                        meta['field_class_name'] = 'text_field' + str(meta_field_count)
                                        meta_field_count += 1
                                        
                                        if meta.get('font_size'):
                                            meta['font_size'] = int(meta.get('font_size'))
                                        else:
                                            meta['font_size'] = 8
                                            
                                        if meta.get('font_color'):
                                            meta['font_color'] = self.validate_color(meta.get('font_color'))    
                                        else:
                                            meta['font_color'] = "rgb(0, 0, 0)"
                                            
                                        meta['field_data'] = ""
                                        
                                        if meta.get('font_family'):
                                            if meta.get('font_family') in FONT_FAMILY:
                                                pass
                                            else:
                                                raise InvalidFontFamilyError(f"Invalid Font Family: Exception "
                                                    "raised due to Invalid fonts.") 
                                        else:
                                            meta['font_family'] = "helvetica"
                                            
                                        
                                        if meta.get('font_weight'):
                                            if meta.get('font_weight') == 'bold':
                                                pass
                                            else:
                                                raise Exception(f"Invalid Font Weight: Exception "
                                                    "raised due to Invalid font weight.") 
                                        else:
                                            meta['font_weight'] = "normal"
                                            
                                        if meta.get('font_style'):
                                            if meta.get('font_style') == 'italic':
                                                pass
                                            else:
                                                raise Exception(f"Invalid Font style: Exception "
                                                    "raised due to Invalid font style.") 
                                        else:
                                            meta['font_style'] = "normal"
                                        
                                        if meta.get('text_decoration'):
                                            if meta.get('text_decoration') == 'underline':
                                                pass
                                            else:
                                                raise Exception(f"Invalid Text decoration: Exception "
                                                    "raised due to Invalid text decoration.") 
                                        else:
                                            meta['text_decoration'] = None
                                            
                                        prepared_meta.append(meta)
                                    else:
                                        raise InvalidRecipientStructureError(f"Invalid Recipient Field: Exception "
                                            "raised due to missing required values. Ensure that top, left, document_order,"
                                            "width, and height are provided.")
                            
                                if meta.get('field_name') == 'title':
                                    if meta.get('page_no') and meta.get('width') and meta.get('height') and \
                                        meta.get('document_order') and meta.get('top') and meta.get('left'): 
                                        
                                        meta['container_type'] = 'text_field'
                                        meta['x'] = meta['left']
                                        meta['y'] = meta['top']
                                        meta['document_key'] = self.documents[meta.get('document_order')-1]['document_key']
                                        meta['type'] = 'text'
                                        
                                        meta['field_class_name'] = 'text_field' + str(meta_field_count)
                                        meta_field_count += 1
                                        
                                        if meta.get('font_size'):
                                            meta['font_size'] = int(meta.get('font_size'))
                                        else:
                                            meta['font_size'] = 8
                                            
                                        if meta.get('font_color'):
                                            meta['font_color'] = self.validate_color(meta.get('font_color'))    
                                        else:
                                            meta['font_color'] = "rgb(0, 0, 0)"
                                            
                                        meta['field_data'] = ""
                                        
                                        if meta.get('font_family'):
                                            if meta.get('font_family') in FONT_FAMILY:
                                                pass
                                            else:
                                                raise InvalidFontFamilyError(f"Invalid Font Family: Exception "
                                                    "raised due to Invalid fonts.") 
                                        else:
                                            meta['font_family'] = "helvetica"
                                            
                                        
                                        if meta.get('font_weight'):
                                            if meta.get('font_weight') == 'bold':
                                                pass
                                            else:
                                                raise Exception(f"Invalid Font Weight: Exception "
                                                    "raised due to Invalid font weight.") 
                                        else:
                                            meta['font_weight'] = "normal"
                                            
                                        if meta.get('font_style'):
                                            if meta.get('font_style') == 'italic':
                                                pass
                                            else:
                                                raise Exception(f"Invalid Font style: Exception "
                                                    "raised due to Invalid font style.") 
                                        else:
                                            meta['font_style'] = "normal"
                                        
                                        if meta.get('text_decoration'):
                                            if meta.get('text_decoration') == 'underline':
                                                pass
                                            else:
                                                raise Exception(f"Invalid Text decoration: Exception "
                                                    "raised due to Invalid text decoration.") 
                                        else:
                                            meta['text_decoration'] = None
                                            
                                        prepared_meta.append(meta)
                                    else:
                                        raise InvalidRecipientStructureError(f"Invalid Recipient Field title: Exception "
                                            "raised due to missing required values. Ensure that top, left, document_order,"
                                            "width, and height are provided.")
                            
                                if meta.get('field_name') == 'plain_text':
                                    if meta.get('page_no') and meta.get('width') and meta.get('height') and \
                                        meta.get('document_order') and meta.get('top') and meta.get('left') and meta.get('field_data'): 
                                        
                                        meta['container_type'] = 'text_field'
                                        meta['x'] = meta['left']
                                        meta['y'] = meta['top']
                                        meta['document_key'] = self.documents[meta.get('document_order')-1]['document_key']
                                        meta['type'] = 'text'
                                        
                                        meta['field_class_name'] = 'text_field' + str(meta_field_count)
                                        meta_field_count += 1
                                        
                                        if meta.get('font_size'):
                                            meta['font_size'] = int(meta.get('font_size'))
                                        else:
                                            meta['font_size'] = 8
                                            
                                        if meta.get('font_color'):
                                            meta['font_color'] = self.validate_color(meta.get('font_color'))    
                                        else:
                                            meta['font_color'] = "rgb(0, 0, 0)"
                                        
                                        if not meta.get('field_data'):
                                            meta['field_data'] = "Note "
                                        
                                        
                                        if meta.get('font_family'):
                                            if meta.get('font_family') in FONT_FAMILY:
                                                pass
                                            else:
                                                raise InvalidFontFamilyError(f"Invalid Font Family: Exception "
                                                    "raised due to Invalid fonts.") 
                                        else:
                                            meta['font_family'] = "helvetica"
                                            
                                        
                                        if meta.get('font_weight'):
                                            if meta.get('font_weight') == 'bold':
                                                pass
                                            else:
                                                raise Exception(f"Invalid Font Weight: Exception "
                                                    "raised due to Invalid font weight.") 
                                        else:
                                            meta['font_weight'] = "normal"
                                            
                                        if meta.get('font_style'):
                                            if meta.get('font_style') == 'italic':
                                                pass
                                            else:
                                                raise Exception(f"Invalid Font style: Exception "
                                                    "raised due to Invalid font style.") 
                                        else:
                                            meta['font_style'] = "normal"
                                        
                                        if meta.get('text_decoration'):
                                            if meta.get('text_decoration') == 'underline':
                                                pass
                                            else:
                                                raise Exception(f"Invalid Text decoration: Exception "
                                                    "raised due to Invalid text decoration.") 
                                        else:
                                            meta['text_decoration'] = None
                                        
                                        
                                        if meta.get('external_link_url'):
                                            meta["is_link_inserted"] = True
                                        else:
                                            meta["is_link_inserted"] = False
                                            
                                        prepared_meta.append(meta)
                                    else:
                                        raise InvalidRecipientStructureError(f"Invalid Recipient Field plain_text: Exception "
                                            "raised due to missing required values. Ensure that field_data, top, left, document_order,"
                                            "width, and height are provided.")
                                        
                                
                                if meta.get('field_name') == 'comment_text':
                                    if meta.get('page_no') and meta.get('width') and meta.get('height') and \
                                        meta.get('document_order') and meta.get('top') and meta.get('left'): 
                                        
                                        meta['container_type'] = 'text_field'
                                        meta['x'] = meta['left']
                                        meta['y'] = meta['top']
                                        meta['document_key'] = self.documents[meta.get('document_order')-1]['document_key']
                                        meta['type'] = 'text'
                                        
                                        meta['field_class_name'] = 'text_field' + str(meta_field_count)
                                        meta_field_count += 1
                                        
                                        if meta.get('font_size'):
                                            meta['font_size'] = int(meta.get('font_size'))
                                        else:
                                            meta['font_size'] = 8
                                            
                                        if meta.get('font_color'):
                                            meta['font_color'] = self.validate_color(meta.get('font_color'))    
                                        else:
                                            meta['font_color'] = "rgb(0, 0, 0)"
                                            
                                        meta['field_data'] = " "
                                        
                                        if meta.get('font_family'):
                                            if meta.get('font_family') in FONT_FAMILY:
                                                pass
                                            else:
                                                raise InvalidFontFamilyError(f"Invalid Font Family: Exception "
                                                    "raised due to Invalid fonts.") 
                                        else:
                                            meta['font_family'] = "helvetica"
                                            
                                        
                                        if meta.get('font_weight'):
                                            if meta.get('font_weight') == 'bold':
                                                pass
                                            else:
                                                raise Exception(f"Invalid Font Weight: Exception "
                                                    "raised due to Invalid font weight.") 
                                        else:
                                            meta['font_weight'] = "normal"
                                            
                                        if meta.get('font_style'):
                                            if meta.get('font_style') == 'italic':
                                                pass
                                            else:
                                                raise Exception(f"Invalid Font style: Exception "
                                                    "raised due to Invalid font style.") 
                                        else:
                                            meta['font_style'] = "normal"
                                        
                                        if meta.get('text_decoration'):
                                            if meta.get('text_decoration') == 'underline':
                                                pass
                                            else:
                                                raise Exception(f"Invalid Text decoration: Exception "
                                                    "raised due to Invalid text decoration.") 
                                        else:
                                            meta['text_decoration'] = None
                                        
                                            
                                        prepared_meta.append(meta)
                                    else:
                                        raise InvalidRecipientStructureError(f"Invalid Recipient Field comment_text: Exception "
                                            "raised due to missing required values. Ensure that top, left, document_order,"
                                            "width, and height are provided.")
                                
                                
                                if meta.get('field_name') == 'drawing':
                                    if meta.get('page_no') and meta.get('width') and meta.get('height') and \
                                        meta.get('document_order') and meta.get('top') and meta.get('left'): 
                                        
                                        meta['container_type'] = 'drawing'
                                        meta['x'] = meta['left']
                                        meta['y'] = meta['top']
                                        meta['document_key'] = self.documents[meta.get('document_order')-1]['document_key']
                                        meta['type'] = 'image'
                                        
                                        meta['field_class_name'] = 'drawing' + str(meta_field_count)
                                        meta_field_count += 1
                                        
                                            
                                        meta['field_data'] = None
                                        
                                        
                                            
                                        prepared_meta.append(meta)
                                    else:
                                        raise InvalidRecipientStructureError(f"Invalid Recipient Field drawing: Exception "
                                            "raised due to missing required values. Ensure that top, left, document_order,"
                                            "width, and height are provided.")
                                        
                                        
                                if meta.get('field_name') == 'checkbox':
                                    if meta.get('page_no') and meta.get('width') and meta.get('height') and \
                                        meta.get('document_order') and meta.get('top') and meta.get('left'): 
                                        
                                        meta['container_type'] = 'checkbox'
                                        meta['x'] = meta['left']
                                        meta['y'] = meta['top']
                                        meta['document_key'] = self.documents[meta.get('document_order')-1]['document_key']
                                        meta['type'] = 'checkbox'
                                        
                                        meta['field_class_name'] = 'checkbox' + str(meta_field_count)
                                        meta_field_count += 1
                                        
                                            
                                        meta['field_data'] = "on"
                                        
                                        if meta.get('is_checked'):
                                            meta['is_checked'] = True
                                        else:
                                            meta['is_checked'] = False
                                        
                                        
                                            
                                        prepared_meta.append(meta)
                                    else:
                                        raise InvalidRecipientStructureError(f"Invalid Recipient Field checkbox: Exception "
                                            "raised due to missing required values. Ensure that top, left, document_order,"
                                            "width, and height are provided.")
                                
                                
                                if meta.get('field_name') == 'dropdown':
                                    if meta.get('page_no') and meta.get('width') and meta.get('height') and \
                                        meta.get('document_order') and meta.get('top') and meta.get('left') and meta.get('field_data'): 
                                        
                                        meta['container_type'] = 'dropdown'
                                        meta['x'] = meta['left']
                                        meta['y'] = meta['top']
                                        meta['document_key'] = self.documents[meta.get('document_order')-1]['document_key']
                                        meta['type'] = 'dropdown'
                                        
                                        meta['field_class_name'] = 'dropdown' + str(meta_field_count)
                                        meta_field_count += 1
                                        
                                        if meta.get('font_size'):
                                            meta['font_size'] = int(meta.get('font_size'))
                                        else:
                                            meta['font_size'] = 8
                                            
                                        if meta.get('font_family'):
                                            if meta.get('font_family') in FONT_FAMILY:
                                                pass
                                            else:
                                                raise InvalidFontFamilyError(f"Invalid Font Family: Exception "
                                                    "raised due to Invalid fonts.") 
                                        else:
                                            meta['font_family'] = "helvetica"
                                        
                                            
                                        if len(meta.get('field_data').split(',')) >= 2:
                                            pass
                                        else:
                                            raise InvalidDropDownOptions("Invalid Dropdown options : "
                                                    "Dropdown field_data must have atleast one option and header/title of dropdown."
                                                    "example :- HEADER, OPTION-1, OPTION-2,..,OPTION-N.")
                                        
                                        
                                        
                                            
                                        prepared_meta.append(meta)
                                    else:
                                        raise InvalidRecipientStructureError(f"Invalid Recipient Field checkbox: Exception "
                                            "raised due to missing required values. Ensure that top, left, document_order,"
                                            "width, and height are provided.")
                                
                                
                                if meta.get('field_name') == 'radio':
                                    if meta.get('page_no') and meta.get('width') and meta.get('height') and \
                                        meta.get('document_order') and meta.get('top') and meta.get('left') and meta.get('field_data') and meta.get('group'): 
                                        
                                        meta['container_type'] = 'radio'
                                        meta['x'] = meta['left']
                                        meta['y'] = meta['top']
                                        meta['document_key'] = self.documents[meta.get('document_order')-1]['document_key']
                                        meta['type'] = 'radio'
                                        
                                        meta['field_class_name'] = 'radio' + str(meta_field_count)
                                        meta_field_count += 1
                                        
                                        if meta.get('font_size'):
                                            meta['font_size'] = int(meta.get('font_size'))
                                        else:
                                            meta['font_size'] = 8
                                        
                                            
                                        meta['field_data'] = meta.get('group')+'@-@-@'+meta['field_data']
                                        
                                        
                                            
                                        prepared_meta.append(meta)
                                    else:
                                        raise InvalidRecipientStructureError(f"Invalid Recipient Field radio: Exception "
                                            "raised due to missing required values. Ensure that group, field_data, top, left, document_order,"
                                            "width, and height are provided.")





                            else:
                                raise InvalidRecipientStructureError(f"Invalid Recipient Field: Exception "
                                    "raised due to an invalid field name. The field_name must be one of the"
                                    f"following: {field_name_conc}")
                        recipient['meta_data'] = prepared_meta
                        recipient['meta_info'] = meta_info_selected 
                        return recipient
                    else:
                        raise InvalidRecipientStructureError(f"Invalid Recipient Action : Exception " 
                            "raised when an action is required by the recipient (needs_to_sign/receive_copy).")
                else:
                    raise InvalidRecipientStructureError(f"Invalid Recipient Action : Exception "
                        "raised when an action is required by the recipient (needs_to_sign/receive_copy).")
            else:
                raise InvalidRecipientStructureError(f"Invalid Recipient "
                    ": recipient_name and recipient_email/recipient_phone required.")
        
    def add_recipient(self, recipient):
        verified_recipient = self.verify_recipient(recipient)
        # print(verified_recipient)
        self.recipients.append(verified_recipient)
        return verified_recipient
    
    def get_sign_url(self, recipient_email=None):
        if recipient_email:
            if recipient_email in self.signing_url:
                return self.signing_url[recipient_email]
            raise Exception('Invalid Recipient Email-id.')
        else:
            return self.signing_url
        
    def send_envelope(self, *args, **kwargs):
        
        request_object = {}
        
        
        request_object['holder'] = self.user_id
        
        if kwargs.get('subject'):
            request_object['subject'] = kwargs.get('subject')
        else:
            request_object['subject'] = 'Wesign :' + ','.join([i.get('document_name') for i in self.documents])
            
        if kwargs.get('expiry_date'):
            try:
                date_instance = datetime.datetime.strptime(kwargs.get('expiry_date'), '%Y-%m-%d')
            except(Exception)as e:
                raise ValueError(f"Invalid expiry_date format. The date should be in the YYYY-MM-DD format.")
            
            if date_instance <= datetime.datetime.now():
                raise ValueError(f"expiry_date must be greater than today's date.")
            
            
            request_object['expiry_date'] = kwargs.get('expiry_date')
        else:
            request_object['expiry_date'] = None
            
        if kwargs.get('enable_comments'):
            if isinstance(kwargs.get('enable_comments'), bool):
                request_object['enable_comments'] = kwargs.get('enable_comments')
            else:
                raise TypeError(f"Invalid enable_comments type. It should be a boolean (bool).")
        else:
            request_object['enable_comments'] = False
            
        if kwargs.get('follow_signing_order'):
            if isinstance(kwargs.get('follow_signing_order'), bool):
                request_object['follow_signing_order'] = kwargs.get('follow_signing_order')
            else:
                raise TypeError(f"Invalid follow_signing_order type. It should be a boolean (bool).")
        else:
            request_object['follow_signing_order'] = False
            
        
        if kwargs.get('enable_writing_id'):
            if isinstance(kwargs.get('enable_writing_id'), bool):
                request_object['enable_writing_id'] = kwargs.get('enable_writing_id')
            else:
                raise TypeError(f"Invalid enable_writing_id type. It should be a boolean (bool).")
        else:
            request_object['enable_writing_id'] = False
            
        if kwargs.get('send_email'):
            if isinstance(kwargs.get('send_email'), bool):
                request_object['send_email'] = kwargs.get('send_email')
            else:
                raise TypeError(f"Invalid send_email type. It should be a boolean (bool).")
        else:
            request_object['send_email'] = False
            
        if kwargs.get('follow_envelope_order'):
            if isinstance(kwargs.get('follow_envelope_order'), int):
                request_object['follow_envelope_order'] = kwargs.get('follow_envelope_order')
            else:
                return False, "Invalid follow_envelope_order type. It should be a integer (int)."
        else:
            request_object['follow_envelope_order'] = None
            
            
        if kwargs.get('auto_reminder'):
            if isinstance(kwargs.get('auto_reminder'), int):
                request_object['auto_reminder'] = kwargs.get('auto_reminder')
            else:
                raise TypeError(f"Invalid auto_reminder type. It should be a type integer (int).")
        else:
            request_object['auto_reminder'] = 0
            
        
        if kwargs.get('number_of_reminders'):
            if isinstance(kwargs.get('number_of_reminders'), int):
                request_object['number_of_reminders'] = kwargs.get('number_of_reminders')
            else:
                raise TypeError(f"Invalid number_of_reminders type. It should be a type integer (int).")
        else:
            request_object['number_of_reminders'] = 3
            

            
        if kwargs.get('content'):
            request_object['content'] = kwargs.get('content')
            
            request_object['email_content'] = {
                'content' : kwargs.get('content'),
                'subject' : request_object['subject']
            }
        else:
            request_object['email_content'] = {
                'subject' : request_object['subject']
            }
            
        if kwargs.get('send_email_recipient'):
            if isinstance(kwargs.get('send_email_recipient'), bool):
                request_object['send_email_recipient'] = kwargs.get('send_email_recipient')
            else:
                raise TypeError(f"Invalid send_email_recipient type. It should be a boolean (bool).")
        else:
            request_object['send_email_recipient'] = False
            
            
            
            
        # print(request_object)
        
        request_object['envelope_documents'] = self.documents
        request_object['envelope_recepients'] = self.recipients
        request_object['from_sdk'] = True
        # print(request_object)
        
        
        url = self.api_domain+"/api/v1/send/envelope"
        payload = json.dumps(request_object)
        headers = {
            'api-key': self.api_key,
            'Content-Type': 'application/json'
        }

        # print(payload)
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 200:
            res = response.json()
            if res['status_code'] == 200:
                for i in res['signings_url']:
                    self.signing_url[i['recipient']] = i['signing_url']
                return res
            else:
                raise Exception(res['message'])
            
        elif response.status_code == 400:
            res = response.json()
            raise Exception(res['message'])
        else:
            raise EnvelopeSendingError()
        
        pass


class DocumentExtractor(WesignSDK):
    def __init__(self, api_uri, api_key, envelope_id):
        """
        Initiate Document Signing Process.
        :param str api_uri: the api_uri of wesign api domain.
        :param str api_key: the api_key provided by Wesign.com through webapp.
        :param int envelope_id: the id of envelope.
        """
        if api_uri in ['https://dev.wesign.com', 'https://api.wesign.com']:
            self.api_domain = api_uri
        else:
            raise InvalidHostError()
        
        self.api_domain = api_uri
        
        self.envelope_id = envelope_id
        
        if api_key:
            self.api_key = api_key
        else:
            raise ValueError(f"Invalid API key: {api_key}")
            
        self.envelope_documents = []
        self.user_id = self.validate_api_key()
        self.envelope = self.get_envelope_details(envelope_id)
    
    def get_envelope_details(self, envelope_id):
        """
        Get Envelope details.
        
        """
        url = self.api_domain+"/api/v1/envelope/details/"+str(envelope_id)

        
        headers = {
        'api-key': self.api_key,
        'Content-Type': 'application/json'
        }

        response = requests.request("GET", url, headers=headers)
        if response.status_code == 200:
            res = response.json()
            self.envelope_documents = res['envelope']['envelope_documents']
            return res['envelope']
        else:
            raise InvalidEnvelopeError()

        return None
    
    def list_documents(self):
        li = []
        for i in self.envelope_documents:
            li.append({
                'document_name' : i.get('document_name'),
                'is_attachment' : i.get('is_attachment'),
                'document_key' : i.get('document_key')
            })
        return li
    
    def download_documents(self, download_path='/'):
        if self.envelope_documents:
            for doc in self.envelope_documents:
                url = self.api_domain+"/api/v1/envelope/document/access?key="+str(doc.get('document_key'))

                payload = ""
                headers = {
                'api-key': self.api_key
                }
                response = requests.request("GET", url, headers=headers, data=payload)
                
                if response.status_code == 200:
                    
                    res = response.json()
                    
                    
                    file_url = res['url']
                    local_filename = doc.get('document_name')
                    if local_filename.split('.')[-1] == 'pdf':
                        pass
                    else:
                        local_filename = doc.get('document_name') + '.pdf'

                    response = requests.get(file_url)
                    local_filename = os.path.join(download_path, local_filename)
                    print('DOWNLOADING FILE : ', doc.get('document_name'))
                    with open(local_filename, 'wb') as file:
                        file.write(response.content)
                        
                else:
                    raise InvalidAPIKeyError()
        
        else:
            raise Exception("Documents not found.")    
        
    

# wesign_sdk = WesignSDK('https://dev.wesign.com','KDk8FTJBSsg5WrfPpyqIBelk8LzaGgnW8rM38npUWFrX3QOQC0s7zXQ7YdzuQtPuvOvIKah1zpXCAo73QB1NJHEIKucrGwPeS5R0IFyHbpfuQ24zolpmpeI4FSZzxEhfl70XvixyR5O343kO4PbquqVjUNs2GWOeBU5qpaxsxF92ohe4VNxhoNOTjgPARF0v4Iyz5lBR6HLrVb9xtrtpxDbOJgWXJd0QD1vPprdEL8Vr3tvc')
# # # # print(wesign_sdk)
# wesign_sdk.upload_documents('/home/mayur/Downloads/10-pg-blank.pdf')

# wesign_sdk.upload_documents('/home/mayur/Downloads/aaa.pdf')


# wesign_sdk = WesignSDK('https://dev.wesign.com','fQycaFgWoGbv1JmBO8wkDXqYKAESjdnTMSEGDD3XzoF5GlqWw1lHWsHnA3GeEiKY5NAjjH0jj51RrAhaeCpL6AQYfhk3TXovmDESZ29XBaIwGhL0OurLPOOLChPBKeVLfSmxnW6Ac6fNOJt7o74BY23c4dKD8vDMKQOkyY454irnp9OMWUi3hGAcHZvvC0E4k1rsQBd2wlOWnC0IQiY1igpNcbXii0UmfKhQGVRd5Zx3sy7n')


# wesign_sdk.upload_documents('/home/mayur/Downloads/claims agreement.pdf')



# data = {
#     "recipient_name": "mayur",
#     "recipient_email": "mayurbppatil@gmail.com",
#     "action": "needs_to_sign",
#     "meta_data":[{
#         "document_order" : 1,
#         "page_no" : 1,
#         "field_name": "signature",
#         "left" : 375,
#         "top" : 688,
#         "height":30,
#         "width":60
# }]
# }

# data = {
#         "recipient_name": "mayur",
#         "recipient_email": "mayurbppatil@gmail.com",
#         "action": "needs_to_sign",
#         "meta_data": [
#             {
#                 "page_no": 1,
#                 "left": 1,
#                 "top": 1,
#                 "width": 100,
#                 "height": 100,
#                 "document_order":1,
#                 "field_name": "signature",
#                 "include_date_name": True,
#                 "signature_with_border": True
#             },
            
#             {
#                 "page_no": 1,
#                 "left": 120,
#                 "top": 1,
#                 "width": 100,
#                 "height": 100,
#                 "document_order":1,
#                 "field_name": "initial",
#                 "include_date_name": None,
#                 "initial_with_border": False
#             },
            
#             {
#                 "page_no": 1,
#                 "left": 240,
#                 "top": 1,
#                 "width": 100,
#                 "height": 20,
#                 "document_order":1,
#                 "field_name": "email",
#                 "font_color" : "rgb(0,0,0)"
#             },
            
#             {
#                 "page_no": 1,
#                 "left": 1,
#                 "top": 150,
#                 "width": 100,
#                 "height": 20,
#                 "document_order":1,
#                 "field_name": "comment_text",
#                 "font_color" : "rgb(0,0,0)"
#             },
            
#             {
#                 "page_no": 1,
#                 "left": 120,
#                 "top": 150,
#                 "width": 100,
#                 "height": 20,
#                 "document_order":1,
#                 "field_name": "plain_text",
#                 "font_color" : "rgb(0,0,0)",
#                 "field_data" : "Field Data"
#             },
            
#             {
#                 "page_no": 1,
#                 "left": 240,
#                 "top": 150,
#                 "width": 100,
#                 "height": 100,
#                 "document_order":1,
#                 "field_name": "drawing",
#             },
            
#             {
#                 "page_no": 1,
#                 "left": 1,
#                 "top": 270,
#                 "width": 20,
#                 "height": 20,
#                 "document_order":1,
#                 "field_name": "attachment",
#                 "required_field_checkbox": True
#             },
            
           
            
#         ],
        
#     }
    
# print(wesign_sdk.documents)

# wesign_sdk.add_recipient(data)

# response = wesign_sdk.send_envelope(subject='subject', expiry_date="2024-12-07", enable_comments = True, follow_signing_order=True, enable_writing_id=True, auto_reminder=0, number_of_reminders=2, send_email=False)

# print(wesign_sdk.get_sign_url('mayurbppatil@gmail.com'))
# print(wesign_sdk.recipients)
# print(wesign_sdk.documents)


# wesign_doc = DocumentExtractor('https://dev.wesign.com','fQycaFgWoGbv1JmBO8wkDXqYKAESjdnTMSEGDD3XzoF5GlqWw1lHWsHnA3GeEiKY5NAjjH0jj51RrAhaeCpL6AQYfhk3TXovmDESZ29XBaIwGhL0OurLPOOLChPBKeVLfSmxnW6Ac6fNOJt7o74BY23c4dKD8vDMKQOkyY454irnp9OMWUi3hGAcHZvvC0E4k1rsQBd2wlOWnC0IQiY1igpNcbXii0UmfKhQGVRd5Zx3sy7n', 1163)
# # print(wesign_doc.list_documents('/home/mayur/Documents/sdk_download'))

# wesign_doc.download_documents('/home/mayur/Documents/')

if __name__ == "__main__":
    # Code to execute if run as a script
    # print("Running as a script")
    pass