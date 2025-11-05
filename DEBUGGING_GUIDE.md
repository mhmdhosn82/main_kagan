# Debugging Guide for Kagan Management Software

This guide explains how to use the enhanced error handling and logging features to debug issues with the application.

## Error Handling Features

The application now includes comprehensive error handling and logging to help identify issues:

### 1. Logging System

All application activities are logged to files in the `logs/` directory. Log files are named by date (e.g., `kagan_20251105.log`).

**Location**: `logs/kagan_YYYYMMDD.log`

### 2. What Gets Logged

The application logs the following events:

#### Application Lifecycle
- Application startup
- User login attempts (success and failure)
- UI initialization steps
- Sample data initialization
- Window visibility events
- Application shutdown

#### Error Events
- All exceptions with full stack traces
- Failed operations with context
- Warning messages for non-critical issues

### 3. Log Levels

- **DEBUG**: Detailed information for diagnosis (e.g., "Creating sidebar navigation")
- **INFO**: General informational messages (e.g., "User logged in successfully")
- **WARNING**: Warning messages for non-critical issues (e.g., "Continuing application startup despite sample data error")
- **ERROR**: Error messages with exception details

## How to Debug Login Issues

If the main window doesn't appear after login, follow these steps:

### Step 1: Check the Console Output

When you run the application from the command line:
```bash
python3 main.py
```

You'll see log messages printed to the console. Look for error messages or exceptions.

### Step 2: Check the Log File

Navigate to the `logs/` directory and open the most recent log file:
```bash
cat logs/kagan_YYYYMMDD.log
```

Look for:
- **ERROR** level messages indicating what went wrong
- Stack traces showing where the error occurred
- The last successful operation before the failure

### Step 3: Identify the Problem

Common issues and their log signatures:

#### UI Initialization Failure
```
INFO - Setting up user interface
ERROR - Error in setup_ui: ...
```
**Likely cause**: Problem with UI components or missing dependencies

#### Sample Data Initialization Failure
```
INFO - Initializing sample data
ERROR - Error initializing sample data: ...
WARNING - Continuing application startup despite sample data error
```
**Likely cause**: Database issue (this won't prevent the app from starting)

#### Section Display Failure
```
INFO - Showing section: dashboard
ERROR - Error showing dashboard: ...
```
**Likely cause**: Problem loading a specific section

#### Database Connection Issue
```
ERROR - Error getting setting 'theme': ...
```
**Likely cause**: Database connection or schema issue

### Step 4: Error Dialogs

For critical errors that prevent the application from starting, you'll see an error dialog with:
- The error type and message
- A note to check the log files for details

## Example Log Output

### Successful Startup
```
2025-11-05 21:41:00,000 - KaganApp - INFO - Starting Kagan Management Software
2025-11-05 21:41:00,100 - KaganApp - INFO - === Starting Kagan Management Application ===
2025-11-05 21:41:00,200 - KaganApp - INFO - Initializing login screen
2025-11-05 21:41:00,300 - KaganApp - INFO - Login screen initialized successfully
2025-11-05 21:41:05,000 - KaganApp - DEBUG - Login attempt started
2025-11-05 21:41:05,100 - KaganApp - DEBUG - Attempting to authenticate user: admin
2025-11-05 21:41:05,200 - KaganApp - INFO - User 'admin' authenticated successfully
2025-11-05 21:41:05,300 - KaganApp - INFO - User logged in successfully: admin
2025-11-05 21:41:05,400 - KaganApp - DEBUG - Configuring main window
2025-11-05 21:41:05,500 - KaganApp - DEBUG - Setting theme from settings
2025-11-05 21:41:05,600 - KaganApp - INFO - Setting up user interface
2025-11-05 21:41:05,700 - KaganApp - DEBUG - Creating sidebar navigation
2025-11-05 21:41:06,000 - KaganApp - INFO - UI setup completed successfully
2025-11-05 21:41:06,100 - KaganApp - INFO - Initializing sample data
2025-11-05 21:41:06,200 - KaganApp - INFO - Sample data already exists, skipping initialization
2025-11-05 21:41:06,300 - KaganApp - INFO - Making main window visible
2025-11-05 21:41:06,400 - KaganApp - INFO - Main window is now visible and focused
2025-11-05 21:41:06,500 - KaganApp - INFO - Entering main event loop
```

### Failed Startup (Example)
```
2025-11-05 21:41:00,000 - KaganApp - INFO - Starting Kagan Management Software
2025-11-05 21:41:00,100 - KaganApp - INFO - === Starting Kagan Management Application ===
2025-11-05 21:41:05,300 - KaganApp - INFO - User logged in successfully: admin
2025-11-05 21:41:05,600 - KaganApp - INFO - Setting up user interface
2025-11-05 21:41:05,700 - KaganApp - ERROR - Error in setup_ui: AttributeError: 'NoneType' object has no attribute 'grid'
Traceback (most recent call last):
  File "main.py", line 123, in setup_ui
    self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
AttributeError: 'NoneType' object has no attribute 'grid'
2025-11-05 21:41:05,800 - KaganApp - ERROR - Error during application initialization: AttributeError: ...
```

## Troubleshooting Common Issues

### Issue: No log file created
**Solution**: Check that the application has write permissions in its directory

### Issue: Log file exists but is empty
**Solution**: The application may have crashed before logging started. Check console output.

### Issue: Window doesn't appear but no errors in log
**Solution**: The application may be running in the background. Check:
1. If the window is minimized
2. If the window is behind other windows
3. If there's a window manager issue (try maximizing or bringing to front)

## Getting Help

When reporting issues, please include:
1. The full log file from the `logs/` directory
2. Steps to reproduce the issue
3. Your operating system and Python version
4. Any error dialogs that appeared

## Technical Details

### Logging Implementation
- **Module**: `app_logger.py`
- **Logger Name**: `KaganApp`
- **Log Format**: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`
- **Handlers**: FileHandler (to log file) and StreamHandler (to console)

### Error Handling Strategy
1. **Non-Critical Errors**: Logged but don't stop the application (e.g., sample data errors)
2. **Critical Errors**: Logged, shown to user via dialog, and may stop the application
3. **Section Errors**: Logged and shown to user, with fallback to dashboard
4. **Login Errors**: Logged and shown in the login screen

### Files Modified
- `main.py`: Added error handling to all major methods
- `auth.py`: Added error handling to login process
- `app_logger.py`: New logging module
- `.gitignore`: Updated to exclude log files
