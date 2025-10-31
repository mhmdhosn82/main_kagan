# Technical Documentation - Kagan Collection Management System

## Architecture Overview

### Design Pattern: Modular MVC Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     main.py                              │
│              (Main Application Controller)               │
└──────────────────┬──────────────────────────────────────┘
                   │
         ┌─────────┴─────────┐
         │                   │
    ┌────▼────┐         ┌───▼────┐
    │UI Utils │         │Database│
    │(View)   │         │(Model) │
    └────┬────┘         └───┬────┘
         │                  │
         └────┬─────────────┘
              │
    ┌─────────┴──────────────────┐
    │     Section Modules        │
    │  (Controllers + Views)     │
    ├────────────────────────────┤
    │ • salon_section.py         │
    │ • cafe_section.py          │
    │ • gamnet_section.py        │
    │ • employee_section.py      │
    │ • customer_section.py      │
    │ • invoice_section.py       │
    │ • campaign_section.py      │
    │ • reports_section.py       │
    └────────────────────────────┘
```

## Module Breakdown

### Core Modules

#### 1. `database.py`
**Purpose**: Data persistence layer

**Key Components**:
- `Database` class: Manages SQLite connection and operations
- Table schema creation
- CRUD operations wrapper
- Transaction management

**Tables**:
- `employees` - Staff records
- `customers` - Customer profiles
- `salon_services` - Service catalog
- `salon_appointments` - Appointment scheduling
- `salon_service_records` - Completed services
- `cafe_menu` - Food/drink items
- `cafe_orders` - Order records
- `cafe_order_items` - Order line items
- `gamnet_devices` - Gaming hardware
- `gamnet_sessions` - Gaming sessions
- `gamnet_reservations` - Device bookings
- `invoices` - Unified billing
- `campaigns` - Marketing campaigns
- `attendance` - Employee check-in/out
- `employee_commissions` - Commission tracking
- `messages` - Notification queue

#### 2. `ui_utils.py`
**Purpose**: UI theming and reusable components

**Key Components**:
- Color scheme definition (glassmorphism theme)
- Custom widget classes:
  - `GlassFrame` - Styled container
  - `GlassButton` - Styled button
  - `GlassEntry` - Styled text input
  - `GlassLabel` - Styled text label
  - `GlassScrollableFrame` - Scrollable container
- Font configuration
- Helper functions for UI creation

**Theme Colors**:
```python
COLORS = {
    'primary': '#6366f1',       # Indigo
    'secondary': '#8b5cf6',     # Purple
    'background': '#0f172a',    # Dark blue
    'surface': '#1e293b',       # Surface
    'text': '#f1f5f9',          # Light text
    'success': '#10b981',       # Green
    'warning': '#f59e0b',       # Orange
    'error': '#ef4444',         # Red
}
```

#### 3. `main.py`
**Purpose**: Application entry point and main controller

**Key Components**:
- `KaganManagementApp` class: Main application window
- Navigation sidebar
- Section management (lazy loading)
- Dashboard with quick stats
- Sample data initialization

**Navigation Flow**:
```
Dashboard → Section Selection → Tab Navigation → Actions
```

### Section Modules

Each section follows the same pattern:

```python
class SectionName:
    def __init__(self, parent):
        self.parent = parent
        self.frame = GlassScrollableFrame(parent)
        self.setup_ui()
    
    def setup_ui(self):
        # Create tabs and layouts
        pass
    
    def get_frame(self):
        return self.frame
```

#### `salon_section.py`
**Features**:
- Appointment booking with stylist selection
- Service catalog management
- Service recording with ratings
- Automatic commission calculation

**Key Methods**:
- `book_appointment()` - Create new appointment
- `add_service()` - Add service to catalog
- `record_service()` - Log completed service with rating

#### `cafe_section.py`
**Features**:
- Menu management by category
- Order creation with multiple items
- Bill splitting functionality
- Sales reporting

**Key Methods**:
- `add_menu_item()` - Add item to menu
- `add_to_order()` - Add item to current order
- `complete_order()` - Finalize and save order
- `show_daily_sales()` - Display sales report

#### `gamnet_section.py`
**Features**:
- Device inventory management
- Session timing with auto-calculation
- Advance reservations
- Usage analytics

**Key Methods**:
- `add_device()` - Register new gaming device
- `start_session()` - Begin gaming session
- `end_session()` - End session and calculate charge
- `make_reservation()` - Create device reservation

#### `employee_section.py`
**Features**:
- Employee registration with roles
- Attendance tracking (check-in/out)
- Commission reports
- Performance analytics

**Key Methods**:
- `add_employee()` - Register new employee
- `check_in()` / `check_out()` - Attendance tracking
- `show_performance()` - Generate performance report

#### `customer_section.py`
**Features**:
- Customer registration
- Purchase history tracking
- Loyalty points management
- Digital wallet

**Key Methods**:
- `register_customer()` - Create customer profile
- `view_history()` - Show purchase history
- `add_points()` / `add_to_wallet()` - Manage rewards

#### `invoice_section.py`
**Features**:
- Unified cross-section invoicing
- Campaign code application
- Multiple payment methods
- Payment processing

**Key Methods**:
- `add_to_invoice()` - Add item to invoice
- `apply_campaign()` - Apply discount code
- `create_invoice()` - Generate invoice
- `process_payment()` - Handle payment

#### `campaign_section.py`
**Features**:
- Campaign creation with codes
- Automated messaging
- Customer segmentation
- Campaign analytics

**Key Methods**:
- `create_campaign()` - Create new campaign
- `send_birthday_messages()` - Auto birthday greetings
- `send_inactive_messages()` - Re-engagement messaging

#### `reports_section.py`
**Features**:
- Sales reports (daily/weekly/monthly)
- Section performance comparison
- Customer statistics
- Employee performance metrics

**Key Methods**:
- `show_daily_sales()` - Daily revenue report
- `compare_sections()` - Cross-section analysis
- `show_customer_stats()` - Customer metrics

## Database Schema Details

### Key Relationships

```sql
-- Invoice to Customer (Many-to-One)
invoices.customer_id → customers.id

-- Service Record to Employee (Many-to-One)
salon_service_records.stylist_id → employees.id

-- Order to Barista (Many-to-One)
cafe_orders.barista_id → employees.id

-- Session to Device (Many-to-One)
gamnet_sessions.device_id → gamnet_devices.id

-- Commission to Employee (Many-to-One)
employee_commissions.employee_id → employees.id
```

### Indexing Strategy

Recommended indexes for performance:
```sql
CREATE INDEX idx_customer_phone ON customers(phone);
CREATE INDEX idx_invoice_date ON invoices(invoice_date);
CREATE INDEX idx_appointment_date ON salon_appointments(appointment_date);
CREATE INDEX idx_employee_section ON employees(section);
```

## Data Flow Examples

### Booking Workflow
```
User Input → salon_section.book_appointment()
    ↓
Validate customer (create if needed)
    ↓
Insert into salon_appointments table
    ↓
Refresh appointments display
```

### Invoice Workflow
```
Add items from sections → invoice_section.add_to_invoice()
    ↓
Apply discount code → invoice_section.apply_campaign()
    ↓
Create invoice → invoice_section.create_invoice()
    ↓
Process payment → invoice_section.process_payment()
    ↓
Update customer stats (loyalty points, wallet, total spent)
```

### Commission Calculation
```
Service completed → record_service()
    ↓
Calculate: price × (commission_rate / 100)
    ↓
Insert into salon_service_records
    ↓
Insert into employee_commissions
```

## Extension Points

### Adding New Sections

To add a new business section:

1. Create `new_section.py`:
```python
from ui_utils import *
from database import db

class NewSection:
    def __init__(self, parent):
        self.parent = parent
        self.frame = GlassScrollableFrame(parent)
        self.setup_ui()
    
    def setup_ui(self):
        # Build UI
        pass
    
    def get_frame(self):
        return self.frame
```

2. Update `main.py`:
```python
from new_section import NewSection

# In KaganManagementApp.setup_ui():
nav_items.append(("New Section", self.show_new_section))

# Add method:
def show_new_section(self):
    self.show_section('new_section', NewSection)
```

3. Add database tables in `database.py` if needed

### Adding New Reports

In `reports_section.py`:
```python
def show_new_report(self):
    self.report_text.delete('1.0', 'end')
    
    # Query database
    data = db.fetchall("SELECT ...")
    
    # Format and display
    for row in data:
        self.report_text.insert('end', f"{row['column']}\n")
```

## Performance Considerations

### Database Optimization
- Use parameterized queries (prevents SQL injection)
- Batch inserts for bulk operations
- Regular VACUUM for SQLite maintenance
- Consider adding indexes for frequently queried columns

### UI Optimization
- Lazy loading of sections (only create when accessed)
- Limit query results with LIMIT clause
- Use pagination for large datasets
- Cache static data (e.g., employee list)

### Memory Management
- Close database connections properly
- Clear large text widgets periodically
- Limit in-memory data structures

## Security Considerations

### Current Implementation
- SQLite with file-based storage
- No network exposure
- Local authentication (OS-level)

### Production Recommendations
1. Add user authentication system
2. Implement role-based access control
3. Encrypt sensitive data (customer info, financial data)
4. Add audit logging
5. Regular backups
6. Input validation and sanitization

## Testing

### Unit Tests
Run database tests:
```bash
python test_database.py
```

### Integration Tests
Run full demo:
```bash
python demo.py
```

### Manual Testing
1. Launch application
2. Navigate through all sections
3. Create test data
4. Verify calculations
5. Check reports

## Deployment

### Standalone Executable
Use PyInstaller:
```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

### Requirements
- Python 3.8+
- customtkinter >= 5.2.0
- pillow >= 10.0.0
- matplotlib >= 3.7.0
- reportlab >= 4.0.0
- qrcode >= 7.4.0

## Maintenance

### Database Backup
```bash
# Manual backup
cp kagan.db kagan_backup_$(date +%Y%m%d).db

# Automated backup script
sqlite3 kagan.db ".backup kagan_backup.db"
```

### Log Management
Consider adding logging:
```python
import logging

logging.basicConfig(
    filename='kagan.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

## Future Enhancements

1. **Web Interface**: Flask/Django web application
2. **Mobile App**: React Native or Flutter
3. **Cloud Sync**: PostgreSQL with cloud hosting
4. **SMS Integration**: Twilio for notifications
5. **Payment Gateway**: Stripe/PayPal integration
6. **Advanced Analytics**: Machine learning for predictions
7. **Multi-location**: Support for multiple branches
8. **API**: RESTful API for third-party integrations

## Contributing

### Code Style
- Follow PEP 8 guidelines
- Use docstrings for functions/classes
- Keep functions focused and small
- Comment complex logic

### Pull Request Process
1. Fork repository
2. Create feature branch
3. Write tests
4. Update documentation
5. Submit pull request

## License

MIT License - See LICENSE file for details

## Contact

For technical questions or contributions, contact the repository maintainer.
