# Kagan Collection Management System - Enhanced Version

## Overview

This is a comprehensive enterprise-level management software for the Kagan Collection, integrating three business sections (Men's Salon, Cafe Bar, and Gaming Net) with advanced features including Persian RTL support, SMS integration, inventory management, and multi-user authentication.

## 🆕 New Features (Enhanced Version)

### 1. **Multi-User Authentication System**
- Secure login with username and password
- Password hashing using SHA-256
- Default admin user: `admin` / `admin123`
- Session management with role-based access control
- Three user roles: Admin, Manager, Employee

### 2. **Persian RTL Support**
- Full Persian/Farsi translation
- Right-to-left (RTL) layout support
- Bilingual interface (Persian/English)
- Persian calendar (Jalali) support for date selection
- RTL-aware UI components

### 3. **SMS Panel Integration**
- Support for multiple SMS providers:
  - Twilio (International)
  - Kavenegar (Iranian)
  - Ghasedak (Iranian)
- **Automatic SMS Features:**
  - Survey SMS sent 24 hours after service
  - Birthday greeting SMS on customer birthdays
  - Reactivation SMS for inactive customers (monthly)
- **Manual SMS Features:**
  - Send to single customer or groups
  - Filter by active/inactive customers
  - Pre-defined message templates
  - Character counter
  - SMS history tracking with delivery status

### 4. **Inventory Management**
- Product/stock management for all sections
- SKU tracking
- Unit cost and selling price
- Reorder level alerts
- Low stock notifications
- Stock by section (Salon, Cafe, Gamnet)
- Supplier linkage

### 5. **Supplier Management**
- Supplier database with contact information
- Purchase order tracking
- Supplier-product relationships
- Active/inactive supplier status

### 6. **Expense Tracking**
- Comprehensive expense categorization:
  - Rent
  - Utilities
  - Salaries
  - Supplies
  - Maintenance
  - Marketing
  - Other
- Payment method tracking
- Receipt number recording
- Expense filtering by category
- Date-based expense reports

### 7. **Advanced Settings Panel**
- **Appearance Settings:**
  - Theme selection (Dark/Light mode)
  - Language selection (Persian/English)
  - Font configuration
- **Business Settings:**
  - Default currency
  - Tax rate
  - Business hours
  - Contact information
  - Loyalty points configuration
- **SMS Configuration:**
  - SMS provider selection
  - API credentials management
- **Backup & Restore:**
  - Manual database backup
  - Database restore from backup
  - Backup directory configuration
  - Auto-backup scheduling
  - Backup history tracking
- **User Management (Admin only):**
  - Add new users
  - Assign roles
  - View all users
  - User activity tracking

### 8. **Enhanced Reporting System**
- **Date Range Filters:**
  - Daily
  - Weekly
  - Monthly
  - Quarterly
  - Yearly
  - Custom date range
- **Persian Calendar Support:**
  - Jalali/Shamsi calendar for Persian users
  - Date conversion between Gregorian and Jalali
- **Advanced Reports:**
  - Revenue breakdown by section
  - Top services/products
  - Payment method analysis
  - Customer analytics and segmentation
  - Employee performance metrics
  - Profit & Loss statements
  - Inventory status reports
- **Customer Segmentation:**
  - VIP customers (high spenders)
  - Regular customers (active)
  - At-risk customers (30-90 days inactive)
  - Lost customers (90+ days inactive)

### 9. **Customer Loyalty Program**
- Points accumulation system
- Points redemption tracking
- Configurable points rate
- Transaction history
- Loyalty analytics

### 10. **Database Enhancements**
- 10+ new database tables
- Normalized schema with foreign keys
- Transaction support
- Comprehensive data tracking
- Automatic backup system

## 🚀 Installation

### Requirements
- Python 3.8 or higher
- pip package manager
- Operating System: Windows, macOS, or Linux

### Setup Instructions

1. **Clone the repository:**
```bash
git clone https://github.com/mhmdhosn82/main_kagan.git
cd main_kagan
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
python main.py
```

## 📝 Default Login Credentials

On first launch, use these credentials:
- **Username:** `admin`
- **Password:** `admin123`
- **Role:** Administrator (full access)

⚠️ **Important:** Change the default password after first login!

## 🔧 Configuration

### SMS Provider Setup

1. Go to **Settings** → **SMS Configuration**
2. Select your SMS provider (Twilio, Kavenegar, or Ghasedak)
3. Enter your API credentials
4. Save settings

**Note:** SMS features require valid API credentials from your chosen provider.

### Database Backup

1. Go to **Settings** → **Backup & Restore**
2. Configure backup directory
3. Enable automatic backups (optional)
4. Set backup frequency (daily/weekly/monthly)
5. Click "Backup Now" for manual backup

### Language Selection

1. Go to **Settings** → **Appearance**
2. Select language (Persian/English)
3. Restart application for full effect

## 📊 Database Schema

### New Tables (Enhanced Version)

1. **users** - User authentication and roles
2. **settings** - Application configuration
3. **inventory_items** - Product inventory
4. **suppliers** - Supplier information
5. **purchase_orders** - Purchase order tracking
6. **purchase_order_items** - PO line items
7. **expenses** - Business expenses
8. **loyalty_transactions** - Customer loyalty points
9. **sms_history** - SMS tracking and history
10. **notifications** - System notifications
11. **backup_history** - Backup tracking
12. **payment_transactions** - Payment gateway logs

## 🎯 Usage Guide

### Creating a New User (Admin Only)

1. Navigate to **Settings** → **Users** tab
2. Fill in user details:
   - Username (unique)
   - Password
   - Full Name
   - Role (admin/manager/employee)
3. Click "Add User"

### Sending SMS

**Manual SMS:**
1. Go to **SMS Panel** → **Manual SMS**
2. Choose recipient(s):
   - Single customer (enter phone)
   - All customers
   - Active customers only
   - Inactive customers only
3. Select or create message template
4. Click "Send SMS"

**Automatic SMS:**
1. Go to **Settings** → **SMS Configuration**
2. Configure SMS provider
3. Automatic SMS will be sent based on triggers:
   - Survey SMS: 24 hours after service
   - Birthday SMS: On customer's birthday
   - Reactivation SMS: Monthly to inactive customers

### Managing Inventory

**Adding Products:**
1. Go to **Inventory** → **Add Product**
2. Fill in product details:
   - Name, Category, Section
   - SKU, Quantity, Unit
   - Unit Cost, Selling Price
   - Reorder Level
   - Supplier
3. Click "Add"

**Checking Low Stock:**
1. Go to **Inventory** → **Low Stock Alerts**
2. View items below reorder level
3. Take action to reorder

### Tracking Expenses

1. Go to **Expenses** → **Add Expense**
2. Fill in expense details:
   - Category (rent, utilities, salaries, etc.)
   - Description
   - Amount
   - Date
   - Payment method
   - Receipt number
3. Click "Add"

### Generating Reports

**Sales Report:**
1. Go to **Reports** → **Sales Reports**
2. Select time period (daily/weekly/monthly/quarterly/yearly/custom)
3. For custom range, enter start and end dates
4. Enable "Use Persian Calendar" if needed
5. Click "Generate Report"

**Advanced Analytics:**
1. Go to **Reports** → **Advanced Analytics**
2. Choose report type:
   - Customer Analytics & Segmentation
   - Profit & Loss Statement
   - Employee Performance Report
   - Inventory Status & Alerts

## 🔐 Role-Based Permissions

### Admin
- Full system access
- User management
- Settings configuration
- All reports and analytics
- Database backup/restore

### Manager
- View all data
- Create/edit transactions
- Generate reports
- Limited settings access
- No user management

### Employee
- View assigned sections
- Create transactions
- Basic reports
- No settings access
- No user management

## 🌐 Multi-Language Support

The application supports:
- **Persian (فارسی)** - Default language with RTL support
- **English** - Full English translation

Switch languages in Settings → Appearance → Language

## 📱 SMS Templates

Pre-defined templates available:
- **Birthday:** Birthday wishes with special offer
- **Promotional:** Discount codes and special offers
- **Reactivation:** Message for inactive customers
- **Custom:** Create your own messages

All templates support customer name personalization.

## 💾 Backup & Restore

### Automatic Backup
- Configured in Settings → Backup & Restore
- Frequency: Daily, Weekly, or Monthly
- Backups stored in configured directory

### Manual Backup
1. Go to Settings → Backup & Restore
2. Click "Backup Now"
3. Backup file created with timestamp

### Restore
1. Go to Settings → Backup & Restore
2. Click "Restore from Backup"
3. Select backup file
4. Confirm restoration
5. **Restart application**

## 🐛 Troubleshooting

### Common Issues

**Login fails:**
- Verify username and password
- Check caps lock
- Use default credentials: admin/admin123

**SMS not sending:**
- Verify SMS provider is configured
- Check API credentials
- Ensure internet connectivity
- Review SMS history for error messages

**Backup fails:**
- Check backup directory exists
- Verify write permissions
- Ensure sufficient disk space

**Database errors:**
- Restore from backup
- Check file permissions
- Contact support

## 📚 Dependencies

- customtkinter >= 5.2.0
- pillow >= 10.0.0
- matplotlib >= 3.7.0
- reportlab >= 4.0.0
- qrcode >= 7.4.0
- python-bidi >= 0.4.2
- arabic-reshaper >= 3.0.0
- jdatetime >= 4.1.0
- requests >= 2.31.0

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

For questions or support:
- Open an issue on GitHub
- Contact: mhmdhosn82

## 🎉 Acknowledgments

This enhanced version includes contributions for:
- Persian language support
- Enterprise-level features
- SMS integration
- Advanced analytics
- Multi-user security

---

**Version:** 2.0 (Enhanced)  
**Last Updated:** October 2025  
**Developer:** mhmdhosn82
