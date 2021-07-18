# MC Vinyl - Vinyl Records E-Commerce Site

## 4th Milestone Project

## Full Stack Frameworks with Django

## Code Institute 2021

---

The brief for this project was to build a full-stack website using the Django framework and which utilised a relational database such as MySQL or Postgres and provided some e-commerce functionality by using Stripe payments. MC Vinyl is a vinyl records store where users; staff or customers can interact with the site giving them full CRUD functionality over a Postgres database.

In the case of staff they can add, edit or delete products. They have a messaging app where they can converse with customers regarding problems with orders.

For customers they can purchase products. If they register to the site they can leave, edit, delete or upvote product reviews. They also have a wishlist which saves to their profile for convenient ordering of favourites. They can view past orders and contact the site owner regarding an order via the messaging function. User authentication is provided. 

The design is based on user experience principles. Clean coding and a responsive mobile first method were employed. Bootstrap 4 was used to aid the responsiveness and front-end design. 

---

### See the image below for an example of the responsiveness of the site.

Click the image to be taken to a live demo of the site:

[![homepage][1]][2]

[1]: ./documentation/images_for_readme/am-i-responsive.jpg
[2]: https://mc-vinyl.herokuapp.com "Live Site" ###################################################

---

### **Contents:**

[1. UX Design](#1-ux-design)

[2. Features and Functionality](#2-features-and-functionality)

[3. Technologies Used](#3-technologies-used)

[4. Testing](#4-testing)

[5. Deployment](#5-deployment)

[6. Credits and Notes](#6-credits-and-notes)

---

### **1. UX Design**

#### Strategy

_User Stories:_

There are 2 types of users of the site: the site staff (including owner/administrator) or a customer user.

As the site owner/administrator:

- I want the site layout to be a typical e-commerce with the expected features and smooth navigation between sections.
- I want users to be able to register, login and change password.
- I want the site to be relatively secure for users.
- I want customers to be able to purchase and pay for products.
- I want customers to be able to save favourite items to a wishlist for later which is saved to their account.
- I want customers to be able to save profile information to their account.
- I want staff to be able to add, edit and delete products.
- I want customers to be able to message staff and vice versa with a record kept of all conversations.
- I want customers to be able to search and sort products.
- I want users to be able to make new reviews and edit or delete old reviews.
- I want users to be able to rate products and i want the rating to be updated if reviews are adjusted or deleted.
- I want users to be able to sort reviews.
- I want users to be able to upvote/like other reviews.
- I want the site to have a staff account with exclusive features, such as, crud of products, messaging, adding genres, view all orders.
- I want any text inputs by users to be validated.
- I want users to be able to see updates or news on the site through social media links.
- I want a site that is not crashing with bugs and if there is an error, that it is managed in a good way for the user.

As a customer:

- I want the site to be appealing and easy to use.
- I want the site navigation between sections to be easy.
- I want to be able to search and sort products easily.
- I want to be able to purchase products and pay securely.
- I want to be able to save profile information so i don't have to type the same information every time I order.
- I want to be able to save products to a wishlist, which I may purchase at a later date.
- I want to be able to see past orders and be easily able to contact the site owner in the event of a problem with an order.
- I want be able to be able to read and sort reviews by other customers.
- I want to be able to upvote other most useful reviews for other customers.
- I want to be able to leave reviews myself and be able to edit, or delete those reviews.
- I want to be able to rate products.
- I want to be able to register and change my password.
- I want to know that the site is secure and safe to use.
- I want to be aware of updates or new features through social links.
- I want a site that is not slow or full of bugs and if there is an error it is managed properly.

#### Scope

From researching other similar vinyl e-commerce sites it should be possible to provide a broadly similar experience.

Based on the results of the Strategy research the features to be included are:

- Home: Landing page with large obvious CTA and the purpose of the site should be obvious.
- Users can register, login and change password.
- Passwords are validated and hashed.
- Products can be searched by artist, title and genre.
- Products can be sorted by price, rating or alphabetically.
- A wishlist which saves to a user profile.
- A payment system to purchase products using Stripe.
- A user profile where customer shipping information and past orders and associated communication can be saved.
- Sortable product reviews and ratings can be added, edited and deleted.
- Staff can leave a comment underneath a review.
- Reviews can be upvoted.
- Staff messaging app for communicating with customers regarding orders.
- Staff can view all orders and search by customer.
- Staff can add, edit and delete products.
- Staff can add new genre or promotion fields.
- Footer: Links to social media.


From the strategy table all the above features appear viable. Some basic features such as pagination and a contact form may be left out for now due to time constraints. A wishlist and the messaging app for use between staff and customers are more relevant to the project requirements and interesting features to have instead. A CSP strategy would be useful to boost security but may also be left aside for now due to time constraints.

#### Structure

- A pretty typical e-commerce structure with all important pages accessible from any page from the Navbar at the top of the page, including the shopping cart.
- Customer Wishlist link is in the Navbar.
- User account features are accessible through a dropdown sub-menu in the Navbar along with staff features such as the messaging app.
- Custom error page, for 404, 500 and CSRF errors so in the case of a broken internal link or where a CSRF form token has expired, a button is provided for the user to return to safety.

#### Skeleton

Wireframes made in Balsamiq Wireframes were used for basic layout. These can be viewed here:

[Landing Page All Sizes](./documentation/wireframes/landing_page.png)

[Admin Controls Page All Sizes](./documentation/wireframes/admin_controls.png)

[Browse Reviews Page All Sizes](./documentation/wireframes/browse_my_reviews.png)

[New Review Search Page All Sizes](./documentation/wireframes/new_review_search.png)

[New/Edit Review Page All Sizes](./documentation/wireframes/new_edit_review.png)

[Review Detail Page All Sizes](./documentation/wireframes/review_detail.png)

[Register Page All Sizes](./documentation/wireframes/register.png)

[Change Password Page All Sizes](./documentation/wireframes/change_password.png)

[Contact Page All Sizes](./documentation/wireframes/contact_page.png)

#### Surface

[Pixabay](https://pixabay.com/) provided the free background image and the logo icon. The main font is a Google font called Monoton which conveniently matches the vinyl theme, with the secondary font being Montserrat.
The main colors used were #F9F6F6 for the background contrasting with #451D1D for much of the text and the footer. #A20B0B is used for the banner announcing free delivery.

![ColourChoices][3]

[3]: ./documentation/images_for_readme/palette.png "Colour Choices"

---

### **2. Features and Functionality**

The site was designed with a mobile first approach. Customised Bootstrap was used to help with the responsiveness and layout of the site. In addition targeted media queries were used to assist with this. The site borrows much of the functionality of Stripe payments from the Boutique Ado project however modified to suit this application. Superuser staff do not have access to the admin backend of the site. There is a specific Staff setting to allow that. 

The Crispy Forms add-on is used throughout the site to aid form formatting. Each form has a CSRF tag for added security.

Bootstrap toasts are used to provide feedback to the user regarding an action by utilising the Django message system levels and displaying the messages within the toasts.

_Landing Page:_

The landing page features a simple layout with a background image which assists in directing the user as to the purpose of the site and a large CTA to enter the shop. The navbar alternatively gives access to search the site directly or to log-in.

_Authentication Pages:_

Including Log-in, log-out, register, verification and change password are all handled using the Django-Allauth add-on which integrates seamlessly.

_Products Page:_

User can see all products. They can search and sort. The search input will search by artist or title or genre. Genres can be clicked directly or the dropdown sort allows sorting by price, rating or alphabetically. Product ratings are shown and additional edit and delete product buttons are shown to superusers.

_Product Details Page:_

Here users can see details of the product. The track listing makes use of the add-on Django-Better-Admin-Arrayfield. A Postgres relational database was used both locally and when deployed, as the sqlite3 or mysql versions will not handle the arrayfield.

If a user is logged in they can; add the product to their wishlist, add it to their cart, leave a review and rating. They can also sort reviews by most popular review, by latest review or highest/lowest rating. There is also a button to edit or delete their own review. Users can also upvote a review by clicking the thumbs-up symbol. 

Superusers can again see the additional edit and delete buttons. 

_Product Review Page:_

Here there's a form where users can edit or delete a past review and superusers can leave a comment beneath a review, which can be useful if it is a complaint. A modal is used to confirm a delete action.

_Wishlist Page:_

The wishlist allows users to make a list of up to 10 favourite products which they might like to purchase at some point in the future. For convenience there's are buttons to add each individual product to the cart or all items at once. This is one of the big advantages for a customer to sign up to the site as they cannot access or use the wishlist otherwise. If they click on the wishlist it will direct them to the sign-in page.

_Cart Page:_

As with any e-commerce site the cart shows the products added for purchase and a total to be paid including delivery.

_Checkout Page:_

The checkout page shows details of the intended purchases including a delivery cost if total is less than the free delivery threshold. Stripe credit card payments input are integrated into the template.

_My Profile Page:_

From here customers can save address details to make checkout quicker and easier. The can also view past orders and start a conversation with the site owners regarding a particular order. When they receive a message back they will also get an email notification to let them know they have a new message. A users username and email address are fixed and are the ones they signed up with.

**Superuser Features:**

_Messaging App:_

From the messaging app main page site admin with superuser status can view all message threads both open and closed. They can choose to view open or closed separately and they can refresh messages or delete whole threads for maintenence purposes. Unread messages are in bold print and the user is informed if they've replied to a thread. Message threads are started by customers if they have an issue with an order. When the customer sends a message the site admin gets an email notification. The unique order number is used as a reference number for each message thread and messages are displayed by grouping them by ref. number and ordering by date.

_Message Thread Page:_

On this page the site admin can see a summary of the order in question and can reply to the customer. They can also open or close the thread.

_All Orders Page:_

From here the site admin can view all customer orders. They can search by username or by "no account" for anonymous users.

_Add & Edit Product Page:_

Allows a site admin to add a new product or edit an existing one. A check is performed to make sure that the new SKU product identifier does not already exist in the database. The customised Django Better Arrayfield makes it an easy task to add album track listings.

_Product Tags Admin Page:_

Allows a site admin to add a new product genres or promotion tags. Both programatical and reader friendly names are required. The programatical name is validated and does not allow spaces or special characters. Repetition is also checked.

_Custom Error Pages:_

Custom error pages are included for http 400, 403, 403CSRF and 500 errors.

_Other features of the backend of the site:_

__Project File Structure__: The project is structured and folders named as per the Django documentation and recommendations. Styling and javascript are split out to the various apps where appropriate. A separate utils folder for helper functions was created for the send email function as it is used across various apps.

__Defensive Programming__: As mentioned previously defensive programming was a key consideration. Potential errors are considered where they could possibly arise so that they could be handled appropriately. The @login_required decorator is used throughout to aid security of the site by preventing unauthorised users accessing functions through URL's. All URL's have been manually checked in the browser address bar to ensure expected functionality and security. Functions that require it have checks to see if the user is a superuser and authorised to access it. Validation on inputs is used where necessary. In all instances where the database is modified POST requests are used for some additional security.

_There are no known outstanding bugs in the site._

__Additional Security Considerations__:

Django has in-built security through it middleware in settings and Django templates protects against the majority of XSS attacks.

In addition:

- All sensitive variables are stored in environment variables.
- The session cookie and CSRF cookie are set to secure.
- The SECURE_HSTS_SECONDS value is set, which means SecurityMiddleware will set the “Strict-Transport-Security” header. This reduces your exposure to some SSL-stripping man-in-the-middle (MITM) attacks.
- SECURE_HSTS_INCLUDE_SUBDOMAINS is set to true, which means SecurityMiddleware will add the includeSubDomains directive to the Strict-Transport-Security header.
- The session cookie is set to time-out after 3 hours.
- Cross-Site Request Forgery (CSRF) attacks are dealt with by using the CSRF Token tag inside any form {% csrf_token %}.


__Postgres Database Collections Schema__:

![DatabaseSchema][4]

[4]: ./documentation/images_for_readme/database_schema.png "Database Schema"

 A Postgres relational database set up in Heroku for convenience and linked to in environmental variables, was used in development as well as the deployed version, as the sqlite3 or mysql database options would not handle the arrayfield used for track listings. The database consists of 10 models with some common relationships to each other as marked on the diagram above:

_User Model_

- This model is supplied by Django Allauth and contains the key user authentication information, including username, email and password.

_UserProfile Model_

- Contains user editable information such as shipping/billing address and phone number. It has a one-to-one relationaship with User.

_UserMessage Model_

- For user messages. Contains fields such as message body, message date, message read, message topic closed. User messages are associated with a certain order by setting the ref. number equal to the particular order number. It includes User as a foreign-key.

_Order Model_

- For user e-commerce orders. Contains fields such as the order number, order date, shipping/billing details (which could be different from those in UserProfile), original cart items, delivery cost and totals. It includes UserProfile as a foreign-key.

_OrderLineItem Model_

- Represents a line in an order, product price * quantity with the lineitem_total field holding the result. It includes Order and Product as foreign-keys.

_Wishlist Model_

- Contains a many-to-many field of Products. It has a one-to-one relationaship with User.

_Product Model_

- Represents a single products details. It includes fields such as artist, title, sku, rating and price. The image field contains a path to the product image. The track list field uses an ArrayField to store the album track list. Includes Genre and Promotion many-to-many fields.

_Genre Model_

- Represents a music genre tag. It includes a programatical name and a friendly name.

_Promotion Model_

- Represents an e-commerce promotions tag. It includes a programatical name and a friendly name.

_ProductReview Model_

- Represents a user review of a product. Includes the fields; review body, review date, review rating, upvote count and an admin comment field, where the site admin can respond to a complaint. It features User and Product foreign-keys and upvote_list which is a User linked many-to-many field, the length of which can be used to give the upvote count field value. A choices array is supplied for the review rating IntegerField.

---

### **3. Technologies Used**

_IDE and Languages:_

- Gitpod - IDE used.
- HTML - Base structural language.
- CSS - Language used for styling.
- JavaScript - for application functionality and DOM manipulation.
- Python - for backend functionality.
- Django templating language in Django template renders.

_Libraries, frameworks and Add-ons:_

- Django 3.2.3 - is a Python-based free and open-source web framework that follows the model–template–views architectural pattern.
- Django-allauth 0.44.0 - Integrated set of Django applications addressing authentication, registration, account management.
- Django-better-admin-arrayfield 1.4.2 - Formats model ArrayFields into separate inputs rather than a comma separated list.
- Django-crispy-forms 1.11.2 - Formats form renders in templates.
- Bootstrap 4.6.0 - Used to help with grid layout, screen size responsiveness and other features such as buttons and toasts.
- JavaScript, Popper.js, and jQuery as part of Bootstrap.
- Font Awesome for icons.
- Google Fonts for Monoton and Montserrat fonts.
- Stripe - for processing credit card payments.

_Database:_

- Postgres - Relational Database.

_Hosting and Version Control:_

- GitHub - Holding repository.
- Git - Version control.
- Heroku - for hosting the site.

_Other Tools:_

- Balsamiq - For wireframes.
- Microsoft Paint 3D - For editing images.
- Browserstack - To check base compatibility.
- freeformatter.com - to format html files.
- tinyjpg.com - to reduce image file size.
- Autoprefixer - used to automatically add browser compatibility prefixes.
- w3c - for HTML and CSS validation.
- jshint - for JavaScript validation.
- pylint - for python validation.
- Chrome Development Tools - for checking performance and accessibility.
- [quickDBD](www.quickdatabasediagrams.com) - for the database schema.

As per industry practice and to reduce the number of small commits on the master branch, separate branches were created and used for features (where appropriate) and for the readme file as they were developed. These were squashed, merged and deleted after use.

---

### **4. Testing**

__Final testing of links, responsiveness and Live Website test cases can be found in the [final testing document here](./documentation/testing.md).__

---

### **5. Deployment**

The live site is deployed to [Heroku](https://www.heroku.com), a cloud application platform. The deployment procedure for this was as follows:

1. The repository for the site was generated in Github based on the [Code Institute Full Template](https://github.com/Code-Institute-Org/gitpod-full-template).

2. 

4. In the IDE CLI make a requirements file containing all installed dependencies using the following command:
    - `pip3 freeze --local > requirements.txt`

5. Again in the IDE CLI make a Procfile using command:
    - `echo web: gunicorn mc_vinyl.wsgi:application > Procfile`

6. Debug must be set to False for production.

7. Make a [Heroku](https://www.heroku.com) account and create a new App.

    ![CreateNewApp][5]

    [5]: ./documentation/images_for_readme/create-new-app.jpg "Create New App"

8. Give it a name and choose the appropriate region.

    ![NameApp][6]

    [6]: ./documentation/images_for_readme/name-app.jpg "Name New App"

9. Go to settings and click on Reveal Config Vars.

    ![Settings][7]

    [7]: ./documentation/images_for_readme/settings.jpg "Settings"

10. Enter the environmental variables for the project from the env.py file.

    ![EnvVariables][8]

    [8]: ./documentation/images_for_readme/env-variables.jpg "Environmental Variables"

11. Then select Deploy and click connect to Github. Type the repository name in the search box and press search. Just below that, this should find the repository. Click Connect. Heroku is now connected to the Github repository.

    ![ConnectGithub][9]

    [9]: ./documentation/images_for_readme/connect-github.jpg "Connect Github"

12. Finally select the correct branch (in this case Master) and click on Deploy Branch. Automatic or manual deployment can be used as preferred. The message "Your app was successfully deployed." should appear. Click View to view the now deployed app.

    ![DeployBranch][10]

    [10]: ./documentation/images_for_readme/deploy-branch.jpg "Deploy Branch"

---

_For this website to be run locally it can downloaded as a ZIP file or it can be cloned, however it needs access to a database schema named "movie_review" as highlighted in the earlier section:_

- To download ZIP copy:

1. On GitHub, navigate to the main page of the repository.
2. Above the list of files, click Code.
3. Click Download ZIP.
4. Navigate to the local Downloads folder and un-zip the project_one-master folder.

- To Clone using Command Line:

1. On GitHub, navigate to the main page of the repository.
2. Above the list of files, click Code.
3. To clone the repository using HTTPS, under "Clone with HTTPS", copy the URL.
To clone the repository using an SSH key, including a certificate issued by your organization's
SSH certificate authority, click Use SSH, then copy the URL.
4. Open Git Bash.
5. Change the current working directory to the location where you want the cloned directory.
6. Type git clone, and then paste the URL you copied earlier: \$ git clone url-copied-earlier
7. Press Enter to create your local clone.

- To Clone using GitHub Desktop:

1. On GitHub, navigate to the main page of the repository.
2. Above the list of files, click Code.
3. Click "Open with GitHub Desktop" to clone and open the repository with GitHub Desktop.
4. Follow the prompts in GitHub Desktop to complete the clone.

Once the local project directory is in place, create a virtual python environment. Make an env.py file with the following entries:

    - import os
    - ("IP", "0.0.0.0")
    - ("PORT", "5000")
    - ("SECRET_KEY", "\<your secret key\>")
    - ("API_KEY", "\<your api access key\>")
    - ("MONGO_URI", "\<your mongodb uri\>")
    - ("MONGO_DBNAME", "movie_review")

Install the required packages with:

- `pip install -r requirements.txt`

Run the app: 

- `python3 manage.py runserver`

The website should be available at http://127.0.0.1:5000

---

### **6. Credits and Notes**

- All code in this project is completely the authors unless otherwise indicated in the code.

- Free background image supplied from pixabay.com and is free to use without attribution.

- My Mentor for their time and advice.

- Friends and family who tested the site.

---

### **Disclaimer**

- This website is for educational purposes only.

---













---

Trash Can icon used under Font Awesome Licence https://fontawesome.com/license

star rating css https://github.com/chrislingxiao/starrating
