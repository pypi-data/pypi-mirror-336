import requests
import json
import hashlib
import base64
import time
from phonepe_transaction.generate_transactionID import gen_ids
import webbrowser
from phonepe_transaction.env_details import salt_key, merchant_id

class Payment:
    
    def __init__(self):
        self.pay_api = "https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/pay"
        self.salt_index = 1
        self.merchant_id = merchant_id
        self.transaction = gen_ids()
        self.salt_key = salt_key

    def InitalizePayment(self, user_id, amount,MobileNumber,redirectUrl, CallbackUrl = None, salt_key = None, transaction_id = None,merchant_id = None, payment_page_redirect = False):
        
        if salt_key is None:
            salt_key = self.salt_key
        
        if transaction_id is None: 
            transaction_id = self.transaction.generate_id()

        if merchant_id is None:
            merchant_id = self.merchant_id


        def gen_x_verify_key(payload, salt_key, salt_index):
            encode_str = base64.b64encode(payload).decode('utf-8')
            data = f"{encode_str}/pg/v1/pay{salt_key}"
            hash_data = hashlib.sha256(data.encode("utf-8")).hexdigest()
            checksum = f"{hash_data}###{salt_index}"
    
            return checksum, encode_str
        
        try:

            payload = {
                "merchantId" : merchant_id,
                "merchantTransactionId" : transaction_id,
                "merchantUserId" : str(user_id),
                "amount" : int(amount * 100),
                "redirectUrl" : redirectUrl,
                "redirectMode" : "REDIRECT",
                "callbackUrl" : 'http://annc.com',
                "mobileNumber" : MobileNumber,
                "paymentInstrument" : {
                    "type" : "PAY_PAGE"
                }
            }
            
            payload_str = json.dumps(payload).encode('utf-8')

            xverify, encoded_str = gen_x_verify_key(payload_str, self.salt_key, self.salt_index)

            data = {
                "request" : encoded_str
            }     

            headers = {
                "Accept" : "application/json",
                "Content-Type" : "application/json",
                "X-VERIFY" : xverify,
            }   

            retry = 0
            while retry < 5:
                self.response = requests.post(self.pay_api, json=data, headers=headers)
                if self.response.status_code == 429:
                    retry += 1
                    print("Getting An error. Wait Retrying....")
                    time.sleep(10)

                elif self.response.status_code == 200:
                    print("Payment Initalized Successfully...")
                    print(f"Response : {self.response.json()}")
                    print(f"\n Repsonse Code : {self.response.status_code}\nResponse Message : {self.response.json()['code']}\n")
                    
                    if payment_page_redirect == True:
                        redirect = self.response.json()['data']['instrumentResponse']['redirectInfo']['url']
                        webbrowser.open(redirect)
                        time.sleep(60*3)

                    # self.CheckPaymentStatus(transaction_id=transaction_id, merchant_id=self.merchant_id, salt_key=self.salt_key)
                    break

                else:
                    print(f"Error While Initializing Payment Status: {self.response.status_code}")
                    print(f"Respone : {self.response.text}")
                    break
            
            else:
                raise Exception("Unable to process your request. Failed in all 5 attempts! Try Again!!")
        
        except Exception as e:
            print(f"Exception Raised : {e}")



    def CheckPaymentStatus(self, transaction_id, merchant_id = None, salt_key = None):
        
        if salt_key is None:
            salt_key = self.salt_key

        if merchant_id is None:
            merchant_id = self.merchant_id
        
        def generate_x_verify_check_status(merchant_id, merchantTransactionId, salt_key, salt_index):
            sha256_data = f"/pg/v1/status/{merchant_id}/{merchantTransactionId}{salt_key}"

            hash_data = hashlib.sha256(sha256_data.encode('utf-8')).hexdigest()
            x_verify = f"{hash_data}###{salt_index}"
        
            return x_verify

        

        api = f"https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/status/{merchant_id}/{transaction_id}"

        x_verify = generate_x_verify_check_status(merchant_id=merchant_id, merchantTransactionId=transaction_id, salt_key=self.salt_key, salt_index=self.salt_index)

        headers = {
            "Accept" : "application/json",
            "Content-Type" : "application/json",
            "X-VERIFY" : x_verify,
            "X-MERCHANT-ID" : merchant_id
        }

        respond = requests.get(api, headers=headers)

        print("Checking Payment Status.... wait..")
        time.sleep(5)

        retry = 0
        while retry < 5:
            if respond.status_code == 429:
                retry += 1
                print("Getting An error While Checking the Payment Status...")
                time.sleep(10)
            
            elif respond.status_code == 200:
                print("Payment Status : \n")
                print(f"Response : {respond.json()}")
                print(f"\n Response Code: {respond.status_code}\nResponse status : {respond.json()['code']}\nResponse Message : {respond.json()['message']}\n")
                break

            else:
                print(f"Error While Checking Payment Status: {respond.status_code}")
                print(f"Response : {respond.text}")
                break
        else:
            raise Exception("Unable to process payment status Checking Request. Failed in all 5 attempts! Try Again Manually...")



if __name__ == "__main__":
    pay = Payment()
    pay.InitalizePayment(
        user_id="DEV101",
        amount=100,
        MobileNumber=8120098465,
        redirectUrl= "http://annc.com"
    )