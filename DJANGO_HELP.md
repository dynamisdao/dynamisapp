# Dynamis Django Configuration

The following configuration options are available to configure the Django
application.


## `DJANGO_SECRET_KEY`

* required: **true**
* default: **N/A**
* https://docs.djangoproject.com/en/1.9/ref/settings/#secret-key

Sets the secret key that django will use.


## `DJANGO_DEBUG`

* required: **false**
* default: **false**
* https://docs.djangoproject.com/en/1.9/ref/settings/#debug

Should the application be run in debug mode.  Should **always** be false in
production settings.


## `DJANGO_DEBUG_TOOLBAR_ENABLED`

* required: **false**
* default: **false**
* https://github.com/django-debug-toolbar/django-debug-toolbar

Should the debug toolbar be enabled.  This should only be used in development
environments.


## `DJANGO_EMAIL_BACKEND`

* required: **true**
* default: **N/A**
* https://docs.djangoproject.com/en/1.9/ref/settings/#email-backend

Which email backend django should use to send emails.


## `DJANGO_DATABASE_ENGINE`

* required: **true**
* default: **django.db.backends.sqlite3**

A Database Engine.

## `DJANGO_DATABASE_NAME` 
* required: **true**
* default: **dynamisappdb**

A Database name.

## `DJANGO_DATABASE_USER` 
* required: **true**
* default: **N/A**

A Database user account.

## `DJANGO_DATABASE_HOST` 
* required: **true**
* default: **localhost**

A Database host.

## `DJANGO_DATABASE_PORT` 
* required: **true**
* default: **N/A**

A Database port.

## `DJANGO_ATOMIC_REQUESTS`

* required: **false**
* default: **true**
* https://docs.djangoproject.com/en/1.9/ref/settings/#atomic-requests

Whether the database should be configured to use atomic requests.


## `PUBLIC_KEY_PROVIDER_PATH`

* required: **false**
* default: `dynamis.apps.identity.providers.keybase.KeybasePublicKeyProvider`

Configures the path to the class that will be used to lookup public keys during
identity verification.  See the `dynamis.apps.identity` application for more
detail.


## `DJANGO_SITE_DOMAIN`

* required: **true**
* default: **N/A**

A string that should be unique to each instance of the application
(dev/staging/prod) which is used to ensure that signatures are not re-usable
across different versions of the application.


## `DJANGO_DEFAULT_FILE_STORAGE`

* required: **false**
* default: `django.core.files.storage.FileSystemStorage`
* https://docs.djangoproject.com/en/1.9/ref/settings/#default-file-storage

Sets the storage backend that will be used when django deals with files.  Note
that this is not the thing that deals with static files.

For AWS S3, use: `'storages.backends.s3boto.S3BotoStorage'`


## `DJANGO_STATICFILES_STORAGE`

* required: **false**
* default: `django.contrib.staticfiles.storage.StaticFilesStorage`
* https://docs.djangoproject.com/en/1.9/ref/settings/#staticfiles-storage

Set the storage backend that will be used for staticfiles.


## `DJANGO_MEDIA_ROOT`

* required: **false**
* default: `<project-dir>/public/media/`
* https://docs.djangoproject.com/en/1.9/ref/settings/#std:setting-MEDIA_ROOT

Where media files should be stored.


## `DJANGO_MEDIA_URL`

* required: **false**
* default: `/media/`
* https://docs.djangoproject.com/en/1.9/ref/settings/#std:setting-MEDIA_URL

The URL Prefix that will be used when computing media file urls.


## `DJANGO_STATIC_ROOT`

* required: **false**
* default: `<project-dir>/public/media/`
* https://docs.djangoproject.com/en/1.9/ref/settings/#std:setting-STATIC_ROOT

Where static files are collected.


## `DJANGO_STATIC_URL`

* required: **false**
* default: `/static/`
* https://docs.djangoproject.com/en/1.9/ref/settings/#static-url

The URL Prefix that will be used when computing static file urls.


## `DJANGO_EMAIL_BACKEND`

* required: **true**
* default: **N/A**
* https://docs.djangoproject.com/en/1.9/ref/settings/#email-backend


## `DJANGO_EMAIL_HOST`

* required: **false**
* default: `'localhost'`
* https://docs.djangoproject.com/en/1.9/ref/settings/#email-host


## `DJANGO_EMAIL_HOST_USER`

* required: **false**
* default: `''`
* https://docs.djangoproject.com/en/1.9/ref/settings/#email-host-user


## `DJANGO_EMAIL_HOST_PASSWORD`

* required: **false**
* default: `''`
* https://docs.djangoproject.com/en/1.9/ref/settings/#email-host-password


## `DJANGO_EMAIL_PORT`

* required: **false**
* default: `25`
* https://docs.djangoproject.com/en/1.9/ref/settings/#email-port


## `DJANGO_EMAIL_USE_TLS`

* required: **false**
* default: `True`
* https://docs.djangoproject.com/en/1.9/ref/settings/#email-use-tls


## `DJANGO_EMAIL_USE_SSL`

* required: **false**
* default: `False`
* https://docs.djangoproject.com/en/1.9/ref/settings/#email-use-ssl


# AWS Configuration

## `AWS_ACCESS_KEY_ID`

* required: **false**
* default: `None`

The AWS Access Key

## `AWS_SECRET_ACCESS_KEY`

* required: **false**
* default: `None`

The AWS Secret Key

## `AWS_STORAGE_BUCKET_NAME`

* required: **false**
* default: `None`

The bucket to use for AWS S3

## `AWS_DEFAULT_REGION`

* required: **false**
* default: `None`

This enables generation of S3 urls that are appropriately region specific.

Should be one of: 

* `us-east-1`
* `us-west-1`
* `us-west-2`
* `eu-west-1`
* `eu-central-1`
* `ap-northeast-1`
* `ap-northeast-2`
* `ap-southeast-1`
* `ap-southeast-2`
* `sa-east-1`


## `IPFS_HOST`

* required: **false**
* default: N/A


## `IPFS_PORT`

* required: **false**
* default: `443`


## `IPFS_SSL_VERIFY`

* required: **false**
* default: `true`

For use with HTTP auth that sits in front of the IPFS host


## `IPFS_AUTH_USERNAME`

* required: **false**
* default: N/A

For use with HTTP auth that sits in front of the IPFS host


## `IPFS_AUTH_PASSWORD`

* required: **true** (if `IPFS_AUTH_USERNAME` is present)
* default: N/A

For use with HTTP auth that sits in front of the IPFS host


# AWS IAM Configuration for S3 access

The set of credentials that are configured for the S3 bucket need the following
IAM policy attached to their account.

```javascript
{
   "Statement":[
      {
         "Effect":"Allow",
       
         "Action":[
            "s3:ListAllMyBuckets"
         ],
         "Resource":"arn:aws:s3:::*"
      },
      {
         "Effect":"Allow",
         "Action":[
            "s3:ListBucket",
            "s3:GetBucketLocation"
         ],
         "Resource":"arn:aws:s3:::<bucket-name-here>"
      },
      {
         "Effect":"Allow",
         "Action":[
            "s3:*Object*"
         ],
         "Resource":"arn:aws:s3:::<bucket-name-here>/*"
      }
   ]
}
```

And the S3 bucket needs the following CORS configuration.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
    <CORSRule>
        <AllowedOrigin>*</AllowedOrigin>
        <AllowedMethod>GET</AllowedMethod>
        <MaxAgeSeconds>3000</MaxAgeSeconds>
        <AllowedHeader>Authorization</AllowedHeader>
    </CORSRule>
</CORSConfiguration>
```
