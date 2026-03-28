#  Odoo Real Estate Module

This repository contains an **Odoo 18 Real Estate module** built as part of my technical training and extended with real-world business logic and workflow automation.

---

##  Features Implemented

### Property Management

* Create and manage properties with detailed information
* Track property lifecycle using states:

  * New
  * Offer Received
  * Sold

---

### Property Types & Tags

* Categorize properties using property types
* Assign multiple tags for better classification

---

### Property Offers

* Create and manage multiple offers per property
* Track offer status:

  * Pending
  * Accepted
  * Refused

---

### Offer Approval Workflow

* Accept or refuse offers via action buttons
* Enforced business rules:

  * Only **one offer can be accepted per property**
  * All other offers are automatically refused upon acceptance
* Automatic updates on acceptance:

  * Property marked as **Sold**
  * Selling price recorded
  * Buyer assigned

---

###  Smart Insights

* Smart buttons to display:

  * Number of offers per property type
  * Number of properties per property type

---

###  Chatter Integration

* Integrated Odoo chatter for tracking:

  * Property updates
  * Offer activities
* Provides audit trail and communication history

---

### Data Validation

#### Offer Validation

* Prevents offers lower than existing offers
* Ensures competitive and consistent data

#### Availability Date Validation

* Prevents setting availability date in the past using:

  * `@api.onchange` (user warning)
  * `@api.constrains` (backend enforcement)

---

### Sales Information

* Track buyer and salesperson for each property
* Automatically updated during offer acceptance

---

## 🛠️ Tech Stack

* Odoo 18
* Python (Odoo ORM)
* XML (Views & Actions)
* PostgreSQL

---

## What I Learned

* Designing and extending Odoo modules with real business logic
* Implementing workflows across related models
* Enforcing data integrity using constraints and validations
* Using Odoo ORM methods (`filtered`, `mapped`, `write`)
* Building dynamic UI behavior in Odoo 17+ (without `attrs`)
* Debugging XML and Python issues using Odoo logs

---

##  Challenges Faced

* View crashes due to XML structure errors
* Migration changes in Odoo 17+ (removal of `attrs` and `states`)
* Access rights issues from `ir.model.access.csv`
* Handling One2many relationships in views and logic
* Ensuring data consistency across related models

---

## Screenshots

*Add screenshots for:*

* Property form view
* Offer workflow (Accept/Refuse buttons)
* Smart buttons (statistics)
* Chatter section

---

## Status

 Actively improved with additional business logic and workflow enhancements.

---

## Future Improvements

* Role-based access control (Agent vs Manager)
* Email notifications for offer updates
* CRM & Sales module integration
* Reporting dashboard (KPIs & analytics)

---

## 👨‍💻 Author

Developed by [Cayleb]

---



