# Address Book Project

The Address Book Project is a simple API project for managing and retrieving addresses. It provides authentication through sign-up and login APIs, and offers functionality to get, update, and delete addresses. Additionally, there's an API to retrieve all addresses within a specified distance from a given location.

## Table of Contents
- [Features](#features)
- [Authentication](#authentication)
- [API Endpoints](#api-endpoints)
- [Getting Started](#getting-started)
- [Usage Examples](#usage-examples)
- [Contributing](#contributing)
- [License](#license)

## Features

- User authentication with sign-up and login APIs.
- CRUD operations for managing individual addresses.
- Retrieve all addresses within a specified distance from a given location.

## Authentication

The API uses token-based authentication. Users must sign up to obtain an access token, which is required for accessing protected endpoints.

## API Endpoints

### 1. Sign Up
- **Endpoint:** `[/signup](http://127.0.0.1:8000/user/v1/signUp)`
- **Method:** `POST`
- **Parameters:**
  - `emailId`: User's username
  - `password`: User's password

### 2. Login
- **Endpoint:** `[/login](http://127.0.0.1:8000/user/v1/login)`
- **Method:** `POST`
- **Parameters:**
  - `emailId`: User's username
  - `password`: User's password
- **Returns:**
  - `access_token`: Token for accessing protected endpoints

### 3. Get Address
- **Endpoint:** `[/address/{address_id}](http://127.0.0.1:8000/addressBook/v1/fetchUserAddress)`
- **Method:** `GET`
- **Authentication** `Pass access token`

### 4. Update Address
- **Endpoint:** `/address/{address_id}`
- **Method:** `PATCH`
- **Parameters:**
  - `latitude`: New latitude
  - `longitude`: New longitude
- **Authentication** `Pass access token`

### 5. Add Address
- **Endpoint:** `[/address/{address_id}](http://127.0.0.1:8000/addressBook/v1/updateAddress)`
- **Method:** `POST`
- **Parameters:**
  - `latitude`: New latitude
  - `longitude`: New longitude
- **Authentication** `Pass access token`

### 6. Get Addresses Within Distance
- **Endpoint:** `[/addresses-within-distance](http://127.0.0.1:8000/addressBook/v1/addressWithInDistance)`
- **Method:** `POST`
- **Parameters:**
  - `latitude`:  Latitude of the reference location
  - `longitude`: Longitude of the reference location
  - `distance`:  Distance in kilometers

## Getting Started

1. Clone the repository.
2. Install all the required library using pip install -r requirements.txt.
3. Set up a database and configure the connection in the application.
4. To run the server use follwing commands uvicorn app.main:app --reload (By default it will run on port 8000)
