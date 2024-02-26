# PORTOGOLIO - A web application for backend developers

## Table of Contents

1. [Introduction](#introduction)
2. [Author](#author)
3. [Features](#features)
4. [Tech Stack](#tech-stack)
5. [Installation](#installation)
6. [Usage](#usage)
7. [Contributing](#contributing)
8. [Contact](#contact)

## Introduction

PORTOGOLIO is a community-based web application desinged to help backend developers level up their developpement by seeing what other backend developers are working on and what technologies best
suited for their next projects or improve curent ones.

[Live Demo](http://portogolio.boukhalfaml.tech/)
[blog article](https://medium.com/@boukhalfaml1011/portogolio-a-platform-for-backend-engineers-9a1bdaec9aec).

## Author

- **Mohamed Lamine**: Full stack and DevOps

## Features

- **Projects:** Showcase ongoing projects including technologies used, and challenges faced.
- **Comments:** Share constructive comments that highlight both strengths and areas for improvement.

## Tech Stack

- HTML/CSS/JavaScript
- Python/Flask
- SQLAlchemy
- Gunicorn
- MySQL
- Nginx
- HAProxy

## Installation

Follow these steps to get started with portogolio:

1. **Clone the Repository:**
   ```bash
   https://github.com/Your-username/Portogolio.git
   ```

2. **Install Dependencies:**
   ```bash
   cd Portogolio
   pip install -r requirements.txt
   ```

3. **Set up MySQL Database:**
   ```bash
   cat set-up.sql | sudo mysql
   ```

4. **Run the Application:**
   ```bash
   PORTOGOLIO_MYSQL_USER=hbnb_dev PORTOGOLIO__MYSQL_PWD=hbnb_dev_pwd PORTOGOLIO__MYSQL_DB=hbnb_dev_db PORTOGOLIO__MYSQL_HOST=localhost PORTOGOLIO_SECRET_KEY=<ADD_SECRET_KEY_HERE> python3 -m app
   ```

   The application will be accessible at `http://127.0.0.1:5000`.

## Usage:

1. **Login:**
   - Navigate to the login page.
   - Enter your credentials to log in or click on register to create a new acount.

2. **Project:**
   - Navigate to the profile page.
   - click on new project and fill out your project's info.
   - click save.

3. **Comment:**
   - On your profile page scroll down and you should see all the projects you created.
   - On the project page scroll down and you should see all the comments of your project.

4. **Projects and Developer:**
   - Navigate to the projects page and explore projects created by other users.
   - Navigate to the developers page and search for developers with same interests.

---

## Contributing

If you're interested in contributing to the development of Portogolio, we welcome your contributions. Follow these steps to contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Make your changes and commit: `git commit -m 'Add new feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Create a pull request.

## Contact

- **Boukhalfa Mohamed Lamine** : [GitHub](https://github.com/tommy457) | [LinkedIn](https://www.linkedin.com/in/mohamed-lamine-boukhalfa)