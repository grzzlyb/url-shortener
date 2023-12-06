# URL Shortener Web Application

This project is a simple URL shortening web application built using Flask and PostgreSQL to shorten URLs and manage a user's shortened links.

## Overview

The project includes several features:
- User authentication using username and password
- Shortening URLs with a 48-hour expiration
- Viewing the history of shortened URLs with the number of clicks

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/url-shortener.git
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up a PostgreSQL database and configure the `app.py` file with the appropriate credentials.

4. Run the Flask application:

    ```bash
    python app.py
    ```

## Usage

1. Access the application through the browser: `http://localhost:5000/`

2. Register or login with your credentials.

3. Shorten your URLs and manage them through the provided interface.

## Endpoints

- `/home`: Home page
- `/login`: User login page
- `/`: Login page (root endpoint)
- `/logout`: Logout endpoint
- `/shorten`: Shorten URL endpoint
- `/<short_url>`: Redirects to the original URL associated with the provided short URL
- `/base`: Main user dashboard for URL shortening
- `/history`: View history of shortened URLs

## File Structure

- `app.py`: Contains the main Flask application.
- `templates/`: Folder containing HTML templates.
- `static/`: Folder for static files (like images or CSS).
- `README.md`: Documentation file for the repository.
- `requirements.txt`: File containing all necessary Python packages for the project.

## Contributing

Contributions to enhance the project are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create your feature branch: `git checkout -b feature/YourFeature`.
3. Commit your changes: `git commit -am 'Add some feature'`.
4. Push to the branch: `git push origin feature/YourFeature`.
5. Open a pull request.

This project is licensed under the [MIT License](LICENSE).
