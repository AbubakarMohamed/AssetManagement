# Asset Management System

A Django-based application to manage asset lending, tracking, and maintenance. This system allows users to add new assets, lend assets in bulk or individually, track asset usage, and handle returns with conditions.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Asset Management**: Add, edit, and lend assets.
- **Lending System**: Lend assets in bulk or individually with tracking of quantities.
- **Tracking**: View lent assets and return them with conditions (good/bad).
- **Dynamic Updates**: Automatic updates to asset counts based on lending and returning actions.
- **Maintenance**: Manage asset maintenance schedules.

## Installation

### Prerequisites

- Python 3.x
- Django 3.x or later
- pip (Python package installer)

### Steps

1. **Clone the repository**:

    ```bash
    git clone https://github.com/AbubakarMohamed/AssetManagement.git
    cd asset-management-system
    ```

2. **Create and activate a virtual environment**:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
python manage.py 
makemigrations

3. **Apply migrations**:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

4. **Run the development server**:

    ```bash
    python manage.py runserver
    ```

6. **Access the application** at `http://127.0.0.1:8000/`.

## Usage

### Adding New Assets

Navigate to the Home page and use the form to add new assets. Each asset will have an ID, name, quantity, and other relevant details.

### Lending Assets

Use the Track page to lend assets. Select the asset, specify the quantity, and lend it either individually or in bulk.

### Returning Assets

Click on the links in the 'Asset Taken' section on the Home page to access the return form. Specify the condition (good/bad) of the returned assets.

### Maintenance

Use the Maintenance page to manage asset maintenance schedules and logs. Track maintenance activities and update asset conditions as necessary.


## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes. Make sure to include tests for new features or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
