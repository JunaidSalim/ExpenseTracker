# Expense Tracker

Expense Tracker is a fully responsive web application developed using **Django** and seamlessly integrated with **Tailwind CSS**. Designed to efficiently manage personal finances, the application allows users to track their expenses and incomes through a user-friendly interface. Key features include robust user authentication, full CRUD functionality for managing expenses and incomes, and the ability to export financial data in various formats, such as PDF, CSV, and Excel. This project not only serves as a practical financial tool but also showcases the integration of Tailwind CSS with Django to create a modern, responsive user experience.

This project significantly contributed to the enhancement of my knowledge in **Django** and **Tailwind CSS**.

## Demo
https://github.com/user-attachments/assets/066b0a1d-3ebb-4f7f-9147-ea766be04c7d

## Features

- **Expenses and Incomes Dashboard**: A comprehensive dashboard displaying detailed records of expenses and incomes.
- **User Authentication**: Users can sign up, log in, and manage their own accounts securely.
- **CRUD Operations**: Full create, read, update, and delete (CRUD) functionality for both expenses and incomes.
- **Data Export**: Users can export their financial data (incomes and expenses) in PDF, CSV, and Excel formats.
- **Summaries and Stats**: Provides summaries and statistics of incomes and expenses for better financial insights.

## Tech Stack

- **Backend**: Django 
- **Frontend**: Tailwind CSS
- **Database**: PostgreSQL

## Setup Instructions

To set up this project locally, follow these steps:

### Prerequisites

- Python 3.x
- Pip (Python package installer)
- Node.js (for managing Tailwind CSS)
- npm (Node package manager)

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/JunaidSalim/ExpenseTracker.git
    ```
   ```bash
   cd ExpenseTracker
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   ```
   ```bash
   venv\Scripts\activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
    ```bash
   npm install  
    ```

4. **Apply the migrations:**
   ```bash
   python manage.py migrate
   ```
5. Configure .env
    ```bash
    ENVIRONMENT=development
    SECRET_KEY=YOUR_SECRET_KEY
    DB_NAME=YOUR_DATABASE_NAME
    DB_USER=YOUR_DATABASE_USER
    DB_PASSWORD=YOUR_DATABASE_PASSWORD
    DB_HOST=YOUR_DATABASE_HOST
    DB_PORT=YOUR_DATABASE_PORT
    ```
6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

7. **Build Tailwind CSS:**
   ```bash
   npm run build
   ```

8. Open your browser and go to `http://127.0.0.1:8000/` to view the app.


## Contributing

Contributions are welcome! If you’d like to contribute:

1. Fork the repo.
2. Create a new feature branch
3. Make your changes.
4. Push the changes to your fork.
5. Submit a pull request.

Please ensure your code follows best practices and is properly tested.

## License

This project is licensed under the MIT License.
