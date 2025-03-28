# Cross Service Auth

[![PyPI version](https://badge.fury.io/py/cross-service-auth.svg)](https://badge.fury.io/py/cross-service-auth)
[![Downloads](https://pepy.tech/badge/cross-service-auth)](https://pepy.tech/project/cross-service-auth)
[![Downloads](https://pepy.tech/badge/cross-service-auth/month)](https://pepy.tech/project/cross-service-auth)
[![Downloads](https://pepy.tech/badge/cross-service-auth/week)](https://pepy.tech/project/cross-service-auth)

This package implements custom authentication for Django, allowing you to authenticate users between microservices using JWT (JSON Web Token). The package allows you to validate tokens, retrieve user data without having to access the database, and supports dynamic user attributes.

## Description

This package adds a custom authentication class **`CrossServiceJWTAuthentication** to your project, which allows you to verify tokens and get information from them for further user authorization between microservices.

## Dependencies

- **Django** >= 3.0
- **djangorestframework** >= 3.12
- **djangorestframework-simplejwt** >= 4.7

## Installation

1. Download or clone the repository:

   ```bash
   pip install cross-service-auth
   ````
   
## Usage

1. Set a shared key for your microservices
   ```
   SIMPLE_JWT = {
       ...,
       'SIGNING_KEY': 'your-shared-secret-key',
       ...,
   }
   ```

2. Use cross service auth in your views

   ```python
   from cross_service_auth.auth import CrossServiceJWTAuthentication

   class YourView(APIView):
       authentication_classes = [CrossServiceJWTAuthentication]
   ```