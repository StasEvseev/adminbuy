import boto3
from flask import render_template
from flask.ext.script import Command


class UploadStaticFiles(Command):
    def run(self):
        import os
        script_dir = os.path.dirname(os.path.dirname(__file__))

        with open(os.path.join(script_dir, 'static/index.html'), 'w') as f:
            f.write(render_template("index.html").encode('utf8'))

        with open(os.path.join(script_dir, 'static/home.html'), 'w') as f:
            f.write(render_template('home.html').encode('utf8'))
        # from app import app
        # app.upload_static_files(app)

        # user = app.config.get('AWS_ACCESS_KEY_ID')
        # password = app.config.get('AWS_SECRET_ACCESS_KEY')
        # bucket_name = app.config.get('FLASKS3_BUCKET_NAME')
        # location = app.config.get('FLASKS3_REGION')

        # s3 = boto3.client("s3",
        #                   region_name=location,
        #                   aws_access_key_id=user,
        #                   aws_secret_access_key=password)
        #
        # s3.put_object(Bucket=bucket_name,
        #               Key='index.html',
        #               Body=render_template("index.html").encode('utf8'),
        #               ACL="public-read",
        #               ContentType='text/html')
        # s3.put_object(Bucket=bucket_name,
        #               Key='home.html',
        #               Body=render_template("home.html").encode('utf8'),
        #               ACL="public-read",
        #               ContentType='text/html')
