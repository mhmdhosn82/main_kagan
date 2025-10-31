# Kagan Collection Management System - User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Features Guide](#features-guide)
5. [Database Structure](#database-structure)
6. [Troubleshooting](#troubleshooting)

## Introduction

The Kagan Collection Management System is a comprehensive business management solution designed for multi-service establishments. It seamlessly integrates three distinct business sections:

- **Men's Salon**: Professional hair and grooming services
- **Cafe Bar**: Food and beverage service
- **Gamnet**: Gaming center with various gaming platforms

### Key Benefits
- Unified invoicing across all services
- Automatic commission tracking
- Customer loyalty and wallet system
- Campaign and marketing automation
- Comprehensive reporting and analytics
- Modern glassmorphism UI

## Installation

### System Requirements
- Python 3.8 or higher
- 500 MB free disk space
- 2 GB RAM minimum
- Display for GUI (1280x720 or higher recommended)

### Step-by-Step Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/mhmdhosn82/main_kagan.git
   cd main_kagan
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify Installation**
   ```bash
   python test_database.py
   ```

4. **Run Demo (Optional)**
   ```bash
   python demo.py
   ```

5. **Launch Application**
   ```bash
   python main.py
   ```

## Quick Start

### First Time Setup

When you first launch the application:

1. The system will automatically create a SQLite database (`kagan.db`)
2. Sample data will be loaded including:
   - 5 sample employees (stylists, baristas, gaming manager)
   - 5 salon services
   - 8 cafe menu items
   - 6 gaming devices
   - 1 active campaign

### Basic Workflow

#### 1. Register a New Customer
- Navigate to **Customers** section
- Click **Customers** tab
- Enter customer details (name, phone, birthdate)
- Click **Register Customer**

#### 2. Book a Salon Appointment
- Navigate to **Salon** section
- Click **Appointments** tab
- Enter customer phone
- Select date, time, stylist, and service
- Click **Book Appointment**

#### 3. Create a Unified Invoice
- Navigate to **Invoices** section
- Click **Create Invoice** tab
- Enter customer phone
- Add items from different sections:
  - Salon service (e.g., Haircut - $25)
  - Cafe item (e.g., Coffee - $4.50)
  - Gaming session (e.g., 2 hours PC - $10)
- Apply campaign code if available
- Click **Create Invoice**

#### 4. Process Payment
- Go to **Payment** tab
- Enter invoice ID
- Select payment method (Cash/Card/Wallet)
- Click **Process Payment**

## Features Guide

### Dashboard
The dashboard provides a quick overview:
- Today's revenue
- Active customers count
- Pending appointments
- Active gaming sessions
- Recent activity

### Salon Management

#### Appointments
- **Booking**: Schedule appointments with specific stylists
- **Time Management**: View all appointments for the day
- **Status Tracking**: Monitor pending, completed, or cancelled appointments

#### Services
- **Service Menu**: Manage available services (haircut, coloring, etc.)
- **Pricing**: Set prices and duration for each service
- **Commissions**: Configure commission rates per service

#### Service Records
- **Track Services**: Record completed services
- **Ratings**: Collect customer satisfaction ratings (1-5 stars)
- **Reviews**: Capture customer feedback

### Cafe Bar Management

#### Menu Management
- **Categories**: Organize items by Drinks, Food, Desserts, Snacks
- **Descriptions**: Add detailed item descriptions
- **Availability**: Mark items as available or unavailable

#### Orders
- **Create Orders**: Add multiple items to an order
- **Bill Splitting**: Split bills among multiple people
- **Barista Assignment**: Assign specific barista to each order

#### Reports
- **Daily Sales**: View sales for current day
- **Popular Items**: Identify best-selling menu items

### Gamnet Management

#### Device Management
- **Add Devices**: Register gaming devices (PC, PlayStation, Xbox, VR)
- **Rates**: Set hourly rates per device
- **Availability**: Track which devices are in use

#### Sessions
- **Start Session**: Begin gaming session for a customer
- **Timers**: Automatic time tracking
- **End Session**: Calculate charges based on duration

#### Reservations
- **Advance Booking**: Allow customers to reserve devices
- **Schedule Management**: View upcoming reservations

#### Reports
- **Daily Usage**: Track total gaming time and revenue
- **Peak Hours**: Identify busiest times
- **Device Performance**: Compare revenue across devices

### Employee Management

#### Employee Records
- **Add Employees**: Register staff with roles and sections
- **Base Salary**: Set monthly base salary
- **Commission Rates**: Configure commission percentages

#### Attendance
- **Check-In/Out**: Track employee attendance
- **Late Tracking**: Monitor punctuality
- **Work History**: View attendance records

#### Reports
- **Performance**: View services performed and customer ratings
- **Commissions**: Track earned commissions
- **Payroll**: Calculate total earnings (salary + commissions)

### Customer Management

#### Registration
- **Customer Profiles**: Store customer information
- **Contact Details**: Phone numbers for communication
- **Birthdate**: Enable birthday promotions

#### History
- **Service History**: View all past salon services
- **Purchase History**: See cafe orders and gaming sessions
- **Total Spending**: Track lifetime customer value

#### Loyalty & Wallet
- **Loyalty Points**: Reward frequent customers
- **Digital Wallet**: Allow prepaid balances
- **Point Redemption**: Use points for discounts

### Campaign Management

#### Create Campaigns
- **Discount Campaigns**: Set percentage-based discounts
- **Campaign Codes**: Generate unique codes
- **Duration**: Set start and end dates

#### Messaging
- **Birthday Greetings**: Automatic birthday messages
- **Inactive Customers**: Re-engage customers who haven't visited
- **Campaign Notifications**: Announce new promotions

#### Analytics
- **Campaign Usage**: Track how many times codes are used
- **Customer Engagement**: Monitor active vs inactive customers

### Reports & Analytics

#### Sales Reports
- **Daily**: Current day's revenue
- **Weekly**: Last 7 days performance
- **Monthly**: Current month statistics

#### Section Performance
- **Salon**: Services performed, top stylists
- **Cafe**: Orders, popular items
- **Gamnet**: Sessions, device utilization
- **Comparison**: Revenue distribution across sections

#### Overall Statistics
- **Today's Overview**: Customers served, appointments, revenue
- **Customer Stats**: Total, active, new customers
- **Employee Performance**: Top performers by commissions

## Database Structure

### Core Tables

#### Employees
- Stores staff information, roles, and commission rates
- Tracks active/inactive status and last work date

#### Customers
- Customer profiles with contact information
- Loyalty points and wallet balance
- Visit tracking for engagement analysis

#### Salon Services
- Service catalog with pricing
- Duration and commission configuration

#### Cafe Menu
- Menu items with categories
- Descriptions and pricing

#### Gamnet Devices
- Gaming device inventory
- Hourly rates and availability status

#### Invoices
- Unified invoicing across all sections
- Payment method tracking
- Campaign code application

#### Campaigns
- Marketing campaign definitions
- Discount percentages and codes
- Active date ranges

### Relationships
- **Invoices** link to **Customers**
- **Service Records** link to **Employees**, **Customers**, and **Services**
- **Orders** link to **Customers** and **Employees**
- **Sessions** link to **Devices** and **Customers**

## Troubleshooting

### Common Issues

#### Application Won't Start
**Problem**: `ModuleNotFoundError: No module named 'tkinter'`
**Solution**: 
- On Ubuntu/Debian: `sudo apt-get install python3-tk`
- On macOS: tkinter comes with Python
- On Windows: Reinstall Python with tkinter support

#### Database Issues
**Problem**: Database locked or corrupted
**Solution**:
```bash
# Backup existing database
mv kagan.db kagan.db.backup

# Restart application to create fresh database
python main.py
```

#### Display Issues
**Problem**: Window too small or elements overlapping
**Solution**: Adjust window size in `main.py`:
```python
self.geometry("1600x1000")  # Change from 1400x900
```

### Performance Optimization

For large datasets:
1. Regular database cleanup of old records
2. Archive old invoices to separate database
3. Limit report date ranges

### Support

For issues or questions:
1. Check the GitHub Issues page
2. Review the documentation
3. Run `python demo.py` to verify installation

## Best Practices

### Daily Operations
1. Check dashboard at start of day
2. Review pending appointments
3. Update device availability
4. Process any pending invoices

### Weekly Tasks
1. Review sales reports
2. Check employee attendance
3. Update menu items based on popularity
4. Send re-engagement messages to inactive customers

### Monthly Tasks
1. Generate comprehensive reports
2. Calculate employee commissions
3. Review and update campaigns
4. Backup database

## Advanced Features

### Unified Invoicing Example
Create an invoice combining services from all sections:

```
Customer: Mohammad Rezaei
Items:
  [Salon] Haircut - $25.00
  [Cafe] Cappuccino - $4.50
  [Cafe] Club Sandwich - $8.00
  [Gamnet] 2 hours PC gaming - $10.00
  
Subtotal: $47.50
Campaign (WELCOME20): -$9.50
Total: $38.00
```

### Commission Tracking
Automatic commission calculation:
- Stylist performs $100 haircut with 15% commission = $15 earned
- Barista serves $50 in orders with 12% commission = $6 earned
- All commissions tracked in employee_commissions table

### Customer Loyalty
Automatic loyalty point calculation:
- Customer spends $100 = 100 loyalty points
- Points can be redeemed for discounts
- Wallet balance available for quick payments

## Conclusion

The Kagan Collection Management System provides a complete solution for managing multi-service businesses. With integrated sections, unified invoicing, and comprehensive reporting, it streamlines operations and improves customer experience.

For updates and new features, check the GitHub repository regularly.
