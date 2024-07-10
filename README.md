# E-commerce Platform Backend

This project is a Django-based backend for an e-commerce platform, featuring user and admin functionalities, product management, shopping cart, order processing, and real-time updates using WebSockets.

## Technology Stack

- Django
- Django Rest Framework (DRF)
- Celery
- Docker
- MySQL
- WebSockets (Django Channels)
- Redis (for Channels and Celery)

## Project Setup Instructions

### Prerequisites

- Python 3.8+
- Docker and docker-compose
- MySQL
- Redis

### Setup Steps

1. Clone the repository:
2. Create a virtual environment and activate it:
3. Install the required packages:
4. Set up the MySQL database:
- Create a new MySQL database for the project
- Update the database configuration in `ecommerce_backend/settings.py`

5. Set up environment variables:
- Create a `.env` file in the project root and add the following:
  ```
  SECRET_KEY=your_secret_key
  DEBUG=True
  DATABASE_URL=mysql://user:password@localhost:3306/dbname
  ```

6. Run migrations:
7. Create a superuser:
8. Start the Redis server

9. Start the Celery worker:
10. Run the development server:
 ```
 python manage.py runserver
 ```

11. (Optional) To use Docker, build and run the containers:
 ```
 docker-compose up --build
 ```

## API Documentation

### Authentication

- `POST /api/auth/register/`: Register a new user
- `POST /api/auth/login/`: Log in a user
- `POST /api/auth/logout/`: Log out a user
- `POST /api/auth/request-otp/`: Request OTP for login
- `POST /api/auth/verify-otp/`: Verify OTP and log in

### Products

- `GET /api/products/`: List all products
- `POST /api/products/`: Create a new product (Admin only)
- `GET /api/products/{id}/`: Retrieve a specific product
- `PUT /api/products/{id}/`: Update a product (Admin only)
- `DELETE /api/products/{id}/`: Delete a product (Admin only)
- `POST /api/products/bulk-upload/`: Bulk upload products (Admin only)

### Shopping Cart

- `GET /api/cart/`: Retrieve the current user's cart
- `POST /api/cart/add_item/`: Add an item to the cart
- `POST /api/cart/remove_item/`: Remove an item from the cart
- `POST /api/cart/update_item/`: Update item quantity in the cart

### Orders

- `GET /api/orders/`: List all orders (User: own orders, Admin: all orders)
- `POST /api/orders/`: Create a new order
- `GET /api/orders/{id}/`: Retrieve a specific order
- `PUT /api/orders/{id}/`: Update an order status (Admin only)
- `DELETE /api/orders/{id}/`: Cancel an order (restrictions may apply)

## WebSocket Endpoints

- `ws/products/`: Real-time updates for product sold counts
- `ws/echo/`: Echo server for testing WebSocket functionality

## Additional Information and Assumptions

1. **User Roles**: The system assumes two main user roles: regular users and admins. Admins have additional privileges like product management and order status updates.

2. **Authentication**: The system uses token-based authentication. Include the token in the Authorization header for authenticated requests.

3. **OTP Login**: OTP-based login is available as an alternative authentication method. OTPs are assumed to be sent via email in this implementation.

4. **Product Inventory**: The system assumes a simple inventory management where stock is reduced upon order placement. More complex inventory management may be needed for a production system.

5. **Order Status**: Orders have various statuses (e.g., pending, processing, shipped, delivered, cancelled). Only admins can update the status.

6. **Bulk Upload**: The bulk upload feature for products is implemented as an asynchronous task using Celery. Large datasets may take some time to process.

7. **Real-time Updates**: WebSockets are used to provide real-time updates on product sold counts. This feature assumes a stable WebSocket connection can be maintained.

8. **Email Notifications**: The system is set up to send email notifications for events like order confirmation. Ensure proper email backend configuration for this to work.

9. **Security**: Basic security measures are in place, but a thorough security audit is recommended before deploying to production.

10. **Testing**: Unit tests are included for major functionalities. However, more comprehensive testing, including integration and end-to-end tests, is recommended for production use.

