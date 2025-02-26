# Restaurant Booking and Inventory Management System (Year 12 Web Application)

![website](https://github.com/OliverW147/Y12-Restaurant-Website-Task-1/blob/main/image.png?raw=true)

This repository contains the development of a web-based solution for restaurant inventory and booking management. The system leverages a Python-based backend, developed in the previous iteration, and integrates it with a user-friendly web interface. This system is designed to streamline restaurant operations, including customer booking, meal ordering, inventory management, and staff authentication.

## Overview

The goal of the system is to:

- **Automate inventory tracking** to eliminate manual processes and minimize errors.
- **Integrate online bookings** with pre-ordering functionality to enhance customer experience.
- **Allow customer and staff logins** via an account system for authentication.
- **Generate low-stock alerts** for staff when ingredients are running low.
- **Provide statistics** on ingredient usage to improve inventory planning.

This README outlines the structure, goals, and functionality of the web application, including details on the frontend and backend components, development stages, and key features.

## Features

- **Booking Management**: Customers can book tables, select meal options, and check availability. Staff can manage and cancel bookings.
- **Inventory Management**: Staff can manage ingredient stock, add or remove items, and receive alerts for low-stock items.
- **Meal Management**: Staff can add, remove, and update the meal menu, ensuring ingredient stock is maintained.
- **Account System**: Both customers and staff have login and registration functionalities, with session-based management for authentication.
- **Statistics and Usage Logs**: The system tracks ingredient usage, allowing staff to predict shortages and make better decisions on reordering.

## System Design

The system's functionality is divided into frontend and backend components:

- **Backend**: The backend is implemented in Python, utilizing the Flask framework to create routes, manage bookings, track inventory, handle user authentication, and manage meals.
- **Frontend**: The frontend consists of HTML, CSS, and JavaScript, using Bootstrap for styling and dynamic page interactions. It is designed to be responsive and user-friendly.

A flowchart is used to visualize the interactions between different components of the system, guiding the logic behind the user interactions and server responses.

## Development Stages

The project development was divided into three key stages:

### 1. **Initial Development and Basic Functionality**
   - The first iteration focuses on implementing core functionalities, such as:
     - Customer login and registration
     - Booking management
     - Inventory management
     - Meal selection and stock checking
   - Backend objects such as **Bookings**, **Inventory**, **Meals**, **Usages**, and **Accounts** were initialized and integrated into the Flask routes.
   - Basic HTML forms were created to handle user inputs and booking processes.

### 2. **Bug Fixing and Enhanced Features**
   - The second iteration addressed issues identified during testing:
     - Preventing booking outside operating hours using JavaScript to dynamically generate available times.
     - Introducing functionality for staff to manage the meal menu and update ingredient stock.
     - Improved booking naming convention by linking bookings to customer session usernames.
     - Enhancing user feedback with color-coded success and failure messages.

### 3. **Styling and Final Enhancements**
   - The third iteration focused on styling and improving the UI:
     - The homepage layout was refined with Bootstrap components, including a jumbotron for an engaging introduction.
     - New sections for "About Us," "Our Menu," and "Contact Us" were added.
     - Navigation buttons dynamically changed based on user roles (customer or staff).
     - Improved form and table designs for better usability.
     - The staff dashboard was overhauled to provide easy access to the management features.

## Installation and Usage

1. **Clone or Download** the repository to your local machine.
2. **Install Flask**:
   - Run the following command to install the necessary dependencies:
     ```
     pip install flask
     ```
3. **Run the Application**:
   - Launch the application by running the `app.py` file. This will start the Flask web server.
   - Access the application through your web browser at `http://127.0.0.1:5000/`.

4. **Sign Up/Log In**:
   - Customers can create an account, log in, and book tables.
   - Staff members can log in with predefined credentials to manage bookings, inventory, and meal data.

## Future Enhancements

- **Persistent Data Storage**: Currently, the system uses in-memory data structures. Integrating a database (e.g., SQLite, PostgreSQL) would allow for persistent storage of bookings, inventory, and user accounts.
- **Advanced Features**: Future iterations could include advanced features like:
  - Email notifications for booking confirmations and low-stock alerts.
  - Integration with a payment gateway for processing online payments.
  - Customer feedback system to improve service quality.

## Acknowledgements

- **Flask**: For providing a simple yet powerful web framework that integrates seamlessly with Python.
- **Bootstrap**: For the responsive design framework used to style the website.
- **OpenTable**: For inspiration in designing the user interface.
- **Python**: For being the core programming language behind the system.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
