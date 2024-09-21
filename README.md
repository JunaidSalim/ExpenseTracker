# Expense Tracker

Expense Tracker is a fully functional and responsive web application built using **Django** and styled with **Tailwind CSS**. This project not only serves as a personal expense and income tracking tool but also demonstrates how Tailwind CSS can be integrated seamlessly with Django. The app includes features such as CRUD operations for managing expenses and incomes, user authentication, and exporting data to various formats.

This project significantly contributed to the enhancement of my knowledge in **Django** and **Tailwind CSS**.

## Demo

## Features

- **Expenses and Incomes Dashboard**: A comprehensive dashboard displaying detailed records of expenses and incomes.
- **User Authentication**: Users can sign up, log in, and manage their own accounts securely.
- **CRUD Operations**: Full create, read, update, and delete (CRUD) functionality for both expenses and incomes.
- **Data Export**: Users can export their financial data (incomes and expenses) in PDF, CSV, and Excel formats.
- **Summaries and Stats**: Provides detailed summaries and statistics of incomes and expenses for better financial insights.

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

5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

6. **Build Tailwind CSS:**
   ```bash
   npm run build
   ```

7. Open your browser and go to `http://127.0.0.1:8000/` to view the app.


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
