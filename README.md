# 🐕 Sniff Job - Job Fraud Detection Dashboard

A modern dark-themed web application built with Streamlit and SQLite that helps users analyze job postings for potential fraud.

## Features

### 🔍 Job Post Analyzer
- **URL Analysis**: Analyze job postings from any job board (LinkedIn, Indeed, etc.)
- **Manual Entry**: Manual job posting input (coming soon)
- **AI-Powered Detection**: Simulated AI analysis with confidence scores
- **Result Classification**: Legit, Suspicious, or Fraud detection

### 📊 Dashboard
- **Dark Theme**: Modern navy-blue dark theme with responsive design
- **Sidebar Navigation**: Intuitive navigation with icons
- **User Profile**: Token system and subscription management
- **Notifications**: Real-time notification system

### 📁 File Management
- **CV Upload**: Upload and manage multiple resumes
- **Sniff History**: Track all job analyses
- **File Storage**: Secure file storage system

### 👤 User Management
- **Session-Based Login**: Secure authentication system
- **Profile Management**: User settings and preferences
- **Subscription Plans**: Free and premium tiers

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone or download the project files**
   ```bash
   # If using git
   git clone <repository-url>
   cd fraudjobdetection
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Access the application**
   - Open your web browser
   - Navigate to `http://localhost:8501`

## Demo Account

For quick testing, use the built-in demo account:
- **Username**: `demo`
- **Password**: `demo123`

Or click the "Use Demo Account" button on the login screen.

## Project Structure

```
fraudjobdetection/
├── app.py              # Main Streamlit application
├── database.py         # SQLite database operations
├── requirements.txt    # Python dependencies
├── README.md          # Project documentation
├── uploads/           # User uploaded files (auto-created)
└── sniffjob.db        # SQLite database (auto-created)
```

## Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `password`: Hashed password
- `plan`: Subscription plan (Free/Premium)
- `tokens`: User tokens for API calls
- `created_at`: Account creation timestamp
- `last_login`: Last login timestamp

### Resumes Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `file_name`: Original filename
- `file_path`: Storage path
- `upload_date`: Upload timestamp

### Job History Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `job_url`: Analyzed job URL
- `job_title`: Extracted job title
- `company`: Extracted company name
- `result`: Analysis result (Legit/Fraud/Suspicious)
- `confidence_score`: AI confidence percentage
- `analysis_details`: Detailed analysis
- `timestamp`: Analysis timestamp

### Notifications Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `message`: Notification message
- `is_read`: Read status
- `created_at`: Notification timestamp

## Usage Guide

### Analyzing a Job Posting

1. **Login** to your account or use the demo account
2. **Navigate** to the Dashboard (default page)
3. **Enter** a job URL in the input field
4. **Click** "🔍 Sniff It" to analyze
5. **View** the analysis results with confidence scores

### Uploading a Resume

1. **Go to** "Upload CV" from the sidebar
2. **Choose** your resume file (PDF/DOC/DOCX)
3. **Upload** and view confirmation
4. **Manage** your resumes from the same page

### Viewing History

1. **Navigate** to "Sniff History" in the sidebar
2. **Browse** all your previous job analyses
3. **Filter** by status or date
4. **Click** on URLs to revisit job postings

## Customization

### Theme Customization
Edit the CSS variables in `app.py` under the `load_css()` function:

```css
:root {
    --primary-bg: #0f172a;      /* Main background */
    --secondary-bg: #1e293b;    /* Card backgrounds */
    --accent-blue: #3b82f6;     /* Primary accent */
    --accent-hover: #2563eb;    /* Hover state */
    --text-primary: #f1f5f9;    /* Main text */
    --text-secondary: #94a3b8;  /* Secondary text */
}
```

### Adding New Pages
1. Create a new render function in `app.py`
2. Add the page to the navigation menu in `render_sidebar()`
3. Add routing logic in the `main()` function

## Security Features

- **Password Hashing**: SHA-256 encryption for user passwords
- **Session Management**: Secure session-based authentication
- **Input Validation**: URL validation and sanitization
- **File Upload Security**: Restricted file types and secure storage

## Technologies Used

- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: SQLite
- **Styling**: Custom CSS with dark theme
- **Authentication**: Session-based login system

## Future Enhancements

- [ ] Real AI/ML integration for job analysis
- [ ] Email notifications for analysis results
- [ ] Advanced search and filtering
- [ ] Export functionality for history
- [ ] Mobile-responsive design improvements
- [ ] Multi-language support
- [ ] API integration with job boards
- [ ] Advanced analytics dashboard

## Troubleshooting

### Common Issues

1. **Database Error**: Ensure `sqlite3` is available (built-in with Python)
2. **File Upload Issues**: Check if `uploads/` directory has write permissions
3. **Port Conflicts**: Change Streamlit port using `streamlit run app.py --server.port 8502`
4. **CSS Not Loading**: Refresh the browser cache (Ctrl+F5)

### Getting Help

If you encounter issues:
1. Check the terminal for error messages
2. Ensure all dependencies are installed correctly
3. Verify Python version compatibility
4. Check file permissions for the project directory

## License

This project is for educational and demonstration purposes. Please ensure compliance with job board terms of service when using URL analysis features.

## Contributing

Feel free to submit issues and enhancement requests to improve the application.
