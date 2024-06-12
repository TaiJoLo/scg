# Project Report for Web Application

## Part 1: Design Decisions

### Routes and Templates

#### Home Route ("/")

When designing the home route, I wanted to create a welcoming and informative landing page for the staff. I decided to use the Bootstrap hero component because it provides a clear and visually appealing way to highlight key information. The hero component allows for a large heading and some descriptive text, making it ideal for a landing page. I assumed that users, primarily internal staff, would prefer a straightforward entry point into the application, and the hero component effectively achieves this by drawing attention to the main purpose of the portal.

#### Booking Route ("/booking")

When designing the booking route, I aimed to enhance user experience by breaking down the process into manageable steps using a multi-step form approach. This design involved three key templates: `datepicker.html`, `booking_form.html`, and `success.html`.

Initially, a GET request renders the `datepicker.html` template, allowing users to select the booking date using a datepicker form element, ensuring the correct date format. Once the booking date is selected, a POST request submits the date, and the application renders the `booking_form.html` template for further booking details. This template includes a dropdown (`select`) for selecting customers and radio buttons for selecting site occupancy, minimizing manual entry errors and presenting clear options.

After gathering all necessary booking details, another POST request is made to the `/booking/add` route to finalize the booking. This route processes the form submission, updates the database by adding a row for each night of the booking, and then renders the `success.html` template to confirm the booking. This separation of routes ensures each step is handled efficiently.

**Success Page Implementation**

The `success.html` template is created to handle success messages uniformly across various routes, meeting the requirement for an appropriate confirmation page or redirection. This template provides a consistent user experience by using a standard layout for all success confirmations.

In the routes, I included an action parameter to enable conditional rendering within the `success.html` template. This approach allows the template to display appropriate messages and details based on the specific action that was performed. For instance, the action parameter helps distinguish between a successful booking, customer addition, or customer update.

The `success.html` template uses conditional logic to render different messages and details based on the action value passed from the route. This implementation ensures that users receive relevant feedback tailored to their specific actions, all while maintaining a cohesive design throughout the application.

#### Campers Route ("/campers")

The campers route is designed to allow users to select a date and view a list of campers for that date. Initially, a GET request renders the `datepicker_camper.html` template, which provides a datepicker form element for users to select a date. Once a date is selected, a POST request retrieves the list of campers for that date and renders the `camper_list.html` template.

This approach ensures that users can focus on one task at a time, making the process more user-friendly. The table uses Bootstrap classes such as `table`, `table-hover`, and `table-primary` to enhance its appearance. The `table-hover` class adds a hover effect to each row, improving visual feedback for users. The `table-primary` class is applied to the table header to distinguish it from the rest of the table. 

#### Search Customer Route ("/search_customer")

The `search_customer.html` template includes an input field with a placeholder to guide users in entering the search term. When the form is submitted, a POST request handles partial text matches in the customer database.

Search results are displayed using the `search_result.html` template, which presents the data in a well-structured, Bootstrap-styled table. This ensures the interface is visually appealing and user-friendly, allowing staff to quickly find and manage customer information.

**Conditional Logic in search_result.html**

The `search_result.html` template uses conditional logic to show different content based on the route. For the `customerlistforsummary` route, it displays a "Customer Summary Report" heading. For the `search_customer` route, it shows search results for the provided search term. For the `customerlistforedit` route, it displays an "Edit Customer" heading.

Table headers are plain text for the `search_customer` route, and sortable links for other routes. Bootstrap classes like `table`, `table-hover`, and `table-primary` are used to enhance the table's appearance and usability. The `table-hover` class adds a hover effect to rows, while the `table-primary` class distinguishes the table header.

Action buttons in the table rows vary by route. For the `customerlistforsummary` route, a "View Summary" button is displayed. For the `customerlistforedit` route, an "Edit" button is shown. For the `search_customer` route, both "Edit" and "View Summary" buttons are available, providing comprehensive management options.

**Workaround for Sorting in search_customer Route**

I chose to remove the sorting function for the table headings in the `search_customer` route. This decision was made because clicking the sortable table headings would initiate a GET request, redirecting back to the `search_customer` template and losing the context of the original search term. To maintain the functionality and user experience, I opted to keep the table headers as plain text in this specific route.

#### Customer Add Route ("/customeradd")

When designing the customer add route, I aimed to streamline the process of adding new customers using a consistent form. The `customer_form.html` template handles the form submission through a POST request, which adds the new customer to the database. Upon successful addition, the `success.html` template is rendered to confirm the action. This design ensures a uniform user experience across different tasks.

The `customer_form.html` template includes text inputs for customer details, with validation patterns to ensure correct data entry. The validation patterns include checks for alphabetic characters in names and basic email validation. Required fields are enforced to prevent incomplete form submissions.

By using a consistent form template for both adding and editing customers, the application maintains a clean and intuitive interface, making it easy for staff to manage customer information accurately. The confirmation provided by the `success.html` template ensures that the customer is added correctly and provides immediate feedback to the user.

#### Customer Edit Route ("/customeredit")

When designing the customer edit route, I aimed to streamline the process of updating existing customer information and adding new customers using the same form. The `customer_form.html` template is used for both adding new customers and updating existing ones, leveraging conditional logic (IF statements) to differentiate between the two actions.

A POST request handles the form submission, whether adding a new customer or updating an existing one. Upon successful completion, the `success.html` template is rendered to confirm the action. This design ensures a consistent and intuitive interface for staff when managing customer details.

Customers can be edited from the result of a customer search or by using the "Edit Customer" navigation item in the sidebar to locate the customer. This flexibility allows staff to quickly find and update customer information. When using the "Edit Customer" nav item, the application employs a sorting function in the `search_result.html` template, enabling staff to sort the list of customers by name, email, or phone. This feature enhances usability by allowing staff to efficiently navigate and find the specific customer they need to edit.

#### Customer List Summary Route ("/customerlistsummary")

When designing the customer list summary route, I aimed to provide an intuitive interface that allows staff to easily select a customer and view their summary report. The `/customerlistsummary` route ensures correct results with a suitable order and layout.

When users navigate to this route, the application retrieves a list of customers from the database and displays it using the `search_result.html` template. This template presents the customer list in a well-structured table format, making it easy for staff to find and select the desired customer.

**Conditional Logic for Displaying Results**

The template uses conditional logic to display different content based on the route. For the `/customerlistsummary` route, it shows a "Customer Summary Report" heading. The table headers are sortable links, enabling users to re-order the list as needed.

**Summary Report Display**

Clicking the "View Summary" button navigates to the `/customersummary` route, which uses the `customer_summary.html` template to display detailed information about the selected customer.

The summary report is formatted using Bootstrap classes like `table`, `table-hover`, and `table-primary` to enhance readability and usability. The `table-hover` class adds a hover effect to rows, while the `table-primary` class highlights the table header.

By considering the order and layout of elements, the summary report interface ensures staff can easily access and interpret the information, meeting the requirement for displaying correct results in a suitable manner.

### Navigation

Initially, I considered using a top navigation bar but chose a sidebar for its professional dashboard feel and better use of vertical space. The sidebar provides clear links to main features like Make Booking, Camper List, and Search Customer, improving accessibility and usability. It remains visible while navigating different sections, making it easier for users to switch between tasks. This choice ensures a consistent, organized interface suitable for a staff-facing application and allows for easy expansion as new features are added.

### Board Layout

I used a base template (`base.html`) with common elements like the header and navigation sidebar to create a uniform layout across all pages. Extending this base template in other templates ensures consistency in styling and simplifies template management. This approach creates a cohesive look and feel throughout the application, making it easier to maintain and navigate.

### Data Validation on Forms

I implemented HTML5 form validation features like `pattern`, `required`, `minlength`, and `maxlength` to ensure data integrity. For the phone number input, I set a minimum length of 1 and a maximum length of 12, assuming staff will carefully enter the complete number. The pattern attribute allows digits and an optional leading '+' sign for international numbers (`pattern="\+?[0-9]{1,12}"`).

For the first name and family name inputs, I set a minimum length of 2 alphabetic characters, a maximum length of 45 characters for the first name, and 60 characters for the family name. This decision is based on the assumption that these lengths are sufficient to accommodate common names. The pattern attribute enforces that only alphabetic characters are allowed, which helps maintain data consistency and prevents invalid input.

For email validation, I used a simple pattern that checks for the presence of the '@' symbol, ensuring a basic level of validity.

Other validation measures include marking all fields as required to prevent submission of incomplete forms.

### Form Elements

In the booking form (`booking_form.html`), a dropdown (select) is used to list customers, allowing staff to choose from existing customer records rather than typing in names manually. This minimizes the risk of typos and ensures data consistency. Similarly, radio buttons are used for selecting site occupancy, presenting clear and mutually exclusive options to the user, which helps in making accurate selections.

The assumption is that the customer and site data are already populated in the database, allowing the dropdown and radio button elements to function correctly.

### Flowchart

```plaintext
Routes and Templates Flow:

1. / (home.html)
2. /booking (datepicker.html -> booking_form.html -> success.html)
3. /campers (datepicker_camper.html -> camper_list.html)
4. /search_customer (search_customer.html -> search_result.html)
5. /customeredit (customer_form.html -> success.html)
6. /customeradd (customer_form.html -> success.html)
7. /customerlistsummary (search_result.html -> customer_summary.html)
8. /customerlistedit (search_result.html -> customer_form.html)
9. /customersummary (customer_summary.html)


```


## Part 2 - Database questions

### 1. What SQL statement creates the customer table and defines its fields/columns?

```sql
CREATE TABLE IF NOT EXISTS `customers` (
  `customer_id` INT NOT NULL AUTO_INCREMENT,
  `firstname` VARCHAR(45) NULL,
  `familyname` VARCHAR(60) NOT NULL,
  `email` VARCHAR(255) NULL,
  `phone` VARCHAR(12) NULL,
  PRIMARY KEY (`customer_id`));

```
### 2. Which line of SQL code sets up the relationship between the customer and booking tables? 

```sql
CONSTRAINT `customer`
    FOREIGN KEY (`customer`)
    REFERENCES `scg`.`customers` (`customer_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
```
This line is part of the CREATE TABLE statement for the bookings table. It defines a foreign key constraint named customer that links the customer column in the bookings table to the customer_id column in the customers table, establishing a relationship between the two tables.

### 3. Which lines of SQL code insert details into the sites table? 

```sql
INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('P1', '5');
INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('P4', '2');
INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('P2', '3');
INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('P5', '8');
INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('P3', '2');
INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('U1', '6');
INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('U2', '2');
INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('U3', '4');
INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('U4', '4');
INSERT INTO `sites` (`site_id`, `occupancy`) VALUES ('U5', '2');

```

### 4. Suppose that as part of an audit trail, the time and date a booking was added to the database needed to be recorded. What fields/columns would you need to add to which tables? Provide the table name, new column name and the data type. (Do not implement this change in your app.) 

- **Table Name:** **`bookings`**
- **New Column Name:** **`created_at`**
- **Data Type:** **`DATETIME`**

### 5. Suppose the ability for customers to make their own bookings was added. Describe two different changes that would be needed to the data model to implement this. (Do not implement these changes in your app.) 

Here are two significant changes:

#### **1. Add a User Authentication System:**

**New Table: `users`**

- **Table Name:** **`users`**
- **Columns:**
    - **`user_id`** INT NOT NULL AUTO_INCREMENT PRIMARY KEY
    - **`username`** VARCHAR(50) NOT NULL UNIQUE
    - **`password_hash`** VARCHAR(255) NOT NULL
    - **`email`** VARCHAR(255) NOT NULL UNIQUE
    - **`created_at`** DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    - **`updated_at`** DATETIME NULL ON UPDATE CURRENT_TIMESTAMP

**Purpose:**
This table will store user authentication details, such as usernames and hashed passwords, to manage customer logins and ensure secure access to the booking system.

**SQL statement:**

```jsx
CREATE TABLE IF NOT EXISTS `users` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(50) NOT NULL UNIQUE,
  `password_hash` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL UNIQUE,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`)
);

```

#### **2. Link Customers to User Accounts:**

**Modify Existing Table: `customers`**

- **Add New Column:** **`user_id`** INT NULL, FOREIGN KEY (**`user_id`**) REFERENCES **`users`** (**`user_id`**)

**Purpose:**
This change creates a link between the **`customers`** table and the **`users`** table. It allows each customer to be associated with a user account, enabling tracking and managing of customer-specific bookings.

**SQL statement:**

```jsx
ALTER TABLE `customers`
ADD COLUMN `user_id` INT NULL,
ADD CONSTRAINT `fk_user`
  FOREIGN KEY (`user_id`)
  REFERENCES `users` (`user_id`);

```

#### **Summary of Changes:**

1. **User Authentication Table:**
    - Create a new table **`users`** to store user authentication details, allowing customers to log in and make bookings.
2. **Link Customers to Users:**
    - Add a **`user_id`** column to the **`customers`** table to link customer records to user accounts, enabling user-specific actions and tracking.
