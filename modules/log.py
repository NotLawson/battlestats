## Logging module for the application
# This module handles logging for the application. It sets up the logger and provides functions to log messages at different levels.
# It saves the logs to the database and prints to the console. 
# Each log contains the following information:
# - ID: Unique identifier for the log entry
# - Timestamp: When the log entry was created
# - Level: The severity level of the log entry (e.g., INFO, WARNING, ERROR)
# - Message: The log message
# - User ID: The ID of the user associated with the log entry (if applicable)
# - function: The function where the log entry was created (if applicable)
# - module: The module where the log entry was created (if applicable)
# - request: The request details associated with the log entry (if applicable)


# (not implemented yet, using the default Flask logger for now)