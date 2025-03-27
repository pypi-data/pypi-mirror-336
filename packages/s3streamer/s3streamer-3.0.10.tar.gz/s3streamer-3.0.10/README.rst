==============
**s3streamer**
==============

Overview
--------

Stream files to AWS S3 using multipart upload.

.. image:: https://gitlab.com/fer1035_python/modules/pypi-s3streamer/-/raw/main/S3Streamer.png
   :width: 400
   :alt: Flowchart

A frontend module to upload files to AWS S3 storage. The module supports large files as it chunks them into smaller sizes and recombines them into the original file in the specified S3 bucket. It employs multiprocessing, and there is the option of specifying the size of each chunk as well as how many chunks to send in a single run. The defaults are listed in **Optional Arguments** below.  

The solution provides a dashboard in `CloudWatch <https://console.aws.amazon.com/cloudwatch/home#dashboards/>`_ to monitor file operations. You may also need to manually deploy the API in `API Gateway <https://console.aws.amazon.com/apigateway/>`_ after deployment and changes.

Prerequisites
-------------

- An AWS S3 bucket to receive uploads.
- An AWS Lambda function to perform backend tasks.
- The AWS `CloudFormation template <https://gitlab.com/fer1035_python/modules/pypi-s3streamer/-/tree/main/cloudformation/s3streamer.yaml>`_ to create these resources is available, or login to your AWS account and click on this `quick link <https://console.aws.amazon.com/cloudformation/home?#/stacks/create/review?templateURL=https://warpedlenses-public.s3.ap-southeast-1.amazonaws.com/cloudformation/s3streamer.yaml>`_.
- The endpoint URL and API key will be created by CloudFormation. They can be found in the `Lambda <https://console.aws.amazon.com/lambda/>`_ and `API Gateway <https://console.aws.amazon.com/apigateway/>`_ consoles.

Required Arguments
------------------

- Position 1: Filename (local full / relative path to the file)
- Position 2: Destination path in the S3 bucket
- Position 3: Endpoint URL
- Position 4: API key

Optional Arguments
------------------

- path: Destination path in the S3 bucket (default: /)
- parts: Number of multiprocessing parts to send simultaneously (default: 10)
- part_size: Size of each part in MB (default: 100)
- tmp_path: Location of local temporary directory to store temporary files created by the module (default: '/tmp')
- purge: Whether to purge the specified file instead of uploading it (default: False)
- force: Whether to force the upload even if the file already exists in the S3 bucket (default: False)

Usage
-----

Installation:

.. code-block:: BASH

   pip3 install s3streamer
   # or
   python3 -m pip install s3streamer

In Python3:

.. code-block:: PYTHON

   # To upload a new file.
   import s3streamer

   if __name__ == "__main__":
      response = s3streamer.stream(
         "myfile.iso",
         "installer/images",
         "https://s3streamer.api.example.com/upload",
         "my-api-key",
         parts=5,
         part_size=30,
         tmp_path="/Users/me/Desktop",
         purge=False
      )
   
      print(response)

   # To remove a file from S3.
   import s3streamer

   if __name__ == "__main__":
      response = s3streamer.stream(
         "myfile.iso", 
         "installer/images", 
         purge=True
      )

      print(response)

To simplyfy operations, the endpoint and API key can also be set as environment variables:

.. code-block:: BASH

   export S3STREAMER_ENDPOINT="https://s3streamer.api.example.com/upload"
   export S3STREAMER_API_KEY="my-api-key"

By doing so, the upload command can be simplified to:

.. code-block:: PYTHON

   import s3streamer

   if __name__ == "__main__":
      response = s3streamer.stream(
         "myfile.iso",
         "installer/images"
      )

      print(response)

with default values for the optional (keyword) arguments.  

If the upload is successful, the file will be available at **installer/images/myfile.iso**.
