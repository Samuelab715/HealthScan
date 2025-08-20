# Medical Information Collection System

## Overview

This is a Flask-based web application designed to collect and display medical information through an interactive form. The system captures patient data including personal information, underlying diseases, allergies, vital signs, and pregnancy status, then provides a summary view of the submitted information. The application serves as a medical assessment tool with a clean, user-friendly interface optimized for healthcare data collection.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templating with Flask for server-side rendering
- **Styling**: Custom CSS with modern, clean design focused on medical form usability
- **Form Handling**: HTML forms with JavaScript for dynamic field toggling (pregnancy field visibility based on gender selection)
- **User Experience**: Flash messaging system for form validation feedback and error handling

### Backend Architecture
- **Framework**: Flask web framework with lightweight, minimal setup
- **Application Structure**: Simple two-route architecture:
  - `/` - Displays the medical information collection form
  - `/submit` - Processes form submissions and renders summary page
- **Data Processing**: Form data extraction and basic validation without persistent storage
- **Session Management**: Flask sessions with configurable secret key from environment variables
- **Logging**: Python logging configured at DEBUG level for development

### Data Storage Solutions
- **Current Implementation**: No persistent data storage - data only exists during request lifecycle
- **Data Handling**: In-memory processing of form submissions with immediate display in summary view
- **Session Storage**: Temporary flash messages stored in Flask sessions

### Authentication and Authorization
- **Current State**: No authentication or authorization implemented
- **Security**: Basic session secret key configuration from environment variables

## External Dependencies

### Core Dependencies
- **Flask**: Web framework for routing, templating, and request handling
- **Python Standard Library**: 
  - `os` for environment variable access
  - `logging` for application logging

### Frontend Dependencies
- **No External Libraries**: Pure HTML, CSS, and minimal JavaScript
- **Font Stack**: System fonts (-apple-system, BlinkMacSystemFont, Segoe UI, Roboto)

### Deployment Configuration
- **Host Configuration**: Configured to run on `0.0.0.0:5000` for container compatibility
- **Environment Variables**: 
  - `SESSION_SECRET` for Flask session security (falls back to development default)

### Missing Integrations
- **Database**: No database integration currently implemented
- **External APIs**: No third-party API integrations
- **Cloud Services**: No cloud service dependencies
- **Email/Notifications**: No notification systems integrated