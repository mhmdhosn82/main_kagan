# Quick Setup Guide - Kagan Collection Management System

## Installation Steps

### 1. Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning the repository)

### 2. Install Dependencies

```bash
# Clone the repository
git clone https://github.com/mhmdhosn82/main_kagan.git
cd main_kagan

# Install required Python packages
pip install -r requirements.txt
```

### 3. First Run

```bash
# Run the application
python main.py
```

### 4. Login

On first launch, use these default credentials:
- **Username:** `admin`
- **Password:** `admin123`

The login screen will appear automatically.

### 5. Initial Configuration

After logging in:

1. **Change Default Password** (Recommended)
   - Go to Settings → Users
   - Add a new admin user with a secure password
   - Delete or disable the default admin account

2. **Configure Language**
   - Go to Settings → Appearance
   - Select Persian (فارسی) or English
   - Restart the application

3. **Set Business Details**
   - Go to Settings → Business
   - Enter your currency, tax rate, business hours
   - Add contact information

4. **Setup SMS (Optional)**
   - Go to Settings → SMS Configuration
   - Choose SMS provider (Twilio, Kavenegar, or Ghasedak)
   - Enter API credentials
   - Test SMS functionality

5. **Configure Backup**
   - Go to Settings → Backup & Restore
   - Set backup directory
   - Enable automatic backups
   - Perform initial backup

## Features Overview

### User Roles
- **Admin:** Full system access
- **Manager:** View and edit, limited settings
- **Employee:** Basic operations only

### Main Sections
- **Dashboard:** Overview and quick stats
- **Salon:** Appointment booking, services
- **Cafe Bar:** Menu, orders, billing
- **Gamnet:** Device management, gaming sessions
- **Invoices:** Unified invoicing system
- **Employees:** Staff management
- **Customers:** Customer database, loyalty
- **Inventory:** Stock management, alerts
- **Suppliers:** Supplier database, purchase orders
- **Expenses:** Expense tracking
- **SMS Panel:** Manual and automatic SMS
- **Campaigns:** Marketing campaigns
- **Reports:** Advanced analytics and reports
- **Settings:** System configuration

## Common Tasks

### Add a New User
1. Go to Settings → Users (admin only)
2. Enter username, password, full name
3. Select role (admin/manager/employee)
4. Click "Add User"

### Create an Invoice
1. Go to Invoices → Create Invoice
2. Enter customer phone number
3. Add items from Salon/Cafe/Gamnet
4. Apply campaign code if applicable
5. Create invoice
6. Process payment

### Send SMS
1. Go to SMS Panel → Manual SMS
2. Choose recipients (single/group)
3. Select or write message
4. Click "Send SMS"

### Generate Report
1. Go to Reports → Sales Reports
2. Select time period
3. Choose date range if custom
4. Click "Generate Report"

### Backup Database
1. Go to Settings → Backup & Restore
2. Click "Backup Now"
3. Wait for confirmation
4. Backup file saved in configured directory

## Troubleshooting

### Application won't start
- Check Python version: `python --version` (must be 3.8+)
- Reinstall dependencies: `pip install -r requirements.txt`
- Check for error messages

### Can't login
- Use default credentials: admin/admin123
- Check caps lock is off
- Ensure database file exists (kagan.db)

### Database error
- Delete kagan.db (will recreate with defaults)
- Or restore from backup

### SMS not working
- Verify SMS provider is configured
- Check API credentials are correct
- Ensure internet connection
- Check SMS history for error messages

## SMS Provider Setup

### Twilio (International)
1. Sign up at twilio.com
2. Get Account SID and Auth Token
3. Get a Twilio phone number
4. Enter credentials in Settings → SMS Configuration

### Kavenegar (Iranian)
1. Sign up at kavenegar.com
2. Get API key from panel
3. Enter API key in Settings → SMS Configuration

### Ghasedak (Iranian)
1. Sign up at ghasedak.me
2. Get API key from panel
3. Enter API key in Settings → SMS Configuration

## Persian Calendar

The system supports Persian (Jalali/Shamsi) calendar for date selection in reports.

To use Persian calendar:
1. Go to Reports
2. Enable "Use Persian Calendar (Jalali)"
3. Dates will be displayed in Persian calendar format

## Data Migration

To migrate data from old system:
1. Backup current database
2. Use database tools to import data into new tables
3. Verify data integrity
4. Test thoroughly before production use

## Support

For help:
- Read ENHANCED_README.md for detailed documentation
- Check existing issues on GitHub
- Create new issue for bugs or feature requests

## Security Best Practices

1. **Change default password immediately**
2. **Use strong passwords** for all users
3. **Regular backups** (daily recommended)
4. **Limit admin access** to trusted users only
5. **Keep SMS API keys secure**
6. **Review user access** regularly
7. **Monitor expense entries** for fraud
8. **Update software** when new versions available

## Next Steps

After setup:
1. Add employees
2. Add customers
3. Configure services and menu
4. Add gaming devices
5. Set up inventory items
6. Add suppliers
7. Start using the system!

---

**Need Help?** Open an issue on GitHub or contact support.
