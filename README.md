# GreenSteps 🌱

GreenSteps is an eco-habit tracking application built with Streamlit. It allows users to log their daily eco-friendly actions, track their impact over time, and contribute to a global community effort to promote sustainability.

## Features

- **User Authentication**: Register and log in securely to track your eco-habits.
- **Eco-Habit Logging**: Log daily eco-friendly actions such as carpooling, skipping meat, or using public transport.
- **Eco-Points System**: Earn points for each eco-action and track your progress.
- **Personal Impact Dashboard**: Visualize your daily and total eco-points with interactive charts.
- **Global Community Impact**: See how the global community is contributing to sustainability.
- **Streaks and Badges**: Earn badges for consistent contributions (e.g., 7-day streak, 30-day streak).

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Required Python libraries: `streamlit`, `sqlite3`, `pandas`, `plotly`, `streamlit-authenticator`

Install the dependencies using:

```bash
pip install streamlit pandas plotly streamlit-authenticator
```

# Running the Application
Clone the repository and navigate to the project directory.

Run the Streamlit app:
```
streamlit run app.py
```
Open the app in your browser at http://localhost:8501.

# Database Setup
The application uses an SQLite database (greensteps.db) to store user data and logs. The database tables are automatically created when the app is run for the first time.

# Usage
1. Register: Create an account using your email and password.
2. Log In: Access your personalized dashboard after logging in.
3. Log Eco-Actions: Select eco-friendly habits you completed today and submit your log.
4. Track Progress: View your daily eco-points, total points, and streaks.
5. Explore Global Impact: Check the global community's eco-points trend.

# Eco Habits & Points
| Habit                  | Points |
|------------------------|--------|
| Carpooling 🚗          | 1.5    |
| Reused Container ♻️    | 1.0    |
| Skipped Meat 🍃         | 2.0    |
| Used Public Transport 🚲| 1.5    |
| No-Plastic Day 🛍️      | 2.5    |
| Others (Custom) 📝      | 1.0    |

# Contributing
Contributions are welcome! Feel free to fork the repository and submit a pull request.

# Acknowledgments
1. Streamlit for the interactive UI framework.
2. Plotly for data visualization.
3. SQLite for database management.

----
Start tracking your eco-habits today and make a difference! 🌍 

