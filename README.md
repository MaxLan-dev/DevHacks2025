# BRIEF DESCRIPTION: 

This is a Food4U team's project for University of Manitoba's devClub 2025 hackathon.
It implements a system which allows the small businesses to search for local food suppliers (in particular, farmers) and connect with them in order to source the food products directly and more efficiently for their business.  

The system can be accessed here: https://food4u-5ka6.onrender.com
Note: If the website does not load after clicking the link, wait for abour 40 seconds and try again. Since the website is hosted on a free host, the system is not active when no one uses it for a while, and is being re-deployed automatically whenever someone accesses it.

## Project Goals
The Food4U project aims to bridge the gap between small businesses and local food suppliers by:
- Simplifying the process of sourcing fresh, cpeaper and local food products.
- Supporting local farmers by connecting them directly to businesses.
- Reducing reliance on large-scale distributors for small businesses.

## Key Features
- **Search Functionality:** Small businesses can search for suppliers based on location, product type, or availability.
- **Supplier Profiles:** Detailed pages for suppliers including products offered and reviews from other businesses.
- **User Authentication:** Secure login for businesses to manage their profiles and interactions.
- **Direct Communication:** Tools to facilitate direct contact between businesses and suppliers (e.g., messaging or contact info sharing).
- **Product Listings:** A catalog of available food products with details like price and quantity.

# IMPLEMENTATION:  

The system uses SQLlite-implemented databases to store the information of users (small businesses), suppliers, reviews of suppliers, authentification details and products information.  
Below is the EER-diagram of the schema of the used database:  

![image](https://github.com/user-attachments/assets/0ac7a594-5bcc-450e-a34a-5267b8aa8998)  

Also, a Django framework is used for managing the database, handling user's requests and serving the webpages.
In addition, web technologies, such as HTML, CSS and JavaScript (JS) are used for implementing the user-interface (via webpages).

### Summary of Technologies Used
- **Backend**: Django (5.1) with Python (3.12), python-dotenv(1.0.1) and 
- **Database**: SQLite (lightweight, file-based) with SQLAlchemy (2.0.30)
- **Frontend**: HTML (3), CSS (5), JavaScript
- **Hosting**: Render (for deployment)
- **Version Control**: Git/GitHub


## Installation, Setup and Running
To run the Food4U project locally, follow these steps:

### Prerequisites
- Python 3.12 (preferrably 3.12)
- Git
- A virtual environment tool (e.g., `venv`)

### Steps to run the project
1. Clone the repository:  
   git clone https://github.com/MaxLan-dev/DevHacks2025.git
   cd food4u

   You can also download the repository as a .zip to your local machine and extract it.

2. Create the dependencies:  
   In the repository, cloned to your machine, navigate to DevHacks2025/food4u/food4u
   In the current directory, create .env file and put SECRET_KEY = 'YOUR-Django-SECRET-KEY' in there. Save the changes.
   
4. Build the project:  
   Now, open your terminal and cd to DIRECTORY_WHERE_REPOSITORY_WAS_CLONED_TO/DevHacks2025/food4u
   In your current directory, type "python manage.py makemigrations registration" and hit Enter.
   Then, type "python manage.py migrate" and hit Enter.

6. Run the project:  
   Now, in your current directory from previous step, type "python manage.py runserver" and hit Enter.
   This will run the server and interface of the project.

8. Accessing the interface:
   After step 6, a new window will open in your default browser.
   By opening that window, you will be able to see and interact with a user-interface of the project.




## Future Improvements
- Add ability for suppliers to register and use the platform.
- Add a map integration to visualize supplier locations.
- Implement real-time messaging between businesses and suppliers.
- Expand the database to include more product categories and filters.
- Enhance security with two-factor authentication and other safety enhancements.
- Include AI-powered chatbot for small businesses and farmers to help them write long messages and make the communications between 2 parties faster and more efficient.
   
