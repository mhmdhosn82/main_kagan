# Kagan Collection Management System

A comprehensive Python-based management software for the Kagan collection with a sleek glassmorphism UI. Integrates three business sections (Men's Salon, Cafe Bar, and Gamnet/Gaming Net) into a unified management and invoicing system.

## Features

### 🏢 Business Sections

#### Men's Salon
- Appointment booking with stylist selection
- Service registration (haircut, coloring, mask, etc.)
- Customer ratings and reviews
- Automatic commission calculation per service

#### Cafe Bar
- Menu management with categories
- Order processing and bill splitting
- Barista assignment per order
- Daily sales reports and popular items analysis

#### Gamnet (Gaming Net)
- Device management (PC, PlayStation, Xbox, VR)
- Session timers with automatic charge calculation
- Advance reservations
- Customer credit accounts
- Usage reports and peak hours analysis

### 💰 Invoice & Cashier
- Unified invoicing across all sections
- Multiple payment methods (Cash, Card, Wallet)
- Discount and campaign code application
- Digital invoice generation

### 👥 Employee Management
- Role-based employee records
- Attendance tracking with check-in/out
- Commission calculations
- Performance reports
- Automatic payroll calculations

### 👤 Customer Management
- Customer registration and profiles
- Purchase and service history
- Loyalty points system
- Digital wallet for payments
- Visit tracking

### 📢 Campaigns & Marketing
- Discount campaign creation
- Automatic SMS notifications
- Birthday greetings
- Inactive customer re-engagement
- Campaign analytics

### 📊 Reports & Analytics
- Sales reports (daily, weekly, monthly)
- Section performance comparison
- Customer statistics
- Employee performance metrics
- Revenue breakdowns

## Installation

### Requirements
- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/mhmdhosn82/main_kagan.git
cd main_kagan
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Usage

### First Launch
On first launch, the application will:
- Create a SQLite database (`kagan.db`)
- Initialize all necessary tables
- Load sample data (employees, services, menu items, devices)

### Navigation
- Use the sidebar to navigate between sections
- Dashboard shows quick overview and stats
- Each section has multiple tabs for different operations

### Common Workflows

#### Creating a Unified Invoice
1. Go to "Invoices" section
2. Enter customer phone number
3. Add items from Salon, Cafe, or Gamnet
4. Apply campaign codes if available
5. Create invoice
6. Process payment in the Payment tab

#### Booking a Salon Appointment
1. Go to "Salon" section
2. Navigate to "Appointments" tab
3. Enter customer details
4. Select date, time, stylist, and service
5. Click "Book Appointment"

#### Starting a Gaming Session
1. Go to "Gamnet" section
2. Navigate to "Sessions" tab
3. Enter customer phone
4. Select available device
5. Click "Start Session"
6. When finished, select device and click "End Session"

## Architecture

### Modular Structure
```
main_kagan/
├── main.py                 # Main application entry point
├── database.py            # Database schema and operations
├── ui_utils.py            # UI components and glassmorphism theme
├── salon_section.py       # Salon management module
├── cafe_section.py        # Cafe Bar management module
├── gamnet_section.py      # Gaming Net management module
├── employee_section.py    # Employee management module
├── customer_section.py    # Customer management module
├── invoice_section.py     # Invoice and cashier module
├── campaign_section.py    # Campaigns and marketing module
├── reports_section.py     # Reports and analytics module
└── requirements.txt       # Python dependencies
```

### Database
- Uses SQLite for data persistence
- Normalized schema with foreign key relationships
- Automatic commission tracking
- Transaction support

### UI Framework
- Built with customtkinter for modern, native-looking UI
- Glassmorphism design with dark theme
- Responsive layouts
- Tab-based navigation within sections

## Technologies

- **Python 3.8+**: Core programming language
- **customtkinter**: Modern UI framework with glassmorphism support
- **SQLite**: Embedded database
- **Pillow**: Image processing
- **Matplotlib**: Charts and visualizations
- **ReportLab**: PDF invoice generation
- **QRCode**: QR code generation for digital coupons

## Future Enhancements

- [ ] Web-based customer panel
- [ ] Mobile app integration
- [ ] SMS gateway integration
- [ ] Card reader integration
- [ ] Advanced analytics with charts
- [ ] Multi-language support (full Vazir font integration)
- [ ] Cloud backup
- [ ] Multi-location support

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is licensed under the MIT License.

## Contact

For questions or support, please contact the repository owner.