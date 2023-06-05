# Fresh-Mart-E-commerce-Web-App


This is an e-commerce web application designed to provide users with a convenient platform for buying food products online. With a user-friendly interface and seamless ordering process, this web app aims to enhance the online shopping experienc for those who are unable to leave their homes to purchase foodstuffs. It offers separate implementations using Django and FastAPI to cater to different preferences and requirements

## Features

- User Registration and Authentication: Users can create accounts, login, and manage their profiles.
- Product Catalog: Displays a wide range of products and images.
- Cart Management: Users can add products to their cart, update quantities, and remove items.
- Secure Checkout: Integration with secure payment gateways to facilitate secure transactions with Paystack.
- Order Processing: Efficient order management system for tracking and processing user orders.
- Responsive Design: The web app is designed to be responsive and accessible across different devices.

## Technologies Used

- Python
- Django Framework
- FastAPI
- HTML/CSS
- JavaScript
- Bootstrap
- SQLite


## Installation and Setup

1. Clone the repository:

2. Navigate to the project directory: `cd freshmart-django`

3. Create and activate a virtual environment: `pipenv shell`

4. Install the dependencies: `pipenv install -r requirements.txt`

5. Set up the database: python manage.py migrate

7. Open your web browser and access the application at `http://localhost:8000`.
8. Access FastAPI backend code seperately: exit previous virtual environment `deactivate`
9. Navigate to the fastapi directory: `cd ..` then `cd freshmart-fastapi`
10. create a virtual environment: `pipenv shell`
11. install dependecies: `pipenv install -r requirements.txt`
12. start the development server: `uvicorn main:app --reload`
13. Access the app in your browser at `http://localhost:8000`


## Deployment

The application can be deployed to a production environment using platforms like Heroku. Refer to the official documentation for detailed deployment instructions.

## Contributing

Contributions are welcome! If you have any suggestions or want to report a bug, please open an issue or submit a pull request.

## Acknowledgements

We would like to acknowledge the contributions of the open-source community and the following resources:

- Django Documentation: [https://docs.djangoproject.com/](https://docs.djangoproject.com/)
- Bootstrap Documentation: [https://getbootstrap.com/docs/](https://getbootstrap.com/docs/)

## Contact

For any inquiries or questions, please contact ikponmwosaenabs@gmail.com).
