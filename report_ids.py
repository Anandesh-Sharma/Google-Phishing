import requests
from helpers import get_token, get_a_proxy
import json


def request(email, report_id, add_message):
    TOKEN = get_token('6LdZHQYTAAAAAFnofYfPjNlXpxWAqTwfLh9d0zL2',
                      f'https://support.google.com/google-ads/troubleshooter/4578507?ai={report_id}&hl=en-US#ts=6006595')
    payload = {
        "resource": {
            "form_id": "vio_other_aw_policy",
            "header": [
                {
                    "name": "userAdType",
                    "value": "type_search"
                },
                {
                    "name": "violating_policy",
                    "value": "cyber_attack"
                },
                {
                    "name": "dang_prod_details",
                    "value": "phishing_ie_stealing_credentials_financial_details_etc"
                },
                {
                    "name": "contact_email",
                    "value": email
                },
                {
                    "name": "clickstring_ie",
                    "value": report_id
                },
                {
                    "name": "provide_details_req",
                    "value": add_message
                },
                {
                    "name": "product_google_search",
                    "value": "google_ads"
                },
                {
                    "name": "policy_cyber_attack",
                    "value": "cyber_attack"
                },
                {
                    "name": "nn:---- Automatically added fields ----",
                    "value": ""
                },
                {
                    "name": "Language",
                    "value": "en-GB"
                },
                {
                    "name": "IIILanguage",
                    "value": "en-GB"
                },
                {
                    "name": "country_code",
                    "value": "US"
                },
                {
                    "name": "auto-helpcenter-id",
                    "value": "177"  # it could be different for US
                },
                {
                    "name": "auto-helpcenter-name",
                    "value": "google-ads"
                },
                {
                    "name": "auto-internal-helpcenter-name",
                    "value": "adwords3"
                },
                {
                    "name": "auto-full-url",
                    "value": f"https://support.google.com/google-ads/troubleshooter/4578507?ai={report_id}&hl=en-US#ts=6006595"
                },
                {
                    "name": "auto-user-logged-in",
                    "value": "false"
                },
                {
                    "name": "auto-user-was-internal",
                    "value": "false"
                },
                {
                    "name": "IssueType",
                    "value": "vio_other_aw_policy"
                },
                {
                    "name": "form-id",
                    "value": "vio_other_aw_policy"
                },
                {
                    "name": "form",
                    "value": "vio_other_aw_policy"
                },
                {
                    "name": "subject-line-field-id",
                    "value": ""
                },
                {
                    "name": "body-text-field-id",
                    "value": ""
                },
                {
                    "name": "AutoDetectedBrowser",
                    "value": "Chrome 18.0.1025.166"
                },
                {
                    "name": "AutoDetectedOS",
                    "value": "Android 4.2.1"
                },
                {
                    "name": "MendelExperiments",
                    "value": "10800112,10800235,10800244,10800253,10800284,10800286,10800300,10800319,10800380,10800396,10800403,10800523,10800561,10800589,10800621,10800639,10800691,10800702,10800704"
                },
                {
                    "name": "Form.support-content-visit-id",
                    "value": "637507546889350471-1618777111"  # have a expiry
                },
                {
                    "name": "experiment_0_id",
                    "value": ""
                },
                {
                    "name": "experiment_0_status",
                    "value": "OFF"
                },
                {
                    "name": "experiment_1_id",
                    "value": ""
                },
                {
                    "name": "experiment_1_status",
                    "value": "OFF"
                }
            ],
            "subject": "",
            "content": "",
            "validate_only": False,
            "validation_info": "Cgp1c2VyQWRUeXBlChB2aW9sYXRpbmdfcG9saWN5ChlzaG9wcGluZ19wb2xpY3lfdmlvbGF0aW9uChh0cmFkZW1hcmtfc3BlY2lmaWNhdGlvbnMKEmNvdW50ZXJmZWl0X3NlYXJjaAoQdHJhZGVtYXJrX3NlYXJjaAoSdHJhZGVtYXJrX3Nob3BwaW5nChRjb3VudGVyZmVpdF9zaG9wcGluZwoRZGFuZ19wcm9kX2RldGFpbHMKFGxlZ2FsX2lzc3Vlc19kZXRhaWxzCgxldV91c2VyX3RleHQKDWNvbnRhY3RfZW1haWwKDmNsaWNrc3RyaW5nX2llChljbGlja3N0cmluZ19pZV9zaG9wcGluZ18xChZjbGlja3N0cmluZ19pZV9vdGhlcl8xChljbGlja3N0cmluZ19pZV9kaXNwbGF5X2FkChNwcm92aWRlX2RldGFpbHNfb3B0ChNwcm92aWRlX2RldGFpbHNfcmVxChVwcm9kdWN0X2dvb2dsZV9zZWFyY2gKF3Byb2R1Y3RfZ29vZ2xlX3Nob3BwaW5nCg9wcm9kdWN0X3lvdXR1YmUKE3BvbGljeV9jeWJlcl9hdHRhY2sKFnBvbGljeV9oYXRlZnVsX2NvbnRlbnQKE3BvbGljeV9sZWdhbF9pc3N1ZXMKGXBvbGljeV9taXNsZWFkaW5nX2NvbnRlbnQKJXBvbGljeV9kYW5nZXJvdXNfcHJvZHVjdHNfb3Jfc2VydmljZXMKIHBvbGljeV9udWRpdHlfYW5kX3NleHVhbF9jb250ZW50ChBwb2xpY3lfdHJhZGVtYXJrChJwb2xpY3lfY291bnRlcmZlaXQKDHBvbGljeV9vdGhlcgodcG9saWN5X2luYWNjdXJhdGVfaW5mb3JtYXRpb24KOnBvbGljeV9wcm9ibGVtYXRpY19wcm9tb3Rpb25fb2ZfaGVhbHRoY2FyZV9yZWxhdGVkX3Byb2R1Y3QSGQoKdXNlckFkVHlwZRILdHlwZV9zZWFyY2gSGwoKdXNlckFkVHlwZRINdHlwZV9zaG9wcGluZxIaCgp1c2VyQWRUeXBlEgx0eXBlX3lvdXR1YmUSGAoKdXNlckFkVHlwZRIKdHlwZV9vdGhlchIgChB2aW9sYXRpbmdfcG9saWN5EgxjeWJlcl9hdHRhY2sSHQoQdmlvbGF0aW5nX3BvbGljeRIJaGF0ZV9jb250EiAKEHZpb2xhdGluZ19wb2xpY3kSDGxlZ2FsX2lzc3VlcxIjChB2aW9sYXRpbmdfcG9saWN5Eg9taXNsZWFkaW5nX2NvbnQSHQoQdmlvbGF0aW5nX3BvbGljeRIJZGFuZ19wcm9kEhwKEHZpb2xhdGluZ19wb2xpY3kSCHNleF9jb250EicKEHZpb2xhdGluZ19wb2xpY3kSE3RyYWRlbWFya192aW9sYXRpb24SLwoQdmlvbGF0aW5nX3BvbGljeRIbY291bnRlcmZlaXRfZ29vZHNfdmlvbGF0aW9uEhcKEHZpb2xhdGluZ19wb2xpY3kSA290aBImChlzaG9wcGluZ19wb2xpY3lfdmlvbGF0aW9uEgloYXRlX2NvbnQSMwoZc2hvcHBpbmdfcG9saWN5X3Zpb2xhdGlvbhIWaW5hY2N1cmF0ZV9pbmZvcm1hdGlvbhInChlzaG9wcGluZ19wb2xpY3lfdmlvbGF0aW9uEgpoZWFsdGhfbWVkEiYKGXNob3BwaW5nX3BvbGljeV92aW9sYXRpb24SCWRhbmdfcHJvZBIqChlzaG9wcGluZ19wb2xpY3lfdmlvbGF0aW9uEg1hZHVsdF9jb250ZW50EjAKGXNob3BwaW5nX3BvbGljeV92aW9sYXRpb24SE3RyYWRlbWFya192aW9sYXRpb24SOAoZc2hvcHBpbmdfcG9saWN5X3Zpb2xhdGlvbhIbY291bnRlcmZlaXRfZ29vZHNfdmlvbGF0aW9uEiAKGXNob3BwaW5nX3BvbGljeV92aW9sYXRpb24SA290aBJVChh0cmFkZW1hcmtfc3BlY2lmaWNhdGlvbnMSOWNsb2FraW5nX2llX2RlY2VwdGl2ZV9yZWRpcmVjdGlvbl91cG9uX2NsaWNraW5nX29uX3RoZV9hZBI0Chh0cmFkZW1hcmtfc3BlY2lmaWNhdGlvbnMSGGNvbnRlbnRfaW52b2x2aW5nX21pbm9ycxIhChh0cmFkZW1hcmtfc3BlY2lmaWNhdGlvbnMSBWRydWdzEisKGHRyYWRlbWFya19zcGVjaWZpY2F0aW9ucxIPZXVfdXNlcl9jb25zZW50EiUKGHRyYWRlbWFya19zcGVjaWZpY2F0aW9ucxIJZmFrZV9uZXdzElkKGHRyYWRlbWFya19zcGVjaWZpY2F0aW9ucxI9ZmFsc2VfY2xhaW1zX2Fib3V0X2lkZW50aXR5X3F1YWxpZmljYXRpb25zX3Byb2R1Y3Rfb3Jfc2VydmljZRI5Chh0cmFkZW1hcmtfc3BlY2lmaWNhdGlvbnMSHWhlYWx0aGNhcmVfcHJvZHVjdF9vcl9zZXJ2aWNlElcKGHRyYWRlbWFya19zcGVjaWZpY2F0aW9ucxI7aW5hY2N1cmF0ZV9pbmZvcm1hdGlvbl9pZV9wcmljaW5nX2F2YWlsYWJpbGl0eV9zaGlwcGluZ19ldGMScgoYdHJhZGVtYXJrX3NwZWNpZmljYXRpb25zElZtYWx3YXJlX2llX2RlY2VwdGl2ZV9yZWRpcmVjdGlvbl93aXRob3V0X2NsaWNraW5nX29uX3RoZV9hZF91bmF1dGhvcml6ZWRfZG93bmxvYWRzX2V0YxJkChh0cmFkZW1hcmtfc3BlY2lmaWNhdGlvbnMSSG1pc2xlYWRpbmdfdXNlX29mX215X3RyYWRlX25hbWVfY29tcGFueV9uYW1lX29yX3JlZ2lzdGVyZWRfYnVzaW5lc3NfbmFtZRIuChh0cmFkZW1hcmtfc3BlY2lmaWNhdGlvbnMSEm51ZGl0eV9wb3Jub2dyYXBoeRIhChh0cmFkZW1hcmtfc3BlY2lmaWNhdGlvbnMSBW90aGVyElIKGHRyYWRlbWFya19zcGVjaWZpY2F0aW9ucxI2cGhpc2hpbmdfaWVfc3RlYWxpbmdfY3JlZGVudGlhbHNfZmluYW5jaWFsX2RldGFpbHNfZXRjEmAKGHRyYWRlbWFya19zcGVjaWZpY2F0aW9ucxJEcHJpY2VfaW5mb3JtYXRpb25fdGhhdF9kb2VzbnRfbWF0Y2hfaW5mb3JtYXRpb25fb25fbWVyY2hhbnRzX3dlYnNpdGUSSAoYdHJhZGVtYXJrX3NwZWNpZmljYXRpb25zEixwcm9kdWN0X2lzX25vdF9pbl9zdG9ja19vbl9tZXJjaGFudHNfd2Vic2l0ZRJFChh0cmFkZW1hcmtfc3BlY2lmaWNhdGlvbnMSKXByb2R1Y3RzX29yX3NlcnZpY2VzX3RoYXRfYXJlbnRfYXZhaWxhYmxlEmMKGHRyYWRlbWFya19zcGVjaWZpY2F0aW9ucxJHc2hpcHBpbmdfaW5mb3JtYXRpb25fdGhhdF9kb2VzbnRfbWF0Y2hfaW5mb3JtYXRpb25fb25fbWVyY2hhbnRzX3dlYnNpdGUSIwoYdHJhZGVtYXJrX3NwZWNpZmljYXRpb25zEgd0b2JhY2NvEjYKGHRyYWRlbWFya19zcGVjaWZpY2F0aW9ucxIadHJhZGVtYXJrc19pbl9zaG9wcGluZ19hZHMSSAoYdHJhZGVtYXJrX3NwZWNpZmljYXRpb25zEix2aW9sYXRpb25fb2ZfcHJpbnRlcl9jYXJ0cmlkZ2VzX3JlcXVpcmVtZW50cxIjChh0cmFkZW1hcmtfc3BlY2lmaWNhdGlvbnMSB3dlYXBvbnMSTgoRZGFuZ19wcm9kX2RldGFpbHMSOWNsb2FraW5nX2llX2RlY2VwdGl2ZV9yZWRpcmVjdGlvbl91cG9uX2NsaWNraW5nX29uX3RoZV9hZBItChFkYW5nX3Byb2RfZGV0YWlscxIYY29udGVudF9pbnZvbHZpbmdfbWlub3JzEhoKEWRhbmdfcHJvZF9kZXRhaWxzEgVkcnVncxIkChFkYW5nX3Byb2RfZGV0YWlscxIPZXVfdXNlcl9jb25zZW50Eh4KEWRhbmdfcHJvZF9kZXRhaWxzEglmYWtlX25ld3MSUgoRZGFuZ19wcm9kX2RldGFpbHMSPWZhbHNlX2NsYWltc19hYm91dF9pZGVudGl0eV9xdWFsaWZpY2F0aW9uc19wcm9kdWN0X29yX3NlcnZpY2USMgoRZGFuZ19wcm9kX2RldGFpbHMSHWhlYWx0aGNhcmVfcHJvZHVjdF9vcl9zZXJ2aWNlElAKEWRhbmdfcHJvZF9kZXRhaWxzEjtpbmFjY3VyYXRlX2luZm9ybWF0aW9uX2llX3ByaWNpbmdfYXZhaWxhYmlsaXR5X3NoaXBwaW5nX2V0YxJrChFkYW5nX3Byb2RfZGV0YWlscxJWbWFsd2FyZV9pZV9kZWNlcHRpdmVfcmVkaXJlY3Rpb25fd2l0aG91dF9jbGlja2luZ19vbl90aGVfYWRfdW5hdXRob3JpemVkX2Rvd25sb2Fkc19ldGMSXQoRZGFuZ19wcm9kX2RldGFpbHMSSG1pc2xlYWRpbmdfdXNlX29mX215X3RyYWRlX25hbWVfY29tcGFueV9uYW1lX29yX3JlZ2lzdGVyZWRfYnVzaW5lc3NfbmFtZRInChFkYW5nX3Byb2RfZGV0YWlscxISbnVkaXR5X3Bvcm5vZ3JhcGh5EhoKEWRhbmdfcHJvZF9kZXRhaWxzEgVvdGhlchJLChFkYW5nX3Byb2RfZGV0YWlscxI2cGhpc2hpbmdfaWVfc3RlYWxpbmdfY3JlZGVudGlhbHNfZmluYW5jaWFsX2RldGFpbHNfZXRjElkKEWRhbmdfcHJvZF9kZXRhaWxzEkRwcmljZV9pbmZvcm1hdGlvbl90aGF0X2RvZXNudF9tYXRjaF9pbmZvcm1hdGlvbl9vbl9tZXJjaGFudHNfd2Vic2l0ZRJBChFkYW5nX3Byb2RfZGV0YWlscxIscHJvZHVjdF9pc19ub3RfaW5fc3RvY2tfb25fbWVyY2hhbnRzX3dlYnNpdGUSPgoRZGFuZ19wcm9kX2RldGFpbHMSKXByb2R1Y3RzX29yX3NlcnZpY2VzX3RoYXRfYXJlbnRfYXZhaWxhYmxlElwKEWRhbmdfcHJvZF9kZXRhaWxzEkdzaGlwcGluZ19pbmZvcm1hdGlvbl90aGF0X2RvZXNudF9tYXRjaF9pbmZvcm1hdGlvbl9vbl9tZXJjaGFudHNfd2Vic2l0ZRIcChFkYW5nX3Byb2RfZGV0YWlscxIHdG9iYWNjbxIvChFkYW5nX3Byb2RfZGV0YWlscxIadHJhZGVtYXJrc19pbl9zaG9wcGluZ19hZHMSQQoRZGFuZ19wcm9kX2RldGFpbHMSLHZpb2xhdGlvbl9vZl9wcmludGVyX2NhcnRyaWRnZXNfcmVxdWlyZW1lbnRzEhwKEWRhbmdfcHJvZF9kZXRhaWxzEgd3ZWFwb25zElEKFGxlZ2FsX2lzc3Vlc19kZXRhaWxzEjljbG9ha2luZ19pZV9kZWNlcHRpdmVfcmVkaXJlY3Rpb25fdXBvbl9jbGlja2luZ19vbl90aGVfYWQSMAoUbGVnYWxfaXNzdWVzX2RldGFpbHMSGGNvbnRlbnRfaW52b2x2aW5nX21pbm9ycxIdChRsZWdhbF9pc3N1ZXNfZGV0YWlscxIFZHJ1Z3MSJwoUbGVnYWxfaXNzdWVzX2RldGFpbHMSD2V1X3VzZXJfY29uc2VudBIhChRsZWdhbF9pc3N1ZXNfZGV0YWlscxIJZmFrZV9uZXdzElUKFGxlZ2FsX2lzc3Vlc19kZXRhaWxzEj1mYWxzZV9jbGFpbXNfYWJvdXRfaWRlbnRpdHlfcXVhbGlmaWNhdGlvbnNfcHJvZHVjdF9vcl9zZXJ2aWNlEjUKFGxlZ2FsX2lzc3Vlc19kZXRhaWxzEh1oZWFsdGhjYXJlX3Byb2R1Y3Rfb3Jfc2VydmljZRJTChRsZWdhbF9pc3N1ZXNfZGV0YWlscxI7aW5hY2N1cmF0ZV9pbmZvcm1hdGlvbl9pZV9wcmljaW5nX2F2YWlsYWJpbGl0eV9zaGlwcGluZ19ldGMSbgoUbGVnYWxfaXNzdWVzX2RldGFpbHMSVm1hbHdhcmVfaWVfZGVjZXB0aXZlX3JlZGlyZWN0aW9uX3dpdGhvdXRfY2xpY2tpbmdfb25fdGhlX2FkX3VuYXV0aG9yaXplZF9kb3dubG9hZHNfZXRjEmAKFGxlZ2FsX2lzc3Vlc19kZXRhaWxzEkhtaXNsZWFkaW5nX3VzZV9vZl9teV90cmFkZV9uYW1lX2NvbXBhbnlfbmFtZV9vcl9yZWdpc3RlcmVkX2J1c2luZXNzX25hbWUSKgoUbGVnYWxfaXNzdWVzX2RldGFpbHMSEm51ZGl0eV9wb3Jub2dyYXBoeRIdChRsZWdhbF9pc3N1ZXNfZGV0YWlscxIFb3RoZXISTgoUbGVnYWxfaXNzdWVzX2RldGFpbHMSNnBoaXNoaW5nX2llX3N0ZWFsaW5nX2NyZWRlbnRpYWxzX2ZpbmFuY2lhbF9kZXRhaWxzX2V0YxJcChRsZWdhbF9pc3N1ZXNfZGV0YWlscxJEcHJpY2VfaW5mb3JtYXRpb25fdGhhdF9kb2VzbnRfbWF0Y2hfaW5mb3JtYXRpb25fb25fbWVyY2hhbnRzX3dlYnNpdGUSRAoUbGVnYWxfaXNzdWVzX2RldGFpbHMSLHByb2R1Y3RfaXNfbm90X2luX3N0b2NrX29uX21lcmNoYW50c193ZWJzaXRlEkEKFGxlZ2FsX2lzc3Vlc19kZXRhaWxzEilwcm9kdWN0c19vcl9zZXJ2aWNlc190aGF0X2FyZW50X2F2YWlsYWJsZRJfChRsZWdhbF9pc3N1ZXNfZGV0YWlscxJHc2hpcHBpbmdfaW5mb3JtYXRpb25fdGhhdF9kb2VzbnRfbWF0Y2hfaW5mb3JtYXRpb25fb25fbWVyY2hhbnRzX3dlYnNpdGUSHwoUbGVnYWxfaXNzdWVzX2RldGFpbHMSB3RvYmFjY28SMgoUbGVnYWxfaXNzdWVzX2RldGFpbHMSGnRyYWRlbWFya3NfaW5fc2hvcHBpbmdfYWRzEkQKFGxlZ2FsX2lzc3Vlc19kZXRhaWxzEix2aW9sYXRpb25fb2ZfcHJpbnRlcl9jYXJ0cmlkZ2VzX3JlcXVpcmVtZW50cxIfChRsZWdhbF9pc3N1ZXNfZGV0YWlscxIHd2VhcG9ucw",
            "language": "en-GB",
            "helpcenter_id": "177",
            "active_experiments": "CjVBZFdvcmRzX0NTYXRfRGlzc2F0X0RyaXZlcnNfRXhwZXJpbWVudDo6Q29udHJvbF9ncm91cAoyQWRXb3Jkc19Db250ZW50X1RlbXBsYXRlX0V4cGVyaW1lbnQ6OkNvbnRyb2xfZ3JvdXA",
            "referer": "",
            "referer_title": "",
            "timezone_offset_minutes": -330,
            "form_frd_values": [
                {
                    "frd_value": {
                        "frd_context": {
                            "frd_identifier": 8000043,
                            "context_type": 15
                        },
                        "frd_identifier": 8000043,
                        "selected_value_list": {
                            "enum_value_identifiers": {
                                "value": [
                                    "trust_safety"
                                ]
                            }
                        }
                    },
                    "frd_id": 8000043,
                    "frd_value_type": 4,
                    "hd": []
                },
                {
                    "frd_value": {
                        "frd_context": {
                            "frd_identifier": 8000085,
                            "context_type": 15
                        },
                        "frd_identifier": 8000085,
                        "selected_value_list": {
                            "enum_value_identifiers": {
                                "value": [
                                    "engineering"
                                ]
                            }
                        }
                    },
                    "frd_id": 8000085,
                    "frd_value_type": 4,
                    "hd": []
                },
                {
                    "frd_value": {
                        "frd_context": {
                            "frd_identifier": 8000157,
                            "context_type": 15
                        },
                        "frd_identifier": 8000157,
                        "selected_value_list": {
                            "enum_value_identifiers": {
                                "value": [
                                    "needs_automation"
                                ]
                            }
                        }
                    },
                    "frd_id": 8000157,
                    "frd_value_type": 4,
                    "hd": []
                },
                {
                    "frd_value": {
                        "frd_context": {
                            "frd_identifier": 8000046,
                            "context_type": 15
                        },
                        "frd_identifier": 8000046,
                        "selected_value_list": {
                            "enum_value_identifiers": {
                                "value": [
                                    "user_reports"
                                ]
                            }
                        }
                    },
                    "frd_id": 8000046,
                    "frd_value_type": 4,
                    "hd": []
                },
                {
                    "frd_value": {
                        "frd_context": {
                            "frd_identifier": 8000016,
                            "context_type": 15
                        },
                        "frd_identifier": 8000016,
                        "selected_value_list": {
                            "enum_value_identifiers": {
                                "value": [
                                    "cases"
                                ]
                            }
                        }
                    },
                    "frd_id": 8000016,
                    "frd_value_type": 4,
                    "hd": []
                },
                {
                    "frd_value": {
                        "frd_context": {
                            "frd_identifier": 8000007,
                            "context_type": 15
                        },
                        "frd_identifier": 8000007,
                        "selected_value_list": {
                            "enum_value_identifiers": {
                                "value": [
                                    "gmr"
                                ]
                            }
                        }
                    },
                    "frd_id": 8000007,
                    "frd_value_type": 4,
                    "hd": []
                },
                {
                    "frd_value": {
                        "frd_context": {
                            "frd_identifier": 8000078,
                            "context_type": 15
                        },
                        "frd_identifier": 8000078,
                        "selected_value_list": {
                            "enum_value_identifiers": {
                                "value": [
                                    "en_us"
                                ]
                            }
                        }
                    },
                    "frd_id": 8000078,
                    "frd_value_type": 4,
                    "hd": []
                },
                {
                    "frd_value": {
                        "frd_context": {
                            "frd_identifier": 8000041,
                            "context_type": 15
                        },
                        "frd_identifier": 8000041,
                        "selected_value_list": {
                            "enum_value_identifiers": {
                                "value": [
                                    "external"
                                ]
                            }
                        }
                    },
                    "frd_id": 8000041,
                    "frd_value_type": 4,
                    "hd": []
                },
                {
                    "frd_value": {
                        "frd_context": {
                            "frd_identifier": 8000017,
                            "context_type": 15
                        },
                        "frd_identifier": 8000017,
                        "selected_value_list": {
                            "enum_value_identifiers": {
                                "value": [
                                    "support_content"
                                ]
                            }
                        }
                    },
                    "frd_id": 8000017,
                    "frd_value_type": 4,
                    "hd": []
                },
                {
                    "frd_value": {
                        "frd_context": {
                            "frd_identifier": 8000083,
                            "context_type": 15
                        },
                        "frd_identifier": 8000083,
                        "selected_value_list": {
                            "enum_value_identifiers": {
                                "value": [
                                    "form"
                                ]
                            }
                        }
                    },
                    "frd_id": 8000083,
                    "frd_value_type": 4,
                    "hd": []
                },
                {
                    "frd_value": {
                        "frd_context": {
                            "frd_identifier": 8000103,
                            "context_type": 15
                        },
                        "frd_identifier": 8000103,
                        "selected_value_list": {
                            "enum_value_identifiers": {
                                "value": [
                                    "help_center"
                                ]
                            }
                        }
                    },
                    "frd_id": 8000103,
                    "frd_value_type": 4,
                    "hd": []
                },
                {
                    "frd_value": {
                        "frd_identifier": 8000104,
                        "frd_context": {
                            "frd_identifier": 8000104,
                            "context_type": 15
                        },
                        "selected_value_list": {
                            "enum_value_identifiers": {
                                "value": [
                                    "direct_to_form"
                                ]
                            }
                        }
                    },
                    "frd_id": 8000104
                }
            ],
            "parent_case_name": "",
            "submission_channel": 0,
            "cases_attachment": []
        },
        "recaptcha_response": TOKEN
    }
    headers = {
        'authority': 'support.google.com',
        # 'x-supportcontent-allowapicookieauth': 'true',
        # 'x-supportcontent-xsrftoken': '',
        'user-agent': 'Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19',
        'content-type': 'text/plain;charset=UTF-8',
        'accept': '*/*',
        'origin': 'https://support.google.com',
        'x-client-data': 'CI6KywE=',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://support.google.com/google-ads/troubleshooter/4578507?ai={}&hl=en-US'.format(report_id),
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }
    url = "https://support.google.com/apis/cufinsert?v=0&psd=%7B%7D&helpcenter=google-ads&hl=en-GB&key=support-content&request_source=1&service_configuration=&mendel_ids=10800235,10800244,10800253,10800284,10800286,10800300,10800380,10800396,10800403,10800523,10800561,10800589,10800621,10800639,10800691,10800702,10800704,10800112"
    try:
        response = requests.post(url=url, data=json.dumps(payload), headers=headers, proxies=get_a_proxy()).json()
        if response["result"][0] == "ACCEPTED":
            return {'status': True, 'message': 'Success', 'google': 'report_ids', 'report_id': report_id}
    except Exception as e:
        return {'status': False, 'message': str(e), 'google': 'report_ids', 'report_id': report_id}
