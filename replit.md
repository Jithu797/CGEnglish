English Communication Course Builder
Overview
This is a Flask-based web application that generates educational content for English communication courses using OpenAI's API. The application provides a user-friendly interface for creating various types of educational materials including multiple choice questions, cheat sheets, drag & drop activities, textual questions, and listening exercises.

User Preferences
Preferred communication style: Simple, everyday language.

System Architecture
Frontend Architecture
Framework: HTML templates with Bootstrap for responsive UI
Styling: Bootstrap with Replit dark theme + custom CSS for enhanced user experience
JavaScript: Vanilla JavaScript for client-side interactions and API communication
Icons: Font Awesome for consistent iconography
Backend Architecture
Framework: Flask (Python web framework)
API Integration: OpenAI client for content generation
File Processing: openpyxl for Excel file generation and manipulation
Cross-Origin Support: Flask-CORS for handling cross-origin requests
Template System
Base Template: Shared layout with navigation, Bootstrap integration, and responsive design
Dashboard: Main interface for topic selection and API key configuration
Generator: Content creation interface with customizable parameters
Key Components
1. Content Generation Engine
Purpose: Generate educational content using OpenAI's API
Features: Supports multiple content types (MCQ, cheat sheets, activities)
Customization: Adjustable temperature settings for creativity control
2. Topic Management System
Configuration: JavaScript-based topic definitions with prompts and metadata
Flexibility: Easy addition of new topics through topics.js file
Categorization: Organized by communication skills (business, conversation, etc.)
3. Excel Export Functionality
Library: openpyxl for creating formatted Excel files
Styling: Professional formatting with fonts, colors, and alignment
Output: Downloadable Excel files for offline use
4. API Key Management
Security: Client-side storage of API keys (not server-side)
Flexibility: Dynamic OpenAI client initialization
Privacy: Keys never sent to application servers
Data Flow
User Input: API key configuration and content generation parameters
Topic Selection: Choose from predefined communication topics
Content Generation: Send prompts to OpenAI API with user preferences
Processing: Parse and format generated content
Export Options: Display content in web interface or generate Excel files
Download: Provide formatted files for offline use
External Dependencies
Required APIs
OpenAI API: Content generation service (requires user-provided API key)
Python Libraries
flask: Web framework
flask-cors: Cross-origin resource sharing
openai: OpenAI API client
openpyxl: Excel file manipulation
logging: Application logging
Frontend Libraries
Bootstrap: UI framework with dark theme
Font Awesome: Icon library
jQuery (implied): For Bootstrap functionality
Deployment Strategy
Development Environment
Entry Point: main.py runs Flask development server
Configuration: Debug mode enabled for development
Host/Port: Configured for 0.0.0.0:5000 (container-friendly)
Environment Variables
SESSION_SECRET: Flask session security (defaults to dev key)
OpenAI API keys managed client-side (not environment variables)
File Structure
/
├── app.py              # Main Flask application
├── main.py             # Application entry point
├── templates/          # HTML templates
│   ├── base.html       # Base template with navigation
│   ├── dashboard.html  # Topic selection interface
│   └── generator.html  # Content generation interface
└── static/             # Static assets
    ├── css/            # Custom styles
    └── js/             # Client-side JavaScript
Key Architectural Decisions
Client-side API Key Storage: Chosen for security and privacy - keys never reach the server
Template-based UI: Provides consistent styling and easy maintenance
Modular Topic System: JavaScript configuration allows easy content expansion
Excel Export: Provides offline usability for educational content
Dark Theme: Professional appearance suitable for extended use
The application is designed to be lightweight, secure, and easily extensible for additional English communication topics and content types.