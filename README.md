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
- **Endpoint:** `/signup`
- **Method:** `POST`
- **Parameters:**
  - `username`: User's username
  - `password`: User's password

### 2. Login
- **Endpoint:** `/login`
- **Method:** `POST`
- **Parameters:**
  - `username`: User's username
  - `password`: User's password
- **Returns:**
  - `access_token`: Token for accessing protected endpoints

### 3. Get Address
- **Endpoint:** `/address/{address_id}`
- **Method:** `GET`
- **Parameters:**
  - `address_id`: ID of the address to retrieve

### 4. Update Address
- **Endpoint:** `/address/{address_id}`
- **Method:** `PUT`
- **Parameters:**
  - `address_id`: ID of the address to update
  - Other fields for address details

### 5. Delete Address
- **Endpoint:** `/address/{address_id}`
- **Method:** `DELETE`
- **Parameters:**
  - `address_id`: ID of the address to delete

### 6. Get Addresses Within Distance
- **Endpoint:** `/addresses-within-distance`
- **Method:** `GET`
- **Parameters:**
  - `latitude`: Latitude of the reference location
  - `longitude`: Longitude of the reference location
  - `distance`: Distance in kilometers

## Getting Started

1. Clone the repository.
2. Install the required dependencies.
3. Set up a database and configure the connection in the application.
4. Run the application.

## Usage Examples

Here are some examples demonstrating how to use the API:

### Sign Up
```bash
curl -X POST -H "Content-Type: application/json" -d '{"username": "user1", "password": "password123"}' http://your-api-url/signup
