"""
Errors and exceptions for slackr
"""


class AccessError(Exception):
    """
    Exception that is raised when accessing something that you do not have sufficient permissions for
    """
